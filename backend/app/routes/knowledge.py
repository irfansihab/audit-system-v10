"""Routes Knowledge / Wiki.

- W1 (baca vault): vault_search / vault_get_page → panel "Cari Wiki". Read-only.
- W2 (promosi pattern): agregasi usulan pattern dari feedback agen lintas
  penugasan (`/pattern-monitor`) + promote jadi pattern wiki resmi (`/patterns`,
  PT/PM). Lihat app.wiki_promote.
- W3 (tulis-balik penugasan ➝ vault): penugasan `LHP_DONE` ➝ generate draft
  `pengawasan-{kode}.md` + delta index/log ➝ review ➝ Download .md (opsi A,
  rekomendasi) atau Apply ke vault (opsi B). Lihat app.wiki_writeback.
- W4 (browser pattern temuan): `/patterns/library` + `/patterns/library/{id}`
  — semua role bisa jelajah 65+ pattern terkurasi lintas 12 skill. Read-only.
  Lihat app.knowledge_browse.

V6 read-only — promosi menulis ke folder wiki proyek, bukan ke V6.
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import knowledge_browse, wiki_promote, wiki_writeback
from app.auth import get_current_user
from app.config import get_settings
from app.database import get_db
from app.models import (
    Penugasan,
    Role,
    User,
    WikiProposal,
    WikiProposalStatus,
)
from app.routes.feedback import _collect_feedback
from app.tools.wiki_tools import vault_get_page, vault_search


def _is_lhp_done(folder: Path) -> bool:
    """Cocokkan dengan `compute_penugasan_status` di storage.py: LHP_DONE bila ada
    dokumen laporan `_LHP/{LHP-SUBSTANSI|LHA|LHR|LHE|LP}-*.docx`. Inline supaya
    hemat query (kita tidak butuh derivasi penuh untuk filtering candidate)."""
    lhp_dir = folder / "_LHP"
    return lhp_dir.exists() and any(
        next(lhp_dir.glob(pat), None) is not None
        for pat in ("LHP-SUBSTANSI*.docx", "LHA-*.docx", "LHR-*.docx", "LHE-*.docx", "LP-*.docx")
    )

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/wiki/search")
async def wiki_search(
    q: str,
    limit: int = 12,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Cari catatan vault relevan dengan query `q`."""
    return vault_search(q, limit=max(1, min(limit, 50)))


@router.get("/wiki/page")
async def wiki_page(
    name: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Baca isi lengkap satu catatan vault by name (aman dari path traversal)."""
    return vault_get_page(name)


# =============================================================================
# W2 — promosi pattern
# =============================================================================

@router.get("/pattern-monitor")
async def pattern_monitor(
    days: int = Query(90, ge=1, le=365, description="Window hari ke belakang"),
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Agregasi usulan pattern (`pattern_suggestions`) dari feedback agen lintas
    penugasan. Kandidat yg berulang = bahan promosi jadi pattern wiki resmi.

    Read-only & role-agnostik (sejalan dgn /feedback/aggregate).
    """
    rows = (
        await db.execute(select(Penugasan.folder_path, Penugasan.skill, Penugasan.obyek))
    ).all()
    folders: list[Path] = []
    folder_meta: dict[str, dict] = {}
    for folder_path, skill, obyek in rows:
        if not folder_path:
            continue
        p = Path(folder_path)
        folders.append(p)
        folder_meta[p.name] = {
            "skill": skill if isinstance(skill, str) else getattr(skill, "value", str(skill)),
            "obyek": obyek or "",
        }

    cutoff = datetime.utcnow() - timedelta(days=days)
    feedback_rows = _collect_feedback(folders, cutoff)
    result = wiki_promote.aggregate_pattern_suggestions(feedback_rows, folder_meta)
    result["days"] = days
    result["total_feedback"] = len(feedback_rows)
    return result


@router.post("/patterns")
async def create_pattern(
    body: dict = Body(...),
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Promote satu usulan jadi pattern wiki resmi (tulis file .md). PT/PM only."""
    role = current[1]
    if role not in (Role.PT, Role.PM):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Promosi pattern hanya untuk PT/PM (kurasi knowledge). Role Anda: {role.value}.",
        )

    res = wiki_promote.promote_pattern(
        skill=str(body.get("skill", "")).strip(),
        pattern_id=str(body.get("pattern_id") or body.get("id") or "").strip(),
        judul=str(body.get("judul", "")).strip(),
        kategori=str(body.get("kategori", "")).strip(),
        severity=str(body.get("severity", "MEDIUM")).strip(),
        kriteria_baku=str(body.get("kriteria_baku", "")).strip(),
        kondisi=str(body.get("kondisi", "")).strip(),
        akibat=str(body.get("akibat", "")).strip(),
        rekomendasi=str(body.get("rekomendasi", "")).strip(),
        bukti=str(body.get("bukti", "")).strip(),
        tags=body.get("tags") if isinstance(body.get("tags"), list) else None,
        sumber_penugasan=body.get("sumber_penugasan") if isinstance(body.get("sumber_penugasan"), list) else None,
    )
    if not res.get("ok"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, res.get("error", "gagal promote pattern"))
    return res


# =============================================================================
# W3 — tulis-balik penugasan ➝ vault
# =============================================================================

def _proposal_to_dict(p: WikiProposal) -> dict:
    """Serialisasi WikiProposal untuk respons HTTP."""
    return {
        "id": p.id,
        "penugasan_id": p.penugasan_id,
        "nama_file": p.nama_file,
        "ringkasan": p.ringkasan,
        "status": p.status.value if hasattr(p.status, "value") else str(p.status),
        "dibuat_at": p.dibuat_at.isoformat() if p.dibuat_at else None,
        "diupdate_at": p.diupdate_at.isoformat() if p.diupdate_at else None,
        "applied_at": p.applied_at.isoformat() if p.applied_at else None,
    }


def _proposal_with_content(p: WikiProposal) -> dict:
    """Versi lengkap termasuk konten markdown + delta."""
    base = _proposal_to_dict(p)
    base["konten_md"] = p.konten_md
    base["delta_index"] = p.delta_index
    base["delta_log"] = p.delta_log
    return base


@router.get("/writeback/candidates")
async def writeback_candidates(
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Daftar penugasan LHP_DONE + status proposal-nya (none / draft / applied /
    rejected). Read-only & role-agnostik."""
    rows = (
        await db.execute(
            select(
                Penugasan.id,
                Penugasan.kode,
                Penugasan.obyek,
                Penugasan.skill,
                Penugasan.folder_path,
                Penugasan.updated_at,
            ).order_by(Penugasan.updated_at.desc())
        )
    ).all()

    # Bulk-load proposals (1 query)
    proposal_rows = (
        await db.execute(
            select(WikiProposal.penugasan_id, WikiProposal.status, WikiProposal.nama_file)
        )
    ).all()
    proposal_by_pid = {pid: (st, nf) for pid, st, nf in proposal_rows}

    items: list[dict] = []
    for pid, kode, obyek, skill, folder_path, updated_at in rows:
        if not folder_path:
            continue
        folder = Path(folder_path)
        if not _is_lhp_done(folder):
            continue
        skill_value = skill if isinstance(skill, str) else getattr(skill, "value", str(skill))
        st_proposal, nf_proposal = proposal_by_pid.get(pid, (None, None))
        items.append({
            "penugasan_id": pid,
            "kode": kode,
            "obyek": obyek,
            "skill": skill_value,
            "lhp_done_at": updated_at.isoformat() if updated_at else None,
            "proposal_status": (
                st_proposal.value if hasattr(st_proposal, "value")
                else (st_proposal if st_proposal else "NONE")
            ),
            "nama_file": nf_proposal,
        })
    return {"items": items, "total": len(items)}


async def _load_penugasan_or_404(db: AsyncSession, penugasan_id: int) -> Penugasan:
    p = (
        await db.execute(select(Penugasan).where(Penugasan.id == penugasan_id))
    ).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Penugasan {penugasan_id} tidak ditemukan")
    return p


@router.post("/writeback/{penugasan_id}/generate")
async def writeback_generate(
    penugasan_id: int,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Generate (atau regenerate) draft catatan vault dari penugasan LHP_DONE.

    Akses: PT / PM / KT (kurasi + tulis catatan operasional). AT cuma boleh
    lihat preview (via /proposal).
    """
    user, role = current
    if role not in (Role.PT, Role.PM, Role.KT):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Generate draft wiki hanya untuk PT/PM/KT. Role Anda: {role.value}.",
        )

    p = await _load_penugasan_or_404(db, penugasan_id)
    folder = Path(p.folder_path)
    if not _is_lhp_done(folder):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Penugasan belum LHP_DONE — tulis-balik wiki menunggu LHP terbit.",
        )

    ketua_tim_nama: str | None = None
    if p.ketua_tim_id:
        kt = (
            await db.execute(select(User.nama_lengkap).where(User.id == p.ketua_tim_id))
        ).scalar_one_or_none()
        ketua_tim_nama = kt

    skill_value = p.skill if isinstance(p.skill, str) else getattr(p.skill, "value", str(p.skill))
    built = wiki_writeback.build_proposal_from_folder(
        penugasan_dict={
            "kode": p.kode,
            "obyek": p.obyek,
            "skill": skill_value,
            "nomor_st": p.nomor_st,
            "tanggal_st": p.tanggal_st,
            "created_at": p.created_at,
        },
        folder=folder,
        ketua_tim_nama=ketua_tim_nama,
    )

    # Upsert (1 baris per penugasan_id)
    existing = (
        await db.execute(select(WikiProposal).where(WikiProposal.penugasan_id == penugasan_id))
    ).scalar_one_or_none()

    now = datetime.utcnow()
    if existing:
        existing.nama_file = built["nama_file"]
        existing.konten_md = built["konten_md"]
        existing.delta_index = built["delta_index"]
        existing.delta_log = built["delta_log"]
        existing.ringkasan = built["ringkasan"]
        existing.status = WikiProposalStatus.DRAFT  # regenerate → DRAFT (perlu re-apply manual)
        existing.diupdate_at = now
        # Tidak reset applied_at/applied_by — info historis bila pernah apply
        proposal = existing
    else:
        proposal = WikiProposal(
            penugasan_id=penugasan_id,
            nama_file=built["nama_file"],
            konten_md=built["konten_md"],
            delta_index=built["delta_index"],
            delta_log=built["delta_log"],
            ringkasan=built["ringkasan"],
            status=WikiProposalStatus.DRAFT,
            dibuat_at=now,
            diupdate_at=now,
        )
        db.add(proposal)

    await db.commit()
    await db.refresh(proposal)
    return _proposal_with_content(proposal)


@router.get("/writeback/{penugasan_id}/proposal")
async def writeback_proposal(
    penugasan_id: int,
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Ambil proposal terkini untuk satu penugasan (kalau ada)."""
    p = (
        await db.execute(select(WikiProposal).where(WikiProposal.penugasan_id == penugasan_id))
    ).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Belum ada proposal — generate dulu.")
    return _proposal_with_content(p)


@router.get("/writeback/{penugasan_id}/download")
async def writeback_download(
    penugasan_id: int,
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PlainTextResponse:
    """Unduh konten .md (opsi A — Obsidian flow). Semua role boleh."""
    p = (
        await db.execute(select(WikiProposal).where(WikiProposal.penugasan_id == penugasan_id))
    ).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Belum ada proposal — generate dulu.")
    return PlainTextResponse(
        content=p.konten_md,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{p.nama_file}"'},
    )


@router.post("/writeback/{penugasan_id}/apply")
async def writeback_apply(
    penugasan_id: int,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Tulis langsung ke vault (opsi B). PT/PM only."""
    user, role = current
    if role not in (Role.PT, Role.PM):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Apply ke vault hanya untuk PT/PM. Role Anda: {role.value}.",
        )

    settings = get_settings()
    vault_root = settings.vault_path
    if vault_root is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Vault tidak dikonfigurasi — set APP_VAULT_PATH. Pakai Download .md sebagai gantinya.",
        )

    p = (
        await db.execute(select(WikiProposal).where(WikiProposal.penugasan_id == penugasan_id))
    ).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Belum ada proposal — generate dulu.")

    try:
        res = wiki_writeback.apply_to_vault(
            vault_root=vault_root,
            nama_file=p.nama_file,
            konten_md=p.konten_md,
            delta_index=p.delta_index or "",
            delta_log=p.delta_log or "",
        )
    except wiki_writeback.WikiWriteBackError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    p.status = WikiProposalStatus.APPLIED
    p.applied_at = datetime.utcnow()
    p.applied_by_user_id = user.id
    await db.commit()
    await db.refresh(p)

    out = _proposal_to_dict(p)
    out["apply_result"] = res
    return out


@router.post("/writeback/{penugasan_id}/reject")
async def writeback_reject(
    penugasan_id: int,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Tandai proposal REJECTED — tidak masuk vault. PT/PM only."""
    role = current[1]
    if role not in (Role.PT, Role.PM):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Tolak proposal hanya untuk PT/PM. Role Anda: {role.value}.",
        )
    p = (
        await db.execute(select(WikiProposal).where(WikiProposal.penugasan_id == penugasan_id))
    ).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Belum ada proposal.")
    p.status = WikiProposalStatus.REJECTED
    await db.commit()
    await db.refresh(p)
    return _proposal_to_dict(p)


# =============================================================================
# W4 — Pattern Library Browser
#
# Tujuan: 65+ pattern temuan terkurasi di `wiki/temuan-patterns/<skill>/` jadi
# bisa dijelajah manual lewat web — semua role (bukan hanya agen). Sebelumnya
# pattern hanya bisa dibaca agen via tool `list_temuan_patterns` / `get_temuan_pattern`.
# =============================================================================


@router.get("/patterns/library")
async def patterns_library(
    skill: str | None = Query(None, description="Filter skill folder (mis. 'reviu-pengadaan'). Kosong = semua skill."),
    severity: str | None = Query(None, description="Filter severity: CRITICAL / HIGH / MEDIUM / LOW."),
    search: str | None = Query(None, description="Substring case-insensitive di id/judul/kategori/kriteria_baku/tags."),
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Jelajah pattern temuan terkurasi. Semua role boleh baca."""
    return knowledge_browse.list_pattern_library(
        skill=skill or None,
        severity=severity or None,
        search=search or None,
    )


@router.get("/patterns/library/{pattern_id}")
async def patterns_library_get(
    pattern_id: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Baca isi lengkap satu pattern (frontmatter + body markdown)."""
    res = knowledge_browse.get_pattern_full(pattern_id)
    if not res:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Pattern '{pattern_id}' tidak ditemukan. Cek /knowledge/patterns/library untuk daftar valid.",
        )
    return res


# ===========================================================================
# Template KP & PKP (INTEGRAL workflow tahapan 1 + 2)
# ===========================================================================

def _parse_template_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter dari template markdown. Return (meta, body)."""
    import re
    m = re.match(r"^---\n(.*?\n)---\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        import yaml
        meta = yaml.safe_load(m.group(1)) or {}
        return meta, m.group(2)
    except Exception:  # noqa: BLE001
        return {}, text


@router.get("/templates/{kind}")
async def list_templates(
    kind: str,
    skill: str = Query(default=""),
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """List template KP atau PKP dari wiki.

    Args:
        kind: 'kp' atau 'pkp'
        skill: filter skill (mis. 'audit-pengadaan'). Empty = semua.

    Return: {items: [{slug, judul, skill, jenis, field_required, field_optional}, ...]}
    """
    if kind not in ("kp", "pkp"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "kind harus 'kp' atau 'pkp'")
    s = get_settings()
    root = s.wiki_path / "templates" / kind
    if not root.is_dir():
        return {"items": []}
    items: list[dict] = []
    for f in sorted(root.glob("*.md")):
        try:
            txt = f.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _ = _parse_template_frontmatter(txt)
        s_filter = (skill or "").strip().lower()
        f_skill = str(meta.get("skill", "")).strip().lower()
        if s_filter and f_skill != s_filter and f_skill != "default":
            continue
        # Extract title from first h1
        body_lines = txt.split("\n")
        title = next((l.replace("# ", "").strip() for l in body_lines if l.startswith("# ")), f.stem)
        items.append({
            "slug": f.stem,
            "judul": title,
            "skill": f_skill or "default",
            "jenis": meta.get("jenis"),
            "field_required": meta.get("field_required", []),
            "field_optional": meta.get("field_optional", []),
            "versi": meta.get("versi"),
        })
    return {"items": items, "count": len(items)}


@router.get("/templates/{kind}/{slug}")
async def get_template(
    kind: str,
    slug: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Ambil isi lengkap 1 template KP/PKP."""
    if kind not in ("kp", "pkp"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "kind harus 'kp' atau 'pkp'")
    s = get_settings()
    f = s.wiki_path / "templates" / kind / f"{slug}.md"
    if not f.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Template {kind}/{slug} tidak ditemukan")
    try:
        txt = f.read_text(encoding="utf-8")
    except OSError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Gagal baca: {e}")
    meta, body = _parse_template_frontmatter(txt)
    return {
        "slug": slug,
        "kind": kind,
        "meta": meta,
        "body": body,
        "raw": txt,
    }


# ---------------------------------------------------------------------------
# Pengelolaan Template KP/PKP (menu Knowledge > Template) — Pengendali Teknis
# bisa buat/edit/hapus + generate draft dari wiki oleh AI. Baca: semua role.
# Template dipakai form KP/PKP INTEGRAL (routes/penugasan kp-md/sasaran).
# ---------------------------------------------------------------------------
_TEMPLATE_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,80}$")
_PROTECTED_TEMPLATES = {"kp-default", "pkp-default"}


def _require_pt_template(role: Role) -> None:
    if role != Role.PT:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Hanya Pengendali Teknis (PT) yang boleh mengelola template. Role Anda: {role.value}.",
        )


def _validate_template_text(kind: str, text: str) -> tuple[dict, str]:
    """Validasi template: wajib frontmatter YAML + field `skill`, dan ada judul H1.
    Return (meta, body) bila valid; raise 422 bila tidak."""
    meta, body = _parse_template_frontmatter(text)
    if not isinstance(meta, dict) or not meta:
        raise HTTPException(422, "Template wajib diawali frontmatter YAML (--- ... ---) berisi minimal `skill`.")
    if not str(meta.get("skill", "")).strip():
        raise HTTPException(422, "Frontmatter wajib memuat `skill` (mis. audit-pengadaan / default).")
    if not any(l.startswith("# ") for l in body.split("\n")):
        raise HTTPException(422, "Body template wajib memuat satu judul H1 (baris diawali '# ').")
    return meta, body


class TemplatePayload(BaseModel):
    raw: str = Field(..., min_length=20, description="Isi lengkap template (frontmatter + body markdown)")


@router.put("/templates/{kind}/{slug}")
async def upsert_template(
    kind: str,
    slug: str,
    payload: TemplatePayload,
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Buat/timpa 1 template KP/PKP. Hanya Pengendali Teknis."""
    _user, role = current
    _require_pt_template(role)
    if kind not in ("kp", "pkp"):
        raise HTTPException(400, "kind harus 'kp' atau 'pkp'")
    slug = slug.strip().lower()
    if not _TEMPLATE_SLUG_RE.match(slug):
        raise HTTPException(422, "slug hanya huruf kecil/angka/strip, 2-81 karakter.")
    meta, _body = _validate_template_text(kind, payload.raw)
    s = get_settings()
    root = s.wiki_path / "templates" / kind
    root.mkdir(parents=True, exist_ok=True)
    f = root / f"{slug}.md"
    existed = f.is_file()
    tmp = f.with_suffix(".md.tmp")
    tmp.write_text(payload.raw, encoding="utf-8")
    import os as _os
    _os.replace(tmp, f)
    return {"ok": True, "slug": slug, "kind": kind, "action": "replaced" if existed else "created",
            "skill": str(meta.get("skill", ""))}


@router.delete("/templates/{kind}/{slug}")
async def delete_template(
    kind: str,
    slug: str,
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Hapus 1 template KP/PKP. Hanya PT. Template default dilindungi."""
    _user, role = current
    _require_pt_template(role)
    if kind not in ("kp", "pkp"):
        raise HTTPException(400, "kind harus 'kp' atau 'pkp'")
    slug = slug.strip().lower()
    if slug in _PROTECTED_TEMPLATES:
        raise HTTPException(400, f"Template '{slug}' adalah fallback default — tidak boleh dihapus.")
    s = get_settings()
    f = s.wiki_path / "templates" / kind / f"{slug}.md"
    if not f.is_file():
        raise HTTPException(404, f"Template {kind}/{slug} tidak ditemukan")
    f.unlink()
    return {"ok": True, "deleted": slug, "kind": kind}


class TemplateGeneratePayload(BaseModel):
    skill: str = Field(..., description="Slug skill target, mis. audit-pengadaan")
    instruksi: str = Field(default="", description="Arahan tambahan opsional dari PT")


@router.post("/templates/{kind}/generate")
async def generate_template(
    kind: str,
    payload: TemplateGeneratePayload,
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Generate DRAFT template KP/PKP dari pengetahuan wiki oleh AI (tidak disimpan;
    PT meninjau lalu simpan lewat PUT). Hanya PT."""
    _user, role = current
    _require_pt_template(role)
    if kind not in ("kp", "pkp"):
        raise HTTPException(400, "kind harus 'kp' atau 'pkp'")
    skill = payload.skill.strip().lower()
    if not skill:
        raise HTTPException(422, "skill wajib diisi.")
    s = get_settings()

    # Kumpulkan konteks wiki: template default/base + panduan format skill (bila ada).
    ctx_parts: list[str] = []
    base_f = s.wiki_path / "templates" / kind / f"{kind}-{skill}.md"
    default_f = s.wiki_path / "templates" / kind / f"{kind}-default.md"
    for f in (base_f, default_f):
        if f.is_file():
            ctx_parts.append(f"### Contoh template {kind} ({f.stem}):\n{f.read_text(encoding='utf-8')[:4000]}")
            break
    # Panduan format skill dari knowledge/skills/<skill>/ (SKILL.md ringkas).
    # wiki_path = .../knowledge/wiki → skills = wiki_path.parent/skills.
    skill_md = s.wiki_path.parent / "skills" / skill / "SKILL.md"
    if skill_md.is_file():
        ctx_parts.append(f"### Ringkas SKILL {skill}:\n{skill_md.read_text(encoding='utf-8')[:3000]}")
    konteks = "\n\n".join(ctx_parts) or "(tidak ada contoh template/skill di wiki — susun dari struktur umum)"

    from app.llm_extract import resolve_anthropic_key
    key = resolve_anthropic_key()
    if not key:
        raise HTTPException(503, "API key AI belum dikonfigurasi — generate tidak tersedia. Isi manual via editor.")

    kind_label = "Kartu Penugasan (KP)" if kind == "kp" else "Program Kerja Pengawasan (PKP)"
    prompt = (
        f"Anda membantu Inspektorat menyusun DRAFT template {kind_label} untuk jenis pengawasan '{skill}'.\n"
        f"Gunakan gaya & struktur template contoh dan substansi skill di bawah. Output HARUS berupa markdown "
        f"template lengkap: diawali frontmatter YAML (--- ... ---) dengan field minimal `skill: {skill}`, `kind: {kind}`, "
        f"`jenis`, `field_required` (list), `field_optional` (list); lalu body dengan satu judul H1 dan "
        f"placeholder `{{{{nama_field}}}}` untuk bagian yang diisi via form INTEGRAL. Jangan menambah penjelasan di luar template.\n"
        + (f"\nArahan tambahan PT: {payload.instruksi}\n" if payload.instruksi.strip() else "")
        + f"\n=== KONTEKS WIKI ===\n{konteks}\n=== AKHIR KONTEKS ==="
    )
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        draft = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(502, f"Gagal generate via AI: {e}")
    # Bersihkan bila model membungkus dengan ```
    if draft.startswith("```"):
        draft = re.sub(r"^```[a-z]*\n?", "", draft)
        draft = re.sub(r"\n?```$", "", draft).strip()
    meta, _b = _parse_template_frontmatter(draft)
    return {"ok": True, "kind": kind, "skill": skill, "draft": draft,
            "meta_terdeteksi": meta, "catatan": "DRAFT — tinjau & simpan lewat tombol Simpan (PUT)."}


# ===========================================================================
# Kriteria Pengawasan — kelola regulasi wiki (menu Knowledge > Kriteria
# Pengawasan). Satu file markdown per regulasi di `wiki/konteks/regulasi/`.
# Baca: semua role. Tulis/hapus: HANYA Pengendali Teknis.
#
# File di folder ini ikut dibaca agen lewat preload konteks (lihat
# app/preload_context.py::_bundle_konteks) — jadi regulasi yang di-upload di
# sini benar-benar memperkaya cheat-sheet anti-halusinasi, bukan cuma tampilan.
# ===========================================================================
import re as _re

from fastapi import File, UploadFile


def _require_pt_knowledge(role: Role) -> None:
    if role != Role.PT:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Hanya Pengendali Teknis (PT) yang boleh mengelola regulasi. Role Anda: {role.value}.",
        )


def _regulasi_dir() -> Path:
    d = get_settings().wiki_path / "konteks" / "regulasi"
    d.mkdir(parents=True, exist_ok=True)
    return d


_REGULASI_SLUG_RE = r"^[a-z0-9]+(-[a-z0-9]+)*$"


def _slugify_regulasi(text: str) -> str:
    s = text.lower()
    s = _re.sub(r"[/.]", "-", s)
    s = _re.sub(r"[^a-z0-9-]+", "-", s)
    s = _re.sub(r"-{2,}", "-", s).strip("-")
    return s[:80] or "regulasi"


@router.get("/regulasi")
async def regulasi_list(
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Daftar regulasi wiki (konteks/regulasi/*.md) + regulasi-kunci.md inti."""
    items: list[dict] = []
    for f in sorted(_regulasi_dir().glob("*.md")):
        try:
            txt = f.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _body = _parse_template_frontmatter(txt)
        items.append({
            "slug": f.stem,
            "judul": meta.get("judul") or f.stem,
            "nomor": meta.get("nomor") or "",
            "tahun": meta.get("tahun") or "",
            "status": meta.get("status") or "",
            "sumber_file": meta.get("sumber_file") or "",
            "updated": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            "size_bytes": f.stat().st_size,
        })
    # regulasi-kunci.md = cheat sheet inti (dikelola terpisah, tidak bisa dihapus dari UI)
    kunci = get_settings().wiki_path / "konteks" / "regulasi-kunci.md"
    return {
        "items": items,
        "total": len(items),
        "kunci_ada": kunci.exists(),
    }


@router.get("/regulasi/{slug}")
async def regulasi_get(
    slug: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Isi lengkap 1 regulasi (markdown mentah, untuk baca & form edit)."""
    if slug == "regulasi-kunci":
        f = get_settings().wiki_path / "konteks" / "regulasi-kunci.md"
    else:
        if not _re.match(_REGULASI_SLUG_RE, slug):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
        f = _regulasi_dir() / f"{slug}.md"
    if not f.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Regulasi '{slug}' tidak ada.")
    return {"slug": slug, "content": f.read_text(encoding="utf-8")}


@router.put("/regulasi/{slug}")
async def regulasi_update(
    slug: str,
    payload: dict = Body(...),
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Simpan perubahan isi regulasi — PT only. `regulasi-kunci` boleh diedit
    (cheat sheet inti), tapi TIDAK bisa dihapus."""
    user, role = current
    _require_pt_knowledge(role)
    content = payload.get("content")
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Body harus {'content': '<markdown>'} dan tidak kosong.")
    if slug == "regulasi-kunci":
        f = get_settings().wiki_path / "konteks" / "regulasi-kunci.md"
    else:
        if not _re.match(_REGULASI_SLUG_RE, slug):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
        f = _regulasi_dir() / f"{slug}.md"
    if not f.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Regulasi '{slug}' tidak ada.")
    f.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    return {"ok": True, "slug": slug}


@router.delete("/regulasi/{slug}")
async def regulasi_delete(
    slug: str,
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Hapus 1 regulasi — PT only. `regulasi-kunci.md` dilindungi."""
    user, role = current
    _require_pt_knowledge(role)
    if slug == "regulasi-kunci":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "regulasi-kunci.md adalah cheat sheet inti anti-halusinasi — tidak bisa dihapus dari UI.",
        )
    if not _re.match(_REGULASI_SLUG_RE, slug):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
    f = _regulasi_dir() / f"{slug}.md"
    if not f.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Regulasi '{slug}' tidak ada.")
    f.unlink()
    return {"ok": True, "slug": slug, "deleted": True}


@router.post("/regulasi/upload", status_code=status.HTTP_201_CREATED)
async def regulasi_upload(
    file: UploadFile = File(...),
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Upload dokumen regulasi (PDF) → auto-generate draft markdown ke wiki.

    PT only. Ekstraksi DETERMINISTIK (pdfplumber + regex judul/nomor) — hasil
    ditandai DRAFT-OTOMATIS dan wajib diverifikasi auditor; tidak ada LLM di
    jalur ini, jadi tidak ada risiko sitasi karangan.
    """
    user, role = current
    _require_pt_knowledge(role)
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Hanya file PDF yang didukung.")

    import io

    import pdfplumber

    raw = await file.read()
    if len(raw) > 40 * 1024 * 1024:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File terlalu besar (maks 40 MB).")
    try:
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            pages = [(p.extract_text() or "") for p in pdf.pages[:5]]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"PDF tidak bisa dibaca: {exc}")
    text = "\n".join(pages).strip()
    if not text:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Tidak ada teks terbaca (kemungkinan PDF hasil scan tanpa OCR) — tambahkan regulasi manual lewat Edit.",
        )

    # Deteksi jenis + nomor + tahun: "PERATURAN MENTERI KEUANGAN ... NOMOR 62 TAHUN 2023"
    head = text[:3000]
    m = _re.search(
        r"(UNDANG-UNDANG|PERATURAN\s+PEMERINTAH(?:\s+PENGGANTI\s+UNDANG-UNDANG)?|PERATURAN\s+PRESIDEN|"
        r"PERATURAN\s+MENTERI[\sA-Z]*?|KEPUTUSAN\s+MENTERI[\sA-Z]*?)\s+"
        r"(?:REPUBLIK\s+INDONESIA\s+)?NOMOR\s+([0-9]+[A-Z0-9/.\- ]*?)\s+TAHUN\s+(\d{4})",
        head.upper(),
    )
    jenis = _re.sub(r"\s+", " ", m.group(1)).title() if m else ""
    nomor = m.group(2).strip() if m else ""
    tahun = m.group(3) if m else ""
    # Judul: teks setelah "TENTANG"
    mt = _re.search(r"\bTENTANG\b\s*\n?(.{5,300}?)(?:\n\s*\n|DENGAN RAHMAT|Menimbang)", head.upper(), _re.DOTALL)
    tentang = _re.sub(r"\s+", " ", mt.group(1)).strip().title() if mt else ""

    judul = " ".join(x for x in [jenis, f"Nomor {nomor} Tahun {tahun}" if nomor else "", ("tentang " + tentang) if tentang else ""] if x).strip()
    if not judul:
        judul = Path(file.filename or "regulasi").stem.replace("_", " ").replace("-", " ").title()
    slug = _slugify_regulasi(f"{jenis} {nomor} {tahun}" if nomor else judul)

    f_out = _regulasi_dir() / f"{slug}.md"
    if f_out.exists():
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Regulasi '{slug}' sudah ada di wiki — edit yang ada atau hapus dulu.",
        )

    excerpt = text[:2500]
    md = f"""---
id: REGULASI-{slug.upper()}
kategori: konteks
judul: "{judul}"
nomor: "{nomor}"
tahun: "{tahun}"
status: DRAFT-OTOMATIS
sumber_file: "{file.filename}"
tanggal_dibuat: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [regulasi]
---

# {judul}

> ⚠️ **DRAFT OTOMATIS** hasil ekstraksi `{file.filename}` — pasal kunci belum diisi.
> WAJIB diverifikasi auditor sebelum dipakai sebagai rujukan kriteria/temuan.

## Pasal Kunci

| Pasal | Topik | Kutipan inti |
|---|---|---|
| [DIISI AUDITOR] | [DIISI AUDITOR] | [DIISI AUDITOR] |

## Kutipan Halaman Awal (ekstraksi otomatis, maks 2.500 karakter)

```
{excerpt}
```
"""
    f_out.write_text(md, encoding="utf-8")
    return {"ok": True, "slug": slug, "judul": judul, "nomor": nomor, "tahun": tahun, "file": f_out.name}
