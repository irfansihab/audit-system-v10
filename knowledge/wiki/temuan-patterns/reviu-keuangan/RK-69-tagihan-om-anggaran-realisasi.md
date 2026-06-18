---
id: RK-69
skill: reviu-keuangan
kategori: RK-LIKUIDITAS
severity: MEDIUM
judul: "Tagihan OM — Keterbatasan Anggaran & Payment Timing Delay"
kriteria_baku: "PMK Pelaksanaan Anggaran + Perpres 16/2018 Pasal 27 (SLA & Payment Terms)"
tags: [om-tkppse, likuiditas, anggaran, payment-delay, cash-flow]
---

# RK-69: Tagihan OM — Keterbatasan Anggaran & Payment Timing Delay

## Pattern Kondisi

**Tagihan operasional & maintenance (OM) dari vendor layanan infrastruktur (TKPPSE, server, telekomunikasi) terpenuhi terlambat akibat keterbatasan ketersediaan anggaran** di unit yang bertanggung jawab. Pekerjaan/layanan sudah berjalan, tetapi pembayaran tertunda sampai anggaran tersedia. Indikator umum:

- Tagihan masuk ke unit audit dengan status "menunggu ketersediaan anggaran"
- Invoice dari vendor belum di-pay >30 hari (aging tagihan panjang)
- SLA service belum terpenuhi karena payment delay (vendor warning/penalti)
- Realisasi anggaran vs DIPA rendah di awal tahun (cash flow mismatch dengan RKAT)
- Vendor mulai escalate atau threat service disruption

## Kriteria

PMK Pelaksanaan Anggaran mensyaratkan SPJ tagihan didukung bukti transfer >7 hari dari invoice date (atau per SLA kontrak). Perpres 16/2018 Pasal 27 — Penyedia berhak pembayaran sesuai jadwal di kontrak; keterlambatan >30 hari adalah breach & dapat trigger penalty clause atau service reduction.

## Akibat

1. Service disruption risk (vendor bisa stop layanan jika payment delay)
2. Penalti kontrak atau escalation dari vendor (denda, balas bersih)
3. SLA tidak terpenuhi → impact ke operasional sistem kritis (TKPPSE, networking)
4. Cash flow forecasting sulit (budget vs realisasi tidak aligned dengan RKAT)
5. Compliance risk: tagihan belum di-SPJ padahal jatuh tempo

## Bukti Yang Harus Dicari

| Dokumen | Section / Field | Yang dicari |
|---------|-----------------|-------------|
| Invoice / Tagihan | invoice date, amount, due date | aging tagihan vs due date |
| Kontrak / SLA | payment term, default clause | kapan batas pembayaran? ada penalty? |
| Rekap DIPA | realisasi per-bulan | ada bulan dengan realisasi <50%? |
| Email/Surat dari Vendor | tanggal, isi | ada warning/escalation soal payment? |
| SAKTI / Jurnal Pembayaran | tgl posting | lag antara invoice date & payment date |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-RK-69",
  "assigned_to": "{nama anggota}",
  "judul": "Tagihan OM {vendor} Rp{X} — Payment Delay {n} Hari Akibat Keterbatasan Anggaran",
  "kondisi": "Tagihan OM {vendor}/{layanan} invoice {tgl} Rp{X}; due date {tgl}, namun pembayaran baru di-process {tgl} (delay {n} hari). Penyebab: realisasi anggaran unit masih {%} per DIPA (belum available untuk SPJ tagihan). {Vendor} telah mengirim {n} reminder email; service belum disrupted namun dalam status 'warning'.",
  "kriteria": "PMK Pelaksanaan Anggaran — SPJ tagihan dalam {n} hari; Perpres 16/2018 Pasal 27 — payment default >30 hari adalah breach kontrak.",
  "akibat": "Risk service disruption; compliance risk (SAKTI posting delayed); vendor relation tension; SLA at risk; cash flow misprojection.",
  "dokumen_sumber": [{"file": "SK-155 LHR Audit OM TKPPSE Tahap 4", "hal": "X", "kutipan": "Tagihan OM Rp10.6M menunggu ketersediaan anggaran ..."}]
}
```

## Contoh Kasus Historis

- **Audit OM TKPPSE Tahap 4 (SK-155, 06 Juni 2026)** — Tagihan OM TKPPSE untuk bulan {bulan} 202X invoice {tgl} Rp10.6M; due date {tgl}. Namun sampai audit fieldwork {tgl}, tagihan belum di-pay (delay {n} hari). Tim audit menemukan email dari vendor TKPPSE tgl {tgl} reminder payment, dengan ancaman "if payment not received by {date}, service will be degraded to maintenance-only mode." Root cause: realisasi anggaran unit masih {%}; anggaran tersebut dialokasikan ke program prioritas lain. Lihat [[nota-dinas-ir2-juni-2026]] SK-155, [[lhr-om-tkppse-2025]].

## Catatan

- Pasangan cash flow: [[reviu-keuangan/RK-67-pnbp-overstating-pencatatan]] (akurasi) dan [[audit-pengadaan/AP-28-kelebihan-bayar-insiden]] (payment accuracy)
- Sering terjadi di unit yang pagu terbatas dan multiple competing priorities
- Rekomendasi: (1) Cash flow planning per-vendor per-bulan (proactive budget management); (2) Early warning system: vendor invoice >7 hari belum di-pay → escalate ke billing; (3) SOP payment priority untuk critical infrastructure (TKPPSE ranked #1); (4) Establish payment reserve untuk recurring OM; (5) Negotiate payment term dengan vendor (extend to 45 hari untuk flexibility)
