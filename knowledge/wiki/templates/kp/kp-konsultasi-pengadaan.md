---
jenis: kp_template
skill: konsultasi-pengadaan
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
  - "pattern: KSP-57..KSP-59 dari temuan-patterns/konsultasi-pengadaan/"
  - "Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021, Perpres 46/2025"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Pendampingan/Konsultasi Pengadaan Barang/Jasa (Advisory)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021, Perpres 46/2025

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Mendampingi unit kerja secara berkelanjutan dan preventif dalam proses pengadaan barang/jasa (penyusunan dokumen perencanaan hingga pelaksanaan), bersifat advisory dan tidak menggantikan keputusan PPK/PA/KPA.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Kegiatan pendampingan paket/proses pengadaan sesuai permintaan unit kerja — hadir di rapat penyusunan KAK/spesifikasi, reviu draft HPS sebelum tender, dan klarifikasi prosedur saat proses berjalan.

## Sasaran Pengawasan

Sasaran baku untuk skill `konsultasi-pengadaan` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Mendampingi penyusunan dokumen perencanaan pengadaan (KAK/spesifikasi)
- Mendampingi penyusunan & reviu HPS sebelum tender
- Memberi advisory atas kewajaran metode pemilihan penyedia
- Mencatat kegiatan pendampingan/klarifikasi prosedur saat proses berjalan (KSP-59)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[KSP-57]]..[[KSP-59]] (E-Katalog tanpa mini-kompetisi, pemaketan/spesifikasi belum jelas, Itjen advisor pra-pengadaan)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. Perpres 12/2021; Perlem LKPP 12/2021; Perpres 46/2025)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/konsultasi-pengadaan/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Pendampingan = advisory/preventif pra-pengadaan, tanpa keyakinan, tidak mengikat; output Laporan Hasil Pendampingan, bukan LHA/LHR.*
