# Panduan Ekstraksi Kriteria — 5 Skill Umum

**Berlaku untuk:** audit-umum, reviu-umum, pemantauan-umum, evaluasi-umum, konsultansi-umum

---

## Tujuan

Skill umum bersifat **criteria-driven**: kriteria pengujian datang dari folder `input/kriteria/` yang diunggah auditor saat penugasan dimulai. Panduan ini menjelaskan cara skill mendeteksi, mengekstrak, dan mengindeks kriteria secara konsisten lintas 5 skill.

## Format Input yang Didukung

Skill harus mampu membaca **bebas-format** dari `input/kriteria/`:

| Ekstensi | Tools | Catatan |
|----------|-------|---------|
| `.pdf` | `pdftotext` (per CLAUDE.md, bukan Read tool) | Default untuk regulasi resmi |
| `.docx` | python-docx atau pandoc | Sering untuk rancangan/draft internal |
| `.xlsx` / `.xls` | openpyxl / pandas | Sering untuk matriks kriteria/LKE |
| `.txt` / `.md` | langsung baca | Catatan/ringkasan |
| `.csv` / `.tsv` | pandas | Daftar item terstruktur |
| `.html` | BeautifulSoup | Ekspor dari sistem internal |

**Untuk PDF berisi gambar (scan)**: jalankan OCR dulu (`ocrmypdf` atau setara). Catat di audit trail jika OCR diperlukan.

## Klasifikasi Kriteria

Setiap potongan kriteria diklasifikasi pada 3 dimensi:

### Dimensi 1: Tingkat Hierarki Hukum
| Level | Contoh | Kekuatan |
|-------|--------|----------|
| L1 - UUD | UUD 1945 | Tertinggi |
| L2 - UU/Perppu | UU 1/2004, UU 17/2003 | Mengikat seluruh K/L |
| L3 - PP | PP 60/2008 | Mengikat |
| L4 - Perpres | Perpres 16/2018 | Mengikat |
| L5 - Permen | PermenPAN-RB, Permen Komdigi | Mengikat sektoral |
| L6 - Perdirjen / Perka | Perlem LKPP | Mengikat operasional |
| L7 - SE / Surat | SE Menteri | Petunjuk |
| L8 - SOP / SK Internal | SK Sekjen, SOP unit | Mengikat internal |
| L9 - Pedoman / Juklak | Juknis evaluasi | Petunjuk operasional |

### Dimensi 2: Sifat
- **Mengikat** (kewajiban/larangan/syarat) — gunakan untuk pengujian kepatuhan
- **Indikatif** (panduan, best practice) — gunakan dengan hati-hati, bukan dasar temuan keras
- **Definisi** — kamus istilah, tidak diuji langsung tetapi digunakan untuk interpretasi

### Dimensi 3: Tipe Pasal/Butir
- **Substantif** — apa yang harus dilakukan/tidak dilakukan
- **Prosedural** — bagaimana melakukannya, urutan, format
- **Sanksi** — konsekuensi pelanggaran
- **Lain** — definisi, ketentuan peralihan, dst

## Format Matriks Kriteria Internal

Setelah ekstraksi, susun **Matriks Kriteria** sebagai sheet di KKA/KKR/KKE/KKM/KKK. Format kolom standar:

| Kolom | Isi | Wajib? |
|-------|-----|--------|
| `id` | K01, K02, ... (incremental) | ✅ |
| `sumber` | Nama dokumen + tahun (contoh: "PP 60/2008") | ✅ |
| `pasal_butir` | Pasal X ayat Y / Butir Z | ✅ |
| `kutipan` | Teks pasal/butir lengkap (≤500 char per kutipan) | ✅ |
| `level_hierarki` | L1–L9 | ✅ |
| `sifat` | mengikat/indikatif/definisi | ✅ |
| `tipe` | substantif/prosedural/sanksi/lain | ✅ |
| `aspek_terkait` | tag aspek pengawasan (perencanaan/pelaksanaan/keuangan/dll) | ✅ |
| `relevansi_skill` | tag skill (audit/reviu/pemantauan/evaluasi/konsultansi) | Opsional |
| `catatan_auditor` | catatan/justifikasi tambahan dari auditor | Opsional |
| `file_sumber` | nama file di `input/kriteria/` | ✅ |
| `halaman` | hal. n PDF / sel cell jika xlsx | ✅ |

## Algoritma Ekstraksi (Pseudocode)

```
FOR setiap file di input/kriteria/:
  1. Deteksi tipe (ekstensi + magic bytes)
  2. Ekstrak teks (pdftotext / docx2txt / openpyxl)
  3. Identifikasi tipe dokumen:
     - Cocokkan judul vs pola: "UU NOMOR X TAHUN Y", "PERATURAN MENTERI", "STANDAR OPERASIONAL", "LEMBAR KERJA EVALUASI", dst
  4. Untuk dokumen regulasi:
     - Parse struktur: BAB → Pasal → Ayat
     - Setiap Pasal/Ayat = 1 entri kriteria kandidat
  5. Untuk LKE/instrumen:
     - Parse baris/kolom matriks
     - Setiap baris kriteria = 1 entri
  6. Untuk SOP/Juklak:
     - Parse heading → langkah/aturan
     - Setiap aturan WAJIB/HARUS/DILARANG = 1 entri
  7. Klasifikasi tiap entri (level/sifat/tipe)
  8. Tambahkan ke matriks_kriteria.xlsx di _KKP/

OUTPUT: _KKP/matriks-kriteria.xlsx + _KKP/kriteria.json
```

## Ringkasan Ekstraksi Kriteria

Setelah ekstraksi, susun ringkasan kriteria berikut (kapan & bagaimana dikonfirmasi ke auditor diatur **orkestrator**, bukan skill):

```
Ringkasan Kriteria yang Diekstrak:
- Total file: N
- Total entri kriteria: M (mengikat: x, indikatif: y, definisi: z)
- Distribusi level: L2=…, L3=…, L4=…, L5=…
- Aspek terdeteksi: [perencanaan: a, pelaksanaan: b, …]
- File yang tidak dapat di-parse otomatis: [daftar — perlu verifikasi manual auditor]
```

Kelengkapan/ketepatan matriks kriteria dikonfirmasi ke auditor sesuai alur orkestrator sebelum dipakai untuk pengujian.

## Aturan Pemilihan Kriteria untuk Pengujian

Tidak semua kriteria yang diekstrak akan dipakai. Pilih kriteria untuk pengujian dengan aturan:

- **Selalu pakai**: L2-L4 (UU, PP, Perpres) yang relevan dengan objek
- **Pakai jika spesifik**: L5-L6 yang spesifik untuk objek
- **Pakai dengan hati-hati**: L7 (SE) — sebagai konfirmasi, bukan dasar utama temuan keras
- **Pakai sebagai konteks**: L8 (SOP) — jika auditan WAJIB menerapkan SOP-nya sendiri
- **Hanya rujukan**: L9 (Pedoman) — untuk best practice, bukan dasar temuan kepatuhan

## Konflik antar Kriteria

Jika dua kriteria saling bertentangan (mis. SOP internal lebih ketat/kendur dari Permen), terapkan **lex superior**:

1. Hierarki hukum lebih tinggi mengalahkan yang lebih rendah (L2 > L3 > … > L9)
2. Yang lebih khusus mengalahkan yang lebih umum (lex specialis derogat lex generalis)
3. Yang lebih baru mengalahkan yang lebih lama (lex posterior derogat lex priori)

Dokumentasikan keputusan konflik di kolom `catatan_auditor`.

## Penyimpanan & Audit Trail

Untuk setiap penugasan:

```
_KKP/
├── matriks-kriteria.xlsx    # Hasil ekstraksi terstruktur
├── kriteria.json            # Versi JSON untuk audit trail
└── audit-trail-ekstraksi.md # Log: file apa, kapan diparse, hasil
```

## Referensi Skill yang Sudah Punya Kriteria Built-in

Jika kriteria yang dibutuhkan sudah ada di skill spesifik, **gunakan skill spesifik** alih-alih skill umum:

- Pengadaan Barang/Jasa → `audit-pengadaan`, `reviu-pengadaan`, `pemantauan-pengadaan`, `konsultasi-pengadaan`
- RKA-K/L → `reviu-rka-kl`
- SAKIP / Kinerja → `evaluasi-sakip`, `audit-kinerja`
- SPIP / MR → `evaluasi-spip`, `evaluasi-manajemen-risiko`
- Reformasi Birokrasi → `evaluasi-reformasi-birokrasi`

Skill umum melengkapi, bukan menggantikan skill spesifik.
