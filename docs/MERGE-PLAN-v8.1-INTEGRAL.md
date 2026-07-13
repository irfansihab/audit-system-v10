# Rencana Merge — `audit-system-v8.1` (INTEGRAL tim) ↔ v10 (engine)

> **Status: RENCANA saja. Belum ada perubahan kode/skill/engine.** Dokumen ini hasil investigasi read-only atas `github.com/marchelianaba/audit-system-v8.1` (clone dangkal) dibanding `sistem audit v10`. Dibuat 9 Jul 2026.

---

## 0. Ringkasan eksekutif (baca ini dulu)

**Realitas berbeda dari kesan awal.** v8.1 **bukan** rebuild INTEGRAL besar yang terpisah. Dari riwayat git-nya:

- Repo v8.1 hanya punya **1 branch (`main`), 7 commit**, dan **commit awalnya = "audit system v8.8"** (`dd8ba40`).
- Seluruh isi "INTEGRAL / CACM / EWS / TLHP / SIMWAS v2 / LhpReview / 7-tahapan" di README·HANDOVER·ROADMAP v8.1 **diwarisi dari v8.8** — bukan pekerjaan baru v8.1.
- Delta **nyata** v8.1 di atas v8.8 = **2 commit**: `d1180f1` (LKE SPIP/SAKIP rev4 + *batching per KK Lead* + template baru) dan `b716beb` (hapus artefak test/eval).

**Sementara itu v10 sudah menyerap seluruh v8.8** (Merge v8.8→v10 TUNTAS: render_lhp per-seksi, survey pendahuluan, gate LKE) **dan jauh melampauinya**: 20 skill *engine-ready* (pivot orkestrasi keluar dari skill), 3 skill BARU reviu keuangan + kriteria riil bernomor, eval harness *judge-aware*, doktrin lintas-skill (KKSAR/scoping/kriteria-tambahan/SAIPI), `export_dhp`/`export_surat`, route `administrasi`, `AdminTUPanel`, render buta-DB (P1c), plus RB masuk rezim LKE.

> **Kesimpulan:** v10 ⊇ v8.8 ⊇ (v8.1 − LKE). **Cakupan merge sebenarnya = MENGADOPSI 1 subsistem: peningkatan LKE (batching per KK Lead + template rev4 + kriteria SAKIP) dari v8.1 → v10**, direkonsiliasi dengan LKE v10 yang sudah lebih maju. Bukan reconciliation dua produk.

---

## 1. Bukti investigasi (read-only)

| Cek | Hasil |
|---|---|
| Branch v8.1 | hanya `main` (`git ls-remote`: 1 head) |
| Jumlah commit | 7; **initial = `dd8ba40` "audit system v8.8"** |
| Delta atas v8.8 (`9de52be..HEAD`) | `d1180f1` (LKE rev4/batching) + `b716beb` (hapus test/eval) |
| Skill *engine-ready* di v8.1 | **0** (skill masih pre-pivot: frontmatter `model`/`auto_execute`/`auto_execute_command` aktif — mis. `reviu-pengadaan` v1.7 v8.1 masih `auto_execute: true`) |
| Skill reviu keuangan (LK/PIPK/PNBP) di v8.1 | **tidak ada** |
| Doktrin scoping / kriteria-tambahan di v8.1 | **tidak ada** |
| Backend `app/` skeleton | ~95% identik (keduanya turun dari v8.8): `cacm_*`, `tlhp`, `lembar_reviu`, `survey_pendahuluan`, `lke_writer/lke_tools`, dll |
| v10-only (tak ada di v8.1) | `export_dhp.py`, `export_surat.py`, `routes/administrasi.py`, `AdminTUPanel.tsx`, `_LKE_EXCEL_SKILLS` + **RB**, `lke_writer.py`, skill `_draft` |
| v8.1-only (tak ada di v10) | `prefill_temuan.py` (v10 **sengaja hapus** di P3 — JANGAN kembalikan), **`lke_tools.py` batching per KK Lead** (15 fungsi), template LKE rev4 |

---

## 2. Peta divergensi (siapa unggul di mana)

| Domain | v10 (engine) | v8.1 (INTEGRAL tim) | Resolusi |
|---|---|---|---|
| **Skill (substansi)** | 20 engine-ready + 3 reviu keuangan + doktrin | 19 pre-pivot, tanpa reviu keuangan | **v10 menang mutlak** — JANGAN ambil skill v8.1 (akan membatalkan pivot P1) |
| **Eval / mutu** | harness judge-aware, golden, fixtures | dihapus (`b716beb`) | **v10 menang** — abaikan `b716beb` |
| **Render laporan** | render_lhp per-seksi (dari v8.8) + export_dhp/surat | render_lhp per-seksi (dari v8.8) | **setara** (sumber sama); v10 + export_* |
| **App-layer** (CACM/EWS/TLHP/LhpReview/SIMWAS/login) | ada (warisan v8.8) | ada (warisan v8.8) | **setara** (sumber sama) — verifikasi 3-way di Fase 0 |
| **Route administrasi/TU** | `administrasi.py` + `AdminTUPanel.tsx` | tidak ada | **v10 menang** |
| **LKE (evaluasi-spip/sakip)** | fill_lke + `lke_writer` + gate + **RB** di rezim + naming `LKE-terisi-<skill>.xlsx` | **batching per KK Lead** + **template rev4** + kriteria SAKIP diperbarui | **REKONSILIASI** — ini inti merge (Fase 1–3) |
| **Frontend visibilitas LKE** | — | LKE Excel tampil di panel Kertas Kerja & Draf Laporan (`page.tsx`) | **port dari v8.1** (Fase 4) |

---

## 3. Keputusan arah (perlu konfirmasi Anda)

**Rekomendasi: `v10` sebagai BASIS ("engine-forward"), port delta LKE v8.1 ke v10.**

Alasan: v10 secara faktual **superset** dari v8.1 kecuali subsistem LKE. Menjadikan v10 basis = pekerjaan paling kecil & paling aman (hanya adopsi 1 subsistem), tanpa risiko meregресi engine.

**Alternatif (bila git/ deployment tim mewajibkan repo v8.1 sebagai "repo of record" yang tersambung SIMWAS v2):** jadikan v8.1 basis, lalu **transplan engine v10** ke dalamnya. Karena engine v10 sudah *engine-ready* (orkestrasi ada di prompt, bukan skill; render buta-DB), transplan bersifat **mekanis tapi berpermukaan luas**: ganti SELURUH `knowledge/skills/` + `prompts/` + `app/tools|render|eval` + doktrin dengan versi v10, tambah 3 skill baru, tambah `export_dhp/surat`+`administrasi`. Risiko lebih tinggi (banyak file) — hanya tempuh bila ada alasan kepemilikan repo.

> ⚠ **Keputusan ini milik Anda** (tergantung: repo mana yang di-deploy ke SIMWAS v2, siapa yang lanjut maintain, kepemilikan git tim). Sisa rencana ditulis untuk jalur **rekomendasi (v10 basis)**; catatan untuk jalur alternatif diberi tanda *(ALT)*.

---

## 4. Cakupan merge sebenarnya (jalur v10 basis)

**PORT dari v8.1 → v10 (subsistem LKE saja):**
1. `backend/app/tools/lke_tools.py` — logika **batching per KK Lead** (243 baris berubah). Rekonsiliasi dengan LKE v10 (`lke_writer.py` + `lke_tools.py` + gate + RB).
2. Template LKE **rev4**: `lke-spip-kementerian.xlsx` (580KB→7.1MB), `LKE SPIP.xlsx`, `lke-sakip-kementerian.xlsx`. Rekonsiliasi lokasi (`knowledge/templates/` v8.1 vs `references/templates/` v10).
3. `evaluasi-sakip/references/01-kriteria-lke-permen88-2021.md` — pembaruan kriteria/cell-map (663 baris).
4. Penghapusan `cell-map-formulas.json` (−1513) — bila formula kini embedded di template (verifikasi jangan memutus fill_lke v10).
5. `evaluasi-spip/SKILL.md` & `evaluasi-sakip/SKILL.md` — perubahan "fill_lke WAJIB" **diadaptasi ke format engine-ready v10** (jangan bawa kembali orkestrasi/`auto_execute`).
6. `backend/app/prompts/anggota_tim.md` (+23) — langkah LKE; merge ke versi v10 (yang sudah punya scoping/kriteria-tambahan).
7. `frontend/app/penugasan/[id]/page.tsx` (+31) — tampilkan LKE Excel di panel; rekonsiliasi dengan frontend v10.

**JANGAN port:**
- ❌ `b716beb` (hapus eval) — v10 mempertahankan eval.
- ❌ Skill v8.1 apa pun secara utuh (pre-pivot → membatalkan P1). Hanya cuplikan LKE-spesifik yang diadaptasi.
- ❌ `prefill_temuan.py` — sudah dihapus sengaja di v10.
- ❌ Isi warisan v8.8 (CACM/TLHP/SIMWAS/dll) — sudah ada di v10.

---

## 5. Rencana bertahap (jalur v10 basis)

### Fase 0 — Pra-flight (WAJIB sebelum sentuh kode)
- Buat branch `feat/merge-v8.1-lke` di v10.
- **Diff 3-arah pada subsistem LKE** untuk memastikan tak ada kejutan: bandingkan file LKE (lke_tools/lke_writer/kkp_tools/2 SKILL/kriteria/template) antara **v8.8 (ancestor) ↔ v10 ↔ v8.1**. Tetapkan hunk mana milik v8.1-baru vs v10-baru.
- Verifikasi asumsi "v10 ⊇ v8.8" di level file (spot-check render_lhp, survey, gate LKE) — bila ada file v8.8 yang belum di v10, catat.
- **DoD:** matriks hunk LKE final + daftar file target.

### Fase 1 — Rekonsiliasi tool LKE (`lke_tools.py`)
- Padukan **batching per KK Lead** (v8.1) ke dalam LKE v10, **pertahankan**: konvensi `fill_lke(skill, entries) → _KKP/LKE-terisi-<skill>.xlsx`, gate `_LKE_EXCEL_SKILLS` (termasuk **RB**), guard sel-formula runtime.
- Bila v8.1 & v10 punya fungsi bertumpuk (mis. writer), pilih satu jalur; hindari dua implementasi paralel.
- **DoD:** `fill_lke` menghasilkan LKE-terisi dengan batching, untuk spip/sakip/**rb**, tanpa menimpa sel-formula.

### Fase 2 — Template LKE rev4 + kriteria SAKIP
- Adopsi template rev4 (spip/sakip). **Selaraskan lokasi** ke konvensi v10 (`references/templates/`), atau tetapkan `knowledge/templates/` sebagai kanonik & sesuaikan resolver template. Satu sumber kebenaran.
- Terapkan pembaruan `01-kriteria-lke-permen88-2021.md`.
- Uji: peta cell rev4 cocok dengan `fill_lke` v10 (tak ada sel salah/tergeser).
- **DoD:** LKE-terisi rev4 valid dibuka Excel, agregator & predikat benar.

### Fase 3 — SKILL.md LKE (adaptasi engine-ready)
- Terapkan "fill_lke WAJIB" & perbaikan baris stale **dalam gaya v10** (substansi murni; TANPA `model`/`auto_execute`; orkestrasi tetap di `anggota_tim.md`/INTEGRAL).
- Pastikan pengecualian LKE (tak menerima kriteria-tambahan yang mengubah instrumen) tetap utuh.
- **DoD:** frontmatter tetap engine-ready; grep `auto_execute` di skill = 0.

### Fase 4 — Frontend visibilitas LKE
- Port perubahan `page.tsx` agar LKE Excel tampil di panel Kertas Kerja (AT) & Draf Laporan (KT), rekonsiliasi dengan frontend v10 (jaga `AdminTUPanel` & fitur v10-only).
- **DoD:** `next build` hijau; file `_KKP/LKE-terisi-*.xlsx` terlihat di kedua panel.

### Fase 5 — Validasi
- **LKE E2E**: setup → agen isi → `fill_lke` (batching) → `_KKP/LKE-terisi-<skill>.xlsx` → gate `render_kkp_docx` → tampil di UI. Untuk spip **dan** sakip **dan** rb.
- **Eval harness hijau**: `live_measure`/`run_eval` untuk evaluasi-spip/sakip (+rb) tetap SKOR sehat (LKE=AoI); tidak ada regresi 20 skill lain.
- **Render deterministik**: sweep render bersih 0 placeholder (jaga jalur render tunggal v10).
- **DoD:** semua hijau; 0 regresi engine.

*(ALT — bila v8.1 jadi basis):* balik arah — Fase 1–4 diganti "transplan engine v10 ke v8.1": salin `knowledge/skills/` + `prompts/` + `app/{tools,render,eval,export_dhp,export_surat}` + `routes/administrasi` + `AdminTUPanel` dari v10, tambah 3 skill baru, hapus `prefill_temuan`, lalu jalankan Fase 5 yang sama.

---

## 6. Register risiko & konflik

| Risiko | Dampak | Mitigasi |
|---|---|---|
| **Ambil skill v8.1 utuh** | Batalkan pivot engine-ready P1 (regres 20 skill) | Hanya adaptasi cuplikan LKE; JANGAN salin folder skill v8.1 |
| **LKE ber-evolusi ganda** (v10 RB vs v8.1 batching) | Konflik/logika dobel | Diff 3-arah (Fase 0); satukan satu jalur; pertahankan RB v10 + naming v10 |
| **Lokasi template beda** (`knowledge/templates` vs `references/templates`) | Template tak ketemu saat fill_lke | Tetapkan satu lokasi kanonik + sesuaikan resolver |
| **Hapus `cell-map-formulas.json`** | fill_lke v10 kehilangan formula | Verifikasi formula kini embedded di template rev4 sebelum hapus |
| **Reintroduksi `prefill_temuan`/eval-removal** | Regres v10 | Abaikan `b716beb`; jangan bawa `prefill_temuan` |
| **Frontend v10-only tergerus** | Hilang `AdminTUPanel`/fitur v10 | Merge hunk-level pada `page.tsx`, bukan timpa file |

---

## 7. Gerbang validasi (semua harus hijau sebelum merge ke main)
1. Diff 3-arah LKE terdokumentasi (Fase 0).
2. `fill_lke` batching → LKE-terisi valid untuk spip/sakip/rb; gate aktif.
3. Template rev4 + peta cell benar (buka Excel, agregator OK).
4. Skill LKE tetap engine-ready (grep `auto_execute`=0).
5. Eval: evaluasi-spip/sakip/rb sehat; 20 skill lain 0 regresi.
6. `next build` hijau; LKE terlihat di 2 panel.
7. Render sweep 0 placeholder.

---

## 8. Rekomendasi & langkah berikutnya
- **Konfirmasi arah** (§3): v10 basis (rekomendasi) atau v8.1 basis.
- Setelah dikonfirmasi → jalankan **Fase 0** (diff 3-arah LKE) untuk mengunci daftar hunk sebelum sentuh kode.
- Estimasi jalur rekomendasi: **kecil** (1 subsistem LKE), risiko rendah karena engine v10 tak disentuh.
- Catatan komunikasi ke tim: perjelas bahwa v8.1 ≈ v8.8 + LKE; agar tim tak menaruh pekerjaan baru di skill pre-pivot (arahkan kontribusi ke format engine-ready v10).

---

*Dokumen turunan: `docs/MERGE-PLAN-v8.8-to-v10.md` (pola merge sebelumnya) · investigasi read-only clone `marchelianaba/audit-system-v8.1`.*
