# Templates Wiki — KP & PKP

Template ini dipakai oleh:
- **PT (Pengendali Teknis)** saat mengisi Kartu Penugasan (KP) di tahapan 1
- **KT (Ketua Tim)** saat mendetailkan KP menjadi Program Kerja Pengawasan (PKP) di tahapan 2

## Struktur

- `kp/kp-<skill>.md` — Template Kartu Penugasan per skill
- `pkp/pkp-<skill>.md` — Template Program Kerja Pengawasan per skill

## Format

Template pakai placeholder `{{field_name}}` yang akan diisi via form UI INTEGRAL AI Workspace.

Field metadata di frontmatter:
- `field_required`: list field yang wajib diisi
- `field_optional`: field opsional
- `output_format`: format hasil render (umumnya `docx`)
- `sumber_wiki`: pointer ke pattern/regulasi/konteks terkait (untuk telusur sumber)

### Format PKP v2.0 — STRUKTUR WAJIB (dibaca parser impor UI)

Tombol **"Import dari Wiki"** di tab PKP mem-parse template mengikuti **format INTEGRAL**
(I. Perencanaan / II. Pelaksanaan / III. Pelaporan). Heading & struktur bullet **harus persis**,
kalau tidak impor tak menemukan isinya:

- `## I. Perencanaan` → tiap bullet flat `- …` → langkah kerja kelompok **I. Perencanaan**.
- `## II. Pelaksanaan` → harus ada baris memuat teks **"Sasaran baku"**, lalu daftar:
  bullet **top-level** `- …` = baris **Sasaran** (deskripsi); **sub-bullet** indentasi 2 spasi
  `  - …` = **Langkah Kerja** sasaran tsb.
- `## III. Pelaporan` → tiap bullet flat `- …` → langkah kerja kelompok **III. Pelaporan**.

Impor hanya mengisi I/III bila masih kosong (tak menimpa isian KT); sasaran di-dedup by deskripsi.
Implementasi parser: `frontend/app/penugasan/[id]/page.tsx`
(`extractSasaranBakuFromTemplate`, `extractLangkahSection`).

## Skill yang ter-cover (17 skill + 1 default)

Satu template PKP & KP per skill di `knowledge/skills/` (kecuali `*-shared`/`graduasi`/`panduan`):

`audit-kinerja`, `audit-pengadaan`, `audit-umum`, `evaluasi-manajemen-risiko`,
`evaluasi-reformasi-birokrasi`, `evaluasi-sakip`, `evaluasi-spip`, `evaluasi-umum`,
`kepatuhan-saipi`, `konsultansi-umum`, `konsultasi-pengadaan`, `pemantauan-pengadaan`,
`pemantauan-tindak-lanjut`, `pemantauan-umum`, `reviu-pengadaan`, `reviu-rka-kl`, `reviu-umum`
— plus `default` (fallback).

> Backend `/knowledge/templates/{kind}?skill=` mem-filter by skill dan selalu menyertakan
> `default` sebagai fallback. Menambah skill baru = tambah file `pkp-<skill>.md` + `kp-<skill>.md`.
>
> **Status:** template **PKP** dan **KP** sudah lengkap 17 skill + default (format v2.0).

### Impor KP (Kartu Penugasan)

Tombol **"Import dari Wiki — Pakai Template KP"** di tab KP:
- `## Tujuan Pengawasan` / `## Ruang Lingkup` / `## Dasar Hukum & Referensi Regulasi`
  → mengisi field Tujuan/Ruang Lingkup/Dasar **hanya bila kosong** (baris ber-`{{ }}` dilewati;
  jadi teks "baku" harus baris biasa).
- `## Sasaran Pengawasan` dengan baris **"Sasaran baku"** + bullet `- …` → daftar **Sasaran KP**
  (otomatis **sync ke PKP** saat KP disimpan). Sasaran KP & PKP per skill sengaja **identik**.
