---
jenis: pkp_template
skill: default
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
  - "konteks: pola-temuan-berulang, regulasi-kunci"
  - "PANDUAN skill spesifik penugasan"
---

# Program Kerja Pengawasan (PKP) — Default (fallback lintas skill)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP), Surat Tugas, dan hasil survei pendahuluan/penjajakan
- Pahami tujuan, sasaran, dan ruang lingkup penugasan
- Tetapkan kriteria/standar pengawasan yang relevan (rujuk regulasi-kunci di wiki)
- Susun program kerja terinci, jadwal, dan alokasi anggota tim
- Identifikasi & kumpulkan dokumen/data yang dibutuhkan (KP, PKP, bahan auditi)

## II. Pelaksanaan

Sasaran baku (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran) — sesuaikan dengan PANDUAN skill:

- Menilai kesesuaian objek pengawasan terhadap kriteria/standar yang berlaku
  - Bandingkan kondisi aktual dengan kriteria yang ditetapkan
  - Dokumentasikan bukti yang memadai pada KKP
- Mengidentifikasi simpulan/temuan substantif beserta dampaknya
  - Susun unsur Kondisi–Kriteria–Sebab–Akibat (sesuai doktrin skill)
  - Verifikasi bukti pendukung sebelum disimpulkan
- Merumuskan rekomendasi/saran perbaikan
  - Pastikan rekomendasi dapat ditindaklanjuti dan terukur

## III. Pelaporan

- Kompilasi & reviu kertas kerja (KKP) berikut bukti pendukung
- Susun simpulan dan daftar temuan/saran
- Bahas hasil dengan unit auditi (exit meeting/konfirmasi)
- Susun draft laporan hasil pengawasan sesuai jenis penugasan
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi via SIMWAS

## Sumber Wiki Terkait

- Konteks: [[pola-temuan-berulang]], [[regulasi-kunci]], [[glossary-komdigi]]
- Pattern temuan: lihat folder `temuan-patterns/<skill>/` sesuai jenis penugasan
- PANDUAN substansi: `knowledge/skills/<skill>/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Template fallback. Untuk skill spesifik, gunakan `pkp-<skill>.md`. Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
