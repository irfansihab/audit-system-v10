"""Routes autentikasi — prototype login dengan role saja.

Karena ini prototype internal, login tidak butuh password atau NIP.
Auditor cukup pilih role di UI, backend auto-pick user seed pertama
yang punya `role_default == role` tersebut.

Produksi nanti diganti SSO Komdigi (OIDC).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_session_token, verify_password
from app.config import get_settings
from app.database import get_db
from app.models import Role, User
from app.schemas import LoginRequest, SessionOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=SessionOut)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)) -> SessionOut:
    """Login username + password (Workstream B).

    Jalur utama: `username` + `password` → verifikasi bcrypt → token (role = role_default user).
    Jalur LEGACY (dev only, APP_ENV != production): `role` (+ optional `email`) tanpa password.
    """
    # --- Jalur utama: username + password ---
    if req.username and req.password:
        user = (
            await db.execute(select(User).where(User.username == req.username))
        ).scalar_one_or_none()
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Username atau password salah.")
        # role_default tersimpan sbg str di kolom → normalkan ke enum Role.
        role = user.role_default if isinstance(user.role_default, Role) else Role(user.role_default)
        token = create_session_token(user.id, role)
        return SessionOut(user=UserOut.model_validate(user), role_aktif=role, token=token)

    # --- Jalur legacy (dev): role saja, tanpa password ---
    if req.role is not None:
        if get_settings().app_env.lower().startswith("prod"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Login role-only dimatikan di produksi. Gunakan username + password.",
            )
        if req.email:
            user = (await db.execute(select(User).where(User.email == req.email))).scalar_one_or_none()
        else:
            user = (await db.execute(
                select(User).where(User.role_default == req.role).order_by(User.id).limit(1)
            )).scalar_one_or_none()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User role {req.role.value} tidak ditemukan.")
        token = create_session_token(user.id, req.role)
        return SessionOut(user=UserOut.model_validate(user), role_aktif=req.role, token=token)

    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sertakan username + password.")


@router.get("/users", response_model=list[UserOut])
async def list_users(
    role: Role | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[UserOut]:
    """Daftar user seed (opsional filter by role_default).

    Publik (prototype) — dipakai layar login untuk menampilkan pilihan orang
    saat satu role punya >1 user (mis. beberapa Anggota Tim), dan dipakai KT
    untuk dropdown assignment sasaran ke nama AT yang sebenarnya.
    """
    stmt = select(User).order_by(User.id)
    if role is not None:
        stmt = stmt.where(User.role_default == role)
    rows = (await db.execute(stmt)).scalars().all()
    return [UserOut.model_validate(u) for u in rows]
