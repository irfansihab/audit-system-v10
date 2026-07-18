---
jenis: pkp_template
skill: reviu-laporan-keuangan
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
  - "regulasi: PMK 255/PMK.09/2015 dkk. (lihat SKILL.md)"
  - "konteks: regulasi-kunci + pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Reviu Laporan Keuangan

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari KP/ST dan tetapkan kriteria reviu: PMK 255/PMK.09/2015 dkk. (lihat SKILL.md)
- Identifikasi & minta dokumen sumber yang diperlukan per sasaran (lihat kontrak dokumen skill)
- Alokasikan anggota tim per sasaran + jadwal per langkah

## II. Pelaksanaan

Sasaran baku untuk skill `reviu-laporan-keuangan` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai kesesuaian penyajian LK dengan SAP (basis akrual)
  - Telaah struktur & pos LRA/Neraca/LO/LPE terhadap PP 71/2010 (PSAP) + Buletin Teknis
  - Uji saldo normal & keterkaitan antar-laporan (mis. surplus/defisit LO → LPE)
- Menilai kelengkapan & keandalan CaLK
  - Telaah pengungkapan wajib: kebijakan akuntansi, rincian pos material, kejadian penting
  - Cocokkan angka CaLK vs face LK (PMK 100/2025 per pos)
- Menilai hasil rekonsiliasi (SAKTI↔SPAN, internal, BMN, kas)
  - Telaah BAR & selisih/suspend — tiap selisih wajib terjelaskan (PMK 171/2021 jo. 158/2023; PMK 232/2022)
  - Telusuri tindak lanjut selisih periode sebelumnya
- Menilai akurasi saldo & klasifikasi akun (BAS)
  - Uji ketepatan penggunaan akun per PMK 214/2013 jo. 42/2025
  - Tandai akun suspend/salah klasifikasi material
- Menilai kepatuhan proses penyusunan & reviu berjenjang
  - Telaah jenjang unit akuntansi + jadwal penyampaian (PMK 232/2022)
  - Pastikan kelengkapan menuju Pernyataan Telah Direviu (PMK 255/2015)
- Menilai tindak lanjut temuan berdampak LK
  - Telusuri koreksi atas temuan BPK/reviu terdahulu yang memengaruhi saldo/penyajian (LHP BPK + status TLHP)

## III. Pelaporan

- Kompilasi catatan hasil reviu per aspek di Kertas Kerja (KKP) — K/K/S/A, Sebab anti-mengarang
- Susun simpulan dengan bahasa keyakinan terbatas + konfirmasi/tanggapan unit yang direviu
- Susun draft Laporan Hasil Reviu (LHR) + kelengkapan sesuai skill (mis. Pernyataan Telah Direviu bila dipersyaratkan)
- Reviu berjenjang KT → PT sebelum finalisasi

---

*Disusun Ketua Tim (KT) di tahapan 2 dari sasaran KP; sasaran tersinkron ke `_PKP/sasaran-assignment.json`.*
