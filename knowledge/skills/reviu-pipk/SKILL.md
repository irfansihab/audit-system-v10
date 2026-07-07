---
name: reviu-pipk
jenis: Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)
format_laporan: kksa
dasar-hukum: PMK Pedoman PIPK (PMK 14/PMK.09/2017 — konfirmasi versi berlaku), PP 60/2008 (SPIP)
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.1"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT, perlu pengisian & validasi auditor senior.
---

# Skill: Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP yang melakukan **reviu atas Pengendalian Intern atas Pelaporan Keuangan (PIPK)** — menilai **kecukupan desain** dan **efektivitas operasi** pengendalian yang menjamin keandalan pelaporan keuangan (asersi: keberadaan/keterjadian, kelengkapan, hak & kewajiban, penilaian/alokasi, penyajian & pengungkapan). Reviu memberi **keyakinan terbatas** atas simpulan efektivitas PIPK yang dibuat entitas. **Bukan audit**; tidak menyatakan opini, tidak menghitung kerugian negara. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **dokumen penerapan & penilaian PIPK** entitas — penetapan lingkup & identifikasi risiko pelaporan keuangan, dokumentasi pengendalian tingkat entitas & tingkat proses/transaksi, kertas kerja pengujian pengendalian (ToC)/Control Self-Assessment (CSA), simpulan efektivitas PIPK, rencana perbaikan; plus LK terkait sebagai konteks asersi. Fakta ditarik dari digest; verifikasi ke sumber untuk kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu (DRAFT — perlu pengisian & validasi auditor)

> Kerangka rancangan awal; kriteria pasti (PMK/pasal) **wajib dikonfirmasi berlaku**. Nilai per elemen: kecukupan **desain** + efektivitas **operasi** (Memadai / Memadai dengan catatan / Tidak memadai).

| # | Aspek | Yang dinilai | Kriteria acuan (kandidat) |
|---|-------|--------------|---------------------------|
| 1 | **Lingkup & identifikasi risiko pelaporan keuangan** | Akun/proses signifikan & asersi teridentifikasi; risiko salah saji dipetakan | PMK Pedoman PIPK |
| 2 | **Pengendalian tingkat entitas** (entity-level) | Lingkungan pengendalian, penilaian risiko, informasi & komunikasi, pemantauan | PMK Pedoman PIPK + PP 60/2008 (unsur SPIP) |
| 3 | **Pengendalian tingkat proses/transaksi** | Kontrol per siklus (pendapatan, belanja, aset/persediaan, kas) memadai & dijalankan | PMK Pedoman PIPK |
| 4 | **Pengujian pengendalian (ToC) & CSA** | Metode/ sampel memadai; simpulan didukung bukti | PMK Pedoman PIPK |
| 5 | **Simpulan efektivitas & rencana perbaikan** | Simpulan konsisten dengan hasil pengujian; kelemahan → rencana aksi (AoI) | PMK Pedoman PIPK |
| 6 | **Keandalan dokumentasi PIPK** | Kertas kerja lengkap, tertelusur, ter-review berjenjang | PMK Pedoman PIPK |

## Format Unsur Temuan (KKSAR)

Catatan reviu **K/K/S/A** — **Kondisi** (kelemahan pengendalian: proses/kontrol + dokumen), **Kriteria** (PMK PIPK/PP 60/2008 + pasal, kutip **presisi**), **Sebab** (anti-mengarang), **Akibat** (risiko salah saji/keandalan pelaporan; **tanpa kerugian negara**). **Rekomendasi di LHR.** Doktrin: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan → Hasil Reviu (per aspek/level pengendalian) → Simpulan efektivitas PIPK (keyakinan terbatas) → Saran perbaikan. Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria untuk dibundel — lihat `references/README.md`)

Lihat [`references/README.md`](references/README.md) untuk daftar kriteria kandidat + status konfirmasi.

## Batasan

- Reviu = keyakinan terbatas atas simpulan PIPK entitas, **bukan** pengujian pengendalian menyeluruh oleh APIP; bukan opini.
- Kriteria PIPK teknis & dapat diperbarui → **konfirmasi versi PMK**; kriteria tak tersedia → catatan, bukan temuan.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-laporan-keuangan`, `reviu-pnbp`). PIPK menopang keandalan LK (kaitan dengan asersi LK); temuan kelemahan pengendalian material → dapat memicu pendalaman audit.
