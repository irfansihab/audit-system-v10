---
name: pemantauan-tindak-lanjut
format_laporan: kksa
version: 0.2
jenis: Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)
fungsi: Pemantauan — Monitoring (tanpa keyakinan/assurance)
dasar-hukum: PP 60/2008 Pasal 50, Permenpan 5/2008
model: claude-sonnet-4-6
output: Laporan Hasil Pemantauan TLHP + Update Status
status: skeleton
changelog:
  - v0.2 (2026-06-17): Refactor orkestrasi ke v7 — Tahap P0–P4 seragam; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); role+sasaran via sasaran-assignment.json; HITL=KT approve KKP→KT draft Laporan Pemantauan. Substansi status TL dipertahankan.
---

# Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)

## Identitas
- **Nama Skill:** pemantauan-tindak-lanjut
- **Versi:** 0.2 (19 April 2026; refactor v7 17 Juni 2026)
- **Jenis Pengawasan:** Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)
- **Fungsi APIP:** Pemantauan/monitoring — **tidak memberi keyakinan (assurance)**, hanya melaporkan status/perkembangan tindak lanjut
- **Format Output:** Laporan Hasil Pemantauan TLHP + matrix aging Excel
- **Model AI:** Claude Sonnet 4.6

## Eksekusi di v7 (orkestrasi — seragam semua skill pemantauan)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dari `_PKP/sasaran-assignment.json` (diisi KT via UI Setup). AT hanya kerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline P3:** *tidak ada tool v7 — manual* (baca dokumen/rekomendasi ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** P0→P3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft Laporan Pemantauan**.
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → cek status TL per rekomendasi → `append_temuan` (status + Sebab bila terbukti; jika tidak "tidak ditemukan penyebab"/"tidak cukup data", jangan mengarang) → `record_pkp_assessment` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Pemantauan (P0–P4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **P0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode dari KP jelas; daftar rekomendasi/temuan yang dipantau + bukti TL tersedia; susun `context.md` bila placeholder. | AT (auto) |
| **P1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan pemantauan, ruang lingkup (rekomendasi/periode), metodologi — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **P2 — Program Kerja Pengawasan (PKP)** | Per sasaran: daftar rekomendasi yang dipantau · bukti TL yang diminta · kriteria status TL. | KT (UI Setup) |
| **P3 — Pelaksanaan** | Per rekomendasi: nilai status TL (Selesai / Dalam Proses / Belum Ditindaklanjuti / Tidak Dapat Ditindaklanjuti) berdasarkan bukti + hitung umur (aging) → `append_temuan` (status + Sebab bila terbukti; jika tidak "tidak ditemukan penyebab"/"tidak cukup data", jangan mengarang) → `record_pkp_assessment`. | AT (auto) |
| **P4 — Laporan Pemantauan** | Render Laporan Hasil Pemantauan TLHP + Nota Dinas; rekap status TL, aging per PIC & daftar rekomendasi kritis yang masih terbuka. | KT |

## Tujuan

Memastikan seluruh rekomendasi pengawasan eksternal (BPK) dan internal (BPKP, Itjen) **ditindaklanjuti tepat waktu dan tepat substansi** oleh unit kerja Kemkomdigi. Output: laporan periodik yang dikirim ke Menteri/Sekjen dengan dashboard status + daftar rekomendasi kritis yang belum selesai.

## Ruang Lingkup

- **TLHP BPK**: rekomendasi LHP BPK (per semester, tahun berjalan + backlog)
- **TLHP BPKP**: rekomendasi LHP BPKP (evaluasi SPIP, audit kinerja, review LK)
- **TLHP APIP**: rekomendasi LHP Itjen (audit + reviu + evaluasi)
- **Peer Review**: rekomendasi peer review APIP (jika ada)

## Paradigma

**Monitoring** — bukan assurance. Auditor mencatat status *apa adanya* berdasarkan bukti tindak lanjut yang diserahkan unit kerja. **Analisis Sebab (anti-mengarang)** — diisi bila terbukti dari bukti (mis. penyebab keterlambatan TL); bila tidak ditemukan/bukti tidak cukup → tulis "Tidak ditemukan penyebab"/"Tidak cukup data", jangan mengarang. Pemantauan tidak menghitung kerugian.

## Kolom KKP / Tabel Pemantauan

| No | Asal LHP | No Rek | Substansi Rekomendasi | PIC | Deadline | Status | Umur (hari) | Keterangan |
|----|----------|--------|-----------------------|-----|----------|--------|-------------|-----------|

**Status values**:
- **Selesai** — bukti tindak lanjut lengkap dan memadai, rekomendasi ditutup
- **Dalam Proses** — ada tindak lanjut parsial, perlu pendalaman
- **Belum Ditindaklanjuti** — tidak ada bukti tindak lanjut
- **Tidak Dapat Ditindaklanjuti** — justifikasi kuat kenapa rek tidak relevan lagi (perlu SK penghapusan)

**Umur (hari)** = hari sejak terbit LHP sampai cut-off pemantauan.
- 0–90 hari: 🟢 hijau
- 91–180 hari: 🟡 kuning
- 181–365 hari: 🟠 orange
- >365 hari: 🔴 merah (kritis — wajib perhatian Menteri)

## Alur Eksekusi

### Langkah 1 — Muat Daftar Rekomendasi

Sumber data (urutan prioritas):
1. Database TLHP Itjen (jika sudah ada aplikasi internal — integrasi ke depan)
2. File Excel rekap manual `TLHP-[sumber]-[tahun].xlsx`
3. Scan/ekstrak rekomendasi dari file LHP (.pdf/.docx) di folder `lhp-sumber/`

### Langkah 2 — Klasifikasi Status

Baca folder bukti tindak lanjut (`bukti-tl/`) per rekomendasi:
- Jika ada ≥1 bukti relevan + substansial → *Dalam Proses* (minimal)
- Jika bukti menutup seluruh item rekomendasi → *Selesai*
- Jika tidak ada file bukti → *Belum Ditindaklanjuti*

**Anti-halusinasi**: setiap status harus mengutip nama file bukti (atau "tidak ada file").

### Langkah 3 — Aging Analysis

Hitung umur (hari), klasifikasikan ke kategori warna. Agregasi per PIC:

```
PIC: [Unit Kerja]
  Total rekomendasi: [n]
  Selesai: [n]
  Proses: [n]
  Belum: [n] (merah: [n], orange: [n], kuning: [n])
  Aging rata-rata belum-selesai: [hari]
```

### Langkah 4 — Identifikasi Rekomendasi Kritis

Rekomendasi dengan umur >365 hari + status ≠ Selesai otomatis naik ke **Daftar Kritis** yang disorot di laporan + ringkasan eksekutif ke Menteri.

### Langkah 5 — Susun Laporan

Laporan Hasil Pemantauan TLHP di-render KT pada tahap **P4** (ikuti `panduan-format-umum/PANDUAN.md`).

Struktur:
1. Ringkasan Eksekutif (1 halaman — untuk Menteri/Sekjen)
2. Statistik Umum (total rek, % selesai, per sumber)
3. Aging per PIC (tabel + ranking worst)
4. Daftar Rekomendasi Kritis (>365 hari)
5. Rekomendasi percepatan
6. Lampiran: matrix lengkap (Excel separate)

## Integrasi dengan Skill Lain

- **evaluasi-spip**: skor Komponen IV (Informasi-Komunikasi) dan V (Pemantauan) bisa memakai data TLHP sebagai bukti dukung
- **evaluasi-sakip**: Komponen Evaluasi Akuntabilitas Internal merujuk persentase penyelesaian TLHP
- **audit-kinerja**: temuan berulang dari TLHP bisa jadi input Hipotesis Audit Awal di Memo SP

## Kerangka References yang Dibutuhkan

| # | File | Isi | Status |
|---|------|-----|--------|
| 01 | `01-pp-60-2008-spip.md` | Pasal kewajiban TLHP | ⬜ |
| 02 | `02-keputusan-bpk-tlhp.md` | Mekanisme koordinasi Kemkomdigi-BPK | ⬜ |
| 03 | `03-template-matrix-aging.xlsx` | Template Excel untuk aging analysis | ⬜ |
| 04 | `04-panduan-klasifikasi-status.md` | Kriteria detail kapan rek dianggap Selesai/Proses/Belum | ⬜ |

## Status Skill

⬜ **SKELETON** — v0.1 (19 April 2026). Dibuat sebagai bagian upgrade sistem v2.8. Perlu piloting di 1 penugasan pemantauan TLHP aktual untuk validasi alur + template.

## Catatan Implementasi

- Pemantauan TLHP dilakukan **rutin per semester** (Jan–Jun, Jul–Des) oleh Itjen → bangun template yang reusable lintas periode.
- Laporan dikirim bersamaan dengan LHP tahunan Itjen ke Menteri.
- Integrasi masa depan: pull data dari SIMWAS Itjen (aplikasi internal) — saat ini masih manual Excel.
