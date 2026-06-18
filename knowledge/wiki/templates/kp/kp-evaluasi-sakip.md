---
jenis: kp_template
skill: evaluasi-sakip
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
  - "pattern: ESK-30 dari temuan-patterns/evaluasi-sakip/"
  - "PermenPAN-RB 88/2021 tentang Evaluasi AKIP"
  - "konteks: pola-temuan-berulang"
---

# Kartu Penugasan — Evaluasi SAKIP

## Identitas Penugasan

- **Nomor Surat Tugas**: {{nomor_st}}
- **Tanggal Surat Tugas**: {{tanggal_st}}
- **Judul Penugasan**: {{judul_penugasan}}

## Dasar Hukum & Referensi Regulasi

PermenPAN-RB Nomor 88 Tahun 2021 tentang Evaluasi Akuntabilitas Kinerja Instansi Pemerintah (AKIP).

{{#referensi_regulasi}}
Tambahan referensi yang dirujuk auditor: {{referensi_regulasi}}
{{/referensi_regulasi}}

## Tujuan Pengawasan

{{tujuan_pengawasan}}

Tujuan baku skill ini: Menilai implementasi SAKIP unit kerja terhadap kriteria LKE PermenPAN-RB 88/2021 dan menyimpulkan predikat AKIP (evaluasi ber-LKE — keyakinan terbatas).

## Ruang Lingkup

{{ruang_lingkup}}

Ruang lingkup baku: 4 komponen / 12 sub-komponen / 79 kriteria LKE AKIP pada unit kerja dan periode yang dievaluasi, berdasarkan folder bukti dukung.

## Sasaran Pengawasan

Sasaran baku untuk skill `evaluasi-sakip` (impor → daftar Sasaran KP; otomatis sync ke PKP saat disimpan):

- Menilai komponen Perencanaan Kinerja (bobot 30%)
- Menilai komponen Pengukuran Kinerja (bobot 30%)
- Menilai komponen Pelaporan Kinerja (bobot 15%)
- Menilai komponen Evaluasi Akuntabilitas Kinerja Internal (bobot 25%)

## Jadwal Pelaksanaan

- **Mulai**: {{jadwal_mulai}}
- **Selesai**: {{jadwal_selesai}}

## Tim Pengawasan

{{tim_pengawasan}}

## Catatan Pengendali Teknis

{{catatan_pt}}

## Sumber Wiki Terkait

- Pattern: [[ESK-30]] (stagnasi predikat AKIP; lihat juga ESK-31 s.d. ESK-34)
- Regulasi/Pedoman: [[regulasi-kunci]] (PermenPAN-RB 88/2021 tentang Evaluasi AKIP)
- Konteks: [[pola-temuan-berulang]]
- PANDUAN substansi: `knowledge/skills/evaluasi-sakip/SKILL.md`

---

*Diisi Pengendali Teknis (PT) di tahapan 1; setelah disimpan, KT mendetailkan jadi Program Kerja Pengawasan (PKP).*
