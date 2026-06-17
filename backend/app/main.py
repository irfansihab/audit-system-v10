"""Entry point FastAPI."""
import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager

# Windows: asyncpg butuh ProactorEventLoop, tapi uvicorn default pakai SelectorEventLoop.
# Patch ini harus jalan SEBELUM uvicorn spawn event loop — modul-level adalah satu-satunya
# tempat yang pasti dieksekusi lebih awal. Tidak berpengaruh di Linux/Mac.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routes import agen, auth, cacm, dashboard, dokumen, feedback, files, graduasi, knowledge, lembar_reviu, penugasan, skills, tlhp

settings = get_settings()
log = logging.getLogger(__name__)

# Export ANTHROPIC_API_KEY ke env var supaya `claude-agent-sdk` subprocess
# bisa baca saat dia spawn `claude` CLI. Pydantic-settings hanya populate
# settings object — TIDAK set env real. Tanpa ini, agen (anggota_tim/ketua_tim)
# gagal dgn "API Error: 401 Invalid authentication credentials" saat uvicorn
# dijalankan dari context yg env-nya tidak punya key (mis. Claude Code shell).
#
# Aturan: HORMATI env yg sudah ada (operator override). Hanya inject bila
# env kosong dan settings punya nilai. Idempoten untuk reload.
if settings.anthropic_api_key and not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
    log.info("ANTHROPIC_API_KEY di-export dari .env ke env proses (untuk SDK subprocess)")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Buat tabel saat startup (idempoten). Untuk migrasi lebih ketat pakai Alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Seed dummy TLHP bila tabel kosong (C5 — idempoten).
    try:
        from app.routes.tlhp import seed_tlhp_dummy
        async with SessionLocal() as db:
            n = await seed_tlhp_dummy(db)
            if n:
                log.info("Seed TLHP dummy: %s rekomendasi", n)
    except Exception:  # noqa: BLE001 — seed best-effort, jangan blokir startup
        log.exception("Seed TLHP dummy gagal (lanjut)")
    yield


app = FastAPI(
    title="Audit AI v7",
    version="0.1.0",
    description="Backend Audit AI v7 — Inspektorat II Komdigi",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(penugasan.router)
app.include_router(dokumen.router)
app.include_router(agen.router)
app.include_router(files.router)
app.include_router(feedback.router)
app.include_router(knowledge.router)
app.include_router(cacm.router)
app.include_router(skills.router)
app.include_router(dashboard.router)
app.include_router(tlhp.router)
app.include_router(lembar_reviu.router)
app.include_router(graduasi.router)


@app.get("/", tags=["meta"])
async def root():
    return {
        "name": "Audit AI v7",
        "version": "0.1.0",
        "env": settings.app_env,
        "docs": "/docs",
    }


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}
