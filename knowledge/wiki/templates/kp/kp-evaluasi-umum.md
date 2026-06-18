---
jenis: kp_template
skill: evaluasi-umum
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
  - "pattern: EV-01 dari temuan-patterns/evaluasi-umum/"
  - "kerangka kriteria evaluasi yang disepakati per penugasan"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Evaluasi Umum

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Kriteria evaluasi disepakati per penugasan (Permen/Perdirjen, rencana strategis, atau SOP objek evaluasi yang relevan).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Menilai secara substantif efektivitas sistem/program/kebijakan terhadap kriteria yang disepakati (evaluasi — keyakinan terbatas).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Objek evaluasi (program/kebijakan/sistem) beserta dokumen pendukungnya pada periode yang dievaluasi.

## Sasaran Pengawasan

Sasaran baku untuk skill `evaluasi-umum` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kesesuaian objek evaluasi terhadap kriteria yang ditetapkan
- Menilai efektivitas pencapaian tujuan program/kebijakan/sistem
- Menguji kelengkapan dan keandalan dokumen pendukung
- Menilai kepatuhan terhadap prosedur baku yang berlaku

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[EV-01]] (kelengkapan dokumen pendukung; lihat juga EV-02, EV-03)
- Regulasi/Pedoman: [[regulasi-kunci]] (kriteria evaluasi yang disepakati per penugasan)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-umum/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
