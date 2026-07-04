# Scripts Pendukung — evaluasi-sakip (legacy + bukti dukung)

Folder ini memuat 4 script pendukung untuk skill `evaluasi-sakip`. **BUKAN pipeline utama.** Di v7/v8 evaluasi-sakip dijalankan secara agen-driven (orkestrasi via `backend/app/prompts/anggota_tim.md`), bukan pipeline batch. Script `digest_lke`/`cross_check`/`render_lhe` dari sistem lama (audit-system-v4) tidak dibawa ke v7/v8.

## Daftar Script

| Script | Fungsi | Format Input | Dependency |
|--------|--------|--------------|------------|
| `extract_lke.py` | Parse legacy LKE `.xls` ke JSON terstruktur | `.xls` (Excel 97-2003) | **xlrd 1.2.0** |
| `fill_lke_apip.py` | Auto-fill kolom APIP di LKE `.xls` legacy | `.xls` (Excel 97-2003) | **xlrd 1.2.0** |
| `read_local_bukti.py` | Augment LKE JSON dengan teks PDF/xlsx bukti dukung | folder lokal | pdfplumber, openpyxl |
| `download_bukti.py` | Download bukti dukung dari URL evsakip | URL | requests |

## Status Pemakaian (per 6 Mei 2026)

- **`extract_lke.py` & `fill_lke_apip.py`** → **legacy / dipakai jika auditee masih kirim LKE format `.xls`**. Per Mei 2026, alur produksi memakai LKE `.xlsx` Komdigi 2025 yang diproses lewat tool pengisian LKE (`fill_lke`) pada alur agen — bukan pipeline batch.
- **`read_local_bukti.py`** → **aktif** dipakai di alur v5.0 untuk augment JSON LKE dengan teks bukti dukung lokal sebelum analisis Claude.
- **`download_bukti.py`** → **kondisional** — dipakai bila bukti dukung disimpan di portal evsakip (download massal sebelum read_local_bukti).

## Instalasi Dependency

```bash
# Untuk legacy .xls (extract_lke.py, fill_lke_apip.py):
pip install xlrd==1.2.0 --break-system-packages

# Catatan: xlrd >= 2.0 tidak lagi support .xlsx — gunakan 1.2.0 untuk .xls legacy.
# Untuk LKE .xlsx modern: openpyxl sudah cukup (sudah dipasang).
```

## Panduan Migrasi LKE `.xls` → `.xlsx`

Alur agen (engine) memproses LKE dalam format `.xlsx`. Kalau auditee masih kirim LKE dalam format Excel 97-2003 (`.xls`):

1. **Opsi cepat (disarankan):** Buka di Excel → Save As → `Excel Workbook (*.xlsx)` → LKE `.xlsx` siap dipakai pada alur agen (pengisian & validasi LKE via tool `fill_lke`).
2. **Opsi skrip:** Pakai `extract_lke.py` untuk parse `.xls` legacy → JSON terstruktur sebagai bahan augmentasi (lihat `read_local_bukti.py`).

Catatan: skill ini **agen-driven** (tanpa pipeline batch/auto-execute) — orkestrasi urutan langkah diatur orkestrator, bukan skrip di folder ini.
