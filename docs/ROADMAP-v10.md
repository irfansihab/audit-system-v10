# Roadmap v10 — Hardening · Penyelarasan Workflow · Simplifikasi

**Basis:** fork v9 (engine-ready 16/16). **Pivot:** AI = ENGINE; orkestrator+UI = INTEGRAL; FE/BE v10 = harness uji. **Sumber backlog teknis:** `docs/SKILL-AUDIT-BACKLOG-v9.md`.

**Prinsip kerja tiap fase:** harness tetap hijau · perubahan markdown/skill tanpa restart · yang menyentuh output → uji (eval harness + judge / E2E live) · commit + push per unit · doktrin (KKSAR/LKE) tak diubah tanpa alasan eksplisit.

---

## Fase 0 — Tuntaskan pondasi engine (sisa P1) · *enabler*
Menutup lapis portabilitas agar hardening berpijak pada engine yang benar-benar buta-orkestrasi.
- **0.1 P1#8 — de-UI prompt agen** (`anggota_tim.md`/`ketua_tim.md`): ganti "tab Setup/via UI"/status `DISETUJUI_KT` → kontrak file/data. *Markdown, risiko rendah.*
- **0.2 P1c — lepas `render_kkp_docx` & `read_context` dari DB** → kontrak file `_KKP/hitl-overlay.json` (`{rejected_ids, edits}`) + hook backend materialisasi (hybrid: file → fallback DB) + **uji live** (edit temuan → render → konfirmasi terterap). *Satu-satunya sisa P1 sentuh backend; bisa ditunda bila ingin fokus hardening dulu.*
- **DoD:** tak ada skill/tool/prompt yang mengasumsikan UI/DB v9; harness E2E hijau.

## Fase 1 — Hardening skill (fokus #1)
Mutu & ketahanan output tiap skill.
- **1.1 Reference rusak/legacy (P2)** — `reviu-umum`/`graduasi` rujuk `audit-system-v4` → `panduan-format-umum`; `audit-kinerja` 7/8 reference TODO/absen → ground-kan (RCA/2E); `kepatuhan-saipi` (`qc_saipi.py`/`wiki/raw/*.pdf`); `konsultasi-pengadaan`/`reviu-pengadaan` README hilang.
- **1.2 Terminologi baku (P2)** — `CCSAA`→**KKSAR** (audit-kinerja/pengadaan/umum); `3E`→**2E** (audit-kinerja, lingkup ekonomis ditunda).
- **1.3 reviu-rka-kl rule→checklist tuntas (P2)** — buang jejak "40 rules"/`cross_check`/benchmark; checklist murni.
- **1.4 Versi/frontmatter konsisten (P2)** — satukan versi lintas file; `model:` sudah dicabut saat engine-ready — pastikan bersih.
- **1.5 kepatuhan-saipi (P2)** — cek unsur **Sebab** (SAIPI 2320) untuk jenis ber-KKSA + kodefikasi.
- **1.6 Uji kualitas terukur** — perluas eval harness ke semua skill (golden case + rubrik + judge); tetapkan **baseline** precision/recall/narasi per skill; jadikan gate regresi.
- **DoD:** 0 reference rusak; terminologi seragam; baseline kualitas terekam & lulus ambang.

## Fase 2 — Penyelarasan workflow dengan Pedoman Pengawasan (fokus #2) · *ciri khas v10*
Selaraskan alur kerja engine ke Pedoman/Juknis Pengawasan — **SK ikut sistem**, bukan sebaliknya.
- **2.1 Petakan gap** — bandingkan tahapan/artefak engine (KP→PKP→KKP→LHP→Daftar Temuan) vs Pedoman Pengawasan. *Butuh dokumen pedoman dari auditor.*
- **2.2 Selaraskan tahapan produksi** — sampai **laporan disetujui** (garis finis); adopsi hanya elemen pedoman yang **menambah nilai**, buang yang administratif-murni (→ ranah TU/INTEGRAL).
- **2.3 Selaraskan format artefak & penomoran** dengan pedoman (kode surat, struktur KKP/LHP, Daftar Temuan & Rekomendasi).
- **2.4 Tegaskan batas produksi vs administrasi** (garis serah: ekspor LHP + Daftar Temuan; sisanya administrasi).
- **DoD:** matriks gap engine↔pedoman + tahapan/artefak selaras, tanpa mengorbankan mesin produksi.

## Fase 3 — Simplifikasi fitur (fokus #3)
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
