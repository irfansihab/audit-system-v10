---
name: reviu-laporan-keuangan
jenis: Reviu Laporan Keuangan (LK Kementerian/Lembaga)
format_laporan: kksa
dasar-hukum: PMK Standar Reviu LK K/L (PMK 255/PMK.09/2015 jo. PMK 8/PMK.09/2019 — konfirmasi versi berlaku), PP 71/2010 (SAP), PP 8/2006
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.1"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT, perlu pengisian & validasi auditor senior.
---

# Skill: Reviu Laporan Keuangan (LK K/L)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP (bukan auditor penuh) yang melakukan **reviu atas Laporan Keuangan Kementerian/Lembaga** untuk memberi **keyakinan terbatas** bahwa LK disusun **sesuai Standar Akuntansi Pemerintahan (SAP)** dan sistem pengendalian intern memadai, **sebelum LK disampaikan** (ditandatangani Pernyataan Telah Direviu). Reviu **bukan audit** — tidak menyatakan opini, tidak menghitung kerugian negara; menelaah penyajian, pengungkapan, rekonsiliasi, dan kepatuhan proses. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **komponen LK** (LRA, Neraca, LO, LPE, CaLK; LAK/LPSAL untuk BUN) beserta **data dukung**: rekonsiliasi (SAKTI/SAIBA ↔ SPAN, internal, BMN/SIMAK-BMN, kas), Bagan Akun Standar, kertas kerja penyusunan, LK periode sebelumnya, dan LHP BPK/reviu terdahulu. Fakta ditarik dari digest dokumen yang diunggah; buka halaman sumber hanya untuk verifikasi angka/kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu (DRAFT — perlu pengisian & validasi auditor)

> Kerangka aspek di bawah adalah **rancangan awal**; kriteria pasti (nomor PMK/pasal) **wajib dikonfirmasi status berlakunya** oleh auditor sebelum dijadikan acuan (lihat Referensi). Setiap aspek dinilai per elemen: **Sesuai / Sesuai dengan catatan / Tidak sesuai**.

| # | Aspek | Yang dinilai | Kriteria acuan (kandidat) |
|---|-------|--------------|---------------------------|
| 1 | **Kesesuaian penyajian dengan SAP** | Struktur & pos LRA/Neraca/LO/LPE sesuai basis akrual | PP 71/2010 (SAP) + Buletin Teknis SAP |
| 2 | **Kelengkapan & keandalan CaLK** | Pengungkapan wajib (kebijakan akuntansi, rincian pos material, kejadian penting) | PP 71/2010 (PSAP CaLK) |
| 3 | **Rekonsiliasi** | SAKTI/SAIBA ↔ SPAN; internal; BMN (SIMAK); kas — tanpa selisih/suspend tak terjelaskan | PMK Sistem Akuntansi (SAKTI) + PMK penyusunan LK |
| 4 | **Akurasi saldo & klasifikasi akun** | Ketepatan akun (BAS), tidak ada suspend/salah klasifikasi material | PMK Bagan Akun Standar + Kebijakan Akuntansi Pempus |
| 5 | **Kepatuhan proses penyusunan** | Jadwal, reviu berjenjang, Pernyataan Telah Direviu | PMK Standar Reviu LK K/L |
| 6 | **Tindak lanjut temuan berdampak LK** | Koreksi atas temuan BPK/reviu terdahulu yang memengaruhi saldo/penyajian | LHP BPK + status TLHP |

## Format Unsur Temuan (KKSAR)

Catatan reviu direkam **K/K/S/A** — **Kondisi** (fakta: pos/angka/dokumen + rujukan), **Kriteria** (SAP/PMK + pasal, kutip **presisi** — lihat `panduan-format-umum`), **Sebab** (anti-mengarang: diisi bila terbukti; bila tidak → "Tidak ditemukan penyebab"/"Tidak cukup data"), **Akibat** (dampak pada keandalan/penyajian LK; **tanpa perhitungan kerugian negara**). **Rekomendasi disusun di LHR, bukan di KKP.** Doktrin unsur & Sebab: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan (dasar, tujuan, ruang lingkup, metodologi) → Hasil Reviu (per aspek) → Simpulan (keyakinan terbatas) → Saran/Rekomendasi → **Pernyataan Telah Direviu** (lampiran). Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria untuk dibundel — lihat `references/README.md`)

Daftar kriteria kandidat + status "perlu konfirmasi berlaku" ada di [`references/README.md`](references/README.md). Bundel dokumen kriteria di `references/` setelah divalidasi auditor.

## Batasan

- Reviu = **keyakinan terbatas**, bukan audit/opini; tidak menghitung kerugian negara.
- Kriteria akuntansi bersifat teknis & sering diperbarui → **konfirmasi versi PMK/Bultek terbaru** sebelum menilai; kriteria acuan tak tersedia → catatan/"tidak cukup data", bukan temuan.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-pipk`, `reviu-pnbp`). Berbeda dari `reviu-rka-kl` (perencanaan anggaran T+1) — LK menelaah **realisasi & penyajian keuangan** (ex-post). Indikasi penyimpangan material/kerugian → eskalasi ke audit.
