---
jenis: kp_template
skill: default
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
  - "konteks: pola-temuan-berulang, regulasi-kunci"
  - "PANDUAN skill spesifik penugasan"
---

# Kartu Penugasan — Default (fallback lintas skill)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Sesuai jenis pengawasan — rujuk regulasi-kunci di wiki dan PANDUAN skill terkait.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memperoleh hasil pengawasan yang memadai atas kesesuaian objek terhadap kriteria/standar yang berlaku, serta merumuskan simpulan dan rekomendasi perbaikan.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Objek pengawasan sesuai Surat Tugas, periode dan unit kerja yang ditetapkan.

## Sasaran Pengawasan

Sasaran baku untuk skill `default` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan) — sesuaikan dengan PANDUAN skill:

- Menilai kesesuaian objek pengawasan terhadap kriteria/standar yang berlaku
- Mengidentifikasi simpulan/temuan substantif beserta dampaknya
- Merumuskan rekomendasi/saran perbaikan

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Konteks: [[pola-temuan-berulang]], [[regulasi-kunci]], [[glossary-komdigi]]
- PANDUAN substansi: `knowledge/skills/<skill>/SKILL.md`

---

*Template fallback. Untuk skill spesifik, gunakan `kp-<skill>.md`. Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
