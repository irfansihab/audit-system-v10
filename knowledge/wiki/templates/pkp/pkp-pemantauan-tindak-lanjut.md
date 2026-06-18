---
jenis: pkp_template
skill: pemantauan-tindak-lanjut
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
  - "pattern: PTL-48, PTL-49, PTL-50, PTL-51, PTL-52 dari temuan-patterns/pemantauan-tindak-lanjut/"
  - "PP 60/2008 Pasal 50, Permenpan 5/2008, UU 15/2004 Pasal 20"
  - "konteks: pola-temuan-berulang"
---

# Program Kerja Pengawasan (PKP) — Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)

## Identitas

Nomor PKP: {{nomor_pkp}} — detail operasional dari Kartu Penugasan (KP) {{nomor_st}} ({{tanggal_st}}).

**Judul Program**: {{judul_program}}

## I. Perencanaan

- Pelajari Kartu Penugasan (KP)/Surat Tugas, tujuan, ruang lingkup (rekomendasi + periode), dan PIC/unit yang dipantau; pemantauan TLHP = monitoring status/perkembangan tindak lanjut, tanpa pernyataan keyakinan dan tanpa perhitungan kerugian.
- Muat daftar rekomendasi/komitmen yang dipantau (TLHP BPK per semester + backlog; TLHP BPKP; TLHP APIP/Itjen; peer review) dari database TLHP, rekap Excel `TLHP-[sumber]-[tahun].xlsx`, atau ekstrak rekomendasi dari LHP sumber di `lhp-sumber/`.
- Tetapkan kriteria status TL dan cut-off pemantauan: Selesai (bukti lengkap & memadai, rek ditutup) / Dalam Proses (TL parsial) / Belum Ditindaklanjuti (tidak ada bukti) / Tidak Dapat Ditindaklanjuti (justifikasi kuat + perlu SK penghapusan); kategori aging warna 0–90🟢, 91–180🟡, 181–365🟠, >365🔴.
- Susun matriks pemantauan TLHP (No · Asal LHP · No Rek · Substansi · PIC · Deadline · kriteria status) dan alokasi tim per PIC/sumber sesuai `sasaran-assignment.json`.
- Minta bukti tindak lanjut dari unit pemilik TL (folder `bukti-tl/` per rekomendasi); setiap status wajib mengutip nama file bukti atau "tidak ada file" (anti-halusinasi).

## II. Pelaksanaan

Sasaran baku untuk skill `pemantauan-tindak-lanjut` (impor → baris Sasaran; sub-butir → Langkah Kerja per sasaran):

- Mengklasifikasikan status tindak lanjut per rekomendasi berdasarkan bukti (pattern PTL-49).
  - Baca folder `bukti-tl/` per rekomendasi: ≥1 bukti relevan & substansial → Dalam Proses (minimal); bukti menutup seluruh item rek → Selesai; tidak ada file → Belum Ditindaklanjuti.
  - Catat status via `append_temuan` dengan mengutip nama file bukti; Sebab keterlambatan diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data".
- Menghitung aging tiap rekomendasi yang belum selesai dan agregasi per PIC (pattern PTL-49).
  - Hitung umur (hari) sejak terbit LHP sampai cut-off, klasifikasikan ke kategori warna (🟢/🟡/🟠/🔴).
  - Agregasi per PIC: total rek, Selesai/Proses/Belum, dan aging rata-rata belum-selesai; tandai asimetri rate TL antar-Ditjen sebagai isu kinerja penyelesaian TL.
- Mengidentifikasi rekomendasi kritis dan rekomendasi struktural/ownership yang outstanding (pattern PTL-48, PTL-51).
  - Naikkan rekomendasi umur >365 hari + status ≠ Selesai ke Daftar Kritis; sorot rekomendasi struktural outstanding >2 tahun yang butuh regulasi/MoU (UU 15/2004 Pasal 20 + Pedoman TLHP).
  - Tandai rekomendasi yang ownership-nya fragmen pasca-likuidasi/perubahan SOTK sebagai isu kepemilikan yang perlu penegasan PIC.
- Memantau status outstanding finansial rekomendasi (setor ke kas negara/verifikasi) (pattern PTL-50, PTL-52).
  - Inventarisasi outstanding finansial per rekomendasi (nilai belum disetor / verifikasi belum tuntas) berdasarkan bukti setor/verifikasi.
  - Catat sebagai status TL (bukan kerugian); tandai scope gap verifikasi & nilai belum disetor sebagai isu yang perlu tindak lanjut + rekomendasi percepatan.

## III. Pelaporan

- Kompilasi bukti tindak lanjut & status per rekomendasi di KKP (matrix aging), pastikan tiap status mengutip nama file bukti atau "tidak ada file".
- Susun rekapitulasi status TL & sisa rekomendasi terbuka: statistik umum (% selesai, per sumber), aging per PIC (tabel + ranking worst), dan Daftar Rekomendasi Kritis (>365 hari).
- Konfirmasi status TL dengan unit pemilik TL; dokumentasikan tanggapan dan komitmen percepatan unit.
- Susun draft Laporan Hasil Pemantauan TLHP + Nota Dinas (ikuti `panduan-format-umum/PANDUAN.md`), termasuk Ringkasan Eksekutif untuk Menteri/Sekjen dan rekomendasi percepatan (disusun KT); lampirkan matrix aging Excel.
- Reviu berjenjang (AT → KT → PT → Inspektur) dan finalisasi Laporan Pemantauan TLHP via SIMWAS.

## Sumber Wiki Terkait

- Pattern: [[PTL-48]], [[PTL-49]], [[PTL-50]], [[PTL-51]], [[PTL-52]] (dari temuan-patterns/pemantauan-tindak-lanjut/)
- Regulasi: [[regulasi-kunci]] (PP 60/2008 Pasal 50, Permenpan 5/2008, UU 15/2004 Pasal 20)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-tindak-lanjut/SKILL.md`

## Catatan Ketua Tim

[Diisi KT bila ada catatan khusus untuk tim]

---

*Diisi Ketua Tim (KT) di tahapan 2 — PKP = detail operasional Kartu Penugasan (KP).*
