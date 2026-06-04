# Kriteria CACM — folder draft

> **STATUS: DRAFT PRE-IMPLEMENTATION (3 Juni 2026)**
> Folder ini dipersiapkan untuk fase 1 implementasi *Mesin Kriteria CACM Multi-Sumber*.
> Lihat rencana lengkap di [`docs/rencana-cacm-kriteria.html`](../../../docs/rencana-cacm-kriteria.html).

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
| 1 — SIRUP port | `PBJ-*.yaml` (9 file dari `ews-rules-verified.md`) | ⏳ pending |
| 2 — Anggaran  | `ANG-*.yaml` (5 file) | ⏳ pending |
| 3 — SPSE       | `SPSE-*.yaml` (6 file) | ⏳ pending |
| 4 — Kinerja    | `KIN-*.yaml` (TBD) | ⏳ butuh klarifikasi sumber |

## Folder gitignore policy

Folder ini **di-track** di git. Auditor PT/PM revisi via Pull Request (audit trail lewat git log).
File `_draft/` (kalau ada untuk eksperimen) sudah di-gitignore lewat top-level rule.

---

*Dokumen ini placeholder; implementasi belum dimulai.*
