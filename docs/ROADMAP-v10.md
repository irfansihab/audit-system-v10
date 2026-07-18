# Roadmap v10 — Hardening · Penyelarasan Workflow · Simplifikasi

**Basis:** fork v9 (engine-ready 16/16). **Pivot:** AI = ENGINE; orkestrator+UI = INTEGRAL; FE/BE v10 = harness uji. **Sumber backlog teknis:** `docs/SKILL-AUDIT-BACKLOG-v9.md`.

**Prinsip kerja tiap fase:** harness tetap hijau · perubahan markdown/skill tanpa restart · yang menyentuh output → uji (eval harness + judge / E2E live) · commit + push per unit · doktrin (KKSAR/LKE) tak diubah tanpa alasan eksplisit.

> **Status keseluruhan (18 Jul 2026, malam) — v10 FINAL di PR #1 (17 commit), siap UAT skill riil.** Fase 0–6 ✅ · Sprint akhir: **CACM multi-dimensi** (ANGGARAN+KINERJA, ingest multi-sumber, kelola kriteria UI PT-only, usulan kriteria dari wiki) · **Knowledge 5 submenu terkelola** (Pattern · Template KP/PKP [20 skill] · Kriteria Pengawasan [upload regulasi→wiki→preload agen] · Kelola Skill [baca/buat/edit + graduasi] · Tulis-balik) · **BUKTI-LAPANGAN** (AT upload hasil pemeriksaan fisik/observasi/diskusi ahli → digest semua skill → doktrin wajib-analisis 3 titik) · **Audit sistem menyeluruh 4-agen**: ±44 temuan, **36 diperbaiki terverifikasi** (data-loss render KKP ter-filter, QC PASS palsu, path traversal, role-gate, TOCTOU, fairness harness, HITL setujui/tolak temuan yang tak pernah punya UI, pool DB ingest 3-fase, error-senyap FE) · **Regulasi dasar PBJ TERVERIFIKASI dari teks asli 5 PDF** (Perpres 16/2018·12/2021·46/2025 + Perlem 12/2021·4/2024): salah-sitasi dikoreksi (PL=38(3), konsultansi=41(3), split=20(2)d, PjL=38/41(4)-(5)), temuan baru **PL konstruksi ≤Rp400jt & kriteria PjL diperluas (46/2025)**, konflik Perlem 4/2024 terpecah (=lampiran D&B), RUP 31 Maret=Perlem 11/2021 Ps 8(2) (konfirmasi auditor). **Berikutnya: Fase 7 UAT auditor.** **v11: integrasi ev-SAKIP/e-Ziko/SPIP via jalur ingest multi-sumber CACM.**
>
> Status per 7 Jul (histori): **Fase 0 ✅ · Fase 1 ✅ · Fase 2 ✅ · Fase 3 ✅ (inti) · Fase 4 🟢 (16/16 terukur live).** Merge v8.8 ✅. **Baseline live 16/16 skill = semua doktrin tervalidasi** (audit RCA+kerugian, reviu/evaluasi-nonLKE/pemantauan Sebab anti-mengarang, LKE AoI, konsultansi pendapat, RKA/PBJ digest). **Hardening lanjutan (1.7–1.15)** + **doktrin lintas-skill baku** (sasaran-first scoping · kriteria tambahan · presisi Kriteria · SAIPI) + **fix** (ST=metadata INTEGRAL, istilah LKE, RB masuk rezim LKE). **Perluasan: 3 skill BARU reviu keuangan** (LK/PIPK/PNBP) — rumah+checklist+teruji live (lihat Fase 5). Metode bikin/uji skill sudah E2E terbukti (`build_fixtures.py`+`live_measure.py`). **Forward: Fase 6 (Integrasi Wiki) + Fase 7 (User Test / UAT auditor)** = jalur dari "terukur via judge" → "**tervalidasi manusia & siap produksi**".

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
  - ✅ **1.8 Harness ukur-kualitas LIVE siap** (4 Jul, main `01b904d`) — `backend/eval/live_measure.py` (runner reusable: stage fixture → agen AT → `temuan.json` → skor `run_eval.score_case` deterministik+judge) + `eval/fixtures/build_fixtures.py` (pembangun fixture sintetis ber-cacat per skill; cacat ditanam di `ringkasan_teks` digest, cocok golden `expected_key_issues`). **Engine fix** ditemukan saat menyiapkan: `read_ingested_digest` buta thd digest generik (9 skill criteria-driven) → ditambah cabang surface `ringkasan_teks`. **Baseline live 8/16** (main `f40772f`): reviu-umum 1.00 · evaluasi-umum 1.00 · evaluasi-MR 1.00 · pemantauan-umum 0.969 · audit-umum 0.845 (+ reviu/audit-pengadaan). Semua doktrin ber-temuan tervalidasi. Fix harness: `judge_recall` retry-on-empty (flaky matches kosong → recall 0.0 palsu). Sinyal nyata: audit-umum kriteria=0.50 (presisi sitasi pasal audit — sama audit-pengadaan). *Catatan: skor tinggi sebagian artefak fixture sintetis bersih; golden+fixture WAJIB divalidasi auditor.* ✅ **1.9 Baseline live 16/16 TUNTAS** (main `e14fe04`): LKE (spip/sakip/rb=AoI via temuan.json) 1.00; konsultansi via jalur skor BARU `judge_pendapat` (konsultansi-umum 1.00, konsultasi-pengadaan 0.40◊); reviu-rka-kl (digest TOR/RAB) 0.984. **Sinyal hardening terkonfirmasi lintas-skill: presisi kutipan pasal LEMAH di SEMUA skill AUDIT** (audit-pengadaan/umum kriteria=0.50, audit-kinerja RAGU×4) → prioritas hardening berikut. konsultasi-pengadaan 0.40◊ **DIKOREKSI ke 1.00** (1.11: bug truncation `judge_pendapat` cap 6K vs pendapat 22K — poin akhir terpotong; fix cap→40K, re-skor coverage/ketepatan 1.00). ⚠ skor tinggi sebagian artefak fixture bersih; golden+fixture WAJIB validasi auditor.
  - ✅ **1.10–1.15 Hardening & doktrin lintas-skill (7 Jul)** — **1.10** presisi kutipan **KRITERIA** skill audit (anti-mengarang→Kriteria di audit-umum/-kinerja/-pengadaan; bukti tutup-loop: audit-kinerja 4 RAGU→0, audit-umum SPP-SPM k1→k2); rule diangkat ke **doktrin bersama `panduan-format-umum`** (+ grounding temuan-negatif) → pemantauan-TL 3 RAGU→0. **1.11** fix truncation `judge_pendapat` (konsultasi-pengadaan 0.40→**1.00**). **1.12** Standar Audit APIP **Permenpan 5/2008 → SAIPI/AAIPI 2021** (knowledge+fixtures). **1.13** doktrin **sasaran-first scoping** ke SEMUA skill non-LKE (panduan + orkestrator + 13 pointer; **LKE dikecualikan**) — teruji live reviu-rka-kl & reviu-pengadaan (scoping benar + precision-trap lolos; studi kasus 2-penugasan). **1.14** opsi **upload kriteria tambahan** semua skill non-LKE (panduan + orkestrator + 13 pointer). **1.15** **Surat Tugas = metadata INTEGRAL** (bukan upload, 4 skill dikoreksi); **selisih istilah LKE** diselaraskan (`fill_lke`→`_KKP/LKE-terisi-<skill>.xlsx`); **evaluasi-reformasi-birokrasi masuk rezim LKE** (gate + fill_lke) seperti SPIP/SAKIP. Baseline 16/16 kini lebih kokoh (RAGU sitasi hilang di audit+pemantauan).
  - *Sisa (opt-in, butuh API):* validasi auditor atas 13 golden + fixture · terus perbaiki presisi kutipan pasal audit.
- **DoD:** 0 reference rusak ✅ · terminologi seragam ✅ · baseline kualitas terekam (**16/16 live**, 16/16 golden) ✅.

## Fase 2 — Penyelarasan workflow dengan Pedoman Pengawasan (fokus #2) · *ciri khas v10*
Selaraskan alur kerja engine ke Pedoman/Juknis Pengawasan — **SK ikut sistem**, bukan sebaliknya.

> **✅ SELESAI (3 Jul 2026, `docs/PENYELARASAN-PEDOMAN-v10.md`).** Material pedoman diwarisi dari v9 (`USULAN-REVISI-SK.md`: 36 SDP + 13 errata + matriks proporsionalitas) + Pedoman asli di vault. Re-validasi konformansi engine v10 (pasca hardening + merge v8.8 + P1): **engine SELARAS** — errata sisi-engine (#1 shell, #2 KKSAR, #4 audit-leak, #5 assurance per-jenis, #6 survei audit-only) **semua terpenuhi**; merge v8.8 malah memperkuat (laporan faithful per-jenis). Semua artefak SDP produksi ADA (P.05 survei kini terimplementasi, PL.08 KKP+gate LKE, M.01-03 kendali mutu, K.01 Daftar Temuan, Tahapan 8 TU). Errata sisa = ranah **draft SK** (birokrasi), bukan engine. **0 perubahan kode** — engine sudah selaras.
- **2.1 Petakan gap** — bandingkan tahapan/artefak engine (KP→PKP→KKP→LHP→Daftar Temuan) vs Pedoman Pengawasan. *Butuh dokumen pedoman dari auditor.*
- **2.2 Selaraskan tahapan produksi** — sampai **laporan disetujui** (garis finis); adopsi hanya elemen pedoman yang **menambah nilai**, buang yang administratif-murni (→ ranah TU/INTEGRAL).
- **2.3 Selaraskan format artefak & penomoran** dengan pedoman (kode surat, struktur KKP/LHP, Daftar Temuan & Rekomendasi).
- **2.4 Tegaskan batas produksi vs administrasi** (garis serah: ekspor LHP + Daftar Temuan; sisanya administrasi).
- **DoD:** matriks gap engine↔pedoman + tahapan/artefak selaras, tanpa mengorbankan mesin produksi.

## Fase 3 — Simplifikasi fitur (fokus #3)

> **Progres:** ✅ **3.1+3.2** konsolidasi render LHR — buang tool `render_lhr_pbj` redundan (jalur reviu-pengadaan legacy via cross_check rule) → `render_report` jadi jalur tunggal semua skill KKSA (diverifikasi deterministik reviu+audit); `cross_check` tak lagi dirujuk app/ (deprecated, file v6 dibiarkan); fix hard-key `tanggal_exit_meeting`→`.get()`. Scan dead-tool: **0 dead**. ✅ **3.3 P4 meta-skill SELESAI** (10 Jul, main `7456562`) — `kepatuhan-saipi` & `graduasi-skill-spesifik` **dipindah `knowledge/skills/` → `knowledge/meta/`**; `skills/` kini hanya jenis pengawasan asli; registry `_HIDDEN_FROM_PICKER` kosong + `_EXCLUDE_DIRS` diramping; `_scan()`=19 skill. Aman: QC baca V6 copy `backend/v6/skills/kepatuhan-saipi` (utuh); tak ada runtime `load_skill` meta-skill; graduasi.py port self-contained. ✅ **3.4 ramping audit-kinerja SELESAI** (550→405 baris, −26%) — detail Survey Pendahuluan (research online + template Memo SP) → `references/09`, template sub-skill → `references/10`; substansi inti (2E/8-aspek/materialitas/KKSAR) tetap; **eval 0.883 (= baseline, no regresi)**.
- **3.1 Dead-code lanjutan** — `cross_check.py` (v6) tandai deprecated & pastikan tak diekspos; sisir tool/route tak terpakai.
- **3.2 Konsolidasi tool/format** — rapikan render/lhr/kkp tooling; format laporan jenis-aware satu sumber.
- **3.3 P4 meta-skill → INTEGRAL** — `kepatuhan-saipi` (QC SAIPI) & `graduasi-skill-spesifik` (pengembangan) keluar dari `knowledge/skills/` jadi tooling/reference portabel.
- **3.4 Ramping prompt & skill sisa** — turunkan yang masih gemuk (mis. audit-kinerja) ke references.
- **DoD:** engine lebih ramping & hemat token; tak ada meta-skill di jalur produksi substansi.

## Fase 4 — Validasi menyeluruh
- E2E live per keluarga skill (harness) + regression eval harness + rubrik divalidasi auditor.
- **DoD:** semua skill lulus baseline kualitas; harness E2E hijau end-to-end.

## Fase 5 — Perluasan skill (skill BARU) · *dimensi baru*

Menambah cakupan jenis pengawasan. Metode baku (terbukti E2E): folder + `SKILL.md` (auto-discover, profil `kksa`, render via fallback template generic) → **checklist per-aspek** → **fixture + golden** (`build_fixtures.py`) → **`live_measure.py`** → SKOR.

> **✅ 5.1 Rumah + isi 3 skill reviu keuangan (7 Jul).** `reviu-laporan-keuangan`, `reviu-pipk`, `reviu-pnbp` — engine-ready (portabilitas + scoping + kriteria-tambahan pointer; KKSAR Sebab anti-mengarang; keyakinan terbatas; PW.04.04), checklist 6-aspek terisi, `references/README` daftar kriteria kandidat. **Teruji live semua SKOR 1.00** (recall 1.0; umpan presisi lolos): LK 4/4 cacat 0-RAGU · PIPK 0-RAGU · PNBP 3/3 cacat (3 RAGU `kriteria` = **artefak nomor PMK/PP tarif masih placeholder**). Total skill terdaftar → **19** (dari 16).

- **5.1a ✅ Kriteria RIIL PNBP & LK — DIBUNDEL** (regulasi diunggah auditor 9 Jul). **PNBP** (`reviu-pnbp` v0.2): **PP 43/2023** (jenis & tarif, ganti PP 80/2015) · **PMK 155/PMK.02/2021 jo. PMK 58/2023** (jatuh tempo Ps.41 · tunggakan→piutang Ps.42 · optimalisasi Ps.55A · rekonsiliasi triwulanan Ps.135 · pengawasan APIP Ps.136) · **Permen Kominfo 1/2024** (tarif Rp0/0%) → ringkasan `.md` + PDF (PP 43/PMK 58/Permen 1) di `references/`; aspek/checklist diikat pasal; **RAGU `kriteria` PNBP tertutup**. **LK** (`reviu-laporan-keuangan` v0.2): **PMK 255/PMK.09/2015** (standar reviu; keyakinan terbatas; tahapan perencanaan→pelaksanaan(KKR)→pelaporan CHR/IHR/LHR; Pernyataan Telah Direviu) diringkas. **Wiki** `konteks/regulasi-kunci.md` +seksi PNBP & Reviu LK.
- **5.1b ✅ PIPK & Kebijakan Akuntansi — DIBUNDEL** (regulasi diunggah auditor 9 Jul). **PIPK** (`reviu-pipk` v0.2): **PMK 17/PMK.09/2019** (Pedoman Penerapan/Penilaian/Reviu PIPK Pempus — **mengganti PMK 14/PMK.09/2017**; PITE, PI tingkat proses/transaksi, ToC/CSA, klasifikasi kelemahan, CHR→LHR PIPK + PTD) diringkas ke `references/01-...md`, aspek diikat pasal; **RAGU `kriteria` PIPK tertutup**. **LK** (`reviu-laporan-keuangan` v0.3): **PMK 100/2025** (Kebijakan Akuntansi Pempus — ganti PMK 231/PMK.05/2022 jo. PMK 57/2023; ruang lingkup Ps.4 per pos; pengakuan/pengukuran/penyajian/pengungkapan; berlaku TA 2025) diringkas + PDF. **Wiki** +seksi PIPK & Kebijakan Akuntansi.
- **5.1c ✅ Pendukung LK — DIBUNDEL** (regulasi diunggah auditor 9 Jul). **PMK 232/PMK.05/2022** (Sistem Akuntansi & Pelaporan Keuangan Instansi — unit akuntansi UAKPA→UAPPA-W→UAPPA-E1→UAPA, rekonsiliasi, penyampaian LK semester/tahunan) · **PMK 214/PMK.05/2013 jo. PMK 42/2025** (BAS — 12 segmen; sinergi pusat-daerah PP 1/2024) · **PMK 171/PMK.05/2021 jo. PMK 158/2023** (Sistem SAKTI — sumber angka LK, rekonsiliasi ↔ SPAN) → diringkas `references/03-05` (+PDF BAS/Sinergi/SAKTI; induk PMK 232 & Lampiran BAS dari JDIH). Aspek reviu LK (rekonsiliasi/akurasi/kepatuhan proses) diikat nomor spesifik. `reviu-laporan-keuangan` v0.4. **Kriteria inti 3 skill reviu keuangan (PNBP/LK/PIPK) kini LENGKAP & bernomor — tak ada RAGU kriteria tersisa.**
- **5.2 ✅ (sebagian — inti selesai, 10 Jul main `25ebceb`)** — investigasi "template LHP per-skill" menemukan celah **substantif, bukan kosmetik**: `build_dasar_hukum_blocks(jenis)` di `render_lhp.py` hanya meng-handle `"pengadaan"` → LHP 3 skill reviu keuangan hanya memuat PP 60/2008 + SAIPI + PKPT (**kriteria riil yang baru dibundel TIDAK muncul di laporan**). **Fix:** cabang jenis untuk `reviu-laporan-keuangan` (PMK 255/2015 · PP 71/2010 · PMK 100/2025 · PMK 232/2022), `reviu-pipk` (PMK 17/2019), `reviu-pnbp` (UU 9/2018 · PP 43/2023 · PMK 155/2021 jo 58/2023). Diverifikasi unit-test + **render nyata** (0 placeholder). Metodologi & simpulan **sudah benar** (else-branch reviu-* pakai `_build_metodologi_reviu`+`build_simpulan_reviu` yang jenis-neutral) → tak diubah; template **generic tetap dipakai** (skema placeholder sama; klon bespoke = duplikasi tanpa nilai). *Sisa opsional:* template bespoke `reviu-laporan-keuangan` untuk lampiran **Pernyataan Telah Direviu** (khas PMK 255/2015) · golden divalidasi auditor (Fase 7.1) · perluas pola wiki per skill (Fase 6.2).
  - ⚠ *Catatan uji:* fixture eval punya `jenis_pengawasan=""` (eval jalan `--no render`) → jalur render jenis-aware **tak ter-cover eval**; di produksi diisi `routes/penugasan.py`. Verifikasi render dilakukan manual dgn jenis di-set.
- **DoD:** skill baru lolos baseline live + kriteria riil ter-bundel & tervalidasi auditor.

## Fase 6 — Integrasi Wiki (knowledge base ↔ engine) · *baru*

Perdalam pemanfaatan **wiki** (pola temuan, regulasi kunci, catatan objek) oleh skill/agen, & rapikan sinkronisasi vault↔git. Wiki sudah dipakai (agen `list_temuan_patterns`, `read_preload_context`); fase ini memperkuat & memperluas.
- **6.1 Sinkronisasi wiki** — `knowledge/wiki` (di-git, ~84 pattern) ↔ `llm-wiki/wiki` (vault, ~217 catatan, gitignored) via alur `wiki_update`; pastikan pola & catatan terbaru masuk engine (dua arah, anti-drift).
- **6.2 Pattern-driven quality** — `temuan-patterns/<skill>/` jadi (a) **hipotesis awal** agen (`list_temuan_patterns`) & (b) `pattern_ref` di golden case. Perluas cakupan pola per skill (termasuk **3 skill baru** reviu keuangan). Loop belajar: `submit_feedback` → usul pola baru (mis. AP-30/AP-31) masuk wiki setelah reviu.
- **6.3 Preload konteks objek** — `read_preload_context` menyuplai **regulasi kunci + catatan objek** per penugasan; perkuat cakupan, kesegaran, & keterhubungan ke kriteria skill.
- **6.4 Regulasi ↔ kriteria** — jadikan wiki regulasi-kunci sumber pemutakhiran nomor/pasal kriteria skill (mendukung doktrin *currency* — mis. konfirmasi PP tarif PNBP, PMK terbaru).
- **DoD:** pola/regulasi/catatan wiki tersinkron & terpakai konsisten oleh 19 skill; golden ber-`pattern_ref`; loop feedback→wiki berjalan.

## Fase 7 — User Test (UAT auditor) & go-live · *baru*

Validasi **dunia nyata oleh auditor** — bukan hanya fixture sintetis + judge. Menjawab caveat berulang "golden/fixture perlu validasi auditor".
- **7.1 Validasi golden + fixture** oleh auditor senior — sahkan `expected_key_issues`; koreksi diksi (mis. audit-umum Q4/Q5). Skor jadi **baseline resmi** setelah divalidasi manusia.
- **7.2 UAT E2E per keluarga skill** dengan **berkas penugasan NYATA** (bukan sintetis) — auditor menilai kualitas temuan & laporan (KKP/LHP) end-to-end.
- **7.3 Konfirmasi & bundel kriteria riil** — nomor PP/PMK (khusus 3 skill baru: PP tarif PNBP Komdigi, PMK SAKTI/BAS/Penyusunan LK, status PMK 14/2017 PIPK) → **hilangkan RAGU `kriteria`**.
- **7.4 Uji integrasi INTEGRAL** — orkestrator nyata menyuplai kontrak file (`sasaran-assignment.json`, `hitl-overlay.json`) + alur/tombol UI; pastikan engine buta-DB berjalan mulus di produksi.
- **DoD:** skill lolos UAT auditor; baseline **tervalidasi manusia**; siap produksi di INTEGRAL.

---

## Kontrak dokumen per skill — reminder unggah (WAJIB vs OPSIONAL)

**Berlaku umum:** Surat Tugas + sasaran/lingkup = **metadata dari INTEGRAL** (TIDAK diunggah). Semua skill **non-LKE** boleh menerima **Kriteria tambahan (opsional)**.

**Unggah kriteria sendiri (regulasi/SOP) + objek:**
- **audit-umum** — WAJIB: kriteria (regulasi/SOP/SK/Juklak) + dokumen objek · OPSIONAL: ND permintaan, data pendukung.
- **reviu-umum** — WAJIB: kriteria (juklak/juknis/format/SOP) + dokumen objek · OPSIONAL: data pendukung.
- **evaluasi-umum** — WAJIB: kriteria evaluasi (pedoman + LKE/rubrik) + dokumen & data objek · OPSIONAL: instrumen survei, data baseline.
- **pemantauan-umum** — WAJIB: kriteria/acuan (rencana aksi/target/jadwal/instruksi bertenggat) + data realisasi · OPSIONAL: data historis, foto/BA, dashboard.
- **audit-kinerja** — WAJIB: dokumen internal program (proses bisnis/SOP/target/PK) sbg kriteria + data kinerja & objek · OPSIONAL: sub-skill program.
- **evaluasi-manajemen-risiko** — WAJIB: Piagam MR, Formulir 1–5, LED, SK Komite MR, dokumen SPIP.

**Berbasis LKE** (tanpa opsi kriteria tambahan):
- **evaluasi-spip** — WAJIB: LKE SPIP (template *bundled*) + folder bukti dukung per unsur.
- **evaluasi-sakip** — WAJIB: LKE SAKIP self-assessment (PermenPAN-RB 88/2021) + bukti dukung per sub-komponen (evsakip).
- **evaluasi-reformasi-birokrasi** — WAJIB: LKE RB (*diunggah*) + Rencana Aksi/Road Map RB + bukti dukung · OPSIONAL: laporan capaian triwulan, Renstra/PK.

**Pengadaan & Anggaran (PBJ / RKA-K/L):**
- **reviu-rka-kl** — WAJIB: TOR/KAK + RAB **per RO** · OPSIONAL: data dukung harga (survei/RFI, kontrak pembanding, HPS).
- **reviu-pengadaan** — WAJIB: dok perencanaan–pemilihan (KAK/HPS/dok tender); *aspek RUP:* populasi RKA/DIPA + export SIRUP · OPSIONAL: studi kelayakan (FS), kontrak pembanding/RFI.
- **audit-pengadaan** — WAJIB: dokumen **seluruh siklus** PBJ (KAK/HPS/Kontrak/BAST/pembayaran/dok pemeriksaan) · OPSIONAL: studi kelayakan (FS), data pendukung.
- **pemantauan-pengadaan** — WAJIB: kontrak + laporan progres + BA kemajuan + dokumen pembayaran.

**Reviu keuangan (BARU):**
- **reviu-laporan-keuangan** — WAJIB: komponen LK (LRA/Neraca/LO/LPE/CaLK) + rekonsiliasi (SAKTI↔SPAN/BMN/kas) + BAS/kertas kerja · OPSIONAL: LK periode lalu, LHP BPK.
- **reviu-pipk** — WAJIB: dok penerapan/penilaian PIPK (lingkup & risiko, dokumentasi pengendalian entitas & proses, kertas kerja ToC/CSA, simpulan efektivitas) + LK konteks · OPSIONAL: rencana perbaikan.
- **reviu-pnbp** — WAJIB: target & realisasi PNBP, SK/penetapan tarif, PNBP terutang per wajib bayar, bukti setor/SSBP (SIMPONI), kartu piutang · OPSIONAL: izin & realisasi penggunaan, rekonsiliasi.

**Lainnya:**
- **pemantauan-tindak-lanjut** — WAJIB: daftar rekomendasi (dari LHP/CHR) + bukti tindak lanjut per rekomendasi · OPSIONAL: rekap TLHP internal.
- **konsultansi-umum** — WAJIB: ND/disposisi + **pertanyaan tertulis** + dokumen konteks objek · OPSIONAL: dokumen kriteria/regulasi.
- **konsultasi-pengadaan** — WAJIB: pertanyaan advisory + draft dokumen PBJ yang didampingi · OPSIONAL: regulasi/SE terkait.

> Dokumen WAJIB tak lengkap → engine mencatat **keterbatasan** ("tidak cukup data"), bukan mengarang deviasi. LKE scan/gambar tak terekstrak → turunkan 1 level predikat + catat keterbatasan.

---

## Urutan disarankan
**Fase 0–3 ✅ · Fase 4 (16/16 live) 🟢 · Fase 5 (skill baru) berjalan.** Forward: **Fase 6 (Integrasi Wiki)** + **Fase 7 (User Test / UAT auditor)** — dua ini yang membawa v10 dari "terukur via judge" ke "**tervalidasi manusia & siap produksi**". Fase 6 & 7 dapat berjalan **paralel** (wiki memperkaya pola; UAT memvalidasi output). Prasyarat UAT yang menunggu Anda: (a) validasi golden/fixture auditor · (b) konfirmasi nomor kriteria (3 skill baru) · (c) berkas penugasan nyata untuk uji E2E.
