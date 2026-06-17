"""Agen Claude untuk INTEGRAL (engine Audit AI).

Dua agen ber-LLM (hardened): Anggota Tim (susun KKP) + Ketua Tim (susun LHR).
Ingestion = worker DETERMINISTIK (routes/agen._run_ingestion), bukan agen.
QC SAIPI = tool SINKRON (run_qc_kkp/run_qc_lhp), bukan agen.
"""
from app.agents.anggota_tim import build_anggota_tim_agent
from app.agents.ketua_tim import build_ketua_tim_agent

__all__ = [
    "build_anggota_tim_agent",
    "build_ketua_tim_agent",
]
