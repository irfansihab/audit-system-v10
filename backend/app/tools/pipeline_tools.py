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
    "Jalankan DIGEST reviu-rka-kl (mode full-AI digest-only): auto-pair TOR↔RAB lalu "
    "parse tiap RO jadi tor-{N}.json + rab-{N}.json (7 blok substansi TOR + komponen "
    "RAB). TANPA rule deterministik — penilaian dilakukan AGEN via checklist di SKILL "
    "reviu-rka-kl (Kriteria IR2 PMK 107/2024: dasar hukum, kerangka logis, KPI SMART, "
    "kelengkapan, kewajaran biaya/SBM, konsistensi TOR↔RAB). Setelah ini baca via "
    "`read_digest` (tanpa arg ro=index semua RO; ro=<id> untuk detail) → analisis per "
    "checklist → append_temuan. Otomatis staging TOR/RAB dari folder upload.",
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
            "--penugasan", str(folder),
            "--tor-dir", "input/objek/TOR",
            "--rab-dir", "input/objek/RAB",
            "--workers", str(args.get("workers", 4)),
            "--digest-only",  # full-AI: digest per RO saja, tanpa cross_check/cross-RO/render
        ],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}{warn_txt}"}],
            "is_error": True,
        }
    n_ro = len(list((folder / "_KKP").glob("tor-*.json")))
    return {
        "content": [{
            "type": "text",
            "text": (
                f"OK|digest-only (full-AI, tanpa rule)|RO_terdigest={n_ro}|output={folder / '_KKP'}{warn_txt} "
                f"| LANGKAH BERIKUT: `read_digest` (index RO) → `read_digest(ro=<id>)` per RO → "
                f"analisis per checklist SKILL reviu-rka-kl → append_temuan"
            ),
        }]
    }


@tool(
    "run_batch_audit_pbj",
    "Jalankan DIGEST audit-pengadaan (mode full-AI digest-only): parse SELURUH dokumen "
    "siklus pengadaan (KAK/HPS/Kontrak/BAST/dokumen pemeriksaan/pembayaran) jadi JSON "
    "terstruktur di _KKP/pengadaan-digest.json. TANPA rule deterministik — penilaian "
    "dilakukan AGEN via checklist di SKILL audit-pengadaan (output-vs-kontrak, kewajaran "
    "HPS, kerugian negara, dll). Setelah ini, baca fakta via `read_digest`, lalu analisis "
    "per checklist → append_temuan (KKP: Judul|Kondisi|Kriteria|Sebab|Akibat|Sumber).",
    {"penugasan_folder": str, "role": str},
)
async def run_batch_audit_pbj(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    role = (args.get("role") or "AT").upper()
    code, out, err = await run_v6_script(
        "scripts/audit-pengadaan/run_batch.py",
        ["--penugasan", str(folder), "--digest-only"],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}"}],
            "is_error": True,
        }
    digest = safe_read_json(folder / "_KKP" / "pengadaan-digest.json")
    jenis = list((digest or {}).get("dokumen", {}).keys()) if isinstance(digest, dict) else []
    missing = (digest or {}).get("missing_types", []) if isinstance(digest, dict) else []
    return {
        "content": [{
            "type": "text",
            "text": (
                f"OK|role={role}|digest-only (full-AI, tanpa rule)|dokumen_terdeteksi={jenis}"
                f"|missing={missing}|output={folder / '_KKP' / 'pengadaan-digest.json'} "
                f"| LANGKAH BERIKUT: `read_digest` → analisis per checklist SKILL "
                f"(WAJIB output-vs-kontrak + isi Sebab di KKP)"
            ),
        }]
    }


@tool(
    "run_batch_pbj",
    "Jalankan DIGEST reviu-pengadaan (mode full-AI digest-only): parse dokumen "
    "perencanaan-pemilihan (KAK/HPS/Kontrak/RFI/dll) jadi JSON terstruktur di "
    "_KKP/pengadaan-digest.json. TANPA rule deterministik — penilaian dilakukan AGEN "
    "via checklist di SKILL reviu-pengadaan (kelengkapan/kesesuaian administratif, "
    "justifikasi, identifikasi kebutuhan, dll). Setelah ini baca fakta via `read_digest`, "
    "lalu analisis per checklist → append_temuan (KKP: Judul|Kondisi|Kriteria|Sebab|Akibat).",
    {"penugasan_folder": str, "role": str, "context_path": str},
)
async def run_batch_pbj(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    role = (args.get("role") or "AT").upper()
    code, out, err = await run_v6_script(
        "scripts/reviu-pengadaan/run_batch.py",
        ["--penugasan", args["penugasan_folder"], "--digest-only", "--role", role],
        timeout=300,
    )
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:600]}"}],
            "is_error": True,
        }
    digest = safe_read_json(folder / "_KKP" / "pengadaan-digest.json")
    jenis = list((digest or {}).get("dokumen", {}).keys()) if isinstance(digest, dict) else []
    missing = (digest or {}).get("missing_types", []) if isinstance(digest, dict) else []
    return {
        "content": [{
            "type": "text",
            "text": (
                f"OK|role={role}|digest-only (full-AI, tanpa rule)|dokumen_terdeteksi={jenis}"
                f"|missing={missing}|output={folder / '_KKP' / 'pengadaan-digest.json'} "
                f"| LANGKAH BERIKUT: `read_digest` → analisis per checklist SKILL reviu-pengadaan"
            ),
        }]
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


@tool(
    "run_digest_generic",
    "Digest GENERIK untuk skill yang TIDAK punya pipeline V6 khusus (audit-kinerja, "
    "audit-umum, evaluasi-*, kepatuhan-saipi, konsultansi-umum, konsultasi-pengadaan, "
    "pemantauan-*, reviu-umum). Iterate seluruh dokumen di folder penugasan, ekstrak "
    "teks via LiteParse, klasifikasi jenis (KRITERIA/OBJEK/NOTULEN/SK/LKE/dst), tulis "
    "satu JSON per file di `_INGESTED/<jenis>-<nn>.json` dengan: ringkasan_teks (cap "
    "6K char), kata_kunci, regulasi_terdeteksi, tanggal_terdeteksi, "
    "nilai_rupiah_terdeteksi. TIDAK panggil LLM. Pakai ini sebagai LANGKAH AWAL untuk "
    "skill criteria-driven supaya hemat token vs read_pdf_page mentah.",
    {"penugasan_folder": str},
)
async def run_digest_generic(args: dict) -> dict:
    from app.digest_generic import digest_folder
    folder = Path(args["penugasan_folder"])
    try:
        result = digest_folder(folder)
    except Exception as e:  # noqa: BLE001
        return {
            "content": [{"type": "text", "text": f"FAILED|{e}"}],
            "is_error": True,
        }
    per_jenis_str = ", ".join(f"{k}={v}" for k, v in sorted(result.get("per_jenis", {}).items()))
    return {
        "content": [{
            "type": "text",
            "text": (
                f"OK|digested={result['n_digested']}/{result['n_total']} files | "
                f"per_jenis: {per_jenis_str} | "
                f"output: _INGESTED/*.json"
            ),
        }]
    }


_DIGEST_BIG_KEYS = {"_raw_first_chars", "raw_text_pages", "raw_text", "raw", "pages_text"}


def _strip_big(d, _depth=0):
    """Buang field teks-mentah besar + truncate, supaya digest muat di output tool."""
    if isinstance(d, dict):
        return {k: _strip_big(v, _depth + 1) for k, v in d.items() if k not in _DIGEST_BIG_KEYS}
    if isinstance(d, list):
        return [_strip_big(x, _depth + 1) for x in d[:25]]
    if isinstance(d, str):
        return d[:500]
    return d


@tool(
    "read_digest",
    "Baca DIGEST terstruktur hasil run_batch_* mode digest-only (full-AI). "
    "PENGADAAN (audit/reviu-pengadaan): _KKP/pengadaan-digest.json → fakta per dokumen "
    "(KAK/HPS/Kontrak/BAST/pemeriksaan/pembayaran: nilai, periode, SLA, jaminan, "
    "elemen_justifikasi, lingkup_komponen, identifikasi_kebutuhan, dll). "
    "RKA-K/L: tor-*.json + rab-*.json per RO → tanpa arg `ro` mengembalikan INDEX semua RO "
    "(id + ringkas TOR/RAB); dengan arg `ro=<id>` mengembalikan digest LENGKAP RO itu "
    "(7 blok substansi TOR + komponen RAB). Pakai INI sebagai sumber fakta utama (hemat "
    "token, JANGAN baca ulang semua PDF); read_pdf_page hanya verifikasi halaman/kutipan.",
    {
        "type": "object",
        "properties": {
            "penugasan_folder": {"type": "string"},
            "ro": {"type": "string",
                   "description": "OPSIONAL. ID RO (RKA-K/L) untuk detail satu RO; "
                                  "kosongkan untuk INDEX semua RO atau digest PBJ."},
        },
        "required": ["penugasan_folder"],
    },
)
async def read_digest(args: dict) -> dict:
    kkp = Path(args["penugasan_folder"]) / "_KKP"
    ro_sel = str(args.get("ro") or "").strip()

    # --- PBJ: pengadaan-digest.json ---
    digest = safe_read_json(kkp / "pengadaan-digest.json")
    if isinstance(digest, dict) and digest.get("dokumen"):
        ringkas: dict = {}
        for jenis, entries in (digest.get("dokumen") or {}).items():
            ringkas[jenis] = [{
                "filename": e.get("filename"),
                "classified_by": e.get("classified_by", "nama"),
                "parsed": {k: v for k, v in (e.get("parsed") or {}).items()
                           if k not in _DIGEST_BIG_KEYS},
            } for e in (entries or [])]
        payload = {
            "jenis": "pengadaan",
            "dokumen": ringkas,
            "missing_types": digest.get("missing_types", []),
            "unclassified_files": digest.get("unclassified_files", [])[:10],
        }
        return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)[:8000]}]}

    # --- RKA-K/L: tor-*.json + rab-*.json per RO ---
    tors = sorted(kkp.glob("tor-*.json"))
    rabs = sorted(kkp.glob("rab-*.json"))
    if tors or rabs:
        ids = sorted({p.stem.split("-", 1)[1] for p in (tors + rabs)})
        if ro_sel:  # detail satu RO
            tor = _strip_big(safe_read_json(kkp / f"tor-{ro_sel}.json") or {})
            rab = _strip_big(safe_read_json(kkp / f"rab-{ro_sel}.json") or {})
            payload = {"jenis": "rka-kl", "ro": ro_sel, "tor": tor, "rab": rab}
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)[:8000]}]}
        # index semua RO (ringkas)
        idx = []
        for rid in ids:
            tor = safe_read_json(kkp / f"tor-{rid}.json") or {}
            rab = safe_read_json(kkp / f"rab-{rid}.json") or {}
            idx.append({
                "ro": rid,
                "tor_nama": (tor.get("nama_ro") or tor.get("nama") or tor.get("judul") or "")[:120],
                "tor_keys": [k for k in tor.keys() if k not in _DIGEST_BIG_KEYS][:15],
                "rab_total": rab.get("total") or rab.get("nilai_total"),
                "rab_komponen": rab.get("komponen_count") or len(rab.get("komponen", []) or []),
            })
        payload = {"jenis": "rka-kl", "total_ro": len(ids), "index": idx,
                   "catatan": "Panggil read_digest(ro=<id>) untuk digest lengkap satu RO."}
        return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)[:8000]}]}

    return {
        "content": [{"type": "text", "text": (
            "FAILED|digest tak ada di _KKP/ — jalankan run_batch_* (digest-only) dulu "
            "(pengadaan-digest.json untuk PBJ, atau tor-/rab-*.json untuk RKA-K/L)."
        )}],
        "is_error": True,
    }


PIPELINE_TOOLS = [
    run_batch_rka, run_batch_pbj, run_batch_audit_pbj, run_digest_generic,
    read_pdf_page, read_anomalies, read_digest, read_preload_context,
]
