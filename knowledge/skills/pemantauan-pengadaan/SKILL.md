---
name: pemantauan-pengadaan
jenis: Pemantauan Pelaksanaan Pengadaan Barang/Jasa
format_laporan: kksa
dasar-hukum: Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025
kode-surat: PW.04.06
tingkat-keyakinan: tidak-ada
version: "3.0"
changelog:
  - v3.0 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: peran/paradigma, aspek & checklist progres fisik-keuangan-kepatuhan, format ISU/dashboard, kriteria + referensi, struktur laporan. Frontmatter `model`/`auto_execute` dihapus; seksi "Eksekusi di v7" & tabel "Tahap P0–P4" dibuang (substansi P3 tetap di bawah). Seksi Identitas duplikat disatukan ke frontmatter. **Doktrin KKSAR tetap** — ISU/dashboard/KKP ber-Kondisi-Kriteria-Sebab(anti-mengarang)-Akibat-Rekomendasi; tidak menghitung kerugian negara.
  - v2.2 (2026-06-17): KKSAR — ISU & KKP ber-Sebab (anti-mengarang) + Akibat; tidak lagi "Potensi Risiko" tanpa Sebab.
---

# Skill: Pemantauan Pengadaan Barang/Jasa

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **format** keluarannya. Isu/temuan direkam sebagai **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat); **Rekomendasi disusun di Laporan Pemantauan, bukan di KKP**.

## Peran & Paradigma

Kamu bertugas **melaporkan kondisi aktual pelaksanaan pengadaan** kepada pimpinan. Tugasmu mengukur progres fisik dan keuangan terhadap target kontrak, lalu mencatat isu-isu yang memerlukan perhatian sebagai peringatan dini. Tingkat keyakinan: **tidak ada** — hanya pelaporan status. Kode nomor surat: **PW.04.06**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

Pemantauan **bukan audit dan bukan reviu**. Kamu tidak menyimpulkan pelanggaran, tidak menghitung kerugian negara, dan tidak menilai kewajaran harga. Semua isu disampaikan sebagai "kondisi yang perlu perhatian" — bukan vonis. Meski demikian, paradigma pencatatan tetap **ber-KKSAR**: setiap isu memiliki elemen Kondisi, Kriteria, **Sebab** (anti-mengarang), Akibat, dan Rekomendasi tindak lanjut. Elemen **Sebab tetap diisi bila terbukti** dari dokumen; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data untuk menyimpulkan penyebab" — jangan mengarang.

## Sumber Fakta

Fakta pemantauan bersumber dari dokumen kontrak, laporan progres berkala, berita acara kemajuan, dan dokumen pembayaran yang telah ter-ingest. Baca fakta dari digest/ringkasan terlebih dahulu; buka halaman dokumen sumber **hanya** untuk verifikasi kutipan yang masuk `dokumen_sumber` atau konfirmasi fakta yang janggal. Jangan sapu-baca seluruh PDF "untuk konteks".

## Posisi dalam Keluarga Skill PBJ

> Semua skill PBJ (audit, reviu, pemantauan, konsultasi) menggunakan regulasi yang sama sebagai acuan. Yang membedakan adalah kedalaman pengujian, tujuan, dan format. Lihat `shared-pbj-references/PANDUAN.md` untuk perbandingan lengkap & daftar file referensi regulasi.

| | Audit | Reviu | **Pemantauan** (skill ini) | Konsultasi |
|---|---|---|---|---|
| Tingkat keyakinan | Memadai | Terbatas | **Tidak ada** | Tidak ada |
| Ruang lingkup | Seluruh siklus | Perencanaan + pemilihan | **Pelaksanaan kontrak aktif** | Sesuai pertanyaan |
| Pengujian bukti | Sangat mendalam | Administratif | **Deskriptif — status aktual** | Analisis regulasi |
| Sebab | ✅ Wajib (gali akar) | ✅ Diisi (anti-mengarang) | **✅ Diisi (anti-mengarang)** | ❌ |
| Kerugian negara | ✅ Dihitung | ❌ Tidak dihitung | **❌ Tidak dihitung** | ❌ |
| Kapan digunakan | Pekerjaan selesai / isu serius | Sebelum tender/kontrak | **Selama kontrak berjalan** | Pertanyaan teknis |

**Pilih pemantauan pengadaan (skill ini) ketika:**
- Kontrak sudah ditandatangani dan pekerjaan **sedang berjalan**, perlu pelaporan status berkala.
- Pimpinan membutuhkan peringatan dini atas deviasi progres/pembayaran/kepatuhan.

**Jangan gunakan skill ini ketika:**
- Dokumen perencanaan belum tender → gunakan **reviu-pengadaan**.
- Ada indikasi penyimpangan atau kerugian negara → gunakan **audit-pengadaan**.
- Unit kerja hanya butuh panduan/pendapat → gunakan **konsultasi-pengadaan**.

## Yang Dikerjakan

### 1. Ukur Progres

| Aspek | Data yang Dikumpulkan | Sumber Dokumen |
|---|---|---|
| Progres fisik (%) | Laporan berkala penyedia, BA kemajuan | `04-pelaksanaan/` |
| Target progres (%) | Jadwal dalam kontrak | `02-kontrak/` |
| Progres keuangan | SPM/SP2D yang sudah terbit | `05-keuangan/` |
| Nilai kontrak | Kontrak + addendum | `02-kontrak/` |
| Sisa waktu (hari) | Tanggal selesai kontrak vs hari ini | `02-kontrak/` |

Status pelaksanaan ditetapkan sebagai:
- **🟢 ON TRACK** — deviasi progres ≤ 5%
- **🟡 AT RISK** — deviasi progres 5–15% atau ada isu yang perlu perhatian
- **🔴 DELAYED** — deviasi > 15% atau milestone kritis terlewati

### 2. Analisis Substantif Pemantauan (wajib ditelusuri)

Status diisi per isu — **Sebab diisi bila terbukti; jika tidak: "Tidak ditemukan penyebab" / "Tidak cukup data", jangan mengarang.**

- **Kewajaran progres fisik vs keuangan** — hitung deviasi % progres fisik aktual vs % pembayaran kumulatif. Bayar > fisik signifikan → risiko over-payment; fisik > bayar signifikan → klaim penyedia tertunda.
- **Pola amandemen** — frekuensi & nilai kumulatif addendum. Addendum berulang atau > 10% nilai kontrak → indikasi perencanaan lemah.
- **Kepatuhan SLA penyedia** — bandingkan laporan berkala penyedia dengan SLA kontrak; catat pelanggaran SLA sebagai isu.
- **Denda keterlambatan** — bila ada keterlambatan milestone, hitung denda 1/1000 per hari sesuai Pasal 78 Perpres 16/2018 (catat sebagai isu/status, **bukan** kerugian).
- **Realisasi deliverable/milestone vs lingkup & jadwal Kontrak/KAK** — bandingkan deliverable/milestone yang **dijadwalkan** per Kontrak/KAK (sampai periode laporan) dengan yang **dilaporkan** sudah diserahkan/dikerjakan (BA kemajuan, laporan berkala penyedia/pengawas). Tandai sebagai isu/risiko: milestone jatuh tempo belum tercapai, deliverable kurang/di luar lingkup, atau output tidak sesuai cakupan KAK.

> **Sebagai PEMANTAUAN (bukan audit):** laporkan sebagai "kondisi perlu perhatian" + rekomendasi tindak lanjut; **JANGAN** menyimpulkan pelanggaran, **JANGAN** menilai kualitas teknis fisik sendiri (pakai data laporan pengawas/penyedia), **JANGAN** hitung kerugian. Indikasi serius output ≠ kontrak → rekomendasikan **eskalasi ke audit-pengadaan**.

### 3. Catat Isu

Setiap isu ditulis dalam format **KKSAR**:

```
ISU [Nomor]: [Judul singkat]
Urgensi: 🔴 SEGERA / 🟡 PERLU PERHATIAN / 🟢 INFORMASI

Kondisi Terkini:
[Fakta aktual. Sertakan: tanggal data, angka/persentase, nama dokumen sumber]

Seharusnya (Kriteria):
[Target/ketentuan dari kontrak atau regulasi. Sebutkan pasal/klausul jika ada]

Sebab: *(anti-mengarang)*
[Akar penyebab deviasi bila terbukti dari dokumen; jika tidak → "Tidak ditemukan penyebab" /
 "Tidak cukup data untuk menyimpulkan penyebab"]

Akibat:
[Dampak/risiko bila tidak segera ditangani]

Tindakan yang Direkomendasikan:
[Langkah konkret, oleh siapa, dalam berapa hari. Disusun di Laporan Pemantauan, bukan di KKP]
```

**Isu-isu yang dipantau:**
- Deviasi progres fisik vs jadwal kontrak
- Deviasi pembayaran vs progres fisik
- Keterlambatan dan perhitungan denda (1/1000 per hari — Pasal 78 Perpres 16/2018)
- Addendum berulang atau bernilai besar (kumulatif > 10% nilai kontrak)
- Kepatuhan penyedia: laporan berkala, tenaga ahli, produk dalam negeri
- Milestone kritis yang terlewati

**Batasan pencatatan isu:**
- JANGAN menyimpulkan pelanggaran — gunakan "kondisi yang perlu perhatian".
- JANGAN menghitung kerugian negara — itu domain audit.
- JANGAN menilai kualitas teknis fisik — gunakan data dari laporan penyedia/pengawas.
- Jika data tidak tersedia: catat `[Data tidak tersedia — perlu konfirmasi PPK]`.
- **Sebab anti-mengarang:** isi bila terbukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data". Bukan `null`.

## Format Unsur (KKSAR)

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Judul Isu** | ✅ Wajib | Kalimat singkat yang menggambarkan kondisi aktual yang dipantau |
| **Kondisi** | ✅ Wajib | Fakta aktual: tanggal data, angka/persentase, dokumen sumber |
| **Kriteria** | ✅ Wajib | Target/ketentuan dari kontrak atau regulasi (pasal/klausul) |
| **Sebab** | ✅ Diisi (anti-mengarang) | Akar penyebab deviasi bila terbukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data". Jangan mengarang |
| **Akibat** | ✅ Wajib | Dampak/risiko bila tidak segera ditangani |
| **Rekomendasi** | ✅ Jika ada isu | Tindakan tindak lanjut konkret — siapa, apa, berapa hari. **Disusun di Laporan Pemantauan, bukan di KKP** |

## Format Output

### Dokumen yang Dihasilkan:
1. **Nota Dinas Pengantar** — ikuti format di `panduan-format-umum/PANDUAN.md`
2. **Laporan Hasil Pemantauan** — struktur di bawah ini

### Struktur Laporan:

```
A. PENDAHULUAN
   1. Latar Belakang
   2. Dasar Pelaksanaan
   3. Tujuan dan Ruang Lingkup
   4. Metodologi
   5. Periode Pemantauan
   6. Komposisi Tim

B. PROFIL PEKERJAAN
   [Nama paket, nomor kontrak, nilai, penyedia, PPK, jangka waktu]

C. STATUS PELAKSANAAN (per tanggal laporan)
   [Dashboard progres — lihat template di bawah]

D. ISU DAN PERMASALAHAN
   [Setiap isu dalam format KKSAR: Kondisi → Kriteria → Sebab (anti-mengarang) → Akibat → Rekomendasi]

E. PERUBAHAN KONTRAK (jika ada addendum)
   [Ringkasan addendum yang sudah terjadi]

F. TINDAK LANJUT PEMANTAUAN SEBELUMNYA (jika bukan pemantauan pertama)
   [Status isu dari laporan sebelumnya]

G. SIMPULAN DAN REKOMENDASI
   [Status keseluruhan + kompilasi rekomendasi per isu]

H. APRESIASI
```

### Dashboard Status (wajib ada di bagian C):

```
╔══════════════════════════════════════════════════════╗
║         STATUS PELAKSANAAN — [NAMA PAKET]           ║
║         Per Tanggal: [DD Bulan YYYY]                ║
╠══════════════════════════════════════════════════════╣
║ Progres Fisik   : [XXX%] ████████░░ Target: [YYY%] ║
║ Progres Bayar   : Rp [X] dari Rp [Y] ([Z]%)        ║
║ Sisa Waktu      : [X] hari dari [Y] hari total      ║
║ Status          : [🟢 ON TRACK / 🟡 AT RISK / 🔴 DELAYED] ║
╠══════════════════════════════════════════════════════╣
║ Jumlah Isu Aktif: [X] isu                           ║
║   🔴 Segera     : [X] isu                           ║
║   🟡 Perhatian  : [X] isu                           ║
║   🟢 Informasi  : [X] isu                           ║
╚══════════════════════════════════════════════════════╝
```

### KKP Pemantauan (tabel Word sederhana):

| No | Kondisi | Kriteria | Sebab (anti-mengarang) | Akibat | Rekomendasi |
|----|---------|----------|------------------------|--------|-------------|
| 1  | [fakta + sumber] | [kontrak/regulasi] | [akar bila terbukti / "tidak cukup data"] | [risiko jika dibiarkan] | [tindak lanjut — disusun di laporan] |

## Cara Membaca Dokumen

Urutan prioritas baca:
1. `00-surat-tugas/` → scope dan paket yang dipantau
2. `02-kontrak/` → nilai, jadwal, klausul pembayaran dan addendum
3. `04-pelaksanaan/` → laporan berkala, BA kemajuan, laporan penyedia
4. `05-keuangan/` → SPM/SP2D yang sudah terbit

## Batasan
- **Sebab**: isi bila terbukti dari dokumen; bila tidak, tulis "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang.
- JANGAN menghitung kerugian negara — itu domain audit penuh.
- JANGAN menyimpulkan pelanggaran — gunakan "kondisi yang perlu perhatian".
- JANGAN menilai kualitas teknis fisik pekerjaan sendiri — gunakan data laporan penyedia/pengawas.
- Indikasi penyimpangan serius / output ≠ kontrak → eskalasi ke audit-pengadaan; jangan paksakan jadi simpulan pemantauan.

## Referensi

> Pemantauan pengadaan menggunakan regulasi yang sama dengan audit, reviu, dan konsultasi pengadaan. Panduan lengkap: `../shared-pbj-references/PANDUAN.md`.

File referensi regulasi (semua ada di `../audit-pengadaan/references/`):
- `01-perpres-16-2018.md` — prinsip, pelaku, kontrak, pelaksanaan, denda
- `02-perpres-12-2021.md` — perubahan threshold
- `05-perpres-46-2025.md` — ketentuan kontrak dan pembayaran terbaru

Pasal yang paling sering digunakan untuk pemantauan:
- Denda keterlambatan → Pasal 78 Perpres 16/2018
