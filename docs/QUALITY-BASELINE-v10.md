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
| audit-kinerja | draft-01 | **1.00** | 1.00 | 0.50‡ | 1.00 | 0.67 | **0.883** | ✅ terukur (1.9, 4 temuan, 8-aspek RCA) |
| pemantauan-tindak-lanjut | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.9, 5 temuan, matriks status TL) |
| pemantauan-pengadaan | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.9, 4 temuan) |
| evaluasi-spip | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.9, 4 AoI, LKE tanpa-Sebab) |
| evaluasi-sakip | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.9, 5 AoI) |
| evaluasi-reformasi-birokrasi | draft-01 | **1.00** | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** | ✅ terukur (1.9, 4 AoI) |
| reviu-rka-kl | pdn-031010 | **1.00** | 1.00 | — | 0.94 | 1.00 | **0.984** | ✅ terukur (1.9, 4 temuan, digest TOR/RAB) |

**Konsultansi — jalur skor PENDAPAT** (`judge_pendapat`: coverage poin + ketepatan + advisory_wajar; bukan recall-temuan):

| Skill | Golden | coverage | ketepatan | advisory_wajar | skor | Status |
|---|---|---|---|---|---|---|
| konsultansi-umum | draft-01 | 1.00 | 1.00 | ✅ | **1.00** | ✅ terukur (1.9, 4 poin) |
| konsultasi-pengadaan | draft-01 | 1.00 | 1.00 | ✅ | **1.00**◊ | ✅ terukur (1.11, 5 poin, re-skor pasca fix truncation) |

**16/16 terukur live** (per 6 Jul, harness `eval/live_measure.py`). Semua run: `build_fixtures.py` (digest/TOR-RAB sintetis ber-cacat; konsultansi = skenario pertanyaan advisory). ⚠ **Skor tinggi (banyak 1.00) sebagian ARTEFAK fixture sintetis "bersih"** — cacat ditanam unambiguous di digest → mudah ditangkap; dokumen nyata lebih berisik. Golden + fixture **WAJIB divalidasi auditor** sebelum jadi baseline resmi.

◊ konsultasi-pengadaan **KOREKSI (1.11)**: skor awal 0.40 ternyata **BUG HARNESS (truncation), BUKAN celah skill**. `judge_pendapat` memangkas pendapat ke 6.000 char, padahal pendapat agen **22.052 char** → poin di bagian akhir (P2 urutan pemaketan/spesifikasi/HPS, P4 self-review threat/batas peran APIP, P5 eskalasi audit) terpotong sebelum dinilai. **Re-skor dgn teks penuh (cap dinaikkan ke 40.000 char): coverage 1.00 · ketepatan 1.00 → SKOR 1.00** — kelima poin SEBENARNYA ada & tepat. Pelajaran: verifikasi root cause (baca teks penuh) sebelum menyimpulkan celah skill. Fix di `eval/judge.py`.

### Hardening 1.10 — presisi kutipan Kriteria skill AUDIT (tutup-loop, `5603469`)

Menindaklanjuti sinyal `kriteria` lemah di SEMUA skill audit. Fix (doktrin: anti-mengarang→KRITERIA) di audit-umum/-kinerja/-pengadaan: unsur Kriteria WAJIB kutip **regulasi+nomor+tahun+pasal/ayat/butir** dari matriks (bukan "prinsip umum"); DILARANG stretch pasal yang tak langsung mengatur; kondisi tanpa kriteria spesifik = indikasi kelemahan pengendalian (bukan deviasi terkonfirmasi). **Bukti re-ukur live:** audit-kinerja **4 RAGU→0** (semua VALID k2, `kriteria` 0.5→1.0); audit-umum SPP-SPM **k1→k2** (kutip SOP butir 7, tak lagi stretch prinsip), RAGU 3→2. Residu audit-umum = keterbatasan **fixture** (tarif SBM di-relay via digest SOP bukan salinan PMK; eselon narasumber tak dibuktikan) + **grounding bukti-negatif** (temuan "daftar hadir tak dilampirkan") — bukan celah sitasi skill. *Catatan metrik: composite `skor` audit-umum tetap ~0.83 krn recall di-cap artefak diksi golden (Q4/Q5) + variance antar-run; metrik yang relevan utk fix ini = `kriteria`/jumlah RAGU, dan itu membaik.*

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
- **Terukur judge: 16/16** (6 Jul, sesi harness). Semua doktrin tervalidasi live: audit (Sebab WAJIB/RCA + kerugian negara), reviu/evaluasi-nonLKE/pemantauan (Sebab anti-mengarang), **LKE** (spip/sakip/rb — AoI tanpa-Sebab via temuan.json; runner tanpa-render sehingga gate LKE-xlsx tak menghalangi identifikasi AoI), **konsultansi** (jalur `judge_pendapat`), **reviu-rka-kl** (digest TOR/RAB staged di `_KKP`). **Sinyal hardening lintas-skill:** presisi kutipan pasal `kriteria` LEMAH di SEMUA skill AUDIT (audit-pengadaan 0.50, audit-umum 0.50, audit-kinerja RAGU×4) → **prioritas hardening berikut: presisi sitasi pasal/kriteria skill audit.** ~~konsultasi-pengadaan coverage 0.40~~ → **DIKOREKSI ke 1.00** (bug truncation judge_pendapat, bukan celah skill — lihat ◊ di atas).
- **Catatan format golden:** skill ber-temuan (audit/reviu/evaluasi/pemantauan) pakai `expected_key_issues`; **evaluasi ber-LKE** (sakip/spip/rb) → expected = AoI/gap tanpa Sebab; **konsultasi** (×2) pakai `expected_pendapat` — **harness recall-vs-temuan tak berlaku**, perlu mode eval "ketepatan pendapat"; **pemantauan-tindak-lanjut** dinilai atas status-TL/aging, runner mungkin perlu adaptasi.
- Rencana perluasan (opt-in, berbiaya API + butuh fixture/dok input per skill):
  1. Draft golden stub 13 skill (dari checklist tiap SKILL) → validasi auditor.
  2. Baseline live per keluarga (fixture digest sintetis ber-cacat, pola pilot) → judge → isi registri.
  3. Jadikan Tingkat-1 (deterministik) gate wajib di tiap latihan skill; Tingkat-2 (judge) di milestone.

## Catatan
Baseline pilot reviu-pengadaan diukur pada skill engine-ready (identik v9→v10). Angka precision/unsur/kriteria/narasi = 1.00 menjadikannya **referensi mutu** keluarga reviu; grounded/recall perlu re-ukur dengan dokumen sumber nyata untuk angka non-artefak.
