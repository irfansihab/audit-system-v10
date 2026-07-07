"""Harness pengukuran LIVE kualitas skill — generate temuan via agen AT lalu skor.

Alur:
  1. Stage fixture sintetis ber-cacat (`eval/fixtures/<skill>/`) → folder penugasan
     di `data/penugasan/eval-<skill>-<ts>/` (context.md lengkap = tanpa DB/get_team_members).
  2. Jalankan agen Anggota Tim (build_anggota_tim_agent + ClaudeSDKClient) →
     hasil `_KKP/temuan.json`.
  3. Skor via `eval.run_eval.score_case` terhadap golden case (deterministik + judge).

Pakai (dari backend/):
    .venv/bin/python -m eval.live_measure --skill reviu-umum                 # full (judge)
    .venv/bin/python -m eval.live_measure --skill reviu-umum --no-judge      # gratis (deterministik)
    .venv/bin/python -m eval.live_measure --skill reviu-umum --stage-only     # stage saja, tak jalankan agen
    .venv/bin/python -m eval.live_measure --skill reviu-umum --keep           # jangan hapus folder hasil

Model agen: default settings.agent_model (Sonnet). Judge: EVAL_JUDGE_MODEL (default opus).
Fixture menetapkan: 00-input/ (stub sumber), _INGESTED/*.json (digest ber-cacat),
_PKP/sasaran-assignment.json (sasaran DISETUJUI_KT), context.md (lengkap).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, ".")

from app.config import get_settings  # noqa: E402

EVAL_DIR = Path(__file__).parent
FIXTURE_DIR = EVAL_DIR / "fixtures"
GOLDEN_DIR = EVAL_DIR / "golden"


def _golden_for_skill(skill: str) -> dict | None:
    for p in sorted(GOLDEN_DIR.glob("*.json")):
        c = json.loads(p.read_text())
        if c.get("skill") == skill:
            return c
    return None


def _golden_by_id(case_id: str) -> dict | None:
    for p in sorted(GOLDEN_DIR.glob("*.json")):
        c = json.loads(p.read_text())
        if c.get("case_id") == case_id:
            return c
    return None


# Skill digest-only PBJ/RKA: sumber fakta = read_digest (bukan read_ingested_digest);
# digest sudah di-stage di _KKP → JANGAN jalankan run_batch_*.
_DIGEST_PIPELINE = {"reviu-rka-kl", "reviu-pengadaan", "audit-pengadaan"}


def _pendapat_prompt(skill: str, folder: str, at_name: str) -> str:
    """Prompt konsultansi — hasilkan PENDAPAT advisory (bukan temuan)."""
    return (
        f"Penugasan kode=eval-{skill}, skill={skill}, folder={folder}\n"
        f"Pengguna: {at_name} (Anggota Tim)\n\n"
        "context.md SUDAH lengkap. Ini penugasan KONSULTANSI (advisory). Langkah: read_context → "
        "load_skill + read_skill_reference (pahami format pendapat & batas advisory) → read_ingested_digest "
        "(materi permintaan) → susun PENDAPAT untuk tiap pertanyaan dengan alur "
        "**Pertanyaan → Dasar Hukum (pasal/ayat spesifik) → Analisis → Pendapat**. "
        "Jaga sifat advisory: TIDAK mengikat, TIDAK memvonis pelanggaran, TIDAK menghitung kerugian negara, "
        "keputusan akhir pada pejabat berwenang; eskalasi ke audit bila ada indikasi pelanggaran material. "
        "JANGAN append_temuan, JANGAN render docx. "
        "TULIS PENDAPAT LENGKAP sebagai jawaban teks akhir (semua pertanyaan terjawab, dasar hukum eksplisit)."
    )


def _at_prompt(skill: str, folder: str, at_name: str) -> str:
    """Prompt AT — fokus produksi temuan, hemat giliran, tanpa render docx."""
    if skill in _DIGEST_PIPELINE:
        sumber = ("read_digest (SUMBER FAKTA UTAMA — digest RKA/PBJ SUDAH tersedia di _KKP; "
                  "JANGAN jalankan run_batch_*; untuk RKA: read_digest index lalu read_digest(ro=<id>))")
    else:
        sumber = ("read_ingested_digest (SUMBER FAKTA UTAMA; JANGAN buka PDF, digest sudah memuat ringkasan)")
    return (
        f"Penugasan kode=eval-{skill}, skill={skill}, folder={folder}\n"
        f"Pengguna: {at_name} (Anggota Tim)\n\n"
        "context.md SUDAH lengkap (jangan susun ulang). Tugas: analisis dokumen objek "
        "vs kriteria dan susun TEMUAN (KKP) untuk sasaran milikmu.\n"
        f"Langkah hemat: read_context → (bila skill lain) load_skill + read_skill_reference "
        f"untuk elemen K/K/S/A(/R) & gate → {sumber} → telusuri tiap elemen kriteria satu per satu → "
        "append_temuan untuk yang TIDAK sesuai (dokumen_sumber wajib: file persis dari "
        "read_context.input_files + halaman + kutipan dari ringkasan digest) → submit_feedback "
        "(WAJIB isi pkp_assessment). JANGAN render_kkp_docx. "
        "Patuhi doktrin skill: Sebab sesuai jenis (audit=WAJIB/RCA; reviu/evaluasi-nonLKE/pemantauan="
        "anti-mengarang, boleh 'tidak cukup data'; konsultansi=tanpa Sebab). "
        "Anti-mengarang: hanya temuan TERKONFIRMASI dari bukti; yang belum pasti → catatan, bukan temuan. "
        "Lapor ringkas: jumlah temuan + judulnya."
    )


async def _run_agent(folder_abs: str, skill: str, at_name: str, *, pendapat: bool = False) -> dict:
    from claude_agent_sdk import ClaudeSDKClient
    from app.agents.anggota_tim import build_anggota_tim_agent

    opts = build_anggota_tim_agent()
    tools: list[str] = []
    texts: list[str] = []
    prompt = _pendapat_prompt(skill, folder_abs, at_name) if pendapat else _at_prompt(skill, folder_abs, at_name)
    async with ClaudeSDKClient(options=opts) as c:
        await c.query(prompt)
        async for m in c.receive_response():
            for b in (getattr(m, "content", None) or []):
                t = type(b).__name__
                if t == "TextBlock":
                    texts.append(b.text)
                elif t == "ToolUseBlock":
                    nm = getattr(b, "name", "?")
                    tools.append(nm)
                    print("  →", nm, flush=True)
    full = "".join(texts)
    return {"tools": dict(Counter(tools)), "text_tail": full[-800:], "text_full": full}


def _score_pendapat(golden: dict, pendapat_text: str, folder: str, *, use_judge: bool) -> dict:
    """Skor konsultansi: coverage poin + ketepatan + advisory_wajar (judge_pendapat)."""
    expected = golden.get("expected_pendapat", [])
    result = {
        "case_id": golden["case_id"], "skill": golden.get("skill"), "folder": folder,
        "mode": "pendapat", "n_expected": len(expected), "pendapat_len": len(pendapat_text or ""),
    }
    if not (pendapat_text or "").strip():
        result["error"] = "pendapat kosong — agen tak menghasilkan teks."
        print(f"\n=== CASE {golden['case_id']} ({golden.get('skill')}) · mode=pendapat ===\n  ⚠ {result['error']}")
        return result
    if not use_judge:
        print(f"\n=== CASE {golden['case_id']} · mode=pendapat · {len(pendapat_text)} char (judge dilewati) ===")
        return result
    import anthropic
    from eval import judge
    try:
        out = judge.judge_pendapat(expected, pendapat_text)
    except anthropic.APIStatusError as e:
        result["judge_error"] = f"{type(e).__name__}: {getattr(e,'message',str(e))}"
        print(f"  ⚠ judge dilewati — {result['judge_error']}")
        return result
    poin = out.get("poin", [])
    n = len(expected) or 1
    covered = sum(1 for p in poin if p.get("tertangani"))
    tepat = sum(1 for p in poin if p.get("tertangani") and p.get("tepat"))
    coverage = round(covered / n, 3)
    ketepatan = round(tepat / n, 3)
    advisory = bool(out.get("advisory_wajar"))
    # skor: coverage & ketepatan setara; advisory_wajar = gerbang mutu (−0.1 bila gagal).
    skor = round(0.5 * coverage + 0.5 * ketepatan - (0.0 if advisory else 0.1), 3)
    result["judge"] = {"model": judge.JUDGE_MODEL, "poin": poin, "advisory_wajar": advisory,
                       "metrik": {"coverage": coverage, "ketepatan": ketepatan,
                                  "advisory_wajar": advisory, "skor_gabungan": max(skor, 0.0)}}
    print(f"\n=== CASE {golden['case_id']} ({golden.get('skill')}) · mode=pendapat · {len(expected)} poin ===")
    print(f"  Judge ({judge.JUDGE_MODEL}):")
    for p in poin:
        mark = "✓" if p.get("tertangani") else "✗"
        tp = "tepat" if p.get("tepat") else "kurang-tepat"
        print(f"    [{mark} {tp:12}] {p['expected_id']}: {p['alasan'][:70]}")
    print(f"  advisory_wajar={advisory}")
    print(f"  METRIK: coverage={coverage} · ketepatan={ketepatan} → SKOR={max(skor,0.0)}")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="slug skill (mis. reviu-umum)")
    ap.add_argument("--fixture", default=None, help="nama dir fixture (default = skill)")
    ap.add_argument("--case", default=None, help="case_id golden (default = pertama yg cocok skill)")
    ap.add_argument("--at-name", default="Sarah Auditor", help="nama AT (harus = assigned_to di fixture)")
    ap.add_argument("--no-judge", action="store_true", help="skor deterministik saja (tanpa API judge)")
    ap.add_argument("--stage-only", action="store_true", help="stage fixture saja, tak jalankan agen")
    ap.add_argument("--keep", action="store_true", help="jangan hapus folder hasil setelah skor")
    args = ap.parse_args()

    settings = get_settings()
    if settings.anthropic_api_key:
        os.environ["ANTHROPIC_API_KEY"] = str(settings.anthropic_api_key)
    if getattr(settings, "claude_code_oauth_token", None):
        os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = str(settings.claude_code_oauth_token)

    fixture = FIXTURE_DIR / (args.fixture or args.skill)
    if not fixture.is_dir():
        print(f"Fixture tidak ada: {fixture}", file=sys.stderr)
        return 1
    golden = _golden_by_id(args.case) if args.case else _golden_for_skill(args.skill)
    if not golden:
        print(f"Golden case ('{args.case or args.skill}') tak ditemukan.", file=sys.stderr)
        return 1

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_folder = f"eval-{args.fixture or args.skill}-{ts}"
    dest = settings.data_dir / "penugasan" / run_folder
    shutil.copytree(fixture, dest)
    print(f"Fixture di-stage → {dest}")

    if args.stage_only:
        print("(--stage-only) selesai; jalankan agen manual bila perlu.")
        return 0

    is_pendapat = bool(golden.get("expected_pendapat"))
    folder_abs = os.path.abspath(str(dest))
    mode = "KONSULTANSI/pendapat" if is_pendapat else "temuan"
    print(f"\n=== Jalankan agen AT ({settings.agent_model}) · skill={args.skill} · mode={mode} ===")
    run_info = asyncio.run(_run_agent(folder_abs, args.skill, args.at_name, pendapat=is_pendapat))
    print("\nTOOLS:", run_info["tools"])
    print("--- ekor teks AT ---\n" + run_info["text_tail"])

    if is_pendapat:
        r = _score_pendapat(golden, run_info["text_full"], run_folder, use_judge=not args.no_judge)
    else:
        # Skor pakai run_eval (folder relatif terhadap data_root).
        from eval import run_eval
        case = dict(golden)
        case["folder"] = run_folder
        case.pop("temuan_inline", None)
        r = run_eval.score_case(case, use_judge=not args.no_judge)
        run_eval.print_summary(r)

    out_dir = EVAL_DIR / "out"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"live-{args.skill}-{ts}.json"
    out.write_text(json.dumps({"run": run_info, "score": r}, ensure_ascii=False, indent=2))
    print(f"\n→ hasil: {out}")

    if not args.keep:
        shutil.rmtree(dest, ignore_errors=True)
        print(f"(folder hasil dihapus; --keep untuk menyimpan)")
    else:
        print(f"(folder hasil disimpan: {dest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
