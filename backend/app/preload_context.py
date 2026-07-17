"""Pre-load konteks bundle untuk agen AT/KT — Prioritas 1 peningkatan kualitas.

Sebelum agen mulai analisis/susun temuan, sistem otomatis tarik konteks dari
4 sumber dan disusun jadi satu file markdown `_PRELOAD/context-bundle.md`.
Agen baca file ini di langkah awal (lewat tool `read_preload_context`) supaya
mulai dengan **tangan penuh**, bukan kosong.

4 sumber konteks:
1. **Vault organisasi** (llm-wiki) — catatan kaya per Direktorat, riwayat BPK,
   profil vendor. Pencarian by keyword obyek penugasan.
2. **Pattern temuan terkurasi** — pattern wiki utk skill penugasan (top severity
   first, max 8 pattern).
3. **Konteks pendukung** — pola-temuan-berulang, glossary, regulasi-kunci.
4. **Riwayat penugasan serupa** — catatan W3 writeback (`pengawasan-*.md`) di
   vault yg cocok dgn skill + obyek similarity.

Tidak ada panggilan LLM. Deterministik, cepat (~1-2 detik), file-based.
Caller tinggal panggil `build_preload_bundle(penugasan)` lalu simpan.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app import knowledge_browse
from app.config import get_settings
from app.tools.wiki_tools import (
    _available_skills,
    _parse_frontmatter,
    _patterns_dir,
    _scan_pattern_files,
    vault_get_page,
    vault_search,
)

settings = get_settings()


# ---------------------------------------------------------------------------
# Helper — extract keywords dari obyek penugasan utk pencarian vault
# ---------------------------------------------------------------------------

_STOPWORDS_ID = {
    "dan", "atau", "atas", "di", "ke", "dari", "untuk", "yang", "dengan",
    "pada", "oleh", "dalam", "ini", "itu", "akan", "telah", "sudah",
    "ta", "tahun", "anggaran", "periode", "tahap", "fase",
    "kementerian", "kemkomdigi", "komdigi", "kominfo",
    "ditjen", "direktorat", "dit", "sub", "satker", "satuan", "kerja", "unit",
    "reviu", "audit", "pengawasan",
    "the", "of", "a",
}

_WORD_RE = re.compile(r"[a-z0-9]+")


def _extract_keywords(text: str, top_n: int = 6) -> list[str]:
    """Tokenize lowercase + buang stopword + ambil top_n by frekuensi/order."""
    if not text:
        return []
    tokens = _WORD_RE.findall(text.lower())
    out: list[str] = []
    seen: set[str] = set()
    for t in tokens:
        if len(t) < 4 or t in _STOPWORDS_ID:
            continue
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
        if len(out) >= top_n:
            break
    return out


# ---------------------------------------------------------------------------
# Sumber 1: Vault organisasi (llm-wiki)
# ---------------------------------------------------------------------------

def _bundle_vault_notes(obyek: str, max_pages: int = 4) -> dict:
    """Cari catatan vault relevan dgn obyek penugasan + tarik isi top match."""
    keywords = _extract_keywords(obyek, top_n=6)
    if not keywords:
        return {"keywords": [], "notes": [], "skip_reason": "no keywords from obyek"}

    query = " ".join(keywords)
    res = vault_search(query, limit=max_pages * 2)
    if not res.get("configured"):
        return {"keywords": keywords, "notes": [], "skip_reason": "vault tidak dikonfigurasi (APP_VAULT_PATH kosong)"}
    results = res.get("results") or []

    notes_out: list[dict] = []
    for r in results[:max_pages]:
        name = r.get("name") or ""
        page = vault_get_page(name)
        if not page.get("found"):
            continue
        notes_out.append({
            "name": name,
            "section": r.get("section") or "",
            "summary": r.get("summary") or "",
            "content": (page.get("content") or "")[:6000],  # cap supaya bundle tidak meledak
        })
    return {"keywords": keywords, "notes": notes_out}


# ---------------------------------------------------------------------------
# Sumber 2: Pattern wiki untuk skill
# ---------------------------------------------------------------------------

_SEV_RANK = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "": 9}


def _bundle_patterns(skill: str, max_patterns: int = 8) -> dict:
    """Ambil pattern wiki terkurasi untuk skill, urut by severity desc."""
    files = _scan_pattern_files(skill)
    items: list[dict] = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, body = _parse_frontmatter(content)
        items.append({
            "id": str(meta.get("id", f.stem)),
            "judul": str(meta.get("judul", "")),
            "kategori": str(meta.get("kategori", "")),
            "severity": str(meta.get("severity", "")).upper(),
            "kriteria_baku": str(meta.get("kriteria_baku", "")),
            "tags": meta.get("tags", []) if isinstance(meta.get("tags"), list) else [],
            "body_excerpt": body[:1500] if body else "",
        })
    items.sort(key=lambda x: (_SEV_RANK.get(x["severity"], 9), x["id"]))
    return {"skill": skill, "total_available": len(items), "top": items[:max_patterns]}


# ---------------------------------------------------------------------------
# Sumber 3: Konteks pendukung (pola-berulang, glossary, regulasi)
# ---------------------------------------------------------------------------

def _bundle_konteks() -> dict:
    """Baca konteks pendukung dari wiki tim — anti-halusinasi.

    3 file inti + regulasi tambahan yang dikelola lewat UI Knowledge >
    Kriteria Pengawasan (`konteks/regulasi/*.md`, mis. hasil upload dokumen).
    Regulasi tambahan di-cap per file DAN total supaya bundle tidak meledak
    saat koleksinya tumbuh.
    """
    konteks_dir = settings.wiki_path / "konteks"
    out: dict[str, str] = {}
    for kategori in ("pola-temuan-berulang", "glossary-komdigi", "regulasi-kunci"):
        f = konteks_dir / f"{kategori}.md"
        if not f.exists():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        # buang frontmatter bila ada
        _, body = _parse_frontmatter(text)
        out[kategori] = body[:4000]  # cap

    reg_dir = konteks_dir / "regulasi"
    if reg_dir.is_dir():
        total_cap = 6000  # total budget utk seluruh regulasi tambahan
        parts: list[str] = []
        used = 0
        for f in sorted(reg_dir.glob("*.md")):
            if used >= total_cap:
                parts.append(f"_(+ regulasi lain terpotong — lihat wiki konteks/regulasi/{f.name} dst.)_")
                break
            try:
                _, body = _parse_frontmatter(f.read_text(encoding="utf-8"))
            except OSError:
                continue
            piece = body.strip()[:1500]
            parts.append(piece)
            used += len(piece)
        if parts:
            out["regulasi-tambahan"] = "\n\n---\n\n".join(parts)
    return out


# ---------------------------------------------------------------------------
# Sumber 4: Riwayat penugasan serupa (catatan W3 writeback di vault)
# ---------------------------------------------------------------------------

def _bundle_writeback_history(skill: str, obyek: str, top_n: int = 3) -> list[dict]:
    """Tarik catatan `pengawasan-*.md` di vault yg related skill+obyek."""
    try:
        items = knowledge_browse.suggest_context_from_writeback(skill=skill, obyek=obyek, top_n=top_n)
    except Exception:
        return []
    # Tarik isi singkat tiap catatan
    out: list[dict] = []
    for it in items:
        name = (it.get("nama_file") or "").removesuffix(".md")
        page = vault_get_page(name)
        if not page.get("found"):
            continue
        out.append({
            "nama_file": it.get("nama_file"),
            "judul": it.get("judul") or "",
            "jumlah_temuan": it.get("jumlah_temuan") or 0,
            "similarity": it.get("similarity") or 0.0,
            "content": (page.get("content") or "")[:3000],
        })
    return out


# ---------------------------------------------------------------------------
# Komposisi bundle markdown
# ---------------------------------------------------------------------------

def _format_bundle(
    *,
    penugasan_kode: str,
    obyek: str,
    skill: str,
    vault: dict,
    patterns: dict,
    konteks: dict,
    writeback: list[dict],
) -> str:
    """Susun bundle markdown utk dibaca agen di langkah awal."""
    lines: list[str] = []
    lines.append(f"# Konteks Pra-Loaded — {penugasan_kode}")
    lines.append("")
    lines.append("> Bundle ini dibangun otomatis sebelum kamu jalan. Pakai sbg referensi utama.")
    lines.append(f"> **Obyek:** {obyek}")
    lines.append(f"> **Skill:** {skill}")
    lines.append("")

    # 1. Pattern wiki
    lines.append("## 1. Pattern Temuan Terkurasi (acuan format temuan)")
    if patterns.get("top"):
        lines.append(f"_Top {len(patterns['top'])} dari {patterns['total_available']} pattern utk skill `{skill}` — urut severity._")
        lines.append("")
        for p in patterns["top"]:
            sev = p.get("severity") or "—"
            lines.append(f"### [{p['id']}] {p['judul']}  · `{sev}` · {p.get('kategori', '')}")
            if p.get("kriteria_baku"):
                lines.append(f"**Kriteria baku:** {p['kriteria_baku']}")
            tags = p.get("tags") or []
            if tags:
                lines.append(f"tags: {', '.join(str(t) for t in tags)}")
            if p.get("body_excerpt"):
                lines.append("")
                lines.append(p["body_excerpt"])
            lines.append("")
    else:
        lines.append(f"_Tidak ada pattern terkurasi untuk skill `{skill}`. Skill mungkin criteria-driven — load_skill saat butuh._")
        lines.append("")

    # 2. Konteks pendukung
    lines.append("## 2. Konteks Pendukung — Anti-Halusinasi")
    for kat, body in konteks.items():
        lines.append(f"### {kat}")
        lines.append(body)
        lines.append("")

    # 3. Vault organisasi
    lines.append("## 3. Catatan Vault Organisasi (related obyek)")
    if vault.get("skip_reason"):
        lines.append(f"_Skip: {vault['skip_reason']}._")
    elif not vault.get("notes"):
        lines.append(f"_Tidak ada catatan vault yg relevan dgn obyek (keyword: {', '.join(vault.get('keywords', []))})._")
    else:
        lines.append(f"_Keyword pencarian: `{' '.join(vault.get('keywords', []))}`. {len(vault['notes'])} catatan terkurasi._")
        lines.append("")
        for n in vault["notes"]:
            lines.append(f"### {n['name']}")
            if n.get("summary"):
                lines.append(f"_{n['summary']}_")
            lines.append("")
            lines.append(n.get("content") or "")
            lines.append("")

    # 4. Riwayat penugasan serupa
    lines.append("## 4. Riwayat Penugasan Serupa (catatan W3 writeback)")
    if not writeback:
        lines.append("_Belum ada penugasan selesai dgn skill+obyek serupa di vault._")
    else:
        for w in writeback:
            sim_pct = (w.get("similarity") or 0.0) * 100
            lines.append(f"### {w.get('judul') or w.get('nama_file')}")
            lines.append(f"_File: `{w.get('nama_file')}` · {w.get('jumlah_temuan', 0)} temuan · similarity {sim_pct:.0f}%_")
            lines.append("")
            lines.append(w.get("content") or "")
            lines.append("")

    lines.append("---")
    lines.append("_Bundle dibangun deterministik — re-build kapan saja via tombol 'Refresh Konteks' di UI._")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_preload_bundle(
    *,
    penugasan_kode: str,
    obyek: str,
    skill: str,
) -> dict[str, Any]:
    """Bangun konteks bundle utk satu penugasan.

    Return dict {markdown, stats, sources}. Caller (route) yg simpan file.
    """
    vault = _bundle_vault_notes(obyek)
    patterns = _bundle_patterns(skill)
    konteks = _bundle_konteks()
    writeback = _bundle_writeback_history(skill, obyek)

    md = _format_bundle(
        penugasan_kode=penugasan_kode,
        obyek=obyek,
        skill=skill,
        vault=vault,
        patterns=patterns,
        konteks=konteks,
        writeback=writeback,
    )

    stats = {
        "char_count": len(md),
        "n_vault_notes": len(vault.get("notes") or []),
        "n_patterns": len(patterns.get("top") or []),
        "n_konteks": len(konteks),
        "n_writeback_history": len(writeback),
        "vault_keywords": vault.get("keywords") or [],
    }
    return {"markdown": md, "stats": stats}


def save_preload_bundle(folder: Path, md: str) -> Path:
    """Simpan bundle ke `_PRELOAD/context-bundle.md` di folder penugasan."""
    target_dir = folder / "_PRELOAD"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "context-bundle.md"
    target.write_text(md, encoding="utf-8")
    return target
