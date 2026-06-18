---
id: RK-68
skill: reviu-keuangan
kategori: RK-SISTEM
severity: HIGH
judul: "Piutang PNBP — Lag Sinkronisasi Antara Sistem Manajemen Piutang & SAKTI"
kriteria_baku: "PMK 107/2024 Pasal 61 (Reconciliation & Data Integrity) + PP 60/2008 Pasal 4 (SPI)"
tags: [piutang, pnbp, sinkronisasi, lag, sakti, system-integration]
---

# RK-68: Piutang PNBP — Lag Sinkronisasi Antara Sistem Manajemen Piutang & SAKTI

## Pattern Kondisi

**Piutang PNBP tercatat di sistem manajemen piutang berbeda signifikan dengan data di SAKTI** (Sistem Akuntansi Keuangan), mengakibatkan **lag sinkronisasi yang material** (biasanya lag 1 bulan atau lebih). Indikator umum:

- Piutang PNBP di laporan SAKTI ≠ piutang di sistem manajemen piutang (misal: SPAN, SimPiutang)
- Gap sinkronisasi konsisten: selisih Rp200jt–Rp500jt atau lebih per bulan
- Post-closing adjustment besar (>5% aset) untuk reconcile piutang
- Interface sistem tidak real-time; data diupdate manual/batch mingguan/bulanan
- Aging piutang tidak akurat di LK (karena terdapat piutang "ghost" yang sudah lunas tapi belum di-update SAKTI)

## Kriteria

PMK 107/2024 Pasal 61 — Laporan Keuangan wajib didasari data yang lengkap, akurat, dapat direkonsiliasi, dan bebas dari selisih material. PP 60/2008 Pasal 4(2) mensyaratkan SPI mampu mengidentifikasi & mengatasi penyimpangan data. Piutang merupakan komponen material aset; lag sinkronisasi >1% aset materiality adalah deficiency.

## Akibat

1. Laporan Keuangan berpotensi misstated (understatement atau overstatement aset/piutang)
2. Manajemen risiko piutang tidak akurat (aging, outstanding, doubtful accounts tidak correct)
3. Cash flow forecasting meleset (realisasi kas vs proyeksi berbeda)
4. Temuan BPK atas completeness & accuracy of piutang
5. SPI dinilai tidak efektif (terutama di elemen Information & Communication)

## Bukti Yang Harus Dicari

| Dokumen | Section / Field | Yang dicari |
|---------|-----------------|-------------|
| Laporan SAKTI (Neraca) | Piutang PNBP | nominal, aging |
| Laporan Sistem Manajemen Piutang | piutang outstanding | nominal, aging, tgl terakhir update |
| Rekonsiliasi Piutang | SAKTI vs Sistem Piutang | gap per-bulan, trend, penyebab |
| Payment receipt / Kwitansi | tgl, nominal, status di SAKTI | ada yang lunas tapi belum update SAKTI? |
| Interface Log / Batch Upload | tgl upload, record count, error | frekuensi sinkronisasi, ada failed record? |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-RK-68",
  "assigned_to": "{nama anggota}",
  "judul": "Piutang PNBP — Lag Sinkronisasi Rp{X} Antara Sistem Manajemen Piutang & SAKTI",
  "kondisi": "Piutang PNBP di SAKTI (per {bulan} 202X): Rp{SAKTI}, sedangkan di sistem manajemen piutang: Rp{system}. Selisih Rp{X} (lag {n} hari). Penyebab: {interface manual / batch update tidak real-time / reconciliation tertunda}. Terdapat {n} invoice yang sudah lunas di sistem piutang tapi belum di-mark lunas di SAKTI.",
  "kriteria": "PMK 107/2024 Pasal 61 — data wajib lengkap, akurat, reconcilable; PP 60/2008 Pasal 4 — SPI wajib deteksi & atasi penyimpangan.",
  "akibat": "LK potentially misstated; cash flow forecast meleset; aging piutang tidak akurat; TLHP tracking sulit; SPI deficiency di Information & Communication.",
  "dokumen_sumber": [{"file": "SK-156 Konfirmasi TLHP Itjen II", "hal": "X", "kutipan": "Piutang PNBP selisih Rp316.4M lag sync 1 bulan SAKTI ..."}]
}
```

## Contoh Kasus Historis

- **Konfirmasi TLHP Inspektorat Jenderal (SK-156, 05 Juni 2026)** — Piutang PNBP per neraca SAKTI Mei 2026 tercatat Rp{X}. Setelah reconciliation dengan sistem manajemen piutang, piutang outstanding yg benar Rp{Y}. **Gap Rp316.4M** dengan lag 1 bulan. Penyebab: interface SAKTI-SimPiutang tidak real-time, upload batch harian Jam 08:00 saja. Terdapat {n} piutang sudah dibayar akhir Mei tapi belum di-update SAKTI sampai awal Juni. Lihat [[nota-dinas-ir2-juni-2026]] SK-156, [[pemantauan-tindak-lanjut/PTL-49-integrity-sistem]].

## Catatan

- Pasangan akurasi: [[reviu-keuangan/RK-67-pnbp-overstating-pencatatan]] (kesalahan pencatatan unit)
- Lag sinkronisasi adalah SPI deficiency di elemen IT Governance & System Design (PP 60/2008)
- Rekomendasi: (1) Interface real-time atau minimal intraday SAKTI-SimPiutang; (2) Daily reconciliation report; (3) SOP reconciliation piutang dengan deadline T+1; (4) Approval workflow untuk piutang >Rp500jt sebelum SAKTI posting
