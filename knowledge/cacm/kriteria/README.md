# Kriteria CACM

> **STATUS: AKTIF.** Dipakai evaluator (`backend/app/cacm_evaluator.py`) untuk
> menilai MERAH/KUNING/HIJAU atas observasi CACM. Dimensi PENGADAAN memakai data
> riil dari agent EWS; dimensi ANGGARAN & KINERJA masih data dummy — lihat
> peringatan di bawah.

Setiap file `<ID>.yaml` di sini = 1 kriteria yang dipakai v7 untuk evaluasi MERAH/KUNING/HIJAU
atas data CACM (SIRUP, DIPA, SPSE, Kinerja). Skema YAML lihat sample
[`PBJ-PDN-RASIO.yaml`](./PBJ-PDN-RASIO.yaml).

## Konvensi ID

- **Prefix dimensi:** `PBJ-` (SIRUP perencanaan pengadaan), `ANG-` (DIPA/anggaran), `SPSE-` (SPSE realisasi), `KIN-` (kinerja).
- **Topik:** mengikuti pola `PREFIX-TOPIK-VARIAN`, mis. `PBJ-PL-BATAS-NILAI`, `ANG-REALISASI-Q3`.
- **ID unik** lintas dimensi.

## Field wajib di setiap YAML

Lihat sample. Validator akan menolak YAML yang:
- Tidak punya: `id`, `revisi`, `nama`, `dimensi`, `sumber_data`, `regulasi`, `metric`, `thresholds`.
- `thresholds` tidak punya ≥1 entry MERAH atau ≥1 entry HIJAU (paling sedikit dua status untuk bisa membedakan).
- `metric.expression` tidak bisa di-parse oleh DSL.

## Status implementasi (per fase rencana)

| Fase | Folder/files yang akan dibuat | Status |
|------|-------------------------------|--------|
| 1 — SIRUP port | `PBJ-*.yaml` (9 file dari `ews-rules-verified.md`) | ✅ 9 file, data agent EWS riil |
| 2 — Anggaran  | `ANG-*.yaml` (5 file) | 🟡 2 dari 5 — **ambang & data masih DUMMY** |
| 3 — SPSE       | `SPSE-*.yaml` (6 file) | ⏳ pending |
| 4 — Kinerja    | `KIN-*.yaml` (TBD) | 🟡 2 file — **DUMMY + sumber data belum diklarifikasi** |

### ⚠️ Yang WAJIB dibereskan sebelum ANG-*/KIN-* dipakai atas data riil

Kriteria `ANG-*` & `KIN-*` dibuat bersamaan dengan fixture dummy
(`backend/app/fixtures/cacm-sample-anggaran-kinerja.json`) untuk membuka jalur
CACM multi-sumber. Yang belum beres — jangan diperlakukan sebagai kriteria matang:

1. **Ambang belum divalidasi auditor.** Semua angka threshold (50/75, 35/50,
   70/90, 15/30) adalah placeholder, bukan hasil konfirmasi target resmi.
2. **Regulasi belum dikonfirmasi.** Entry bertanda `[VERIFIKASI AUDITOR]` harus
   diganti nomor pasal yang benar-benar dicek.
3. **Sumber data KINERJA masih asumsi** (`kinerja_eperformance`). Perlu keputusan:
   e-Performance, SAKIP/LKj, SMART DJA, atau input manual INTEGRAL?
4. **Belum periode-aware.** `ANG-SERAPAN-RENDAH` menilai sama saja di Q1 maupun
   Q4; `ANG-NUMPUK-Q4` hanya sah setelah Q4 berjalan. Lihat `periode_relevansi`.
5. **Belum ada skill pelaksanaan anggaran** — `promote.skill` ANG-* sementara
   diarahkan ke `reviu-umum`.

Ingest data dummy: `POST /cacm/observasi/ingest-sample` (PT), atau tombol
"＋ Contoh Anggaran & Kinerja" di halaman CACM.

## Folder gitignore policy

Folder ini **di-track** di git. Auditor PT/PM revisi via Pull Request (audit trail lewat git log).
File `_draft/` (kalau ada untuk eksperimen) sudah di-gitignore lewat top-level rule.

---

*Revisi kriteria oleh PT/PM lewat Pull Request — audit trail via git log.*
