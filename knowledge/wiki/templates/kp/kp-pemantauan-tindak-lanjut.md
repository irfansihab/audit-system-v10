---
jenis: kp_template
skill: pemantauan-tindak-lanjut
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
  - "pattern: PTL-49 dari temuan-patterns/pemantauan-tindak-lanjut/"
  - "PP 60/2008 Pasal 50, Permenpan 5/2008, UU 15/2004 Pasal 20"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PP 60/2008 Pasal 50, Permenpan 5/2008, UU 15/2004 Pasal 20.

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Memantau status/perkembangan tindak lanjut rekomendasi pengawasan eksternal (BPK) dan internal (BPKP/APIP) agar ditindaklanjuti tepat waktu dan tepat substansi, tanpa pernyataan keyakinan dan tanpa perhitungan kerugian.

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: Rekomendasi TLHP BPK (tahun berjalan + backlog), TLHP BPKP, TLHP APIP/Itjen, dan peer review APIP — status TL, aging per PIC, serta outstanding finansial untuk periode (cut-off) tertentu.

## Sasaran Pengawasan

Sasaran baku untuk skill `pemantauan-tindak-lanjut` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Mengklasifikasikan status tindak lanjut per rekomendasi berdasarkan bukti (pattern PTL-49).
- Menghitung aging tiap rekomendasi yang belum selesai dan agregasi per PIC (pattern PTL-49).
- Mengidentifikasi rekomendasi kritis dan rekomendasi struktural/ownership yang outstanding (pattern PTL-48, PTL-51).
- Memantau status outstanding finansial rekomendasi (setor ke kas negara/verifikasi) (pattern PTL-50, PTL-52).

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[PTL-48]], [[PTL-49]], [[PTL-50]], [[PTL-51]], [[PTL-52]] (dari temuan-patterns/pemantauan-tindak-lanjut/)
- Regulasi: [[regulasi-kunci]] (PP 60/2008 Pasal 50, Permenpan 5/2008, UU 15/2004 Pasal 20)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/pemantauan-tindak-lanjut/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
