# Fase 4 — Asesmen Per-Hunk Tidying (Merge v8.8→v10)

**Hasil: TIDAK ada yang di-port. Semua file backend yang berbeda = v10-ahead.** Mengambil versi v8.8 akan MEREGRESI kerja engine-ready + hardening + fitur v9. Keputusan: pertahankan v10.

## Tinjauan 10 file backend berbeda (v8.8 vs v10 main pasca Fase 1–3)
| File | Δ | Arah | Alasan v10-ahead |
|---|---|---|---|
| config.py | 4 | v10 | `dev_seed_password` (hardening seed v9) |
| main.py | 10 | v10 | router `administrasi` + patch Windows ProactorEventLoop v10 |
| models.py | 10 | v10 | Role `TU` + status workflow disederhanakan (pivot engine-only) |
| schemas.py | 9 | v10 | `skill` required & folder-driven (bukan enum/opsional) |
| init_db.py | 23 | v10 | seed user TU + `dev_seed_password` dari env |
| storage.py | 58 | v10 | `compute_penugasan_status` versi v10 |
| routes/lembar_reviu.py | 49 | v10 | PM QA/QC 14 butir (jenjang mutu v9) |
| routes/agen.py | 115 | v10 | prompt/tool engine-ready + additions v9 |
| v6/scripts/render_kkp.py | 7 | v10 | **P0: kolom KKP pemantauan +Akibat** (v10 doktrin lebih benar) |
| routes/dokumen.py | 14 | (keputusan) | akses upload |

## Keputusan
**dokumen.py (kontrol akses upload):** v8.8 = AT/KT/PT untuk skill audit; v10 = AT-saja semua skill. **Diputuskan: PERTAHANKAN v10 (AT-saja)** — lebih ketat & sederhana.

## Kesimpulan
Backend v8.8 (pre-pivot, snapshot v8.8) lebih LAMA dari v10 dalam dimensi engine-ready/hardening/fitur v9. Nilai v8.8 seluruhnya ada di **subsistem laporan (Fase 1)**, **survei pendahuluan (Fase 2)**, dan **gate LKE (Fase 3)** — sudah di-merge. Fase 4 tidak menghasilkan perubahan kode. **Sisa: Fase 5 (frontend).**
