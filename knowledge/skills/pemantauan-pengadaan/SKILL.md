---
name: pemantauan-pengadaan
format_laporan: kksa
version: 2.2
jenis: Pemantauan Pelaksanaan Pengadaan Barang/Jasa
dasar-hukum: Perpres 16/2018 jo. Perpres 12/2021, Perpres 46/2025
model: claude-haiku-4-5-20251001
auto_execute: false
changelog:
  - v2.2 (2026-06-17): Refactor orkestrasi ke v7 — Tahap P0–P4 seragam; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); role+sasaran via sasaran-assignment.json; HITL=KT approve KKP→KT draft Laporan Pemantauan; tak ada tool pipeline v7 (manual). Substansi pemantauan kontrak/PBJ dipertahankan.
---

# Skill: Pemantauan Pengadaan Barang/Jasa

## Identitas
- **Jenis Pengawasan:** Pemantauan Pelaksanaan Pengadaan Barang/Jasa
- **Tingkat Keyakinan:** Tidak ada — hanya pelaporan status
- **Kode Nomor Surat:** PW.04.06
- **Versi:** 2.2

---

## Eksekusi di v7 (orkestrasi — seragam semua skill pemantauan)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dari `_PKP/sasaran-assignment.json` (diisi KT via UI Setup). AT hanya kerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline P3:** *tidak ada tool v7 — manual* (baca dokumen kontrak/progres/pembayaran ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** P0→P3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft Laporan Pemantauan**.
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → pantau status/progres per paket → `append_temuan` (status + Sebab bila terbukti; jika tidak "tidak ditemukan penyebab"/"tidak cukup data", jangan mengarang) → `record_pkp_assessment` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Pemantauan (P0–P4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **P0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode dari KP jelas; dokumen kontrak/progres/pembayaran tersedia; susun `context.md` bila placeholder. | AT (auto) |
| **P1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan pemantauan, ruang lingkup (paket/periode), metodologi — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **P2 — Program Kerja Pengawasan (PKP)** | Per sasaran: paket/aspek yang dipantau · bukti diminta · kriteria status. | KT (UI Setup) |
| **P3 — Pelaksanaan** | Per paket: pantau progres fisik vs pembayaran, kepatuhan jadwal/kontrak → `append_temuan` (status + Sebab bila terbukti; jika tidak "tidak ditemukan penyebab"/"tidak cukup data", jangan mengarang) → `record_pkp_assessment`. Indikasi penyimpangan serius → eskalasi audit-pengadaan. | AT (auto) |
| **P4 — Laporan Pemantauan** | Render Laporan Pemantauan + Nota Dinas; rekap status paket & isu yang perlu tindak lanjut. | KT |

**Analisis substantif yang wajib dilakukan AT pada P3** (status — Sebab diisi bila terbukti; jika tidak "tidak ditemukan penyebab"/"tidak cukup data", jangan mengarang):
- **Kewajaran progres fisik vs keuangan** — hitung deviasi % progres fisik aktual vs % pembayaran kumulatif. Bayar > fisik signifikan → risiko over-payment; fisik > bayar signifikan → klaim penyedia tertunda.
- **Pola amandemen** — frekuensi & nilai kumulatif addendum. Addendum berulang atau > 10% nilai kontrak → indikasi perencanaan lemah.
- **Kepatuhan SLA penyedia** — bandingkan laporan berkala penyedia dengan SLA kontrak; catat pelanggaran SLA sebagai isu.
- **Denda keterlambatan** — bila ada keterlambatan milestone, hitung denda 1/1000 per hari sesuai Pasal 78 Perpres 16/2018 (catat sebagai isu/status, bukan kerugian).
- **Realisasi deliverable/milestone vs lingkup & jadwal Kontrak/KAK** — bandingkan deliverable/milestone yang **dijadwalkan** per Kontrak/KAK (sampai periode laporan) dengan yang **dilaporkan** sudah diserahkan/dikerjakan (BA kemajuan, laporan berkala penyedia/pengawas). Tandai sebagai isu/risiko: milestone jatuh tempo belum tercapai, deliverable kurang/di luar lingkup, atau output tidak sesuai cakupan KAK. **Sebagai PEMANTAUAN (bukan audit):** laporkan sebagai "kondisi perlu perhatian" + rekomendasi tindak lanjut; **JANGAN** menyimpulkan pelanggaran, **JANGAN** menilai kualitas teknis fisik sendiri (pakai data laporan pengawas/penyedia), **JANGAN** hitung kerugian. Indikasi serius output ≠ kontrak → rekomendasikan **eskalasi ke audit-pengadaan**.

---

## Peran Claude

Kamu bertugas **melaporkan kondisi aktual pelaksanaan pengadaan** kepada pimpinan. Tugasmu adalah mengukur progres fisik dan keuangan terhadap target kontrak, lalu mencatat isu-isu yang memerlukan perhatian sebagai peringatan dini.

Pemantauan **bukan audit dan bukan reviu**. Kamu tidak menyimpulkan pelanggaran, tidak menghitung kerugian, dan tidak menilai kewajaran harga. Semua isu disampaikan sebagai "kondisi yang perlu perhatian" — bukan temuan.

---

## Posisi dalam Keluarga Skill PBJ

Baca `shared-pbj-references/PANDUAN.md` untuk:
- Perbandingan lengkap 4 jenis pengawasan pengadaan (audit, reviu, pemantauan, konsultasi)
- Panduan kapan menggunakan skill ini vs skill lainnya
- Daftar file referensi regulasi di `../audit-pengadaan/references/`

**Singkatnya:**

| | Audit | Reviu | **Pemantauan** | Konsultasi |
|---|---|---|---|---|
| Keyakinan | Memadai | Terbatas | **Tidak ada** | Tidak ada |
| Ruang lingkup | Seluruh siklus | Perencanaan + pemilihan | **Pelaksanaan kontrak aktif** | Sesuai pertanyaan |
| Pengujian bukti | Sangat mendalam | Administratif | **Deskriptif — status aktual** | Analisis regulasi |

---

## Yang Dikerjakan

### 1. Ukur Progres

| Aspek | Data yang Dikumpulkan | Sumber Dokumen |
|---|---|---|
| Progres fisik (%) | Laporan berkala penyedia, BA kemajuan | `04-pelaksanaan/` |
| Target progres (%) | Jadwal dalam kontrak | `02-kontrak/` |
| Progres keuangan | SPM/SP2D yang sudah terbit | `05-keuangan/` |
| Nilai kontrak | Kontrak + addendum | `02-kontrak/` |
| Sisa waktu (hari) | Tanggal selesai kontrak vs hari ini | `02-kontrak/` |

Status pelaksanaan ditetapkan sebagai:
- **🟢 ON TRACK** — deviasi progres ≤ 5%
- **🟡 AT RISK** — deviasi progres 5–15% atau ada isu yang perlu perhatian
- **🔴 DELAYED** — deviasi > 15% atau milestone kritis terlewati

### 2. Catat Isu

Setiap isu ditulis dalam format:

```
ISU [Nomor]: [Judul singkat]
Urgensi: 🔴 SEGERA / 🟡 PERLU PERHATIAN / 🟢 INFORMASI

Kondisi Terkini:
[Fakta aktual. Sertakan: tanggal data, angka/persentase, nama dokumen sumber]

Seharusnya (Kriteria):
[Target/ketentuan dari kontrak atau regulasi. Sebutkan pasal/klausul jika ada]

Potensi Risiko: *(jika relevan)*
[Apa yang bisa terjadi jika tidak segera ditangani]

Tindakan yang Direkomendasikan:
[Langkah konkret, oleh siapa, dalam berapa hari]
```

**Isu-isu yang dipantau:**
- Deviasi progres fisik vs jadwal kontrak
- Deviasi pembayaran vs progres fisik
- Keterlambatan dan perhitungan denda (1/1000 per hari — Pasal 78 Perpres 16/2018)
- Addendum berulang atau bernilai besar (kumulatif > 10% nilai kontrak)
- Kepatuhan penyedia: laporan berkala, tenaga ahli, produk dalam negeri
- Milestone kritis yang terlewati

**Batasan pencatatan isu:**
- JANGAN menyimpulkan pelanggaran — gunakan "kondisi yang perlu perhatian"
- JANGAN menghitung kerugian negara — itu domain audit
- JANGAN menilai kualitas teknis fisik — gunakan data dari laporan penyedia/pengawas
- Jika data tidak tersedia: catat `[Data tidak tersedia — perlu konfirmasi PPK]`

---

## Format Output

### Dokumen yang Dihasilkan:
1. **Nota Dinas Pengantar** — ikuti format di `panduan-format-umum/PANDUAN.md`
2. **Laporan Hasil Pemantauan** — struktur di bawah ini

### Struktur Laporan:

```
A. PENDAHULUAN
   1. Latar Belakang
   2. Dasar Pelaksanaan
   3. Tujuan dan Ruang Lingkup
   4. Metodologi
   5. Periode Pemantauan
   6. Komposisi Tim

B. PROFIL PEKERJAAN
   [Nama paket, nomor kontrak, nilai, penyedia, PPK, jangka waktu]

C. STATUS PELAKSANAAN (per tanggal laporan)
   [Dashboard progres — lihat template di bawah]

D. ISU DAN PERMASALAHAN
   [Setiap isu dalam format Kondisi → Kriteria → Potensi Risiko → Rekomendasi]

E. PERUBAHAN KONTRAK (jika ada addendum)
   [Ringkasan addendum yang sudah terjadi]

F. TINDAK LANJUT PEMANTAUAN SEBELUMNYA (jika bukan pemantauan pertama)
   [Status isu dari laporan sebelumnya]

G. SIMPULAN DAN REKOMENDASI
   [Status keseluruhan + kompilasi rekomendasi per isu]

H. APRESIASI
```

### Dashboard Status (wajib ada di bagian C):

```
╔══════════════════════════════════════════════════════╗
║         STATUS PELAKSANAAN — [NAMA PAKET]           ║
║         Per Tanggal: [DD Bulan YYYY]                ║
╠══════════════════════════════════════════════════════╣
║ Progres Fisik   : [XXX%] ████████░░ Target: [YYY%] ║
║ Progres Bayar   : Rp [X] dari Rp [Y] ([Z]%)        ║
║ Sisa Waktu      : [X] hari dari [Y] hari total      ║
║ Status          : [🟢 ON TRACK / 🟡 AT RISK / 🔴 DELAYED] ║
╠══════════════════════════════════════════════════════╣
║ Jumlah Isu Aktif: [X] isu                           ║
║   🔴 Segera     : [X] isu                           ║
║   🟡 Perhatian  : [X] isu                           ║
║   🟢 Informasi  : [X] isu                           ║
╚══════════════════════════════════════════════════════╝
```

### KKP Pemantauan (tabel Word sederhana):

| No | Kondisi Terkini | Target / Kriteria | Isu / Risiko | Rekomendasi |
|----|-----------------|-------------------|--------------|-------------|
| 1  | [fakta + sumber] | [kontrak/regulasi] | [risiko jika dibiarkan] | [tindakan konkret] |

---

## Cara Membaca Dokumen

Urutan prioritas baca:
1. `00-surat-tugas/` → scope dan paket yang dipantau
2. `02-kontrak/` → nilai, jadwal, klausul pembayaran dan addendum
3. `04-pelaksanaan/` → laporan berkala, BA kemajuan, laporan penyedia
4. `05-keuangan/` → SPM/SP2D yang sudah terbit

---

## Referensi Regulasi

Pemantauan pengadaan menggunakan regulasi yang sama dengan audit, reviu, dan konsultasi pengadaan.

**Panduan lengkap:** `../shared-pbj-references/PANDUAN.md`

**File referensi regulasi** (semua ada di `../audit-pengadaan/references/`):
- `01-perpres-16-2018.md` — prinsip, pelaku, kontrak, pelaksanaan, denda
- `02-perpres-12-2021.md` — perubahan threshold
- `05-perpres-46-2025.md` — ketentuan kontrak dan pembayaran terbaru

Untuk pemantauan, pasal yang paling sering digunakan:
- Denda keterlambatan → Pasal 78 Perpres 16/2018
