#!/usr/bin/env python3
"""
graduasi.py — Auto-generate skill spesifik dari penugasan yang dikerjakan dengan skill umum.

Usage:
    python graduasi.py --penugasan ID1 [ID2 ...] [--nama NAMA_SKILL] [--root PATH] [--no-script]
    python graduasi.py --promote NAMA_SKILL [--root PATH]
    python graduasi.py --reject NAMA_SKILL [--root PATH]
    python graduasi.py --list

Workflow gate-based (lihat audit-system-v4/skills/graduasi-skill-spesifik/SKILL.md):
    Gate 0: validasi input penugasan
    Gate 1: deteksi domain & penamaan
    Gate 2: konsolidasi kriteria
    Gate 3: mining pola temuan & red flag
    Gate 4: generate skill draft di skills/_draft/<nama>/
    Gate 5: review & promote (manual oleh auditor)

Catatan: script ini adalah orchestrator; analisis bahasa alami dilakukan oleh Claude
(skill graduasi-skill-spesifik) yang memanggil script ini untuk operasi deterministik
(scan folder, parse JSON/XLSX, hitung frekuensi, tulis file).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# ----------------------------------------------------------------------
# Konstanta & helper
# ----------------------------------------------------------------------

DEFAULT_ROOT = Path("audit-system-v4")
SKILLS_DIR = "skills"
DRAFT_DIR = "_draft"
PENUGASAN_DIR = "penugasan"
GRADUASI_LOG = "feedback/graduasi-log.json"

VALID_FUNGSI = {"audit", "reviu", "pemantauan", "evaluasi", "konsultansi"}
PARENT_SKILL_BY_FUNGSI = {f: f"{f}-umum" for f in VALID_FUNGSI}

STOPWORD_ID = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "atau", "adalah",
    "akan", "telah", "pada", "oleh", "dalam", "sebagai", "tidak", "ini",
    "itu", "juga", "dapat", "wajib", "harus", "sebagaimana", "dimaksud",
    "tersebut", "bagi", "kepada", "atas", "agar", "supaya", "jika", "apabila",
    "demikian", "maka", "peraturan", "pemerintah", "menteri", "undang",
    "pasal", "ayat", "butir", "huruf", "tahun", "nomor", "tanggal",
}

ISO_NOW = lambda: datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def warn(msg: str) -> None:
    print(f"⚠️  {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"ℹ️  {msg}")


def fail(msg: str, code: int = 1) -> "NoReturn":
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def slug(text: str) -> str:
    """Normalize to lowercase-dash-separated."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


# ----------------------------------------------------------------------
# Gate 0 — validasi input
# ----------------------------------------------------------------------

def find_penugasan(root: Path, pid: str) -> Path:
    p = root / PENUGASAN_DIR / pid
    if not p.exists():
        fail(f"Penugasan tidak ditemukan: {p}")
    return p


def validate_penugasan(p: Path) -> dict:
    """Pastikan penugasan punya KKP & LHP. Return metadata."""
    kkp = p / "_KKP"
    lhp = p / "_LHP"
    issues = []
    if not kkp.exists():
        issues.append(f"Folder _KKP tidak ada di {p}")
    if not lhp.exists():
        issues.append(f"Folder _LHP tidak ada di {p}")
    temuan_json = kkp / "temuan.json"
    if not temuan_json.exists():
        issues.append(f"_KKP/temuan.json tidak ada di {p}")
    if issues:
        return {"ok": False, "issues": issues, "path": p}

    try:
        data = json.loads(temuan_json.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "issues": [f"temuan.json invalid: {e}"], "path": p}

    skill = data.get("skill", "")
    fungsi = skill.split("-")[0] if "-umum" in skill else skill
    return {
        "ok": True,
        "path": p,
        "id": p.name,
        "skill": skill,
        "fungsi": fungsi,
        "data": data,
    }


def validate_inputs(root: Path, ids: list[str]) -> tuple[list[dict], str]:
    metas = []
    for pid in ids:
        p = find_penugasan(root, pid)
        meta = validate_penugasan(p)
        if not meta["ok"]:
            for it in meta["issues"]:
                warn(it)
            fail(f"Penugasan {pid} gagal validasi.")
        metas.append(meta)

    fungsi_set = {m["fungsi"] for m in metas}
    if len(fungsi_set) > 1:
        fail(
            f"Penugasan input pakai skill umum berbeda: {fungsi_set}. "
            "Graduasi lintas-fungsi tidak diizinkan."
        )
    fungsi = fungsi_set.pop()
    if fungsi not in VALID_FUNGSI:
        fail(f"Fungsi tidak dikenali: {fungsi}")
    return metas, fungsi


# ----------------------------------------------------------------------
# Gate 1 — deteksi domain & penamaan
# ----------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zA-ZÀ-ÿ]{3,}", text)
    return [t for t in tokens if t not in STOPWORD_ID]


def detect_domain_terms(metas: list[dict], top_k: int = 20) -> list[tuple[str, int]]:
    """Hitung term frequency dari kriteria semua penugasan."""
    counter: Counter[str] = Counter()
    for m in metas:
        kriteria_dir = m["path"] / "input" / "kriteria"
        if not kriteria_dir.exists():
            continue
        for f in kriteria_dir.rglob("*"):
            if f.suffix.lower() in {".txt", ".md"}:
                try:
                    counter.update(tokenize(f.read_text(encoding="utf-8", errors="ignore")))
                except Exception:
                    pass
        # juga tarik dari matriks-kriteria.xlsx via sheet "Matriks Kriteria" jika ada — diparse oleh Claude
        # (script ini hanya pakai sumber teks polos untuk deterministik)
        # JSON kriteria_terindeks juga sumber yang baik
        for entry in m["data"].get("kriteria_terindeks", []) or []:
            counter.update(tokenize(entry.get("kutipan", "")))
            counter.update(tokenize(entry.get("sumber", "")))
    return counter.most_common(top_k)


def detect_core_regulations(metas: list[dict]) -> list[tuple[str, int, float]]:
    """Hitung berapa penugasan memakai tiap sumber regulasi."""
    n = len(metas)
    src_counter: Counter[str] = Counter()
    for m in metas:
        sources = {
            (entry.get("sumber") or "").strip()
            for entry in (m["data"].get("kriteria_terindeks") or [])
        }
        for s in sources:
            if s:
                src_counter[s] += 1
    return [
        (src, cnt, cnt / n)
        for src, cnt in src_counter.most_common()
    ]


def suggest_skill_name(fungsi: str, top_terms: list[tuple[str, int]]) -> str:
    if not top_terms:
        return f"{fungsi}-domain-baru"
    # Ambil 2-3 top term yang ber-arti
    picks = [t for t, _ in top_terms[:3]]
    topik = "-".join(picks[:2])
    return slug(f"{fungsi}-{topik}")


# ----------------------------------------------------------------------
# Gate 2 — konsolidasi kriteria
# ----------------------------------------------------------------------

def consolidate_kriteria(metas: list[dict]) -> list[dict]:
    """Kumpulkan semua kriteria, dedup pakai (sumber, pasal_butir), hitung usage_count."""
    n = len(metas)
    bucket: dict[tuple[str, str], dict] = {}
    for m in metas:
        seen_in_this = set()
        for entry in (m["data"].get("kriteria_terindeks") or []):
            key = (
                (entry.get("sumber") or "").strip(),
                (entry.get("pasal") or entry.get("pasal_butir") or "").strip(),
            )
            if not key[0]:
                continue
            if key not in bucket:
                bucket[key] = {
                    **entry,
                    "usage_count": 0,
                    "usage_penugasan": [],
                }
            if m["id"] not in seen_in_this:
                bucket[key]["usage_count"] += 1
                bucket[key]["usage_penugasan"].append(m["id"])
                seen_in_this.add(key)
    out = []
    for k, v in bucket.items():
        v["usage_persen"] = v["usage_count"] / n
        if v["usage_persen"] >= 0.8:
            v["tier"] = "core"
        elif v["usage_persen"] >= 0.5:
            v["tier"] = "frequent"
        else:
            v["tier"] = "optional"
        out.append(v)
    out.sort(key=lambda x: -x["usage_persen"])
    return out


# ----------------------------------------------------------------------
# Gate 3 — mining pola temuan & red flag
# ----------------------------------------------------------------------

NORM_PATTERNS = [
    (re.compile(r"rp\s*[\d\.,]+"), "<NILAI>"),
    (re.compile(r"\b\d{1,2}\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s+\d{4}\b", re.I), "<TANGGAL>"),
    (re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "<TANGGAL>"),
    (re.compile(r"[A-Za-z0-9_\-]+\.(pdf|docx|xlsx|doc|xls)\b", re.I), "<DOKUMEN>"),
    (re.compile(r"\b\d{2,}\b"), "<NUM>"),
]


def normalize_kondisi(text: str) -> str:
    t = text.lower()
    for patt, repl in NORM_PATTERNS:
        t = patt.sub(repl, t)
    return re.sub(r"\s+", " ", t).strip()


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def cluster_temuan(metas: list[dict], threshold: float = 0.5) -> list[dict]:
    """Kumpulkan semua temuan/catatan, normalisasi, cluster pakai jaccard."""
    items: list[dict] = []
    for m in metas:
        # Cari array temuan/catatan_reviu/items/pendapat
        d = m["data"]
        for key in ("temuan", "catatan_reviu", "items", "temuan_kksa", "pendapat"):
            arr = d.get(key)
            if isinstance(arr, list):
                for entry in arr:
                    kondisi = (
                        entry.get("kondisi")
                        or entry.get("catatan_akibat")
                        or entry.get("teks")
                        or entry.get("realisasi")
                        or entry.get("analisis")
                        or ""
                    )
                    if not kondisi:
                        continue
                    items.append({
                        "penugasan_id": m["id"],
                        "raw": kondisi,
                        "norm": normalize_kondisi(kondisi),
                        "tokens": set(normalize_kondisi(kondisi).split()),
                        "kriteria_ids": entry.get("kriteria_ids") or [],
                        "level_risiko": entry.get("level_risiko") or entry.get("status") or "",
                        "akibat": entry.get("akibat") or entry.get("catatan_akibat") or "",
                    })
                break  # hanya pakai field pertama yang valid

    clusters: list[list[dict]] = []
    for it in items:
        placed = False
        for cl in clusters:
            if any(jaccard(it["tokens"], member["tokens"]) >= threshold for member in cl):
                cl.append(it)
                placed = True
                break
        if not placed:
            clusters.append([it])

    # Aggregate
    out = []
    for cl in clusters:
        distinct_p = {it["penugasan_id"] for it in cl}
        all_kriteria = []
        for it in cl:
            all_kriteria.extend(it["kriteria_ids"])
        akibat_pool = [it["akibat"] for it in cl if it["akibat"]]
        out.append({
            "size": len(cl),
            "distinct_penugasan": len(distinct_p),
            "penugasan_ids": sorted(distinct_p),
            "kriteria_freq": Counter(all_kriteria).most_common(),
            "contoh_kondisi": cl[0]["raw"][:300],
            "pola_kondisi_norm": cl[0]["norm"][:300],
            "akibat_contoh": akibat_pool[0] if akibat_pool else "",
        })
    out.sort(key=lambda x: (-x["distinct_penugasan"], -x["size"]))
    return out


# ----------------------------------------------------------------------
# Gate 4 — generate skill draft
# ----------------------------------------------------------------------

SKILL_MD_TEMPLATE = """---
name: {nama}
version: 0.1
status: draft-pending-approval
jenis: {jenis_pengawasan}
fungsi: {fungsi_apip}
output: {format_output}
parent_skill: {parent_skill}
derived_from:
{derived_from_yaml}
generated_at: {generated_at}
generated_by: graduasi-skill-spesifik v1.0
model: claude-sonnet-4-6
---

# Skill: {nama_titel}

> **⚠️ STATUS DRAFT** — Skill ini hasil graduasi otomatis dari skill umum {parent_skill}.
> Wajib direview oleh auditor sebelum di-promote ke `skills/`.

## Identitas
- **Nama Skill:** {nama}
- **Versi:** 0.1 (draft hasil graduasi)
- **Domain:** {domain_titel}
- **Fungsi APIP:** {fungsi_apip}
- **Parent Skill:** {parent_skill}
- **Model AI:** Claude Sonnet 4.6

## Asal Skill (Audit Trail Graduasi)

Skill ini dihasilkan otomatis dari **{n_penugasan} penugasan** yang dikerjakan dengan skill umum **{parent_skill}**:

{tabel_penugasan_md}

**Statistik graduasi:**
- Regulasi core (≥80% pakai): **{n_core}** kriteria
- Regulasi pendukung (50–80%): **{n_frequent}** kriteria
- Red flag built-in (≥2 distinct penugasan): **{n_redflag}** pola
- Pipeline script: **{pipeline_status}**

## Kapan Skill Ini Digunakan

Skill ini cocok untuk pengawasan domain **{domain_titel}** dengan parent function **{fungsi_apip}**.

**Jangan gunakan ketika:**
- Topik di luar {domain_titel} → gunakan {parent_skill}

## Workflow

Mengikuti workflow gate-based parent skill ({parent_skill}) — lihat `audit-system-v4/skills/{parent_skill}/SKILL.md`.

**Perbedaan dari parent:**
- Kriteria utama sudah built-in di `references/01-regulasi-utama.md` dan `references/02-regulasi-pendukung.md`
- Checklist & red flag domain-specific tersedia di `references/03-checklist-redflag.md`
{tambahan_pipeline}

## Format Output

Sama dengan parent skill {parent_skill}.

## Referensi Wajib Dibaca
- `references/01-regulasi-utama.md` — core regulasi (frekuensi ≥80%)
- `references/02-regulasi-pendukung.md` — regulasi pendukung (50–80%)
- `references/03-checklist-redflag.md` — checklist & red flag built-in
- `audit-system-v4/skills/{parent_skill}/SKILL.md` — workflow dasar
- `audit-system-v4/skills/panduan-format-umum/PANDUAN.md` — format laporan

## Catatan Promote

Saat skill ini di-promote ke `skills/`:
1. Hapus banner ⚠️ STATUS DRAFT di atas
2. Update `version: 0.1` → `version: 1.0` di frontmatter
3. Hapus `status: draft-pending-approval` dari frontmatter
4. Update `audit-system-v4/skills/README-skills-umum.md` — tambah ke decision tree
5. Update `audit-system-v4/feedback/graduasi-log.json` (status → approved-promoted)
"""


def write_skill_md(target: Path, ctx: dict) -> None:
    derived = "\n".join(f"  - {pid}" for pid in ctx["penugasan_ids"])
    tabel = "\n".join(
        f"| {pid} | {tgl} | {obj} |"
        for pid, tgl, obj in ctx["penugasan_table"]
    )
    tabel_full = "| ID Penugasan | Tanggal | Objek |\n|---|---|---|\n" + tabel
    pipeline_status = "ada (skeleton)" if ctx["with_pipeline"] else "tidak (data <5 penugasan)"
    tambahan_pipeline = (
        "- Pipeline pre-digest tersedia di `scripts/digest.py` dan `scripts/cross_check.py`"
        if ctx["with_pipeline"] else ""
    )
    body = SKILL_MD_TEMPLATE.format(
        nama=ctx["nama"],
        nama_titel=ctx["nama"].replace("-", " ").title(),
        jenis_pengawasan=ctx["jenis_pengawasan"],
        fungsi_apip=ctx["fungsi_apip"],
        format_output=ctx["format_output"],
        parent_skill=ctx["parent_skill"],
        derived_from_yaml=derived,
        generated_at=ctx["generated_at"],
        domain_titel=ctx["domain_titel"],
        n_penugasan=len(ctx["penugasan_ids"]),
        tabel_penugasan_md=tabel_full,
        n_core=ctx["n_core"],
        n_frequent=ctx["n_frequent"],
        n_redflag=ctx["n_redflag"],
        pipeline_status=pipeline_status,
        tambahan_pipeline=tambahan_pipeline,
    )
    target.write_text(body, encoding="utf-8")


def write_regulasi_md(target: Path, kriteria: list[dict], judul: str) -> None:
    lines = [f"# {judul}", "", f"**Generated:** {ISO_NOW()}", ""]
    lines.append("| ID | Sumber | Pasal/Butir | Frekuensi | Kutipan |")
    lines.append("|---|---|---|---:|---|")
    for k in kriteria:
        kid = k.get("id", "—")
        src = k.get("sumber", "")
        psl = k.get("pasal", k.get("pasal_butir", ""))
        freq = f"{k.get('usage_count', 0)}/{int(round(k.get('usage_count',0)/max(k.get('usage_persen',0.0001),0.0001)))}"
        kutip = (k.get("kutipan", "") or "").replace("\n", " ").replace("|", "/")
        if len(kutip) > 200:
            kutip = kutip[:200] + "…"
        lines.append(f"| {kid} | {src} | {psl} | {freq} | {kutip} |")
    target.write_text("\n".join(lines), encoding="utf-8")


def write_checklist_redflag(target: Path, clusters: list[dict], n_total: int) -> None:
    lines = [
        "# Checklist & Red Flag Built-in",
        "",
        f"**Generated:** {ISO_NOW()}",
        f"**Total cluster temuan:** {len(clusters)}",
        f"**Sumber:** {n_total} penugasan",
        "",
        "---",
        "",
    ]
    redflags = [c for c in clusters if c["distinct_penugasan"] >= 2]
    if not redflags:
        lines.append("> Tidak ada cluster pola yang muncul di ≥2 penugasan.")
        lines.append("> Skill ini perlu lebih banyak penugasan untuk membangun red flag built-in.")
    for i, c in enumerate(redflags, 1):
        lines.append(f"## RF-{i:02d}")
        lines.append(f"- **Frekuensi**: {c['distinct_penugasan']} penugasan distinct (size cluster {c['size']})")
        lines.append(f"- **Penugasan sumber**: {', '.join(c['penugasan_ids'])}")
        if c["kriteria_freq"]:
            top = ", ".join(f"{k}({v})" for k, v in c["kriteria_freq"][:5])
            lines.append(f"- **Kriteria yang biasa dilanggar**: {top}")
        lines.append(f"- **Pola kondisi (normalisasi)**: `{c['pola_kondisi_norm']}`")
        lines.append(f"- **Contoh kondisi mentah**: {c['contoh_kondisi']}")
        if c["akibat_contoh"]:
            lines.append(f"- **Akibat khas**: {c['akibat_contoh'][:300]}")
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")


PIPELINE_DIGEST_PY = '''#!/usr/bin/env python3
"""digest.py — pre-digest untuk skill {nama} (skeleton hasil graduasi).

Sesuaikan dengan domain spesifik. Pola: scan folder → klasifikasi dokumen → emit JSON terstruktur.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--penugasan", required=True, help="Path folder penugasan")
    args = ap.parse_args()
    p = Path(args.penugasan)
    out = {{
        "skill": "{nama}",
        "penugasan": p.name,
        "dokumen": {{}},
        # TODO: implementasi klasifikasi dokumen sesuai domain
    }}
    target = p / "_KKP" / "{nama}-digest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {{target}}")

if __name__ == "__main__":
    main()
'''

PIPELINE_CROSSCHECK_PY = '''#!/usr/bin/env python3
"""cross_check.py — rule-based cross-check untuk skill {nama} (skeleton hasil graduasi).

Implementasikan rules deterministik dari red flag yang sudah dimining.
Lihat references/03-checklist-redflag.md untuk daftar pola.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

RULES = [
    # TODO: konversi tiap RF di references/03-checklist-redflag.md jadi rule programmatic
    # contoh:
    # {{"id": "RF-01", "aspek": "perencanaan", "check": lambda d: ...}},
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--penugasan", required=True)
    args = ap.parse_args()
    p = Path(args.penugasan)
    digest = json.loads((p / "_KKP" / "{nama}-digest.json").read_text(encoding="utf-8"))
    anomalies = []
    for rule in RULES:
        # TODO: jalankan rule
        pass
    target = p / "_KKP" / "{nama}-anomalies.json"
    target.write_text(json.dumps(anomalies, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {{target}} ({{len(anomalies)}} anomali)")

if __name__ == "__main__":
    main()
'''


def write_pipeline_skeleton(scripts_dir: Path, nama: str) -> None:
    scripts_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "digest.py").write_text(PIPELINE_DIGEST_PY.format(nama=nama), encoding="utf-8")
    (scripts_dir / "cross_check.py").write_text(PIPELINE_CROSSCHECK_PY.format(nama=nama), encoding="utf-8")
    (scripts_dir / "README.md").write_text(
        f"# Pipeline {nama} (skeleton)\n\n"
        "Skeleton script otomatis dari graduasi.\n\n"
        "Implementasikan TODO di digest.py & cross_check.py sebelum dipakai.\n",
        encoding="utf-8",
    )


def write_metadata(target: Path, ctx: dict) -> None:
    meta = {
        "nama_skill": ctx["nama"],
        "parent_skill": ctx["parent_skill"],
        "domain": ctx["domain_titel"],
        "tingkat_graduasi": ctx["tingkat"],
        "penugasan_sumber": ctx["penugasan_ids"],
        "statistik": {
            "n_penugasan": len(ctx["penugasan_ids"]),
            "n_kriteria_core": ctx["n_core"],
            "n_kriteria_frequent": ctx["n_frequent"],
            "n_redflag": ctx["n_redflag"],
        },
        "with_pipeline": ctx["with_pipeline"],
        "generated_at": ctx["generated_at"],
        "status": "draft-pending-approval",
        "promoted_at": None,
        "promoted_to": None,
        "reviewer": None,
    }
    target.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def append_graduasi_log(root: Path, entry: dict) -> None:
    log_path = root / GRADUASI_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        try:
            log = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            log = []
    else:
        log = []
    log.append(entry)
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


# ----------------------------------------------------------------------
# Promote / reject
# ----------------------------------------------------------------------

def promote(root: Path, nama: str) -> None:
    src = root / SKILLS_DIR / DRAFT_DIR / nama
    dst = root / SKILLS_DIR / nama
    if not src.exists():
        fail(f"Draft tidak ditemukan: {src}")
    if dst.exists():
        fail(f"Skill aktif dengan nama yang sama sudah ada: {dst}")
    shutil.move(str(src), str(dst))
    # Update SKILL.md: hapus banner draft, ubah status & version (manual edit recommended;
    # script ini hanya catat di log)
    info(f"Promoted: {src} → {dst}")
    info("⚠️  Edit manual SKILL.md: hapus banner DRAFT, ubah version: 0.1 → 1.0, hapus status field.")
    log_path = root / GRADUASI_LOG
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
        for e in log:
            if e.get("nama_skill") == nama and e.get("status") == "draft-pending-approval":
                e["status"] = "approved-promoted"
                e["promoted_at"] = ISO_NOW()
                e["promoted_to"] = str(dst.relative_to(root))
        log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def reject(root: Path, nama: str) -> None:
    src = root / SKILLS_DIR / DRAFT_DIR / nama
    if not src.exists():
        fail(f"Draft tidak ditemukan: {src}")
    shutil.rmtree(src)
    info(f"Rejected & removed: {src}")
    log_path = root / GRADUASI_LOG
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
        for e in log:
            if e.get("nama_skill") == nama and e.get("status") == "draft-pending-approval":
                e["status"] = "rejected"
        log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def list_drafts(root: Path) -> None:
    draft_root = root / SKILLS_DIR / DRAFT_DIR
    if not draft_root.exists():
        info("Tidak ada draft skill (folder _draft/ belum dibuat).")
        return
    drafts = [
        d for d in sorted(draft_root.iterdir())
        if d.is_dir() and not d.name.startswith(".")
    ]
    if not drafts:
        info("Tidak ada draft skill.")
        return
    info(f"Daftar draft skill ({len(drafts)} item):")
    for d in drafts:
        meta_path = d / "METADATA.md"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                info(f"  📦 {d.name} | tingkat: {meta.get('tingkat_graduasi')} | "
                     f"sumber: {len(meta.get('penugasan_sumber', []))} penugasan | "
                     f"status: {meta.get('status')}")
            except Exception:
                info(f"  📦 {d.name} (METADATA.md korup)")
        else:
            info(f"  📦 {d.name} (tanpa METADATA)")


# ----------------------------------------------------------------------
# Orchestrator
# ----------------------------------------------------------------------

PARENT_LABEL = {
    "audit": ("Audit", "Assurance — Keyakinan Memadai", "LHA + KKA + JSON"),
    "reviu": ("Reviu", "Assurance — Keyakinan Terbatas", "LHR + KKR + JSON"),
    "pemantauan": ("Pemantauan", "Assurance — Status & Progres", "LHPemantauan + KKM + JSON"),
    "evaluasi": ("Evaluasi", "Assurance — Penilaian Substantif", "LHE + KKE + JSON"),
    "konsultansi": ("Konsultansi", "Consulting — Pendapat / Saran", "Memo Konsultasi + JSON"),
}


def graduate(root: Path, ids: list[str], nama_override: str | None, with_pipeline_flag: bool | None) -> None:
    info(f"Gate 0: validasi {len(ids)} penugasan...")
    metas, fungsi = validate_inputs(root, ids)
    parent_skill = PARENT_SKILL_BY_FUNGSI[fungsi]
    label = PARENT_LABEL[fungsi]

    info("Gate 1: deteksi domain...")
    top_terms = detect_domain_terms(metas)
    core_regs = detect_core_regulations(metas)
    nama = nama_override or suggest_skill_name(fungsi, top_terms)
    nama = slug(nama)
    if not nama.startswith(f"{fungsi}-"):
        nama = f"{fungsi}-{nama}"
    info(f"  Top terms: {[t for t,_ in top_terms[:5]]}")
    info(f"  Regulasi inti (≥80%): {[s for s,_,p in core_regs if p >= 0.8]}")
    info(f"  Nama skill diusulkan: {nama}")

    # Cek konflik
    if (root / SKILLS_DIR / nama).exists():
        fail(f"Skill aktif dengan nama '{nama}' sudah ada. Pilih nama lain via --nama.")
    if (root / SKILLS_DIR / DRAFT_DIR / nama).exists():
        fail(f"Draft '{nama}' sudah ada. Hapus dulu (--reject {nama}) atau pilih nama lain.")

    info("Gate 2: konsolidasi kriteria...")
    konsol = consolidate_kriteria(metas)
    core_k = [k for k in konsol if k["tier"] == "core"]
    freq_k = [k for k in konsol if k["tier"] == "frequent"]
    info(f"  Core: {len(core_k)} | Frequent: {len(freq_k)} | Optional: {len(konsol)-len(core_k)-len(freq_k)}")

    info("Gate 3: mining pola temuan...")
    clusters = cluster_temuan(metas)
    redflags = [c for c in clusters if c["distinct_penugasan"] >= 2]
    info(f"  Clusters total: {len(clusters)} | Red flag (≥2 distinct): {len(redflags)}")

    # Tingkat graduasi
    n = len(metas)
    if with_pipeline_flag is None:
        with_pipeline = (n >= 5)
    else:
        with_pipeline = with_pipeline_flag
    if n == 1:
        tingkat = "minimum"
    elif n < 5:
        tingkat = "standar"
    else:
        tingkat = "penuh"
    info(f"Tingkat graduasi: {tingkat} (with_pipeline={with_pipeline})")

    info(f"Gate 4: tulis draft di skills/_draft/{nama}/")
    target = root / SKILLS_DIR / DRAFT_DIR / nama
    (target / "references").mkdir(parents=True, exist_ok=True)
    (target / "templates").mkdir(parents=True, exist_ok=True)

    ctx = {
        "nama": nama,
        "domain_titel": nama.removeprefix(f"{fungsi}-").replace("-", " ").title(),
        "fungsi_apip": label[1],
        "jenis_pengawasan": f"{label[0]} (spesifik domain hasil graduasi)",
        "format_output": label[2],
        "parent_skill": parent_skill,
        "penugasan_ids": [m["id"] for m in metas],
        "penugasan_table": [(m["id"], "—", "—") for m in metas],  # tanggal/objek diisi auditor saat review
        "n_core": len(core_k),
        "n_frequent": len(freq_k),
        "n_redflag": len(redflags),
        "with_pipeline": with_pipeline,
        "tingkat": tingkat,
        "generated_at": ISO_NOW(),
    }

    write_skill_md(target / "SKILL.md", ctx)
    if core_k:
        write_regulasi_md(target / "references" / "01-regulasi-utama.md", core_k, "Regulasi Utama (Core ≥80%)")
    else:
        (target / "references" / "01-regulasi-utama.md").write_text(
            "# Regulasi Utama\n\n> Belum ada kriteria yang dipakai di ≥80% penugasan sumber. Auditor harus mengisi manual.\n",
            encoding="utf-8",
        )
    if freq_k:
        write_regulasi_md(target / "references" / "02-regulasi-pendukung.md", freq_k, "Regulasi Pendukung (Frequent 50–80%)")
    else:
        (target / "references" / "02-regulasi-pendukung.md").write_text(
            "# Regulasi Pendukung\n\n> Belum ada kriteria di rentang 50–80%. Auditor dapat menambahkan manual.\n",
            encoding="utf-8",
        )
    write_checklist_redflag(target / "references" / "03-checklist-redflag.md", clusters, n)
    if with_pipeline:
        write_pipeline_skeleton(target / "scripts", nama)
    write_metadata(target / "METADATA.md", ctx)

    # Templates xlsx/docx — pakai placeholder (Claude/skill akan generate via openpyxl/python-docx jika diminta)
    (target / "templates" / "README.md").write_text(
        "# Templates\n\nKKA-template.xlsx dan LHA-skeleton.docx diisi saat skill di-promote.\n"
        "Auditor dapat menyalin template dari `audit-system-v4/templates/` yang relevan.\n",
        encoding="utf-8",
    )

    append_graduasi_log(root, {
        "timestamp": ctx["generated_at"],
        "nama_skill": nama,
        "parent_skill": parent_skill,
        "penugasan_sumber": ctx["penugasan_ids"],
        "tingkat_graduasi": tingkat,
        "with_pipeline": with_pipeline,
        "status": "draft-pending-approval",
        "promoted_at": None,
        "promoted_to": None,
    })

    info("")
    info(f"✅ Draft selesai: {target}")
    info("")
    info("Langkah berikut (manual oleh auditor):")
    info(f"  1. Review SKILL.md, references/, dan METADATA.md di {target}")
    info("  2. Edit/refine red flag dan template — buang false positive")
    info(f"  3. Promote: python graduasi.py --promote {nama}")
    info(f"  4. Reject:  python graduasi.py --reject {nama}")


# ----------------------------------------------------------------------
# Discovery — kandidat untuk batch graduasi (mode mingguan/bulanan)
# ----------------------------------------------------------------------

def _load_graduasi_log(root: Path) -> list[dict]:
    log_path = root / GRADUASI_LOG
    if not log_path.exists():
        return []
    try:
        return json.loads(log_path.read_text(encoding="utf-8"))
    except Exception:
        return []


def _already_graduated(log: list[dict], pid: str) -> list[str]:
    """Return daftar nama_skill yang sudah pernah pakai penugasan ini."""
    out = []
    for e in log:
        if pid in (e.get("penugasan_sumber") or []):
            out.append(f"{e.get('nama_skill')} ({e.get('status')})")
    return out


def find_candidates(root: Path) -> dict:
    """Scan semua penugasan, kelompokkan kandidat graduasi per parent skill umum."""
    pen_root = root / PENUGASAN_DIR
    log = _load_graduasi_log(root)
    by_fungsi: dict[str, list[dict]] = {f: [] for f in VALID_FUNGSI}
    skipped: list[dict] = []

    if not pen_root.exists():
        return {"by_fungsi": by_fungsi, "skipped": skipped, "total": 0, "log": log}

    for p in sorted(pen_root.iterdir()):
        if not p.is_dir() or p.name.startswith("_") or p.name.startswith("."):
            continue
        meta = validate_penugasan(p)
        if not meta["ok"]:
            skipped.append({"id": p.name, "alasan": "; ".join(meta["issues"])[:120]})
            continue
        skill = meta["skill"] or ""
        # Hanya graduate dari skill umum
        if not skill.endswith("-umum"):
            skipped.append({"id": p.name, "alasan": f"skill: {skill or '(kosong)'} — bukan skill umum"})
            continue
        fungsi = meta["fungsi"]
        if fungsi not in VALID_FUNGSI:
            skipped.append({"id": p.name, "alasan": f"fungsi tidak dikenali: {fungsi}"})
            continue

        # Tanggal selesai (proksi: mtime _LHP/ atau _KKP/temuan.json)
        try:
            mtime = max(
                (p / "_LHP").stat().st_mtime if (p / "_LHP").exists() else 0,
                (p / "_KKP" / "temuan.json").stat().st_mtime,
            )
            tgl = datetime.fromtimestamp(mtime).date().isoformat()
        except Exception:
            tgl = "—"

        # Objek (proksi: dari temuan.json kalau ada)
        objek = (
            (meta["data"].get("objek")
             or meta["data"].get("ringkasan")
             or "—")
        )
        if isinstance(objek, dict):
            objek = objek.get("nama") or "—"

        prev_grad = _already_graduated(log, p.name)

        by_fungsi[fungsi].append({
            "id": p.name,
            "tgl_selesai": tgl,
            "objek": str(objek)[:80],
            "previous_graduations": prev_grad,
        })

    # Sort tiap kelompok by tanggal asc
    for f in by_fungsi:
        by_fungsi[f].sort(key=lambda x: x["tgl_selesai"])

    total = sum(len(v) for v in by_fungsi.values())
    return {"by_fungsi": by_fungsi, "skipped": skipped, "total": total, "log": log}


def print_candidates(root: Path, only_unscheduled: bool = False) -> None:
    """Tampilkan kandidat batch graduasi. only_unscheduled=True menyembunyikan yang sudah promoted."""
    res = find_candidates(root)
    by_fungsi = res["by_fungsi"]
    today = datetime.now().date().isoformat()

    info(f"Kandidat graduasi (scan tanggal {today}):")
    info("")

    for fungsi in ("audit", "reviu", "pemantauan", "evaluasi", "konsultansi"):
        items = by_fungsi[fungsi]
        # Filter yang sudah pernah promoted (jika diminta)
        if only_unscheduled:
            items = [
                it for it in items
                if not any("approved-promoted" in s for s in it["previous_graduations"])
            ]
        parent = PARENT_SKILL_BY_FUNGSI[fungsi]

        if not items:
            info(f"📋 {parent} (0 kandidat)")
            continue

        info(f"📋 {parent} ({len(items)} kandidat):")
        for it in items:
            prev_marker = ""
            if it["previous_graduations"]:
                prev_marker = f"  [riwayat: {', '.join(it['previous_graduations'])}]"
            info(f"  - {it['id']} — {it['tgl_selesai']} — {it['objek']}{prev_marker}")

        # Saran command
        if len(items) >= 1:
            ids_str = " ".join(it["id"] for it in items)
            tier = "minimum" if len(items) == 1 else "standar" if len(items) < 5 else "penuh"
            info(f"  → Tingkat: {tier} | Saran command:")
            info(f"     graduasi.py --penugasan {ids_str} --nama {fungsi}-<topik>")
        info("")

    if res["skipped"]:
        info(f"Dilewati ({len(res['skipped'])}):")
        for s in res["skipped"][:10]:
            info(f"  - {s['id']}: {s['alasan']}")
        if len(res["skipped"]) > 10:
            info(f"  ... dan {len(res['skipped']) - 10} lainnya")
        info("")

    info(f"Total kandidat valid: {res['total']}")
    info("")
    info("💡 Mode batch — direkomendasikan dijalankan per minggu (Jumat sore) atau per bulan.")
    info("   Pisahkan sesi graduasi dari sesi penugasan agar workflow penugasan tetap cepat.")


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Graduasi skill spesifik dari penugasan (mode batch direkomendasikan: mingguan/bulanan)"
    )
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="Root audit-system-v4 (default: audit-system-v4)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--penugasan", nargs="+", help="ID penugasan sumber (≥1) — eksekusi graduasi")
    g.add_argument("--promote", help="Promote draft ke skills/")
    g.add_argument("--reject", help="Reject draft (hapus folder)")
    g.add_argument("--list", action="store_true", help="Daftar draft yang ada")
    g.add_argument("--candidates", action="store_true", help="Scan kandidat batch graduasi (untuk sesi mingguan/bulanan)")
    ap.add_argument("--only-unscheduled", action="store_true", help="Filter: sembunyikan penugasan yang sudah pernah jadi sumber graduasi promoted")
    ap.add_argument("--nama", help="Override nama skill (default: auto-suggest)")
    ap.add_argument("--no-script", action="store_true", help="Jangan generate pipeline meski data ≥5")
    ap.add_argument("--force-script", action="store_true", help="Paksa generate pipeline meski data <5")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    if not root.exists():
        fail(f"Root tidak ditemukan: {root}")

    if args.list:
        list_drafts(root)
        return
    if args.candidates:
        print_candidates(root, only_unscheduled=args.only_unscheduled)
        return
    if args.promote:
        promote(root, args.promote)
        return
    if args.reject:
        reject(root, args.reject)
        return
    if args.penugasan:
        with_pipe = None
        if args.no_script:
            with_pipe = False
        if args.force_script:
            with_pipe = True
        graduate(root, args.penugasan, args.nama, with_pipe)


if __name__ == "__main__":
    main()
