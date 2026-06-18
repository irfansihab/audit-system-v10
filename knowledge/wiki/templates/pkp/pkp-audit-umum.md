---
jenis: pkp_template
skill: audit-umum
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
  - "pattern: AU-01, AU-02, AU-03 dari temuan-patterns/audit-umum/"
  - "kriteria yang diunggah auditor (regulasi/SOP/SK/juklak di input/kriteria/)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Audit Umum (Criteria-Driven)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/Surat Tugas, hasil Survei Pendahuluan, dan profil risiko objek untuk menajamkan fokus audit.
- Pahami tujuan, sasaran, dan ruang lingkup audit (yang diaudit dan yang TIDAK diaudit) sesuai sasaran-assignment.json.
- Ekstrak dan tetapkan kriteria/standar dari seluruh isi folder `input/kriteria/` (regulasi nasional/internal, mengikat/non-mengikat, level UU/PP/Perpres/Permen/Perdirjen/SOP); susun matriks kriteria internal sebagai acuan pengujian.
- Petakan proses/objek yang diaudit terhadap matriks kriteria, dan uraikan tiap sasaran generik menjadi checklist per-kriteria (uji per-elemen, bukan global).
- Susun program kerja, jadwal pengujian, alokasi tim, dan pendekatan sampling/materialitas (catatan administratif/reguler/material/prioritas tinggi).
- Identifikasi dan minta dokumen/data objek (`input/objek/`) serta data pendukung yang dibutuhkan untuk pengujian.

## II. Pelaksanaan

Sasaran baku untuk skill `audit-umum` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Menilai kelengkapan dokumen pendukung objek audit terhadap kriteria yang diunggah (pattern AU-01).
  - Inventarisasi dokumen wajib menurut matriks kriteria, lalu cek keberadaan tiap dokumen pada objek audit.
  - Uji kelengkapan unsur/lampiran tiap dokumen; catat dokumen/unsur yang tidak ada sebagai temuan (Kondisi–Kriteria–Sebab–Akibat).
  - Telusuri sebab ketidaklengkapan (kelemahan SOP, pengendalian internal, atau kapasitas pelaksana).
- Menguji konsistensi data antardokumen pendukung (pattern AU-02).
  - Bandingkan nilai/angka/identitas yang sama yang muncul di lebih dari satu dokumen (mis. nilai, tanggal, volume, pihak).
  - Tandai selisih/inkonsistensi yang material; tetapkan dokumen mana yang valid berdasarkan kriteria.
  - Analisis akar penyebab inkonsistensi dan dampaknya terhadap keandalan objek audit.
- Menguji kepatuhan terhadap prosedur baku/regulasi yang diunggah (pattern AU-03).
  - Uji kesesuaian pelaksanaan objek per pasal/butir kriteria (matriks kriteria), satu temuan per elemen yang tidak sesuai.
  - Kumpulkan bukti memadai untuk tiap kondisi: sumber dokumen + halaman/pasal + tanggal + nilai (jika ada).
  - Nyatakan eksplisit elemen yang "telah memenuhi" dan elemen yang tidak sesuai beserta unsur K/K/S/A.
- Mengukur nilai dan tingkat materialitas atas ketidaksesuaian yang ditemukan.
  - Hitung nilai rupiah dampak tiap ketidaksesuaian bila terukur.
  - Klasifikasikan temuan ke level risiko (catatan administratif/reguler/material/prioritas tinggi) dan tandai temuan >Rp 500 jt untuk reviu KT.

## III. Pelaporan

- Kompilasi dan reviu KKA/KKP beserta bukti pendukung; pastikan tiap kondisi terdokumentasi dengan rujukan `[Nama File hal. X par. Y]`.
- Susun temuan dalam format Kondisi–Kriteria–Sebab–Akibat dan beri kodefikasi temuan SIM-HP pada KKP.
- Lakukan exit meeting/konfirmasi auditi atas temuan; dokumentasikan tanggapan auditi.
- Susun draft Laporan Hasil Audit (LHA) format surat dinas + Nota Dinas (ikuti `panduan-format-umum/PANDUAN.md`), termasuk rekomendasi material yang disusun KT.
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi LHA via SIMWAS; temuan >Rp 1 M atau indikasi pidana dieskalasi ke Inspektur.

## Sumber Wiki Terkait

- Pattern: [[au-01-01-kelengkapan-dokumen]], [[au-02-02-konsistensi-data]], [[au-03-03-kepatuhan-prosedur]] (dari temuan-patterns/audit-umum/)
- Regulasi: [[regulasi-kunci]] (kriteria yang diunggah auditor di `input/kriteria/` — criteria-driven; tidak ada regulasi baku tunggal)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/audit-umum/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP). Setiap audit didahului Survei Pendahuluan.*
