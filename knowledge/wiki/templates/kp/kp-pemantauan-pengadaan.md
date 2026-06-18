---
jenis: kp_template
skill: pemantauan-pengadaan
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
  - "pattern: PMP-56 dari temuan-patterns/pemantauan-pengadaan/"
  - "Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025 (Pasal 78 denda keterlambatan)"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Pemantauan Pengadaan Barang/Jasa

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025 (Pasal 78 denda keterlambatan; Pasal 18/22 perencanaan & SIRUP).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Melaporkan kondisi aktual pelaksanaan kontrak pengadaan aktif (progres fisik vs keuangan, kepatuhan jadwal/kontrak) sebagai peringatan dini, tanpa pernyataan keyakinan dan tanpa perhitungan kerugian.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Pelaksanaan kontrak aktif — progres fisik & keuangan, deliverable/milestone, amandemen/denda keterlambatan, serta status kesiapan rencana pengadaan (RUP/SIRUP) untuk paket dan periode (cut-off) tertentu.

## Sasaran Pengawasan

Sasaran baku untuk skill `pemantauan-pengadaan` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Memantau kewajaran progres fisik vs keuangan per paket kontrak (pattern PMP-56).
- Memantau realisasi deliverable/milestone vs lingkup & jadwal Kontrak/KAK (pattern PMP-56).
- Memantau pola amandemen kontrak dan kepatuhan jadwal/denda keterlambatan (pattern PMP-56).
- Memantau status kesiapan rencana pengadaan (RUP/SIRUP) dan progres pemilihan/komitmen (pattern PMP-55, PMP-53, PMP-54).

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[PMP-53]], [[PMP-54]], [[PMP-55]], [[PMP-56]] (dari temuan-patterns/pemantauan-pengadaan/)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025 — Pasal 78 denda keterlambatan, Pasal 18/22 perencanaan & SIRUP)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-pengadaan/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
