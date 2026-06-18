---
jenis: kp_template
skill: reviu-umum
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
  - "pattern: RV-01 dari temuan-patterns/reviu-umum/"
  - "kriteria reviu = juklak/juknis/SOP/format yang diunggah auditor"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Reviu Umum (Criteria-Driven)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Kriteria reviu bersifat criteria-driven: dokumen acuan yang berlaku (juklak/juknis/SOP/format/peraturan internal) yang diunggah auditor.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas ("nothing has come to our attention") atas kepatuhan dokumen/proses administratif terhadap kriteria yang ditetapkan, tanpa menggali akar masalah.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Desk review terbatas atas dokumen/proses administratif-prosedural hanya pada hal yang dipersyaratkan oleh kriteria acuan (juklak/juknis/SOP/format) yang diunggah auditor.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-umum` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kelengkapan dokumen/persyaratan terhadap kriteria yang ditetapkan
- Menilai konsistensi data antar dokumen pendukung
- Menilai kepatuhan format dan substansi minimal terhadap kriteria
- Menilai kepatuhan prosedur/tahapan terhadap juklak/juknis/SOP

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[RV-01]]..[[RV-03]] (kelengkapan dokumen, konsistensi data, kepatuhan prosedur — starter generic)
- Regulasi: [[regulasi-kunci]] (kriteria reviu = dokumen acuan/juklak/juknis/SOP/format yang diunggah auditor)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/reviu-umum/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
