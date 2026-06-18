---
id: AP-26
skill: audit-pengadaan
kategori: PBJ-PEMBAYARAN
severity: CRITICAL
judul: "Pembayaran Retroaktif Tidak Memenuhi 3 Syarat LKPP"
kriteria_baku: "Surat LKPP 22441/D.4.1/10/2025 + Perpres 46/2025 Pasal 9(1)f²"
tags: [retroaktif, lkpp, analisis-urgensi, reviu-apip, audit-bpkp, om-tkppse, audit-pengadaan]
---

# AP-26: Pembayaran Retroaktif Tidak Memenuhi 3 Syarat LKPP

## Pattern Kondisi

Pembayaran atas pekerjaan tanpa kontrak dilegalisasi secara retroaktif, tetapi tidak memenuhi syarat formal yang ditetapkan LKPP. Indikator umum:

- Tidak ada **memo analisis urgensi** dari PA/KPA
- **Reviu APIP** belum dilakukan / belum terbit Laporan Hasil Verifikasi
- **Audit BPKP** menolak/belum dilaksanakan
- Pembayaran dilakukan/diusulkan sebelum ketiga syarat terpenuhi

## Kriteria

Surat LKPP **22441/D.4.1/10/2025** + Perpres 46/2025 Pasal 9(1)f² mensyaratkan **3 syarat kumulatif** untuk pembayaran retroaktif: (1) **analisis urgensi**, (2) **reviu APIP**, (3) **audit BPKP**. Ketiganya wajib terpenuhi sebelum pembayaran.

## Akibat

1. Pembayaran berisiko menjadi temuan/kerugian negara
2. Nilai tidak dapat diakui sebagai utang/tunggakan (mis. Rp57,34M)
3. Risiko hukum bagi PA/KPA
4. Vendor dapat memutus layanan akibat tunggakan tak terselesaikan

## Bukti Yang Harus Dicari

| Dokumen | Yang dicari |
|---------|-------------|
| Memo analisis urgensi | ada/tidak + tanggal |
| Laporan Hasil Verifikasi APIP | ada/tidak + simpulan |
| Surat penugasan/hasil audit BPKP | diterima/ditolak |
| Bukti pembayaran | tanggal vs pemenuhan 3 syarat |

## Format Temuan (untuk diisi agen ke `append_temuan`)

```json
{
  "sasaran_id": "S-AP-26",
  "assigned_to": "{nama anggota}",
  "judul": "Pembayaran Retroaktif {pekerjaan} Rp{X} Tidak Penuhi 3 Syarat LKPP",
  "kondisi": "Pembayaran retroaktif {pekerjaan} Rp{X} diusulkan, namun: (1) analisis urgensi {ada/tidak}; (2) reviu APIP {status}; (3) audit BPKP {ditolak/belum}. Syarat kumulatif LKPP 22441 belum terpenuhi.",
  "kriteria": "Surat LKPP 22441/D.4.1/10/2025 + Perpres 46/2025 Pasal 9(1)f² — 3 syarat kumulatif (urgensi + reviu APIP + audit BPKP) wajib sebelum pembayaran retroaktif.",
  "akibat": "Pembayaran berisiko kerugian negara; nilai tidak dapat diakui sebagai utang; risiko hukum PA/KPA; vendor berpotensi putus layanan.",
  "dokumen_sumber": [{"file": "...", "halaman": "X", "kutipan": "..."}]
}
```

## Contoh Kasus Historis

- **KHA Revisi-2 OM TKPPSE (Rp16M–Rp57M)** — framework LKPP 22441 mensyaratkan 3 syarat (analisis urgensi, reviu APIP, audit BPKP); **ketiganya gagal** → Rp57,34M tidak dapat diakui sebagai tunggakan. Lihat [[kha-revisi2-om-tkppse-2024-rp16-rp57]], [[surat-bpkp-pelimpahan-audit-tkppse-2026]], [[pattern-temuan]] P-07.

- **ND-148 Pemantauan Tindak Lanjut OM TKPPSE (Mei 2026)** — Perpres 46/2025 framework untuk kontrak retroaktif **belum finalisasi**. Rp57M OM TKPPSE pembayaran diusulkan, namun:
  - Syarat #1 (analisis urgensi): Unclear in recent record
  - Syarat #2 (reviu APIP): Unclear status
  - Syarat #3 (audit BPKP): **DITOLAK** — kategori "OM Tidak Dapat Didukung" (ND-148)
  - **Result**: Perpres 46/2025 Pasal 9(1)f² framework NOT YET FINAL + BPKP rejection = pembayaran menjadi berisiko kerugian negara
  - Outstanding Rp92M (OM TKPPSE + JAR + P3KJT), semua mengandung risiko legal framework yang belum matang
  - Evidence: Lihat [[nota-dinas-ir2-mei-2026-batch2]] (ND-148 Pemantauan TL, ND-150/151 per-program asimetri), [[pemantauan-tlhp-wasdig-november-2025]], [[surat-bpkp-pelimpahan-audit-tkppse-2026]]

## Catatan

- Catatan penting: APIP **harus** issue Laporan Hasil Verifikasi sebelum bayar; eskalasi ke BPKP jika nilai >Rp10M.
- Sinergi: AP-23 (akar: pekerjaan tanpa kontrak).
