---
jenis: kp_template
skill: reviu-laporan-keuangan
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
  - "regulasi: PMK 255/PMK.09/2015 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Kartu Penugasan — Reviu Laporan Keuangan

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PMK 255/PMK.09/2015 (Standar Reviu atas LK K/L), PP 71/2010 (SAP) + PMK 100/2025 (Kebijakan Akuntansi, LK TA 2025+; TA<2025: PMK 231/2022 jo. 57/2023), PMK 171/2021 jo. 158/2023 (SAKTI), PMK 214/2013 jo. 42/2025 (BAS), PMK 232/2022 (SAPKI).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas bahwa Laporan Keuangan disusun sesuai Standar Akuntansi Pemerintahan (SAP) dan bebas dari salah saji material, sebagai dasar Pernyataan Telah Direviu (PMK 255/2015).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Desk review atas LRA/Neraca/LO/LPE + CaLK, hasil rekonsiliasi (SAKTI↔SPAN, BMN, kas), dan proses penyusunan LK periode berkenaan. Reviu bukan audit — tidak memberikan opini.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-laporan-keuangan` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kesesuaian penyajian LK dengan SAP (basis akrual)
- Menilai kelengkapan & keandalan CaLK
- Menilai hasil rekonsiliasi (SAKTI↔SPAN, internal, BMN, kas)
- Menilai akurasi saldo & klasifikasi akun (BAS)
- Menilai kepatuhan proses penyusunan & reviu berjenjang
- Menilai tindak lanjut temuan berdampak LK

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[reviu-laporan-keuangan/RK-69-tagihan-om-anggaran-realisasi]], [[reviu-laporan-keuangan/RK-70-cross-dipa-transfer-control]]
- Regulasi: [[regulasi-kunci]] (PMK 255/PMK.09/2015 dkk. (lihat SKILL.md))
- PANDUAN substansi: `knowledge/skills/reviu-laporan-keuangan/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
