"""LLM-judge untuk eval kualitas temuan agen.

Memakai Anthropic SDK langsung (bukan claude_agent_sdk) dengan forced tool-use
agar output terstruktur & valid — kompatibel dengan anthropic==0.42.0 yang belum
punya messages.parse()/output_config.

Model judge bisa diatur via env EVAL_JUDGE_MODEL (default claude-opus-4-8 — judge
butuh akurasi tinggi, frekuensi rendah jadi biaya tak jadi soal). Bila API key
belum punya akses Opus, set EVAL_JUDGE_MODEL=claude-sonnet-4-6.
"""
from __future__ import annotations

import json
import os
from typing import Any

import anthropic

from app.config import get_settings

JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "claude-opus-4-8")

_settings = get_settings()
_client = anthropic.Anthropic(api_key=_settings.anthropic_api_key)


def _call_tool(system: str, user: str, tool_name: str, schema: dict, max_tokens: int = 4096) -> dict[str, Any]:
    """Panggil model dengan tool_choice terkunci → kembalikan input tool (dict)."""
    resp = _client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=max_tokens,
        system=system,
        tools=[{"name": tool_name, "description": "Rekam hasil penilaian.", "input_schema": schema}],
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user}],
    )
    for block in resp.content:
        if getattr(block, "type", None) == "tool_use":
            return dict(block.input)
    raise RuntimeError("Judge tidak mengembalikan tool_use block")


# ---------------------------------------------------------------------------
# A. Skor per-temuan (precision + narasi)
# ---------------------------------------------------------------------------

_PER_TEMUAN_SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "indeks temuan (mulai 0) sesuai urutan input"},
                    "grounded": {"type": "integer", "enum": [0, 1, 2]},
                    "kriteria_tepat": {"type": "integer", "enum": [0, 1, 2]},
                    "unsur_lengkap": {"type": "integer", "enum": [0, 1, 2]},
                    "narasi": {"type": "integer", "enum": [0, 1, 2]},
                    "alasan": {"type": "string", "description": "1-2 kalimat, bahasa Indonesia"},
                },
                "required": ["index", "grounded", "kriteria_tepat", "unsur_lengkap", "narasi", "alasan"],
            },
        }
    },
    "required": ["scores"],
}

def _per_temuan_system(is_audit: bool, kriteria_context: str = "") -> str:
    if is_audit:
        unsur_rule = ("- unsur_lengkap: kondisi/kriteria/SEBAB/akibat semua terisi substantif "
                      "(penugasan AUDIT wajib menggali sebab/akar penyebab).")
    else:
        unsur_rule = ("- unsur_lengkap: kondisi/kriteria/akibat terisi substantif. "
                      "PENTING: ini penugasan REVIU/EVALUASI/PEMANTAUAN — TIDAK menggali penyebab; "
                      "'sebab' yang kosong itu BENAR dan TIDAK boleh menurunkan skor.")
    if kriteria_context:
        # Judge tanpa akses teks regulasi cenderung meng-cap sitasi sub-pasal
        # granular ke 1 ("tidak dapat diverifikasi"). Suplai ringkasan kriteria
        # yang BERLAKU agar sitasi bisa diverifikasi, bukan diragukan buta.
        kriteria_rule = (
            "- kriteria_tepat: VERIFIKASI sitasi terhadap REFERENSI KRITERIA di bawah. "
            "Pasal/nomor yang dikutip agen COCOK & KONSISTEN dengan referensi → 2 "
            "(JANGAN turunkan hanya karena sitasi spesifik/granular — presisi itu benar). "
            "Regulasi/pasal TIDAK ada di referensi & tak dapat dipastikan → maksimal 1. "
            "BERTENTANGAN dgn referensi / salah nomor / salah subjek pasal → 0. "
            "Jangan lagi menilai 'tidak dapat diverifikasi' untuk pasal yang ADA di referensi ini.")
        ref_block = f"\n\n=== REFERENSI KRITERIA (regulasi berlaku — untuk verifikasi sitasi) ===\n{kriteria_context}\n=== akhir referensi ===\n"
    else:
        kriteria_rule = "- kriteria_tepat: regulasi yang dikutip nyata, pasal benar, relevan dengan kondisi. Regulasi karangan/salah → 0."
        ref_block = ""
    return f"""Anda auditor senior APIP Inspektorat yang menilai mutu temuan hasil pengawasan (Kertas Kerja Pengawasan).
Nilai SETIAP temuan secara adversarial — default skeptis. Pakai rubrik (skor 0/1/2 per aspek):
- grounded: dokumen_sumber ada (file+halaman+kutipan) DAN kutipan benar-benar mendukung 'kondisi' (angka cocok). Bila tak ber-bukti → 0.
{kriteria_rule}
{unsur_rule}
- narasi: bahasa jelas, formal, angka konsisten, tidak ambigu.
PENTING: JANGAN menilai rekomendasi — di tahap KKP temuan TIDAK memuat rekomendasi (itu ranah LHR/Ketua Tim).
Nilai hanya 4 aspek di atas (grounded/kriteria_tepat/unsur_lengkap/narasi). Verdict dihitung otomatis dari skor, jangan kirim verdict.
Jangan menilai murah hati — tujuan menemukan temuan ngawur, bukan meloloskannya.{ref_block}"""


def judge_per_temuan(temuan_list: list[dict], is_audit: bool = False, kriteria_context: str = "") -> list[dict]:
    """Skor tiap temuan. Kembalikan list dict skor (urut sesuai input).

    kriteria_context: ringkasan regulasi yang berlaku (references skill + wiki
    regulasi-kunci) agar judge dapat MEMVERIFIKASI sitasi pasal alih-alih
    menandainya 'tidak dapat diverifikasi'. Kosong = perilaku lama (skeptis buta).
    """
    payload = []
    for t in temuan_list:
        payload.append({
            "judul": t.get("judul_temuan"),
            "kondisi": t.get("kondisi"),
            "kriteria": t.get("kriteria"),
            "sebab": t.get("sebab"),
            "akibat": t.get("akibat"),
            "dokumen_sumber": t.get("dokumen_sumber", []),
        })
    user = ("Nilai temuan berikut (JSON array; index dimulai 0). "
            "Kembalikan satu objek skor per temuan via tool.\n\n"
            + json.dumps(payload, ensure_ascii=False, indent=2))
    out = _call_tool(_per_temuan_system(is_audit, kriteria_context), user, "rekam_skor_temuan", _PER_TEMUAN_SCHEMA,
                     max_tokens=400 + 220 * len(payload))
    scores = out.get("scores", [])
    scores.sort(key=lambda s: s.get("index", 0))
    return scores


# ---------------------------------------------------------------------------
# B. Recall vs reference
# ---------------------------------------------------------------------------

_RECALL_SCHEMA = {
    "type": "object",
    "properties": {
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "expected_id": {"type": "string"},
                    "tertangani": {"type": "boolean"},
                    "matched_temuan_index": {"type": "integer", "description": "indeks temuan yang menutup isu ini; -1 bila tidak ada"},
                    "alasan": {"type": "string"},
                },
                "required": ["expected_id", "tertangani", "matched_temuan_index", "alasan"],
            },
        }
    },
    "required": ["matches"],
}

_RECALL_SYSTEM = """Anda auditor senior APIP. Anda diberi (1) daftar isu yang SEHARUSNYA ditemukan
(expected_key_issues, hasil validasi auditor) dan (2) daftar temuan yang BENAR diproduksi agen.
Untuk tiap expected issue, tentukan apakah ada temuan yang secara substansi menutupinya (boleh beda
kata, yang penting inti masalah & kriterianya sama). Jangan longgar: kecocokan dangkal/topik beda = tidak tertangani."""


def judge_recall(expected_issues: list[dict], temuan_list: list[dict]) -> list[dict]:
    # Payload ramping: hanya id + ringkas yang diperlukan untuk pencocokan
    # (materialitas/kriteria_acuan/pattern_ref tak relevan & membebani prompt).
    exp = [{"id": e.get("id"), "ringkas": e.get("ringkas")} for e in expected_issues]
    produced = [{"index": i, "judul": t.get("judul_temuan"), "kondisi": (t.get("kondisi") or "")[:400]}
                for i, t in enumerate(temuan_list)]
    user = ("EXPECTED_KEY_ISSUES:\n" + json.dumps(exp, ensure_ascii=False, indent=2)
            + "\n\nTEMUAN_DIPRODUKSI:\n" + json.dumps(produced, ensure_ascii=False, indent=2)
            + "\n\nCocokkan tiap expected issue. Kembalikan SATU objek match per expected issue via tool.")
    # Judge Opus sesekali mengembalikan matches KOSONG (flaky tool-call) → skor recall
    # jadi 0.0 palsu. Retry hingga 2x bila kosong padahal ada expected & temuan.
    matches: list[dict] = []
    for _ in range(3):
        out = _call_tool(_RECALL_SYSTEM, user, "rekam_recall", _RECALL_SCHEMA,
                         max_tokens=500 + 180 * len(exp))
        matches = out.get("matches", [])
        if matches or not (exp and produced):
            break
    return matches


# ---------------------------------------------------------------------------
# C. Ketepatan PENDAPAT (skill konsultansi — advisory, bukan temuan)
# ---------------------------------------------------------------------------

_PENDAPAT_SCHEMA = {
    "type": "object",
    "properties": {
        "poin": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "expected_id": {"type": "string"},
                    "tertangani": {"type": "boolean", "description": "pendapat mencakup substansi poin ini"},
                    "tepat": {"type": "boolean", "description": "arah saran & dasar hukum benar, tidak menyesatkan"},
                    "alasan": {"type": "string"},
                },
                "required": ["expected_id", "tertangani", "tepat", "alasan"],
            },
        },
        "advisory_wajar": {"type": "boolean",
                           "description": "pendapat bersifat advisory/tidak mengikat, tidak menyimpulkan pelanggaran, tidak mengarang kewajiban"},
        "catatan": {"type": "string"},
    },
    "required": ["poin", "advisory_wajar"],
}

_PENDAPAT_SYSTEM = """Anda auditor senior APIP yang menilai mutu PENDAPAT KONSULTANSI (advisory pra-pelaksanaan).
Konsultansi = memberi pendapat/saran (Pertanyaan → Dasar Hukum → Analisis → Pendapat), TIDAK menyimpulkan
pelanggaran, TIDAK menghitung kerugian negara, TIDAK mengikat (keputusan tetap di pejabat berwenang).
Anda diberi (1) daftar POIN pendapat yang SEHARUSNYA disampaikan (expected, hasil validasi auditor) dan
(2) PENDAPAT yang diproduksi agen. Untuk tiap expected poin nilai: tertangani (substansi poin tercakup?) &
tepat (arah saran + dasar hukum/pasal benar & tidak menyesatkan?). Jangan longgar: kecocokan dangkal/arah
saran salah = tidak tertangani/tidak tepat. Nilai juga advisory_wajar: apakah pendapat menjaga sifat
advisory (tidak mengikat, tidak memvonis pelanggaran, tidak mengarang kewajiban regulasi)."""


def judge_pendapat(expected_pendapat: list[dict], pendapat_text: str) -> dict:
    exp = [{"id": e.get("id"), "poin": e.get("poin"), "dasar_hukum": e.get("dasar_hukum")}
           for e in expected_pendapat]
    # Pendapat advisory bisa panjang (memo 5+ pertanyaan → puluhan ribu char).
    # Cap tinggi agar poin di bagian akhir tak "terpotong" (bug: cap 6K dulu memangkas
    # jawaban → poin dinilai 'tidak tertangani' padahal ADA). Opus input muat besar.
    user = ("EXPECTED_POIN_PENDAPAT:\n" + json.dumps(exp, ensure_ascii=False, indent=2)
            + "\n\nPENDAPAT_DIPRODUKSI:\n" + (pendapat_text or "(kosong)")[:40000]
            + "\n\nNilai tiap poin + advisory_wajar via tool.")
    out: dict = {"poin": [], "advisory_wajar": False}
    for _ in range(3):
        out = _call_tool(_PENDAPAT_SYSTEM, user, "rekam_pendapat", _PENDAPAT_SCHEMA,
                         max_tokens=500 + 180 * len(exp))
        if out.get("poin") or not exp:
            break
    return out
