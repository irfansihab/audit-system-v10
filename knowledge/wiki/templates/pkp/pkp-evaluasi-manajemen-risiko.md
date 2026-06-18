---
jenis: pkp_template
skill: evaluasi-manajemen-risiko
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
  - "pattern: EMR-39 dari temuan-patterns/evaluasi-manajemen-risiko/"
  - "Pedoman Menkomdigi 6/2017 (kriteria utama) + ISO 31000:2018 (pendukung)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Evaluasi Manajemen Risiko

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/ST dan dokumen MR unit (Piagam Risiko, Formulir 1–5, laporan pemantauan triwulan/tahunan) periode yang dievaluasi.
- Siapkan Lembar Kerja Evaluasi (LKE) MR sesuai Pedoman Menkomdigi 6/2017 (5 proses MR); ISO 31000:2018 sebagai referensi pendukung bila pedoman internal belum mengatur.
- Tetapkan komponen/dimensi maturitas yang dinilai: Penetapan Konteks, Penilaian Risiko, Penanganan Risiko, Pemantauan & Pelaporan, dan Tingkat Kematangan (TKPMR).
- Alokasikan anggota tim per komponen LKE sesuai kompetensi; tetapkan jadwal dan keluaran tiap penanggung jawab (pendekatan uji petik).
- Minta dokumen sumber & data dukung MR dari unit auditi (formulir konteks, profil/peta risiko, rencana penanganan, laporan pemantauan).

## II. Pelaksanaan

Sasaran baku untuk skill `evaluasi-manajemen-risiko` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai Penetapan Konteks (Formulir 1)
  - Uji kelengkapan 7 elemen konteks: sasaran, struktur UPR, stakeholder, peraturan, kategori risiko, kriteria risiko, matriks & selera risiko (Bab III.A.2).
  - Verifikasi keselarasan konteks dengan SOTK dan kemutakhiran pedoman MR yang berlaku (lihat pattern EMR-42).
- Menilai Penanganan Risiko (Formulir 3)
  - Uji bahwa risiko sedang–sangat tinggi memiliki rencana aksi yang bukan sekadar pengendalian rutin (Bab III.A.4).
  - Verifikasi kelengkapan 5 elemen rencana aksi dan keberadaan rencana kontinjensi (lihat pattern EMR-41).
- Menilai Pemantauan & Pelaporan (Formulir 4–5)
  - Uji pelaksanaan pemantauan triwulanan 4 kali (April, Juli, Oktober, Januari) dan ketersediaan laporannya (lihat pattern EMR-39).
  - Verifikasi pembaruan LED dan pelaporan tren risiko kepada pemilik risiko (Bab III.A.5).
- Menilai Komitmen & Tingkat Kematangan (TKPMR)
  - Verifikasi penandatanganan/pengunggahan Piagam Risiko dan kelengkapan pemilik risiko top-down (lihat pattern EMR-40, EMR-43).
  - Tetapkan posisi tingkat kematangan (Risk Naive s.d. Risk Enable) atas 4 parameter: kepemimpinan, proses MR, aktivitas penanganan, dan hasil (Bab IV).

## III. Pelaporan

- Kompilasi pengisian LKE MR & bukti dukung per komponen/proses di KKP.
- Hitung nilai dan tetapkan tingkat kematangan MR (TKPMR, keyakinan terbatas) sesuai Pedoman Menkomdigi 6/2017.
- Konfirmasi kondisi, Area of Improvement (AoI), dan hasil penilaian dengan unit auditi.
- Susun draft Laporan Hasil Evaluasi (LHE) MR beserta saran/rekomendasi perbaikan per proses MR.
- Lakukan reviu berjenjang (AT → KT → PT) dan finalisasi LHE via SIMWAS.

## Sumber Wiki Terkait

- Pattern: [[EMR-39]] — Pemantauan Risiko Triwulanan Belum Diinput (+ [[EMR-40]] piagam belum TTD, [[EMR-41]] rencana penanganan belum diisi, [[EMR-42]] pedoman MR usang, [[EMR-43]] gap komitmen top-down)
- Regulasi/Pedoman: [[regulasi-kunci]] (Pedoman Menkomdigi 6/2017 — kriteria utama; ISO 31000:2018 pendukung)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-manajemen-risiko/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
