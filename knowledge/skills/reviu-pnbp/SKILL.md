---
name: reviu-pnbp
jenis: Reviu Penerimaan Negara Bukan Pajak (PNBP)
format_laporan: kksa
dasar-hukum: UU 9/2018 (PNBP); PP 43/2023 (Jenis & Tarif PNBP Kominfo/Komdigi, ganti PP 80/2015); PMK 155/PMK.02/2021 jo. PMK 58/2023 (Tata Cara Pengelolaan PNBP); Permen Kominfo 1/2024 (Tarif Rp0/0%); PP 58/2020 (Pengelolaan PNBP) & PP 1/2021 (Pemeriksaan PNBP)
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.2"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT.
  - v0.2 (2026-07-09): **Kriteria RIIL dibundel** — PP 43/2023, PMK 155/2021 jo. PMK 58/2023, Permen Kominfo 1/2024 dikonfirmasi & diringkas ke `references/` (+ PDF PP 43/PMK 58/Permen 1). Aspek/checklist diikat ke pasal spesifik (jatuh tempo Ps. 41, piutang Ps. 42, rekonsiliasi Ps. 135, tarif nol Permen 1/2024). RAGU `kriteria` PNBP tertutup. (Validasi golden/fixture auditor tetap menyusul.)
---

# Skill: Reviu Penerimaan Negara Bukan Pajak (PNBP)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP yang melakukan **reviu atas pengelolaan Penerimaan Negara Bukan Pajak (PNBP)** — menelaah **kesesuaian tarif, penetapan/penghitungan, penagihan, penyetoran ke kas negara, penggunaan (bila diizinkan), serta penatausahaan & pelaporan** PNBP dengan ketentuan. Memberi **keyakinan terbatas**; **bukan audit** (tidak menghitung kerugian negara, tidak menyatakan opini). Untuk Komdigi, objek PNBP dominan: **BHP frekuensi radio, IPFR, sertifikasi/perizinan**. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **data & dokumen PNBP** — target & realisasi PNBP, SK/penetapan tarif, dokumen penetapan PNBP terutang per wajib bayar, kartu piutang PNBP & umur piutang, bukti setor/SSBP (SIMPONI), izin & realisasi penggunaan PNBP, laporan & rekonsiliasi PNBP. Fakta ditarik dari digest; verifikasi ke sumber untuk angka/kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu

> Kriteria inti sudah **dibundel & bernomor** di [`references/`](references/) — kutip **presisi** (nomor + pasal). Untuk BHP frekuensi/IPFR pakai **formula PP 43/2023 Pasal 3/10**. Nilai per elemen: **Sesuai / Sesuai dengan catatan / Tidak sesuai**. Bila versi berlaku suatu kriteria tak dapat dipastikan untuk periode objek → "perlu konfirmasi berlaku", bukan deviasi terkonfirmasi.

| # | Aspek | Yang dinilai | Kriteria acuan (bernomor) |
|---|-------|--------------|---------------------------|
| 1 | **Jenis & tarif PNBP** | Jenis dipungut termasuk daftar; tarif/formula = PP berlaku | **PP 43/2023** Ps. 1–3, 10 (BHP ISR/IPFR) + **Permen Kominfo 1/2024** (tarif Rp0/0%) |
| 2 | **Penetapan/penghitungan PNBP terutang** | Akurasi hitung per wajib bayar; formula/variabel benar | **PP 43/2023** Ps. 3 (formula ISR) / Ps. 10 (IPFR) + **PMK 155/2021 jo. 58/2023** Ps. 59–60 |
| 3 | **Penagihan & piutang PNBP** | Bayar ≤ jatuh tempo; tunggakan → piutang, umur & penyisihan wajar | **PMK 155/2021 jo. 58/2023** Ps. 41 (jatuh tempo), Ps. 42 (→ Piutang), Ps. 55A (optimalisasi piutang) |
| 4 | **Penyetoran ke Kas Negara** | Tepat **waktu** & **jumlah** (SIMPONI/SSBP) | **UU 9/2018** (payung: setor ke Kas Negara) + **PMK 155/2021** (pembayaran/penyetoran) |
| 5 | **Penggunaan Dana PNBP** (bila diizinkan) | Sesuai izin & **Pagu Penggunaan Dana PNBP** | **PMK 155/2021 jo. 58/2023** (penggunaan dana PNBP, Ps. 108 dst) + KMK/PMK izin penggunaan |
| 6 | **Penatausahaan & pelaporan** | Pencatatan, **rekonsiliasi**, pelaporan akurat & lengkap | **PMK 155/2021** (penatausahaan & pelaporan) Ps. 135 (rekonsiliasi triwulanan) |

### Checklist Reviu PNBP (per aspek — wajib ditelusuri; nilai per elemen: Sesuai / Sesuai dgn catatan / Tidak sesuai)

**Aspek 1 — Jenis & tarif:** jenis PNBP yang dipungut termasuk **daftar PP 43/2023 Ps. 1(1)** (BHP frekuensi, sertifikasi/pengujian alat telekomunikasi, pos, telekomunikasi, penyiaran, SPBE, dll); **tarif/formula = PP 43/2023** (ISR Ps. 3, IPFR Ps. 10). Memakai **PP 80/2015 (sudah dicabut)** atau tarif di luar ketetapan → catatan. Tarif **Rp0/0%** hanya sah bila memenuhi **Permen Kominfo 1/2024** (jenis Ps. 2 + persyaratan).

**Aspek 2 — Penetapan/penghitungan terutang:** akurasi penghitungan PNBP terutang **per wajib bayar** (dasar pengenaan, formula BHP/IPFR benar); tidak ada **kurang hitung/kurang pungut**.

**Aspek 3 — Penagihan & piutang:** pembayaran **≤ jatuh tempo (PMK 155/2021 Ps. 41)**; tunggakan **wajib dicatat sebagai Piutang PNBP (Ps. 42)** — **umur (aging)** dianalisis, **penyisihan** wajar; potensi kurang bayar → **optimalisasi penyelesaian piutang (Ps. 55A, PMK 58/2023)** sebelum hasil verifikasi; tunggakan lama tanpa upaya tagih → catatan.

**Aspek 4 — Penyetoran ke Kas Negara:** setor **tepat waktu & tepat jumlah** (SSBP via **SIMPONI**); **tidak ada PNBP mengendap** di bendahara/rekening di luar kas negara; kesesuaian tanggal pungut vs setor.

**Aspek 5 — Penggunaan PNBP** (bila objek ber-izin guna): penggunaan **sesuai izin (KMK/PMK)** & **proporsi/pagu**; tidak dipakai di luar peruntukan.

**Aspek 6 — Penatausahaan & pelaporan:** pencatatan & **rekonsiliasi PNBP** (unit ↔ SIMPONI ↔ LK) akurat; realisasi PNBP di LRA/LO konsisten.

> Tiap elemen **tidak sesuai** → catatan **K/K/S/A** (Kondisi = fakta PNBP: nilai/wajib bayar/tanggal + dokumen; Kriteria kutip **presisi** UU 9/2018 / PP 43/2023 / PMK 155/2021 jo. 58/2023 / Permen Kominfo 1/2024 + pasal; Sebab anti-mengarang; Akibat = risiko kurang pungut/terlambat setor/salah guna — **tanpa** menghitung kerugian negara; **indikasi kurang bayar material → eskalasi audit**). Elemen sesuai → "telah memenuhi". Bila versi berlaku suatu PP/PMK tak dapat dipastikan untuk periode objek → catatan/"tidak cukup data", bukan deviasi terkonfirmasi.

## Format Unsur Temuan (KKSAR)

Catatan reviu **K/K/S/A** — **Kondisi** (fakta PNBP: nilai/wajib bayar/tanggal + dokumen), **Kriteria** (UU 9/2018/PP tarif/PMK + pasal, kutip **presisi**), **Sebab** (anti-mengarang), **Akibat** (risiko PNBP kurang pungut/terlambat setor/salah guna — **tanpa perhitungan kerugian negara**; indikasi kurang bayar signifikan → eskalasi audit). **Rekomendasi di LHR.** Doktrin: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan → Hasil Reviu (per aspek pengelolaan PNBP) → Simpulan (keyakinan terbatas) → Saran/Rekomendasi. Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria dibundel — lihat [`references/`](references/))

Kriteria inti sudah **dibundel & bernomor**:
- [`01-pp-43-2023-jenis-tarif-pnbp-komdigi.md`](references/01-pp-43-2023-jenis-tarif-pnbp-komdigi.md) (+ PDF) — jenis & tarif/formula.
- [`02-pmk-155-2021-jo-58-2023-pengelolaan-pnbp.md`](references/02-pmk-155-2021-jo-58-2023-pengelolaan-pnbp.md) (+ PDF PMK 58) — perencanaan → penetapan → jatuh tempo → piutang → penatausahaan.
- [`03-permen-kominfo-1-2024-tarif-nol-pnbp.md`](references/03-permen-kominfo-1-2024-tarif-nol-pnbp.md) (+ PDF) — tarif Rp0/0%.
- [`README.md`](references/README.md) — daftar lengkap + status; PMK piutang/penggunaan tambahan bila diperlukan auditor.

## Batasan

- Reviu = keyakinan terbatas; tidak menghitung kerugian negara & tidak menetapkan kurang bayar final (ranah audit/pemeriksaan).
- **Tarif PNBP per-K/L dapat diperbarui** → gunakan **PP 43/2023 jo. Permen Kominfo 1/2024** untuk periode berlaku; bila periode objek di luar rentang berlaku suatu regulasi → catatan/"tidak cukup data", bukan temuan.
- Nama K/L di regulasi = **"Komunikasi dan Informatika" (Kominfo)**; kini **Komdigi**. Kutip nama sesuai teks; jangan ubah.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-laporan-keuangan`, `reviu-pipk`). PNBP juga menjadi pos pendapatan di LK (kaitan dengan reviu LK). Indikasi kurang pungut/penyimpangan material → eskalasi ke audit.
