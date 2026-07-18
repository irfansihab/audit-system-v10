"""Chat AI berbasis pengetahuan wiki (RAG).

Cikal bakal chatbot WA/Telegram: endpoint stateless-ish yang menerima
pertanyaan + riwayat, MENGAMBIL konteks relevan dari wiki (vault catatan +
regulasi kunci terkurasi), lalu menjawab HANYA berbasis konteks itu
(anti-halusinasi: bila tak ada di wiki → nyatakan tidak tahu). Mengembalikan
jawaban + daftar sumber supaya bisa ditelusuri.

Reusable: karena input = {question, history} dan output = {answer, sources},
webhook WA/Telegram nanti tinggal memanggil endpoint yang sama.
"""
from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.config import get_settings
from app.models import Role, User
from app.tools.wiki_tools import vault_search, vault_get_page

router = APIRouter(prefix="/chat", tags=["chat"])

_MAX_CTX_NOTES = 4          # jumlah catatan vault yang di-embed penuh
_PER_NOTE_CHARS = 1600      # potong tiap catatan
_MAX_HISTORY = 8            # batasi giliran riwayat yang dikirim ke model


class ChatTurn(BaseModel):
    role: str = Field(..., description="'user' atau 'assistant'")
    content: str


class ChatAskPayload(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)
    history: list[ChatTurn] = Field(default_factory=list)


def _search_curated_wiki(question: str, top: int = 3) -> list[tuple[str, str, str]]:
    """Cari file .md terkurasi di knowledge/wiki (pattern temuan + konteks) yang
    cocok dengan istilah pertanyaan. Return [(label, path_rel, isi_terpotong)]."""
    s = get_settings()
    roots = [s.wiki_path / "temuan-patterns", s.wiki_path / "konteks", s.wiki_path / "templates"]
    terms = [t for t in re.split(r"\W+", question.lower()) if len(t) >= 4]
    if not terms:
        return []
    scored: list[tuple[int, str, Path]] = []
    for root in roots:
        if not root.is_dir():
            continue
        for f in root.rglob("*.md"):
            if f.name.lower() == "readme.md":
                continue
            try:
                txt = f.read_text(encoding="utf-8")
            except OSError:
                continue
            low = txt.lower()
            score = sum(low.count(t) for t in terms) + 3 * sum(f.stem.lower().count(t) for t in terms)
            if score > 0:
                scored.append((score, f.stem, f))
    scored.sort(key=lambda x: -x[0])
    out = []
    for _sc, stem, f in scored[:top]:
        try:
            out.append((stem, str(f.relative_to(s.wiki_path)), f.read_text(encoding="utf-8")[:1500]))
        except OSError:
            continue
    return out


def _collect_context(question: str) -> tuple[str, list[dict]]:
    """Ambil konteks wiki relevan + daftar sumber."""
    parts: list[str] = []
    sources: list[dict] = []

    # 0) Wiki terkurasi (pattern temuan + konteks + template) — inti pengetahuan tim.
    for label, path_rel, isi in _search_curated_wiki(question, top=3):
        parts.append(f"### Wiki terkurasi: {label} ({path_rel})\n{isi}")
        sources.append({"jenis": "pattern", "nama": label, "summary": path_rel})

    # 1) Catatan vault paling relevan (full-text scoring).
    hits = vault_search(question, limit=8)
    for r in (hits.get("results") or [])[:_MAX_CTX_NOTES]:
        name = r.get("name")
        if not name:
            continue
        try:
            page = vault_get_page(name)
        except Exception:  # noqa: BLE001
            continue
        body = (page.get("content") or page.get("body") or "")[:_PER_NOTE_CHARS]
        if not body.strip():
            continue
        parts.append(f"### Catatan wiki: {name}\n{body}")
        sources.append({"jenis": "catatan", "nama": name, "summary": (r.get("summary") or "")[:160]})

    # 2) Regulasi kunci terkurasi (anti-halusinasi sitasi).
    s = get_settings()
    reg = s.wiki_path / "konteks" / "regulasi-kunci.md"
    if reg.is_file():
        try:
            txt = reg.read_text(encoding="utf-8")
            # ambil bagian yang menyebut kata kunci pertanyaan bila ada, else awal.
            q_terms = [t for t in question.lower().split() if len(t) >= 4]
            idx = next((txt.lower().find(t) for t in q_terms if txt.lower().find(t) >= 0), -1)
            snippet = txt[max(0, idx - 400): idx + 1200] if idx >= 0 else txt[:1500]
            parts.append(f"### Regulasi kunci (terkurasi):\n{snippet}")
            sources.append({"jenis": "regulasi", "nama": "regulasi-kunci", "summary": "daftar regulasi & pasal terverifikasi"})
        except OSError:
            pass

    return ("\n\n".join(parts) or "(tidak ada konteks wiki yang cocok)"), sources


@router.post("/ask")
async def chat_ask(
    payload: ChatAskPayload,
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Jawab pertanyaan bebas berbasis pengetahuan wiki. Semua role boleh."""
    from app.llm_extract import resolve_anthropic_key
    key = resolve_anthropic_key()
    if not key:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            "API key AI belum dikonfigurasi — chat tidak tersedia.")

    konteks, sources = _collect_context(payload.question)

    system = (
        "Anda asisten pengetahuan untuk auditor Inspektorat II Kementerian Komunikasi dan Digital. "
        "Jawab HANYA berdasarkan KONTEKS WIKI yang diberikan. Bila informasi tidak ada di konteks, "
        "katakan jujur bahwa hal itu belum ada di basis pengetahuan wiki dan jangan mengarang "
        "(anti-halusinasi). Jangan mengarang nomor pasal/regulasi. Jawab ringkas, dalam Bahasa "
        "Indonesia, dan bila relevan sebutkan nama catatan/regulasi sumbernya. "
        f"\n\n=== KONTEKS WIKI ===\n{konteks}\n=== AKHIR KONTEKS ==="
    )
    msgs = []
    for t in payload.history[-_MAX_HISTORY:]:
        role = "assistant" if t.role == "assistant" else "user"
        msgs.append({"role": role, "content": t.content[:4000]})
    msgs.append({"role": "user", "content": payload.question})

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            system=system,
            messages=msgs,
        )
        answer = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, f"Gagal menjawab via AI: {e}")

    return {"answer": answer, "sources": sources, "n_sumber": len(sources)}
