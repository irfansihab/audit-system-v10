---
jenis: kp_template
skill: reviu-rka-kl
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
  - "pattern: RKA-01 dari temuan-patterns/reviu-rka-kl/"
  - "PMK 107/2024 (perubahan PMK 62/PMK.02/2023) Pasal 61; Kriteria IR2"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Reviu RKA-K/L

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PMK 107/2024 (perubahan PMK 62/PMK.02/2023) Pasal 61 tentang Petunjuk Penyusunan dan Penelaahan RKA-K/L, Kriteria IR2, serta PMK SBM/SBK tahun anggaran berkenaan.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas atas kelengkapan dan substansi TOR, kerangka logis Rincian Output, serta kewajaran biaya RKA-K/L sesuai PMK 107/2024 Pasal 61 dan Kriteria IR2.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Desk review dokumen TOR/KAK, RAB, dan RKA-Satker per Rincian Output (RO) untuk tahap pagu yang ditetapkan, dibandingkan terhadap SBM/SBK tahun anggaran berkenaan.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-rka-kl` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kelengkapan dan substansi TOR (7 blok Kriteria IR2)
- Menilai kerangka logis dan parameter keberhasilan Rincian Output (RO)
- Menilai kecukupan komponen/sub-komponen dan cost analysis terhadap output
- Menilai kewajaran biaya (RAB vs SBM/SBK) dan konsistensi TOR ↔ RAB

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[RKA-01]]..[[RKA-07]] (TOR 7 blok, RO tanpa parameter keberhasilan, komponen belum cukup, TOR tanpa metode pengadaan, ketidakselarasan metode-tahapan, cost analysis belum ada, indikator OM tidak sesuai prinsip)
- Regulasi: [[regulasi-kunci]] (PMK 107/2024 Pasal 61; Kriteria IR2; PMK SBM/SBK tahun berjalan)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/reviu-rka-kl/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
