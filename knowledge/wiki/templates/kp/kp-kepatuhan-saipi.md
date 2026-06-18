---
jenis: kp_template
skill: kepatuhan-saipi
versi: 2.0
output_format: docx
field_required:
  - nomor_st
  - tanggal_st
  - judul_penugasan
  - tujuan_pengawasan
  - ruang_lingkup
  - jadwal_mulai
  - jadwal_selesai
  - tim_pengawasan
field_optional:
  - referensi_regulasi
  - dasar_penugasan_tambahan
  - catatan_pt
sumber_wiki:
  - "pattern: SAIPI-60..SAIPI-66 dari temuan-patterns/kepatuhan-saipi/"
  - "PER-01/AAIPI/DPN/2021 (SAIPI), IPPF 2017, PP 60/2008, IACM"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Penilaian Kepatuhan SAIPI / Penjaminan Mutu APIP

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PER-01/AAIPI/DPN/2021 (Standar Audit Intern Pemerintah Indonesia/SAIPI), IPPF 2017, PP 60/2008, dan kerangka IACM

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Menilai kepatuhan penyelenggaraan pengawasan APIP terhadap Standar Audit Intern Pemerintah Indonesia (SAIPI) — Standar Atribut (1100, 1200, 1300) dan Standar Kinerja (2200, 2300, 2400) — sebagai dasar penjaminan mutu dan penguatan kapabilitas APIP.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Telaah framework tata kelola APIP (Piagam Audit Intern, KKSAR, Pedoman, SOP, dokumen IACM), telaah sejawat/QAIP, register risiko fraud, dan sampel KKA/KKP/LHP, dinilai per elemen/standar SAIPI.

## Sasaran Pengawasan

Sasaran baku untuk skill `kepatuhan-saipi` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kepatuhan Piagam Audit Intern & program jaminan/peningkatan mutu (SAIPI-60, SAIPI-63, SAIPI-66)
- Menilai kepatuhan perencanaan penugasan & sasaran (SAIPI-62, SAIPI-64)
- Menilai kepatuhan pelaksanaan & dokumentasi penugasan (SAIPI-65)
- Menilai kepatuhan komunikasi hasil penugasan (SAIPI-61)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[SAIPI-60]]..[[SAIPI-66]] (Piagam belum diperbarui, terminologi non-baku, PIA belum memadai, telaah sejawat kedaluwarsa, register risiko fraud, KKA tanpa root cause, framework APIP multi-elemen)
- Regulasi: [[regulasi-kunci]] (PER-01/AAIPI/DPN/2021 — SAIPI; IPPF 2017; PP 60/2008; IACM)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/kepatuhan-saipi/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Output = laporan penilaian kepatuhan SAIPI/QAIP + rekomendasi penguatan kapabilitas APIP.*
