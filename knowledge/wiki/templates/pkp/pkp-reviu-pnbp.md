---
jenis: pkp_template
skill: reviu-pnbp
versi: 1.0
output_format: docx
field_required:
  - nomor_pkp
  - sasaran_list
  - langkah_kerja_list
  - tim_anggota_assignment
field_optional:
  - referensi_kp
  - risk_profile
  - timeline_per_langkah
sumber_wiki:
  - "regulasi: UU 9/2018 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Reviu Pengelolaan PNBP

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari KP/ST dan tetapkan kriteria reviu: UU 9/2018 dkk. (lihat SKILL.md)
- Identifikasi & minta dokumen sumber yang diperlukan per sasaran (lihat kontrak dokumen skill)
- Alokasikan anggota tim per sasaran + jadwal per langkah

## II. Pelaksanaan

Sasaran baku untuk skill `reviu-pnbp` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai kesesuaian jenis & tarif PNBP dengan PP berlaku
  - Uji jenis yang dipungut vs daftar PP 43/2023 Ps.1–3, 10 (BHP ISR/IPFR); cek tarif Rp0/0% per Permen Kominfo 1/2024
- Menilai akurasi penetapan/penghitungan PNBP terutang
  - Uji hitung per wajib bayar: formula ISR (PP 43/2023 Ps.3) / IPFR (Ps.10); PMK 155 jo.58/2023 Ps.59–60
- Menilai penagihan & pengelolaan piutang PNBP
  - Telaah pembayaran vs jatuh tempo (PMK 155 Ps.41); tunggakan → piutang (Ps.42); umur & optimalisasi (Ps.55A)
- Menilai ketepatan waktu & jumlah penyetoran ke Kas Negara
  - Cocokkan bukti setor SIMPONI/SSBP vs penetapan (UU 9/2018; PMK 155)
- Menilai penggunaan dana PNBP sesuai izin
  - Telaah kesesuaian penggunaan dgn izin & Pagu Penggunaan Dana PNBP (PMK 155 jo.58/2023 Ps.108 dst.)
- Menilai penatausahaan & pelaporan (termasuk rekonsiliasi)
  - Telaah pencatatan, laporan, dan BAR rekonsiliasi triwulanan ≤1 bulan (PMK 155 Ps.135)

## III. Pelaporan

- Kompilasi catatan hasil reviu per aspek di Kertas Kerja (KKP) — K/K/S/A, Sebab anti-mengarang
- Susun simpulan dengan bahasa keyakinan terbatas + konfirmasi/tanggapan unit yang direviu
- Susun draft Laporan Hasil Reviu (LHR) + kelengkapan sesuai skill (mis. Pernyataan Telah Direviu bila dipersyaratkan)
- Reviu berjenjang KT → PT sebelum finalisasi

---

*Disusun Ketua Tim (KT) di tahapan 2 dari sasaran KP; sasaran tersinkron ke `_PKP/sasaran-assignment.json`.*
