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
| reviu-umum | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.8, live_measure, 4 temuan) |
| audit-umum | draft-01 | **1.00** | 1.00 | 0.50‡ | 1.00 | 0.60§ | **0.845** | ✅ terukur (1.8, 4 temuan) |
| evaluasi-umum | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.8, 4 temuan) |
| pemantauan-umum | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **0.969** | ✅ terukur (1.8, 4 temuan) |
| evaluasi-manajemen-risiko | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.8, 5 temuan) |
| reviu-rka-kl | ×2 | — | — | — | — | — | — | golden ada, belum di-judge (butuh digest TOR/RAB) |
| *(8 skill lain)* | — | — | — | — | — | — | — | LKE/konsultansi/PBJ-lain — perlu fixture/jalur skor |

**8/16 terukur live** (per 6 Jul, harness `eval/live_measure.py`). Semua run: metode `build_fixtures.py` (digest sintetis ber-cacat). ⚠ **Skor tinggi (banyak 1.00) sebagian ARTEFAK fixture sintetis "bersih"** — cacat ditanam unambiguous di digest → mudah ditangkap; dokumen nyata lebih berisik. Golden + fixture **WAJIB divalidasi auditor** sebelum jadi baseline resmi.

\* recall 0.5 & grounded pilot reviu = **artefak harness sintetis** (digest tanpa PDF primer; 1 dari 2 expected issue tak diberi data). Sinyal murni skill: precision/unsur/kriteria/narasi = 1.00.
‡ audit-umum `kriteria`=0.50: 3 temuan RAGU krn kutipan kriteria kurang presisi (SBM/SOP dikutip generik, bukan pasal spesifik) + 1 grounding lemah (temuan "ketiadaan dokumen" sulit dibuktikan langsung). **Menegaskan sinyal hardening yang sama dgn audit-pengadaan: presisi kutipan pasal/kriteria skill AUDIT.**
§ audit-umum recall 0.60 = **artefak phrasing golden**, bukan gagal agen: Q4 (dekomposisi per-elemen) = ekspektasi metodologi, bukan "temuan" terpisah; Q5 diksi golden mendeskripsikan ANTI-pola ("kerugian negara NAMUN Sebab tak digali") padahal agen JUSTRU menghitung kerugian + gali Sebab RCA → tak "cocok". Golden audit-umum perlu revisi auditor.
\*\* audit-pengadaan: 6/6 cacat tertangkap (metode PL>ambang, HPS 1-sumber, SBM TA≠DIPA, tanpa jaminan, BAST palsu 100%, **kelebihan bayar→kerugian negara**), semua **Sebab RCA nyata** (doktrin audit ✓). recall 0.67 = AE3 (denda) tak ditanam di fixture. **Sinyal hardening asli:** `kriteria` = 0.50 (1 temuan `TIDAK_VALID` krn kutipan pasal SBM lemah; 4 RAGU krn judge menuntut presisi pasal lebih tinggi utk audit) → **target hardening: presisi kutipan kriteria/pasal skill audit.** Agen memakai `list_temuan_patterns` (wiki) & mengusulkan pola baru AP-30/AP-31.

## Cara menambah baseline sebuah skill
1. Buat `eval/golden/case-<skill>.json`: `{case_id, skill, folder, expected_key_issues:[{id,ringkas,kriteria_acuan,materialitas}], _catatan_validasi}` — **`expected_key_issues` WAJIB divalidasi auditor senior** (lihat DRAFT ews01).
2. Jalankan agen pada penugasan/fixture → hasilkan `temuan.json`.
3. `run_eval --case <id>` (judge) → catat skor di tabel atas.
4. Skor jadi **baseline**; run berikut yang turun signifikan = regresi.

## Cakupan & rencana
- **Golden case: 16/16** — 3 tervalidasi-awal (audit/reviu-pengadaan, reviu-rka-kl) + **13 DRAFT** (Fase 1.6, diturunkan dari checklist SKILL + pola `knowledge/wiki/temuan-patterns/<skill>/`; tiap expected ber-`pattern_ref`). **Semua 13 DRAFT WAJIB divalidasi auditor senior** sebelum jadi baseline.
- **Terukur judge: 8/16** (reviu/audit-pengadaan + reviu/audit/evaluasi/pemantauan-umum + evaluasi-manajemen-risiko) — semua doktrin ber-temuan tervalidasi live: reviu & evaluasi-nonLKE & pemantauan (Sebab anti-mengarang), audit (Sebab WAJIB/RCA + kerugian negara). **Sisa 8:** 3 LKE (spip/rb/sakip — perlu jalur skor AoI/LKE-xlsx), 2 konsultansi (perlu mode "ketepatan pendapat"), reviu-rka-kl + 2 PBJ-lain (perlu fixture digest TOR/RAB/pengadaan). Tambah fixture ber-temuan = 1 skenario di `eval/fixtures/build_fixtures.py` (mekanis).
- **Catatan format golden:** skill ber-temuan (audit/reviu/evaluasi/pemantauan) pakai `expected_key_issues`; **evaluasi ber-LKE** (sakip/spip/rb) → expected = AoI/gap tanpa Sebab; **konsultasi** (×2) pakai `expected_pendapat` — **harness recall-vs-temuan tak berlaku**, perlu mode eval "ketepatan pendapat"; **pemantauan-tindak-lanjut** dinilai atas status-TL/aging, runner mungkin perlu adaptasi.
- Rencana perluasan (opt-in, berbiaya API + butuh fixture/dok input per skill):
  1. Draft golden stub 13 skill (dari checklist tiap SKILL) → validasi auditor.
  2. Baseline live per keluarga (fixture digest sintetis ber-cacat, pola pilot) → judge → isi registri.
  3. Jadikan Tingkat-1 (deterministik) gate wajib di tiap latihan skill; Tingkat-2 (judge) di milestone.

## Catatan
Baseline pilot reviu-pengadaan diukur pada skill engine-ready (identik v9→v10). Angka precision/unsur/kriteria/narasi = 1.00 menjadikannya **referensi mutu** keluarga reviu; grounded/recall perlu re-ukur dengan dokumen sumber nyata untuk angka non-artefak.
