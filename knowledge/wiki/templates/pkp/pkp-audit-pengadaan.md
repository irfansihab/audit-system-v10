---
jenis: pkp_template
skill: audit-pengadaan
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
  - "pattern: AP-23..AP-29 (temuan-patterns/audit-pengadaan)"
  - "regulasi: Perpres 16/2018 jo. 12/2021; Perpres 46/2025 Ps. 9(1)f²"
  - "konteks: pola-temuan-berulang (Pola 1,2,8,9)"
---

# Program Kerja Pengawasan (PKP) — Audit Pengadaan Barang/Jasa

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari KP, Surat Tugas, dan hasil Survei Pendahuluan (profil risiko pengadaan)
- Pahami tujuan, sasaran, dan ruang lingkup audit pengadaan
- Tetapkan kriteria: Perpres 16/2018 jo. 12/2021, Peraturan LKPP, kontrak & spesifikasi teknis
- Petakan siklus pengadaan yang diaudit (perencanaan → pemilihan → kontrak → pelaksanaan → pembayaran/serah terima)
- Susun program kerja terinci, jadwal, dan alokasi anggota tim per sasaran
- Identifikasi & minta dokumen: KAK/TOR, HPS, dokumen pemilihan, kontrak, BAST, dokumen pemeriksaan/penerimaan, bukti bayar

## II. Pelaksanaan

Sasaran baku untuk skill `audit-pengadaan` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai kesesuaian perencanaan pengadaan dengan kebutuhan riil dan ketentuan
  - Telaah KAK/TOR & identifikasi kebutuhan vs volume yang diadakan
  - Periksa kewajaran HPS (sumber harga independen) dan status RUP/SIRUP
- Menilai kepatuhan proses pemilihan penyedia
  - Telaah metode pemilihan, dokumen pemilihan, dan evaluasi penawaran
  - Periksa keabsahan kontrak/SPK dan adendum (nomor, tanggal, substansi)
- Menguji kesesuaian output pekerjaan dengan kontrak/KAK/spesifikasi teknis
  - Bandingkan barang/jasa yang diterima vs spesifikasi dan volume kontrak
  - Telaah dokumen pemeriksaan/penerimaan oleh PPK/tim teknis atas barang yang diterima
- Menguji kewajaran pembayaran terhadap output yang benar-benar diterima
  - Cocokkan nilai pembayaran dengan kuantitas/kualitas output yang diterima (deteksi kelebihan bayar)
  - Telaah pembayaran retroaktif/tanpa kontrak terhadap syarat Perpres 46/2025 & LKPP
- Menilai kecukupan bukti pendukung output pekerjaan
  - Pastikan setiap output didukung bukti pemeriksaan/pengujian yang memadai
  - Telaah pemantauan SLA/prestasi pekerjaan dan penerapan denda bila ada

## III. Pelaporan

- Kompilasi & reviu kertas kerja (KKP) berikut bukti pendukung
- Susun temuan (Kondisi–Kriteria–Sebab–Akibat) + kodefikasi temuan SIM-HP
- Bahas temuan dengan auditi (exit meeting/konfirmasi) dan minta tanggapan
- Susun draft Laporan Hasil Audit (LHA) + rekomendasi yang dapat ditindaklanjuti
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi via SIMWAS

## Sumber Wiki Terkait

- Pattern: [[AP-23]]..[[AP-29]] (pekerjaan tanpa kontrak, SLA tak termonitor, data prestasi tak memadai, pembayaran retroaktif, vendor lock-in, kelebihan bayar, kurs/klasifikasi akun)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. 12/2021; Perpres 46/2025 Ps. 9(1)f²)
- Konteks: [[pola-temuan-berulang]] (Pola 1 kontrak tanpa kontrak, Pola 8 anomali administrasi kontrak)
- PANDUAN substansi: `knowledge/skills/audit-pengadaan/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP). Setiap audit didahului Survei Pendahuluan.*
