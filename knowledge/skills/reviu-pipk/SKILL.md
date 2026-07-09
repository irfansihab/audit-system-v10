---
name: reviu-pipk
jenis: Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)
format_laporan: kksa
dasar-hukum: PMK 17/PMK.09/2019 (Pedoman Penerapan, Penilaian & Reviu PIPK Pempus — mengganti PMK 14/PMK.09/2017); PP 60/2008 (SPIP); Pasal 8 UU 17/2003 & Pasal 55 UU 1/2004
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.2"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT.
  - v0.2 (2026-07-09): **Kriteria PIPK dikonfirmasi & diringkas** — PMK 14/PMK.09/2017 **sudah diganti PMK 17/PMK.09/2019** (regulasi diunggah auditor 9 Jul) → ringkasan `references/01-...md`. Aspek/checklist diikat pasal/definisi PMK 17/2019 (PITE, tingkat proses/transaksi, ToC, CHR/LHR PIPK, PTD). RAGU `kriteria` PIPK tertutup. (Validasi golden/fixture auditor tetap menyusul.)
---

# Skill: Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP yang melakukan **reviu atas Pengendalian Intern atas Pelaporan Keuangan (PIPK)** — menilai **kecukupan desain** dan **efektivitas operasi** pengendalian yang menjamin keandalan pelaporan keuangan (asersi: keberadaan/keterjadian, kelengkapan, hak & kewajiban, penilaian/alokasi, penyajian & pengungkapan). Reviu memberi **keyakinan terbatas** atas simpulan efektivitas PIPK yang dibuat entitas. **Bukan audit**; tidak menyatakan opini, tidak menghitung kerugian negara. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **dokumen penerapan & penilaian PIPK** entitas — penetapan lingkup & identifikasi risiko pelaporan keuangan, dokumentasi pengendalian tingkat entitas & tingkat proses/transaksi, kertas kerja pengujian pengendalian (ToC)/Control Self-Assessment (CSA), simpulan efektivitas PIPK, rencana perbaikan; plus LK terkait sebagai konteks asersi. Fakta ditarik dari digest; verifikasi ke sumber untuk kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu

> Kriteria inti = **PMK 17/PMK.09/2019** (ganti PMK 14/2017), diringkas di [`references/01-...md`](references/01-pmk-17-2019-pipk.md). Kutip **presisi** pasal/istilah. Nilai per elemen: kecukupan **desain** + efektivitas **operasi** (Memadai / Memadai dengan catatan / Tidak memadai).

| # | Aspek | Yang dinilai | Kriteria acuan (bernomor) |
|---|-------|--------------|---------------------------|
| 1 | **Lingkup & identifikasi risiko pelaporan keuangan** | Akun/proses signifikan & asersi teridentifikasi; risiko salah saji dipetakan (RCM) | **PMK 17/2019** (penetapan lingkup: materialitas · key business processes · akun signifikan · asersi · penilaian risiko) |
| 2 | **Pengendalian tingkat entitas** (PITE) | Lingkungan pengendalian, penilaian risiko, informasi & komunikasi, pemantauan | **PMK 17/2019** (PITE) + **PP 60/2008** (5 unsur SPIP) |
| 3 | **Pengendalian tingkat proses/transaksi** | Kontrol per siklus (pendapatan, belanja, aset/persediaan, kas) memadai & dijalankan | **PMK 17/2019** (PI Tingkat Proses/Transaksi) |
| 4 | **Pengujian pengendalian (ToC) & CSA** | Metode/ sampel memadai; menguji efektivitas operasi; simpulan didukung bukti | **PMK 17/2019** (Pengujian PITE & Tingkat Proses/Transaksi) |
| 5 | **Simpulan efektivitas & rencana perbaikan** | Simpulan konsisten dengan hasil pengujian; defisiensi diklasifikasi → rencana aksi (AoI); output CHR→LHR PIPK + PTD | **PMK 17/2019** (klasifikasi kelemahan · CHR/LHR PIPK · PTD) |
| 6 | **Keandalan dokumentasi PIPK** | Kertas kerja lengkap, tertelusur, ter-review berjenjang | **PMK 17/2019** (dokumentasi) |

### Checklist Reviu PIPK (per aspek — wajib ditelusuri; nilai kecukupan DESAIN + efektivitas OPERASI: Memadai / Memadai dgn catatan / Tidak memadai)

**Aspek 1 — Lingkup & identifikasi risiko:** akun/proses **signifikan** teridentifikasi; **asersi** (keberadaan/keterjadian, kelengkapan, hak & kewajiban, penilaian/alokasi, penyajian) dipetakan; **Risk-Control Matrix (RCM)** ada & risiko salah saji terhubung ke pengendalian kunci.

**Aspek 2 — Pengendalian tingkat entitas:** 5 unsur SPIP (PP 60/2008) di level entitas terdokumentasi & berjalan — lingkungan pengendalian, penilaian risiko, kegiatan pengendalian, informasi & komunikasi, pemantauan.

**Aspek 3 — Pengendalian tingkat proses/transaksi:** kontrol kunci per siklus (**pendapatan/PNBP, belanja, aset & persediaan, kas**) memadai & dijalankan — **otorisasi, rekonsiliasi, pemisahan fungsi (SoD), pembatasan akses**; tidak ada rangkap fungsi tak terkendali.

**Aspek 4 — Pengujian pengendalian (ToC) & CSA:** metode & **ukuran sampel** memadai; ToC menguji efektivitas operasi (bukan sekadar keberadaan dokumen); simpulan didukung bukti pengujian.

**Aspek 5 — Simpulan efektivitas & rencana perbaikan:** simpulan efektivitas PIPK **konsisten** dengan hasil pengujian (tidak overstated); **defisiensi** (defisiensi/ signifikan/ material weakness) diklasifikasi; kelemahan → **rencana aksi perbaikan (AoI)** dgn PIC & target.

**Aspek 6 — Keandalan dokumentasi:** kertas kerja lengkap, tertelusur ke bukti, ter-review berjenjang.

> Tiap elemen **tidak memadai** → catatan **K/K/S/A** (Kondisi = kelemahan desain/operasi pengendalian; Kriteria kutip **presisi** PMK 17/PMK.09/2019 / PP 60/2008 + pasal; Sebab anti-mengarang; Akibat = **risiko salah saji/keandalan pelaporan**, tanpa kerugian negara). Elemen memadai → nyatakan "telah memenuhi". Bila periode objek di luar rentang berlaku PMK 17/2019 → catatan, bukan deviasi terkonfirmasi.

## Format Unsur Temuan (KKSAR)

Catatan reviu **K/K/S/A** — **Kondisi** (kelemahan pengendalian: proses/kontrol + dokumen), **Kriteria** (PMK PIPK/PP 60/2008 + pasal, kutip **presisi**), **Sebab** (anti-mengarang), **Akibat** (risiko salah saji/keandalan pelaporan; **tanpa kerugian negara**). **Rekomendasi di LHR.** Doktrin: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan → Hasil Reviu (per aspek/level pengendalian) → Simpulan efektivitas PIPK (keyakinan terbatas) → Saran perbaikan. Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria dibundel — lihat [`references/`](references/))

- [`01-pmk-17-2019-pipk.md`](references/01-pmk-17-2019-pipk.md) — Pedoman Penerapan/Penilaian/Reviu PIPK (ganti PMK 14/2017); PITE, tingkat proses/transaksi, ToC, CHR/LHR PIPK, PTD.
- [`README.md`](references/README.md) — daftar lengkap + status. PP 60/2008 (SPIP) sbg unsur pengendalian pendukung.

## Batasan

- Reviu = keyakinan terbatas atas simpulan PIPK entitas, **bukan** pengujian pengendalian menyeluruh oleh APIP; bukan opini.
- **PMK 17/PMK.09/2019** menggantikan PMK 14/PMK.09/2017 — gunakan yang berlaku untuk periode objek; bila di luar rentang → catatan, bukan temuan.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-laporan-keuangan`, `reviu-pnbp`). PIPK menopang keandalan LK (kaitan dengan asersi LK); temuan kelemahan pengendalian material → dapat memicu pendalaman audit.
