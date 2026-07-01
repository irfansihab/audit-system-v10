# Baseline Kualitas Output Skill — v10 (Fase 1.6)

Tujuan: kualitas output tiap skill **terukur** & **ter-gate regresi**. Basis rubrik: `backend/eval/RUBRIC.md`. Runner: `backend/eval/run_eval.py`.

## Dua-tingkat gate

**Tingkat 1 — Deterministik (tanpa API, murah, jalankan tiap skill dilatih):**
`.venv/bin/python -m eval.run_eval --case <id> --no-judge`
- `unsur_lengkap` (jenis-aware: audit K/K/S/A; reviu/evaluasi/pemantauan K/K/A + Sebab anti-mengarang; LKE tanpa-Sebab)
- `grounding_presence` (dokumen_sumber ada)
- `qc_saipi` (gate SAIPI, termasuk **cek Sebab jenis-aware** hasil Fase 1.5)
- Lolos = tak ada unsur wajib kosong + QC tanpa gap KRITIS.

**Tingkat 2 — Judge LLM (API, on-demand, untuk baseline & regresi bermakna):**
`.venv/bin/python -m eval.run_eval --case <id>` (set `EVAL_JUDGE_MODEL=claude-sonnet-4-6`)
- Metrik: `tidak_ngawur` (precision, target ≥0.85), `recall` (vs `expected_key_issues`, target ≥0.80), `narasi_agregat`, `skor_gabungan` (0.40·precision + 0.35·recall + 0.25·narasi).

## Registri baseline (per skill)

| Skill | Golden case | precision | unsur | kriteria | narasi | recall | skor | Status |
|---|---|---|---|---|---|---|---|---|
| reviu-pengadaan | ews01 | **1.00** | 1.00 | 1.00 | 1.00 | 0.50\* | 0.825 | ✅ terukur (pilot P1a) |
| audit-pengadaan | audit-synthetic | **0.83** | 0.92 | 0.50 | 0.92 | 0.67\*\* | 0.796 | ✅ terukur (v10 Fase1.6, 6 temuan) |
| reviu-rka-kl | ×2 | — | — | — | — | — | — | golden ada, belum di-judge |
| *(13 skill lain)* | — | — | — | — | — | — | — | **belum ada golden** |

\* recall 0.5 & grounded pilot reviu = **artefak harness sintetis** (digest tanpa PDF primer; 1 dari 2 expected issue tak diberi data). Sinyal murni skill: precision/unsur/kriteria/narasi = 1.00.
\*\* audit-pengadaan: 6/6 cacat tertangkap (metode PL>ambang, HPS 1-sumber, SBM TA≠DIPA, tanpa jaminan, BAST palsu 100%, **kelebihan bayar→kerugian negara**), semua **Sebab RCA nyata** (doktrin audit ✓). recall 0.67 = AE3 (denda) tak ditanam di fixture. **Sinyal hardening asli:** `kriteria` = 0.50 (1 temuan `TIDAK_VALID` krn kutipan pasal SBM lemah; 4 RAGU krn judge menuntut presisi pasal lebih tinggi utk audit) → **target hardening: presisi kutipan kriteria/pasal skill audit.** Agen memakai `list_temuan_patterns` (wiki) & mengusulkan pola baru AP-30/AP-31.

## Cara menambah baseline sebuah skill
1. Buat `eval/golden/case-<skill>.json`: `{case_id, skill, folder, expected_key_issues:[{id,ringkas,kriteria_acuan,materialitas}], _catatan_validasi}` — **`expected_key_issues` WAJIB divalidasi auditor senior** (lihat DRAFT ews01).
2. Jalankan agen pada penugasan/fixture → hasilkan `temuan.json`.
3. `run_eval --case <id>` (judge) → catat skor di tabel atas.
4. Skor jadi **baseline**; run berikut yang turun signifikan = regresi.

## Cakupan & rencana
- **Golden case: 3/16** (audit-pengadaan, reviu-pengadaan, reviu-rka-kl). **Gap: 13 skill.**
- **Terukur judge: 2/16** (reviu-pengadaan, audit-pengadaan) — dua doktrin tervalidasi live: reviu (Sebab anti-mengarang) & audit (Sebab WAJIB/RCA + kerugian negara).
- Rencana perluasan (opt-in, berbiaya API + butuh fixture/dok input per skill):
  1. Draft golden stub 13 skill (dari checklist tiap SKILL) → validasi auditor.
  2. Baseline live per keluarga (fixture digest sintetis ber-cacat, pola pilot) → judge → isi registri.
  3. Jadikan Tingkat-1 (deterministik) gate wajib di tiap latihan skill; Tingkat-2 (judge) di milestone.

## Catatan
Baseline pilot reviu-pengadaan diukur pada skill engine-ready (identik v9→v10). Angka precision/unsur/kriteria/narasi = 1.00 menjadikannya **referensi mutu** keluarga reviu; grounded/recall perlu re-ukur dengan dokumen sumber nyata untuk angka non-artefak.
