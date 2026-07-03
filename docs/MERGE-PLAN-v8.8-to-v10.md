# Rencana Merge: audit-system-v8.8 (marchelianaba) → v10

**Status:** RENCANA disetujui — **belum ada perubahan kode/skill/template diterapkan** (eksekusi menyusul). **Sumber:** `marchelianaba/audit-system-v8` @ `9de52be` (v8.8, 28 Jun 2026). **Target:** `irfansihab/audit-system-v10`.

> **Keputusan (1 Jul 2026):**
> - **Cakupan = PENUH** (Fase 1–5, termasuk rekonsiliasi frontend). Fase 4 (per-hunk tidying) & Fase 5 (frontend) kini **dalam cakupan**, bukan opsional.
> - **Adopsi pemisahan LHP audit per-jenis** (Laporan Hasil Audit → **Kinerja / Umum / Pengadaan** terpisah), selaras skill `audit-*` v10 — perlu memastikan routing template (skeleton `template-lhp-audit-kinerja/umum/pengadaan.docx` + `format_registry`/resolve).
> - **QC SAIPI:** pertahankan versi **v10** (`check_LAK_005` Sebab jenis-aware); JANGAN ambil `qc_saipi.py` v8.8.
> - **Reviu LKj/SPIP tabel-kriteria:** tetap di luar cakupan (fase lanjutan, sesuai catatan desain v8.8).
> - **Eksekusi belum dimulai** — dokumen ini di-commit sebagai acuan; langkah berikut menunggu aba-aba.

## 1. Situasi & lineage
v8.8 = **keturunan paralel** dari v8 (bukan leluhur v10). Timeline: v8 → { v9→v10 (Juknis + engine-ready + hardening) } dan { v8.x→v8.8 (revisi format laporan + tidying, dipakai sbagai **engine SIMWAS V2**) }. Keduanya punya kerja yang tidak dimiliki lawannya. History v8.8 di-squash ("Initial commit: audit system v8.8"), jadi merge = **port selektif berbasis konten**, bukan `git merge`.

**Inti nilai v8.8 (yang diminta):** *pemakaian template laporan* — `render_lhp.py` dirombak **454→3108 baris** dengan skeleton **placeholder per-seksi** (mis. `{{A1_LATAR_BELAKANG}}`, `{{III_A_PERENCANAAN}}`, `{{BAB2_1_TUJUAN_DESAIN}}`, `{{IV_REKOMENDASI}}`) — laporan jauh lebih faithful per jenis. v10 masih skema **generik-loop** (`{{HASIL_REVIU_LOOP}}`, `{{GAMBARAN_UMUM}}`).

## 2. Peta divergensi (file berbeda)
| Area | Δ | Arah dominan |
|---|---|---|
| `knowledge/templates` | 18 differ + 2 baru | **v8.8 ahead** (skeleton revisi + LHP Audit Kinerja/Umum) |
| `backend/v6/scripts` | render_lhp.py, render_kkp.py, qc_saipi.py | **campur** (render_lhp=v8.8 ahead; qc_saipi=v10 ahead [fix Sebab]) |
| `backend/app` | 25 differ; v8.8-only: `survey_pendahuluan.py`, `prefill_temuan.py`; v10-only: `export_dhp.py`, `export_surat.py`, `administrasi.py` | **campur** |
| `knowledge/skills` | 24 differ | **v10 ahead** (engine-ready; v8.8 pre-pivot) → **JANGAN port** |
| `frontend` | 7 differ; v10-only `AdminTUPanel` | campur; **prioritas rendah** (harness) |

## 3. Klasifikasi

### 3A. PORT dari v8.8 (nilai tinggi)
1. **Subsistem render laporan (headline)** — unit terkopel:
   - `backend/v6/scripts/render_lhp.py` (versi 3108-baris, fill per-seksi).
   - `knowledge/templates/_skeleton-lhp/*.docx` (18 skeleton revisi).
   - `knowledge/templates/Laporan Hasil Audit Kinerja.docx` + `...Audit Umum.docx` (2 baru) + template LHP top-level lain yang berubah.
   - Boundary **stabil**: `format_registry.py` IDENTIK; `lhr_tools._render_kksa` memanggil `scripts/render_lhp.py --template` dengan pola sama di kedua repo → swap kompatibel di batas.
2. **`survey_pendahuluan.py`** (v8.8-only) — renderer *Laporan Survei Pendahuluan* .docx untuk skill audit (tahap A0), dibangun python-docx dari `context.md`+`_INGESTED`+`_PKP`. Fitur deliverable baru; self-contained. Port modul + wiring pemanggil (`routes/penugasan.py`).
3. **Gate LKE-Excel-mandatory** (`kkp_tools.py:535–560` v8.8) — `render_kkp_docx` menolak bila LKE Excel belum dibuat untuk SPIP/SAKIP (deliverable wajib). Selaras doktrin LKE v10. Port sebagai hunk ke `render_kkp_docx` v10.

### 3B. JANGAN PORT (akan meregresi v10)
- **`knowledge/skills/*`** — v8.8 pre-pivot (mis. reviu-pengadaan masih 5× "Eksekusi di v7"). Meng-overwrite = membatalkan **engine-ready 16/16 + hardening Fase 1**. Substansi template ada di file template/render, bukan di skill → skip total.
- **`prefill_temuan.py`** — sudah dihapus di v10 (P3 dead-code). Jangan hidupkan.
- Apa pun yang membalik: QC SAIPI Sebab jenis-aware (v10 `qc_saipi.py`), penghapusan dead-code (`read_anomalies`/`build_draft`), frontmatter `model:`, terminologi KKSAR/2E.
- **v10-only jangan hilang:** `export_dhp.py`, `export_surat.py`, `administrasi.py`, `render_daftar_temuan`/`append_lampiran_tabel`/`append_lampiran_diagram` di `lhr_tools.py` (0 di v8.8).

### 3C. PER-HUNK (tinjau, cherry-pick selektif)
File berbeda karena KEDUA sisi berubah — jangan overwrite; bandingkan hunk:
- `backend/app/tools/lhr_tools.py` — adopsi boundary render_lhp v8.8 **+ pertahankan** additions v10 (daftar_temuan/lampiran).
- `backend/app/tools/kkp_tools.py` — ambil gate LKE v8.8; pertahankan P3/engine-ready v10.
- `backend/app/prompts/{anggota_tim,ketua_tim}.md` — v10 engine-ready + de-anomali; v8.8 punya alur render_report per-profil. Rekonsiliasi hati-hati (jangan balik engine-ready).
- `backend/v6/scripts/render_kkp.py` — bandingkan; ambil perbaikan v8.8 bila ada.
- `models.py/config.py/init_db.py/schemas.py/storage.py/routes/*` — mayoritas **v10 ahead** (TU/administrasi/export). Default **pertahankan v10**; cherry-pick hanya tidying v8.8 yang jelas & tak konflik.

## 4. Kontrak data yang WAJIB diverifikasi (pra-port render_lhp)
render_lhp v8.8 mengisi seksi dari struktur data. Pastikan skema v10 cocok:
- `_KKP/temuan.json` (skema temuan K/K/S/A + kode), `_LHP/rekomendasi.json`, `context.md` (Gambaran Umum, Identitas), `_LHP/penilaian_lke.json` / `saran.json` / penilaian RB.
- Bila v8.8 render_lhp mengharap field yang v10 tak hasilkan (atau sebaliknya) → sesuaikan tool penulis (bukan render). **Cek ini di Fase 0.**

## 5. Risiko
- **R1 (utama):** render_lhp v8.8 mengasumsikan skema data / placeholder yang berbeda → LHP gagal/pincang. *Mitigasi:* diff skema + uji render tiap profil di harness sebelum commit.
- **R2:** overwrite tak sengaja meregresi engine-ready/hardening. *Mitigasi:* whitelist file (3A), larangan (3B); tinjau per-hunk (3C); registry-load + grep residu setelah tiap langkah.
- **R3:** boundary lhr_tools bergeser (offset baris beda) → invocation putus. *Mitigasi:* rekonsiliasi fungsi `_render_kksa`/`render_report`, uji live.
- **R4:** `render_lhp.py` V6 diperlakukan "read-only" secara konvensi — tapi ini justru file yang di-swap. *Mitigasi:* ini penggantian berversi, bukan edit ad-hoc; dokumentasikan.

## 6. Urutan eksekusi bertahap (tiap fase: harness hijau + commit)
- **Fase 0 — Pra-flight (tanpa ubah v10):** ekstrak & bandingkan skema data (temuan/rekomendasi/context/lke/saran/rb) + set placeholder tiap skeleton v8.8 vs kontrak render_lhp v8.8; petakan gap. **Gerbang:** daftar penyesuaian jelas.
- **Fase 1 — Subsistem render laporan:** copy 18 skeleton + 2 template; swap `render_lhp.py`; rekonsiliasi `lhr_tools.py` (jaga additions v10). **Uji:** render LHP live tiap keluarga (reviu/audit/evaluasi-LKE/pemantauan) di harness → QC. **Gerbang:** LHP ter-render benar + additions v10 utuh.
- **Fase 2 — Survei Pendahuluan:** port `survey_pendahuluan.py` + wiring. **Uji:** generate laporan survei untuk penugasan audit.
- **Fase 3 — Gate LKE mandatory:** port hunk ke `render_kkp_docx`. **Uji:** SPIP/SAKIP tanpa LKE → render ditolak; dengan LKE → lolos.
- **Fase 4 — Per-hunk sisa (DALAM CAKUPAN):** cherry-pick tidying v8.8 yang bernilai (render_kkp, prompt, backend) tanpa meregresi engine-ready/hardening. Tinjau tiap hunk; default pertahankan v10.
- **Fase 5 — Frontend (DALAM CAKUPAN):** rekonsiliasi `login/page.tsx`, `penugasan/[id]/page.tsx`, `penugasan/page.tsx`, `HeroPenugasan/LembarReviuPanel/TopBar` — pertahankan `AdminTUPanel` (v10-only) + fitur admin/TU; adopsi perbaikan v8.8. Uji di harness (login → penugasan → render).

## 7. Keputusan (terjawab 1 Jul 2026)
1. **Cakupan** → **PENUH** (Fase 1–5, termasuk per-hunk & frontend).
2. **LHP audit per-jenis** → **ADOPSI** pemisahan Kinerja/Umum/Pengadaan. Tugas tambahan: pastikan `resolve_lhp_template`/`format_registry` merutekan tiap `audit-*` ke skeleton-nya; verifikasi 3 skeleton + template top-level tersedia & placeholder-nya diisi render_lhp.
3. **QC SAIPI** → **PERTAHANKAN v10** (`check_LAK_005` Sebab jenis-aware). Jangan ambil `qc_saipi.py` v8.8.
4. **Reviu LKj/SPIP tabel-kriteria** → **DI LUAR CAKUPAN** (fase lanjutan).

## 8. Langkah berikut
Eksekusi **belum dimulai** (sesuai keputusan "commit rencana dulu"). Saat diberi aba-aba, mulai **Fase 0 (pra-flight, read-only)** → lapor gap skema → lanjut Fase 1. Repo sumber tersedia di clone lokal `scratchpad/v8-simwas` (bisa di-clone ulang: `gh repo clone marchelianaba/audit-system-v8`).
