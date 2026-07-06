# Roadmap v10 — Hardening · Penyelarasan Workflow · Simplifikasi

**Basis:** fork v9 (engine-ready 16/16). **Pivot:** AI = ENGINE; orkestrator+UI = INTEGRAL; FE/BE v10 = harness uji. **Sumber backlog teknis:** `docs/SKILL-AUDIT-BACKLOG-v9.md`.

**Prinsip kerja tiap fase:** harness tetap hijau · perubahan markdown/skill tanpa restart · yang menyentuh output → uji (eval harness + judge / E2E live) · commit + push per unit · doktrin (KKSAR/LKE) tak diubah tanpa alasan eksplisit.

> **Status keseluruhan (1 Jul 2026):** **Fase 1 pada dasarnya TUNTAS** (1.1–1.5 selesai; 1.6 kerangka + 16/16 golden + 2/16 terukur live + fix presisi kriteria SBM). **Fase 0 / 2 / 3 / 4 belum mulai.** Dua doktrin tervalidasi live: reviu (Sebab anti-mengarang, skor 0.825) & audit (Sebab WAJIB/RCA + kerugian negara, 0.796). Commit hardening: `dd451ed`, `356ee70`, `52e4ad0`, `88a94c9`, `8c97ad5`, `5e0f534`.

---

## Fase 0 — Tuntaskan pondasi engine (sisa P1) · *enabler*
Menutup lapis portabilitas agar hardening berpijak pada engine yang benar-benar buta-orkestrasi.
- **0.1 P1#8 — de-UI prompt agen** (`anggota_tim.md`/`ketua_tim.md`): ganti "tab Setup/via UI"/status `DISETUJUI_KT` → kontrak file/data. *Markdown, risiko rendah.*
- **0.2 P1c — lepas `render_kkp_docx` & `read_context` dari DB** → kontrak file `_KKP/hitl-overlay.json` (`{rejected_ids, edits}`) + hook backend materialisasi (hybrid: file → fallback DB) + **uji live** (edit temuan → render → konfirmasi terterap). *Satu-satunya sisa P1 sentuh backend; bisa ditunda bila ingin fokus hardening dulu.*
- **DoD:** tak ada skill/tool/prompt yang mengasumsikan UI/DB v9; harness E2E hijau.

## Fase 1 — Hardening skill (fokus #1)
Mutu & ketahanan output tiap skill.

- ✅ **1.1 Reference rusak/legacy** — 3 pointer opsional mati (`references/02-*` yang tak pernah ada, konten sudah inline) dibuang; jejak `audit-system-v4` tersisa hanya di meta-skill `graduasi` (P4).
- ✅ **1.2 Terminologi baku** — `CCSAA`→**KKSAR** (audit-kinerja/pengadaan); `3E`→**2E** (audit-kinerja, ekonomis di luar lingkup → eskalasi audit-pengadaan).
- ✅ **1.3 reviu-rka-kl rule→checklist** — sudah bersih pasca engine-ready (satu-satunya "rule" = pernyataan benar "tidak ada rule deterministik").
- ✅ **1.4 Versi/frontmatter konsisten** — `model:` **0 di seluruh skill** (dibuang dari 2 meta-skill terakhir); tak ada drift versi body.
- ✅ **1.5 kepatuhan-saipi Sebab** — QC SAIPI 2320 kini **jenis-aware**: spec SKILL + **enforcement `qc_saipi.py:check_LAK_005`** (dulu stale: hanya audit) → audit KRITIS · reviu/evaluasi-nonLKE/pemantauan PERINGATAN · LKE/konsultasi NOT_APPLICABLE.
- 🟢 **1.6 Uji kualitas terukur** — kerangka baseline + gate 2-tingkat + registri (`docs/QUALITY-BASELINE-v10.md`); **golden 16/16** (13 DRAFT dari checklist+`wiki/temuan-patterns`, ber-`pattern_ref`; perlu **validasi auditor**); **terukur judge 2/16 live** (reviu 0.825, audit 0.796); **1.6c** presisi kriteria SBM (Perpres 26 + PMK SBM TA) — tindak lanjut sinyal `kriteria=0.50`.
  - ✅ **1.7 Sweep hardening 14 skill "pengawasan lain"** (4 Jul, main `95525a0`) — audit read-only 4 keluarga (umum/LKE/kinerja/pemantauan+PBJ) thd rubrik H1–H7 + doktrin Sebab per-grup + anti-mengarang + reference integrity. **2 KRITIS** (reviu-umum padanan "Sebab=tidak ada" bertentangan dgn body anti-mengarang; pemantauan-tindak-lanjut tabel Referensi menunjuk folder+4 file yang tak ada) + **5 SEDANG** (PANDUAN kinerja masih 3E aktif; audit-umum anjur "berpotensi"; gate HITL "WAJIB Gate 1/2" di referensi shared; konsultasi README drift "Rekomendasi WAJIB"→assurance; evaluasi-sakip scripts README rujuk skrip pipeline mati + framing auto-execute) + RINGAN (label harness "Task 02b/03/04") — SEMUA diperbaiki. Verifikasi negatif: `format_laporan:kksa` dipertahankan (kunci profil render, bukan token terminologi); evaluasi-manajemen-risiko = non-LKE KKSAR (benar); kepatuhan-saipi/graduasi = P4→INTEGRAL (di luar lingkup). Body 14 skill pada dasarnya sudah baik pasca P1+Fase 1 — residu terpusat di file referensi/pendukung.
  - ✅ **1.8 Harness ukur-kualitas LIVE siap** (4 Jul, main `01b904d`) — `backend/eval/live_measure.py` (runner reusable: stage fixture → agen AT → `temuan.json` → skor `run_eval.score_case` deterministik+judge) + `eval/fixtures/build_fixtures.py` (pembangun fixture sintetis ber-cacat per skill; cacat ditanam di `ringkasan_teks` digest, cocok golden `expected_key_issues`). **Engine fix** ditemukan saat menyiapkan: `read_ingested_digest` buta thd digest generik (9 skill criteria-driven) → ditambah cabang surface `ringkasan_teks`. **Baseline live 8/16** (main `f40772f`): reviu-umum 1.00 · evaluasi-umum 1.00 · evaluasi-MR 1.00 · pemantauan-umum 0.969 · audit-umum 0.845 (+ reviu/audit-pengadaan). Semua doktrin ber-temuan tervalidasi. Fix harness: `judge_recall` retry-on-empty (flaky matches kosong → recall 0.0 palsu). Sinyal nyata: audit-umum kriteria=0.50 (presisi sitasi pasal audit — sama audit-pengadaan). *Catatan: skor tinggi sebagian artefak fixture sintetis bersih; golden+fixture WAJIB divalidasi auditor.* ✅ **1.9 Baseline live 16/16 TUNTAS** (main `e14fe04`): LKE (spip/sakip/rb=AoI via temuan.json) 1.00; konsultansi via jalur skor BARU `judge_pendapat` (konsultansi-umum 1.00, konsultasi-pengadaan 0.40◊); reviu-rka-kl (digest TOR/RAB) 0.984. **Sinyal hardening terkonfirmasi lintas-skill: presisi kutipan pasal LEMAH di SEMUA skill AUDIT** (audit-pengadaan/umum kriteria=0.50, audit-kinerja RAGU×4) → prioritas hardening berikut. konsultasi-pengadaan coverage 0.40 = poin advisory-governance kurang. ⚠ skor tinggi sebagian artefak fixture bersih; golden+fixture WAJIB validasi auditor.
  - *Sisa (opt-in, butuh API):* fixture + baseline live keluarga lain (kinerja/LKE/pemantauan/konsultansi via `build_fixtures.py`) · validasi auditor atas 13 golden + fixture · terus perbaiki presisi kutipan pasal audit.
- **DoD:** 0 reference rusak ✅ · terminologi seragam ✅ · baseline kualitas terekam (2/16 live, 16/16 golden) 🟢.

## Fase 2 — Penyelarasan workflow dengan Pedoman Pengawasan (fokus #2) · *ciri khas v10*
Selaraskan alur kerja engine ke Pedoman/Juknis Pengawasan — **SK ikut sistem**, bukan sebaliknya.

> **✅ SELESAI (3 Jul 2026, `docs/PENYELARASAN-PEDOMAN-v10.md`).** Material pedoman diwarisi dari v9 (`USULAN-REVISI-SK.md`: 36 SDP + 13 errata + matriks proporsionalitas) + Pedoman asli di vault. Re-validasi konformansi engine v10 (pasca hardening + merge v8.8 + P1): **engine SELARAS** — errata sisi-engine (#1 shell, #2 KKSAR, #4 audit-leak, #5 assurance per-jenis, #6 survei audit-only) **semua terpenuhi**; merge v8.8 malah memperkuat (laporan faithful per-jenis). Semua artefak SDP produksi ADA (P.05 survei kini terimplementasi, PL.08 KKP+gate LKE, M.01-03 kendali mutu, K.01 Daftar Temuan, Tahapan 8 TU). Errata sisa = ranah **draft SK** (birokrasi), bukan engine. **0 perubahan kode** — engine sudah selaras.
- **2.1 Petakan gap** — bandingkan tahapan/artefak engine (KP→PKP→KKP→LHP→Daftar Temuan) vs Pedoman Pengawasan. *Butuh dokumen pedoman dari auditor.*
- **2.2 Selaraskan tahapan produksi** — sampai **laporan disetujui** (garis finis); adopsi hanya elemen pedoman yang **menambah nilai**, buang yang administratif-murni (→ ranah TU/INTEGRAL).
- **2.3 Selaraskan format artefak & penomoran** dengan pedoman (kode surat, struktur KKP/LHP, Daftar Temuan & Rekomendasi).
- **2.4 Tegaskan batas produksi vs administrasi** (garis serah: ekspor LHP + Daftar Temuan; sisanya administrasi).
- **DoD:** matriks gap engine↔pedoman + tahapan/artefak selaras, tanpa mengorbankan mesin produksi.

## Fase 3 — Simplifikasi fitur (fokus #3)

> **Progres (3 Jul 2026):** ✅ **3.1+3.2** konsolidasi render LHR — buang tool `render_lhr_pbj` redundan (jalur reviu-pengadaan legacy via cross_check rule) → `render_report` jadi jalur tunggal semua skill KKSA (diverifikasi deterministik reviu+audit); `cross_check` tak lagi dirujuk app/ (deprecated, file v6 dibiarkan); fix hard-key `tanggal_exit_meeting`→`.get()`. Scan dead-tool: **0 dead** (46 tool, semua terpakai — `read_survey_pendahuluan` via kt_extra). 🟡 **3.3 P4 meta-skill → INTEGRAL** & **3.4 ramping audit-kinerja (545)** DITUNDA (struktural/substansi-berat, risiko > nilai; kepatuhan-saipi/graduasi sudah tersegregasi via `_HIDDEN_FROM_PICKER`/`_EXCLUDE_DIRS`).
- **3.1 Dead-code lanjutan** — `cross_check.py` (v6) tandai deprecated & pastikan tak diekspos; sisir tool/route tak terpakai.
- **3.2 Konsolidasi tool/format** — rapikan render/lhr/kkp tooling; format laporan jenis-aware satu sumber.
- **3.3 P4 meta-skill → INTEGRAL** — `kepatuhan-saipi` (QC SAIPI) & `graduasi-skill-spesifik` (pengembangan) keluar dari `knowledge/skills/` jadi tooling/reference portabel.
- **3.4 Ramping prompt & skill sisa** — turunkan yang masih gemuk (mis. audit-kinerja) ke references.
- **DoD:** engine lebih ramping & hemat token; tak ada meta-skill di jalur produksi substansi.

## Fase 4 — Validasi menyeluruh
- E2E live per keluarga skill (harness) + regression eval harness + rubrik divalidasi auditor.
- **DoD:** semua skill lulus baseline kualitas; harness E2E hijau end-to-end.

---

## Urutan disarankan
**Fase 0 (0.1 dulu, 0.2 opsional-tunda) → Fase 1 → Fase 2 (saat dokumen pedoman siap) → Fase 3 → Fase 4.** Fase 2 dapat mulai kapan saja setelah dokumen Pedoman Pengawasan tersedia (paralel dengan Fase 1). Prioritas cepat-berdampak: **1.1 reference rusak** & **1.2 terminologi** (langsung menaikkan mutu output), lalu **1.6 baseline kualitas** sebagai gate.
