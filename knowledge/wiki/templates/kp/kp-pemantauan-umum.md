---
jenis: kp_template
skill: pemantauan-umum
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
  - "pattern: PM-01 dari temuan-patterns/pemantauan-umum/"
  - "kriteria/target/rencana yang diunggah auditor (criteria-driven; tidak ada regulasi baku tunggal)"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Pemantauan Umum (Criteria-Driven)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

Criteria-driven: kriteria/target/rencana yang diunggah auditor di `input/kriteria/` (rencana aksi, target periode, jadwal milestone, instruksi pimpinan) — tidak ada regulasi baku tunggal.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Melaporkan status pelaksanaan objek yang dipantau terhadap rencana/target/kriteria yang sudah ditetapkan untuk mendeteksi deviasi dini, tanpa penggalian akar masalah dan tanpa pernyataan keyakinan.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Pemantauan status & progres pelaksanaan kebijakan/program/rencana aksi/kepatuhan instruksi pimpinan untuk objek dan periode (cut-off) tertentu.

## Sasaran Pengawasan

Sasaran baku untuk skill `pemantauan-umum` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Memantau kelengkapan dan ketersediaan dokumen/data pendukung realisasi terhadap kriteria yang diunggah (pattern PM-01).
- Memantau capaian realisasi terhadap target/rencana per item dan menetapkan status warna (pattern PM-01).
- Memantau konsistensi data realisasi antar-sumber/antar-periode (pattern PM-02).
- Memantau kepatuhan terhadap prosedur baku/instruksi/jadwal yang dipantau (pattern PM-03).

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[PM-01]], [[PM-02]], [[PM-03]] (starter generic — dari temuan-patterns/pemantauan-umum/)
- Regulasi: [[regulasi-kunci]] (kriteria/target yang diunggah auditor di `input/kriteria/` — criteria-driven)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-umum/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
