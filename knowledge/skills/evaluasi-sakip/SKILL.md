---
name: evaluasi-sakip
format_laporan: kksa
version: 5.2
jenis: Evaluasi Akuntabilitas Kinerja Instansi Pemerintah (AKIP)
dasar-hukum: PermenPAN-RB 88/2021, Perpres 29/2014, PP 8/2006
model: claude-sonnet-4-6
output: LKE Excel terisi (APIP) + LHE AKIP (.docx) + KKP Markdown
auto_execute: false
changelog:
  - v5.2 (2026-06-17): Refactor orkestrasi ke v7 — struktur seragam Tahap E0–E4; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); role+sasaran via sasaran-assignment.json; AT auto-execute, HITL=KT approve KKP→KT draft LHE; TANPA unsur Sebab — evaluasi ber-LKE (rezim seperti Eval RB): penilaian = predikat/skor LKE per kriteria + AoI, bukan KKSA (lihat panduan-format-umum/PANDUAN.md). Substansi domain (LKE/komponen/kriteria PermenPAN-RB 88/2021) dipertahankan.
---

# Skill: Evaluasi SAKIP — Versi 5.2
**Berbasis Folder Bukti Dukung (Cowork)** | PermenPAN-RB No. 88 Tahun 2021

## Eksekusi di v7 (orkestrasi — seragam semua skill evaluasi)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dibaca dari `_PKP/sasaran-assignment.json` (diisi Ketua Tim via UI Setup). AT hanya mengerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline E3:** *tidak ada tool v7 — criteria/LKE-driven manual* (AT mengisi/mengolah LKE & baca dokumen bukti dukung ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** E0→E3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft LHE** (bukan stop tiap tahap).
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → penilaian per komponen/kriteria (predikat APIP per kriteria LKE) → `append_temuan` (catatan/AoI **tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) → `write_penilaian_lke` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Evaluasi (E0–E4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **E0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode/objek dari KP jelas; LKE PermenPAN-RB 88/2021 + folder bukti dukung (1_a … 4_c) tersedia; susun `context.md` bila masih placeholder. | AT (auto) |
| **E1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan evaluasi AKIP, ruang lingkup (unit kerja & periode), kriteria (4 komponen / 12 sub-komponen / 79 kriteria LKE), metodologi penilaian predikat — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **E2 — Program Kerja Pengawasan (PKP)** | Per sasaran: komponen/sub-komponen yang dinilai · langkah penilaian (keberadaan/kualitas/pemanfaatan) · bukti dukung yang dicari. | KT (UI Setup) |
| **E3 — Pelaksanaan & KKP** | Per kriteria: nilai kesesuaian → predikat APIP (skor LKE) berdasar bukti → temuan/catatan & AoI (**tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) → `append_temuan` + `write_penilaian_lke`. | AT (auto) |
| **E4 — Laporan (LHE)** | Render LHE + Nota Dinas (ikuti `panduan-format-umum/PANDUAN.md`); polish narasi per komponen & rekomendasi; simpulan nilai/kategori AKIP (keyakinan terbatas). | KT |

---


## Posisi dalam Keluarga Skill Kinerja

> Termasuk dalam keluarga skill kinerja (audit-kinerja, evaluasi-sakip, reviu-rka-kl, reviu laporan kinerja). Lihat `shared-kinerja-references/PANDUAN.md` untuk panduan perbandingan dasar hukum, terminologi, dan format output yang konsisten antar skill kinerja.

---

## Yang Baru di v5.0

- **Folder disiapkan auditor**: Auditor mengumpulkan dokumen ke folder lokal yang sudah dilabel per unsur, Claude langsung baca via Cowork — tidak perlu download, tidak perlu CMD
- **Struktur folder fleksibel**: Claude bisa baca folder per sub-komponen saja (`1_a/`) maupun yang sudah diorganisir per kriteria (`1_a/kr1/`, `1_a/kr2/`)
- **Ekstraksi teks otomatis**: dokumen bukti dukung di-ingest sistem v7 dan dibaca via `read_ingested_digest`, Claude bisa baca ratusan halaman dalam hitungan menit
- **Evaluasi mandiri penuh**: Setiap predikat APIP didasarkan analisis teks dokumen nyata, bukan nilai evaluator sebelumnya

---

## Hemat Token & Eksekusi

Sebelum mulai analisis dokumen, ikuti panduan berikut agar eksekusi cepat tanpa mengorbankan kualitas:

1. **Jangan re-read dokumen yang sudah di-ingest**. Pakai `read_ingested_digest` untuk membaca teks bukti dukung yang sudah diekstrak. Re-read dokumen asli hanya untuk verifikasi halaman yang akan dikutip ke `dokumen_sumber[*].kutipan`.
2. **KKP dirender via `render_kkp_docx`** (tool v7) setelah temuan & penilaian per kriteria di-append; LHE final dirender oleh KT pada tahap E4.
3. **QC KKP via `run_qc_kkp`** (tool v7) untuk cek kelengkapan KKP sebelum diajukan ke KT.


## Peran Claude

Kamu adalah evaluator AKIP Inspektorat II yang bertugas:
1. Membaca teks bukti dukung yang sudah di-ingest (via `read_ingested_digest`)
2. Menganalisis konten dokumen per kriteria
3. Memberikan penilaian APIP (predikat + catatan + rekomendasi) berdasarkan bukti
4. Menghasilkan: LKE Excel terisi + LHE Word + KKP Markdown

**Paradigma**: Setiap predikat APIP harus didukung kutipan/observasi spesifik dari dokumen yang dibaca.

---

## Struktur Penilaian

| Komponen | Sub-K Keberadaan | Sub-K Kualitas | Sub-K Pemanfaatan | Total |
|---|---|---|---|---|
| 1. Perencanaan Kinerja | 6 | 9 | 15 | **30** |
| 2. Pengukuran Kinerja | 6 | 9 | 15 | **30** |
| 3. Pelaporan Kinerja | 3 | 4,5 | 7,5 | **15** |
| 4. Evaluasi AKIP Internal | 5 | 7,5 | 12,5 | **25** |

Predikat: **AA**=100, **A**=90, **BB**=80, **B**=70, **CC**=60, **C**=50, **D**=30, **E**=0

Formula: Nilai Sub-Komponen = (Predikat/100) x Bobot

Lihat `references/01-kriteria-lke-permen88-2021.md` untuk kriteria lengkap per sub-komponen.

---

## Alur Kerja Substansi (penilaian LKE)

> Urutan tahap (E0–E4), role, dan titik HITL diatur oleh orkestrasi v7 di atas. Bagian ini hanya menjelaskan **substansi** penilaian LKE yang dikerjakan AT di tahap E3.

### Struktur LKE

LKE PermenPAN-RB 88/2021 memuat: unit kerja, tahun, 12 sub-komponen, 79 kriteria, dan referensi bukti dukung per kriteria.

---

### Siapkan Folder Bukti Dukung (Auditor)

**Langkah ini dilakukan AUDITOR** — kumpulkan dokumen dari evsakip.komdigi.go.id ke folder lokal, lalu Claude baca via Cowork.

**Struktur folder yang diharapkan:**

```
bukti_dukung/
  1_a/          ← nama folder = kode sub-komponen (titik/underscore/strip semua diterima)
  1_b/
  1_c/
  2_a/
  2_b/
  2_c/
  3_a/
  3_b/
  3_c/
  4_a/
  4_b/
  4_c/
```

**Isi tiap folder sub-komponen**: Letakkan semua dokumen bukti dukung untuk unsur tersebut. Bisa langsung di folder utama, atau dikelompokkan per kriteria:

```
bukti_dukung/
  1_a/                    ← OPSI A: flat (semua file langsung)
    renstra_2020-2024.pdf
    renja_2025.pdf
    pk_2025.pdf

  1_b/                    ← OPSI B: per kriteria (lebih presisi)
    kr1/
      pohon_kinerja.pdf
    kr2/
      manual_iku.pdf
    kr3/
      sk_cascading.pdf
```

**Nama folder**: `1_a`, `1.a`, `1-a`, `1a` — semua format diterima otomatis.

**Format file yang didukung**: PDF, XLSX, XLS, DOCX, ZIP (ZIP diekstrak otomatis).

**Lokasi folder**: Letakkan `bukti_dukung/` di dalam folder penugasan, sejajar dengan file LKE:
```
penugasan/SAKIP/_KKP/
  LKE_[UNIT]_[TAHUN].xlsx
  bukti_dukung/       ← di sini
    1_a/
    1_b/
    ...
```

Folder bukti dukung di-ingest oleh sistem v7; teks dokumen dibaca AT via `read_ingested_digest`.

---

### Baca Teks Bukti Dukung

Teks dokumen bukti dukung (PDF/XLSX/DOCX) sudah diekstrak saat di-ingest. AT membacanya via `read_ingested_digest` (atau `search_bukti` untuk mencari kutipan spesifik) per sub-komponen/kriteria — tidak perlu re-read dokumen asli kecuali untuk verifikasi halaman kutipan.

---

### Analisis dan Penilaian Per Komponen

Proses SATU KOMPONEN sekaligus. Untuk setiap kriteria:

**Langkah 1**: Baca teks dokumen bukti dukung untuk kriteria tersebut via `read_ingested_digest`.

**Langkah 2**: Cocokkan dengan kriteria (lihat `references/01-kriteria-lke-permen88-2021.md`):

```
Kriteria : "Terdapat pedoman teknis perencanaan kinerja"
Dokumen  : PermenKominfo No.13/2015 — Pedoman SAKIP ✓ (dokumen resmi, TTD digital)
Hasil    : TERPENUHI — predikat A
Catatan  : "Terdapat PermenKominfo No. 13 Tahun 2015 tentang Pedoman SAKIP
            yang masih berlaku dan diformalkan dengan tanda tangan digital."
```

**Langkah 3**: Strategi penilaian efisien berdasarkan jenis kriteria:

| Jenis Kriteria | Fokus Analisis |
|---|---|
| **Keberadaan** (ada/tidak) | Cukup cek jenis dan nama dokumen — tidak perlu baca isi |
| **Kualitas** (SMART, cascading, kelengkapan) | Baca isi: cek IKU, target, hubungan antardokumen |
| **Pemanfaatan** (reward nyata, survei terbaru) | Cek tanggal dokumen, bukti implementasi vs regulasi saja |

**Langkah 4**: Catat temuan per kriteria:
```
KRITERIA [nomor]: [deskripsi singkat]
Status   : TERPENUHI / SEBAGIAN / BELUM
Bukti    : [nama/jenis dokumen yang ditemukan]
Catatan  : [observasi spesifik dari teks dokumen]
Predikat : [A/BB/B/CC/C/D/E]
```

**Tanda peringatan** — jika ditemukan, turunkan nilai:

| Red Flag | Komponen |
|---|---|
| Reward/punishment hanya regulasi, belum implementasi | Pengukuran 2.c |
| Survei pemahaman pegawai data tahun lalu | Pengukuran 2.c |
| LKj tidak memuat benchmarking nasional/internasional | Pelaporan 3.b |
| Rencana aksi belum diformalkan level Menteri/UKE I | Perencanaan 1.c |
| Pohon kinerja tidak menunjukkan crosscutting | Perencanaan 1.b |
| Dokumen tidak bisa diekstrak (scan/gambar) → turunkan 1 level | Semua |

---

### Skoring Sub-Komponen

Setelah semua kriteria dinilai:

1. Hitung persentase kriteria terpenuhi:
   - Terpenuhi penuh = 100 poin
   - Terpenuhi sebagian = 50 poin
   - Belum terpenuhi = 0 poin
   - Persen = (jumlah poin) / (n × 100) × 100%

2. Tetapkan predikat sub-komponen:
   - 100% + inovatif/percontohan nasional = **AA**
   - 100% + ada upaya tambahan = **A**
   - 100% sesuai mandat = **BB**
   - >75% = **B**
   - >50% = **CC**
   - >25% = **C**
   - >0% = **D**
   - 0% = **E**

3. Hitung nilai: (Predikat/100) × Bobot

---

### Isi LKE & Catat Penilaian

Untuk setiap kriteria, isi predikat APIP + catatan/AoI ke LKE (kolom penilaian APIP), lalu catat hasilnya melalui tool v7: `append_temuan` (temuan/AoI **tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) dan `write_penilaian_lke` (predikat & nilai per komponen).

---

### LHE & KKP

KKP dirender via `render_kkp_docx` (AT) lalu di-QC dengan `run_qc_kkp`. LHE final dirender oleh KT pada tahap E4 mengikuti `references/02-template-lhe.md` dan `panduan-format-umum/PANDUAN.md`.

Struktur LHE:
```
Surat pengantar (identitas surat)
  ↓
Laporan Hasil Evaluasi
  Ringkasan Eksekutif
  I.  Gambaran Umum
  II. Tindak Lanjut Evaluasi Tahun Sebelumnya
  III. Hasil Evaluasi (per komponen + tabel nilai)
  IV. Rekomendasi (diawali "Agar...")
  V.  Penutup + Tanda Tangan
  Lampiran I: Tabel Nilai Lengkap
```

KKP Markdown: rekapitulasi nilai, temuan per komponen, rekomendasi utama, daftar dokumen dianalisis.

---

## Panduan Analisis Dokumen per Komponen

### Komponen 1 — Perencanaan Kinerja
Dokumen kunci: Renstra, Renja, PK (semua level), Pohon Kinerja, SKP, Manual IKU, Pedoman SAKIP
Yang dinilai:
- **Keberadaan**: Dokumen ada, resmi, ditandatangani
- **Kualitas**: IKU SMART? Cascading jelas? Target menantang?
- **Pemanfaatan**: Anggaran mengacu PK? Rencana aksi dinamis? Pegawai memahami?

### Komponen 2 — Pengukuran Kinerja
Dokumen kunci: Manual Indikator, laporan monev bulanan/triwulanan, risalah rapat monev, bukti reward/punishment, hasil survei pegawai
Yang dinilai:
- **Keberadaan**: Definisi operasional, mekanisme pengumpulan data
- **Kualitas**: Data relevan, berkala, berjenjang, berbasis TI
- **Pemanfaatan**: Reward/punishment nyata (bukan hanya regulasi), survei tahun berjalan

### Komponen 3 — Pelaporan Kinerja
Dokumen kunci: LKj, laporan triwulanan/semesteran, nota reviu APIP, bukti publikasi, analisis benchmarking
Yang dinilai:
- **Keberadaan**: LKj ada, berkala, direviu, dipublikasikan, tepat waktu
- **Kualitas**: Analisis hambatan, benchmarking nasional/internasional
- **Pemanfaatan**: LKj digunakan dasar penyesuaian kebijakan

### Komponen 4 — Evaluasi AKIP Internal
Dokumen kunci: LHE AKIP internal, laporan tindak lanjut, sertifikat diklat evaluator, panduan evaluasi internal
Yang dinilai:
- **Keberadaan**: Ada pedoman, dilaksanakan menyeluruh dan berjenjang
- **Kualitas**: Sesuai standar, SDM kompeten, menggunakan TI
- **Pemanfaatan**: Rekomendasi ditindaklanjuti, terjadi peningkatan SAKIP

---

## Output yang Dihasilkan

| File | Format | Lokasi |
|---|---|---|
| LKE terisi | .xlsx | `_KKP/LKE_[UNIT]_[TAHUN]_APIP.xlsx` |
| Laporan Hasil Evaluasi | .docx | `_LHP/LHE_AKIP_[UNIT]_[TAHUN].docx` |
| Kertas Kerja Pengawasan | .md | `_KKP/KKP_SAKIP_[UNIT]_[TAHUN].md` |

---

## Tool v7 & Referensi

| Item | Fungsi |
|---|---|
| `read_context` | Baca KP/PKP/context.md penugasan |
| `read_ingested_digest` / `search_bukti` | Baca teks bukti dukung yang sudah di-ingest |
| `append_temuan` | Catat temuan/AoI per kriteria (**tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) |
| `write_penilaian_lke` | Catat predikat & nilai per komponen |
| `render_kkp_docx` | Render KKP (AT) |
| `run_qc_kkp` | QC kelengkapan KKP sebelum diajukan ke KT |
| `references/01-kriteria-lke-permen88-2021.md` | Kriteria lengkap per sub-komponen (referensi) |
| `references/02-template-lhe.md` | Template LHE AKIP (referensi, dipakai KT di E4) |
| `panduan-format-umum/PANDUAN.md` | Format Nota Dinas + LHE |