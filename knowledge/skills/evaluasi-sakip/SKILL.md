---
name: evaluasi-sakip
jenis: Evaluasi Akuntabilitas Kinerja Instansi Pemerintah (AKIP/SAKIP)
format_laporan: lke
dasar-hukum: PermenPAN-RB 88/2021, Perpres 29/2014, PP 8/2006
kode-surat: PW.04.05
tingkat-keyakinan: terbatas
version: "6.0"
changelog:
  - v6.0 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: 5 komponen PermenPAN-RB 88/2021 + skoring/bobot, instrumen LKE, Area of Improvement (AoI), kriteria + referensi, struktur LHE. Frontmatter `model`/`auto_execute`/`output` dihapus; seksi "Eksekusi di v7", tabel "Tahap E0–E4", nama tool sebagai resep, direktif UX, dan changelog naratif lama dibuang. **Doktrin TANPA unsur Sebab (rezim LKE + AoI) dipertahankan utuh.**
---

# Skill: Evaluasi SAKIP (AKIP)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **format** keluarannya.
>
> **Doktrin unsur (KRITIS):** evaluasi SAKIP adalah **rezim LKE** — penilaian = predikat/skor per kriteria pada instrumen LKE PermenPAN-RB 88/2021 + **Area of Improvement (AoI)** & rekomendasi. **BUKAN format KKSA: TIDAK ada unsur Sebab.** Jangan menambahkan unsur Sebab ke evaluasi-sakip (lihat `shared-kinerja-references/PANDUAN.md`: SAKIP "Sebab ❌ Tidak rezim LKE").

## Lingkup & Paradigma

Kamu adalah evaluator AKIP Inspektorat II yang menilai **implementasi sistem SAKIP** suatu unit kerja secara komprehensif terhadap 5 komponen PermenPAN-RB 88/2021. Tingkat keyakinan: **terbatas (evaluatif)**. Kode nomor surat: **PW.04.05**.

Alurnya adalah **penjaminan kualitas atas penilaian mandiri (PM) auditee**, bukan menilai dari nol: auditee mengisi self-assessment di LKE, lalu evaluator memberi **penilaian APIP** per kriteria pada kolom penjaminan kualitas. Selisih PM vs APIP (mis. optimism bias — PM lebih tinggi dari APIP) menjadi **catatan/AoI**.

**Paradigma**: setiap predikat APIP harus didukung kutipan/observasi spesifik dari dokumen bukti dukung yang dibaca — bukan menyalin nilai evaluator/auditee sebelumnya.

## Sumber Fakta: LKE + Bukti Dukung

Penilaian bersumber dari dua hal:
1. **LKE self-assessment auditee** (PermenPAN-RB 88/2021): unit kerja, tahun, 12 sub-komponen, 79 kriteria, nilai PM auditee per kriteria, dan referensi bukti dukung. Cell ber-formula dan sheet agregator **tidak boleh ditimpa** — isi hanya kolom input penilaian APIP.
2. **Folder bukti dukung** yang dikumpulkan auditor (per sub-komponen) — teks dokumen diekstrak otomatis dan dibaca secara deskriptif.

**Hemat token:** baca teks bukti dukung yang sudah diekstrak; jangan re-read PDF asli "untuk konteks". Buka halaman dokumen sumber **hanya** untuk verifikasi halaman yang dikutip. Dokumen yang tidak dapat diekstrak (scan/gambar) → turunkan 1 level predikat dan catat keterbatasan.

### Struktur Folder Bukti Dukung (disiapkan auditor)

Auditor mengumpulkan dokumen dari evsakip.komdigi.go.id ke folder lokal, dilabel per sub-komponen. Nama folder = kode sub-komponen; format `1_a`, `1.a`, `1-a`, `1a` semua diterima. Isi bisa flat (file langsung) atau dikelompokkan per kriteria (`1_a/kr1/`). Format didukung: PDF, XLSX, XLS, DOCX, ZIP (diekstrak otomatis).

```
bukti_dukung/
  1_a/ 1_b/ 1_c/      ← Perencanaan Kinerja
  2_a/ 2_b/ 2_c/      ← Pengukuran Kinerja
  3_a/ 3_b/ 3_c/      ← Pelaporan Kinerja
  4_a/ 4_b/ 4_c/      ← Evaluasi AKIP Internal
```

## Kerangka 5 Komponen & Skoring (PermenPAN-RB 88/2021)

PermenPAN-RB 88/2021 menilai 5 komponen AKIP. Empat komponen **proses** (Perencanaan, Pengukuran, Pelaporan, Evaluasi Internal, total bobot 100) dinilai melalui instrumen LKE; komponen kelima — **Capaian Kinerja** — dinilai sebagai pencapaian sasaran/IKU dan dirangkum di simpulan nilai akhir.

### Bobot Komponen Proses & Sub-Komponen

| Komponen | Keberadaan | Kualitas | Pemanfaatan | Total |
|---|---|---|---|---|
| 1. Perencanaan Kinerja | 6 | 9 | 15 | **30** |
| 2. Pengukuran Kinerja | 6 | 9 | 15 | **30** |
| 3. Pelaporan Kinerja | 3 | 4,5 | 7,5 | **15** |
| 4. Evaluasi AKIP Internal | 5 | 7,5 | 12,5 | **25** |

> Setiap komponen dinilai pada tiga dimensi: **Keberadaan** (dokumen ada/resmi), **Kualitas** (substansi/SMART/cascading/kelengkapan), **Pemanfaatan** (bukti implementasi nyata, bukan sekadar regulasi).

### Predikat & Formula

Predikat per kriteria/sub-komponen: **AA**=100 · **A**=90 · **BB**=80 · **B**=70 · **CC**=60 · **C**=50 · **D**=30 · **E**=0

`Nilai Sub-Komponen = (Predikat / 100) × Bobot`

Penilaian per kriteria → skor sub-komponen → nilai komponen → **nilai AKIP total (0–100) + predikat**. Lihat `references/01-kriteria-lke-permen88-2021.md` untuk kriteria lengkap (79 kriteria) per sub-komponen.

## Instrumen Penilaian (substansi LKE per kriteria)

Proses SATU KOMPONEN sekaligus. Untuk setiap kriteria:

1. **Baca teks bukti dukung** untuk kriteria tersebut.
2. **Cocokkan dengan kriteria** (lihat `references/01-kriteria-lke-permen88-2021.md`). Contoh:
   ```
   Kriteria : "Terdapat pedoman teknis perencanaan kinerja"
   Dokumen  : PermenKominfo No.13/2015 — Pedoman SAKIP ✓ (resmi, TTD digital)
   Hasil    : TERPENUHI — predikat A
   Catatan  : "Terdapat PermenKominfo No.13/2015 tentang Pedoman SAKIP yang masih berlaku."
   ```
3. **Strategi penilaian efisien per jenis kriteria:**

   | Jenis Kriteria | Fokus Analisis |
   |---|---|
   | **Keberadaan** (ada/tidak) | Cukup cek jenis & nama dokumen — tidak perlu baca isi |
   | **Kualitas** (SMART, cascading, kelengkapan) | Baca isi: cek IKU, target, hubungan antardokumen |
   | **Pemanfaatan** (reward nyata, survei terbaru) | Cek tanggal & bukti implementasi vs regulasi saja |

4. **Catat penilaian per kriteria:**
   ```
   KRITERIA [nomor]: [deskripsi singkat]
   Status   : TERPENUHI / SEBAGIAN / BELUM
   Bukti    : [nama/jenis dokumen yang ditemukan]
   Catatan  : [observasi spesifik dari teks dokumen]
   Predikat : [AA/A/BB/B/CC/C/D/E]
   ```

**Tanda peringatan (red flag) — bila ditemukan, turunkan nilai:**

| Red Flag | Komponen |
|---|---|
| Reward/punishment hanya regulasi, belum implementasi | Pengukuran 2.c |
| Survei pemahaman pegawai memakai data tahun lalu | Pengukuran 2.c |
| LKj tidak memuat benchmarking nasional/internasional | Pelaporan 3.b |
| Rencana aksi belum diformalkan level Menteri/UKE I | Perencanaan 1.c |
| Pohon kinerja tidak menunjukkan crosscutting | Perencanaan 1.b |
| Dokumen tidak bisa diekstrak (scan/gambar) → turunkan 1 level | Semua |

### Skoring Sub-Komponen

1. Hitung persentase kriteria terpenuhi: Terpenuhi penuh = 100; Sebagian = 50; Belum = 0. Persen = (jumlah poin) / (n × 100) × 100%.
2. Tetapkan predikat sub-komponen:
   - 100% + inovatif/percontohan nasional = **AA**
   - 100% + ada upaya tambahan = **A**
   - 100% sesuai mandat = **BB**
   - >75% = **B** · >50% = **CC** · >25% = **C** · >0% = **D** · 0% = **E**
3. Nilai = (Predikat / 100) × Bobot.

## Area of Improvement (AoI) & Catatan

Setelah semua kriteria dinilai, susun **catatan/AoI** dari selisih **PM vs APIP** dan dari kriteria yang belum/sebagian terpenuhi. Bila skor mandiri auditee **lebih tinggi** dari hasil APIP (optimism bias) → itu AoI.

**Elemen AoI/catatan (rezim LKE — TANPA unsur Sebab):**

| Elemen | Status | Catatan |
|---|---|---|
| **Komponen/Sub-Komponen** | ✅ Wajib | Komponen & kriteria yang dinilai |
| **Kondisi** | ✅ Wajib | Fakta dari bukti dukung: dokumen apa, isinya, gap-nya |
| **Kriteria** | ✅ Wajib | Kriteria LKE PermenPAN-RB 88/2021 yang menjadi tolok ukur |
| **Nilai (PM vs APIP)** | ✅ Wajib | Predikat/skor mandiri auditee vs penilaian APIP |
| **Akibat/Risiko** | ✅ Wajib | Konsekuensi bila kondisi tidak diperbaiki |
| **Rekomendasi (AoI)** | ✅ Wajib | Tindakan perbaikan konkret — diawali "Agar...". Disusun di LHE |
| ~~**Sebab**~~ | ❌ **TIDAK DIPAKAI** | Evaluasi ber-LKE bukan KKSA — **jangan tambahkan unsur Sebab** |

> **JANGAN** mengisi atau menambahkan unsur **Sebab** pada evaluasi-sakip. Aturan "Sebab anti-mengarang" yang berlaku untuk jenis ber-KKSA (audit/reviu/pemantauan/evaluasi non-LKE) **TIDAK** berlaku di sini — SAKIP adalah trio LKE (bersama RB & SPIP) yang memakai instrumen LKE + AoI tanpa Sebab.

## Panduan Analisis Dokumen per Komponen

### Komponen 1 — Perencanaan Kinerja
Dokumen kunci: Renstra, Renja, PK (semua level), Pohon Kinerja, SKP, Manual IKU, Pedoman SAKIP.
- **Keberadaan**: Dokumen ada, resmi, ditandatangani.
- **Kualitas**: IKU SMART? Cascading jelas? Target menantang?
- **Pemanfaatan**: Anggaran mengacu PK? Rencana aksi dinamis? Pegawai memahami?

### Komponen 2 — Pengukuran Kinerja
Dokumen kunci: Manual Indikator, laporan monev bulanan/triwulanan, risalah rapat monev, bukti reward/punishment, hasil survei pegawai.
- **Keberadaan**: Definisi operasional, mekanisme pengumpulan data.
- **Kualitas**: Data relevan, berkala, berjenjang, berbasis TI.
- **Pemanfaatan**: Reward/punishment nyata (bukan hanya regulasi), survei tahun berjalan.

### Komponen 3 — Pelaporan Kinerja
Dokumen kunci: LKj, laporan triwulanan/semesteran, nota reviu APIP, bukti publikasi, analisis benchmarking.
- **Keberadaan**: LKj ada, berkala, direviu, dipublikasikan, tepat waktu.
- **Kualitas**: Analisis hambatan, benchmarking nasional/internasional.
- **Pemanfaatan**: LKj digunakan sebagai dasar penyesuaian kebijakan.

### Komponen 4 — Evaluasi AKIP Internal
Dokumen kunci: LHE AKIP internal, laporan tindak lanjut, sertifikat diklat evaluator, panduan evaluasi internal.
- **Keberadaan**: Ada pedoman, dilaksanakan menyeluruh dan berjenjang.
- **Kualitas**: Sesuai standar, SDM kompeten, menggunakan TI.
- **Pemanfaatan**: Rekomendasi ditindaklanjuti, terjadi peningkatan SAKIP.

### Komponen 5 — Capaian Kinerja
Penilaian atas pencapaian sasaran/IKU sebagaimana tersaji pada LKj dan data realisasi. Dirangkum ke simpulan nilai AKIP total.

## Struktur Laporan (LHE SAKIP)

```
Surat pengantar / Nota Dinas (ikuti panduan-format-umum/PANDUAN.md)
  ↓
Laporan Hasil Evaluasi (LHE) AKIP
  Ringkasan Eksekutif
  I.   Gambaran Umum
  II.  Tindak Lanjut Evaluasi Tahun Sebelumnya
  III. Hasil Evaluasi (per komponen + tabel nilai)
  IV.  Rekomendasi / Area of Improvement (diawali "Agar...")
  V.   Penutup + Tanda Tangan
  Lampiran I: Tabel Nilai Lengkap (LKE terisi)
```

KKP memuat: rekapitulasi nilai (PM vs APIP per komponen + predikat akhir), catatan/AoI per komponen, rekomendasi utama, dan daftar dokumen yang dianalisis.

## Batasan

- **TANPA unsur Sebab** — rezim LKE; penilaian = predikat/skor per kriteria + AoI. Jangan menambahkan Sebab.
- **Tingkat keyakinan terbatas (evaluatif)** — bukan keyakinan memadai seperti audit.
- **Penjaminan kualitas atas self-assessment**, bukan menilai dari nol; jangan menimpa kolom penilaian mandiri (PM) auditee maupun cell berformula/sheet agregator pada LKE.
- Setiap predikat APIP wajib didukung kutipan/observasi spesifik dari bukti dukung — bukan menyalin nilai pihak lain.
- Lingkup = sistem SAKIP (5 komponen). Bila penugasan menyasar kualitas dokumen LKj saja → gunakan **reviu-umum** dengan kriteria LKj (skill khusus reviu-kinerja BELUM tersedia); bila menguji efektivitas program → **audit-kinerja**.

## Referensi

- `references/01-kriteria-lke-permen88-2021.md` — kriteria lengkap (79) per sub-komponen.
- `references/02-template-lhe.md` — template LHE AKIP.
- `shared-kinerja-references/PANDUAN.md` — perbandingan dasar hukum, terminologi, dan format antar skill kinerja (audit-kinerja, evaluasi-sakip, reviu-rka-kl; reviu LKj via reviu-umum).
- `panduan-format-umum/PANDUAN.md` — format Nota Dinas + LHE; sumber kebenaran doktrin unsur.

## Posisi dalam Keluarga Skill Kinerja

> Termasuk keluarga skill kinerja (audit-kinerja, evaluasi-sakip, reviu-rka-kl; reviu LKj via reviu-umum) — berpijak pada regulasi yang sama (Perpres 29/2014, PermenPAN-RB 53/2014 & 88/2021, PP 8/2006). Yang membedakan: tujuan, waktu, dan kedalaman.

| Dimensi | Evaluasi SAKIP (skill ini) | Reviu LKj | Audit Kinerja | Reviu RKA/KL |
|---|---|---|---|---|
| Tujuan | Nilai implementasi sistem SAKIP (5 komponen) | Keandalan penyajian LKj | Efektivitas/efisiensi/ekonomis program | Kesesuaian & kualitas perencanaan anggaran |
| Tingkat keyakinan | **Terbatas (evaluatif)** | Terbatas | Memadai | Terbatas |
| Objek | Sistem SAKIP (5 komponen, nilai 0–100) | Dokumen LKj final | Program prioritas tertentu | Dokumen RKA/KL |
| Elemen | **LKE: predikat/skor + AoI (TANPA Sebab)** | Tabel 3 aspek + catatan (Sebab diisi) | K/K/**S**/A/R | Catatan per aspek (Sebab diisi) |
| Output | LHE SAKIP + nilai/predikat | LHR + Pernyataan Telah Direviu | LHA Kinerja | LHR RKA/KL |

> **Pilih evaluasi SAKIP** ketika KemenPAN-RB atau pimpinan meminta penilaian implementasi sistem akuntabilitas kinerja instansi secara menyeluruh. Reviu LKj adalah BAGIAN dari komponen Pelaporan Kinerja dalam evaluasi SAKIP.
