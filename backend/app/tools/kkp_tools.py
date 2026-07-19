"""Tools untuk Agen Anggota Tim: append temuan ke temuan.json, render KKP.docx.

Schema temuan.json yang dipakai mengikuti yang dibutuhkan V6 render_kkp.py:

    {
        "penugasan": {
            "kode": str,
            "obyek": str,
            "jenis_pengawasan": str,  # skill: reviu-pengadaan, reviu-rka-kl
            "nomor_st": str,
            "tanggal_st": str,
        },
        "schema_version": "v4.0.0",
        "temuan": [
            {
                "id_temuan": "T-001",
                "sasaran_id": "S-01",
                "anggota_tim": {"nama_lengkap": "Sarah Aulia"},
                "judul_temuan": "...",
                "kondisi": "...",
                "kriteria": "...",
                "sebab": "..." | null,        # null untuk reviu (bukan audit)
                "akibat": "...",
                "dokumen_sumber": [
                    {"file": "02-kontrak/KAK.pdf", "halaman": 3, "kutipan": "..."}
                ],
                "status": "DRAFT",
                "tanggal_input": "ISO datetime",
                "catatan_ketua_tim": null,
                "integral": null,
            },
            ...
        ]
    }

Bridge `append_temuan` menerima input yang lebih sederhana dari agen dan
me-transform ke schema di atas — supaya agen tidak perlu tahu skema render_kkp.
"""
import json
import os
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import tool
from sqlalchemy import select

from app.tools.v6_bridge import qc_summary_counts, run_v6_script, safe_read_json


@tool(
    "read_context",
    "Baca context.md + Kartu Penugasan (_KP/kartu-penugasan.md, diisi PT) + "
    "sasaran-assignment.json (PKP) + daftar file di subfolder input penugasan. "
    "Pakai ini PERTAMA sebelum apapun untuk dapat konteks.",
    {"penugasan_folder": str},
)
async def read_context(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    context_md = (
        (folder / "context.md").read_text(encoding="utf-8")
        if (folder / "context.md").exists()
        else ""
    )
    assignment = safe_read_json(folder / "_PKP" / "sasaran-assignment.json")
    # Kartu Penugasan (tahapan 1, diisi PT) — sumber identitas/tujuan/ruang
    # lingkup resmi saat menyusun context.md. Kosong bila PT belum mengisi.
    kp_path = folder / "_KP" / "kartu-penugasan.md"
    kartu_penugasan = kp_path.read_text(encoding="utf-8") if kp_path.exists() else ""

    # Daftar file di subfolder input (00-input, 01-..., 02-..., dst)
    # supaya agen tahu file mana yang bisa direferensikan di dokumen_sumber.
    input_files: list[str] = []
    for p in folder.iterdir():
        if p.is_dir() and not p.name.startswith("_"):
            for f in p.rglob("*"):
                if f.is_file():
                    input_files.append(str(f.relative_to(folder)))

    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(
                    {
                        "context_md": context_md,
                        "kartu_penugasan": kartu_penugasan,
                        "sasaran_assignment": assignment,
                        "input_files": sorted(input_files),
                    },
                    ensure_ascii=False,
                ),
            }
        ]
    }


@tool(
    "list_ingested",
    "Daftar file JSON hasil ingestion di _INGESTED/.",
    {"penugasan_folder": str},
)
async def list_ingested(args: dict) -> dict:
    folder = Path(args["penugasan_folder"]) / "_INGESTED"
    files = [p.name for p in folder.glob("*.json")] if folder.exists() else []
    return {"content": [{"type": "text", "text": "\n".join(files) or "(kosong)"}]}


_SURVEY_TEXT_CAP = 12000


@tool(
    "read_survey_pendahuluan",
    "Baca bahan Survey Pendahuluan (tahapan 0, khusus audit-*) dari sub-folder "
    "`00-survey/` + teks hasil ekstraksi di `_INGESTED/`. Pakai SAAT setup (Mode A) "
    "untuk menyusun PROFIL RISIKO awal (3E: Ekonomis/Efisien/Efektif) yang mengarahkan "
    "sasaran reviu. Bila kosong, lanjut tanpa survey. Untuk kerangka 3E lengkap, baca "
    "reference skill `references/08-checklist-survey-pendahuluan.md` via read_skill_reference.",
    {"penugasan_folder": str},
)
async def read_survey_pendahuluan(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    survey_dir = folder / "00-survey"
    survey_files = (
        sorted(str(p.relative_to(folder)) for p in survey_dir.rglob("*") if p.is_file())
        if survey_dir.exists()
        else []
    )

    # Teks hasil ekstraksi: cari JSON _INGESTED yang berasal dari dokumen survey.
    # Dokumen survey di-prefix "survey" / "sp" oleh classify; ambil raw_text_pages.
    ingested_dir = folder / "_INGESTED"
    extracted: list[dict] = []
    budget = _SURVEY_TEXT_CAP
    if ingested_dir.exists():
        for jp in sorted(ingested_dir.glob("*.json")):
            stem = jp.stem.lower()
            if not (stem.startswith("survey") or stem.startswith("sp") or "survei" in stem):
                continue
            data = safe_read_json(jp)
            if not isinstance(data, dict):
                continue
            pages = data.get("raw_text_pages") or []
            text = "\n".join(
                p.get("text", "") if isinstance(p, dict) else str(p) for p in pages
            ).strip()
            if not text:
                continue
            snippet = text[:budget]
            budget -= len(snippet)
            extracted.append({"file": jp.name, "text": snippet, "truncated": len(text) > len(snippet)})
            if budget <= 0:
                break

    payload = {
        "ada_survey": bool(survey_files),
        "survey_files": survey_files,
        "extracted": extracted,
        "petunjuk": (
            "Bila ada_survey=false, lewati profil risiko survey dan susun sasaran "
            "berdasarkan PKP/skill seperti biasa. Bila ada: rangkum jadi PROFIL RISIKO "
            "3E (Ekonomis/Efisien/Efektif) — tiap risiko menunjuk sasaran reviu yang "
            "relevan. File belum terekstraksi bisa dibaca via read_pdf_page."
        ),
    }
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}


# (dead-code _detect_skill_from_folder dihapus — tak pernah dipanggil; audit #B12.)



def _normalize_temuan_input(raw: dict) -> dict:
    """Map keys umum yang dipakai agen ke schema V6 render_kkp.

    Agen sering pakai `judul` / `assigned_to`; render_kkp expect
    `judul_temuan` / `anggota_tim.nama_lengkap`. Bridge translate di sini
    supaya agen tidak perlu hafal skema persis.
    """
    out = dict(raw)

    # id alias → id_temuan (agen bisa kirim `id` atau `id_temuan`)
    if "id_temuan" not in out and "id" in out:
        out["id_temuan"] = out.pop("id")

    # judul → judul_temuan
    if "judul_temuan" not in out and "judul" in out:
        out["judul_temuan"] = out.pop("judul")

    # assigned_to (str atau list[str]) → anggota_tim: {"nama_lengkap": str}
    if "anggota_tim" not in out:
        assigned = out.pop("assigned_to", None) or out.pop("anggota", None)
        if isinstance(assigned, list) and assigned:
            assigned = assigned[0]
        if isinstance(assigned, dict):
            out["anggota_tim"] = assigned
        elif isinstance(assigned, str):
            out["anggota_tim"] = {"nama_lengkap": assigned}
        else:
            out["anggota_tim"] = {"nama_lengkap": ""}
    elif isinstance(out.get("anggota_tim"), str):
        out["anggota_tim"] = {"nama_lengkap": out["anggota_tim"]}

    # Default-fill field SAIPI yang wajib di render_kkp
    out.setdefault("sasaran_id", "")
    out.setdefault("kondisi", "")
    out.setdefault("kriteria", "")
    out.setdefault("akibat", "")
    out.setdefault("sebab", None)  # semua jenis isi bila terbukti; else "tidak ditemukan/tidak cukup data" (anti-mengarang)
    out.setdefault("dokumen_sumber", [])

    # Kodefikasi temuan (SIM-HP/APIP) — lihat get_kodefikasi_temuan. Format `<sub>.<param>`.
    # kode_kondisi & kode_rekomendasi diisi semua skill; kode_penyebab hanya audit (ada Sebab).
    out.setdefault("kode_kondisi", "")
    out.setdefault("kode_penyebab", "")
    out.setdefault("kode_rekomendasi", "")

    # Ketertelusuran (WAJIB diisi agen — lihat anggota_tim.md): langkah kerja PKP
    # yang memunculkan temuan + pattern wiki (bila ada). Default kosong agar tidak
    # memblok schema lama, tapi prompt mewajibkan agen mengisinya.
    out.setdefault("langkah_kerja_terkait", "")
    out.setdefault("pattern_id", "")

    # Identitas RO (RKA-K/L multi-RO): label STABIL RO tempat temuan ini berasal
    # (dari `ro_label` di index read_digest — bukan nomor posisional). Kosong untuk
    # penugasan non-RKA / RO tunggal. Dipakai untuk analisis inkremental: RO yang
    # sudah punya temuan (n_temuan>0) tidak dianalisis ulang saat RO baru ditambah.
    out.setdefault("ro", "")

    # Metadata
    out.setdefault("tanggal_input", datetime.utcnow().isoformat() + "Z")
    out.setdefault("status", "DRAFT")
    out.setdefault("catatan_ketua_tim", None)
    out.setdefault("integral", None)

    return out


@tool(
    "append_temuan",
    "Tambah ATAU timpa 1 temuan di _KKP/temuan.json (UPSERT by id_temuan). "
    "Perilaku: bila input memuat `id_temuan` (atau `id`) yang SUDAH ADA → temuan itu "
    "DITIMPA di tempat (untuk koreksi/penyempurnaan, id tetap). Bila tanpa id atau id "
    "belum ada → ditambah sebagai temuan BARU (id auto T-NNN). Jadi: koreksi = kirim "
    "ulang dengan id yang sama (menimpa, tidak menggandakan); temuan baru = tanpa id. "
    "Bridge otomatis transform key sederhana (judul, assigned_to) ke schema V6 "
    "(judul_temuan, anggota_tim.nama_lengkap). Field wajib: sasaran_id, anggota_tim/"
    "assigned_to, judul, kondisi, kriteria, akibat, dokumen_sumber[{file, halaman, kutipan}]. "
    "Ketertelusuran (isi bila ada): langkah_kerja_terkait (langkah PKP yang memunculkan "
    "temuan), pattern_id (id pattern wiki). KODEFIKASI (WAJIB — lihat get_kodefikasi_temuan): "
    "kode_kondisi (wajib), kode_rekomendasi (wajib), kode_penyebab (semua jenis — isi bila penyebab "
    "terbukti; kosongkan bila sebab='tidak ditemukan/tidak cukup data', JANGAN mengarang); "
    "format `<sub>.<param>` mis. 1.104.",
    {
        "penugasan_folder": str,
        "temuan": dict,
    },
)
async def append_temuan(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    path = folder / "_KKP" / "temuan.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    # Init kalau belum ada (umumnya sudah ada karena scaffolding di POST /penugasan,
    # tapi defensive).
    if path.exists():
        data = safe_read_json(path) or {}
        if not data:
            # File ADA tapi gagal parse (korup) — JANGAN re-init envelope kosong:
            # itu menimpa file dan menghapus seluruh temuan tim secara diam-diam.
            # Gagalkan eksplisit; auditor pulihkan dari temuan-full-backup.json /
            # git, atau perbaiki file-nya. (Temuan audit #E1.)
            return {
                "content": [{
                    "type": "text",
                    "text": (
                        "FAILED|_KKP/temuan.json ADA tapi tidak bisa di-parse (korup?) — "
                        "append dibatalkan agar temuan lama tidak tertimpa. "
                        "Minta auditor memeriksa/memulihkan file tersebut dulu."
                    ),
                }],
                "is_error": True,
            }
    else:
        data = {}
    if not data or "penugasan" not in data:
        data = {
            "penugasan": {
                "kode": folder.name,
                "obyek": "",
                "jenis_pengawasan": "",
                "nomor_st": "",
                "tanggal_st": None,
            },
            "schema_version": "v4.0.0",
            "temuan": [],
        }
    data.setdefault("temuan", [])

    new_temuan = _normalize_temuan_input(args["temuan"])

    # UPSERT: bila id_temuan sudah ada → timpa di tempat (koreksi); else append (baru).
    given_id = new_temuan.get("id_temuan")
    action = "appended"
    if given_id:
        idx = next(
            (i for i, t in enumerate(data["temuan"]) if t.get("id_temuan") == given_id),
            None,
        )
        if idx is not None:
            data["temuan"][idx] = new_temuan
            action = "replaced"
        else:
            data["temuan"].append(new_temuan)
    else:
        seq = len(data["temuan"]) + 1
        new_temuan["id_temuan"] = f"T-{seq:03d}"
        data["temuan"].append(new_temuan)

    # Tulis ATOMIK (temp + os.replace) — crash di tengah write tidak boleh
    # meninggalkan temuan.json terpotong (yang lalu memicu jalur "korup" di atas).
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)
    return {
        "content": [
            {
                "type": "text",
                "text": f"OK|action={action}|id={new_temuan['id_temuan']}|total_now={len(data['temuan'])}",
            }
        ]
    }


@tool(
    "reset_temuan",
    "Kosongkan SELURUH temuan di _KKP/temuan.json (header penugasan dipertahankan). "
    "HANYA dipakai saat auditor minta analisis ULANG DARI AWAL (fresh-run pada penugasan "
    "yang sudah punya temuan), supaya hasil lama tidak menumpuk. JANGAN dipakai untuk "
    "koreksi/penyempurnaan biasa — itu pakai append_temuan dengan id yang sama (upsert).",
    {"penugasan_folder": str},
)
async def reset_temuan(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    path = folder / "_KKP" / "temuan.json"
    if not path.exists():
        return {"content": [{"type": "text", "text": "OK|temuan.json belum ada — tidak ada yang direset"}]}
    data = safe_read_json(path) or {}
    before = len(data.get("temuan", []) or [])
    data.setdefault("temuan", [])
    data["temuan"] = []
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"content": [{"type": "text", "text": f"OK|reset|temuan_dihapus={before}|total_now=0"}]}


@tool(
    "get_kodefikasi_temuan",
    "Baca daftar KODEFIKASI TEMUAN standar (SIM-HP/APIP): kode Kondisi, Penyebab, "
    "Rekomendasi (+ Tindak Lanjut). WAJIB dipanggil saat menyusun KKP untuk memberi "
    "kode pada SETIAP temuan: kode_kondisi (wajib), kode_rekomendasi (wajib), "
    "kode_penyebab (hanya AUDIT yang punya unsur Sebab). Format kode `<sub>.<param>` "
    "mis. 1.104. Pilih parameter yang paling cocok dengan substansi temuan.",
    {},
)
async def get_kodefikasi_temuan(_args: dict) -> dict:
    from app.config import get_settings
    path = get_settings().skills_path / "panduan-format-umum" / "kodefikasi-temuan.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {
            "content": [{"type": "text", "text": "NOT_FOUND|kodefikasi-temuan.md tidak tersedia"}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": text}]}


def _read_hitl_overlay(folder: Path):
    """P1c: baca overlay HITL portabel dari `_KKP/hitl-overlay.json`.
    Skema: {"rejected_ids": ["<id_temuan>"...], "edits": {"<id_temuan>": {"<field>": <val>}}}.
    Disuplai ORKESTRATOR (INTEGRAL) atau dimaterialisasi backend harness dari DB.
    Return (rejected:set[str], edits:dict[str,dict]) bila file ada & valid; None bila
    tak ada → caller fallback ke DB (kompat harness lama)."""
    path = folder / "_KKP" / "hitl-overlay.json"
    if not path.is_file():
        return None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(d, dict):
        return None
    rejected = {str(x) for x in (d.get("rejected_ids") or [])}
    raw_edits = d.get("edits") or {}
    edits = {str(k): v for k, v in raw_edits.items() if isinstance(v, dict)}
    return rejected, edits


async def _filter_temuan_by_review(folder: Path) -> tuple[Path | None, dict | None]:
    """Terapkan overlay edit manual (HITL) ke `_KKP/temuan.json` sebelum render.
    Return (backup_path, stats).

    Model HITL baru (17 Jun 2026 — tanpa approve/tolak per-temuan):
      - SEMUA temuan di temuan.json masuk render (kurasi via edit + chat, bukan
        approve). Overlay `edited_fields` diterapkan ke temuan yang diedit.
      - Hanya temuan ber-status REJECTED (data lama) yang di-exclude.
      - Bila tak ada review record sama sekali → JANGAN filter (render apa adanya).
      - Bila gagal query DB → JANGAN filter (best-effort; perilaku lama).

    Saat filter aktif, file asli dibackup ke `_KKP/temuan-full-backup.json`
    dan `temuan.json` ditulis ulang dengan subset. Caller WAJIB panggil
    `_restore_temuan_from_backup` setelah render selesai (sukses/gagal).
    """
    temuan_path = folder / "_KKP" / "temuan.json"
    if not temuan_path.is_file():
        return None, None

    # P1c: overlay HITL dari FILE dulu (portabel: INTEGRAL/harness suplai
    # `_KKP/hitl-overlay.json`), fallback ke DB (Penugasan+TemuanReview) bila tak ada.
    rejected: set[str] = set()
    edits_by_id: dict[str, dict] = {}
    penugasan_id: int | None = None
    overlay = _read_hitl_overlay(folder)
    if overlay is not None:
        rejected, edits_by_id = overlay
    else:
        from app.database import SessionLocal
        from app.models import Penugasan, TemuanReview
        folder_abs = str(folder.resolve())
        try:
            async with SessionLocal() as db:
                row = (await db.execute(
                    select(Penugasan.id).where(Penugasan.folder_path == folder_abs)
                )).first()
                if row is None:
                    row = (await db.execute(
                        select(Penugasan.id).where(Penugasan.kode == folder.name)
                    )).first()
                if row is None:
                    return None, None
                penugasan_id = row[0]
                full_reviews = (await db.execute(
                    select(TemuanReview).where(TemuanReview.penugasan_id == penugasan_id)
                )).scalars().all()
        except Exception:  # noqa: BLE001 — best-effort filter
            return None, None
        if not full_reviews:
            return None, None
        rejected = {r.temuan_id for r in full_reviews if r.status == "REJECTED"}
        edits_by_id = {r.temuan_id: r.edited_fields for r in full_reviews if r.edited_fields}

    # Tak ada overlay sama sekali → bypass (render semua apa adanya).
    if not rejected and not edits_by_id:
        return None, None

    # Sisa backup dari run yang crash (restore tak sempat jalan) → pulihkan
    # DULU. Tanpa ini, filter bekerja atas temuan.json yang SUDAH ter-filter
    # lalu menimpa backup dengan versi ter-filter → temuan asli hilang permanen.
    leftover = folder / "_KKP" / "temuan-full-backup.json"
    if leftover.exists():
        try:
            temuan_path.write_bytes(leftover.read_bytes())
        except OSError:
            pass

    # Load + terapkan overlay (exclude REJECTED + edited_fields).
    try:
        data = json.loads(temuan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    full = data.get("temuan", [])
    if not isinstance(full, list):
        return None, None
    n_edits_applied = 0
    filtered: list[dict] = []
    for t_item in full:
        tid = t_item.get("id_temuan")
        if tid in rejected:
            continue
        edits = edits_by_id.get(tid)
        if edits:
            filtered.append({**t_item, **edits})
            n_edits_applied += 1
        else:
            filtered.append(t_item)
    stats = {
        "n_total": len(full),
        "n_included": len(filtered),
        "n_rejected": len(rejected),
        "n_edits_applied": n_edits_applied,
        "penugasan_id": penugasan_id,
    }

    # Backup + tulis filtered
    backup = folder / "_KKP" / "temuan-full-backup.json"
    try:
        backup.write_bytes(temuan_path.read_bytes())
    except OSError:
        return None, None
    data["temuan"] = filtered
    try:
        temuan_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        # gagal tulis → restore backup
        try:
            temuan_path.write_bytes(backup.read_bytes())
        except OSError:
            pass
        backup.unlink(missing_ok=True)
        return None, None

    return backup, stats


def _restore_temuan_from_backup(folder: Path, backup: Path | None) -> None:
    """Restore `_KKP/temuan.json` dari backup. Always call di finally."""
    if backup is None or not backup.is_file():
        return
    temuan_path = folder / "_KKP" / "temuan.json"
    try:
        temuan_path.write_bytes(backup.read_bytes())
    finally:
        backup.unlink(missing_ok=True)


# Skill evaluasi ber-LKE Excel: output LKE-terisi WAJIB (deliverable utama).
# evaluasi-reformasi-birokrasi diperlakukan sama (LKE 4-dimensi via fill_lke).
_LKE_EXCEL_SKILLS = {"evaluasi-spip", "evaluasi-sakip", "evaluasi-reformasi-birokrasi"}


def _skill_from_assignment(folder: Path) -> str | None:
    """Skill penugasan untuk gate LKE — robust multi-sumber (v10):
    1) _PKP/sasaran-assignment.json['skill'] (bila ada), 2) temuan.json
    penugasan.jenis_pengawasan, 3) parse nama folder."""
    try:
        d = json.loads((folder / "_PKP" / "sasaran-assignment.json").read_text(encoding="utf-8"))
        s = d.get("skill") if isinstance(d, dict) else None
        if isinstance(s, str) and s.strip():
            return s.strip().lower()
    except (OSError, json.JSONDecodeError):
        pass
    try:
        d = json.loads((folder / "_KKP" / "temuan.json").read_text(encoding="utf-8"))
        s = (d.get("penugasan") or {}).get("jenis_pengawasan") if isinstance(d, dict) else None
        if isinstance(s, str) and s.strip():
            return s.strip().lower()
    except (OSError, json.JSONDecodeError):
        pass
    name = folder.name.lower().replace("-", "")
    for s in _LKE_EXCEL_SKILLS:
        if s.replace("-", "") in name:
            return s
    return None


@tool(
    "render_kkp_docx",
    "Render KKP-{nama-anggota}.docx menggunakan scripts/render_kkp.py V6. "
    "Otomatis FILTER temuan: hanya yang status review APPROVED/EDITED yang "
    "masuk ke DOCX (HITL gating). Bila belum ada review record sama sekali "
    "untuk penugasan ini, perilaku LEGACY: render semua temuan apa adanya.",
    {"penugasan_folder": str, "nama_anggota": str},
)
async def render_kkp_docx(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    # GATE LKE (port v8.8 SIMWAS): untuk SPIP/SAKIP, LKE Excel WAJIB sudah dibuat
    # via fill_lke sebelum render KKP — cegah KKP/laporan selesai tanpa deliverable LKE.
    _lke_skill = _skill_from_assignment(folder)
    if _lke_skill in _LKE_EXCEL_SKILLS:
        _lke_xlsx = folder / "_KKP" / f"LKE-terisi-{_lke_skill}.xlsx"
        if not _lke_xlsx.is_file():
            return {"content": [{"type": "text", "text": (
                f"FAILED|LKE Excel WAJIB untuk {_lke_skill} tapi belum dibuat "
                f"(_KKP/LKE-terisi-{_lke_skill}.xlsx tidak ada). Jalankan `fill_lke` "
                f"(isi kolom APIP per unsur/kriteria) LEBIH DULU, baru `render_kkp_docx`. "
                f"Output LKE Excel = deliverable wajib evaluasi ber-LKE; `write_penilaian_lke` "
                f"(JSON rekap) TIDAK menggantikannya."
            )}], "is_error": True}
        # SPIP: LKE rev4 volume besar dikerjakan per BATCH (KK Lead I/II/III) —
        # pastikan SEMUA batch LENGKAP (bukan hanya file ada) agar LKE tak ter-render
        # setengah jadi. Struktur lama = advisory; hanya rev4 di-gate keras. (port v8.1)
        if _lke_skill == "evaluasi-spip":
            from app.tools.lke_tools import spip_batch_progress
            prog = spip_batch_progress(folder)
            if not prog.get("all_complete"):
                if not prog.get("any_measured", True):
                    return {"content": [{"type": "text", "text": (
                        "FAILED|LKE SPIP: tidak ada baris hidup (kolom B) terdeteksi — "
                        "pastikan LKE berisi PM satker & sudah diisi PK sebelum render KKP."
                    )}], "is_error": True}
                if prog.get("struktur") != "old":
                    kurang = []
                    for b in prog.get("batches", []):
                        if b.get("complete"):
                            continue
                        sheets = [f"{sn}: {d.get('sisa', '?')} baris belum PK ({d.get('pct', '?')}%)"
                                  for sn, d in b.get("sheets", {}).items()
                                  if d.get("ok") is False]
                        kurang.append(f"Batch {b['no']} ({b['nama']}): {', '.join(sheets) or 'belum diisi'}")
                    return {"content": [{"type": "text", "text": (
                        f"FAILED|LKE SPIP belum LENGKAP — blok PK masih ada baris kosong: "
                        f"{' | '.join(kurang)}. Lanjutkan `fill_lke` (cek `lke_batch_status`) "
                        f"sampai all_complete, baru `render_kkp_docx`."
                    )}], "is_error": True}
    backup, stats = await _filter_temuan_by_review(folder)
    filter_note = ""
    if stats is not None:
        # PENTING: pakai kunci yang benar-benar ada di stats (n_included/n_total/
        # n_rejected). Dulu merujuk n_approved/n_pending yang TIDAK ada → KeyError
        # dilempar SEBELUM try/finally di bawah → temuan.json tertinggal dalam
        # kondisi ter-filter dan run berikutnya menimpa backup → temuan asli
        # hilang permanen. (Temuan audit #B1.)
        edit_str = f", edits_applied={stats.get('n_edits_applied', 0)}" if stats.get('n_edits_applied') else ""
        filter_note = (
            f" | FILTER:review-applied "
            f"({stats.get('n_included', '?')}/{stats.get('n_total', '?')} masuk, "
            f"rejected={stats.get('n_rejected', 0)}{edit_str})"
        )
    try:
        code, out, err = await run_v6_script(
            "scripts/render_kkp.py",
            [
                "--penugasan",
                args["penugasan_folder"],
                "--anggota",
                args["nama_anggota"],
            ],
            timeout=120,
        )
    finally:
        _restore_temuan_from_backup(folder, backup)
    if code != 0:
        return {
            "content": [{"type": "text", "text": f"FAILED|exit={code}|err={err[:400]}{filter_note}"}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": f"OK|stdout={out[:200]}{filter_note}"}]}


@tool(
    "run_qc_kkp",
    "Jalankan QC SAIPI stage KKP secara SYNCHRONOUS. Memanggil scripts/qc_saipi.py "
    "V6 dengan --stage kkp lalu return status + breakdown severity + excerpt laporan. "
    "Pakai SETELAH semua temuan + KKP.docx selesai untuk gate kepatuhan SAIPI.",
    {"penugasan_folder": str},
)
async def run_qc_kkp(args: dict) -> dict:
    """Sync version dari QC KKP — ganti pola async marker-flag yang lama.

    Pola lama (`request_qc_kkp` writer flag) bermasalah: agen yang memanggilnya
    tidak dapat hasil → improvisasi sendiri. Sync version langsung jalankan
    qc_saipi.py V6 dan return ringkasan untuk dipakai agen langsung.
    """
    folder = Path(args["penugasan_folder"])
    if not folder.exists():
        return {
            "content": [{
                "type": "text",
                "text": f"FAILED|folder penugasan tidak ada: {folder} — cek path (typo?), jangan anggap PASS",
            }],
            "is_error": True,
        }
    code, out, err = await run_v6_script(
        "scripts/qc_saipi.py",
        ["--penugasan", str(folder), "--stage", "kkp"],
        timeout=120,
    )

    # qc_saipi.py exit code: 0=PASS, 2=ada KRITIS (checklist tetap valid),
    # selain itu = ERROR EKSEKUSI → jangan baca checklist (bisa file basi run
    # sebelumnya → status "PASS" palsu). (Temuan audit #E2.)
    if code not in (0, 2):
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"FAILED|stage=kkp|qc_saipi gagal dieksekusi (exit={code}) — "
                    f"status QC TIDAK diketahui, JANGAN anggap PASS. err={err[:300]}"
                ),
            }],
            "is_error": True,
        }

    checklist = safe_read_json(folder / "_QA-SAIPI" / "checklist-kkp.json")
    total_kritis, total_peringatan, total_needs_review, total_ok = qc_summary_counts(checklist)

    if total_kritis > 0:
        status_label = "BLOCKED_KRITIS"
    elif total_peringatan > 0 or total_needs_review > 0:
        status_label = "PASS_WITH_WARNINGS"
    else:
        status_label = "PASS"

    laporan_path = folder / "_QA-SAIPI" / "laporan-qa-kkp.md"
    laporan_excerpt = ""
    if laporan_path.exists():
        laporan_excerpt = laporan_path.read_text(encoding="utf-8")[:4000]

    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"stage=kkp|status={status_label}|exit_code={code}|"
                    f"kritis={total_kritis}|peringatan={total_peringatan}|"
                    f"needs_review={total_needs_review}|ok={total_ok}|"
                    f"laporan_path={laporan_path}\n\n"
                    f"=== LAPORAN QA (excerpt) ===\n{laporan_excerpt}"
                ),
            }
        ]
    }


# =============================================================================
# CONTEXT GENERATION — AI susun context.md dari digest + sasaran (Step 0 AT)
# =============================================================================


# Field kunci yang DIHARAPKAN ada per jenis digest. Sumber tunggal — dipakai
# _run_ingestion (deteksi field hilang → fallback LLM) dan digestion_harness
# (metrik cakupan). Cocokkan dengan key yang diisi _summarize_digest_raw.
COVERAGE_KEYS = {
    "TOR": ["kementerian", "program_nama", "kegiatan_nama", "ro", "total_biaya", "dasar_hukum"],
    "RAB": ["kementerian", "ro", "jumlah_komponen", "total_pagu"],
    # Field PENGADAAN diperluas 3 Jun 2026 (hybrid agresif). KAK & HPS sering
    # non-standar (prefix Signed_, layout berbeda per Satker) → field penting yg
    # auditor butuhkan untuk temuan substantif (dasar_hukum KAK, sumber referensi
    # harga HPS, metode pemilihan, dll) sering kosong di parser deterministik.
    # Dgn field ini ke COVERAGE_KEYS, fallback Haiku akan dipicu otomatis utk
    # mengisi field hilang. Tetap parser-first; Haiku hanya per dokumen kurang.
    "PENGADAAN": [
        "obyek", "nilai_hps", "jangka_waktu",
        "dasar_hukum_kak", "ruang_lingkup", "spesifikasi_teknis_ringkas",
        "metode_pemilihan", "jadwal_pengadaan",
        "sumber_referensi_harga", "nama_vendor_rfi",
        "masa_berlaku_existing",
    ],
}


def _overlay_fallback(data: dict, out: dict) -> dict:
    """Tumpangkan nilai dari blok `_llm_fallback` (hasil fallback LLM saat ingestion)
    untuk key ringkasan yang KOSONG dari parse deterministik.

    Digest deterministik dibiarkan apa adanya (jujur); nilai pulihan disimpan
    terpisah di `data["_llm_fallback"]` saat ingestion. Di sini kita isikan ke
    ringkasan agar konsumen (read_ingested_digest, harness) melihatnya. Provenans
    dicatat di `out["_llm_recovered"]`.
    """
    if not isinstance(data, dict):
        return out
    fb = data.get("_llm_fallback")
    if not isinstance(fb, dict):
        return out
    recovered = []
    for k, v in fb.items():
        if k == "_meta":
            continue
        if out.get(k) in (None, "", [], 0) and v not in (None, "", [], 0):
            out[k] = v
            recovered.append(k)
    if recovered:
        out["_llm_recovered"] = recovered
    return out


def _summarize_digest(name: str, data: dict) -> dict:
    """Ringkasan field kunci satu file digest (untuk context.md / metrik / agen).

    Membungkus parse deterministik (`_summarize_digest_raw`) lalu menumpangkan
    field hasil fallback LLM bila ada (`_overlay_fallback`).
    """
    out = _summarize_digest_raw(name, data)
    return _overlay_fallback(data, out)


def _summarize_digest_raw(name: str, data: dict) -> dict:
    """Ambil field kunci dari satu file digest untuk bahan context.md.

    Catatan: digest RAB JUGA punya `identitas_ro` (seperti TOR), jadi RAB harus
    dideteksi LEBIH DULU (lewat `komponen`/`total_pagu`) — kalau tidak, RAB salah
    ter-label TOR & data komponen/pagu hilang. Pengadaan menyimpan hasil per-dokumen
    di bawah `dokumen`, bukan top-level.
    """
    out: dict = {"file": name}
    if not isinstance(data, dict):
        return out

    # RAB (digest_rab): punya komponen / total_pagu (cek SEBELUM TOR).
    komp = data.get("komponen")
    if komp is not None or data.get("total_pagu") is not None:
        out["jenis"] = "RAB"
        ident = data.get("identitas_ro") or data.get("identitas") or {}
        if isinstance(ident, dict):
            for k in ("kementerian", "unit_eselon_i", "program_nama", "program",
                      "kegiatan_nama", "kegiatan", "ro", "alokasi_dana"):
                if ident.get(k):
                    out[k] = ident[k]
        if isinstance(komp, list):
            out["jumlah_komponen"] = len(komp)
        if data.get("total_pagu") is not None:
            out["total_pagu"] = data["total_pagu"]
        return out

    # TOR (digest_tor): identitas_ro + biaya + dasar_hukum (tanpa komponen).
    idr = data.get("identitas_ro")
    if isinstance(idr, dict):
        out["jenis"] = "TOR"
        for k in ("kementerian", "unit_eselon_i", "program_nama", "kegiatan_nama",
                  "ro", "volume", "satuan"):
            if idr.get(k):
                out[k] = idr[k]
        biaya = data.get("biaya")
        if isinstance(biaya, dict) and biaya.get("total"):
            out["total_biaya"] = biaya["total"]
            if biaya.get("sumber_dana"):
                out["sumber_dana"] = biaya["sumber_dana"]
        dh = data.get("dasar_hukum")
        if isinstance(dh, list):
            out["dasar_hukum"] = [
                f"{d.get('jenis_regulasi') or ''} {d.get('nomor') or ''}/{d.get('tahun') or ''}".strip()
                for d in dh[:8]
            ]
        return out

    # Pengadaan (digest_pengadaan): hasil per-dokumen di `dokumen.{kak,hps,rfi,kontrak}`.
    dok = data.get("dokumen")
    if isinstance(dok, dict):
        out["jenis"] = "PENGADAAN"
        out["dokumen_per_jenis"] = {k: len(v) for k, v in dok.items() if isinstance(v, list)}

        def _first_parsed(key: str) -> dict:
            lst = dok.get(key) or []
            p = lst[0].get("parsed") if lst and isinstance(lst[0], dict) else None
            return p if isinstance(p, dict) else {}

        kak, hps = _first_parsed("kak"), _first_parsed("hps")
        nama = kak.get("nama_pekerjaan") or hps.get("nama_pekerjaan")
        if nama:
            out["obyek"] = nama
        nilai = hps.get("nilai_hps") or kak.get("nilai_hps")
        if nilai:
            out["nilai_hps"] = nilai
        per = kak.get("periode") or hps.get("periode")
        if per:
            out["jangka_waktu"] = per
        if kak.get("sla_value"):
            out["sla"] = kak["sla_value"]
        return out

    # Digest generik (digest_generic — dipakai skill criteria-driven: *-umum,
    # audit-kinerja, evaluasi-*, pemantauan-*, konsultansi): tak punya komponen/
    # identitas_ro/dokumen, tapi punya ringkasan_teks + kata_kunci + regulasi.
    # Surface teks-nya agar read_ingested_digest berguna tanpa buka PDF (hemat token).
    if data.get("ringkasan_teks") is not None or data.get("kata_kunci") is not None:
        out["jenis"] = data.get("jenis") or "GENERIK"
        rk = str(data.get("ringkasan_teks") or "")
        if rk:
            out["ringkasan_teks"] = rk[:1800]
        if data.get("halaman_total"):
            out["halaman_total"] = data["halaman_total"]
        for k in ("kata_kunci", "regulasi_terdeteksi", "tanggal_terdeteksi",
                  "nilai_rupiah_terdeteksi"):
            v = data.get(k)
            if isinstance(v, list) and v:
                out[k] = v[:20]
            elif v:
                out[k] = v
        return out

    # Fallback: pengadaan top-level (struktur lama).
    out["jenis"] = "PENGADAAN"
    for k in ("obyek", "nilai_hps", "metode_pemilihan", "jangka_waktu", "sla"):
        if data.get(k):
            out[k] = data[k]
    return out


@tool(
    "read_ingested_digest",
    "Baca RINGKASAN isi hasil ingestion (_INGESTED/*.json) — field kunci seperti "
    "kementerian, program, kegiatan, RO, volume, total biaya, dasar hukum, jumlah "
    "komponen RAB. Dipakai untuk menyusun context.md. Return JSON ringkas (di-cap).",
    {"penugasan_folder": str},
)
async def read_ingested_digest(args: dict) -> dict:
    folder = Path(args["penugasan_folder"]) / "_INGESTED"
    items: list[dict] = []
    if folder.exists():
        for p in sorted(folder.glob("*.json")):
            data = safe_read_json(p)
            items.append(_summarize_digest(p.name, data))
    # Cap TANPA memotong di tengah string JSON — slicing dumps() menghasilkan
    # JSON invalid yang membingungkan agen saat digest banyak (audit #B7).
    # Strategi: perpendek ringkasan_teks bertahap, lalu (bila masih besar)
    # buang item ekor dengan penanda eksplisit — tetap JSON valid.
    def _dump(payload: dict) -> str:
        return json.dumps(payload, ensure_ascii=False)

    # Budget diperbesar 8000→20000 (18 Jul): saat pengadaan pindah ke digest
    # generik, ringkasan yang terlalu pendek memaksa agen membaca ulang PDF
    # (20x read_pdf_page). Dgn budget lebih besar, isi per-dokumen (≤1800 char)
    # utuh sampai ±10 dokumen → agen mulai dgn fakta lebih lengkap, hemat baca PDF.
    _BUDGET = 20000
    payload = {"total": len(items), "digest": items}
    text = _dump(payload)
    if len(text) > _BUDGET:
        for cap in (1800, 1100, 600):
            for it in items:
                if isinstance(it.get("ringkasan_teks"), str) and len(it["ringkasan_teks"]) > cap:
                    it["ringkasan_teks"] = it["ringkasan_teks"][:cap] + "…"
            text = _dump(payload)
            if len(text) <= _BUDGET:
                break
    total_asli = len(items)
    while len(text) > _BUDGET and len(items) > 1:
        items.pop()
        payload = {
            "total": total_asli,
            "digest": items,
            "terpotong": f"{total_asli - len(items)} digest tidak ditampilkan — panggil read_pdf_page per-file bila perlu",
        }
        text = _dump(payload)
    return {"content": [{"type": "text", "text": text}]}


@tool(
    "get_team_members",
    "Daftar anggota tim penugasan (nama + NIP) berdasarkan assigned_to di "
    "sasaran-assignment.json, di-lookup ke data user. Dipakai untuk mengisi tabel "
    "Tim di context.md. Jabfung tidak tersimpan di sistem — gunakan default wajar.",
    {"penugasan_folder": str},
)
async def get_team_members(args: dict) -> dict:
    from app.database import SessionLocal
    from app.models import User

    folder = Path(args["penugasan_folder"])
    assignment = safe_read_json(folder / "_PKP" / "sasaran-assignment.json")
    names: list[str] = []
    if isinstance(assignment, dict):
        for s in assignment.get("sasaran", []) or []:
            for nm in (s.get("assigned_to") or []):
                if nm and nm not in names:
                    names.append(nm)

    members: list[dict] = []
    if names:
        async with SessionLocal() as db:
            rows = (
                await db.execute(select(User).where(User.nama_lengkap.in_(names)))
            ).scalars().all()
            found = {u.nama_lengkap: u.nip for u in rows}
        for nm in names:
            members.append({"nama": nm, "nip": found.get(nm, "[DIISI AUDITOR]")})

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({"anggota": members}, ensure_ascii=False),
        }]
    }


@tool(
    "write_context_md",
    "Tulis/timpa context.md penugasan dengan konten lengkap (markdown). Pakai untuk "
    "menyimpan context.md hasil generate AI. WAJIB format lolos QC: ada baris "
    "`Tujuan: ...` dan `Ruang Lingkup: ...` (inline, bukan heading), tabel Tim dengan "
    "jabfung (mis. Auditor Madya/Muda/Pertama), tanpa placeholder selain [DIISI AUDITOR].",
    {"penugasan_folder": str, "content": str},
)
async def write_context_md(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    content = args.get("content", "")
    if not content.strip():
        return {
            "content": [{"type": "text", "text": "FAILED|content kosong"}],
            "is_error": True,
        }
    path = folder / "context.md"
    path.write_text(content, encoding="utf-8")
    return {
        "content": [{
            "type": "text",
            "text": f"OK|context.md ditulis ({len(content)} char)",
        }]
    }


# `read_temuan_json` aslinya didefinisikan di lhr_tools (untuk KT). Kita reuse
# di AT supaya bisa deteksi REFINE mode (apakah temuan existing sudah ada) —
# tanpa ini agen AT selalu mulai dari nol saat auditor minta koreksi.
from app.tools.lhr_tools import read_temuan_json  # noqa: E402


@tool(
    "build_context_md_template",
    "Susun context.md DETERMINISTIK dari field penugasan + digest hasil ingestion. "
    "Mengisi 80% bagian context (Identitas, Periode, Tujuan/Ruang Lingkup per skill, "
    "Tim, Ringkasan Obyek dari digest). Bagian 'Gambaran Umum' di-placeholder "
    "`<!-- AI_PARAGRAPH:gambaran_umum -->` untuk diisi LLM/auditor. TIDAK panggil "
    "LLM. Pakai ini sebagai LANGKAH AWAL sebelum write_context_md.",
    {"penugasan_folder": str, "kode": str, "obyek": str, "skill": str,
     "nomor_st": str, "tanggal_st": str, "gambaran_umum": str, "overwrite": bool},
)
async def build_context_md_template(args: dict) -> dict:
    from app.context_template import build_context_md
    folder = Path(args["penugasan_folder"])
    try:
        md = build_context_md(
            kode=args["kode"],
            obyek=args["obyek"],
            skill=args["skill"],
            nomor_st=args.get("nomor_st") or None,
            tanggal_st=args.get("tanggal_st") or None,
            penugasan_folder=folder,
            gambaran_umum=args.get("gambaran_umum") or None,
        )
    except Exception as e:  # noqa: BLE001
        return {
            "content": [{"type": "text", "text": f"FAILED|{e}"}],
            "is_error": True,
        }
    overwrite = bool(args.get("overwrite", False))
    path = folder / "context.md"
    if path.exists() and not overwrite:
        return {
            "content": [{
                "type": "text",
                "text": (
                    f"OK|template siap ({len(md)} char). context.md SUDAH ada — "
                    f"set overwrite=true untuk timpa, atau pakai output ini "
                    f"sebagai bahan write_context_md:\n\n{md}"
                ),
            }]
        }
    folder.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")
    return {
        "content": [{
            "type": "text",
            "text": f"OK|context.md ditulis dari template ({len(md)} char) @ {path}",
        }]
    }


@tool(
    "write_penilaian_aspek",
    "Rekam KESIMPULAN penilaian per aspek/butir checklist SKILL (bukan hanya temuan) ke "
    "_KKP/penilaian-aspek.json. WAJIB untuk reviu/audit ber-KKSA: tutup TIAP butir checklist "
    "yang dinilai — TERMASUK yang SESUAI/memadai — supaya cakupan penilaian TERDOKUMENTASI, "
    "bukan hanya daftar temuan (exception-only). Contoh butir reviu-pengadaan: identifikasi "
    "kebutuhan, spesifikasi teknis (jelas/terukur/tidak over-under-spec), 5 elemen justifikasi "
    "KAK, metodologi HPS, dll. Struktur: aspek=[{aspek, kesimpulan: SESUAI|TIDAK_SESUAI|"
    "TIDAK_CUKUP_DATA, dasar}]. dasar = 1 kalimat pembenaran (bukti dari dokumen). Ditampilkan "
    "render_kkp sebagai tabel 'Kesimpulan Penilaian per Aspek'. Panggil SEBELUM render_kkp_docx.",
    {"penugasan_folder": str, "aspek": list},
)
async def write_penilaian_aspek(args: dict) -> dict:
    folder = Path(args["penugasan_folder"])
    out_dir = folder / "_KKP"
    out_dir.mkdir(parents=True, exist_ok=True)
    _VALID = {"SESUAI", "TIDAK_SESUAI", "TIDAK_CUKUP_DATA"}
    rows: list[dict] = []
    for a in (args.get("aspek") or []):
        if not isinstance(a, dict):
            continue
        k = str(a.get("kesimpulan", "")).strip().upper().replace(" ", "_").replace("-", "_")
        if k not in _VALID:
            k = "TIDAK_CUKUP_DATA"
        rows.append({
            "aspek": str(a.get("aspek", "")).strip(),
            "kesimpulan": k,
            "dasar": str(a.get("dasar", "")).strip(),
        })
    out = out_dir / "penilaian-aspek.json"
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"aspek": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, out)
    n_ts = sum(1 for r in rows if r["kesimpulan"] == "TIDAK_SESUAI")
    n_tcd = sum(1 for r in rows if r["kesimpulan"] == "TIDAK_CUKUP_DATA")
    return {"content": [{"type": "text", "text":
            f"OK|penilaian-aspek ditulis|n_aspek={len(rows)}|tidak_sesuai={n_ts}|tidak_cukup_data={n_tcd}"}]}


KKP_TOOLS = [
    read_context, list_ingested, read_ingested_digest, get_team_members,
    write_context_md, build_context_md_template,
    append_temuan, reset_temuan, get_kodefikasi_temuan, write_penilaian_aspek,
    render_kkp_docx, run_qc_kkp,
    read_temuan_json,
]
