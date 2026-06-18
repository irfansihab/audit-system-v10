---
id: ESK-30
skill: evaluasi-sakip
kategori: SAKIP-HASIL
severity: HIGH
judul: "Stagnasi Predikat AKIP Beberapa Tahun Berturut-turut"
kriteria_baku: "Permenpan-RB 88/2021 tentang Evaluasi Akuntabilitas Kinerja Instansi Pemerintah"
tags: [sakip, akip, predikat, stagnasi, roadmap, permenpanrb-88]
---

# ESK-30: Stagnasi Predikat AKIP Beberapa Tahun Berturut-turut

## Pattern Kondisi

Nilai AKIP tidak naik signifikan dan tertahan pada predikat yang sama selama beberapa tahun. Indikator umum:

- Nilai AKIP naik tipis tahunan tetapi predikat tetap (mis. B selama 3 tahun)
- Belum ada **roadmap** + strategi peningkatan menuju predikat lebih tinggi (BB/A/AA)
- Tidak ada komitmen nyata seluruh unit untuk meningkatkan nilai
- Rekomendasi evaluasi tahun-tahun sebelumnya belum ditindaklanjuti

## Kriteria

Permenpan-RB 88/2021 — evaluasi AKIP menghasilkan nilai + predikat; instansi diharapkan meningkatkan kualitas akuntabilitas kinerja secara berkelanjutan menuju predikat lebih tinggi.

| Rentang Nilai | Predikat |
|---|---|
| 90–100 | AA |
| 80–90 | A |
| 70–80 | BB |
| 60–70 | **B** |
| 50–60 | CC |

## Akibat

1. Akuntabilitas kinerja tidak membaik substantif
2. Indikasi perencanaan/pengukuran lemah yang berulang
3. Reputasi tata kelola Kementerian tertahan

## Bukti Yang Harus Dicari

| Dokumen | Yang dicari |
|---------|-------------|
| LHE AKIP 3 tahun terakhir | tren nilai + predikat |
| Roadmap peningkatan SAKIP | ada/tidak + target |
| Tindak lanjut rekomendasi LHE | status TL rekomendasi sebelumnya |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-ESK-30",
  "assigned_to": "{nama anggota}",
  "judul": "Predikat AKIP {satker} Stagnan '{predikat}' {N} Tahun Berturut-turut",
  "kondisi": "Nilai AKIP {satker}: {thn1} {n1}, {thn2} {n2}, {thn3} {n3} — tetap predikat '{predikat}'. Belum ada roadmap + strategi peningkatan menuju {predikat lebih tinggi}; rekomendasi LHE sebelumnya belum ditindaklanjuti.",
  "kriteria": "Permenpan-RB 88/2021 — instansi diharapkan tingkatkan kualitas akuntabilitas kinerja berkelanjutan menuju predikat lebih tinggi.",
  "akibat": "Akuntabilitas kinerja tidak membaik substantif; indikasi kelemahan perencanaan/pengukuran berulang.",
  "dokumen_sumber": [{"file": "...", "halaman": "X", "kutipan": "68,19 → 68,45 → 69,14 (predikat B) ..."}]
}
```

## Contoh Kasus Historis

- **ND-133 Atensi SAKIP (B/505/AA.05/2025)** — nilai AKIP Kemkomdigi **68,19 (2023) → 68,45 (2024) → 69,14 (2025)**, tetap predikat **B** 3 tahun; belum ada roadmap menuju BB/A/AA. Lihat [[nota-dinas-ir2-mei-2026]] (ND-133), [[lhe-akip-2025-kemkomdigi]], [[pattern-temuan]] P-33.

- **ND-121/134/142 Root Cause: Cascading Eselon II Incomplete (Mei 2026)** — LHE AKIP Kemkomdigi stagnasi B selama 3 tahun di-trace ke **root cause: cascading perencanaan kinerja belum lengkap di level Eselon II** (directorate level):
  - ND-121: Cascading rencana strategis masih belum lengkap → RKA tidak mencerminkan RENSTRA
  - ND-134: RPJP/RPJM/RENSTRA ada, tapi cascading ke unit II belum finalized
  - ND-142: RKA per unit II masih menunjukkan misalignment dengan RENSTRA, penyebab nilai AKIP tidak naik (karena pengukuran kinerja fragmented)
  - **Findings**: Cascading incomplete at Eselon II = perencanaan tidak coherent → pengukuran tidak sesuai real targets → AKIP stuck at 68-69 (B)
  - This is not 3-year-independent incidents, tapi **repeating structural gap**: cascading is yearly activity belum fix
  - Evidence: Lihat [[nota-dinas-ir2-mei-2026-batch2]] (ND-121 Cascading, ND-134 RPJM/cascading, ND-142 RKA alignment), [[lhe-akip-2025-kemkomdigi]], [[surat-tugas-ir2-mei-2026]] (ST-106 cascading improvements template)

## Catatan

- Rekomendasi: susun **roadmap peningkatan SAKIP** dengan milestone + PIC menuju BB.
- Sinergi: ESK-31 (pengukuran terendah jadi penyebab utama stagnasi), ESK-32 (indikator SMART).
