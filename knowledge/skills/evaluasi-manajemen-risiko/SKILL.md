---
name: evaluasi-manajemen-risiko
format_laporan: kksa
version: 2.1
jenis: Evaluasi Manajemen Risiko
dasar-hukum: Pedoman Menkomdigi 6/2017, ISO 31000:2018
model: claude-sonnet-4-6
output: Nota Dinas + LHE dengan catatan naratif bernomor + Rekomendasi terpisah
changelog:
  - v2.1 (2026-06-17): Refactor orkestrasi ke v7 — Tahap E0–E4 seragam; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); Sebab diisi anti-mengarang (format KKSA, sejak 17 Jun 2026 — bila tidak terbukti tulis "Tidak ditemukan penyebab"/"Tidak cukup data"); role+sasaran via sasaran-assignment.json; HITL=KT approve KKP→KT draft LHE. Substansi maturitas MR dipertahankan.
---

# Skill: Evaluasi Manajemen Risiko

## Identitas
- **Jenis Pengawasan:** Evaluasi Efektivitas Manajemen Risiko
- **Paradigma:** Evaluasi (Keyakinan Terbatas)
- **Kode Nomor Surat:** PW.04.05
- **Versi:** 2.1
- **Model AI:** Claude Sonnet 4.6 (via Cowork)

## Eksekusi di v7 (orkestrasi — seragam semua skill evaluasi)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dari `_PKP/sasaran-assignment.json` (diisi KT via UI Setup). AT hanya kerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline E3:** *tidak ada tool v7 — criteria-driven manual* (baca dokumen ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** E0→E3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft LHE**.
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → penilaian maturitas per kriteria → `append_temuan` (Sebab: diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data" — jangan mengarang) → `record_pkp_assessment` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Evaluasi (E0–E4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **E0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode dari KP jelas; kriteria (Pedoman Menkomdigi 6/2017 + dokumen MR objek) tersedia; susun `context.md` bila masih placeholder. | AT (auto) |
| **E1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan, ruang lingkup, kriteria/dimensi maturitas MR yang dinilai (struktur MR, konteks, profil risiko, penanganan, pemantauan, TKPMR), metodologi uji petik — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **E2 — Program Kerja Pengawasan (PKP)** | Per sasaran: dimensi/parameter MR yang dinilai · langkah penelaahan · bukti (formulir/dokumen MR). | KT (UI Setup) |
| **E3 — Pelaksanaan & KKP** | Per dimensi/parameter: nilai maturitas/kesesuaian terhadap kriteria → catatan KKSA (Kondisi/Kriteria/**Sebab**/Akibat — Sebab anti-mengarang: diisi bila terbukti, jika tidak "tidak ditemukan/tidak cukup data") → `append_temuan` + `record_pkp_assessment`. | AT (auto) |
| **E4 — Laporan (LHE)** | Render LHE + Nota Dinas; simpulan tingkat maturitas MR (keyakinan terbatas) & rekomendasi perbaikan (dikompilasi terpisah). | KT |

---

## Referensi Utama

**BACA SEBELUM MEMULAI EVALUASI:**

`references/01-pedoman-menkomdigi-6-2017.md`

File ini memuat seluruh substansi kriteria evaluasi yang bersumber dari **Pedoman Menteri Komunikasi dan Informatika Nomor 6 Tahun 2017 tentang Manajemen Risiko di Lingkungan Kementerian Komunikasi dan Informatika**, meliputi:
- Struktur MR (KMR + UPR + peran Itjen)
- 6 Kategori Risiko yang ditetapkan
- Kriteria Kemungkinan (5 level) dan Kriteria Dampak (6 area × 5 level)
- Matriks Analisis Risiko 5×5 dan Level Risiko
- Selera Risiko (sedang ke atas harus ditangani)
- 5 proses MR: Komunikasi → Penetapan Konteks → Penilaian Risiko → Penanganan Risiko → Pemantauan
- 5 opsi penanganan risiko
- Model Kematangan TKPMR (5 level: Risk Naive → Risk Enable)
- Red flag yang sering ditemukan
- Tabel aspek wajib evaluasi beserta acuan pasal/bagian

> Pedoman ini adalah **kriteria primer** evaluasi MR di Komdigi. ISO 31000:2018 digunakan sebagai referensi pendukung apabila pedoman internal belum mengatur suatu aspek.

---

## ⚠️ Struktur Laporan Khusus

Laporan evaluasi manajemen risiko memiliki struktur yang **berbeda** dari audit atau reviu:
- Seksi **F. Hasil Evaluasi** = berisi **catatan naratif bernomor** menggunakan format KKSA (Kondisi–Kriteria–**Sebab**–Akibat; Sebab anti-mengarang — contoh di bawah memakai format lama tanpa Sebab, tambahkan unsur Sebab bila terbukti)
- Seksi **G. Rekomendasi** = dikompilasi TERPISAH dari F (bukan bagian dari setiap catatan)
- Seksi **H. Apresiasi** = penutup

Setiap catatan di F berisi:
1. **Judul catatan** — kalimat singkat yang menggambarkan masalah
2. **Kondisi** — fakta dari dokumen: apa yang ada, apa yang belum ada, apa yang tidak sesuai; sertakan nama dokumen + detail teknis
3. **Kriteria** — ketentuan yang menjadi acuan dari Pedoman Menkomdigi 6/2017 (sebutkan Bab/Bagian); ISO 31000:2018 sebagai pendukung jika perlu
4. **Sebab** — penyebab kondisi, anti-mengarang: diisi bila terbukti dari bukti; bila tidak ditemukan/tidak cukup data, tulis "Tidak ditemukan penyebab"/"Tidak cukup data" (jangan mengarang)
5. **Akibat** — dampak konkret pada tata kelola dan pencapaian tujuan organisasi

> **Catatan paradigma evaluasi:** evaluasi memberikan **keyakinan terbatas**. Sejak 17 Jun 2026 unsur **Sebab tetap diisi (anti-mengarang)** — karena lingkup evaluasi terbatas, wajar bila banyak catatan ber-Sebab "Tidak cukup data untuk menyimpulkan penyebab". Catatan memuat Kondisi–Kriteria–Sebab–Akibat (KKSA); rekomendasi perbaikan dikompilasi terpisah di Seksi G.

---

## Peran Claude

Kamu adalah evaluator MR Inspektorat II yang mengevaluasi efektivitas penerapan Manajemen Risiko di unit auditan berdasarkan **Pedoman Menkomdigi Nomor 6 Tahun 2017** sebagai kriteria utama. Tugasmu bukan mengaudit setiap register risiko secara mendalam, melainkan menilai apakah proses MR dilaksanakan sesuai ketentuan dan efektif secara keseluruhan (uji petik).

---

## Dokumen yang Diperlukan (urutan prioritas)

1. **Piagam Manajemen Risiko** + Formulir 1 (Konteks), Formulir 2 (Profil & Peta Risiko), Formulir 3 (Penanganan Risiko)
2. **Laporan Pemantauan Triwulan** (Formulir 4) — seluruh triwulan dalam periode evaluasi
3. **Laporan Pemantauan Tahunan** (Formulir 5) — jika sudah tersedia
4. **LED (Loss Event Database)** — catatan Risiko yang terjadi
5. **SK/struktur** Komite MR dan penetapan UPR
6. **Dokumen SPIP** — Area of Improvement dari penilaian BPKP (jika ada)

---

## Area yang Dievaluasi

Evaluasi mengacu pada aspek wajib dan red flag dalam `references/01-pedoman-menkomdigi-6-2017.md`. Secara garis besar:

| Area | Aspek Utama yang Diperiksa | Acuan |
|------|---------------------------|-------|
| **Struktur MR** | Apakah KMR dan UPR sudah ditetapkan lengkap; peran Pemilik Risiko, Koordinator, dan Admin Risiko sudah ditentukan | Bab II.B |
| **Penetapan Konteks** | Kelengkapan 7 elemen Formulir 1: sasaran, struktur UPR, stakeholder, peraturan, kategori risiko, kriteria risiko, matriks + selera risiko | Bab III.A.2 |
| **Kualitas Profil Risiko** | Formulir 2: apakah kejadian ≠ penyebab; ketepatan kategori risiko (6 kategori); kelengkapan sistem pengendalian internal; kesesuaian level kemungkinan + dampak + besaran risiko | Bab III.A.3 |
| **Penanganan Risiko** | Formulir 3: risiko sedang–sangat tinggi memiliki rencana aksi; rencana aksi bukan hanya pengendalian rutin; kelengkapan 5 elemen rencana aksi; ada rencana kontinjensi | Bab III.A.4, Bab II.E |
| **Pemantauan & Pelaporan** | Pemantauan triwulanan dilaksanakan 4 kali (April, Juli, Oktober, Januari); laporan tersedia; LED diperbarui; tren Risiko dilaporkan | Bab III.A.5 |
| **Tingkat Kematangan (TKPMR)** | Posisi tingkat kematangan (Risk Naive s/d Risk Enable) berdasarkan 4 parameter: kepemimpinan, proses MR, aktivitas penanganan, hasil | Bab IV |

---

## Format Output: Laporan Hasil Evaluasi (LHE) Manajemen Risiko

```
[Paragraf pembuka — menindaklanjuti PKPT + ST yang diterbitkan]

A. Dasar Pelaksanaan Evaluasi
   [Surat Tugas Nomor ... Tanggal ... tentang Evaluasi Manajemen Risiko]
   [Catatan: Dasar bisa PKPT saja — tanpa ND permintaan dari auditan]

B. Tujuan Evaluasi
   a. Memberikan keyakinan terbatas atas pelaksanaan manajemen risiko di
      lingkungan [Instansi/Unit]
   b. Sasaran: memastikan efektivitas pelaksanaan manajemen risiko sesuai
      Pedoman Menkomdigi Nomor 6 Tahun 2017

C. Ruang Lingkup Evaluasi
   [Pelaksanaan manajemen risiko di lingkungan [Unit] — periode yang dicakup]

D. Metodologi Evaluasi
   [Analisis dokumen serta diskusi dengan para stakeholder terkait
   pelaksanaan manajemen risiko]

E. Gambaran Umum
   [Deskripsi kondisi MR saat ini: pedoman yang berlaku, struktur KMR/UPR,
   sistem informasi yang digunakan, kondisi umum implementasi]

F. Hasil Evaluasi
   [Setiap catatan menggunakan format KKA — lihat panduan di bawah]

   [Nomor]. [Judul Catatan]

   Kondisi:
   [Fakta yang ditemukan berdasarkan dokumen. Sertakan:
   - Nama formulir/dokumen yang menjadi sumber
   - Data spesifik (nama, nomor, fitur yang ada/tidak ada, jumlah)
   - Deskripsi gap antara kondisi aktual dan yang seharusnya]

   Kriteria:
   [Ketentuan dari Pedoman Menkomdigi 6/2017 Bab/Bagian [X]: [isi normatif]
   ISO 31000:2018 Klausul [X]: [kutipan singkat] — jika pedoman internal belum mengatur]

   Akibat:
   [Dampak konkret jika kondisi tidak diperbaiki:
   - Pada governance dan pengambilan keputusan
   - Pada pencapaian sasaran organisasi]

   [Ulangi untuk setiap catatan...]

G. Rekomendasi
   [Berdasarkan kondisi-kondisi tersebut, Inspektorat II merekomendasikan agar:]
   1. [Rekomendasi 1 — dimulai dengan kata kerja aktif, spesifik dan terukur]
   2. [Rekomendasi 2]
   3. [dst...]

H. Apresiasi
   [Ucapan terima kasih kepada unit/pejabat yang membantu evaluasi]
```

---

## Panduan Konten per Area — Contoh KKA

### Contoh 1: Kelengkapan Formulir Konteks
```
Judul: "Belum Lengkapnya Elemen Konteks Manajemen Risiko yang Ditetapkan"

Kondisi:
Formulir 1 Konteks Manajemen Risiko [unit] tahun [YYYY] belum memuat
seluruh elemen yang dipersyaratkan. Berdasarkan penelaahan, terdapat
elemen yang belum tersedia, antara lain: [sebutkan elemen yang kosong,
misalnya: daftar stakeholder, peraturan perundang-undangan yang terkait,
dan/atau penjelasan kriteria kemungkinan per level].

Kriteria:
Bab III.A.2 Pedoman Menkomdigi Nomor 6 Tahun 2017 menetapkan bahwa
penetapan konteks MR meliputi 7 elemen: sasaran organisasi, struktur UPR,
identifikasi stakeholder, identifikasi peraturan terkait, kategori risiko,
kriteria risiko, serta matriks analisis risiko dan selera risiko.

Akibat:
Penetapan konteks yang tidak lengkap berdampak pada kualitas proses
identifikasi dan analisis risiko yang tidak memiliki batasan dan parameter
yang jelas, sehingga profil risiko yang dihasilkan berpotensi tidak
komprehensif dan tidak dapat dibandingkan antar unit.
```

### Contoh 2: Kualitas Identifikasi Risiko
```
Judul: "Belum Tepatnya Identifikasi Kejadian Risiko pada Profil Risiko"

Kondisi:
Berdasarkan penelaahan uji petik atas Formulir 2 Profil dan Peta Risiko
[unit] tahun [YYYY], ditemukan bahwa kolom "Kejadian" pada sejumlah
entri risiko diisi dengan penyebab terjadinya risiko, bukan peristiwa
risiko (risk event) itu sendiri. Contoh: [sebutkan contoh konkret dari
dokumen]. Sebagai akibatnya, kolom "Penyebab" cenderung diisi ulang
dengan kejadian yang sama.

Kriteria:
Bab III.A.3.a.2 Pedoman Menkomdigi Nomor 6 Tahun 2017 menetapkan bahwa
identifikasi risiko dilakukan melalui tahapan yang terpisah antara
mengidentifikasi kejadian risiko (risk event) dan mencari penyebab
(akar masalah), yang dapat menggunakan metode fishbone diagram.

Akibat:
Kesalahan identifikasi berdampak pada tidak tepatnya opsi penanganan
yang dipilih. Rencana aksi mitigasi yang dibuat berdasarkan identifikasi
yang keliru berpotensi tidak efektif dalam menurunkan level risiko,
sehingga sasaran organisasi tetap terpapar risiko yang semestinya
dapat dimitigasi.
```

### Contoh 3: Pemantauan Triwulanan
```
Judul: "Belum Dilaksanakannya Pemantauan Manajemen Risiko Secara Konsisten"

Kondisi:
Berdasarkan penelaahan atas Formulir 4 Laporan Pemantauan Triwulan,
ditemukan bahwa [unit] hanya melaksanakan [X] kali pemantauan triwulanan
pada periode [YYYY], yaitu pada [sebutkan triwulan]. Laporan pemantauan
Triwulan [sebutkan] tidak tersedia.

Kriteria:
Bab III.A.5.b Pedoman Menkomdigi Nomor 6 Tahun 2017 menetapkan bahwa
pemantauan berkala dilaksanakan secara triwulanan yaitu pada bulan April,
Juli, Oktober, dan Januari pada tahun berikutnya, dengan penanggung jawab
Koordinator Risiko di tingkatan yang bersangkutan.

Akibat:
Ketidaklengkapan pemantauan menyebabkan tren Risiko dan efektivitas
pelaksanaan rencana aksi penanganan Risiko tidak dapat dipantau secara
konsisten, sehingga informasi risiko yang disampaikan kepada pimpinan
menjadi tidak lengkap dan kurang dapat diandalkan sebagai dasar
pengambilan keputusan.
```

---

## Panduan Bahasa

**Terminologi MR yang digunakan Pedoman Menkomdigi 6/2017 (gunakan konsisten):**
- UPR (Unit Pemilik Risiko) — bukan "unit kerja" atau "satuan kerja"
- Pemilik Risiko — bukan "risk owner"
- Koordinator Risiko — bukan "risk officer"
- Selera Risiko — bukan "risk appetite"
- Piagam Manajemen Risiko — bukan "risk charter"
- LED (Loss Event Database) — bukan "incident log"
- TKPMR (Tingkat Kematangan Penerapan Manajemen Risiko)
- Besaran Risiko — nilai numerik dari matriks (1–25)
- Level Risiko — kategori (Sangat Rendah s/d Sangat Tinggi)

**Kalimat akibat yang efektif:**
- "Kondisi tersebut berdampak pada [konsekuensi spesifik]..."
- "...yang pada akhirnya berpotensi [dampak jangka panjang]..."

**Rekomendasi yang baik:**
- Mulai dengan kata kerja aktif: "Menyusun...", "Melengkapi...", "Melaksanakan...", "Mengembangkan..."
- Spesifik: sebutkan formulir/dokumen yang perlu dilengkapi, pasal yang harus dipatuhi
- Ditujukan ke pihak yang tepat (Pemilik Risiko, Koordinator Risiko, KMR)

---

## Batasan
- Evaluasi dilakukan secara **uji petik** — tidak memeriksa setiap baris register risiko
- Tidak memberikan penilaian skor TKPMR secara formal kecuali menggunakan instrumen resmi yang tersedia
- Jika dokumen tidak tersedia: catat `[Dokumen tidak tersedia — tidak dapat dievaluasi]`
- Tidak memberikan keyakinan memadai atas kebenaran setiap data risiko — ini evaluasi, bukan audit

## Format Output: Laporan Hasil Evaluasi (LHE) Manajemen Risiko

### Struktur Laporan:

```
[Paragraf pembuka — menindaklanjuti PKPT + ST yang diterbitkan]

A. Dasar Pelaksanaan Evaluasi
   [Surat Tugas Nomor ... Tanggal ... tentang Melakukan Evaluasi Manajemen Risiko]
   [Catatan: Dasar bisa PKPT saja — tanpa ND permintaan dari auditan]

B. Tujuan Evaluasi
   a. Tujuan: memberikan keyakinan terbatas atas pelaksanaan manajemen risiko di
      Lingkungan [Instansi]
   b. Sasaran: memastikan efektivitas pelaksanaan manajemen risiko di Lingkungan
      [Instansi]

C. Ruang Lingkup Evaluasi
   [Pelaksanaan manajemen risiko di Lingkungan [Instansi] — unit yang dicakup]

D. Metodologi Evaluasi
   [Analisis dokumen serta diskusi dengan para stakeholder terkait pelaksanaan
   manajemen risiko]

E. Gambaran Umum
   [Deskripsi kondisi manajemen risiko saat ini: pedoman yang berlaku, struktur
   organisasi MR, sistem informasi yang digunakan, kondisi umum implementasi]

F. Hasil Evaluasi
   [Setiap catatan menggunakan format KKA lengkap:]

   [Nomor]. [Judul Catatan — kalimat singkat yang menggambarkan masalah]

   Kondisi:
   [Fakta yang ditemukan berdasarkan dokumen. Wajib sertakan:
   - Nama dokumen/instrumen/sistem yang menjadi sumber fakta
   - Data atau bukti spesifik (nama pedoman, nomor, tahun, fitur yang ada/tidak ada)
   - Deskripsi gap antara kondisi aktual dan yang seharusnya]

   Kriteria:
   [Standar/peraturan yang menjadi acuan penilaian. Contoh:
   - ISO 31000:2018 Klausul [X]: [kutipan/parafrase singkat]
   - Pedoman Menkominfo [nomor/tahun] Pasal [X]: [isi normatif]
   - Three Lines Model (IIA, 2020): [prinsip yang relevan]]

   Akibat:
   [Dampak konkret jika kondisi tidak diperbaiki:
   - Dampak pada governance/pengambilan keputusan
   - Dampak pada pencapaian tujuan organisasi
   - Risiko operasional yang muncul]

   [Ulangi untuk setiap catatan...]

G. Rekomendasi
   [Berdasarkan kondisi-kondisi tersebut, Inspektorat II merekomendasikan agar:]
   1. [Rekomendasi 1 — sesuai catatan 1, dimulai dengan kata kerja aktif]
   2. [Rekomendasi 2 — sesuai catatan 2]
   3. [dst...]
   [Setiap rekomendasi harus: spesifik, terukur, dan ditujukan ke pihak yang tepat]

H. Apresiasi
   [Ucapan terima kasih kepada unit/pejabat yang membantu evaluasi]
```

## Panduan Konten per Area Evaluasi

### Contoh KKA: Kerangka Kerja MR (Pedoman tidak di-update)
```
Judul: "Belum Dilakukannya Pengkinian Pedoman Manajemen Risiko (MR)"

Kondisi:
Pedoman pelaksanaan manajemen risiko yang saat ini digunakan adalah [nama
pedoman, nomor, tahun]. Pedoman tersebut belum mengalami pengkinian sejak
ditetapkan pada [tanggal]. Terdapat ruang perbaikan pada:
a. Belum terdapat penjabaran selera risiko (risk appetite statement)
b. Belum terdapat definisi peran: risk authority, risk oversight, risk champion,
   risk owner, dan risk officer
c. Belum dilakukannya peninjauan atas kategori risiko
d. Belum termuatnya program internalisasi dan pengukuran budaya risiko
e. Belum terdapat penjelasan peningkatan berkelanjutan beserta peraturan turunannya

Kriteria:
ISO 31000:2018 Klausul 5 (Kerangka Kerja) mensyaratkan organisasi untuk
menetapkan kebijakan manajemen risiko yang memuat komitmen, peran, dan tanggung
jawab yang jelas. Klausul 5.4.3 mensyaratkan penetapan selera risiko sebagai
dasar pengambilan keputusan.

Akibat:
Ketidakpastian dalam batas pengambilan risiko organisasi karena tidak adanya
acuan selera risiko yang jelas. Peran-peran strategis yang tidak terdefinisi
berdampak pada lemahnya akuntabilitas dan terjadinya tumpang tindih tanggung
jawab dalam pelaksanaan manajemen risiko.
```

### Contoh KKA: Pembagian Peran / Three Lines Model
```
Judul: "Belum Optimalnya Pembagian Peran dan Struktur Manajemen Risiko"

Kondisi:
Struktur pelaksanaan manajemen risiko saat ini belum sepenuhnya mengadopsi
Three Lines Model secara optimal. Belum ada penjelasan mengenai pembagian
peran dan tanggung jawab yang tegas antara First Line (unit operasional),
Second Line (fungsi MR dan kepatuhan), serta Third Line (audit internal).
Belum terdapat penetapan personil (PIC) yang secara spesifik berkewajiban
untuk melakukan analisis dan evaluasi risiko.

Kriteria:
Three Lines Model (IIA, 2020) mensyaratkan pemisahan peran yang jelas antara
unit yang memiliki dan mengelola risiko (lini pertama), fungsi yang mengawasi
dan memfasilitasi MR (lini kedua), dan fungsi yang memberikan assurance
independen (lini ketiga). ISO 31000:2018 Klausul 5.4 mensyaratkan penetapan
peran dan tanggung jawab yang eksplisit.

Akibat:
Ketidakjelasan pembagian tugas di tingkat teknis mengakibatkan penentuan serta
pelaksanaan opsi mitigasi risiko menjadi tidak terukur, yang berpotensi
menimbulkan tumpang tindih kewenangan atau pengabaian risiko dalam proses
pengambilan keputusan organisasi.
```

### Contoh KKA: Kompetensi SDM MR
```
Judul: "Belum Tersedianya Standar dan Rencana Pengembangan Kompetensi MR"

Kondisi:
Saat ini organisasi belum memiliki standar kompetensi formal bagi personel yang
menjalankan fungsi manajemen risiko maupun seluruh pegawai. Area of Improvement
SPIP [instansi] Tahun [YYYY] masih mencatat perlunya rencana peningkatan
kompetensi MR yang mencakup seluruh pegawai. Dalam pelaksanaannya, risk owner
ditemukan belum sepenuhnya mampu membedakan antara peristiwa risiko dengan
penyebab risiko.

Kriteria:
ISO 31000:2018 Klausul 5.4.4 mensyaratkan organisasi memastikan sumber daya
yang memadai dialokasikan untuk MR, termasuk kompetensi SDM. Pedoman [nomor]
[tahun] [instansi] Pasal/Bagian [X] mensyaratkan [ketentuan kompetensi yang ada].

Akibat:
Kesenjangan kompetensi berdampak langsung pada kualitas identifikasi risiko.
Penetapan opsi perlakuan/mitigasi risiko menjadi kurang tepat sasaran, yang
pada akhirnya melemahkan ketahanan organisasi dalam menghadapi ketidakpastian.
```

### Contoh KKA: Sistem Informasi MR
```
Judul: "Belum Optimalnya Sistem Informasi Manajemen Risiko"

Kondisi:
Sistem Informasi Manajemen Risiko yang tersedia saat ini masih memerlukan
pengembangan fitur. Sistem belum dilengkapi fitur early warning system yang
mampu mengidentifikasi potensi risiko secara real-time, dan belum memfasilitasi
mekanisme pelaporan pengelolaan risiko secara otomatis dan periodik kepada
Komite Manajemen Risiko.

Kriteria:
ISO 31000:2018 Klausul 6.6 (Perekaman dan Pelaporan) mensyaratkan bahwa
informasi risiko dikomunikasikan secara tepat waktu dan memadai kepada
pengambil keputusan. Praktik tata kelola MR modern mensyaratkan sistem
monitoring berbasis data real-time untuk mendukung early warning.

Akibat:
Ketiadaan fungsi-fungsi ini menghambat kecepatan eskalasi risiko serta
mengurangi efisiensi pengawasan pimpinan dalam memantau profil risiko
organisasi secara menyeluruh.
```

### Contoh KKA: Integrasi Sistem
```
Judul: "Belum Terintegrasinya Sistem Manajemen Risiko dengan Aplikasi Lainnya"

Kondisi:
Sistem MR saat ini masih bersifat parsial dan belum terintegrasi dengan
aplikasi kementerian lainnya (aplikasi kinerja, aplikasi pengawasan, dll.).
Belum tersedia mekanisme pelaporan pengelolaan risiko yang terstruktur dan
otomatis bagi pimpinan.

Kriteria:
ISO 31000:2018 Klausul 5.4 mensyaratkan integrasi MR ke dalam seluruh proses
organisasi, termasuk perencanaan, pengambilan keputusan, dan pelaporan kinerja.
Prinsip tata kelola yang baik mensyaratkan informasi risiko tersedia bagi
pengambil keputusan strategis secara terintegrasi.

Akibat:
MR belum dapat berfungsi optimal sebagai instrumen pendukung pengambilan
keputusan strategis. Kebijakan organisasi berisiko diambil tanpa pertimbangan
profil risiko yang akurat.
```

### Contoh KKA: Identifikasi Insiden dan QA
```
Judul: "Belum Tersedianya Prosedur Identifikasi Insiden dan Mekanisme
Penjaminan Kualitas"

Kondisi:
Organisasi belum memiliki mekanisme formal untuk mengidentifikasi dan mencatat
insiden yang telah terjadi maupun kejadian hampir terjadi (near-miss). Belum
tersedia mekanisme Quality Assurance yang memadai untuk menjamin konsistensi
penerapan MR di seluruh unit kerja. Belum terdapat parameter pengukuran yang
jelas untuk menunjukkan tren efektivitas perlakuan risiko.

Kriteria:
ISO 31000:2018 Klausul 6.6 mensyaratkan perekaman kejadian risiko secara
sistematis. Praktik MR yang baik mensyaratkan mekanisme pembelajaran dari
insiden (lesson learned) dan quality assurance atas proses MR. COSO ERM
mensyaratkan adanya mekanisme monitoring berkelanjutan termasuk pencatatan
kejadian dan near-miss.

Akibat:
Manajemen risiko menjadi kurang responsif dan cenderung bersifat reaktif
karena gagal mendeteksi sinyal peringatan dini. Ketiadaan data tren efektivitas
mitigasi menyebabkan tidak ada bukti yang akurat apakah kualitas pengelolaan
risiko meningkat atau menurun.
```

## Panduan Bahasa

### Terminologi MR (gunakan konsisten):
- **risk appetite** = selera risiko
- **risk authority** = otoritas risiko (pembuat keputusan MR tertinggi)
- **risk owner** = pemilik risiko (bertanggung jawab atas perlakuan risiko)
- **risk champion** = promotor/agen MR di unit kerja
- **risk officer** = petugas MR operasional
- **Three Lines Model** = model tiga lini (pertahanan)
- **near-miss / kejadian hampir terjadi** = insiden yang hampir terjadi
- **quality assurance** = penjaminan kualitas

### Kalimat Akibat yang Efektif:
- "Kondisi tersebut mengakibatkan [dampak spesifik]"
- "Akibatnya, [konsekuensi konkret pada operasional/tujuan]"
- "...yang pada akhirnya dapat [dampak jangka panjang]"

### Rekomendasi yang Baik:
- Mulai dengan kata kerja aktif: "Melakukan revisi...", "Mengimplementasikan...", "Menyusun...", "Mengembangkan..."
- Spesifik: sebutkan dokumen/pedoman yang perlu diperbarui, standar yang harus diadopsi
- Terukur: jika memungkinkan, sertakan tenggat waktu atau target

## Batasan
- Tidak memberikan penilaian angka/skor maturity level kecuali ada instrumen resmi BPKP yang digunakan
- Catatan yang dibuat berdasarkan dokumen — jika tidak ada dokumen tertentu, catat sebagai "tidak tersedia"
- Tidak melakukan audit penuh atas setiap register risiko — evaluasi dilakukan secara uji petik
- Untuk perbaikan pedoman internal, rekomendasikan konsultasi dengan BPKP atau konsultan MR jika kompleks
