---
jenis: pkp_template
skill: pemantauan-pengadaan
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
  - "pattern: PMP-53, PMP-54, PMP-55, PMP-56 dari temuan-patterns/pemantauan-pengadaan/"
  - "Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025 (Pasal 78 denda keterlambatan)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Pemantauan Pengadaan Barang/Jasa

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/Surat Tugas, tujuan, ruang lingkup (paket + periode), dan paket/komitmen pengadaan yang dipantau; pemantauan = pelaporan status pelaksanaan kontrak aktif, tanpa pernyataan keyakinan dan tanpa perhitungan kerugian.
- Pelajari rekomendasi/komitmen yang dipantau dan dokumen acuan: kontrak + addendum (`02-kontrak/`), jadwal & klausul pembayaran, KAK/lingkup, serta status RUP/SIRUP dan komitmen pengadaan terkait.
- Tetapkan periode pelaporan (cut-off date) dan kriteria status pelaksanaan: 🟢 ON TRACK (deviasi progres ≤5%), 🟡 AT RISK (deviasi 5–15% atau ada isu perhatian), 🔴 DELAYED (deviasi >15% atau milestone kritis terlewati).
- Susun matriks pemantauan per paket/aspek (target progres · tenggat/milestone · bukti diminta · sumber data realisasi · kriteria status) dan alokasi tim sesuai `sasaran-assignment.json`.
- Minta bukti tindak lanjut/progres dari unit & PPK: laporan berkala penyedia, BA kemajuan (`04-pelaksanaan/`), SPM/SP2D terbit (`05-keuangan/`); jika data tidak tersedia tandai `[Data tidak tersedia — perlu konfirmasi PPK]`.

## II. Pelaksanaan

Sasaran baku untuk skill `pemantauan-pengadaan` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Memantau kewajaran progres fisik vs keuangan per paket kontrak (pattern PMP-56).
  - Kumpulkan progres fisik aktual (laporan berkala/BA kemajuan) vs target progres (jadwal kontrak) dan progres keuangan (SPM/SP2D vs nilai kontrak).
  - Hitung deviasi % progres fisik vs % pembayaran kumulatif; bayar > fisik signifikan → risiko over-payment, fisik > bayar signifikan → klaim penyedia tertunda — catat sebagai isu/risiko, bukan temuan.
  - Tetapkan status 🟢/🟡/🔴 per paket dan catat via `append_temuan` (Sebab deviasi diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data").
- Memantau realisasi deliverable/milestone vs lingkup & jadwal Kontrak/KAK (pattern PMP-56).
  - Bandingkan deliverable/milestone yang dijadwalkan sampai periode laporan dengan yang dilaporkan sudah diserahkan/dikerjakan (BA, laporan berkala penyedia/pengawas).
  - Tandai milestone jatuh tempo belum tercapai, deliverable kurang/di luar lingkup, atau output tidak sesuai cakupan KAK sebagai "kondisi perlu perhatian" + rekomendasi tindak lanjut; jangan menilai kualitas teknis fisik sendiri; indikasi serius output ≠ kontrak → eskalasi ke audit-pengadaan.
- Memantau pola amandemen kontrak dan kepatuhan jadwal/denda keterlambatan (pattern PMP-56).
  - Inventarisasi addendum: frekuensi & nilai kumulatif; addendum berulang atau kumulatif >10% nilai kontrak → indikasi perencanaan lemah (catat sebagai isu).
  - Bila ada keterlambatan milestone, hitung denda 1/1000 per hari sesuai Pasal 78 Perpres 16/2018 sebagai isu/status (bukan kerugian); catat pelanggaran SLA penyedia bila ada.
- Memantau status kesiapan rencana pengadaan (RUP/SIRUP) dan progres pemilihan/komitmen (pattern PMP-55, PMP-53, PMP-54).
  - Cek status RUP/SIRUP (mis. pagu status draft tinggi mendekati pelaksanaan — Perpres 16/2018 Pasal 22) dan progres jawaban RFI/komitmen vendor terhadap target pengadaan (Pasal 18).
  - Catat paket dengan kesiapan rendah atau kompetisi belum objektif sebagai isu yang perlu perhatian + rekomendasi percepatan; jangan menyimpulkan pelanggaran.

## III. Pelaporan

- Kompilasi bukti progres/pembayaran dan status per paket di KKP Pemantauan, pastikan tiap kondisi mengutip sumber dokumen + tanggal data atau "tidak ada file".
- Susun dashboard & rekapitulasi status pelaksanaan (🟢/🟡/🔴) per paket dan kompilasi isu (Kondisi → Kriteria → Potensi Risiko → Rekomendasi); sorot sisa milestone/komitmen yang belum tuntas.
- Konfirmasi status & isu dengan PPK/unit pemilik paket; dokumentasikan tanggapan.
- Susun draft Laporan Hasil Pemantauan + Nota Dinas (ikuti `panduan-format-umum/PANDUAN.md`), termasuk simpulan status keseluruhan dan rekomendasi per isu (disusun KT).
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi Laporan Pemantauan via SIMWAS; indikasi penyimpangan serius dieskalasi ke audit-pengadaan.

## Sumber Wiki Terkait

- Pattern: [[PMP-53]], [[PMP-54]], [[PMP-55]], [[PMP-56]] (dari temuan-patterns/pemantauan-pengadaan/)
- Regulasi: [[regulasi-kunci]] (Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025 — Pasal 78 denda keterlambatan, Pasal 18/22 perencanaan & SIRUP)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-pengadaan/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
