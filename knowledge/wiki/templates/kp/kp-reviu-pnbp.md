---
jenis: kp_template
skill: reviu-pnbp
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
  - "regulasi: UU 9/2018 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Kartu Penugasan — Reviu Pengelolaan PNBP

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

UU 9/2018 (PNBP), PP 43/2023 (Jenis & Tarif PNBP Kominfo/Komdigi — ganti PP 80/2015), PMK 155/PMK.02/2021 jo. PMK 58/2023 (Tata Cara Pengelolaan PNBP), Permen Kominfo 1/2024 (tarif Rp0/0%).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memberikan keyakinan terbatas atas kesesuaian pengelolaan PNBP (jenis & tarif, penghitungan terutang, piutang, penyetoran, penggunaan, penatausahaan & pelaporan) dengan ketentuan yang berlaku.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Desk review dokumen pengelolaan PNBP satker periode berkenaan (penetapan terutang, rekap piutang & aging, bukti setor SIMPONI/SSBP, izin & realisasi penggunaan dana, laporan & BAR rekonsiliasi). Tidak menghitung kerugian negara; indikasi kurang bayar material → eskalasi audit.

## Sasaran Pengawasan

Sasaran baku untuk skill `reviu-pnbp` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai kesesuaian jenis & tarif PNBP dengan PP berlaku
- Menilai akurasi penetapan/penghitungan PNBP terutang
- Menilai penagihan & pengelolaan piutang PNBP
- Menilai ketepatan waktu & jumlah penyetoran ke Kas Negara
- Menilai penggunaan dana PNBP sesuai izin
- Menilai penatausahaan & pelaporan (termasuk rekonsiliasi)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[reviu-pnbp/RK-67-pnbp-overstating-pencatatan]], [[reviu-pnbp/RK-68-piutang-pnbp-lag-sinkronisasi]]
- Regulasi: [[regulasi-kunci]] (UU 9/2018 dkk. (lihat SKILL.md))
- PANDUAN substansi: `knowledge/skills/reviu-pnbp/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
