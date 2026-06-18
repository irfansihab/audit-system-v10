---
jenis: kp_template
skill: evaluasi-spip
versi: 2.0
output_format: docx
field_required:
  - nomor_st
  - tanggal_st
  - judul_penugasan
  - tujuan_pengawasan
  - ruang_lingkup
  - jadwal_mulai
  - jadwal_selesai
  - tim_pengawasan
field_optional:
  - referensi_regulasi
  - dasar_penugasan_tambahan
  - catatan_pt
sumber_wiki:
  - "pattern: ESP-35 dari temuan-patterns/evaluasi-spip/"
  - "PP 60/2008 tentang SPIP & Peraturan BPKP 5/2021"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Evaluasi SPIP

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PP Nomor 60 Tahun 2008 tentang SPIP dan Peraturan BPKP Nomor 5 Tahun 2021 tentang Penilaian Maturitas Penyelenggaraan SPIP Terintegrasi.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Melaksanakan Penjaminan Kualitas (PK) atas Penilaian Mandiri (PM) maturitas penyelenggaraan SPIP terintegrasi sesuai Peraturan BPKP 5/2021 (evaluasi ber-LKE — keyakinan terbatas).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Unsur dan sub-unsur SPIP pada LKE (Lingkungan Pengendalian, Penilaian Risiko, Kegiatan Pengendalian, Informasi & Komunikasi, Pemantauan) untuk periode penilaian maturitas.

## Sasaran Pengawasan

Sasaran baku untuk skill `evaluasi-spip` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai unsur Lingkungan Pengendalian (sub-unsur 1.1–1.8)
- Menilai unsur Penilaian Risiko (sub-unsur 2.1–2.2)
- Menilai unsur Kegiatan Pengendalian (sub-unsur 3.1–3.11)
- Menilai unsur Informasi & Komunikasi dan Pemantauan (sub-unsur 4.1–4.2, 5.1–5.2)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[ESP-35]] (skor PM lebih tinggi dari QA; lihat juga ESP-36 s.d. ESP-38)
- Regulasi/Pedoman: [[regulasi-kunci]] (PP 60/2008 & Peraturan BPKP 5/2021)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-spip/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
