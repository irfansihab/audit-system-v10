---
id: ESK-33
skill: evaluasi-sakip
kategori: SAKIP-CASCADING
severity: MEDIUM
judul: "Penjenjangan (Cascading) Kinerja Belum Lengkap s.d. Eselon II / Pegawai"
kriteria_baku: "Permenpan-RB 88/2021 (penjenjangan kinerja)"
tags: [sakip, cascading, penjenjangan, esr-menpan, eselon-ii, permenpanrb-88]
---

# ESK-33: Penjenjangan (Cascading) Kinerja Belum Lengkap

## Pattern Kondisi

Penjenjangan kinerja dari level kementerian hingga Eselon II/pegawai belum lengkap atau belum terukur kualitasnya. Indikator umum:

- Penjenjangan di aplikasi (mis. `esr.menpan.go.id`) belum lengkap sampai Eselon II
- Kualitas cascading (keselarasan pohon kinerja) belum dinilai
- Monev kinerja belum berjenjang sampai level pegawai
- Aplikasi manajemen kinerja belum digunakan efektif

## Kriteria

Permenpan-RB 88/2021 — kinerja harus dijabarkan berjenjang (cascading) dari Kementerian → Eselon I → Eselon II → pegawai dengan keselarasan pohon kinerja.

## Akibat

1. Kinerja unit bawah tidak selaras dengan sasaran strategis atas
2. Nilai komponen Perencanaan/Pengukuran tertahan
3. Akuntabilitas individu lemah

## Bukti Yang Harus Dicari

| Dokumen | Yang dicari |
|---------|-------------|
| Aplikasi e-SR/esr.menpan | kelengkapan penjenjangan s.d Eselon II |
| Pohon kinerja | keselarasan vertikal sasaran-indikator |
| SKP pegawai | turunan dari PK unit |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-ESK-33",
  "assigned_to": "{nama anggota}",
  "judul": "Penjenjangan Kinerja {satker} Belum Lengkap s.d. Eselon II",
  "kondisi": "Penjenjangan kinerja {satker} di {aplikasi} belum lengkap hingga Eselon II; kualitas cascading belum terukur; monev belum berjenjang sampai pegawai; aplikasi manajemen kinerja belum digunakan efektif.",
  "kriteria": "Permenpan-RB 88/2021 — kinerja dijabarkan berjenjang dari Kementerian s.d. pegawai dengan keselarasan pohon kinerja.",
  "akibat": "Kinerja unit bawah tidak selaras sasaran strategis; nilai Perencanaan/Pengukuran tertahan; akuntabilitas individu lemah.",
  "dokumen_sumber": [{"file": "...", "halaman": "X", "kutipan": "..."}]
}
```

## Contoh Kasus Historis

- **LHE AKIP eksternal Kemenpan-RB 2023–2024** — penjenjangan kinerja hingga Eselon II belum lengkap di esr.menpan.go.id; kualitas cascading belum terukur; aplikasi manajemen kinerja belum efektif; monev belum berjenjang sampai pegawai. Lihat [[lhe-akip-eksternal-kemenpanrb-2023-2024]], [[lhe-akip-internal-itjen-2023-2025]].

- **ND-121/134/142 Cascading Eselon II Implementation Gap (Mei 2026)** — Kemkomdigi cascading shows systematic issue:
  - **ND-121** (Cascading rencana strategis belum lengkap): RKT/RENSTRA tidak tercascade penuh ke unit Eselon II — ditemukan mismatch antara RENSTRA top-level vs actual RPKA per direktorat
  - **ND-134** (RPJM & cascading progress): Meski RPJM sudah disiapkan, cascading implementasi per unit II masih incompleted; timeline penyelesaian overdue vs planning
  - **ND-142** (RKA per unit alignment): RKA per unit II menunjukkan indikator yang NOT aligned dengan RENSTRA parent — cascading quality belum terukur, hanya kelengkapan dokumen tanpa substance check
  - **Pattern**: Cascading process is annual (harus ulang tiap tahun), tapi gaps belum teratasi → masalah berulang, menjadi root cause ESK-30 (AKIP stagnation)
  - Evidence: Lihat [[nota-dinas-ir2-mei-2026-batch2]] (ND-121, ND-134, ND-142), [[lhe-akip-2025-kemkomdigi]], [[surat-tugas-ir2-mei-2026]] (ST-106 cascading template improvements)

## Catatan

- Rekomendasi: lengkapi penjenjangan s.d. Eselon II di aplikasi; nilai keselarasan pohon kinerja.
- Sinergi: ESK-32 (indikator SMART di tiap jenjang).
