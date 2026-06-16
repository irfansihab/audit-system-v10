"""Routes TLHP — Tindak Lanjut Hasil Pengawasan (Workstream C5, pilar ke-4).

Memantau status rekomendasi LHP/LHR sampai tuntas — menutup lingkaran pengawasan.
Fase dummy: data dari fixture `tlhp-dummy.json` (nanti diisi dari rekomendasi LHP
terbit Tahapan 7 + sinkron SIMWAS). Aging dihitung di sini dari `tgl_lhp`.

Klasifikasi aging (warna): 0–90 HIJAU · 91–180 KUNING · 181–365 ORANGE · >365 MERAH.
Kritis = umur >365 hari DAN status belum SUDAH.
"""
from datetime import datetime
from pathlib import Path
import json

from fastapi import APIRouter, Depends, Query

from app.auth import get_current_user
from app.models import Role, User

router = APIRouter(prefix="/tlhp", tags=["tlhp"])

_FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "tlhp-dummy.json"


def _aging(umur: int) -> str:
    if umur <= 90:
        return "HIJAU"
    if umur <= 180:
        return "KUNING"
    if umur <= 365:
        return "ORANGE"
    return "MERAH"


def tlhp_enriched() -> list[dict]:
    """Baca fixture + hitung umur/warna/kritis per rekomendasi."""
    try:
        data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []
    today = datetime.utcnow().date()
    out: list[dict] = []
    for r in data.get("rekomendasi", []):
        umur = None
        warna = None
        try:
            tgl = datetime.strptime(str(r.get("tgl_lhp", "")), "%Y-%m-%d").date()
            umur = (today - tgl).days
            warna = _aging(umur)
        except Exception:  # noqa: BLE001
            pass
        status = str(r.get("status", "")).upper()
        selesai = status == "SUDAH"
        out.append({
            **r,
            "umur_hari": umur,
            "warna": warna,
            "kritis": bool(umur is not None and umur > 365 and not selesai),
        })
    return out


def tlhp_summary() -> dict:
    """Ringkasan untuk dashboard F4."""
    items = tlhp_enriched()
    total = len(items)
    by_status: dict[str, int] = {}
    by_warna: dict[str, int] = {}
    for it in items:
        s = str(it.get("status", "")).upper()
        by_status[s] = by_status.get(s, 0) + 1
        w = it.get("warna") or "-"
        by_warna[w] = by_warna.get(w, 0) + 1
    selesai = by_status.get("SUDAH", 0)
    kritis = [it for it in items if it.get("kritis")]
    return {
        "tersedia": True,
        "total": total,
        "selesai": selesai,
        "proses": by_status.get("PROSES", 0),
        "belum": by_status.get("BELUM", 0),
        "tidak_dapat": by_status.get("TIDAK_DAPAT", 0),
        "persen_selesai": round(selesai / total * 100, 1) if total else 0.0,
        "by_warna": by_warna,
        "kritis_count": len(kritis),
        "kritis": [
            {"no_rek": k["no_rek"], "satker": k["satker"], "substansi": k["substansi"][:90],
             "umur_hari": k["umur_hari"], "pic": k.get("pic")}
            for k in sorted(kritis, key=lambda x: x.get("umur_hari") or 0, reverse=True)[:5]
        ],
        "sumber": (json.loads(_FIXTURE.read_text(encoding="utf-8")).get("_meta", {}) if _FIXTURE.exists() else {}).get("sumber", "dummy"),
    }


@router.get("")
async def list_tlhp(
    _current: tuple[User, Role] = Depends(get_current_user),
    satker_kode: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> dict:
    """Daftar rekomendasi TLHP (ber-aging). Filter opsional: satker_kode, status."""
    items = tlhp_enriched()
    if satker_kode:
        items = [i for i in items if i.get("satker_kode") == satker_kode]
    if status:
        items = [i for i in items if str(i.get("status", "")).upper() == status.upper()]
    return {"total": len(items), "items": items}


@router.get("/summary")
async def get_tlhp_summary(
    _current: tuple[User, Role] = Depends(get_current_user),
) -> dict:
    return tlhp_summary()
