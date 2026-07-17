"""Routes Skill — daftar skill pengawasan terdaftar (folder-driven).

Dipakai frontend untuk dropdown jenis penugasan (dinamis, bukan hardcode).
Read-only; sumber data = app.skills_registry (path APP_SKILLS_PATH).
"""
from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import Role, User
from app.skills_registry import list_skills

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("")
async def get_skills(
    _current: tuple[User, Role] = Depends(get_current_user),
) -> list[dict]:
    """Daftar skill terdaftar (slug, name, jenis, output, has_pipeline)."""
    return [
        {
            "slug": s["slug"],
            "name": s["name"],
            "jenis": s["jenis"],
            "output": s["output"],
            "has_pipeline": s["has_pipeline"],
        }
        for s in list_skills()
    ]


# ===========================================================================
# Kelola skill (menu Knowledge > Kelola Skill).
# Baca: semua role. Tulis (edit SKILL.md / buat skill baru): HANYA Pengendali
# Teknis — skill adalah tulang punggung mutu pengawasan, perubahan sembarangan
# langsung mengubah perilaku agen. Tidak ada endpoint hapus skill dari UI
# (terlalu destruktif; hapus lewat git bila memang perlu).
# ===========================================================================
import re
from pathlib import Path

from fastapi import Body, HTTPException, status

from app.skills_registry import (
    _parse_frontmatter,
    _skills_dir,
    get_skill_md,
    list_skill_references,
    refresh,
    skill_dir,
    skill_exists,
)

_SLUG_RE = r"^[a-z0-9]+(-[a-z0-9]+)*$"
_REF_NAME_RE = r"^[A-Za-z0-9._\-]+$"


def _require_pt_skill(role: Role) -> None:
    if role != Role.PT:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Hanya Pengendali Teknis (PT) yang boleh mengelola skill. Role Anda: {role.value}.",
        )


def _validate_skill_md(text: str) -> list[str]:
    """Validasi minimum SKILL.md sebelum ditulis — frontmatter harus parseable
    dan punya `name` + `jenis` (dipakai registry & dropdown penugasan)."""
    errs: list[str] = []
    if not text.strip():
        return ["SKILL.md kosong."]
    fm = _parse_frontmatter(text)
    if not fm:
        errs.append("Frontmatter tidak terbaca — file harus diawali blok '---' berisi 'key: value'.")
        return errs
    if not fm.get("name"):
        errs.append("Frontmatter wajib punya 'name:' (dipakai registry & dropdown penugasan).")
    if not fm.get("jenis"):
        errs.append("Frontmatter wajib punya 'jenis:' (mis. 'Reviu (…)' / 'Audit (…)').")
    return errs


@router.get("/{slug}")
async def get_skill_detail(
    slug: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Detail 1 skill: isi SKILL.md + daftar reference. Semua role baca."""
    if not re.match(_SLUG_RE, slug):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
    content = get_skill_md(slug)
    if content is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skill '{slug}' tidak ada.")
    return {
        "slug": slug,
        "content": content,
        "references": list_skill_references(slug),
    }


@router.get("/{slug}/reference")
async def get_skill_reference(
    slug: str,
    path: str,
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Baca isi 1 file reference skill (read-only, hanya file teks)."""
    if not re.match(_SLUG_RE, slug):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
    d = skill_dir(slug)
    if d is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skill '{slug}' tidak ada.")
    # Anti path-traversal: path harus persis salah satu dari list_skill_references.
    if path not in list_skill_references(slug):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Reference '{path}' tidak terdaftar di skill ini.")
    f = d / path
    if f.suffix.lower() in (".pdf", ".docx", ".xlsx", ".png", ".jpg"):
        return {"slug": slug, "path": path, "binary": True,
                "content": f"(file biner {f.suffix} — {f.stat().st_size:,} bytes; buka dari folder skill)"}
    try:
        return {"slug": slug, "path": path, "binary": False,
                "content": f.read_text(encoding="utf-8")[:120_000]}
    except (OSError, UnicodeDecodeError) as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Gagal baca: {e}")


@router.put("/{slug}")
async def update_skill(
    slug: str,
    payload: dict = Body(...),
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Simpan perubahan SKILL.md — PT only, validasi frontmatter dulu."""
    user, role = current
    _require_pt_skill(role)
    if not re.match(_SLUG_RE, slug):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug tidak valid.")
    content = payload.get("content")
    if not isinstance(content, str):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Body harus {'content': '<isi SKILL.md>'}.")
    errs = _validate_skill_md(content)
    if errs:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, {"errors": errs})
    d = skill_dir(slug)
    if d is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Skill '{slug}' tidak ada — pakai POST untuk buat baru.")
    (d / "SKILL.md").write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    refresh()
    return {"ok": True, "slug": slug}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_skill(
    payload: dict = Body(...),
    current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    """Buat skill baru dari 0 — PT only. Body: {slug, content}.

    Membuat folder `knowledge/skills/<slug>/` + SKILL.md + folder references/
    kosong. Konten divalidasi frontmatter minimal (name + jenis).
    """
    user, role = current
    _require_pt_skill(role)
    slug = str(payload.get("slug") or "").strip().lower()
    content = payload.get("content")
    if not re.match(_SLUG_RE, slug):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Slug tidak valid — huruf kecil/angka/strip, mis. 'reviu-aset-tik'.",
        )
    if not isinstance(content, str):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Body harus {'slug': ..., 'content': '<isi SKILL.md>'}.")
    errs = _validate_skill_md(content)
    if errs:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, {"errors": errs})
    if skill_exists(slug):
        raise HTTPException(status.HTTP_409_CONFLICT, f"Skill '{slug}' sudah ada — pakai Edit.")

    d = _skills_dir() / slug
    d.mkdir(parents=True, exist_ok=False)
    (d / "SKILL.md").write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    (d / "references").mkdir(exist_ok=True)
    refresh()
    return {"ok": True, "slug": slug, "path": str(d)}
