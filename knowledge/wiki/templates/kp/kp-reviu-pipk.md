---
jenis: kp_template
skill: reviu-pipk
versi: 1.0
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
  - "regulasi: PMK 17/PMK.09/2019 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Kartu Penugasan — Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PMK 17/PMK.09/2019 (Pedoman Penerapan, Penilaian & Reviu PIPK — mengganti PMK 14/2017), PP 60/2008 (SPIP, 5 unsur).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas atas kualitas penilaian PIPK yang dilakukan Tim Penilai (entitas), termasuk kewajaran simpulan efektivitas pengendalian intern atas pelaporan keuangan.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Reviu atas dokumen penilaian PIPK entitas: penetapan lingkup, RCM, hasil pengujian PITE dan tingkat proses/transaksi (ToC/CSA), klasifikasi defisiensi, serta CHR/LHR PIPK dan PTD.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-pipk` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai penetapan lingkup & identifikasi risiko pelaporan keuangan
- Menilai penilaian Pengendalian Intern Tingkat Entitas (PITE)
- Menilai pengendalian tingkat proses/transaksi
- Menilai pengujian pengendalian (ToC) & CSA
- Menilai simpulan efektivitas & rencana perbaikan
- Menilai keandalan dokumentasi PIPK

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern khusus PIPK belum ada — pakai [[pola-temuan-berulang]] + regulasi-kunci seksi PIPK.
- Regulasi: [[regulasi-kunci]] (PMK 17/PMK.09/2019 dkk. (lihat SKILL.md))
- PANDUAN substansi: `knowledge/skills/reviu-pipk/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
