# Task 03 — Generate Kertas Kerja Pengawasan (KKP) — v4

> **Model**: `claude-sonnet-4-6` — Analisis dokumen mendalam, sintesis temuan KKSA, memerlukan penalaran tinggi.

> **Hanya boleh dijalankan oleh role: Anggota Tim (AT)**. Akan ditolak oleh `scripts/role_check.py` jika dipanggil oleh ketua tim.

## Tujuan
Analisis dokumen berdasarkan skill yang aktif, lalu hasilkan **KKP dalam dua format**:
1. `_KKP/temuan.json` — sumber kebenaran (untuk inject ke INTEGRAL), valid terhadap `schemas/kkp-temuan.schema.json`.
2. `_KKP/KKP-[nama-anggota].docx` — view per anggota tim (untuk dibaca auditor & ketua tim).

**Penting v4**: anggota tim **HANYA boleh** mengerjakan KKP untuk sasaran yang `assigned_to`-nya mencantumkan namanya di `_PKP/sasaran-assignment.json`. Sasaran milik anggota lain harus dibiarkan untuk dikerjakan anggota tsb.

---

## Pre-Check v4 (WAJIB sebelum mulai)

```bash
# 1. Role check — tolak kalau bukan Anggota Tim
python3 scripts/role_check.py --penugasan penugasan/[nama] --task 03

# 2. Pastikan sasaran-assignment ada
test -f penugasan/[nama]/_PKP/sasaran-assignment.json || \
  { echo "Jalankan Task 01 dulu untuk ekstrak pembagian sasaran."; exit 1; }

# 3. Ambil daftar sasaran milik user yang sedang login (lihat _ROLE.md)
#    Hanya sasaran ini yang boleh diisi di langkah 5.

# 4. Log start
python3 scripts/audit_trail.py log-event --penugasan penugasan/[nama] \
  --action TASK_STARTED --task 03 --target _KKP/temuan.json
```

---

## Prasyarat
- `context.md` sudah ada (Task 01)
- `_PKP/sasaran-assignment.json` sudah ada dan valid (Task 01)
- `_ROLE.md` sudah ada (Task 00)
- (audit-kinerja) Memo SP boleh disusun di chat sebagai bagian dari Task 03 langkah 0a, tidak perlu file terpisah
- KP dan PKP sudah ada di `00-input/` (di-upload auditor dari INTEGRAL)

> **Catatan v4**: Task 02 (Validasi Dokumen) dan Task 02b (Generate KP+PKP) sudah dihapus. KP+PKP datang dari INTEGRAL. File listing + ringkasan dokumen dilakukan inline di Task 03 Langkah 1 & 2 di bawah.

> **Khusus audit-kinerja**: Baca Memo SP sebelum menyusun KKP. Gunakan **Hipotesis Audit Awal (bagian 8 Memo SP)** sebagai daftar awal isu yang diuji di KKP. Setiap temuan di KKP harus dapat ditelusuri ke sasaran hasil penajaman (Memo SP bagian 6) dan tetap berada dalam ruang lingkup terukur (Memo SP bagian 7).

---

## Langkah Eksekusi

### 0. Pre-digest & Cross-check otomatis (WAJIB untuk skill yang memiliki pipeline)

Untuk skill yang sudah memiliki pipeline deterministik di `audit-system-v4/scripts/[skill]/`, jalankan skrip pre-digest dan cross-check **sebelum analisis manual Langkah 1–4**. Tujuan: deteksi anomali struktural bersifat deterministik dipindahkan dari reasoning Claude ke script — hemat konteks, akurasi naik, reproducible.

**Mapping skill → scripts:**

| Skill | Scripts tersedia | Input | Output |
|---|---|---|---|
| `reviu-rka-kl` | `scripts/reviu-rka-kl/{digest_tor,digest_rab,cross_check,render_lhr}.py` | TOR.pdf + RAB.pdf di `03-perencanaan/` | `_KKP/tor.json`, `_KKP/rab.json`, `_KKP/anomalies.json`, `_LHP/LHR-DRAFT.docx` |
| `audit-pengadaan` | `scripts/audit-pengadaan/{digest_pengadaan,cross_check,render_lha}.py` | Folder penugasan (KAK/HPS/Kontrak/BAST/LS/SPTB campuran PDF+DOCX) | `_KKP/pengadaan-digest.json`, `_KKP/anomalies.json`, `_LHP/LHA-DRAFT.docx` |
| `reviu-pengadaan` | Digest reuse `scripts/audit-pengadaan/digest_pengadaan.py` + `scripts/reviu-pengadaan/cross_check.py` | Folder penugasan (KAK/HPS/SPPBJ sampai Kontrak) | Sama — `anomalies.json` dengan kolom KKP tanpa Sebab |
| `evaluasi-sakip` | `scripts/evaluasi-sakip/{digest_lke,cross_check,render_lhe}.py` (v5.0 production) | LKE.xlsx + LKj/PK/RKT pendukung | `_KKP/lke.json`, `_KKP/anomalies.json`, `_LHP/LHE-DRAFT.docx` |
| `evaluasi-spip` | `scripts/evaluasi-spip/{cross_check,render_lhe}.py` (v1.4 — input LKE SPIP sudah JSON dari Task 02 manual) | LKE SPIP (sudah ter-digest manual) | `_KKP/anomalies.json`, `_LHP/LHE-DRAFT.docx` |
| `pemantauan-pengadaan` | `scripts/pemantauan-pengadaan/` (skeleton — reuse `digest_pengadaan.py`) | Kontrak + Laporan Bulanan + BAST progres | Belum v1 |
| (skill lain) | (belum ada — fallback ke Langkah 1 manual) | — | — |

**Eksekusi untuk reviu-rka-kl:**

```bash
# Asumsi: cwd = root repo audit-system-v4
cd audit-system-v4

# Siapkan folder output
mkdir -p penugasan/[nama-penugasan]/_KKP

# 1. Digest TOR
python3 scripts/reviu-rka-kl/digest_tor.py \
  "penugasan/[nama-penugasan]/03-perencanaan/[TOR].pdf" \
  --no-raw \
  -o "penugasan/[nama-penugasan]/_KKP/tor.json"

# 2. Digest RAB
python3 scripts/reviu-rka-kl/digest_rab.py \
  "penugasan/[nama-penugasan]/03-perencanaan/[RAB].pdf" \
  -o "penugasan/[nama-penugasan]/_KKP/rab.json"

# 3. Cross-check
python3 scripts/reviu-rka-kl/cross_check.py \
  "penugasan/[nama-penugasan]/_KKP/tor.json" \
  "penugasan/[nama-penugasan]/_KKP/rab.json" \
  -o "penugasan/[nama-penugasan]/_KKP/anomalies.json"
```

**Hasil yang harus dibaca Claude:**

- `anomalies.json` — daftar anomali terdeteksi otomatis (18 rules, menutupi ~76% catatan umum). Setiap anomali memuat `rule_id`, `severity` (KRITIS/PERINGATAN/INFO), `aspek`, `judul`, `bukti`, dan `draft_catatan` (Kondisi/Kriteria/Akibat/Rekomendasi siap-format).
- `tor.json` dan `rab.json` — struktur terparse sebagai konteks ringkas (baca bila perlu detail, bukan seluruh PDF).

**Penggunaan di Langkah 3–4:**

Catatan-catatan di `anomalies.json` adalah **baseline deterministik**. Claude **tidak perlu meng-ekstraksi ulang** informasi yang sudah ter-parse (nilai rupiah, nomor akun, nama kabupaten, formula BCR, dll.). Fokus Claude pada:
- Memverifikasi bukti tiap anomali (buka halaman TOR/RAB relevan untuk konfirmasi bila ada keraguan)
- Menyaring false positive (rules kadang over-flag; tandai anomali yang perlu dihapus dari KKP)
- **Menambah catatan substantif** yang TIDAK dideteksi rules — mis. kualitas formula KPI (butuh judgment matematis), relevansi kebijakan program, nuansa konteks regional yang hanya auditor tahu
- Memformat `draft_catatan` ke kolom tabel KKP sesuai format skill aktif (Kondisi/Kriteria/[Sebab]/Akibat)

**Bila pre-digest gagal (script error, parser tidak match dokumen):**

Catat error di log, lanjut ke Langkah 1–4 dengan metode manual standar. Sampaikan ke auditor bahwa pipeline gagal sehingga reviu dilakukan secara penuh manual dan memerlukan lebih banyak tokens/waktu.

**Eksekusi untuk audit-pengadaan:**

```bash
cd audit-system-v4

mkdir -p penugasan/[nama-penugasan]/_KKP penugasan/[nama-penugasan]/_LHP

# 1. Digest (scan folder + klasifikasi 14 jenis dokumen + parse)
python3 scripts/audit-pengadaan/digest_pengadaan.py \
  "penugasan/[nama-penugasan]" \
  -o "penugasan/[nama-penugasan]/_KKP/pengadaan-digest.json"

# 2. Cross-check (11 rules atas aspek Perencanaan/Kontrak/Pelaksanaan/Pembayaran)
python3 scripts/audit-pengadaan/cross_check.py \
  "penugasan/[nama-penugasan]/_KKP/pengadaan-digest.json" \
  -o "penugasan/[nama-penugasan]/_KKP/anomalies.json"

# 3. Render LHA (dengan kolom KKP: No, Judul, Kondisi, Kriteria, Sebab, Akibat)
python3 scripts/audit-pengadaan/render_lha.py \
  "penugasan/[nama-penugasan]/_KKP/anomalies.json" \
  "penugasan/[nama-penugasan]/context.md" \
  -o "penugasan/[nama-penugasan]/_LHP/LHA-DRAFT.docx"
```

**Eksekusi untuk reviu-pengadaan** (reuse digest audit-pengadaan):

```bash
python3 scripts/audit-pengadaan/digest_pengadaan.py "penugasan/[nama]" -o "penugasan/[nama]/_KKP/pengadaan-digest.json"
python3 scripts/reviu-pengadaan/cross_check.py "penugasan/[nama]/_KKP/pengadaan-digest.json" -o "penugasan/[nama]/_KKP/anomalies.json"
```

**Eksekusi untuk evaluasi-sakip** (skeleton v0.1 — butuh sample LKE untuk tuning):

```bash
python3 scripts/evaluasi-sakip/digest_lke.py "penugasan/[nama]/03-perencanaan/LKE-SAKIP.xlsx" -o "penugasan/[nama]/_KKP/lke.json"
# cross_check + render belum v1 — Claude harus fallback ke analisis manual untuk 4 komponen SAKIP
```

**Untuk skill yang belum memiliki pipeline**: skip Langkah 0, lanjut langsung ke Langkah 1.

---

### 1. Muat konteks + File Listing

Baca `context.md`. **Untuk audit-kinerja**, baca juga `_SP/SP-[nomor-ST].docx` dan `_PKP/PKP-[nomor-ST].docx`.

Lakukan **file listing** (baca hanya nama file, bukan isi) untuk folder relevan:

| Folder | Baca untuk skill ini? |
|--------|-----------------------|
| `00-surat-tugas/` | ✅ Selalu |
| `01-peraturan-internal/` | ✅ Jika ada |
| `02-kontrak/` | ✅ Reviu/audit pengadaan |
| `03-perencanaan/` | ✅ Selalu untuk reviu/audit |
| `04-pelaksanaan/` | ✅ Audit penuh / pemantauan |
| `05-keuangan/` | ✅ Audit penuh |

> **Pemeriksaan kosong total**: Jika **tidak ada dokumen sama sekali** di seluruh folder relevan (hanya ada ST saja, atau bahkan ST pun tidak ada), **JANGAN lanjutkan analisis**. Sampaikan kepada auditor:
> ```
> ⚠️ TIDAK ADA DOKUMEN UNTUK DIPERIKSA
>
> Untuk menganalisis [jenis pengawasan] atas [obyek], diperlukan minimal dokumen berikut di folder penugasan:
>   • [sebutkan 2–3 dokumen minimum sesuai skill, mis. KAK, HPS, Kontrak]
>
> Saat ini folder berikut kosong:
>   • [daftar folder relevan yang kosong]
>
> Mohon upload dokumen tersebut terlebih dahulu, lalu ketik LANJUT untuk memulai ulang Task 03.
> ```
> Berhenti di sini — jangan membuat KKP dengan analisis halu.

### 2. Ringkasan Singkat Dokumen (inline, hemat token)

Untuk setiap dokumen yang ditemukan, baca secara bertarget (bukan seluruh halaman) dan catat ringkasan singkat **di memori conversation** — tidak perlu disimpan ke file. Gunakan sebagai basis analisis Langkah 3 agar dokumen tidak dibaca berulang.

**Panduan membaca PDF besar (hemat token):**
- Halaman 1–3: Identitas dokumen (judul, tanggal, nilai, penandatangan)
- Halaman latar belakang / tujuan: Periode, nilai SLA, cakupan
- Halaman spesifikasi teknis: SLA, kapasitas, standar, komponen
- Halaman klausul khusus (migrasi, pembayaran, SLA): Komponen biaya
- **Jangan** baca halaman yang tidak relevan dengan aspek yang diperiksa

**Template ringkasan per jenis dokumen:**

```
### [Jenis dok] — [nama file]
- Tanggal / Nomor: [...]
- Nilai (jika ada): Rp [...]
- Periode: [...]
- Poin penting untuk analisis: [butir spesifik relevan dengan SKILL.md]
- Halaman sumber yang dirujuk: [p. 1-3, p. 12, dst.]
```

Jika dokumen wajib tertentu **tidak ada tapi ada dokumen lain**, catat sebagai keterbatasan (tidak stop Task 03) dan nyatakan di KKP bagian "Catatan dokumen tidak tersedia".

### 3. Lakukan analisis dokumen

**Jika Langkah 0 dijalankan dan `_KKP/anomalies.json` tersedia:**
Analisis dimulai dari daftar anomali yang sudah ter-deteksi script. Untuk setiap anomali:
1. Verifikasi bukti (buka halaman TOR/RAB yang dirujuk bila ada keraguan)
2. Tentukan status: **TERIMA** (masuk KKP), **TOLAK** (false positive, skip), atau **MODIFIKASI** (edit draft_catatan sebelum masuk KKP)
3. Lalu **tambahkan catatan substantif** yang tidak dideteksi rules — aspek yang butuh judgment:
   - Kualitas formula/metodologi (mis. formula KPI yang benar secara matematis)
   - Relevansi kebijakan dan arah strategis
   - Nuansa lapangan/konteks regional
   - Analisis kedalaman teks yang tidak tertangkap regex

**Jika Langkah 0 tidak dijalankan** (skill belum punya pipeline, atau script error):
Analisis manual dari ringkasan di Langkah 2. Untuk aspek yang perlu konfirmasi lebih dalam, baca bagian spesifik dokumen asli. Untuk setiap aspek yang diperiksa (sesuai SKILL.md), evaluasi apakah kondisi yang ditemukan sesuai atau tidak sesuai dengan kriteria.

**⚡ UNTUK REVIU PENGADAAN — lakukan pemeriksaan konsistensi internal secara aktif:**
Sebelum menutup analisis, selalu periksa secara eksplisit:
- Apakah ada nilai/angka yang berbeda antara bagian Latar Belakang dan Persyaratan Teknis KAK? (SLA, kapasitas, periode)
- Apakah periode yang disebut di KAK konsisten dengan dokumen pengadaan aktual?
- Apakah KAK menyebut ada proses migrasi, dan apakah komponen biaya migrasi tersebut ada di HPS?
- Apakah nilai HPS proporsional dengan durasi/cakupan pengadaan aktual?

Lihat `references/01-aspek-perencanaan.md` bagian "Pemeriksaan Konsistensi Internal KAK" dan "Pemeriksaan Komponen Biaya HPS" untuk panduan lengkap.

**Prinsip analisis:**
- Catat kondisi berdasarkan fakta dokumen — sertakan nama file + halaman/pasal sumber
- Kriteria dari `references/` — gunakan teks normatif yang tepat (nomor pasal)
- Sebab (SEMUA jenis pengawasan, doktrin 17 Jun 2026 — lihat `panduan-format-umum/PANDUAN.md`): audit = WAJIB gali akar penyebab; reviu/evaluasi/pemantauan = isi bila terbukti dari dokumen, bila tidak tulis jujur "Tidak ditemukan penyebab"/"Tidak cukup data" — JANGAN mengarang
- Akibat: konsekuensi/risiko dari kondisi yang ditemukan; jika sesuai ketentuan nyatakan "tidak ada dampak negatif"
- Setiap catatan memiliki **Judul Temuan** — kalimat deskriptif (lihat panduan judul di bawah)

**Panduan Judul Temuan:**
- Kondisi sesuai    → "[Aspek] Telah Sesuai dengan Ketentuan" / "...Telah Memenuhi Persyaratan"
- Kondisi kurang    → "Terdapat [Masalah] pada [Aspek]" / "[Aspek] Belum [Ditetapkan/Dilengkapi]"
- Tidak dapat dinilai → "[Aspek] Belum Dapat Dinilai karena [Alasan]"

**Jangan cantumkan Rekomendasi di KKP** — rekomendasi dirumuskan bersama auditor setelah feedback KKP diterima.

### 4. Susun daftar catatan/temuan

Urutkan:
- Catatan yang memerlukan tindakan (kondisi tidak sesuai) → dahulukan berdasarkan urgensi
- Catatan yang sesuai ketentuan → di bagian akhir atau beri tanda "(sesuai)"
- Catatan yang tidak dapat dinilai → sertakan dengan keterangan alasan

### 5. Generate KKP Word (tabel sederhana)

Buat file Word dengan format berikut. **Gunakan format sederhana** — tidak perlu warna-warni atau desain kompleks.

#### Struktur dokumen:

```
KERTAS KERJA PENGAWASAN — DRAFT
[Jenis Pengawasan] | [Obyek]
ST: [Nomor ST] | Periode: [tanggal] | Ketua Tim: [nama]
---

DAFTAR CATATAN / TEMUAN

[TABEL — lihat kolom per jenis di bawah]

---
Catatan dokumen tidak tersedia:
[Daftar dokumen yang diperlukan tapi tidak ada]

⚠️ KKP INI ADALAH DRAFT — Mohon berikan feedback melalui chat sebelum LHP dibuat.
Untuk setiap catatan: apakah kondisi/kriteria sudah tepat? Ada yang perlu ditambah/diubah?
```

#### Format kolom tabel berdasarkan jenis pengawasan:

**Audit (keyakinan memadai):**
| No | Judul Temuan | Kondisi | Kriteria | Sebab | Akibat |
|----|-------------|---------|----------|-------|--------|
| 1  | [judul]     | [kondisi fakta + sumber dok] | [pasal + ketentuan] | [akar masalah] | [risiko/dampak] |

**Reviu (keyakinan terbatas):**
| No | Judul Temuan | Kondisi | Kriteria | Akibat |
|----|-------------|---------|----------|--------|
| 1  | [judul]     | [kondisi fakta + sumber dok] | [pasal + ketentuan] | [risiko/dampak] |

**Pemantauan:**
| No | Judul Temuan | Kondisi | Kriteria |
|----|-------------|---------|----------|
| 1  | [judul]     | [kondisi fakta + sumber dok] | [pasal + ketentuan] |

**Evaluasi (RB, MR, SPIP, dll):**
| No | Judul Temuan | Kondisi | Kriteria | Akibat |
|----|-------------|---------|----------|--------|
| 1  | [judul]     | [kondisi fakta + sumber dok] | [pasal/standar] | [risiko/dampak] |

#### Format tabel Word:
- Gunakan table border standar (solid line semua sisi)
- Header baris pertama: bold, background abu-abu muda (#D9D9D9)
- Teks isi: font Arial 10pt, rata kiri
- Lebar kolom: sesuaikan agar terbaca — kolom Kondisi/Kriteria lebih lebar dari kolom No
- Tidak perlu warna per baris berdasarkan status — KKP adalah dokumen kerja, bukan presentasi

### 6. Simpan file

**v4.0.4 — pakai renderer terstandar daripada generate dari scratch.**

KKP DOCX dihasilkan oleh `scripts/render_kkp.py` yang baca `_KKP/temuan.json` (sumber kebenaran) + `context.md`, lalu render tabel sesuai paradigma jenis pengawasan — KKSA penuh (Kondisi-Kriteria-Sebab-Akibat) untuk audit/reviu/evaluasi non-LKE/**pemantauan**; evaluasi ber-LKE (RB/SAKIP/SPIP) tanpa kolom Sebab (rezim LKE); konsultasi pakai kolom khusus — di-handle otomatis.

```bash
# Render KKP untuk anggota saat ini (dari _ROLE.md)
python3 scripts/render_kkp.py --penugasan penugasan/[nama] --anggota "Sarah Aulia"

# atau render untuk semua anggota yang sudah punya temuan
python3 scripts/render_kkp.py --penugasan penugasan/[nama] --all-anggota
```

Output: `_KKP/KKP-[Nama-Anggota].docx` (landscape, kolom auto-sized).

Claude **tidak perlu** menulis script python-docx custom — gunakan renderer ini. Kalau renderer error pada kasus skill baru, fallback ke generate manual dengan struktur yang sama (header standar + tabel kolom sesuai jenis).

### 6a. Jalankan QC otomatis (WAJIB sebelum minta konfirmasi auditor)

Sebelum menyerahkan draft KKP kepada auditor, jalankan **dua QC validator** untuk mendeteksi masalah umum:

**6a.1 — QC anti-halusinasi (sumber dokumen, rek bocor, judul):**
```bash
python3 audit-system-v4/scripts/qc_kkp_lhp.py penugasan/[folder-penugasan] --only kkp
```

**6a.2 — QC kepatuhan SAIPI (v4 — stage KKP):**
```bash
python3 scripts/qc_saipi.py --penugasan penugasan/[folder-penugasan] --stage kkp
```

`qc_saipi.py` mengecek standar SAIPI 1100, 1200, 2200, 2300 (independensi, kecakapan, perencanaan, pelaksanaan). Output:
- `_QA-SAIPI/checklist-kkp.json` (master)
- `_QA-SAIPI/laporan-qa-kkp.md` (narasi)
- 1 event audit-trail (action=`VALIDATION_PASSED` atau `VALIDATION_FAILED`)

**Aturan gate:**
- Exit 0 (PASS) → boleh lanjut ke Langkah 7 (konfirmasi anggota tim).
- Exit 2 (ada KRITIS) → **JANGAN lanjut**. Tampilkan isi `laporan-qa-kkp.md` ke chat, koreksi gap KRITIS dulu, jalankan ulang.
- PERINGATAN/NEEDS_REVIEW → boleh lanjut, tapi sebutkan ringkasannya di pesan ke auditor agar sadar (auditor bisa beri justifikasi tertulis di `_QA-SAIPI/justifikasi.md`).

Aturan hasil QC:

- **Status PASS** (exit 0, tidak ada ERROR) → lanjut ke Langkah 7 (konfirmasi auditor).
- **Status FAIL** (ada ERROR, mis. kondisi tanpa sumber dokumen, rekomendasi terdeteksi di KKP) → **JANGAN minta konfirmasi auditor dulu**. Perbaiki isi KKP berdasar daftar error, simpan ulang, jalankan QC lagi sampai PASS. Dokumentasikan perubahan yang dilakukan ketika memberitahu auditor.
- **Warning** (bukan error fatal, mis. font bukan Arial di beberapa run) → boleh lanjut, tapi sebutkan warning di pesan ke auditor agar ia sadar.

Tujuan QC: menjamin setiap kondisi punya sumber yang bisa ditelusuri (anti-halusinasi) dan KKP tidak bercampur dengan unsur LHP.

### 6b. Tulis JSON `_KKP/temuan.json` (v4 — sumber kebenaran)

Setelah analisis selesai, untuk setiap temuan yang dihasilkan dari sasaran milik user, append ke `_KKP/temuan.json` dengan struktur:

```json
{
  "id_temuan": "T-001",                          // T-NNN unik per penugasan
  "sasaran_id": "S-01",                          // dari sasaran-assignment.json
  "anggota_tim": {                               // dari _ROLE.md
    "nama_lengkap": "Sarah Aulia",
    "role_kode": "AT"
  },
  "judul_temuan": "Kalimat deskriptif kondisi...",
  "kondisi": "...",
  "kriteria": "...",
  "sebab": "...",                                // null untuk reviu/pemantauan
  "akibat": "...",
  "dokumen_sumber": [
    {"file": "03-KAK-XXX.pdf", "halaman": "12", "kutipan": "..."}
  ],
  "tanggal_input": "2026-05-02T15:00:00+07:00",
  "status": "DRAFT",
  "catatan_ketua_tim": null,
  "integral": null
}
```

Validasi:
```bash
python3 scripts/validate_kkp_json.py penugasan/[nama]/_KKP/temuan.json
# harus exit 0 sebelum lanjut.
```

Update `sasaran-assignment.json` — ubah status sasaran user menjadi `SELESAI_KKP` dan isi `id_temuan_terkait`.

Log:
```bash
python3 scripts/audit_trail.py log-event --penugasan penugasan/[nama] \
  --action KKP_TEMUAN_ADDED --task 03 --target _KKP/temuan.json \
  --payload '{"sasaran_id": "S-01", "id_temuan": "T-001"}'

python3 scripts/audit_trail.py log-event --penugasan penugasan/[nama] \
  --action SASARAN_COMPLETED --task 03 --target _PKP/sasaran-assignment.json \
  --payload '{"sasaran_id": "S-01"}'
```

### 6c. Generate Word view per anggota tim (v4)

Setelah `temuan.json` divalidasi, generate `_KKP/KKP-[nama-anggota].docx` yang berisi temuan-temuan milik user (filter `anggota_tim.nama_lengkap == user`).

> Anggota lain bisa generate KKP-nya sendiri di sesi terpisah. JSON `temuan.json` adalah file bersama append-only.

### 7. Konfirmasi kepada auditor

```
=== KKP DRAFT SELESAI (anggota: [Nama Anda]) ===
JSON master  : _KKP/temuan.json   (validator: PASS)
Word view    : _KKP/KKP-[Nama Anda].docx
Sasaran Anda : [S-XX, S-YY] — [N] temuan
QC auto      : PASS [/ PASS dengan [n] warning]

Status sasaran (semua anggota):
  S-01 [Sarah Aulia]   → SELESAI_KKP ([k] temuan)
  S-02 [Budi Hartono]  → BELUM_DIKERJAKAN
  S-03 [Sarah, Budi]   → SELESAI_KKP / BELUM (campuran)

Dokumen tidak tersedia (keterbatasan):
  [daftar jika ada, atau "Semua dokumen tersedia"]

⚠️ Buka file Word di atas, beri feedback di sini:
  - Kondisi/kriteria sudah tepat?
  - Ada temuan yang perlu ditambah/diubah/dihapus?
  - Setelah disetujui, status temuan akan diubah ke DIREVIU_KETUA_TIM
    dan menunggu ketua tim untuk Task 04.
```

---

## Output v4
- `_KKP/temuan.json` — JSON master (untuk INTEGRAL & Task 04)
- `_KKP/KKP-[nama-anggota].docx` — view auditor
- `_PKP/sasaran-assignment.json` di-update (status sasaran → SELESAI_KKP, id_temuan_terkait diisi)
- 3-N events di `_AUDIT-TRAIL/events.jsonl`
- Auditor membuka Word & memberi feedback via chat

## ⛔ GATE — Jangan lanjutkan ke Task 04 sebelum:
1. Auditor sudah membuka dan membaca KKP
2. Auditor memberikan feedback/konfirmasi via chat (minimal "OK lanjut" atau koreksi spesifik)
3. Jika ada koreksi → perbaiki isi KKP sesuai feedback, simpan sebagai versi baru, minta konfirmasi ulang
4. Setelah konfirmasi final → simpan feedback → lanjut ke Task 04

### 📋 Simpan Feedback KKP

Setelah auditor memberikan feedback (baik koreksi maupun persetujuan), simpan ke:
`audit-system-v4/feedback/[YYYY-MM-DD]-KKP-[nomor-ST].md`

Format file feedback:
```
# Feedback KKP — [nomor ST]
Tanggal     : [tanggal hari ini]
Obyek       : [nama obyek dari context.md]
Skill       : [nama skill]
Versi KKP   : [v1 / v2 / dst]

## Feedback Auditor
[Tulis verbatim atau ringkasan koreksi dari auditor]

## Aspek yang Dikoreksi
- [ ] Kondisi (fakta/data)
- [ ] Kriteria (dasar hukum)
- [ ] Akibat/risiko
- [ ] Judul catatan
- [ ] Cakupan (ada catatan yang terlewat / tidak perlu)
- [ ] Format/penyajian
- [ ] Lain-lain: [sebutkan]

## Tindak Lanjut
[Jelaskan perubahan yang dilakukan pada KKP sesuai feedback — atau "Disetujui tanpa koreksi"]
```

> Jika auditor menyetujui tanpa koreksi, tetap simpan feedback dengan isi "Disetujui tanpa koreksi" — ini berguna untuk memahami kasus yang sudah benar.

---

## 🚀 Auto-Inject ke INTEGRAL (BARU — setelah konfirmasi DISETUJUI)

Setelah auditor SETUJU tanpa koreksi lagi, jalankan auto-inject ke INTEGRAL:

```bash
python3 audit-system-v4/scripts/integral_inject.py \
    --penugasan penugasan/[nama-penugasan]
```

Script ini akan:
1. Baca `_KKP/temuan.json` dan filter temuan milik anggota saat ini yang berstatus DISETUJUI
2. Map ke schema INTEGRAL (sebab/akibat boleh `null` untuk Reviu/Pemantauan/Evaluasi)
3. POST ke endpoint `/kertas-kerja` dengan status `ai_draft`
4. Update status temuan ke `DIINJECT_INTEGRAL` di `temuan.json`
5. Catat event `INTEGRAL_EXPORT` di audit trail

### Skip List (Tidak di-Auto-Inject)

Untuk jenis pengawasan berikut, script akan otomatis skip dan minta auditor inject manual:
- `konsultasi-pengadaan` (struktur kolom beda total)
- `evaluasi-spip` (output LKE Excel, bukan tabel KKP)
- `evaluasi-reformasi-birokrasi` (output LKE per triwulan)
- `pemantauan-tindak-lanjut` (output TLHP skeleton)

### Penanganan Error

| Exit code | Arti | Aksi Claude |
|---|---|---|
| 0 | Sukses inject atau skip karena jenis manual-only | Lanjut, tampilkan ID KKP & url_view ke auditor |
| 1 | Error konfigurasi (env var, _ROLE.md) | Beritahu auditor hubungi Admin Inspektorat II |
| 2 | Error validasi (NIP, temuan.json) | Minta auditor lengkapi NIP di _ROLE.md |
| 3 | Error HTTP dari INTEGRAL (403/404/422/5xx) | Tampilkan pesan error, file Excel/JSON tetap di folder, auditor bisa upload manual |

### Pesan ke Auditor (setelah sukses)

```
✅ KKP berhasil dikirim ke INTEGRAL dengan status DRAFT.

📄 ID KKP    : [id_kkp dari response]
🔗 Link review: [url_view dari response]
📊 Jumlah    : [N] temuan

⚠️ PENTING: KKP belum final. Silakan login ke INTEGRAL,
   review draft, lalu klik "Approve" agar muncul di
   dashboard ketua tim/pimpinan.
```

### Konfigurasi (sekali setup oleh Admin)

Env variable yang harus di-set di Cowork org-level:
```
INTEGRAL_API_BASE_URL=https://simwasv2.komdigi.go.id/api/v1
INTEGRAL_SERVICE_TOKEN=<token dari tim INTEGRAL>
COWORK_USER_EMAIL=<auto dari Cowork>
```

NIP auditor harus ada di `_ROLE.md` (field `nip:` di frontmatter), atau di env var `COWORK_USER_NIP`.

---

## Catatan Penting
- **Tidak ada Rekomendasi di KKP** — rekomendasi ada di LHP
- Jika analisis membutuhkan konfirmasi fakta yang nilainya material (>Rp 500 juta untuk audit), tanyakan kepada auditor sebelum memasukkan ke KKP
- Level detail isi tabel disesuaikan dengan jenis pengawasan — audit lebih mendalam dari reviu
