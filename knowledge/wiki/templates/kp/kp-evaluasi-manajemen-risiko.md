---
jenis: kp_template
skill: evaluasi-manajemen-risiko
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
  - "pattern: EMR-39 dari temuan-patterns/evaluasi-manajemen-risiko/"
  - "Pedoman Menkomdigi 6/2017 & ISO 31000:2018"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Evaluasi Manajemen Risiko

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Pedoman Menkomdigi Nomor 6 Tahun 2017 tentang Manajemen Risiko dan ISO 31000:2018.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Menilai efektivitas dan tingkat kematangan penyelenggaraan manajemen risiko (TKPMR) unit kerja terhadap Pedoman Menkomdigi 6/2017 (evaluasi — keyakinan terbatas).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Dokumen MR objek (Formulir 1–5) yang meliputi penetapan konteks, profil & penanganan risiko, pemantauan & pelaporan, serta komitmen/tingkat kematangan pada periode yang dievaluasi.

## Sasaran Pengawasan

Sasaran baku untuk skill `evaluasi-manajemen-risiko` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai Penetapan Konteks (Formulir 1)
- Menilai Penanganan Risiko (Formulir 3)
- Menilai Pemantauan & Pelaporan (Formulir 4–5)
- Menilai Komitmen & Tingkat Kematangan (TKPMR)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[EMR-39]] (pemantauan belum diinput; lihat juga EMR-40 s.d. EMR-43)
- Regulasi/Pedoman: [[regulasi-kunci]] (Pedoman Menkomdigi 6/2017 & ISO 31000:2018)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-manajemen-risiko/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
