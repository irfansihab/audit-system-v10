"""Routes autentikasi — prototype login dengan role saja.

Karena ini prototype internal, login tidak butuh password atau NIP.
Auditor cukup pilih role di UI, backend auto-pick user seed pertama
yang punya `role_default == role` tersebut.

Produksi nanti diganti SSO Komdigi (OIDC).
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import login_guard
from app.auth import (
    create_session_token,
    decode_session_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.config import get_settings
from app.database import get_db
from app.models import Role, User
from app.schemas import ChangePasswordRequest, LoginRequest, SessionOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=SessionOut)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)) -> SessionOut:
    """Login username + password (Workstream B).

    Jalur utama: `username` + `password` → verifikasi bcrypt → token (role = role_default user).
    Jalur LEGACY (dev only, APP_ENV != production): `role` (+ optional `email`) tanpa password.
    """
    # --- Jalur utama: username + password ---
    if req.username and req.password:
        # Proteksi brute-force: tolak lebih dulu bila akun sedang terkunci.
        locked = login_guard.locked_seconds(req.username)
        if locked:
            menit = (locked + 59) // 60
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                f"Terlalu banyak percobaan gagal. Coba lagi dalam ±{menit} menit.",
            )
        user = (
            await db.execute(select(User).where(User.username == req.username))
        ).scalar_one_or_none()
        if not user or not verify_password(req.password, user.password_hash):
            sisa = login_guard.record_failure(req.username)
            pesan = "Username atau password salah."
            if sisa == 0:
                pesan = "Username atau password salah. Akun dikunci sementara karena terlalu banyak percobaan."
            elif sisa <= 2:
                pesan = f"Username atau password salah. Sisa {sisa} percobaan sebelum akun dikunci."
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, pesan)
        login_guard.record_success(req.username)
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


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    req: ChangePasswordRequest,
    current: tuple[User, Role] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Ganti password sendiri (B4). Perlu sesi aktif + password lama benar."""
    user, _ = current
    if not verify_password(req.old_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Password lama salah.")
    min_len = get_settings().password_min_length
    if len(req.new_password) < min_len:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Password baru minimal {min_len} karakter.",
        )
    if req.new_password == req.old_password:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Password baru harus berbeda dari yang lama."
        )
    user.password_hash = hash_password(req.new_password)
    await db.commit()


@router.get("/users")
async def list_users(
    request: Request,
    role: Role | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Daftar user seed (opsional filter by role_default).

    Dipakai layar login (PRA-auth) untuk pilihan akun, dan oleh KT (PASCA-auth)
    untuk dropdown assignment sasaran. Dulu selalu mengembalikan email+NIP
    tanpa autentikasi → enumerasi identitas pegawai oleh siapa pun yang bisa
    menjangkau backend (audit #B9). Kini: TANPA token yang valid → hanya field
    minimum yang memang dibutuhkan layar login (username, nama, role); dengan
    token → lengkap.
    """
    authed = False
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            decode_session_token(auth_header[7:])
            authed = True
        except HTTPException:
            authed = False

    stmt = select(User).order_by(User.id)
    if role is not None:
        stmt = stmt.where(User.role_default == role)
    rows = (await db.execute(stmt)).scalars().all()
    if authed:
        return [UserOut.model_validate(u).model_dump() for u in rows]
    return [
        {
            "id": u.id,
            "username": u.username,
            "nama_lengkap": u.nama_lengkap,
            "role_default": u.role_default.value if hasattr(u.role_default, "value") else u.role_default,
        }
        for u in rows
    ]
