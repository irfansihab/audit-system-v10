"""Agen Ketua Tim — Setup Penugasan + susun draft LHR dari temuan.json.

Agen punya 2 mode:
- Setup Penugasan: ekstrak sasaran dari PKP + assign ke anggota tim → tulis
  sasaran-assignment.json (sebelum AT mulai analisis)
- Susun LHR: setelah AT selesai, baca temuan, susun rekomendasi, render LHR,
  jalankan QC

Tools yang dipakai:
- read_pdf_page (dari pipeline_tools): KT baca PKP/ST untuk ekstrak sasaran
- list_ingested (dari kkp_tools): cek file _INGESTED/ yang sudah diproses
- LHR_TOOLS: write_sasaran_assignment + read/check/write/render/qc
- WIKI_TOOLS: list/get pattern temuan untuk format rekomendasi
- FEEDBACK_TOOLS: submit_feedback retrospective
"""
from claude_agent_sdk import ClaudeAgentOptions

from app.agents.base import build_agent_options
from app.tools.feedback_tools import FEEDBACK_TOOLS
from app.tools.kkp_tools import list_ingested, read_context, read_survey_pendahuluan
from app.tools.lhr_tools import LHR_TOOLS
from app.tools.pipeline_tools import read_pdf_page
from app.tools.skill_tools import SKILL_TOOLS
from app.tools.wiki_tools import WIKI_TOOLS


def build_ketua_tim_agent() -> ClaudeAgentOptions:
    # KT butuh akses ke beberapa tool dari grup lain untuk Setup mode:
    # - read_pdf_page → baca PKP/ST mentah saat ekstrak sasaran
    # - list_ingested → cek hasil ingestion sebelum extract
    # - read_context → baca context.md + sasaran-assignment yang ada
    # - SKILL_TOOLS → muat prosedur skill non-RKA/PBJ saat susun sasaran/LHP
    kt_extra = [read_pdf_page, list_ingested, read_context, read_survey_pendahuluan]
    return build_agent_options(
        prompt_name="ketua_tim",
        tools=LHR_TOOLS + kt_extra + WIKI_TOOLS + SKILL_TOOLS + FEEDBACK_TOOLS,
        server_name="kt",
        # model: default settings.agent_model (Sonnet) — override via env AGENT_MODEL.
    )
