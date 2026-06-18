"""App configuration via environment variables."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.llm_extract import DEFAULT_LLM_MODEL


class Settings(BaseSettings):
    """Konfigurasi sistem.

    Semua nilai di-load dari environment variables. Lihat ../../.env.example.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Abaikan environment variable yang KOSONG agar `.env`/default tetap menang.

        Footgun pydantic-settings: env var bernilai string kosong (mis. shell yang
        meng-`export ANTHROPIC_API_KEY=`) MENGALAHKAN nilai di `.env` — sehingga key
        nyata di `.env` diam-diam hilang. Di sini kita saring env kosong dari sumber
        environment; env var yang BERISI tetap menang (precedence normal terjaga).
        """

        def env_nonempty() -> dict:
            return {
                k: v
                for k, v in env_settings().items()
                if not (isinstance(v, str) and v.strip() == "")
            }

        return (init_settings, env_nonempty, dotenv_settings, file_secret_settings)

    # Anthropic
    anthropic_api_key: str = ""
    # Mode auth untuk agen AT/KT (lewat CLI claude / claude-agent-sdk):
    #   "api"          → pakai ANTHROPIC_API_KEY (tagih API). DEFAULT — wajib untuk PRODUKSI.
    #   "subscription" → JANGAN set API key; CLI pakai login langganan (Claude Max) atau
    #                    CLAUDE_CODE_OAUTH_TOKEN. HEMAT API saat TESTING LOKAL oleh dev.
    #   ⚠ Jangan pakai "subscription" untuk melayani banyak user (langgar ToS langganan).
    #   Catatan: eval-judge & digest LLM fallback TETAP pakai API key (SDK Anthropic langsung).
    agent_auth_mode: str = "api"
    # Token OAuth langganan (hasil `claude setup-token`) — opsional; dipakai bila
    # agent_auth_mode="subscription" dan login ~/.claude tak tersedia (mis. headless).
    claude_code_oauth_token: str = ""
    # Model agen AT/KT. Default Sonnet 4.6 (mutu). Saat TESTING hemat token, set
    # AGENT_MODEL=claude-haiku-4-5 di .env (≈10–15× lebih murah; cukup utk uji alur,
    # bukan uji mutu). Produksi → biarkan Sonnet.
    agent_model: str = "claude-sonnet-4-6"

    # Database
    database_url: str = "postgresql+asyncpg://audit:audit@localhost:5432/audit_v7"

    # App
    app_env: str = "development"
    # Log SETIAP query SQL (SQLAlchemy echo). Default OFF — hidupkan hanya saat
    # debug query; sebelumnya selalu ON di dev → spam log + overhead.
    debug_sql: bool = False
    app_secret_key: str = "dev-secret-please-change"
    app_data_dir: str = "/data"
    app_v6_path: str = "/v6"
    app_wiki_path: str = "/wiki"  # knowledge base auditor (pattern temuan, dll)
    # Folder skill pengawasan (SKILL.md + references) — registry skill v7.
    # Default mengikuti layout repo; di docker di-mount ke /skills.
    app_skills_path: str = "/skills"
    # Folder template laporan standar (LHP skeleton {{...}} per jenis pengawasan
    # di <path>/_skeleton-lhp/template-lhp-[skill].docx). Di docker di-mount ke /templates.
    app_templates_path: str = "/templates"
    # Vault pengetahuan penuh (Obsidian/Karpathy) — read-only referensi. Catatan
    # ada di <app_vault_path>/wiki/. Kosong = fitur baca vault non-aktif.
    app_vault_path: str = ""
    app_cors_origins: str = "http://localhost:3000"

    # CACM / EWS SIRUP (integrasi service agent tim) — C1b
    # Kosong = fitur live (webhook/pull) non-aktif; ingest offline tetap jalan.
    cacm_webhook_secret: str = ""   # verifikasi X-Agent-Signature (HMAC sha256) push agent
    cacm_agent_base_url: str = ""   # mis. http://10.0.0.5:3000 (untuk pull/trigger)
    cacm_agent_api_key: str = ""    # X-API-Key untuk REST agent
    # C2 — otomasi: dari sinyal LIVE (webhook/pull), otomatis buat usulan penugasan.
    # "off" | "merah" (default) | "merah_kuning". Anti-duplikat per satker+kode.
    cacm_auto_promote: str = "merah"
    # Auto-promote OPT-IN untuk CacmFinding v7-native (Fase 1 CACM commit-3, 8 Juni 2026).
    # Default OFF supaya cut-over aman bertahap. Saat dinyalakan, anti-duplikat
    # via _open_usulan_exists yang sudah dual-jalur (cek EWS + v7 untuk satker+kriteria
    # yg setara). Set "merah" atau "merah_kuning" setelah validasi diff EWS vs v7
    # menunjukkan konsistensi (≥90% match status).
    cacm_v7_auto_promote: str = "off"

    # --- Keamanan login (B4) ---------------------------------------------- #
    # Proteksi brute-force pada jalur username+password (in-memory, per-username):
    # bila gagal login `login_max_attempts` kali dalam `login_attempt_window_minutes`,
    # akun dikunci selama `login_lockout_minutes`. Ringan untuk ±80 user 1 proses.
    login_max_attempts: int = 5
    login_attempt_window_minutes: int = 15
    login_lockout_minutes: int = 15
    # Masa berlaku token sesi (JWT). Habis → frontend auto-redirect ke /login.
    session_expire_hours: int = 12
    # Panjang minimum password baru saat ganti password.
    password_min_length: int = 8

    # Token quota per user per jam (safety)
    rate_limit_runs_per_hour: int = 5
    # Batas run agen yang berjalan BERSAMAAN di seluruh sistem (G2 — skala ±80 user).
    # Tiap run = subprocess CLI + LLM + SSE (berat). Lonjakan tak boleh menumbangkan
    # server: bila penuh, request baru ditolak 429 (backpressure), bukan diterima paksa.
    max_concurrent_agent_runs: int = 6

    # Fallback ekstraksi LLM saat digest deterministik kehilangan field kunci.
    # ON default sejak 3 Jun 2026 (hybrid agresif) — KAK/HPS pengadaan banyak
    # non-standar; parser regex sering miss field penting (dasar_hukum,
    # ruang_lingkup, sumber_referensi_harga, dll). Tier-1 parser tetap jadi
    # primary (gratis, cepat, reproducible); Haiku hanya dipanggil per dokumen
    # bila field kunci di COVERAGE_KEYS hilang — selektif & hemat token (~$0.003/doc).
    # Set OFF eksplisit di .env bila ingin parser-only (mis. operasi tanpa internet).
    # Butuh ANTHROPIC_API_KEY. Asumsi: tidak ada dokumen scan (teks selalu terbaca).
    digest_llm_fallback: bool = True
    digest_llm_model: str = DEFAULT_LLM_MODEL

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.app_cors_origins.split(",") if o.strip()]

    @property
    def data_dir(self) -> Path:
        p = Path(self.app_data_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def v6_path(self) -> Path:
        return Path(self.app_v6_path)

    @property
    def wiki_path(self) -> Path:
        return Path(self.app_wiki_path)

    @property
    def skills_path(self) -> Path:
        return Path(self.app_skills_path)

    @property
    def templates_path(self) -> Path:
        return Path(self.app_templates_path)

    @property
    def vault_path(self) -> Path | None:
        """Path vault pengetahuan penuh, atau None bila tidak dikonfigurasi."""
        return Path(self.app_vault_path) if self.app_vault_path.strip() else None

    @property
    def is_dev(self) -> bool:
        return self.app_env == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
