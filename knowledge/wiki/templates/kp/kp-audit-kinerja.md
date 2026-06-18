---
jenis: kp_template
skill: audit-kinerja
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
  - "pattern: AK-17 dari temuan-patterns/audit-kinerja/"
  - "PP 60/2008, PP 8/2006, Standar Audit Intern Pemerintah Indonesia (AAIPI)"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Audit Kinerja (Efektivitas & Efisiensi)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PP 60/2008 tentang SPIP, PP 8/2006 tentang Pelaporan Keuangan dan Kinerja Instansi Pemerintah, dan Standar Audit Intern Pemerintah Indonesia (AAIPI).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memperoleh keyakinan memadai atas efektivitas pencapaian tujuan/target program serta efisiensi penggunaan sumber daya (anggaran, aset, SDM), dan menggali sebab gap kinerja agar rekomendasi menyentuh sistem.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Dimensi Efektivitas & Efisiensi (2E) atas pelaksanaan program/kegiatan — desain logika intervensi, proses bisnis/pengendalian, capaian output–outcome, dan validitas data kinerja; ekonomisitas/kewajaran harga pengadaan di luar lingkup (eskalasi ke audit-pengadaan). Sasaran & ruang lingkup ditajamkan melalui Survei Pendahuluan, bukan disalin verbatim dari Surat Tugas.

## Sasaran Pengawasan

Sasaran baku untuk skill `audit-kinerja` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menguji efektivitas pencapaian target output dan outcome program (aspek 6–7; pattern AK-21).
- Menguji efektivitas sistem/teknologi pengendalian dan proses bisnis program (aspek 4; pattern AK-17, AK-18).
- Menguji efisiensi penggunaan sumber daya (anggaran, aset, SDM) program (aspek 3 & 5; pattern AK-19).
- Menguji validitas data kinerja dan desain indikator program (aspek 1 & 8; pattern AK-21, AK-22).

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[AK-17-sistem-pengendalian-bypass]], [[AK-18-hasil-deteksi-tidak-ditindaklanjuti]], [[AK-19-tumpang-tindih-fungsi]], [[AK-21-capaian-tidak-traceable]], [[AK-22-formula-tarif-belum-cerminkan-nilai]] (dari temuan-patterns/audit-kinerja/)
- Regulasi: [[regulasi-kunci]] (PP 60/2008, PP 8/2006, Standar Audit Intern Pemerintah Indonesia (AAIPI); kriteria teknis dari proses bisnis/SOP/PK program)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/audit-kinerja/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Setiap audit didahului Survei Pendahuluan.*
