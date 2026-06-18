---
jenis: kp_template
skill: konsultansi-umum
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
  - "pattern: KS-01..KS-03 dari temuan-patterns/konsultansi-umum/"
  - "SAIPI Par. 2010 (consulting activity) + dasar hukum spesifik pertanyaan"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Konsultansi Umum (Advisory)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

SAIPI (PER-01/AAIPI/DPN/2021) Par. 2010 — consulting activity, serta dasar hukum spesifik sesuai pertanyaan unit kerja

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan pendapat/saran berbasis dasar hukum atas pertanyaan teknis unit kerja, tanpa memberikan keyakinan dan tidak menggantikan keputusan pejabat berwenang (advisory, tidak mengikat).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Sesuai pertanyaan tertulis unit kerja — pertanyaan dirumuskan presisi (yang dijawab dan yang TIDAK dijawab), terbatas pada telaah dasar hukum dan penyusunan pendapat/saran.

## Sasaran Pengawasan

Sasaran baku untuk skill `konsultansi-umum` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Memetakan pertanyaan/kebutuhan asistensi unit kerja secara presisi
- Menelaah dasar hukum & menyusun pendapat/saran advisory per pertanyaan
- Menilai kelengkapan & konsistensi dokumen pendukung yang menjadi konteks (KS-01, KS-02)
- Memberi catatan kepatuhan terhadap prosedur baku sebagai masukan advisory (KS-03)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[KS-01]]..[[KS-03]] (kelengkapan dokumen, konsistensi data, kepatuhan prosedur — starter generic)
- Regulasi: [[regulasi-kunci]] (SAIPI Par. 2010 consulting activity + dasar hukum spesifik pertanyaan)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/konsultansi-umum/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Konsultansi = advisory, tanpa keyakinan, tidak mengikat; output Memo Konsultasi / Laporan Pendampingan, bukan LHA/LHR.*
