---
jenis: pkp_template
skill: evaluasi-spip
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
  - "pattern: ESP-35 dari temuan-patterns/evaluasi-spip/"
  - "PP 60/2008 + Peraturan BPKP 5/2021 (Maturitas SPIP Terintegrasi)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Evaluasi SPIP (Penjaminan Kualitas Maturitas)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/ST dan dokumen penyelenggaraan SPIP unit (hasil Penilaian Mandiri/PM, kertas kerja, kebijakan pengendalian) periode yang dievaluasi.
- Siapkan Lembar Kerja Evaluasi (LKE) SPIP sesuai PP 60/2008 dan Peraturan BPKP 5/2021 (25 sub-unsur dalam 5 unsur, mencakup MRI dan IEPK).
- Tetapkan komponen dan bobot penilaian maturitas: Penetapan Tujuan, Struktur & Proses, serta Pencapaian Tujuan — termasuk mekanisme penalti.
- Alokasikan anggota tim per unsur/komponen LKE sesuai kompetensi; tetapkan jadwal dan keluaran tiap penanggung jawab.
- Minta dokumen sumber & bukti dukung per unsur/sub-unsur dari unit auditi (SOP, SK, laporan, notulen, register risiko).

## II. Pelaksanaan

Sasaran baku untuk skill `evaluasi-spip` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai unsur Lingkungan Pengendalian (sub-unsur 1.1–1.8)
  - Uji bukti integritas, kode etik, struktur organisasi, dan kebijakan SDM penyelenggara SPIP.
  - Tetapkan Nilai PK (skor maturitas 1–5) per sub-unsur dan catat kompetensi SDM yang belum merata (lihat pattern ESP-38).
- Menilai unsur Penilaian Risiko (sub-unsur 2.1–2.2)
  - Telaah keberadaan register risiko strategis & Rencana Tindak Pengendalian (RTP) serta komunikasinya (lihat pattern ESP-36).
  - Tetapkan Nilai PK per sub-unsur berdasarkan bukti identifikasi dan analisis risiko.
- Menilai unsur Kegiatan Pengendalian (sub-unsur 3.1–3.11)
  - Uji keberadaan & efektivitas kegiatan pengendalian atas risiko utama, termasuk pengendalian berbasis sistem informasi.
  - Verifikasi kertas kerja/aplikasi SPIP yang mendukung pengendalian (lihat pattern ESP-37).
- Menilai unsur Informasi & Komunikasi dan Pemantauan (sub-unsur 4.1–4.2, 5.1–5.2)
  - Telaah ketersediaan informasi pengendalian dan komunikasi internal/eksternal yang relevan.
  - Bandingkan skor Penilaian Mandiri (PM) dengan hasil Penjaminan Kualitas (PK) untuk mendeteksi optimism bias (lihat pattern ESP-35).

## III. Pelaporan

- Kompilasi pengisian LKE SPIP (kolom Nilai PK + Catatan PK) & bukti dukung per unsur/sub-unsur di KKP.
- Hitung nilai dan tetapkan tingkat maturitas SPIP final (Level 1–5, keyakinan terbatas) sesuai Peraturan BPKP 5/2021.
- Konfirmasi kondisi, Area of Improvement (AoI), dan hasil penilaian dengan unit auditi.
- Susun draft Laporan Hasil Evaluasi (LHE) SPIP beserta AoI prioritas dan saran perbaikan.
- Lakukan reviu berjenjang (AT → KT → PT) dan finalisasi LHE via SIMWAS.

## Sumber Wiki Terkait

- Pattern: [[ESP-35]] — Skor PM > QA / Optimism Bias (+ [[ESP-36]] register risiko strategis belum ada, [[ESP-37]] aplikasi SPIP bermasalah, [[ESP-38]] kompetensi SDM belum merata)
- Regulasi/Pedoman: [[regulasi-kunci]] (PP 60/2008 + Peraturan BPKP 5/2021 — Maturitas SPIP Terintegrasi)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-spip/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
