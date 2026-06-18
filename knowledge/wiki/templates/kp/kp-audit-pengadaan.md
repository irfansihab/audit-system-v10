---
jenis: kp_template
skill: audit-pengadaan
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
  - "pattern: AP-23..AP-29 (temuan-patterns/audit-pengadaan)"
  - "regulasi: Perpres 16/2018 jo. 12/2021; Perpres 46/2025 Ps. 9(1)f²"
  - "konteks: pola-temuan-berulang (Pola 1,8)"
---

# Kartu Penugasan — Audit Pengadaan Barang/Jasa

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Perpres 16/2018 jo. Perpres 12/2021, Peraturan LKPP terkait, Perpres 46/2025 Pasal 9 ayat (1) huruf f angka 2.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memperoleh keyakinan memadai atas kepatuhan proses pengadaan, kewajaran HPS, kesesuaian output dengan kontrak/KAK/spesifikasi, dan kewajaran pembayaran terhadap output yang diterima.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Seluruh siklus pengadaan — perencanaan, pemilihan, kontrak, pelaksanaan, hingga pembayaran & serah terima.

## Sasaran Pengawasan

Sasaran baku untuk skill `audit-pengadaan` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kesesuaian perencanaan pengadaan dengan kebutuhan riil dan ketentuan
- Menilai kepatuhan proses pemilihan penyedia
- Menguji kesesuaian output pekerjaan dengan kontrak/KAK/spesifikasi teknis
- Menguji kewajaran pembayaran terhadap output yang benar-benar diterima
- Menilai kecukupan bukti pendukung output pekerjaan

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[AP-23]]..[[AP-29]] (temuan-patterns/audit-pengadaan)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. 12/2021; Perpres 46/2025 Ps. 9(1)f²)
- Konteks: [[pola-temuan-berulang]] (Pola 1, 8)
- PANDUAN substansi: `knowledge/skills/audit-pengadaan/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP). Setiap audit didahului Survei Pendahuluan.*
