---
name: reviu-pnbp
jenis: Reviu Penerimaan Negara Bukan Pajak (PNBP)
format_laporan: kksa
dasar-hukum: UU 9/2018 (PNBP), PP turunan (tarif/pengelolaan/pemeriksaan PNBP), PP Jenis & Tarif PNBP pada Komdigi
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.1"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT, perlu pengisian & validasi auditor senior.
---

# Skill: Reviu Penerimaan Negara Bukan Pajak (PNBP)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP yang melakukan **reviu atas pengelolaan Penerimaan Negara Bukan Pajak (PNBP)** — menelaah **kesesuaian tarif, penetapan/penghitungan, penagihan, penyetoran ke kas negara, penggunaan (bila diizinkan), serta penatausahaan & pelaporan** PNBP dengan ketentuan. Memberi **keyakinan terbatas**; **bukan audit** (tidak menghitung kerugian negara, tidak menyatakan opini). Untuk Komdigi, objek PNBP dominan: **BHP frekuensi radio, IPFR, sertifikasi/perizinan**. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **data & dokumen PNBP** — target & realisasi PNBP, SK/penetapan tarif, dokumen penetapan PNBP terutang per wajib bayar, kartu piutang PNBP & umur piutang, bukti setor/SSBP (SIMPONI), izin & realisasi penggunaan PNBP, laporan & rekonsiliasi PNBP. Fakta ditarik dari digest; verifikasi ke sumber untuk angka/kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu (DRAFT — perlu pengisian & validasi auditor)

> Kerangka rancangan awal; kriteria pasti (UU/PP/PMK + pasal) **wajib dikonfirmasi berlaku** (terutama PP tarif spesifik Komdigi). Nilai per elemen: **Sesuai / Sesuai dengan catatan / Tidak sesuai**.

| # | Aspek | Yang dinilai | Kriteria acuan (kandidat) |
|---|-------|--------------|---------------------------|
| 1 | **Jenis & tarif PNBP** | Jenis dipungut sesuai ketetapan; tarif = PP tarif berlaku | UU 9/2018 + PP Jenis & Tarif PNBP Komdigi |
| 2 | **Penetapan/penghitungan PNBP terutang** | Akurasi hitung per wajib bayar; dasar pengenaan benar | UU 9/2018 + juknis penghitungan (mis. BHP/IPFR) |
| 3 | **Penagihan & piutang PNBP** | Penagihan tepat waktu; piutang tercatat, umur & penyisihan wajar | UU 9/2018 + PMK piutang PNBP |
| 4 | **Penyetoran ke Kas Negara** | Tepat **waktu** & **jumlah** ke kas negara (SIMPONI/SSBP) | UU 9/2018 + PMK penatausahaan PNBP |
| 5 | **Penggunaan PNBP** (bila diizinkan) | Sesuai izin penggunaan & proporsi/pagu | UU 9/2018 + KMK/PMK izin penggunaan PNBP |
| 6 | **Penatausahaan & pelaporan** | Pencatatan, rekonsiliasi, pelaporan PNBP akurat & lengkap | PMK penatausahaan/pelaporan PNBP |

## Format Unsur Temuan (KKSAR)

Catatan reviu **K/K/S/A** — **Kondisi** (fakta PNBP: nilai/wajib bayar/tanggal + dokumen), **Kriteria** (UU 9/2018/PP tarif/PMK + pasal, kutip **presisi**), **Sebab** (anti-mengarang), **Akibat** (risiko PNBP kurang pungut/terlambat setor/salah guna — **tanpa perhitungan kerugian negara**; indikasi kurang bayar signifikan → eskalasi audit). **Rekomendasi di LHR.** Doktrin: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan → Hasil Reviu (per aspek pengelolaan PNBP) → Simpulan (keyakinan terbatas) → Saran/Rekomendasi. Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria untuk dibundel — lihat `references/README.md`)

Lihat [`references/README.md`](references/README.md) untuk daftar kriteria kandidat + status konfirmasi.

## Batasan

- Reviu = keyakinan terbatas; tidak menghitung kerugian negara & tidak menetapkan kurang bayar final (ranah audit/pemeriksaan).
- **Tarif PNBP per-K/L sering diperbarui** → **konfirmasi PP tarif Komdigi terbaru**; kriteria tak tersedia → catatan/"tidak cukup data", bukan temuan.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-laporan-keuangan`, `reviu-pipk`). PNBP juga menjadi pos pendapatan di LK (kaitan dengan reviu LK). Indikasi kurang pungut/penyimpangan material → eskalasi ke audit.
