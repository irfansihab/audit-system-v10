"""Tool wrappers untuk orchestrator V6: run_batch.py per skill."""
import json
import shutil
from pathlib import Path

from claude_agent_sdk import tool

from app.storage import classify_doc_by_filename
from app.tools.v6_bridge import run_v6_script, safe_read_json

# Subfolder tempat app menyimpan TOR/RAB (lihat storage.target_subfolder_for).
_RKA_SRC_SUBFOLDER = "03-perencanaan"


def _stage_rka_inputs(folder: Path) -> tuple[Path, Path, list[str]]:
    """Stage TOR/RAB PDF ke struktur yang dicari V6 run_batch.py.

    App menyimpan TOR/RAB di `03-perencanaan/` dengan nama asli, sedangkan
    auto-pair V6 mensyaratkan `input/objek/{TOR,RAB}/[N] ....pdf` (prefix angka
    = RO id) dan hanya membaca `.pdf`. Helper ini menjembatani gap itu:

    - scan `03-perencanaan/` (fallback ke root penugasan) untuk file TOR/RAB,
    - pasangkan TOR↔RAB berdasarkan urutan nama (TOR ke-i ↔ RAB ke-i = RO i),
    - copy ke `input/objek/TOR/[i] nama.pdf` dan `input/objek/RAB/[i] nama.pdf`,
    - lewati file non-PDF (mis. RAB .xlsx) karena digest V6 hanya menerima PDF.

    Return (tor_dir, rab_dir, warnings).
    """
    warnings: list[str] = []
    tor_files: list[Path] = []
    rab_files: list[Path] = []
    seen: set[str] = set()

    for src in (folder / _RKA_SRC_SUBFOLDER, folder):
        if not src.is_dir():
            continue
        for p in sorted(src.iterdir(), key=lambda x: x.name.lower()):
            if not p.is_file() or p.name in seen:
                continue
            jenis = classify_doc_by_filename(p.name)
            if jenis not in ("TOR", "RAB"):
                continue
            seen.add(p.name)
            if p.suffix.lower() != ".pdf":
                warnings.append(
                    f"{jenis} '{p.name}' bukan PDF — digest V6 RKA hanya menerima PDF "
                    f"format cetak RKA-K/L, file dilewati."
                )
                continue
            (tor_files if jenis == "TOR" else rab_files).append(p)

    tor_dir = folder / "input" / "objek" / "TOR"
    rab_dir = folder / "input" / "objek" / "RAB"
    for d in (tor_dir, rab_dir):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    for i, p in enumerate(tor_files, start=1):
        shutil.copy2(p, tor_dir / f"[{i}] {p.name}")
    for i, p in enumerate(rab_files, start=1):
        shutil.copy2(p, rab_dir / f"[{i}] {p.name}")

    n_pair = min(len(tor_files), len(rab_files))
    if len(tor_files) != len(rab_files):
        warnings.append(
            f"Jumlah TOR ({len(tor_files)}) ≠ RAB ({len(rab_files)}) — hanya "
            f"{n_pair} RO ber-pasangan yang akan diproses (sisanya di-skip auto-pair)."
        )
    if n_pair == 0:
        warnings.append(
            "Tidak ada pasangan TOR↔RAB PDF. Pastikan TOR dan RAB (PDF format "
            "RKA-K/L) sudah di-upload ke kategori perencanaan."
        )

    return tor_dir, rab_dir, warnings


@tool(
    "run_batch_rka",
    "Jalankan pipeline V6 reviu-rka-kl (digest + cross-check anomali). "
    "Otomatis staging TOR/RAB dari folder upload ke struktur yang dibutuhkan V6. "
    "Pipeline ini TIDAK merender LHR (jalan dengan --no-render): LHR adalah hasil "
    "kompilasi temuan.json yang sudah diapprove KT, dirender terpisah oleh KT via "
    "render_lhr_rka — BUKAN dari anomali mentah. "
    "Output: _KKP/anomalies-master.json, _KKP/tor-{N}.json, _KKP/rab-{N}.json.",
    {
        "penugasan_folder": str,
        "workers": int,
        "judul": str,
        "nomor": str,
        "tanggal": str,
        "penerima": str,
    },
)
async def run_batch_rka(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    tor_dir, rab_dir, warns = _stage_rka_inputs(folder)
    warn_txt = ("|warnings=" + "; ".join(warns)) if warns else ""

    if not any(tor_dir.glob("*.pdf")) or not any(rab_dir.glob("*.pdf")):
        return {
            "content": [{
                "type": "text",
                "text": f"FAILED|tidak ada pasangan TOR↔RAB PDF untuk diproses{warn_txt}",
            }],
            "is_error": True,
        }

    code, out, err = await run_v6_script(
        "scripts/reviu-rka-kl/run_batch.py",
        [
            "--penugasan",
            str(folder),
            "--tor-dir",
            "input/objek/TOR",
            "--rab-dir",
            "input/objek/RAB",
            "--workers",
            str(args.get("workers", 4)),
            # LHR di-render terpisah oleh KT dari temuan.json yang diapprove,
            # bukan dari anomali mentah pipeline. Skip Phase 4 render di sini.
            "--no-render",
        ],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}{warn_txt}"}],
            "is_error": True,
        }
    anomalies = safe_read_json(folder / "_KKP" / "anomalies-master.json")
    total = len(anomalies) if isinstance(anomalies, list) else len(anomalies.get("anomalies", []))
    return {
        "content": [
            {"type": "text", "text": f"OK|anomalies_total={total}|output={folder / '_KKP'}{warn_txt}"}
        ]
    }


@tool(
    "run_batch_audit_pbj",
    "Jalankan pipeline V6 audit-pengadaan: digest_pengadaan + cross_check 11 rules "
    "(P.1-4, K.1-3, PL.1, B.1, D.1-2) untuk SELURUH SIKLUS pengadaan (perencanaan → "
    "pemilihan → kontrak → pelaksanaan → pembayaran). Beda dengan reviu-pengadaan "
    "(perencanaan saja), audit-pengadaan WAJIB menganalisis hasil pekerjaan (BAST, "
    "SPM, kewajaran pembayaran) dan WAJIB isi kolom Sebab di setiap temuan KKP. "
    "Output: _KKP/anomalies.json + _KKP/pengadaan-digest.json. KKP format CCSAA "
    "lengkap: Judul | Kondisi | Kriteria | Sebab | Akibat | Sumber.",
    {"penugasan_folder": str, "role": str},
)
async def run_batch_audit_pbj(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    role = (args.get("role") or "AT").upper()
    extra = ["--no-render"] if role == "AT" else []  # LHA dirender KT terpisah
    code, out, err = await run_v6_script(
        "scripts/audit-pengadaan/run_batch.py",
        ["--penugasan", str(folder), *extra],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}"}],
            "is_error": True,
        }
    anomalies = safe_read_json(folder / "_KKP" / "anomalies.json")
    total = len(anomalies) if isinstance(anomalies, list) else len(anomalies.get("anomalies", []))
    return {
        "content": [{
            "type": "text",
            "text": (
                f"OK|role={role}|anomalies_total={total}|output={folder / '_KKP'} "
                f"| AUDIT-MODE: WAJIB analisis hasil pekerjaan + isi kolom Sebab di KKP"
            ),
        }]
    }


@tool(
    "run_batch_pbj",
    "Jalankan pipeline lengkap V6 reviu-pengadaan dengan role gating. "
    "AT → output KKP, KT → output LHR. Skript reuse digest_pengadaan dari audit-pengadaan.",
    {"penugasan_folder": str, "role": str, "context_path": str},
)
async def run_batch_pbj(args: dict) -> dict:
    extra: list[str] = []
    role = args.get("role", "AT").upper()
    if role == "AT":
        extra = ["--role", "AT"]
    else:
        extra = ["--role", "KT"]
    code, out, err = await run_v6_script(
        "scripts/reviu-pengadaan/run_batch.py",
        ["--penugasan", args["penugasan_folder"], *extra],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}"}],
            "is_error": True,
        }
    folder = Path(args["penugasan_folder"])
    anomalies = safe_read_json(folder / "_KKP" / "anomalies.json")
    total = len(anomalies) if isinstance(anomalies, list) else len(anomalies.get("anomalies", []))
    return {
        "content": [
            {"type": "text", "text": f"OK|role={role}|anomalies_total={total}|output={folder / '_KKP'}"}
        ]
    }


@tool(
    "read_pdf_page",
    "Baca teks satu halaman PDF — dipakai agen untuk verifikasi false positive anomali.",
    {"pdf_path": str, "halaman": int},
)
async def read_pdf_page(args: dict) -> dict:
    from pdfplumber import open as open_pdf

    p = Path(args["pdf_path"])
    if not p.exists():
        return {
            "content": [{"type": "text", "text": f"FAILED|file tidak ada: {p}"}],
            "is_error": True,
        }
    try:
        with open_pdf(str(p)) as pdf:
            idx = max(0, args["halaman"] - 1)
            if idx >= len(pdf.pages):
                return {
                    "content": [
                        {"type": "text", "text": f"FAILED|halaman {args['halaman']} di luar rentang"}
                    ],
                    "is_error": True,
                }
            text = pdf.pages[idx].extract_text() or ""
        return {"content": [{"type": "text", "text": text[:4000]}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"FAILED|{str(e)[:200]}"}],
            "is_error": True,
        }


@tool(
    "read_anomalies",
    "Baca daftar LENGKAP anomali hasil pipeline V6 dari _KKP/anomalies-master.json "
    "(reviu-rka-kl) atau _KKP/anomalies.json (reviu-pengadaan). PAKAI SETELAH "
    "run_batch_* supaya kamu tahu SEMUA anomali yang ditemukan rules (rule_id, "
    "severity, aspek, judul, deskripsi, bukti, draft kondisi/kriteria/akibat, RO). "
    "Cross-check sistematis: verifikasi tiap anomali via read_pdf_page lalu "
    "TERIMA/TOLAK/MODIFIKASI sebelum append_temuan. Mencegah anomali terlewat.",
    {"penugasan_folder": str},
)
async def read_anomalies(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    for name in ("anomalies-master.json", "anomalies.json"):
        path = folder / "_KKP" / name
        if not path.exists():
            continue
        data = safe_read_json(path)
        if isinstance(data, dict):
            anomalies = data.get("anomalies", [])
            ringkasan = data.get("ringkasan", {})
        elif isinstance(data, list):
            anomalies, ringkasan = data, {}
        else:
            anomalies, ringkasan = [], {}
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(
                    {
                        "source": name,
                        "total": len(anomalies),
                        "ringkasan": ringkasan,
                        "anomalies": anomalies[:50],
                    },
                    ensure_ascii=False,
                ),
            }]
        }
    return {
        "content": [{
            "type": "text",
            "text": "FAILED|anomalies file tidak ada di _KKP/ — jalankan run_batch_* dulu",
        }],
        "is_error": True,
    }


@tool(
    "read_preload_context",
    "Baca bundle konteks pra-loaded di `_PRELOAD/context-bundle.md` — berisi "
    "pattern wiki terkurasi (top severity), catatan vault terkait obyek, pola-"
    "temuan-berulang, glossary, regulasi, riwayat penugasan serupa. WAJIB dibaca "
    "DULU di langkah awal sebelum susun temuan — supaya mulai dengan tangan "
    "penuh. Mengganti perlu panggilan beruntun search_wiki/list_temuan_patterns/"
    "get_konteks secara terpisah saat awal. Bila bundle belum ada, lanjut pakai "
    "tools lama.",
    {"penugasan_folder": str},
)
async def read_preload_context(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    bundle = folder / "_PRELOAD" / "context-bundle.md"
    if not bundle.exists():
        return {
            "content": [{
                "type": "text",
                "text": (
                    "PRELOAD_BELUM_DIBANGUN|Bundle konteks pra-loaded belum "
                    "dibangun. Auditor bisa generate via tombol 'Refresh Konteks' "
                    "di tab Setup Penugasan, atau lewat POST /penugasan/{id}/"
                    "preload-context. Lanjut pakai tools lama (search_wiki, "
                    "list_temuan_patterns, get_konteks)."
                ),
            }]
        }
    try:
        text = bundle.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "content": [{"type": "text", "text": f"FAILED|gagal baca bundle: {exc}"}],
            "is_error": True,
        }
    # Cap supaya tidak meledak context window (~6K token)
    return {"content": [{"type": "text", "text": text[:24000]}]}


PIPELINE_TOOLS = [
    run_batch_rka, run_batch_pbj, run_batch_audit_pbj,
    read_pdf_page, read_anomalies, read_preload_context,
]
