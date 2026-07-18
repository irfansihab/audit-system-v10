"""Routes Administrasi / Pasca-Persetujuan (Tahapan 8 — peran TU).

Ranah ADMINISTRASI di garis serah: setelah laporan disetujui, TU mengelola paket
ekspor (LHP final + Daftar Temuan & Rekomendasi) + draft surat penyampaian.
Lingkup "handoff + register ringkas": penomoran resmi/TTE/distribusi/arsip TETAP
di SIMWAS. Tindak lanjut dipantau via modul TLHP (sudah ter-ingest saat approval).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.models import LhpReview, Penugasan, Role, User
from app.storage import save_upload

router = APIRouter(prefix="/penugasan", tags=["administrasi"])

_WRITE_ROLES = {Role.TU, Role.PT, Role.PM, Role.ADMIN}

# Daftar dokumen kelengkapan administrasi (mengacu pedoman/SDP). TU mengunggah
# dokumen yang sudah ditandatangani/diproses (di luar produksi substansi v9).
ADMIN_DOCS = [
    {"kode": "ST", "nama": "Surat Tugas", "wajib": True},
    {"kode": "SURAT_PENGANTAR", "nama": "Surat Pengantar Penugasan", "wajib": False},
    {"kode": "PAKTA_INTEGRITAS", "nama": "Pakta Integritas", "wajib": False},
    {"kode": "PERMINTAAN_DATA", "nama": "Surat Permintaan Data", "wajib": True},
    {"kode": "PENYERAHAN_DATA", "nama": "BA / Surat Penyerahan Data", "wajib": False},
    {"kode": "NOTULENSI", "nama": "Notulensi / Kesepakatan Pelaksanaan", "wajib": False},
    {"kode": "BA_PEMBAHASAN", "nama": "Berita Acara Pembahasan Hasil (Exit Meeting)", "wajib": True},
    {"kode": "PERSETUJUAN_DHP", "nama": "Lembar Persetujuan Daftar Hasil/Temuan", "wajib": True},
    {"kode": "SURAT_PENYAMPAIAN", "nama": "Surat Penyampaian LHP (final ber-TTE)", "wajib": True},
    {"kode": "BUKTI_TL", "nama": "Bukti / Laporan Tindak Lanjut", "wajib": False},
    {"kode": "LAINNYA", "nama": "Dokumen administrasi lainnya", "wajib": False},
]
_ADMIN_KODE = {d["kode"] for d in ADMIN_DOCS}
_KELENGKAPAN_SUB = "_ADMIN/kelengkapan"


async def _penugasan(db: AsyncSession, pid: int) -> Penugasan:
    p = (await db.execute(select(Penugasan).where(Penugasan.id == pid))).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Penugasan tidak ditemukan.")
    return p


async def _is_approved(db: AsyncSession, pid: int) -> bool:
    r = (await db.execute(
        select(LhpReview).where(LhpReview.penugasan_id == pid).order_by(LhpReview.id.desc()).limit(1)
    )).scalar_one_or_none()
    return bool(r and r.status == "APPROVED")


def _docx(folder: Path, sub: str, *, exclude: tuple[str, ...] = ()) -> list[dict]:
    d = folder / sub
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.glob("*.docx")):
        if f.name.startswith("~$") or any(x in f.name for x in exclude):
            continue
        out.append({"name": f.name, "path": str(f.relative_to(folder))})
    return out


def _kelengkapan(folder: Path) -> list[dict]:
    """Checklist dokumen kelengkapan administrasi + file yang sudah diunggah.
    File disimpan `_ADMIN/kelengkapan/<KODE>__<nama asli>`."""
    d = folder / _KELENGKAPAN_SUB
    by_kode: dict[str, list[dict]] = {k: [] for k in _ADMIN_KODE}
    if d.is_dir():
        for f in sorted(d.glob("*")):
            if not f.is_file() or f.name.startswith("."):
                continue
            kode = f.name.split("__", 1)[0]
            if kode in by_kode:
                nama = f.name.split("__", 1)[1] if "__" in f.name else f.name
                by_kode[kode].append({"name": nama, "path": str(f.relative_to(folder))})
    return [
        {"kode": doc["kode"], "nama": doc["nama"], "wajib": doc["wajib"], "files": by_kode[doc["kode"]]}
        for doc in ADMIN_DOCS
    ]


@router.get("/{penugasan_id}/administrasi")
async def get_administrasi(
    penugasan_id: int,
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    p = await _penugasan(db, penugasan_id)
    folder = Path(p.folder_path)
    approved = await _is_approved(db, penugasan_id)
    lhp_files = _docx(folder, "_LHP", exclude=("SUBSTANSI", "Daftar-Temuan", "Surat-Penyampaian"))
    daftar = _docx(folder, "_LHP")
    daftar = [f for f in daftar if f["name"].startswith("Daftar-Temuan")]
    surat = _docx(folder, "_ADMIN")
    return {
        "penugasan_id": p.id,
        "approved": approved,
        "paket_ekspor": {
            "lhp": lhp_files,
            "daftar_temuan": daftar,          # auto-generate saat approval (Fase 3)
        },
        "surat_penyampaian": surat,           # draft (Tahapan 8)
        "kelengkapan": _kelengkapan(folder),  # checklist + upload dokumen administrasi (pedoman)
        "catatan_simwas": "Penomoran resmi, TTE, distribusi, dan arsip dilakukan di SIMWAS. "
                          "Tindak lanjut dipantau via modul TLHP (rekomendasi ter-ingest saat approval).",
    }


@router.post("/{penugasan_id}/administrasi/kelengkapan")
async def upload_kelengkapan(
    penugasan_id: int,
    kode: str = Form(...),
    file: UploadFile = File(...),
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Unggah satu dokumen kelengkapan administrasi (sesuai pedoman). Peran TU/PT/PM/Admin."""
    _user, role = current
    if role not in _WRITE_ROLES:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unggah kelengkapan hanya untuk TU/PT/PM/Admin.")
    if kode not in _ADMIN_KODE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Kode dokumen tidak dikenal: {kode}")
    p = await _penugasan(db, penugasan_id)
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Maks 50 MB per file.")
    safe = re.sub(r"[^A-Za-z0-9._() -]", "_", (file.filename or "dokumen.bin")).strip() or "dokumen.bin"
    target = Path(p.folder_path) / _KELENGKAPAN_SUB / f"{kode}__{safe}"
    await save_upload(content, target)
    return {"ok": True, "kode": kode, "name": safe, "path": str(target.relative_to(Path(p.folder_path)))}


@router.delete("/{penugasan_id}/administrasi/kelengkapan")
async def hapus_kelengkapan(
    penugasan_id: int,
    path: str,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Hapus satu file kelengkapan (path relatif). Peran TU/PT/PM/Admin."""
    _user, role = current
    if role not in _WRITE_ROLES:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Hapus kelengkapan hanya untuk TU/PT/PM/Admin.")
    p = await _penugasan(db, penugasan_id)
    base = Path(p.folder_path).resolve()
    target = (base / path).resolve()
    # Boundary dgn separator eksplisit — startswith tanpa os.sep meloloskan
    # folder sibling berawalan "_ADMIN..." (mis. "_ADMIN-lain/").
    admin_dir = (base / "_ADMIN").resolve()
    if not (target == admin_dir or str(target).startswith(str(admin_dir) + os.sep)) or not target.is_file():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Path tidak valid.")
    target.unlink()
    return {"ok": True}


@router.post("/{penugasan_id}/administrasi/surat-penyampaian")
async def buat_surat_penyampaian(
    penugasan_id: int,
    payload: dict = Body(default={}),
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    _user, role = current
    if role not in _WRITE_ROLES:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Surat penyampaian hanya untuk TU/PT/PM/Admin.")
    p = await _penugasan(db, penugasan_id)
    if not await _is_approved(db, penugasan_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Laporan belum disetujui — administrasi belum dapat dimulai.")
    from app.export_surat import build_surat_penyampaian
    out = build_surat_penyampaian(
        Path(p.folder_path),
        nomor=str(payload.get("nomor", "")),
        tanggal=str(payload.get("tanggal", "")),
        tujuan=str(payload.get("tujuan", "")),
        perihal=str(payload.get("perihal", "")),
        auditi=str(payload.get("auditi", "")),
    )
    return {"ok": True, "path": str(out.relative_to(Path(p.folder_path))), "name": out.name}
