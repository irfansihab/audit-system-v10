"""Inisialisasi database: buat tabel + seed user uji.

Dipanggil saat first deploy (lihat fly.toml `release_command`) atau manual:
    python -m app.init_db
"""
import asyncio

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Role, User


# Password DEV bersama untuk semua akun seed (Workstream B). Dipakai quick-login
# auto-fill di layar login. PRODUKSI: ganti password per akun + matikan quick-login.
DEV_PASSWORD = "audit2026"

SEED_USERS = [
    {
        "username": "sarah",
        "email": "auditor.at@komdigi.go.id",
        "nama_lengkap": "Sarah Aulia",
        "nip": "198501012010011001",
        "role_default": Role.AT,
    },
    {
        "username": "citra",
        "email": "auditor.at2@komdigi.go.id",
        "nama_lengkap": "Citra Lestari",
        "nip": "198803152012012002",
        "role_default": Role.AT,
    },
    {
        "username": "budi",
        "email": "auditor.kt@komdigi.go.id",
        "nama_lengkap": "Budi Hartono",
        "nip": "197505152005011002",
        "role_default": Role.KT,
    },
    {
        "username": "inspektur",
        "email": "inspektorat2.kominfo.2@gmail.com",
        "nama_lengkap": "Inspektorat II Komdigi",
        "nip": "197001012000011001",
        "role_default": Role.PT,
    },
    {
        "username": "doddy",
        "email": "pengendali.mutu@komdigi.go.id",
        "nama_lengkap": "Doddy Setiadi",
        "nip": "197203102000031001",
        "role_default": Role.PM,
    },
]


async def seed_auth(db) -> None:
    """Migrasi + seed username/password seed users (idempoten, dipanggil di startup).

    Tabel `users` lama (audit_v7) belum punya kolom username/password_hash → ALTER
    IF NOT EXISTS. Lalu isi username + bcrypt(DEV_PASSWORD) untuk akun seed yang kosong.
    """
    from sqlalchemy import text

    from app.auth import hash_password

    # 1) Kolom (Postgres) — aman bila sudah ada.
    for ddl in (
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(80)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(200)",
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users(username)",
    ):
        try:
            await db.execute(text(ddl))
        except Exception:  # noqa: BLE001
            pass
    await db.commit()

    # 2) Set username + password utk akun seed (insert akun baru spt PM bila belum ada).
    for u in SEED_USERS:
        row = (await db.execute(select(User).where(User.email == u["email"]))).scalar_one_or_none()
        if row is None:
            db.add(User(
                username=u["username"], email=u["email"], nama_lengkap=u["nama_lengkap"],
                nip=u["nip"], role_default=u["role_default"],
                password_hash=hash_password(DEV_PASSWORD),
            ))
            continue
        if not getattr(row, "username", None):
            row.username = u["username"]
        if not getattr(row, "password_hash", None):
            row.password_hash = hash_password(DEV_PASSWORD)
    await db.commit()


async def init():
    print("[init_db] Membuat tabel ...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("[init_db] Seed users (upsert: insert kalau belum ada, update kalau role/nama/nip beda) ...")
    async with SessionLocal() as session:
        for u in SEED_USERS:
            existing = (
                await session.execute(select(User).where(User.email == u["email"]))
            ).scalar_one_or_none()
            if existing:
                # Upsert: cek apakah field-field penting perlu di-update
                # (mis. migrasi PM → PT di production yang sudah punya user existing)
                changed = []
                if existing.role_default != u["role_default"]:
                    changed.append(
                        f"role_default: {existing.role_default.value if hasattr(existing.role_default, 'value') else existing.role_default} → {u['role_default'].value}"
                    )
                    existing.role_default = u["role_default"]
                if existing.nama_lengkap != u["nama_lengkap"]:
                    changed.append(f"nama_lengkap: {existing.nama_lengkap!r} → {u['nama_lengkap']!r}")
                    existing.nama_lengkap = u["nama_lengkap"]
                if existing.nip != u["nip"]:
                    changed.append(f"nip: {existing.nip!r} → {u['nip']!r}")
                    existing.nip = u["nip"]
                if changed:
                    print(f"  ~ {u['email']} UPDATE: {', '.join(changed)}")
                else:
                    print(f"  - {u['email']} sudah ada, tidak ada perubahan")
                continue
            session.add(User(**u))
            print(f"  + {u['email']} ({u['role_default'].value})")
        await session.commit()
    print("[init_db] Selesai.")


if __name__ == "__main__":
    asyncio.run(init())
