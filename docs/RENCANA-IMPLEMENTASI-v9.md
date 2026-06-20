# Rencana Implementasi Bertahap — Audit AI v9 (Penyelarasan Juknis)

Prinsip: **SK mengikuti sistem (v9 = jangkar)** · **v9 = mesin produksi substansi**, garis finis = *laporan disetujui* · pasca‑persetujuan = administrasi (peran TU). Bahan pimpinan: [`penyelarasan-juknis-v8.html`](penyelarasan-juknis-v8.html).

## Ikhtisar fase

| Fase | Tujuan | Bobot | Bergantung |
|---|---|---|---|
| **0** ✅ | Fondasi & higiene (repo publik aman, peran TU, deps) — **SELESAI** | S | — |
| **1** | Format laporan **KKSAR terpadu** (shell seragam + istilah baku + RE per jenis) | M | 0 |
| **1A** ✅ | Penguatan agen **AT**: **Root Cause Analysis** untuk unsur Sebab — **SELESAI** | M | 1 |
| **1B** ✅ | Penguatan agen **KT**: **tabel & diagram** dalam laporan — **SELESAI** | M | 1 |
| **2** | **Lembar Kendali Mutu Berjenjang** (gabung M.01+M.02+M.03) | M | 0 |
| **3** | **Auto‑generate dokumen produksi** (Daftar Temuan & Rekomendasi, indeksasi) | M | 1 |
| **4** | **Tahapan 8 — Administrasi (TU)** (handoff + register ringkas) | L | 0,3 |
| **5** | **Proporsionalitas per jenis** + paket usulan revisi SK | M | 1–4 |

> Prasyarat jalan‑uji v9: `cd frontend && npm install`; `cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

---

## Fase 0 — Fondasi & higiene
**Tujuan:** repo publik bersih + fondasi peran administrasi.
- **0.1 Harden `DEV_PASSWORD`** → pindah ke env (`DEV_SEED_PASSWORD`, default acak bila tak diset). File: `backend/app/init_db.py`. *(S)*
- **0.2 Tambah peran `TU`** ke enum + seed + tipe FE (pola sama seperti penambahan `ADMIN`). File: `backend/app/models.py` (Role), `backend/app/init_db.py` (seed user `tu`), `frontend/lib/api.ts` (`Role`). *(S)*
- **0.3 Regenerasi dependensi** v9 (npm + venv) lalu smoke test backend/frontend. *(S)*

**Acceptance:** tak ada kredensial hidup/keras di repo; login `tu` menghasilkan `role_aktif: TU`; backend `:8000` & frontend `:3000` 200.

> **Status SELESAI (20 Jun):** ✅ password seed via `DEV_SEED_PASSWORD` (acak bila kosong) + quick-login FE via `NEXT_PUBLIC_DEV_PASSWORD` (mati bila kosong); ✅ peran `TU` (enum + seed user `tu` + tipe FE + label TopBar + default stage); ✅ deps v9 ter-install (npm + venv py3.12); ✅ DB diisolasi ke `audit_v9`. Verifikasi: backend app import OK (Role.TU, env terbaca), `tsc` 0 error.
> **Sisa (live smoke, butuh Docker):** nyalakan Docker → `createdb audit_v9` (atau `docker exec <db> createdb -U audit audit_v9`) → jalankan backend (seed otomatis) → uji login `tu`.

---

## Fase 1 — Format laporan KKSAR terpadu
**Tujuan:** semua jenis laporan memakai shell seragam + istilah unsur baku (KKSAR), variasi per jenis yang berprinsip.
- **1.1 Shell seragam**: pastikan render semua jenis = Nota Dinas → Cover → Isi (Pendahuluan → Hasil → Simpulan → Rekomendasi/Saran). File: `backend/app/tools/lhr_tools.py` (`_finalize_jenis`/`_apply_jenis`), template `knowledge/templates/*.docx`. *(M)*
- **1.2 Baku‑kan istilah unsur** di narasi laporan ke **Sebab/Akibat** (bukan "Analisis Penyebab/Dampak‑Risiko"). Cek `_JENIS_PARAGRAF` + template. *(S)*
- **1.3 Tabel pengurangan unsur per jenis** sebagai standar (sudah ada di `render_kkp.py` + `PANDUAN.md`) → jadikan satu sumber kebenaran + acuan SK. *(S)*
- **1.4 Ringkasan Eksekutif (L.06) jenis‑aware**: tambah section + frasa assurance/non‑assurance yang benar (hindari "keyakinan memadai" di pemantauan/konsultansi). File: `lhr_tools.py` + template. *(M)*

**Acceptance:** 6 jenis (LHA/LHR/LHE/LP/Memo + RE) render dengan shell konsisten; istilah unsur = KKSAR; RE benar per jenis. Uji render 1 sampel tiap jenis.

---

## Fase 1A — Penguatan agen AT: Root Cause Analysis untuk Sebab
**Tujuan:** Anggota Tim menyusun unsur **Sebab** dengan metode **Root Cause Analysis (RCA)** — menelusuri dari gejala (Kondisi) ke **akar penyebab**, bukan sebab permukaan/tebakan.
- **1A.1 Doktrin RCA di panduan**: tambahkan metode baku di `PANDUAN.md` (§Sebab) — **5 Whys** (rantai "mengapa" berlapis) + **Fishbone/Ishikawa** dengan kategori APIP: *Manusia/SDM · Metode/Proses/SOP · Sistem/Teknologi · Kebijakan/Regulasi · Sarana/Anggaran*. *(S)*
- **1A.2 Orkestrasi AT**: perkuat `backend/app/prompts/anggota_tim.md` — saat menyusun Sebab, AT **wajib** menelusuri rantai why dan/atau kategori fishbone, **grounded ke bukti** (kutip dokumen sumber). *(M)*
- **1A.3 Anti‑mengarang (tegas)**: RCA **tidak boleh** memaksakan akar tanpa bukti — bila tak cukup → tetap **"Tidak cukup data untuk menyimpulkan penyebab"**. RCA hanya untuk jenis ber‑Sebab (audit/reviu/evaluasi non‑LKE/pemantauan); **bukan** evaluasi‑LKE & konsultansi. *(S)*
- **1A.4 Jejak RCA di KKP** (opsional): rekam rantai why ringkas pada temuan (mis. field `rca` di `temuan.json`) agar **rekomendasi menyentuh akar** (selaras prinsip PANDUAN). File: skema `append_temuan` + `render_kkp.py`. *(M)*
- **1A.5 Checklist skill**: tambahkan butir "Sebab berbasis RCA & terhubung ke rekomendasi" di SKILL.md skill ber‑Sebab. *(S)*

**Acceptance:** pada penugasan audit, Sebab memperlihatkan penelusuran akar (rantai why/kategori fishbone) yang grounded ke bukti dan **terhubung ke rekomendasi**; kasus tanpa bukti tetap jujur "tidak cukup data".

> **Status SELESAI (20 Jun):** ✅ 1A.1 doktrin RCA (5 Whys + Fishbone 5 kategori APIP) di `PANDUAN.md` §Metode RCA; ✅ 1A.2/1A.3 orkestrasi AT diperkuat di `anggota_tim.md` (cari akar via RCA, tiap lapisan didukung bukti, rekomendasi menyentuh akar, anti-mengarang tetap mutlak); ✅ 1A.5 berlaku lintas skill ber-Sebab via PANDUAN bersama + driver AT (tanpa edit 11 SKILL.md). Berlaku hanya jenis ber-Sebab (bukan evaluasi-LKE/konsultansi). **1A.4** (field `rca` terstruktur di temuan.json) = opsional, ditunda. Uji mutu live menyusul saat menjalankan agen (butuh Docker+API).

## Fase 1B — Penguatan agen KT: tabel & diagram dalam laporan
**Tujuan:** Ketua Tim dapat menyisipkan **tabel** dan **diagram** untuk memperjelas laporan (mis. rekap temuan per aspek, matriks nilai/severity, grafik tren TLHP, diagram alur proses).
- **1B.1 Tool render tabel**: kemampuan KT menghasilkan **tabel** (markdown → tabel `.docx` via python‑docx). File: `backend/app/tools/lhr_tools.py` (+ tool `render_table`/penyisipan tabel ke laporan). *(M)*
- **1B.2 Tool render diagram**: grafik gambar (matplotlib → PNG disisipkan ke `.docx`) untuk **bar/pie/line** sederhana — mis. rekap severity per aspek, status TL. Tool `render_chart` (data → gambar → embed). *(M)*
- **1B.3 Orkestrasi KT**: perkuat `backend/app/prompts/ketua_tim.md` — KT memilih kapan tabel/diagram menambah nilai (jangan dekoratif); data tabel/grafik **bersumber dari temuan.json/TLHP**, bukan dikarang. *(S)*
- **1B.4 Bertahap**: mulai **tabel** (mudah & paling dibutuhkan) → lanjut **diagram gambar**. *(—)*

**Acceptance:** KT dapat menambahkan ≥1 tabel rekap + ≥1 diagram (mis. grafik severity per aspek) ke laporan, ter‑render rapi di `.docx`, dengan data dari sumber kebenaran (bukan dikarang).

> **Status SELESAI (20 Jun):** ✅ tool `append_lampiran_tabel` (python-docx) & `append_lampiran_diagram` (matplotlib Agg: bar/pie/line → PNG → embed) di `lhr_tools.py`, terdaftar di `LHR_TOOLS`; ✅ matplotlib ditambah ke `requirements.txt` + terpasang di venv; ✅ `ketua_tim.md` diperkuat (tool + langkah opsional pasca-render, data dari sumber kebenaran/anti-dekoratif). Verifikasi unit: kedua tool menyisipkan tabel + gambar ke docx contoh (1 tabel, 1 image, OK). matplotlib di-import lazy → bila absen, tool tabel tetap jalan & diagram gagal anggun.

## Fase 2 — Lembar Kendali Mutu Berjenjang
**Tujuan:** satu lembar mutu berjenjang menggantikan 3 dokumen SDP‑M yang tumpang tindih.
- **2.1 Backend QC**: perkaya `run_qc_kkp` dengan **14 butir Daftar Periksa QA/QC (SDP‑M.02)** di atas cek SAIPI yang ada. *(M)*
- **2.2 Frontend**: kembangkan `LembarReviuPanel` (sudah ada KT + PT‑verdict hasil dedup LRS) → **3 level**: KT self‑review · PT supervisi (7 area SDP‑M.01) · PM QA‑QC (14 butir) + **sign‑off berjenjang**. File: `frontend/components/LembarReviuPanel.tsx`, `frontend/app/penugasan/[id]/page.tsx`. *(M)*
- **2.3 Sinkron status**: paraf/sign‑off berjenjang tetap memicu approval (yang sudah menarik rekomendasi ke garis serah). *(S)*

**Acceptance:** satu komponen mutu menampilkan 3 level + checklist 14 butir + sign‑off; approval tetap jalan (TLHP handoff tak putus).

---

## Fase 3 — Auto‑generate dokumen produksi (ekspor)
**Tujuan:** dokumen "komunikasi" yang bernilai dihasilkan otomatis dari data, bukan diketik.
- **3.1 Daftar Temuan & Rekomendasi (SDP‑K.01/DHP)** auto dari `_KKP/temuan.json` + rekomendasi → artefak di garis serah. File: skrip render baru (pola `render_kkp.py`) + tool/endpoint. *(M)*
- **3.2 Indeksasi/metadata KKP (SDP‑PL.10)** otomatis (kode `no_kkp` + `dokumen_sumber`), bukan tickmark manual. *(S)*
- **3.3 (Opsional) Log komunikasi/monitoring** dari `agent_runs` (audit trail). *(S)*

**Acceptance:** "Daftar Temuan & Rekomendasi" ter‑generate & terunduh saat laporan disetujui; indeks KKP konsisten.

---

## Fase 4 — Tahapan 8: Administrasi (peran TU)
**Tujuan:** wadah administrasi pasca‑persetujuan, dikerjakan TU, lean (handoff + register ringkas).
- **4.1 Stage 8 di FE**: tambah tahap "Administrasi" di `HeroPenugasan`/`StageGrid` + render konten di `page.tsx`; akses untuk `TU` (read‑only ke substansi). *(M)*
- **4.2 Pemicu & prefill**: saat laporan disetujui → tahap 8 terbuka, ter‑prefill paket ekspor (LHP final + Daftar Temuan dari Fase 3). *(S)*
- **4.3 Isi tahap 8**: (a) paket ekspor; (b) **draft surat penyampaian** LHP (auto dari LHP, TU lengkapi agenda/tanggal); (c) **register tindak lanjut** (status komitmen & pemantauan). Backend: model + endpoint register. *(L)*
- **4.4 Batas SIMWAS**: penomoran resmi/TTE/distribusi/arsip → ekspor ke SIMWAS, bukan diproduksi v9. *(S)*

**Acceptance:** TU login → buka Tahap 8 → lihat paket ekspor, draft surat, isi register TL; auditor tak terbebani.

---

## Fase 5 — Proporsionalitas per jenis + paket usulan SK
**Tujuan:** sistem menampilkan dokumen sesuai jenis penugasan; siapkan bahan revisi SK.
- **5.1 Matriks WAJIB per jenis** (audit/reviu/evaluasi/pemantauan/konsultansi) di‑encode: dokumen/stage yang muncul menyesuaikan jenis. File: konfigurasi skill + FE stage gating. *(M)*
- **5.2 Paket usulan revisi SK**: errata konsistensi + matriks proporsionalitas + tabel pemetaan SDP↔v9 + klausul digital‑native — sebagai lampiran usulan ke penyusun SK. *(M)*

**Acceptance:** UI menyesuaikan dokumen per jenis; dokumen usulan SK siap dibawa ke rapat.

---

## Urutan eksekusi disarankan
`Fase 0 → 1 → (1A, 1B) → 2 → 3 → 4 → 5`. Fase **1A** (AT‑RCA) & **1B** (KT tabel/diagram) berjalan setelah Fase 1 dan bisa paralel dengan Fase 2. Fase 4 menunggu Fase 3 (butuh artefak ekspor). Setiap fase: implementasi → uji (render/endpoint/UI) → commit → push `origin/main`.

**Penguatan agen (1A/1B) = prioritas tinggi**: 1A menaikkan mutu substansi (akar masalah → rekomendasi tepat), 1B menaikkan kejelasan laporan untuk pimpinan. Keduanya bersifat *prompt + tool* sehingga dampaknya lintas semua jenis penugasan.
