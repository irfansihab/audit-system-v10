# Pattern Temuan — Reviu Keuangan

Index pattern temuan yang berlaku untuk skill `reviu-keuangan`. Tambahkan pattern baru di folder ini, lalu update tabel di bawah.

## Index

| ID | Judul | Kategori | Severity | Kriteria Baku |
|----|-------|----------|----------|---------------|
| RK-67 | PNBP Overstating — Kesalahan Pencatatan di Sistem SAKTI | RK-AKURASI | MEDIUM-HIGH | PMK 107/2024 Pasal 63 (Akurasi Laporan Keuangan) |
| RK-68 | Piutang PNBP — Lag Sinkronisasi Antara Sistem Manajemen Piutang & SAKTI | RK-SISTEM | HIGH | PMK 107/2024 Pasal 61 (Reconciliation) + PP 60/2008 |
| RK-69 | Tagihan OM — Keterbatasan Anggaran & Payment Timing Delay | RK-LIKUIDITAS | MEDIUM | PMK Pelaksanaan Anggaran + kontrak SLA |

## Kategori yang dipakai

- `RK-AKURASI` — kesalahan pencatatan, overstatement/understatement, double-posting
- `RK-SISTEM` — data integrity, lag sinkronisasi antar sistem, reconciliation failure
- `RK-LIKUIDITAS` — cash flow constraint, payment delay, budget realization timing
- `RK-ASET` — pencatatan aset, alih status, akumulasi penyusutan
- `RK-PIUTANG` — piutang macet, aging analysis, penghapusan

## Sumber data pattern

Pattern di folder ini disusun dari LHA reviu keuangan Inspektorat II + audit BPK TA 2023–2026:

- Konfirmasi TLHP Itjen II (SK-156, 05 Juni 2026) — PNBP PSrE overstated Rp62.2M; piutang PNBP selisih Rp316.4M lag sync SAKTI
- Audit OM TKPPSE tahap 4 (SK-155, 06 Juni 2026) — tagihan OM Rp10.6M menunggu ketersediaan anggaran
- BPK LHP LK Kominfo 2024–2025 — catatan akurasi, reconciliation, cash flow

Setiap pattern wajib menyebut kasus historis di section "Contoh Kasus Historis".

## Lihat juga

- [[pattern-temuan]] — katalog induk
- [[audit-pengadaan/README]] — pattern audit pengadaan
- [[pemantauan-tindak-lanjut/README]] — pattern pemantauan TLHP
