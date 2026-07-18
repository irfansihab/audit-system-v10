"""Routes Dashboard — satu endpoint ringkas untuk beranda (G1 / F7).

Prinsip kinerja & skala (±80 user): agregat dihitung dari query MURAH (GROUP BY
ber-indeks) + fixture, lalu di-cache singkat (TTL) supaya buka dashboard tidak
memukul DB tiap request. Bukan tabel materialized penuh (itu optimasi lanjutan
bila uji beban menuntut) — ini fondasi ringan-dulu.

Sumber data:
- Penugasan status   → DB (ix_penugasan_status)
- EWS                → DB EwsFinding (ix_ews_findings_status) — fallback kosong
- PKPT (F2)          → fixture pkpt-dummy.json (dummy; nanti sinkron SIMWAS)
- Capaian kinerja(F6)→ fixture capaian-kinerja.json (manual; nanti API kinerja)
- TLHP / permintaan / tren temuan → STUB (modul belum dibangun: C5/F3/F5)
"""
import json
import time
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.models import EwsFinding, Penugasan, Role, User
from app.routes.tlhp import tlhp_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
_PKPT_FIXTURE = _FIXTURES / "pkpt-dummy.json"
_KINERJA_FIXTURE = _FIXTURES / "capaian-kinerja.json"

# Cache ringan global (data org-wide). TTL pendek → ringan untuk banyak user
# tanpa data basi. time.monotonic() aman (bukan wall clock).
_TTL_SECONDS = 30.0
_cache: dict = {"data": None, "ts": 0.0}


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — fixture hilang/rusak → bagian itu kosong
        return {}


def _pkpt_summary() -> dict:
    d = _load_json(_PKPT_FIXTURE)
    items = d.get("kegiatan", []) if isinstance(d, dict) else []
    by_status: dict[str, int] = {}
    for it in items:
        s = str(it.get("status", "")).upper()
        by_status[s] = by_status.get(s, 0) + 1
    total = len(items)
    selesai = by_status.get("SELESAI", 0)
    return {
        "total": total,
        "selesai": selesai,
        "berjalan": by_status.get("BERJALAN", 0),
        "rencana": by_status.get("RENCANA", 0),
        "tertunda": by_status.get("TERTUNDA", 0),
        "persen_selesai": round(selesai / total * 100, 1) if total else 0.0,
        "sumber": (d.get("_meta", {}) or {}).get("sumber", "dummy"),
    }


def _kinerja_summary() -> dict:
    d = _load_json(_KINERJA_FIXTURE)
    return {
        "indikator": d.get("indikator", []) if isinstance(d, dict) else [],
        "sumber": (d.get("_meta", {}) or {}).get("sumber", "manual"),
    }


async def _penugasan_summary(db: AsyncSession) -> dict:
    rows = (await db.execute(
        select(Penugasan.status, func.count()).group_by(Penugasan.status)
    )).all()
    by_status = {str(getattr(s, "value", s)): n for s, n in rows}
    total = sum(by_status.values())
    # "aktif" = bukan draft/selesai final (heuristik ringan).
    selesai_like = sum(v for k, v in by_status.items() if "LHP_DONE" in k or "SELESAI" in k.upper())
    return {"total": total, "by_status": by_status, "selesai": selesai_like, "aktif": total - selesai_like}


async def _ews_summary(db: AsyncSession) -> dict:
    rows = (await db.execute(
        select(EwsFinding.status, func.count()).group_by(EwsFinding.status)
    )).all()
    by_status = {str(s): n for s, n in rows}
    latest = (await db.execute(
        select(EwsFinding.kode, EwsFinding.satker, EwsFinding.status, EwsFinding.judul)
        .order_by(EwsFinding.id.desc()).limit(5)
    )).all()
    return {
        "by_status": by_status,
        "merah": by_status.get("MERAH", 0),
        "kuning": by_status.get("KUNING", 0),
        "terbaru": [
            {"kode": k, "satker": sk, "status": st, "judul": (j or "")[:120]}
            for k, sk, st, j in latest
        ],
    }


@router.get("/summary")
async def dashboard_summary(
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Ringkasan beranda — satu panggilan, di-cache ~30 detik (ringan utk ±80 user)."""
    now = time.monotonic()
    user, role = current
    role_str = role.value if hasattr(role, "value") else str(role)
    if _cache["data"] is not None and (now - _cache["ts"]) < _TTL_SECONDS:
        # _role selalu milik PEMANGGIL — dulu ikut ter-cache dari user pertama
        # yang mengisi cache, jadi user lain melihat role orang lain di payload.
        return {**_cache["data"], "_role": role_str}

    data = {
        "penugasan": await _penugasan_summary(db),
        "ews": await _ews_summary(db),
        "pkpt": _pkpt_summary(),
        "capaian_kinerja": _kinerja_summary(),
        "tlhp": await tlhp_summary(db),  # F4 — modul C5 (DB-backed)
        # Stub — modul belum dibangun (roadmap): F3 permintaan · F5 tren temuan.
        "permintaan_belum_ditindaklanjuti": {"tersedia": False, "catatan": "Belum ada model permintaan (F3)."},
        "tren_temuan_berulang": {"tersedia": False, "catatan": "Belum dirakit (F5)."},
        "_role": role_str,
        "_cache_ttl_detik": int(_TTL_SECONDS),
    }
    _cache["data"] = data
    _cache["ts"] = now
    return data
