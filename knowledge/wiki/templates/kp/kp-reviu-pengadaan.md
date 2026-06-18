---
jenis: kp_template
skill: reviu-pengadaan
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
  - "pattern: RP-08 dari temuan-patterns/reviu-pengadaan/"
  - "Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Reviu Pengadaan Barang/Jasa

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Perpres 16/2018 jo. Perpres 12/2021 tentang Pengadaan Barang/Jasa Pemerintah, serta Peraturan LKPP 12/2021.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas atas kememadaian justifikasi perencanaan, kewajaran HPS, dan kewajaran metode pemilihan pengadaan barang/jasa.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Desk review dokumen tahap perencanaan dan pemilihan — KAK/TOR, HPS dan dokumen pembentuk harga (RFI), rancangan/dokumen kontrak.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-pengadaan` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kememadaian justifikasi dan kelengkapan dokumen perencanaan (KAK)
- Menilai kewajaran HPS dan dukungan sumber harga
- Menilai konsistensi antar dokumen (KAK ↔ HPS ↔ Kontrak)
- Menilai kewajaran metode pemilihan penyedia

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[RP-08]]..[[RP-16]] (HPS multi-source, pekerjaan tanpa kontrak, adendum nomor ganda, SIRUP draft, kajian tanpa rencana aksi, confidentiality audit-trail, perpanjangan lisensi, e-katalog tanpa negosiasi, vendor belum berkontrak)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. Perpres 12/2021; Perlem LKPP 12/2021)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/reviu-pengadaan/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
