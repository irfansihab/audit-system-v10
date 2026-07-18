---
jenis: pkp_template
skill: reviu-pipk
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
  - "regulasi: PMK 17/PMK.09/2019 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Reviu Pengendalian Intern atas Pelaporan Keuangan (PIPK)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari KP/ST dan tetapkan kriteria reviu: PMK 17/PMK.09/2019 dkk. (lihat SKILL.md)
- Identifikasi & minta dokumen sumber yang diperlukan per sasaran (lihat kontrak dokumen skill)
- Alokasikan anggota tim per sasaran + jadwal per langkah

## II. Pelaksanaan

Sasaran baku untuk skill `reviu-pipk` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai penetapan lingkup & identifikasi risiko pelaporan keuangan
  - Telaah materialitas, key business processes, akun signifikan, asersi, dan peta risiko salah saji (RCM) — PMK 17/2019
- Menilai penilaian Pengendalian Intern Tingkat Entitas (PITE)
  - Telaah cakupan 5 unsur SPIP (PP 60/2008): lingkungan pengendalian, penilaian risiko, kegiatan pengendalian, informasi-komunikasi, pemantauan
- Menilai pengendalian tingkat proses/transaksi
  - Telaah kontrol per siklus (pendapatan, belanja, aset/persediaan, kas) — memadai secara desain & dijalankan (termasuk pemisahan tugas/SoD)
- Menilai pengujian pengendalian (ToC) & CSA
  - Telaah metode & kecukupan sampel; efektivitas operasi teruji; simpulan didukung bukti
- Menilai simpulan efektivitas & rencana perbaikan
  - Uji konsistensi simpulan vs hasil pengujian; klasifikasi defisiensi (defisiensi/signifikan/material) → rencana aksi; kelengkapan CHR→LHR PIPK + PTD
- Menilai keandalan dokumentasi PIPK
  - Telaah kelengkapan & ketertelusuran kertas kerja + reviu berjenjang

## III. Pelaporan

- Kompilasi catatan hasil reviu per aspek di Kertas Kerja (KKP) — K/K/S/A, Sebab anti-mengarang
- Susun simpulan dengan bahasa keyakinan terbatas + konfirmasi/tanggapan unit yang direviu
- Susun draft Laporan Hasil Reviu (LHR) + kelengkapan sesuai skill (mis. Pernyataan Telah Direviu bila dipersyaratkan)
- Reviu berjenjang KT → PT sebelum finalisasi

---

*Disusun Ketua Tim (KT) di tahapan 2 dari sasaran KP; sasaran tersinkron ke `_PKP/sasaran-assignment.json`.*
