---
id: SAIPI-66
skill: kepatuhan-saipi
kategori: SAIPI-1300
severity: HIGH
judul: "Framework APIP Multi-Elemen Belum Terintegrasi (Piagam + KKSAR + Pedoman + SOP + IACM)"
kriteria_baku: "SAIPI 1300 (Program Jaminan & Peningkatan Mutu) + IPPF 2017 (5 elemen PIA Framework) + PP 60/2008"
tags: [saipi, framework-apip, piagam-audit, kksar, pedoman, sop, iacm, governance, kepatuhan-saipi]
---

# SAIPI-66: Framework APIP Multi-Elemen Belum Terintegrasi

## Pattern Kondisi

Framework APIP yang terdiri dari **5 elemen inti** (Piagam Audit, KKSAR, Pedoman Pengawasan, SOP Pengawasan, Rencana Pengawasan IACM) masih **terpisah-pisah dan belum finalisasi** sebagai **satu kesatuan kohesif**. Tiap elemen:

- Piagam Audit: Pending reviu hukum, belum TTD final (ND-146, Mei 2026)
- KKSAR: Belum lengkap sebagai bagian terintegrasi framework
- Pedoman Pengawasan Intern: Dalam revisi draft (ND-147, Mei 2026)
- SOP Pengawasan dengan Agile Audit approach: Masih dalam masukan/review (ND-144, Mei 2026)
- Rencana Pengawasan IACM: 17 kegiatan per 5 elemen belum eksekusi operasional (ND-138, Mei 2026)

**Akibat**: IACM **Element 1 skor 2.00 (TERTINGGI RISIKO)** — operasionalisasi standar APIP tertunda, governance APIP framework belum berjalan sebagai ecosystem.

## Kriteria

**SAIPI Par. 1300** (Program Jaminan & Peningkatan Mutu) + **IPPF 2017** (5 elemen Professional Internal Audit Framework: **Piagam, Strategi, Proses, Penjaminan Mutu, Implementasi**) — Framework APIP wajib terintegrasi sebagai ONE ecosystem, tidak terpisah dokumen-dokumen individual. **PP 60/2008** (Penyelenggaraan SPIP Terintegrasi) mewajibkan pengawasan internal (APIP) sebagai bagian integral sistem pengendalian intern.

## Akibat

1. Operasionalisasi standar APIP tertunda — tiap elemen menunggu finalisasi elemen lain
2. IACM Elemen 1 (Piagam Audit, KKSAR) tidak bisa berjalan penuh tanpa SOP + Pedoman final
3. Governance APIP framework tidak kohesif — auditor/satker tidak punya ONE reference framework
4. Penguatan kapabilitas APIP terhambat (terutama untuk audit berbasis risiko, PKPT baru)

## Bukti Yang Harus Dicari

| Dokumen | Yang dicari |
|---------|-------------|
| Piagam Audit Intern | Status: draft/pending vs final TTD |
| KKSAR (Kerangka Kode Audit) | Kelengkapan struktur & integrasi ke SOP |
| Pedoman Pengawasan Intern | Status: draft/revisi vs final |
| SOP Pengawasan Agile Audit | Status: masukan/review vs final |
| Rencana Pengawasan IACM | Status: planned vs operasional (17 kegiatan) |
| Coordination meeting minutes | Evidence dari FGD/Rakor finalisasi framework |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-SAIPI-66",
  "assigned_to": "{nama anggota}",
  "judul": "Framework APIP Multi-Elemen Belum Terintegrasi — Piagam, KKSAR, Pedoman, SOP, IACM Masih Terpisah",
  "kondisi": "Piagam Audit Intern masih pending reviu hukum (ND-146); KKSAR belum lengkap; Pedoman Pengawasan Intern dalam revisi (ND-147); SOP Pengawasan Agile masih dalam masukan (ND-144); Rencana Pengawasan IACM 17 kegiatan belum eksekusi operasional (ND-138). Kelima elemen ini seharusnya satu ecosystem APIP kohesif, namun masih terpisah dokumen dan tahap finalisasi berbeda.",
  "kriteria": "SAIPI 1300 + IPPF 2017 — Framework APIP wajib terintegrasi (Piagam+Strategi+Proses+QA+Implementasi) sebagai ONE ecosystem governance pengawasan internal, bukan dokumen-dokumen terpisah. PP 60/2008 mewajibkan pengawasan internal sebagai bagian integral SPIP terintegrasi.",
  "akibat": "Operasionalisasi standar APIP tertunda; IACM Elemen 1 (governance) tidak bisa berjalan penuh; governance framework tidak kohesif; penguatan kapabilitas APIP terhambat terutama untuk audit berbasis risiko & PKPT baru.",
  "dokumen_sumber": [
    {"file": "ND-144 (5 Mei 2026) — SOP Pengawasan Agile Audit", "halaman": "1", "kutipan": "SOP Pengawasan Intern dengan pendekatan Agile masih dalam reviu & masukan"},
    {"file": "ND-146 (5 Mei 2026) — Piagam Pengawasan Intern", "halaman": "1", "kutipan": "Piagam masih pending reviu hukum, belum TTD final"},
    {"file": "ND-147 (5 Mei 2026) — Pedoman Pengawasan Intern", "halaman": "1", "kutipan": "Pedoman masih dalam finalisasi dari draft"},
    {"file": "ND-138 (18 Mei 2026) — Rencana Pengawasan IACM", "halaman": "1", "kutipan": "IACM Elemen 1 skor 2.00 (tertinggi risiko) — 17 kegiatan per 5 elemen"}
  ]
}
```

## Contoh Kasus Historis

- **ND-138 Rencana Pengawasan IACM (Mei 2026)** — 17 kegiatan untuk 5 elemen IACM, dengan **Elemen 1 (Piagam Audit, KKSAR) skor 2.00 TERTINGGI RISIKO** — menunjukkan framework governance APIP belum matang. Prerequisite operasional: finalisasi Piagam (ND-146), KKSAR, Pedoman (ND-147), SOP (ND-144) sebagai paket integral.

- **ND-136 Masukan Peta Proses Bisnis (13 Mei 2026)** — 16 masukan substansial terhadap Peta Proses Bisnis, menunjukkan **Piagam Audit, KKSAR, prosedur consulting masih belum jelas** dalam proses bisnis yang ter-map.

- **ND-144/146/147 Finalisasi SOP/Piagam/Pedoman (5 Mei 2026)** — ketiga dokumen **masih dalam tahap reviu/draft**, confirmation dari multiple ND bahwa framework documentation belum ready sebagai integrated set.

- Parallel dengan [[nota-dinas-ir2-mei-2026-batch2]] batch 2 ND, lihat evidence [[surat-tugas-ir2-mei-2026]] (ST-106 "Template Laporan Konsultansi" 60 HK Mei-Agustus 2026 — consulting framework belum finalized).

## Rekomendasi Audit

1. **Finalisasi & Koordinasi Framework Integral**: Piagam Audit + KKSAR + Pedoman + SOP dalam 1 paket (cross-check consistency, tidak dokumen terpisah)
2. **Eksekusi Rencana Pengawasan IACM 17 kegiatan ke operasional** (bukan hanya rencana di atas kertas)
3. **Telaah Sejawat Eksternal APIP Framework** — overdue >3 tahun (terakhir ~2023), wajib refresh per SAIPI 1300

## Catatan

- Lintas-relation dengan [[SAIPI-60]] (Piagam Audit) — tapi SAIPI-60 fokus 1 elemen, SAIPI-66 fokus INTEGRASI 5 elemen.
- Lintas-skill P-23 (Pedoman/SOP Usang) — sama jenis governance readiness.
- Foundation untuk [[pattern-temuan]] P-33 (Sistem Maturitas), karena framework APIP adalah prerequisite.
