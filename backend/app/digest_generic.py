"""Digest GENERIK deterministik untuk skill yang tidak punya pipeline V6 khusus.

Skill spesifik (reviu-rka-kl, reviu-pengadaan, audit-pengadaan) sudah punya
pipeline V6 dengan parser bersangkutan (digest_tor, digest_rab, digest_pengadaan).
14 skill lain (audit-kinerja, evaluasi-*, kepatuhan-saipi, konsultansi-umum,
konsultasi-pengadaan, pemantauan-*, audit-umum, reviu-umum) bersifat
criteria-driven — agen baca dokumen objek + kriteria langsung.

Tanpa digest, agen baca PDF mentah halaman per halaman → boros token + lambat
(estimasi 50K-200K tokens/penugasan untuk 5-10 dokumen).

Digest generik ini:
  - Ekstrak teks via LiteParse (deterministik, cepat: 1-3 ms/halaman PDF)
  - Klasifikasi jenis dokumen dari nama file + lokasi subfolder
  - Output JSON ringkas per file: { jenis, file, halaman_total, ringkasan,
    kata_kunci, tanggal_terdeteksi, regulasi_terdeteksi, ... }
  - Cap ringkasan teks ~6K char (~1.5K tokens) — kalau agen butuh detail
    spesifik, dia bisa read_pdf_page langsung ke halaman yang relevan.

Tidak panggil LLM. Pure deterministik.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# Skill yang SUDAH punya pipeline V6 khusus — digest generik di-skip untuk ini.
_SKILL_WITH_NATIVE_DIGEST = {
    "reviu-rka-kl",
    "reviu-pengadaan",
    "audit-pengadaan",
}


# Klasifikasi jenis dokumen berbasis pattern nama file + folder.
# Order matters — pattern lebih spesifik lebih dulu.
_JENIS_PATTERNS: list[tuple[str, list[re.Pattern]]] = [
    # Dokumen Surat Tugas & administrasi
    ("ST", [
        re.compile(r"\b(?:Signed_|TTD_)?ST[\s_\-]\d+", re.IGNORECASE),
        re.compile(r"surat[\s_\-]*tugas", re.IGNORECASE),
    ]),
    ("KP", [
        re.compile(r"\bKP[\s_\-]\d+", re.IGNORECASE),
        re.compile(r"kartu[\s_\-]*penugasan", re.IGNORECASE),
    ]),
    ("PKP", [
        re.compile(r"\bPKP[\s_\-]", re.IGNORECASE),
        re.compile(r"program[\s_\-]*kerja[\s_\-]*peng", re.IGNORECASE),
    ]),
    # Kriteria/regulasi
    ("KRITERIA", [
        re.compile(r"krit(?:eria)?[\s_\-]", re.IGNORECASE),
        re.compile(r"kuesioner|checklist|indikator", re.IGNORECASE),
        re.compile(r"perlem|permen|perka|perpres|pp[\s_\-]\d+|uu[\s_\-]\d+", re.IGNORECASE),
        re.compile(r"\bsop\b|standar[\s_\-]*operasional", re.IGNORECASE),
    ]),
    # Objek pengawasan
    ("OBJEK", [
        re.compile(r"obj(?:ek)?[\s_\-]|objek", re.IGNORECASE),
        re.compile(r"renja|renstra|rkt|perjanjian[\s_\-]*kinerja|pk[\s_\-]\d+", re.IGNORECASE),
        re.compile(r"lkj[\s_\-]?ip|laporan[\s_\-]*kinerja|lakip", re.IGNORECASE),
    ]),
    # Notulen / berita acara / rapat
    ("NOTULEN", [
        re.compile(r"notul(?:en)?|berita[\s_\-]*acara|risalah|minutes|moм", re.IGNORECASE),
        re.compile(r"\bba[\s_\-]\d+", re.IGNORECASE),
    ]),
    # SK / penetapan
    ("SK", [
        re.compile(r"\bsk[\s_\-]|surat[\s_\-]*keputusan", re.IGNORECASE),
        re.compile(r"penetapan", re.IGNORECASE),
    ]),
    # LKE Excel (untuk SPIP/SAKIP/RB)
    ("LKE", [
        re.compile(r"lke|lembar[\s_\-]*kerja[\s_\-]*eval", re.IGNORECASE),
        re.compile(r"penilaian[\s_\-]*mand", re.IGNORECASE),
    ]),
    # Bukti pelaksanaan (foto, laporan progres)
    ("BUKTI", [
        re.compile(r"bukti|evidence|foto|dokumentasi", re.IGNORECASE),
        re.compile(r"progres|kemajuan|capaian", re.IGNORECASE),
    ]),
    # Tindak lanjut hasil pemeriksaan
    ("TLHP", [
        re.compile(r"tlhp|tindak[\s_\-]*lanjut|monitoring", re.IGNORECASE),
        re.compile(r"matriks[\s_\-]*tl|rekap[\s_\-]*tl", re.IGNORECASE),
    ]),
]

# Folder → jenis hint (fallback)
_FOLDER_JENIS_HINT = {
    "00-input": "OBJEK",  # umumnya dokumen objek pengawasan
    "00-surat-tugas": "ST",
    "01-peraturan-internal": "KRITERIA",
    "02-kontrak": "KONTRAK",
    "03-perencanaan": "PERENCANAAN",
    "04-pelaksanaan": "PELAKSANAAN",
    "05-keuangan": "KEUANGAN",
}


def classify_dokumen(file_path: Path) -> str:
    """Klasifikasi jenis dokumen dari nama file + folder. Best-effort.

    Return: kode jenis (ST/KP/PKP/KRITERIA/OBJEK/NOTULEN/SK/LKE/BUKTI/TLHP/...)
    atau 'OTHER' bila tidak match pattern apa pun.
    """
    name = file_path.stem  # tanpa ekstensi
    name_clean = re.sub(r"^(?:Signed_|TTD_|eMaterai_|Paraf_|approved_)", "", name, flags=re.IGNORECASE)

    # Coba match pattern nama dulu (urutan: spesifik → umum)
    for jenis, patterns in _JENIS_PATTERNS:
        for pat in patterns:
            if pat.search(name_clean):
                return jenis

    # Fallback: folder hint
    parent = file_path.parent.name.lower()
    if parent in _FOLDER_JENIS_HINT:
        return _FOLDER_JENIS_HINT[parent]

    return "OTHER"


# ---------------------------------------------------------------------------
# Text-level extraction helpers (deterministik, no LLM)
# ---------------------------------------------------------------------------

_REGULATION_RE = re.compile(
    r"\b("
    r"UU(?:D)?\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"PP\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"Perpres\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"Permen(?:pan(?:\s*RB)?|keu|kominfo|komdigi)?\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"Perka(?:ban)?\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"Perlem\s*LKPP\s*(?:No\.?\s*|Nomor\s*)?\d+(?:\s*[/Tahun]+\s*\d{4})?|"
    r"PMK\s*(?:No\.?\s*|Nomor\s*)?\d+(?:[/PMK\.\d]+)?\s*(?:Tahun\s*)?\d{4}?"
    r")\b",
    re.IGNORECASE,
)

_DATE_RE = re.compile(
    r"\b(\d{1,2})\s+"
    r"(Jan(?:uari)?|Feb(?:ruari)?|Mar(?:et)?|Apr(?:il)?|Mei|Jun(?:i)?|Jul(?:i)?|"
    r"Agu(?:stus)?|Sep(?:tember)?|Okt(?:ober)?|Nov(?:ember)?|Des(?:ember)?)"
    r"\s+(\d{4})\b",
    re.IGNORECASE,
)

_RUPIAH_RE = re.compile(r"Rp\.?\s*[\d.,]+(?:\s*\(.+?\))?")


def extract_keywords(text: str, max_items: int = 15) -> list[str]:
    """Heuristic keyword extraction: capitalize 2-4 grams + filter stopword."""
    # Ambil frasa berhuruf kapital (≥2 kata berturut-turut, mis. "Pusat Data Nasional")
    cap_phrases = re.findall(
        r"(?:[A-Z][a-z]+\s+){1,3}[A-Z][a-z]+", text,
    )
    seen: dict[str, int] = {}
    for p in cap_phrases:
        p = p.strip()
        if len(p) > 60 or len(p.split()) > 5:
            continue
        seen[p] = seen.get(p, 0) + 1
    # Sort by frequency desc, lalu alfabetik
    sorted_kw = sorted(seen.items(), key=lambda x: (-x[1], x[0]))
    return [k for k, _ in sorted_kw[:max_items]]


def extract_regulasi(text: str, max_items: int = 10) -> list[str]:
    """Tarik daftar regulasi (UU, PP, Perpres, Permen, dll). Dedup."""
    seen: dict[str, None] = {}
    for m in _REGULATION_RE.finditer(text):
        norm = re.sub(r"\s+", " ", m.group(1)).strip()
        if norm not in seen:
            seen[norm] = None
            if len(seen) >= max_items:
                break
    return list(seen.keys())


def extract_tanggal_iso(text: str, max_items: int = 10) -> list[str]:
    """Tarik tanggal Indonesia → ISO YYYY-MM-DD. Dedup, urut waktu."""
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6,
        "jul": 7, "agu": 8, "sep": 9, "okt": 10, "nov": 11, "des": 12,
    }
    out: list[str] = []
    seen: set[str] = set()
    for m in _DATE_RE.finditer(text):
        d, mon, y = m.group(1), m.group(2)[:3].lower(), m.group(3)
        mm = months.get(mon)
        if not mm:
            continue
        try:
            iso = f"{int(y):04d}-{mm:02d}-{int(d):02d}"
        except ValueError:
            continue
        if iso not in seen:
            seen.add(iso)
            out.append(iso)
            if len(out) >= max_items:
                break
    return sorted(out)


def extract_nilai_rupiah(text: str, max_items: int = 10) -> list[str]:
    """Tarik nilai rupiah (string mentah). Untuk indikasi nilai material."""
    out: list[str] = []
    for m in _RUPIAH_RE.finditer(text):
        s = re.sub(r"\s+", " ", m.group(0)).strip()
        if s not in out:
            out.append(s)
            if len(out) >= max_items:
                break
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def digest_one_file(
    file_path: Path,
    *,
    max_text_chars: int = 6000,
) -> dict[str, Any]:
    """Digest satu dokumen → dict ringkas. Pakai LiteParse untuk ekstraksi teks.

    Output schema:
        {
            "file": "relative/path/to/file.pdf",
            "jenis": "KRITERIA",          # hasil klasifikasi
            "halaman_total": 12,
            "size_bytes": 245678,
            "ringkasan_teks": "...",       # 6K char pertama, cap
            "kata_kunci": ["...", ...],
            "regulasi_terdeteksi": ["UU 27/2022", ...],
            "tanggal_terdeteksi": ["2026-02-15", ...],
            "nilai_rupiah_terdeteksi": ["Rp 4.500.000.000", ...],
            "halaman_total_chars": 24500,
            "_digest_meta": {
                "engine": "liteparse",
                "version": "0.1",
                "at": "ISO datetime",
            }
        }
    """
    from app.liteparse_extract import extract_pages, available

    if not available():
        # Fallback minimal: return meta-only
        return {
            "file": str(file_path),
            "jenis": classify_dokumen(file_path),
            "size_bytes": file_path.stat().st_size if file_path.is_file() else 0,
            "_digest_meta": {
                "engine": "none",
                "error": "LiteParse tidak tersedia",
                "at": datetime.now(timezone.utc).isoformat(),
            },
        }

    try:
        pages = extract_pages(file_path)
    except Exception as e:  # noqa: BLE001
        return {
            "file": str(file_path),
            "jenis": classify_dokumen(file_path),
            "size_bytes": file_path.stat().st_size if file_path.is_file() else 0,
            "_digest_meta": {
                "engine": "liteparse",
                "error": f"ekstraksi gagal: {e}",
                "at": datetime.now(timezone.utc).isoformat(),
            },
        }

    full_text = "\n\n".join(p for p in pages if p)
    ringkasan = full_text[:max_text_chars]
    if len(full_text) > max_text_chars:
        ringkasan += "\n\n[...TRUNCATED — gunakan read_pdf_page untuk halaman spesifik]"

    return {
        "file": str(file_path),
        "jenis": classify_dokumen(file_path),
        "halaman_total": len(pages),
        "halaman_total_chars": len(full_text),
        "size_bytes": file_path.stat().st_size,
        "ringkasan_teks": ringkasan,
        "kata_kunci": extract_keywords(full_text),
        "regulasi_terdeteksi": extract_regulasi(full_text),
        "tanggal_terdeteksi": extract_tanggal_iso(full_text),
        "nilai_rupiah_terdeteksi": extract_nilai_rupiah(full_text),
        "_digest_meta": {
            "engine": "liteparse",
            "version": "0.1",
            "at": datetime.now(timezone.utc).isoformat(),
        },
    }


def digest_folder(
    penugasan_folder: str | Path,
    *,
    subfolder_scan: list[str] | None = None,
    output_dir: str = "_INGESTED",
) -> dict[str, Any]:
    """Iterate seluruh dokumen di folder penugasan → tulis satu JSON per file.

    Args:
        penugasan_folder: root folder penugasan.
        subfolder_scan: list subfolder yang di-scan. None = SEMUA subfolder
            kecuali yang underscore-prefix (`_KKP`, `_LHP`, dst).
        output_dir: nama subfolder output (default `_INGESTED`).

    Return:
        {
            "n_total": jumlah file ditemukan,
            "n_digested": jumlah berhasil di-digest,
            "n_skip": jumlah skip (tidak supported),
            "per_jenis": {"KRITERIA": 3, "OBJEK": 5, ...},
            "files": [output_paths]
        }
    """
    from app.liteparse_extract import is_supported

    folder = Path(penugasan_folder)
    out_dir = folder / output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Default: semua subfolder non-underscore
    if subfolder_scan is None:
        subfolder_scan = [
            d.name for d in folder.iterdir()
            if d.is_dir() and not d.name.startswith("_")
        ]

    files_to_process: list[Path] = []
    for sub in subfolder_scan:
        sub_path = folder / sub
        if not sub_path.is_dir():
            continue
        for f in sub_path.rglob("*"):
            if f.is_file() and is_supported(f):
                files_to_process.append(f)

    counter_per_jenis: dict[str, int] = {}
    output_files: list[str] = []
    n_skip = 0
    for f in files_to_process:
        digest = digest_one_file(f)
        jenis = digest.get("jenis", "OTHER")
        counter_per_jenis[jenis] = counter_per_jenis.get(jenis, 0) + 1
        # Output filename: <jenis-lower>-<nn>.json
        idx = counter_per_jenis[jenis]
        out_name = f"{jenis.lower()}-{idx:02d}.json"
        out_path = out_dir / out_name
        try:
            # Buat path relatif terhadap folder penugasan supaya portable
            digest["file"] = str(f.relative_to(folder))
        except ValueError:
            pass
        try:
            out_path.write_text(
                json.dumps(digest, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            output_files.append(str(out_path.relative_to(folder)))
        except OSError:
            n_skip += 1

    return {
        "n_total": len(files_to_process),
        "n_digested": len(output_files),
        "n_skip": n_skip,
        "per_jenis": counter_per_jenis,
        "files": output_files,
        "_meta": {
            "engine": "digest_generic",
            "subfolder_scanned": subfolder_scan,
            "at": datetime.now(timezone.utc).isoformat(),
        },
    }


def skill_needs_generic_digest(skill: str | None) -> bool:
    """True bila skill TIDAK punya pipeline V6 khusus → digest generik."""
    if not skill:
        return False
    return str(skill).strip().lower() not in _SKILL_WITH_NATIVE_DIGEST
