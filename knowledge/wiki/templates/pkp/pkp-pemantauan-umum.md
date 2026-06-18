---
jenis: pkp_template
skill: pemantauan-umum
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
  - "pattern: PM-01, PM-02, PM-03 dari temuan-patterns/pemantauan-umum/"
  - "kriteria/target/rencana yang diunggah auditor (rencana aksi, target periode, jadwal milestone, instruksi pimpinan di input/kriteria/)"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Pemantauan Umum (Criteria-Driven)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/Surat Tugas, tujuan, ruang lingkup (objek + periode), dan profil objek untuk menajamkan fokus pemantauan; pemantauan = pelaporan status/progres, bukan penggalian akar masalah dan tanpa pernyataan keyakinan.
- Ekstrak acuan/kriteria pemantauan dari seluruh isi folder `input/kriteria/` (rencana aksi/matriks rencana tindak, target kinerja per periode, jadwal milestone, instruksi/perintah dengan tenggat, atau rekomendasi LHP terdahulu yang dipantau); susun matriks target sebagai acuan status.
- Tetapkan periode pelaporan (cut-off date) dan kriteria status (default: 🟢 ≥95% target/ahead, 🟡 70–95% atau slip ≤10%, 🔴 <70% atau slip >10% atau ada blocker) — dokumentasikan penyesuaian threshold di KP.
- Susun matriks pemantauan per item (target · tenggat · penanggung jawab · sumber data realisasi · indikator status), jadwal pemantauan, dan alokasi tim sesuai `sasaran-assignment.json`.
- Identifikasi dan minta data realisasi/progres terkini dari unit (`input/objek/`: laporan progres, BA, foto, data realisasi) serta data historis untuk trend (`input/data-pendukung/`).

## II. Pelaksanaan

Sasaran baku untuk skill `pemantauan-umum` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Memantau kelengkapan dan ketersediaan dokumen/data pendukung realisasi terhadap kriteria yang diunggah (pattern PM-01).
  - Inventarisasi dokumen/data realisasi wajib menurut matriks target, lalu cek keberadaan tiap dokumen/data per item yang dipantau.
  - Catat status ketersediaan (lengkap/sebagian/tidak ada) dengan mengutip nama file bukti; jika data belum tersedia tandai `[Data tidak tersedia — perlu konfirmasi unit]`, jangan mengarang.
- Memantau capaian realisasi terhadap target/rencana per item dan menetapkan status warna (pattern PM-01).
  - Bandingkan realisasi aktual vs target per item, hitung % capaian dan deviasi jadwal terhadap milestone.
  - Tetapkan status 🟢/🟡/🔴 per kriteria status yang ditetapkan di Perencanaan; tandai item 🔴/🟡 sebagai isu yang perlu perhatian.
  - Catat status via `append_temuan` (status/catatan + usulan percepatan; Sebab deviasi diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data").
- Memantau konsistensi data realisasi antar-sumber/antar-periode (pattern PM-02).
  - Bandingkan nilai/angka/identitas yang sama yang muncul di lebih dari satu sumber (laporan unit, dashboard pihak lain, data historis).
  - Tandai inkonsistensi/selisih material sebagai isu yang perlu klarifikasi unit; jangan menyimpulkan penyimpangan (itu domain audit).
- Memantau kepatuhan terhadap prosedur baku/instruksi/jadwal yang dipantau (pattern PM-03).
  - Uji kesesuaian pelaksanaan item terhadap prosedur/instruksi/jadwal acuan, butir per butir.
  - Catat ketidaksesuaian/slip jadwal sebagai "kondisi yang perlu perhatian" beserta sumber dokumen + tanggal data; eskalasi ke audit-umum bila ditemukan indikasi penyimpangan substantif melebihi deviasi jadwal.

## III. Pelaporan

- Kompilasi bukti realisasi dan status per item di KKPemantauan (`_KKP/03-KKPemantauan.xlsx`), pastikan tiap status mengutip rujukan `[Nama File hal. X par. Y]` atau "tidak ada file".
- Susun rekapitulasi status agregat (🟢/🟡/🔴) per kategori dan trend antar-periode bila pemantauan periodik; sorot item berstatus 🔴/🟡 yang memerlukan intervensi.
- Konfirmasi status & isu deviasi dengan unit pemilik kegiatan; dokumentasikan tanggapan unit.
- Susun draft Laporan Hasil Pemantauan (format surat dinas) + Nota Dinas (ikuti `panduan-format-umum/PANDUAN.md`), termasuk rekomendasi percepatan yang membutuhkan keputusan pimpinan (disusun KT).
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi Laporan Pemantauan via SIMWAS.

## Sumber Wiki Terkait

- Pattern: [[PM-01]], [[PM-02]], [[PM-03]] (starter generic — dari temuan-patterns/pemantauan-umum/)
- Regulasi: [[regulasi-kunci]] (kriteria/target yang diunggah auditor di `input/kriteria/` — criteria-driven; tidak ada regulasi baku tunggal)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-umum/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
