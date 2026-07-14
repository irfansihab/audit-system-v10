"""Meta-skill Graduasi — suling pola penugasan jadi DRAFT skill spesifik.

Port v7-native dari orchestrator cowork `knowledge/meta/graduasi-skill-spesifik/
scripts/graduasi.py` (algoritma sama: deteksi domain, konsolidasi kriteria, cluster
temuan Jaccard), tapi membaca data TERSTRUKTUR v7 (`_KKP/temuan.json`) bukan teks
kriteria mentah, dan menulis ke `knowledge/skills/_draft/<nama>/`.

Human-in-the-loop: generate hanya membuat DRAFT; `promote` (manual) yang
memindahkan ke `knowledge/skills/` agar terdaftar di registry.
"""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

from app.config import get_settings
from app.storage import penugasan_folder

VALID_FUNGSI = {"audit", "reviu", "pemantauan", "evaluasi", "konsultansi", "konsultasi"}

_STOPWORD = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "atau", "adalah", "akan",
    "telah", "pada", "oleh", "dalam", "sebagai", "tidak", "ini", "itu", "juga",
    "dapat", "wajib", "harus", "sebagaimana", "dimaksud", "tersebut", "bagi",
    "kepada", "atas", "agar", "supaya", "jika", "apabila", "maka", "peraturan",
    "pemerintah", "menteri", "undang", "pasal", "ayat", "butir", "huruf", "tahun",
    "nomor", "tanggal", "belum", "ada", "sesuai", "kurang", "perlu", "antara",
}


def _skills_dir() -> Path:
    return get_settings().skills_path


def _draft_dir() -> Path:
    return _skills_dir() / "_draft"


def _slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s-]", "", str(text).lower().strip())
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-ZÀ-ÿ]{3,}", str(text).lower()) if t not in _STOPWORD]


def _read_temuan(folder: Path) -> dict | None:
    p = folder / "_KKP" / "temuan.json"
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _temuan_items(data: dict) -> list[dict]:
    return data.get("temuan", []) if isinstance(data, dict) else []


def _temuan_text(t: dict) -> str:
    return " ".join(str(t.get(k, "")) for k in ("judul_temuan", "judul", "kondisi", "kriteria"))


def validate(kodes: list[str]) -> dict:
    """Validasi penugasan: punya temuan, skill sama. Return {ok, fungsi, skill, metas} / {ok:False, issues}."""
    metas: list[dict] = []
    issues: list[str] = []
    for kode in kodes:
        folder = penugasan_folder(kode)
        data = _read_temuan(folder)
        if data is None:
            issues.append(f"{kode}: _KKP/temuan.json tidak ada")
            continue
        items = _temuan_items(data)
        if not items:
            issues.append(f"{kode}: belum ada temuan")
            continue
        skill = (data.get("penugasan") or {}).get("jenis_pengawasan", "")
        metas.append({"kode": kode, "folder": folder, "skill": skill, "temuan": items})
    if not metas:
        return {"ok": False, "issues": issues or ["tidak ada penugasan valid"]}
    skills = {m["skill"] for m in metas}
    if len(skills) > 1:
        return {"ok": False, "issues": [f"skill berbeda antar penugasan: {skills} — graduasi harus 1 jenis"]}
    skill = skills.pop()
    fungsi = skill.split("-")[0] if skill else ""
    return {"ok": True, "fungsi": fungsi, "skill": skill, "metas": metas, "issues": issues}


def _domain_terms(metas: list[dict], top_k: int = 15) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for m in metas:
        for t in m["temuan"]:
            c.update(_tokenize(_temuan_text(t)))
    return c.most_common(top_k)


def _core_regulations(metas: list[dict]) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    pat = re.compile(r"(PP|PMK|Perpres|Perlem(?:\s*LKPP)?|PermenPAN[- ]?RB|Perka\s*BPKP|UU|SE)\s*[\w./-]*\s*\d+[/\s]*\d{0,4}", re.IGNORECASE)
    for m in metas:
        for t in m["temuan"]:
            for mm in pat.finditer(str(t.get("kriteria", ""))):
                c[mm.group(0).strip()] += 1
    return c.most_common(10)


def _consolidate_kriteria(metas: list[dict]) -> list[str]:
    seen: list[str] = []
    for m in metas:
        for t in m["temuan"]:
            k = str(t.get("kriteria", "")).strip()
            if k and k not in seen:
                seen.append(k)
    return seen


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _cluster_temuan(metas: list[dict], threshold: float = 0.4) -> list[dict]:
    """Kelompokkan temuan mirip (Jaccard token judul+kondisi) → kandidat red-flag."""
    flat = []
    for m in metas:
        for t in m["temuan"]:
            judul = t.get("judul_temuan") or t.get("judul") or ""
            toks = set(_tokenize(judul + " " + str(t.get("kondisi", ""))))
            flat.append({"judul": judul, "toks": toks, "kriteria": t.get("kriteria", "")})
    clusters: list[dict] = []
    used = [False] * len(flat)
    for i in range(len(flat)):
        if used[i]:
            continue
        group = [flat[i]]
        used[i] = True
        for j in range(i + 1, len(flat)):
            if not used[j] and _jaccard(flat[i]["toks"], flat[j]["toks"]) >= threshold:
                group.append(flat[j])
                used[j] = True
        clusters.append({
            "judul": group[0]["judul"],
            "frekuensi": len(group),
            "kriteria": group[0]["kriteria"],
        })
    clusters.sort(key=lambda x: x["frekuensi"], reverse=True)
    return clusters


def list_drafts() -> list[dict]:
    base = _draft_dir()
    out: list[dict] = []
    if base.exists():
        for d in sorted(base.iterdir()):
            if d.is_dir() and (d / "SKILL.md").is_file():
                meta = {}
                mp = d / "meta.json"
                if mp.is_file():
                    try:
                        meta = json.loads(mp.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, OSError):
                        meta = {}
                out.append({"nama": d.name, **{k: meta.get(k) for k in ("fungsi", "skill_induk", "sumber_penugasan", "generated_at", "n_temuan")}})
    return out


def generate_draft(kodes: list[str], nama: str | None = None) -> dict:
    """Gate 0-4: validasi → domain → konsolidasi → cluster → tulis draft. Return ringkasan/err."""
    v = validate(kodes)
    if not v["ok"]:
        return {"ok": False, "issues": v["issues"]}
    metas, fungsi, skill_induk = v["metas"], v["fungsi"], v["skill"]
    terms = _domain_terms(metas)
    regs = _core_regulations(metas)
    kriteria = _consolidate_kriteria(metas)
    clusters = _cluster_temuan(metas)
    n_temuan = sum(len(m["temuan"]) for m in metas)

    if not nama:
        top = "-".join(t for t, _ in terms[:2]) or "spesifik"
        nama = _slug(f"{fungsi}-{top}")
    nama = _slug(nama)
    target = _draft_dir() / nama
    if target.exists():
        return {"ok": False, "issues": [f"draft '{nama}' sudah ada — promote/reject dulu, atau pakai nama lain"]}
    (target / "references").mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow().isoformat() + "Z"
    # SKILL.md (DRAFT)
    skill_md = f"""---
name: {nama}
version: 0.1-draft
status: DRAFT
jenis: "Skill spesifik hasil graduasi dari {skill_induk}"
fungsi: {fungsi}
parent_skill: {skill_induk}
model: claude-sonnet-4-6
---

# Skill (DRAFT): {nama}

> ⚠️ **DRAFT hasil graduasi otomatis** dari {len(metas)} penugasan ({n_temuan} temuan).
> WAJIB direviu auditor sebelum di-*promote* ke `knowledge/skills/`.

## Identitas
- **Skill induk:** `{skill_induk}` (criteria-driven umum)
- **Fungsi:** {fungsi}
- **Disuling dari:** {", ".join(m["kode"] for m in metas)}

## Domain (term dominan)
{", ".join(f"{t} ({n})" for t, n in terms) or "-"}

## Cara pakai
Ikuti workflow skill induk `{skill_induk}` (lihat SKILL.md-nya), dengan fokus
kriteria & pola red-flag di bawah (references/). Format laporan mengikuti induk.

## References
- `references/01-regulasi.md` — kriteria/regulasi yang berulang
- `references/02-checklist-redflag.md` — pola temuan (kandidat red-flag)
"""
    (target / "SKILL.md").write_text(skill_md, encoding="utf-8")

    reg_md = "# Regulasi & Kriteria Berulang (draft graduasi)\n\n"
    if regs:
        reg_md += "## Regulasi inti (frekuensi)\n" + "\n".join(f"- {r} ({n})" for r, n in regs) + "\n\n"
    reg_md += "## Kriteria terkonsolidasi\n" + ("\n".join(f"- {k}" for k in kriteria) or "- (belum ada)")
    (target / "references" / "01-regulasi.md").write_text(reg_md + "\n", encoding="utf-8")

    cl_md = "# Checklist Red-Flag (kandidat, draft graduasi)\n\n"
    cl_md += "| Pola Temuan | Frekuensi | Kriteria |\n|---|---|---|\n"
    for c in clusters:
        cl_md += f"| {c['judul']} | {c['frekuensi']} | {str(c['kriteria'])[:80]} |\n"
    (target / "references" / "02-checklist-redflag.md").write_text(cl_md, encoding="utf-8")

    meta = {
        "nama": nama, "fungsi": fungsi, "skill_induk": skill_induk,
        "sumber_penugasan": [m["kode"] for m in metas], "n_temuan": n_temuan,
        "n_kriteria": len(kriteria), "n_redflag": len(clusters), "generated_at": now,
        "status": "DRAFT",
    }
    (target / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "nama": nama, **meta, "warnings": v.get("issues", [])}


def promote(nama: str) -> dict:
    """Pindahkan draft → knowledge/skills/<nama> + refresh registry. Manual oleh auditor."""
    from app import skills_registry as sreg

    nama = _slug(nama)
    src = _draft_dir() / nama
    if not (src / "SKILL.md").is_file():
        return {"ok": False, "error": f"draft '{nama}' tidak ada"}
    dst = _skills_dir() / nama
    if dst.exists():
        return {"ok": False, "error": f"skill '{nama}' sudah ada di registry"}
    # bump status DRAFT → ACTIVE di SKILL.md
    md = src / "SKILL.md"
    try:
        txt = md.read_text(encoding="utf-8").replace("status: DRAFT", "status: ACTIVE", 1)
        md.write_text(txt, encoding="utf-8")
    except OSError:
        pass
    shutil.move(str(src), str(dst))
    sreg.refresh()
    return {"ok": True, "nama": nama, "skill_terdaftar": sreg.skill_exists(nama)}


def reject(nama: str) -> dict:
    nama = _slug(nama)
    src = _draft_dir() / nama
    if not src.exists():
        return {"ok": False, "error": f"draft '{nama}' tidak ada"}
    shutil.rmtree(src, ignore_errors=True)
    return {"ok": True, "nama": nama}
