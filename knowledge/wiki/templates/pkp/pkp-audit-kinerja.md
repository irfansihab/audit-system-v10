---
jenis: pkp_template
skill: audit-kinerja
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
  - "pattern: AK-17, AK-18, AK-19, AK-20, AK-21, AK-22 dari temuan-patterns/audit-kinerja/"
  - "PP 60/2008, Perpres 29/2014, Standar Audit Intern Pemerintah Indonesia (AAIPI)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Audit Kinerja (Efektivitas & Efisiensi)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/Surat Tugas, Memo Survei Pendahuluan, dan profil risiko per 8 aspek; sasaran & ruang lingkup diambil dari hasil penajaman Memo SP (bukan verbatim ST).
- Pahami tujuan, sasaran, dan ruang lingkup 2E (efektivitas & efisiensi); ekonomisitas/kewajaran harga di luar lingkup — indikasi pengadaan dieskalasi ke audit-pengadaan.
- Tetapkan kriteria dari dokumen internal program (proses bisnis/SOP, Perjanjian Kinerja & IKU, TOR/KAK, DIPA/RKA, regulasi teknis program); sub-skill program dibaca bila tersedia.
- Petakan logika intervensi program (Input → Proses → Output → Outcome) dan kaitkan tiap sasaran/langkah kerja ke aspek dari 8 aspek (hulu desain, enabler, hilir kinerja) — hanya aspek yang tercermin di KP/PKP yang diaudit.
- Susun program kerja, jadwal pengujian, alokasi tim, dan rencana analytical review (target vs realisasi IKU, % serapan vs % capaian fisik), termasuk benchmark/best practice dari Memo SP.
- Identifikasi dan minta dokumen/data kinerja yang masih dibutuhkan sebelum pengujian (bagian 9 Memo SP).

## II. Pelaksanaan

Sasaran baku untuk skill `audit-kinerja` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menguji efektivitas pencapaian target output dan outcome program (aspek 6–7; pattern AK-21).
  - Bandingkan realisasi IKU/output terhadap target Perjanjian Kinerja dan standar output di TOR.
  - Uji petik kualitas output (BAST, cek lapangan/dokumen) dan telusur apakah output berubah menjadi outcome yang sampai ke penerima manfaat.
  - Telusuri sebab gap efektivitas dengan why-tree (menembus enabler ke desain) dan hitung dampak konkret (jumlah penerima manfaat, biaya per unit output).
- Menguji efektivitas sistem/teknologi pengendalian dan proses bisnis program (aspek 4; pattern AK-17, AK-18).
  - Lakukan process walkthrough dan uji pengendalian apakah proses bisnis/SOP memadai dan benar-benar dijalankan.
  - Uji apakah sistem/teknologi pengendalian dapat di-bypass dan apakah hasil deteksi/proses ditindaklanjuti sampai tuntas (closure).
  - Analisis sebab kelemahan proses/pengendalian terhadap pencapaian tujuan program (uji 3E sesuai PP 8/2006 + SAIPI 2200/2300).
- Menguji efisiensi penggunaan sumber daya (anggaran, aset, SDM) program (aspek 3 & 5; pattern AK-19).
  - Bandingkan serapan anggaran terhadap progres fisik dan hitung biaya per unit output (DIPA/RKA + standar biaya).
  - Uji utilisasi aset, beban kerja/kompetensi SDM, dan identifikasi tumpang tindih fungsi antarunit/antarsistem (inefisiensi).
  - Telusuri sebab pemborosan/overhead dan dampaknya terhadap pencapaian target dengan sumber daya yang ada.
- Menguji validitas data kinerja dan desain indikator program (aspek 1 & 8; pattern AK-21, AK-22).
  - Rekalkulasi IKU dan telusur ke data mentah; uji konsistensi antarlaporan (PK vs LKj vs e-monev) untuk mendeteksi capaian yang tidak terverifikasi.
  - Nilai apakah desain indikator/formula tarif sudah mencerminkan nilai ekonomi/outcome (logika intervensi, definisi operasional IKU).
  - Analisis sebab kelemahan desain/validitas data (target terlalu rendah, manipulasi, definisi operasional lemah) dan dampaknya pada keandalan simpulan kinerja.

## III. Pelaporan

- Kompilasi dan reviu KKP beserta bukti pendukung; pastikan tiap kondisi mengutip nama dokumen + pasal/bagian kriteria dan setiap angka mencantumkan sumber.
- Susun temuan dalam format Kondisi–Kriteria–Sebab–Akibat (wajib Sebab via why-tree), tandai aspek (1–8) dan dimensi 2E, serta beri kodefikasi temuan SIM-HP pada KKP.
- Lakukan exit meeting/konfirmasi auditi atas temuan kinerja; dokumentasikan tanggapan auditi.
- Susun draft Laporan Hasil Audit (LHA) Kinerja (temuan per dimensi 2E, simpulan keyakinan memadai) beserta rekomendasi yang disusun KT (matriks Temuan | Rekomendasi | Penanggung Jawab | Target Waktu).
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi LHA via SIMWAS; indikasi fraud dieskalasi ke pimpinan.

## Sumber Wiki Terkait

- Pattern: [[AK-17-sistem-pengendalian-bypass]], [[AK-18-hasil-deteksi-tidak-ditindaklanjuti]], [[AK-19-tumpang-tindih-fungsi]], [[AK-21-capaian-tidak-traceable]], [[AK-22-formula-tarif-belum-cerminkan-nilai]] (dari temuan-patterns/audit-kinerja/)
- Regulasi: [[regulasi-kunci]] (PP 60/2008, Perpres 29/2014, Standar Audit Intern Pemerintah Indonesia (AAIPI); kriteria teknis dari proses bisnis/SOP/PK program)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/audit-kinerja/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP). Setiap audit didahului Survei Pendahuluan.*
