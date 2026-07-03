# Fase 0 — Pra-flight Merge v8.8→v10 (read-only)

**Verdict: 🟢 LANJUT Fase 1 aman.** Data contract kompatibel; tak ada gap skema yang memblokir port `render_lhp.py` (3108) + 18 skeleton. Analisis ini **tidak mengubah kode v10**.

## 1. Boundary & CLI
- `format_registry.py` **IDENTIK** (routing profil sama).
- `lhr_tools._render_kksa` memanggil `scripts/render_lhp.py --template …` dengan pola sama di kedua repo.
- CLI `render_lhp.py` v8.8 = **superset** v10: menambah `--nomor-nota-dinas`, `--tanggal-nota-dinas`, `--survei`, `--tembusan` (semua default None; hanya `--penugasan` wajib). → pemanggilan v10 saat ini **tetap kompatibel**; agar fitur penuh terpakai, **Fase 1: `lhr_tools` teruskan arg baru**.

## 2. Cakupan placeholder
- 18 skeleton, **145 placeholder unik**. render_lhp v8.8 mengisi ~142; 3 sisa (`{{LINK_SURVEI}}`, `{{OBJEK_AUDIT}}`, `{{TAHUN_ANGGARAN}}`) diisi dari args/context (bukan token hardcoded). **Koheren.**

## 3. Data contract (risiko R1) — KOMPATIBEL
render_lhp v8.8 membaca: `_KKP/temuan.json`, `_LHP/rekomendasi.json`, `_KKP/penilaian_lke.json`, `_PKP/sasaran-assignment.json`, `context.md` — **semua dihasilkan v10**.
- **Blok `penugasan`** (nomor_st/tanggal_st/obyek/tahun_anggaran): v10 **menulis** (`render_kkp.py:84`, `kkp_tools.py:302`). v8.8 membaca `kkp.get("penugasan",{}).get(x) or ctx.get(x)` → **fallback ke context.md**, robust.
- **temuan K/K/S/A** + `judul_temuan` + `sebab` + `deskripsi` + `sasaran`: schema berbagi.
- **penilaian_lke.json**: keduanya pakai `komponen`; verifikasi `predikat/interpretasi/total` saat uji render LKE.
- **Producer non-KKSA ADA di v10**: `write_penilaian_rb`, `append_saran`, `append_kegiatan_pendampingan` → profil memo/rb/pendampingan bersumber.

## 4. Titik perhatian (bukan blocker)
1. **`status_tl`** (pemantauan-tindak-lanjut): tak ada producer tool di v8.8 **maupun** v10; render_lhp v8.8 membacanya **defensif** (opsional, dari field temuan yang diisi agen). Verifikasi laporan TL saat uji; bukan blocker.
2. **LKE `predikat/interpretasi`**: konfirmasi nama field saat uji render evaluasi-LKE.
3. **Renderer non-KKSA (memo/rb/pendampingan)** = app-side di `lhr_tools`, **berbeda** antara v8.8↔v10 (bukan bagian render_lhp). Rekonsiliasi **per-hunk** di Fase 1: adopsi versi v8.8 yang selaras skeleton baru, jaga output tetap benar.

## 5. Rekomendasi urutan Fase 1
1. Copy **18 skeleton** (`_skeleton-lhp/*.docx`) + **2 template audit per-jenis** (Laporan Hasil Audit Kinerja/Umum) + skeleton `template-lhp-audit-kinerja/umum/pengadaan.docx`.
2. Swap `backend/v6/scripts/render_lhp.py` → versi v8.8 (3108).
3. Rekonsiliasi `lhr_tools.py`: adopsi boundary v8.8 (teruskan arg CLI baru; renderer non-KKSA) **+ PERTAHANKAN** additions v10 (`render_daftar_temuan`, `append_lampiran_tabel/diagram`, `_latest_lhp_docx`).
4. **Routing per-jenis audit** (keputusan user): `resolve_lhp_template` merutekan `audit-kinerja/umum/pengadaan` ke skeleton masing-masing.
5. **Uji render live** tiap keluarga di harness (reviu · audit · evaluasi-LKE · pemantauan · memo · rb · pendampingan) → `run_qc_lhp`. **Gerbang:** LHP ter-render benar + additions v10 utuh + QC lolos.

## Ringkasan gerbang
| Item | Status |
|---|---|
| Boundary/CLI kompatibel | ✅ |
| Placeholder koheren | ✅ |
| Data contract inti | ✅ |
| Producer non-KKSA ada | ✅ |
| status_tl / LKE predikat | ⚠️ verifikasi saat uji (bukan blocker) |
| Renderer non-KKSA lhr_tools | ⚠️ rekonsiliasi per-hunk Fase 1 |

**Kesimpulan: mulai Fase 1.**
