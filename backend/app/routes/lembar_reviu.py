"""Lembar Reviu berjenjang (format INTEGRAL/SIMWAS).

Dua level checklist supervisi:
- **KT** (Reviu Ketua Tim) atas Kertas Kerja (KKP) — tahapan 4. Kolom: Permasalahan · Status · Paraf.
- **PT** (Reviu Pengendali Teknis) atas Konsep LHP — tahapan 6. Kolom: Permasalahan · Penyelesaian · Status · Paraf.

Aspek A–D baku (sesuai form INTEGRAL). Reviewer mengisi Status (+ Penyelesaian utk PT)
lalu paraf (sign-off). Disimpan 1 lembar per (penugasan, level) di model `LembarReviu`.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.models import LembarReviu, Penugasan, Role, User

router = APIRouter(prefix="/penugasan", tags=["lembar-reviu"])

# Aspek baku per level (dari form INTEGRAL/SIMWAS) -------------------------- #
KT_ASPEK = [
    {"kode": "A", "aspek": "Kecukupan Informasi dalam Kertas Kerja (On Scope)",
     "deskripsi": "Informasi dalam kertas kerja selaras dengan langkah kerja dalam PKP"},
    {"kode": "B", "aspek": "Kodefikasi Temuan",
     "deskripsi": "Penyajian Kodefikasi Temuan pada kertas kerja telah sesuai dengan standar"},
    {"kode": "C", "aspek": "Kesesuaian Informasi dengan Standard (On Standard)",
     "deskripsi": "KKSA telah lengkap tertuang dalam kertas kerja"},
    {"kode": "D", "aspek": "Ketepatan Waktu",
     "deskripsi": "Pengisian kertas kerja sesuai dengan batas waktu yang telah ditetapkan"},
]

PT_ASPEK = [
    {"kode": "A", "aspek": "Tata Bahasa atau Penyajian (On Standard)",
     "deskripsi": "Pelaksanaan Penugasan dan Penyajian Laporan sesuai dengan standar yang berlaku serta laporan menggunakan tata bahasa dan format penyajian yang tepat",
     "penyelesaian_default": "Laporan sudah sesuai standar, tata bahasa, dan format yang berlaku"},
    {"kode": "B", "aspek": "Kecukupan Substansi",
     "deskripsi": "Informasi yang termuat cukup, andal, relevan, dan berguna/bermanfaat untuk mencapai tujuan penugasan",
     "penyelesaian_default": "Informasi yang termuat sudah cukup, andal, relevan, dan bermanfaat"},
    {"kode": "C", "aspek": "Kesesuaian Ruang Lingkup (On Scope)",
     "deskripsi": "Draft LHP sudah sesuai terhadap sasaran pada kartu penugasan",
     "penyelesaian_default": "LHP sudah sesuai dengan sasaran"},
    {"kode": "D", "aspek": "Ketepatan Waktu",
     "deskripsi": "Pelaksanaan Penugasan dan Penyajian Laporan sesuai dengan waktu yang berlaku",
     "penyelesaian_default": "LHP diselesaikan tepat waktu"},
]

STATUS_OPTIONS = ["Sesuai", "Belum Sesuai"]


def _baku(level: str) -> list[dict]:
    return KT_ASPEK if level == "KT" else PT_ASPEK


def _normalize_level(level: str) -> str:
    lv = (level or "").upper()
    if lv not in ("KT", "PT"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "level harus KT atau PT")
    return lv


class ItemIn(BaseModel):
    kode: str
    status: str = "Sesuai"
    penyelesaian: str | None = None


class LembarReviuIn(BaseModel):
    items: list[ItemIn] = []
    catatan: str | None = None
    diparaf: bool = False


def _merge(level: str, saved: LembarReviu | None) -> dict:
    """Gabungkan aspek baku + isian tersimpan → siap dirender frontend."""
    saved_items = {i.get("kode"): i for i in (saved.items or [])} if saved else {}
    has_peny = level == "PT"
    aspek = []
    for b in _baku(level):
        si = saved_items.get(b["kode"], {})
        row = {
            "kode": b["kode"], "aspek": b["aspek"], "deskripsi": b["deskripsi"],
            "status": si.get("status", "Sesuai"),
        }
        if has_peny:
            row["penyelesaian"] = si.get("penyelesaian", b.get("penyelesaian_default", ""))
        aspek.append(row)
    return {
        "level": level,
        "judul": "Reviu Ketua Tim" if level == "KT" else "Reviu Pengendali Teknis",
        "has_penyelesaian": has_peny,
        "status_options": STATUS_OPTIONS,
        "aspek": aspek,
        "catatan": saved.catatan if saved else None,
        "diparaf": saved.diparaf if saved else False,
        "reviewer_nama": saved.reviewer_nama if saved else None,
        "reviewer_nip": saved.reviewer_nip if saved else None,
        "tanggal": saved.tanggal if saved else None,
        "tersimpan": saved is not None,
    }


async def _get(db: AsyncSession, penugasan_id: int, level: str) -> LembarReviu | None:
    return (await db.execute(
        select(LembarReviu).where(
            LembarReviu.penugasan_id == penugasan_id, LembarReviu.level == level
        )
    )).scalar_one_or_none()


@router.get("/{penugasan_id}/lembar-reviu/{level}")
async def get_lembar_reviu(
    penugasan_id: int,
    level: str,
    _current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    lv = _normalize_level(level)
    saved = await _get(db, penugasan_id, lv)
    return _merge(lv, saved)


@router.post("/{penugasan_id}/lembar-reviu/{level}")
async def save_lembar_reviu(
    penugasan_id: int,
    level: str,
    payload: LembarReviuIn,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    lv = _normalize_level(level)
    user, role = current
    # Role-gate: lembar KT ditandatangani Ketua Tim; lembar PT oleh Pengendali Teknis/Mutu.
    if lv == "KT" and role not in (Role.KT, Role.PT, Role.PM):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Lembar Reviu KT hanya untuk Ketua Tim/Pengendali.")
    if lv == "PT" and role not in (Role.PT, Role.PM):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Lembar Reviu PT hanya untuk Pengendali Teknis/Mutu.")
    p = (await db.execute(select(Penugasan).where(Penugasan.id == penugasan_id))).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Penugasan tidak ditemukan.")

    # Bersihkan items ke kode baku saja.
    valid_kode = {b["kode"] for b in _baku(lv)}
    items = [
        {"kode": it.kode, "status": it.status if it.status in STATUS_OPTIONS else "Sesuai",
         **({"penyelesaian": (it.penyelesaian or "")} if lv == "PT" else {})}
        for it in payload.items if it.kode in valid_kode
    ]

    row = await _get(db, penugasan_id, lv)
    if row is None:
        row = LembarReviu(penugasan_id=penugasan_id, level=lv)
        db.add(row)
    row.items = items
    row.catatan = payload.catatan
    row.diparaf = payload.diparaf
    if payload.diparaf:
        row.reviewer_user_id = user.id
        row.reviewer_nama = user.nama_lengkap
        row.reviewer_nip = getattr(user, "nip", None)
        row.tanggal = datetime.utcnow().date().isoformat()
    await db.commit()
    return {"ok": True, **_merge(lv, await _get(db, penugasan_id, lv))}
