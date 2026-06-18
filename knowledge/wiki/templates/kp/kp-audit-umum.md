---
jenis: kp_template
skill: audit-umum
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
  - "pattern: AU-01 dari temuan-patterns/audit-umum/"
  - "kriteria yang diunggah auditor (regulasi/SOP/SK/juklak di input/kriteria/)"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Audit Umum (Criteria-Driven)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PP 60/2008 tentang SPIP dan Standar Audit Intern Pemerintah Indonesia (AAIPI); kriteria substantif diunggah auditor ke `input/kriteria/` (regulasi/SOP/SK/juklak — criteria-driven, tanpa regulasi baku tunggal). Kode surat PW.04.04.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan memadai atas kepatuhan/kewajaran objek yang diaudit terhadap kriteria yang diunggah auditor, serta menggali sebab ketidaksesuaian agar rekomendasi menyentuh sistem.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Kepatuhan/kewajaran objek audit terhadap seluruh kriteria di `input/kriteria/` — diuji per-elemen/per-pasal (bukan global), dengan klasifikasi materialitas (catatan administratif <Rp 10 jt, reguler Rp 10 jt–Rp 500 jt, material >Rp 500 jt, prioritas tinggi >Rp 1 M). Dipakai bila belum ada skill audit topik spesifik.

## Sasaran Pengawasan

Sasaran baku untuk skill `audit-umum` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kelengkapan dokumen pendukung objek audit terhadap kriteria yang diunggah (pattern AU-01).
- Menguji konsistensi data antardokumen pendukung (pattern AU-02).
- Menguji kepatuhan terhadap prosedur baku/regulasi yang diunggah (pattern AU-03).
- Mengukur nilai dan tingkat materialitas atas ketidaksesuaian yang ditemukan.

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[au-01-01-kelengkapan-dokumen]], [[au-02-02-konsistensi-data]], [[au-03-03-kepatuhan-prosedur]] (dari temuan-patterns/audit-umum/)
- Regulasi: [[regulasi-kunci]] (kriteria yang diunggah auditor di `input/kriteria/` — criteria-driven; tidak ada regulasi baku tunggal)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/audit-umum/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Setiap audit didahului Survei Pendahuluan.*
