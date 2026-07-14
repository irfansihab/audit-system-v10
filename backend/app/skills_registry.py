"""Registry skill pengawasan — folder-driven.

v7 menemukan skill dari folder `APP_SKILLS_PATH` (lihat config). Satu skill =
satu subfolder yang memuat `SKILL.md`. Tambah folder = tambah skill, tanpa ubah
kode atau skema DB (kolom `Penugasan.skill` sudah `String`).

Folder non-skill (mis. `shared-*`, `panduan-format-umum`, `_draft`) tidak punya
`SKILL.md` sehingga otomatis tidak terdaftar.

Catatan path: SKILL.md dari sistem cowork lama merujuk `audit-system-v4/...`.
Loader (skill_tools) menyelesaikan reference RELATIF terhadap folder skill — jadi
prefiks lama itu di-strip, bukan di-rewrite massal di file.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from app.config import get_settings

# Skill pipeline V6 yang sudah jalan — selalu valid walau folder skills/ kosong
# (mis. di CI). Mempertahankan kompatibilitas penugasan lama.
LEGACY_SKILLS = ("reviu-rka-kl", "reviu-pengadaan")

# Folder di knowledge/skills/ yang BUKAN skill pengawasan (meski punya SKILL.md).
# Meta-skill (`kepatuhan-saipi` QC SAIPI, `graduasi-skill-spesifik` pengembangan)
# sudah DIPINDAH ke `knowledge/meta/` (P4/Fase 3.3) → tak lagi di sini, jadi tak
# perlu dikecualikan. Sisa yang di-skills/ tapi bukan skill: draft & doktrin bersama.
_EXCLUDE_DIRS = {"_draft", "panduan-format-umum"}

# (kosong sejak 3.3 — meta-skill dipindah ke knowledge/meta/, bukan lagi disembunyikan)
_HIDDEN_FROM_PICKER: set[str] = set()


def _skills_dir() -> Path:
    return get_settings().skills_path


def _slugify(skill: str) -> str:
    return re.sub(r"[^a-z0-9\-]", "-", str(skill).strip().lower())


def _parse_frontmatter(content: str) -> dict:
    """Parser YAML frontmatter sederhana (key: value), tanpa dep PyYAML.

    Cukup untuk metadata skill: name, jenis, fungsi, output, auto_execute, model.
    """
    if not content.startswith("---"):
        return {}
    end = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if not end:
        return {}
    meta: dict = {}
    for line in content[3 : end.start() + 3].splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_\-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            val = val[1:-1]
        meta[key] = val
    return meta


def _skill_meta(skill_dir: Path) -> dict | None:
    """Baca metadata satu folder skill, atau None bila bukan skill."""
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return None
    try:
        text = md.read_text(encoding="utf-8")
    except OSError:
        return None
    fm = _parse_frontmatter(text)
    slug = skill_dir.name
    auto = str(fm.get("auto_execute", "")).strip().lower() in {"true", "1", "yes"}
    return {
        "slug": slug,
        "name": fm.get("name", slug),
        "jenis": fm.get("jenis", ""),
        "fungsi": fm.get("fungsi", ""),
        "output": fm.get("output", ""),
        "model": fm.get("model", ""),
        "auto_execute": auto,
        "has_pipeline": slug in LEGACY_SKILLS,
    }


@lru_cache(maxsize=1)
def _scan() -> dict[str, dict]:
    """Scan folder skills sekali (cached). Key = slug."""
    base = _skills_dir()
    out: dict[str, dict] = {}
    if base.exists():
        for d in sorted(base.iterdir()):
            if not d.is_dir() or d.name in _EXCLUDE_DIRS:
                continue
            meta = _skill_meta(d)
            if meta:
                out[meta["slug"]] = meta
    return out


def refresh() -> None:
    """Bersihkan cache scan (dipakai bila folder skill berubah saat runtime)."""
    _scan.cache_clear()


def list_skills() -> list[dict]:
    """Daftar skill PILIHAN AUDITOR (metadata ringkas), urut slug.

    Mengecualikan meta-skill yang loadable agen tapi bukan jenis pengawasan
    (mis. `kepatuhan-saipi` = QC SAIPI). Skill itu tetap bisa di-`load_skill`
    oleh agen lewat `_scan()`/`skill_exists()`.
    """
    return [m for s, m in _scan().items() if s not in _HIDDEN_FROM_PICKER]


def available_slugs() -> list[str]:
    """Slug skill yang valid: hasil scan ∪ LEGACY (fallback bila folder kosong)."""
    found = set(_scan().keys())
    return sorted(found | set(LEGACY_SKILLS))


def skill_exists(skill: str) -> bool:
    slug = _slugify(skill)
    return slug in _scan() or slug in LEGACY_SKILLS


def skill_dir(skill: str) -> Path | None:
    """Folder skill bila ada (dan SKILL.md hadir), else None."""
    slug = _slugify(skill)
    if slug not in _scan():
        return None
    return _skills_dir() / slug


def get_skill_md(skill: str) -> str | None:
    """Isi SKILL.md sebuah skill, atau None bila tidak ada."""
    d = skill_dir(skill)
    if d is None:
        return None
    md = d / "SKILL.md"
    try:
        return md.read_text(encoding="utf-8")
    except OSError:
        return None


def list_skill_references(skill: str) -> list[str]:
    """Daftar reference (path relatif folder skill) — references/ + scripts/."""
    d = skill_dir(skill)
    if d is None:
        return []
    refs: list[str] = []
    for sub in ("references", "scripts", "checklists"):
        folder = d / sub
        if not folder.is_dir():
            continue
        for f in sorted(folder.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and not f.name.endswith(".pyc"):
                refs.append(str(f.relative_to(d)))
    return refs


# Prefiks layout lama yang perlu di-strip agar resolve relatif folder skill.
_LEGACY_PREFIX = re.compile(r"^audit-system-v4/skills/[^/]+/", re.IGNORECASE)


def read_skill_reference(skill: str, reference: str) -> str | None:
    """Baca isi satu reference (path-traversal safe). Return teks atau None.

    Menerima path relatif ("references/x.md") atau path layout lama
    ("audit-system-v4/skills/<slug>/references/x.md") — prefiks lama di-strip.
    """
    d = skill_dir(skill)
    if d is None:
        return None
    norm = str(reference).replace("\\", "/").strip().lstrip("/")
    norm = _LEGACY_PREFIX.sub("", norm)
    if not norm:
        return None
    base = d.resolve()
    target = (base / norm).resolve()
    # Pastikan tetap di dalam folder skill (cegah traversal ../)
    if base != target and base not in target.parents:
        return None
    if not target.is_file():
        return None
    try:
        return target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
