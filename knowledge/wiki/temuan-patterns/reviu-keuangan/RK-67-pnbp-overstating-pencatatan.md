---
id: RK-67
skill: reviu-keuangan
kategori: RK-AKURASI
severity: MEDIUM-HIGH
judul: "PNBP Overstating — Kesalahan Pencatatan di Sistem SAKTI"
kriteria_baku: "PMK 107/2024 Pasal 63 (Akurasi Laporan Keuangan) + PP 60/2008 Pasal 4 (Identifikasi & Evaluasi)"
tags: [pnbp, akurasi, pencatatan, overstating, sakti, double-posting]
---

# RK-67: PNBP Overstating — Kesalahan Pencatatan di Sistem SAKTI

## Pattern Kondisi

Pendapatan PNBP tercatat lebih tinggi dari realisasi sebenarnya di Laporan Keuangan, akibat **kesalahan pencatatan di sistem SAKTI** (double-posting, duplikat entry, atau posting ke periode yang salah). Indikator umum:

- PNBP yang dilaporkan > PNBP yang diterima kas (gap material)
- Entry yang sama muncul di dua periode atau lebih
- Posting ke rekening PNBP yang salah (misal PSrE vs PSrT)
- Tanda terima/kwitansi tidak cocok dengan posting SAKTI
- Rekonsiliasi kas vs SAKTI berbeda signifikan

## Kriteria

PMK 107/2024 Pasal 63 — Laporan Keuangan wajib disajikan dengan akurat, dapat diverifikasi, dan bebas dari salah saji material. PP 60/2008 Pasal 4 mensyaratkan identifikasi & evaluasi atas penyimpangan SPI. Posting di sistem informasi keuangan wajib sesuai dokumen sumber.

## Akibat

1. Laporan Keuangan overstated (aset/pendapatan lebih tinggi dari realisasi)
2. Kuantifikasi error berpotensi material (misalnya Rp62.2M)
3. Temuan BPK atas akurasi & reconciliation
4. Keputusan manajemen/stakeholder berbasis data yang salah
5. Reputasi audit keuangan Inspektorat II terpengaruh

## Bukti Yang Harus Dicari

| Dokumen | Section / Field | Yang dicari |
|---------|-----------------|-------------|
| SAKTI / Jurnal Penerimaan | tanggal posting, nomor rekening | duplikat entry? posting periode salah? |
| Tanda Terima PNBP | tanggal, nominal, rekening tujuan | cocok dengan posting? ada yang double? |
| Laporan Realisasi PNBP | per-jenis PNBP, per-tanggal | ada transaksi tunggal posting 2x? |
| Rekonsiliasi Kas vs SAKTI | monthly summary | gap > threshold (misal >5% atau >Rp100jt)? |
| LK Triwulan | catatan akuntansi | ada adjournment/koreksi posting? |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-RK-67",
  "assigned_to": "{nama anggota}",
  "judul": "PNBP {jenis} Overstated Rp{X} Akibat Kesalahan Pencatatan SAKTI",
  "kondisi": "PNBP {jenis} dicatat di SAKTI Rp{recorded}, namun realisasi kas hanya Rp{actual}. Gap Rp{X} (overstating) disebabkan {penyebab: duplikat entry / posting periode salah / entry ke rekening yang salah}. Terdapat {n} posting anomali pada tanggal {tgl}.",
  "kriteria": "PMK 107/2024 Pasal 63 — Laporan Keuangan wajib akurat & dapat diverifikasi; PP 60/2008 Pasal 4 — SPI wajib identifikasi & evaluasi penyimpangan.",
  "akibat": "LK overstated; temuan BPK potential; keputusan manajemen berbasis data salah; SPI tidak efektif mendeteksi anomali.",
  "dokumen_sumber": [{"file": "SK-156 Konfirmasi TLHP Itjen II", "hal": "X", "kutipan": "PNBP PSrE overstated Rp62.2M ..."}]
}
```

## Contoh Kasus Historis

- **Konfirmasi TLHP Inspektorat Jenderal (SK-156, 05 Juni 2026)** — PNBP PSrE (Penerimaan Sumber Energi) dicatat di laporan Rp{X}, namun setelah reconciliation realisasi kas hanya Rp{Y}, gap **Rp62.2M overstating**. Penyebab: duplikat entry di SAKTI periode Mei–Juni 2026. Lihat [[nota-dinas-ir2-juni-2026]] SK-156, [[pemantauan-tindak-lanjut/PTL-48-rekomendasi-outstanding-bpk]].

## Catatan

- Pasangan reviu awal: [[reviu-keuangan/RK-68-piutang-pnbp-lag-sinkronisasi]] (lag sinkronisasi sistemik)
- Sering terjadi di akhir tahun atau saat transisi sistem (misal SOTK)
- Rekomendasi: (1) Otomasi reconciliation SAKTI-kas harian; (2) User access control per rekening PNBP; (3) Validasi entry ganda di SAKTI; (4) SOP closing month dengan checklist akurasi PNBP
