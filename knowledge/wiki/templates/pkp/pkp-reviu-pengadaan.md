---
jenis: pkp_template
skill: reviu-pengadaan
versi: 2.0
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
  - "pattern: RP-08..RP-16 (temuan-patterns/reviu-pengadaan)"
  - "regulasi: Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Reviu Pengadaan Barang/Jasa

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari KP/ST dan dokumen pengadaan yang akan direviu (KAK/HPS/RFI/kontrak); tentukan scope (Perencanaan/Pemilihan/Penuh) dari KP
- Tetapkan kriteria reviu: Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021
- Uraikan sasaran generik menjadi Checklist Kelengkapan Justifikasi (kebutuhan, spesifikasi teknis & fungsi, metode pengadaan, waktu penyelesaian, output) dan ceklist kesesuaian per dokumen
- Susun langkah reviu (desk review) per aspek: KAK, HPS, metode pemilihan, kontrak
- Alokasikan anggota tim per sasaran/aspek dokumen pengadaan
- Identifikasi & minta dokumen sumber: KAK/TOR, HPS & dokumen pembentuk harga, RFI vendor, rancangan/dokumen kontrak

## II. Pelaksanaan

Sasaran baku untuk skill `reviu-pengadaan` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai kememadaian justifikasi dan kelengkapan dokumen perencanaan (KAK)
  - Telaah KAK per 5 elemen justifikasi: kebutuhan, spesifikasi teknis & fungsi, metode pengadaan, waktu, output
  - Cek kememadaian dasar kuantitas kebutuhan (jumlah pegawai/beban kerja/ABK/aset existing) untuk antisipasi over-procurement
- Menilai kewajaran HPS dan dukungan sumber harga
  - Validasi HPS didukung minimum 2 sumber harga independen (RFI valid) sesuai Perpres 16/2018 Pasal 26 ayat (5)
  - Cek breakdown komponen HPS dan konsistensi dasar hukum HPS (SBM/Pedoman) dengan Tahun Anggaran pelaksanaan
- Menilai konsistensi antar dokumen (KAK ↔ HPS ↔ Kontrak)
  - Telusuri keterhubungan tiap kebutuhan teknis KAK ke line item HPS dan klausul kontrak
  - Catat komponen HPS tanpa basis di KAK atau klausul kontrak yang tidak konsisten
- Menilai kewajaran metode pemilihan penyedia
  - Cek nilai HPS terhadap ambang batas metode pemilihan (Perpres 16/2018 Pasal 41)
  - Telaah keabsahan dokumen pemilihan/kontrak (nomor, tanggal, adendum) dan kesesuaian metode dengan nilai

## III. Pelaporan

- Kompilasi hasil reviu & catatan kesesuaian per aspek di Kertas Kerja Reviu (KKP)
- Susun Catatan Hasil Reviu / simpulan kesesuaian dengan bahasa keyakinan terbatas
- Konfirmasi catatan reviu dengan unit yang direviu dan minta tanggapan
- Susun draft Laporan Hasil Reviu (LHR) + Nota Dinas pengantar
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi via SIMWAS

## Sumber Wiki Terkait

- Pattern: [[RP-08]]..[[RP-16]] (HPS multi-source, kontrak tanpa kontrak, adendum nomor ganda, SIRUP draft, kajian tanpa rencana aksi, vendor lock-in, perpanjangan lisensi, e-katalog tanpa negosiasi, vendor belum berkontrak)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. Perpres 12/2021; Perlem LKPP 12/2021)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/reviu-pengadaan/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP). Reviu = keyakinan terbatas, lingkup perencanaan–pemilihan.*
