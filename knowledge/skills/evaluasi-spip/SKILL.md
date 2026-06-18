---
name: evaluasi-spip
format_laporan: kksa
version: 1.6
jenis: Penjaminan Kualitas Penilaian Maturitas Penyelenggaraan SPIP Terintegrasi
dasar-hukum: Peraturan BPKP Nomor 5 Tahun 2021
model: claude-sonnet-4-6
output: Lembar Kerja Evaluasi (xlsx) — kolom Nilai PK terisi + Catatan + AoI
template: references/templates/lke-spip-kementerian.xlsx
auto_execute: false
changelog:
  - v1.6 (2026-06-17): Refactor orkestrasi ke v7 — struktur seragam Tahap E0–E4; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); role+sasaran via sasaran-assignment.json; HITL=KT approve KKP→KT draft LHE. TANPA unsur Sebab — evaluasi ber-LKE (rezim seperti Eval RB): penilaian = Nilai PK (skor maturitas LKE) per unsur/sub-unsur + AoI, bukan KKSA (lihat panduan-format-umum/PANDUAN.md). Substansi SPIP (komponen/unsur/sub-unsur, LKE, kriteria gradasi, bobot, penalti) dipertahankan utuh.
---

# Skill: Evaluasi SPIP — Penjaminan Kualitas (PK) oleh APIP

## Eksekusi di v7 (orkestrasi — seragam semua skill evaluasi)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dibaca dari `_PKP/sasaran-assignment.json` (diisi Ketua Tim via UI Setup). AT hanya mengerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline E3:** *tidak ada tool v7 — criteria/LKE-driven manual* (LKE SPIP diisi/diolah manual; baca dokumen ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** E0→E3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft LHE** (bukan stop tiap tahap).
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → penilaian per komponen/sub-unsur SPIP → `append_temuan` (catatan/AoI **tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) → `write_penilaian_lke` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Evaluasi (E0–E4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **E0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode dari KP jelas; LKE SPIP (template `references/templates/lke-spip-kementerian.xlsx`) + dokumen pendukung per unsur tersedia; susun `context.md` bila masih placeholder. | AT (auto) |
| **E1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan, ruang lingkup, komponen/unsur SPIP yang dinilai (Penetapan Tujuan, Struktur & Proses, Pencapaian Tujuan), metodologi PK atas PM — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **E2 — Program Kerja Pengawasan (PKP)** | Per sasaran: unsur/sub-unsur SPIP yang dinilai · langkah pengujian bukti · bukti yang dicari. | KT (UI Setup) |
| **E3 — Pelaksanaan & KKP** | Per unsur/sub-unsur: tetapkan Nilai PK (skor maturitas 1–5 LKE, independen dari Nilai PM) berdasar bukti → catatan/AoI (**tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) → `append_temuan` + `write_penilaian_lke`. Veto penalti via `KK4_PENALTI` bila ada kasus korupsi (lihat seksi Mekanisme Penalti). | AT (auto) |
| **E4 — Laporan (LHE)** | Render LHE + Nota Dinas; simpulan tingkat maturitas SPIP (Level 1–5) & Area of Improvement prioritas. | KT |

## Posisi dalam Keluarga Skill Kinerja

> Termasuk dalam keluarga skill kinerja (audit-kinerja, evaluasi-sakip, evaluasi-spip, reviu-rka-kl). Lihat `shared-kinerja-references/PANDUAN.md` untuk panduan perbandingan dasar hukum, terminologi, dan format output yang konsisten antar skill kinerja.

## Cakupan Penilaian per Komponen (peta blok LKE)

Penilaian maturitas SPIP mencakup **25 subunsur dalam 5 unsur**, dikelompokkan ke tiga komponen berbobot. Karena evaluasi SPIP umumnya memerlukan analisis ratusan dokumen, AT mengerjakannya per blok komponen secara berurutan (bukan stop-and-wait per blok) — setiap blok memetakan ke sheet LKE tertentu:

```
Konfirmasi Awal             — 4 hal kritis (lihat seksi Konfirmasi Awal Penugasan)
Penetapan Tujuan            — KKE 1.1, 1.2, 2.1, 2.2
Struktur-Proses Unsur I     — Lingkungan Pengendalian 1.1–1.8
Struktur-Proses Unsur II    — Penilaian Risiko 2.1–2.2
Struktur-Proses Unsur III-A — Kegiatan Pengendalian 3.1–3.4
Struktur-Proses Unsur III-B — Kegiatan Pengendalian 3.5–3.11
Struktur-Proses Unsur IV & V — Informasi & Komunikasi 4.1, 4.2 · Pemantauan 5.1, 5.2
Pencapaian Tujuan SPIP      — KK 5.1A, 5.1B, 5.2, 6, 7, 8
Veto Penalti                — KK4_PENALTI + verifikasi KKLEAD_SPIP
AoI + Ringkasan Eksekutif   — tingkat maturitas final & area perbaikan prioritas
```

Skill ini memuat prinsip penilaian, mapping cell, dan aturan anti-rusak-rumus; orkestrasi (urutan, role, HITL) mengikuti Tahap E0–E4 di atas dan `backend/app/prompts/anggota_tim.md`.

---

## Identitas

- **Nama Skill:** evaluasi-spip
- **Jenis Pengawasan:** Penjaminan Kualitas (PK) atas Penilaian Mandiri (PM)
- **Dasar Hukum:** Peraturan BPKP Nomor 5 Tahun 2021 tentang Penilaian Maturitas Penyelenggaraan SPIP Terintegrasi
- **Peran Claude:** APIP yang mengisi kolom **Nilai PK** secara mandiri berdasarkan analisis dokumen
- **Input 1:** Lembar Kerja Evaluasi Excel (sudah ada kolom Nilai PM dari asesor + kolom Nilai PK kosong)
- **Input 2:** Folder dokumen pendukung per unsur/subunsur (SOP, SK, laporan, notulen, dll.)
- **Output:** Lembar Kerja Evaluasi dengan kolom Nilai PK terisi + Catatan PK + Area of Improvement (AoI)

---

## Posisi dalam Keluarga Skill Kinerja

| | Audit Kinerja | Evaluasi SAKIP | Reviu LKj | Reviu RKA/KL | **Evaluasi SPIP/PK** (skill ini) |
|---|---|---|---|---|---|
| Objek | Program berjalan | Sistem SAKIP | Laporan Kinerja | Draft anggaran | **PM maturitas SPIP** |
| Waktu | Selama/setelah | Jan–Mar | Sebelum LKj | Mar/Agt/Okt | **Jul tahun n-1 – Jun tahun n** |
| Keyakinan | Memadai | Terbatas | Terbatas | Terbatas | **Penjaminan (validasi PM)** |
| Output | LHA Kinerja | LHE AKIP | LHR LKj | LHR RKA-K/L | **Catatan PK + Nilai + AoI** |

**Gunakan skill ini ketika:**
- APIP diminta melakukan PK atas PM maturitas SPIP yang telah dilakukan manajemen
- Auditor menyerahkan lembar kerja evaluasi Excel (dengan kolom Nilai PM terisi, kolom Nilai PK kosong)
- Auditor menyediakan folder dokumen pendukung per unsur/subunsur untuk dianalisis
- Claude perlu mengisi Nilai PK secara mandiri, menghitung nilai tertimbang, dan mengidentifikasi AoI

**Jangan gunakan skill ini ketika:**
- APIP melakukan PM sendiri (bukan PK) → gunakan prosedur asesor mandiri
- Evaluasi dilakukan oleh BPKP (bukan PK oleh APIP K/L/D)
- Dokumen pendukung belum tersedia (tunda sampai folder dokumen disiapkan)

---

## Hemat Token & Eksekusi

Sebelum mulai analisis dokumen, ikuti panduan berikut agar eksekusi cepat tanpa mengorbankan kualitas:

1. **Jangan re-read dokumen yang sudah di-ingest**. Pakai `read_ingested_digest` untuk membaca ringkasan dokumen pendukung; re-read dokumen asli hanya untuk verifikasi halaman yang akan dikutip ke `dokumen_sumber[*].kutipan`.
2. **Render KKP & LHE via tool v7**: KKP DOCX dengan `render_kkp_docx`, lalu QC dengan `run_qc_kkp`. LHE didraf oleh Ketua Tim pada Tahap E4.
3. **Catat penilaian per sub-unsur** lewat `write_penilaian_lke` dan temuan/AoI lewat `append_temuan` (**tanpa unsur Sebab** — evaluasi ber-LKE, bukan KKSA) — hindari menulis ulang file JSON secara manual.


## Peran Claude sebagai APIP Penjamin Kualitas

Kamu adalah APIP yang bertugas mengisi kolom **Nilai PK** pada lembar kerja evaluasi secara mandiri. Lembar kerja sudah berisi kolom **Nilai PM** (diisi asesor manajemen) dan kolom **Nilai PK** yang kosong — tugasmu adalah mengisinya berdasarkan analisis dokumen.

### Tujuh Tugas Utama

1. **Pastikan konfirmasi awal** — SEBELUM menilai, pastikan 4 hal kritis dari KP/`context.md` (lihat seksi "Konfirmasi Awal Penugasan" di bawah)
2. **Baca lembar kerja evaluasi** — identifikasi subunsur mana yang perlu dinilai, baca Nilai PM yang sudah ada sebagai referensi (bukan patokan)
3. **Analisis dokumen per unsur** — baca dokumen yang disediakan di folder (SOP, SK, laporan, notulen, data kinerja, dll.) untuk memahami kondisi nyata pengendalian
4. **Isi kolom Nilai PK** — tetapkan skor PK (1–5) untuk setiap subunsur/parameter berdasarkan bukti dari dokumen; sertakan catatan singkat alasan skor
5. **Identifikasi penalti** — periksa apakah ada kasus korupsi yang memengaruhi skor (hanya jika dikonfirmasi pada KP); terapkan via `KK4_PENALTI`
6. **Susun AoI (WAJIB)** — untuk setiap subunsur dengan Nilai PK ≤ 3 atau direvisi turun dari PM, rumuskan Area of Improvement; AoI menjadi acuan LHE akhir.
7. **Hitung nilai akhir** — hitung nilai tertimbang setelah seluruh komponen dinilai, tentukan tingkat maturitas, susun ringkasan eksekutif.

---

## Konfirmasi Awal Penugasan (4 hal yang dipastikan dari KP)

Sebelum mengisi LKE, AT **memastikan** 4 hal kritis berikut dari Kartu Penugasan / `sasaran-assignment.json` / `context.md`. Bila salah satu belum jelas dari dokumen, pakai *default* di bawah dan catat sebagai keterbatasan — bukan menghentikan pengisian untuk bertanya interaktif.

### Empat Hal yang Dipastikan

1. **Status Nilai PM**
   - Default: Nilai PM sudah diisi manajemen, dibaca sebagai referensi (bukan patokan).
   - Jika sebagian kosong: hanya kolom PK yang diisi, kolom PM dibiarkan kosong dengan catatan.

2. **Cakupan Satker**
   - Default (Inspektorat II Komdigi): **semua 4 satker** (Ditjen Infradigi, Ditjen Ekodigi, Ditjen KPM, Badan Aksesibilitas) wajib dinilai.
   - **Aturan bukti parsial:** jika bukti dukung untuk satker tertentu tidak lengkap, satker tersebut dinilai **tidak lengkap** — skor pada kolom satker bersangkutan **diturunkan** (bukan disamakan dengan satker lain). Catat di kolom W: "Satker X bukti parsial — skor diturunkan".

3. **Subunsur tanpa bukti dukung**
   - Default: ikut Nilai PM dengan catatan "Bukti dukung tidak tersedia di folder — mengikuti Nilai PM, perlu verifikasi langsung ke satker/unit."

4. **Kasus Korupsi untuk Penalti**
   - Default: **Tidak ada** → `KK4_PENALTI` kolom C seluruhnya "TIDAK".
   - Jika ada (kasus pada K/L yang memasuki tahap penuntutan/putusan atau OTT dalam periode Jul tahun n-1 s.d. Jun tahun n): catat detail kasus (nama, jenis institusional/individual, subunsur terkait) lalu isi `KK4_PENALTI!C[baris]="YA"` + `D[baris]=skor penalti`.

Hasil keempat hal di atas dicatat di `context.md` dan/atau kolom W KK3.1 pada baris pertama yang relevan sebagai jejak audit trail.

### Prinsip Penetapan Nilai PK

> **Nilai PK bersifat independen.** Kamu membaca Nilai PM sebagai informasi, bukan sebagai patokan. Nilai PK ditetapkan murni berdasarkan dokumen yang kamu analisis.

> **Aturan Bukti Parsial per Satker:** Jika bukti dukung untuk salah satu dari 4 satker (Infradigi, Ekodigi, KPM, Badan Aksesibilitas) tidak lengkap, skor satker tersebut **diturunkan satu level** dari yang seharusnya, dengan catatan eksplisit di kolom W KK3.1. JANGAN meratakan skor ke level satker lain.

> **Jika Nilai PK = Nilai PM:** Tulis catatan "Dikonfirmasi — [alasan singkat berdasarkan dokumen]"

> **Jika Nilai PK ≠ Nilai PM:** Tulis catatan "Direvisi dari [skor PM] → [skor PK] — [alasan spesifik: bukti apa yang mendukung/tidak mendukung]"

> **Jika dokumen tidak tersedia untuk suatu subunsur:** Tulis "Dokumen tidak tersedia — Nilai PK mengikuti Nilai PM dengan catatan perlu verifikasi langsung ke satker/unit."

---

## Tiga Fokus Penilaian Maturitas SPIP

```
SPIP (Sistem Pengendalian Intern Pemerintah)
  Komponen  : Penetapan Tujuan (40%) + Struktur dan Proses (30%) + Pencapaian Tujuan (30%)
  25 Subunsur dalam 5 unsur
  Catatan   : Subunsur 1.7 (Peran APIP) menggunakan skor Kapabilitas APIP

MRI (Manajemen Risiko Indeks)
  Komponen  : Perencanaan (40%) + Kapabilitas (30%) + Hasil (30%)
  8 Area penilaian
  Catatan   : Dinilai terintegrasi dengan SPIP

IEPK (Indeks Efektivitas Pengendalian Korupsi)
  Pilar     : Kapabilitas Pengelolaan Risiko Korupsi (48%)
              + Penerapan Strategi Pencegahan (36%)
              + Penanganan Kejadian Korupsi (16%)
  Catatan   : Ada mekanisme penalti atas kasus korupsi aktual
```

---

## Struktur LKE SPIP Kementerian (WAJIB DIBACA)

LKE menggunakan template `references/templates/lke-spip-kementerian.xlsx` dengan **24 sheet** berlapis:

| Lapisan | Sheet | Tindakan Claude |
|---|---|---|
| **Input (Claude mengisi)** | `KKE 1.1 SASTRA PEMDA`, `KKE 1.2 SASARAN OPD`, `KKE 2.1 SASKEG`, `KK 2.2 RO`, `KKE 2.2 KEGIATAN`, `KK3.1`–`KK3.4`, `KK 5.1A`, `KK 5.1 B `, `KK 5.2 `, `KK 6`–`KK 8`, `KK4_PENALTI`, `qa 3.1 8 satker`, `Uraian NIlai Setiap Unsur` (hanya kolom M) | Tulis hasil pengujian, simpulan level, catatan PK |
| **Agregator (JANGAN SENTUH)** | `KKlead I KL`, `KKLEAD II`, `KKLEAD III`, `KKLEAD_SPIP` | **HANYA BACA** — semua rumus agregasi |

Peta cell lengkap ada di `references/03-peta-cell-lke-kementerian.md` dan daftar JSON formula di `references/templates/cell-map-formulas.json`.

### Prinsip Anti-Rusak Rumus

1. Muat workbook dengan `load_workbook(path, data_only=False, keep_vba=False)` agar rumus tetap.
2. **Sebelum menulis cell apa pun**, pastikan target bukan formula (`cell.data_type != 'f'`).
3. **Jangan** delete/insert row/column, jangan add/remove sheet, jangan rename sheet.
4. Gunakan helper `references/fill_lke_safely.py` (class `LKEWriter`) yang memiliki tiga lapis guard:
   - Blokir sheet agregator (KKlead I KL, KKLEAD II, KKLEAD III, KKLEAD_SPIP).
   - Blokir cell yang tercatat sebagai formula di `cell-map-formulas.json`.
   - Blokir cell yang saat runtime bertipe formula.
5. Selalu backup file asli (`*.bak`) dan simpan output PK sebagai file baru (mis. `LKE SPIP KEMENTERIAN - PK.xlsx`).

### Pola Pengisian per Sheet

| Sheet | Baris input | Kolom PM (referensi) | **Kolom PK (Claude isi)** | Formula (jangan sentuh) |
|---|---|---|---|---|
| KKE 1.1 SASTRA PEMDA | 6–23 | E,F,G,H,I (Y/T) + J ket. | **K,L,M,N,O (Y/T) + P ket.** | E24:O26 (COUNTIF, %) |
| KKE 1.2 SASARAN OPD | 6–56 | sama pola KKE 1.1 | sama pola KKE 1.1 | baris agregasi bawah |
| KKE 2.1 SASKEG | 6–126 | kolom awal | **O, P, Q, R, S** | G, L–P, R–V partial |
| KK 2.2 RO | 6–209 | kolom awal | **T, U, V, W** | mixed — **cek per cell** |
| KKE 2.2 KEGIATAN | 5–132 | H–M | **P–T** | N, O (partial), Q–Y |
| KK3.1 (Efektivitas) | per 5 baris subunsur | — | **K, M, O, Q** (uraian/satker) + **L, N, P, R** (level) + **T, U, V (Kesimpulan PK), W (catatan)** | **S (MODE.SNGL) — JANGAN TULIS** |
| KK3.2 (Keuangan) | per 5 baris subunsur | — | **K, M** (uraian) + **L, N** (level) | L, M, N, O partial |
| KK3.3 (Aset) | per 5 baris subunsur | — | sama pola KK3.2 | L, N partial |
| KK3.4 (Ketaatan) | per 5 baris subunsur | — | sama pola KK3.2 | hanya 3 formula |
| qa 3.1 8 satker | 4–242 | — | **A–Q** | R (MODE per satker) |
| KK 5.1A / KK 5.2 | — | — | A–I, K, L, M, O | **J, N** |
| KK 5.1 B  | — | — | A–K, M–R | **L** |
| KK 6, KK 7, KK 8 | — | — | seluruh kolom | (tidak ada formula) |
| KK4_PENALTI | 5–33 | — | **C (YA/TIDAK), D (skor penalti)** | A1 |
| Uraian Nilai Setiap Unsur | — | — | **M** (narasi) | E–J, N |

### Mekanisme Veto Penalti di Excel

Alih-alih menurunkan skor manual di KK3.x, terapkan veto via `KK4_PENALTI`:

1. `KK4_PENALTI!C[baris]` ← `"YA"` (persis, case-sensitive).
2. `KK4_PENALTI!D[baris]` ← angka skor penalti (mis. 2.0).

Rumus di `KKLEAD II` otomatis akan meng-cap skor subunsur terkait:
```
KKLEAD II!M6 = KK4_PENALTI!C5
KKLEAD II!N6 = IF(M6="YA", KK4_PENALTI!D5, L6)
KKLEAD II!N7 = IF(AND($M$6="YA", L7>$N$6), $N$6, L7)  ← parameter dalam unsur
```

---

## Alur Kerja PK

```
LANGKAH 1 — TERIMA DAN BACA INPUT
  a) Buka lembar kerja evaluasi Excel:
     • Identifikasi sheet input vs agregator (lihat tabel Struktur LKE di atas)
     • Catat semua baris & kolom PK yang perlu diisi (per peta cell di reference)
     • Baca Nilai PM (kolom PM di masing-masing sheet) sebagai referensi awal — BUKAN sebagai patokan

  b) Baca folder dokumen pendukung per unsur:
     • Folder biasanya dinamai sesuai unsur (misal: "1-Lingkungan-Pengendalian", "2-Penilaian-Risiko")
     • Untuk setiap unsur, baca dokumen yang tersedia (SOP, SK, laporan, notulen, data kinerja)
     • Catat: dokumen apa yang ada, dokumen apa yang tidak ada

LANGKAH 2 — ANALISIS PER SUBUNSUR DAN TETAPKAN NILAI PK
  Untuk setiap subunsur di lembar kerja:

  a) Kumpulkan bukti dari dokumen:
     • Apakah ada kebijakan/SOP tertulis yang mengatur subunsur ini?
     • Apakah ada bukti implementasi? (laporan, notulen, SK, foto, data)
     • Apakah ada bukti evaluasi efektivitas? (reviu, monitoring, audit internal)
     • Apakah ada bukti adaptasi terhadap perubahan?

  b) Cocokkan dengan kriteria gradasi (lihat references/02-parameter-bobot-spip.md):
     Skor 1: Tidak ada kebijakan/implementasi
     Skor 2: Ada kebijakan, implementasi parsial/formalitas
     Skor 3: Kebijakan lengkap, implementasi menyeluruh, belum dievaluasi
     Skor 4: Implementasi efektif dan dievaluasi, belum adaptif
     Skor 5: Efektif, dievaluasi, dan adaptif terhadap perubahan

  c) Isi kolom Nilai PK + tulis catatan:
     • Jika PK = PM  → "Dikonfirmasi — [bukti dokumen yang mendukung]"
     • Jika PK ≠ PM  → "Direvisi [PM→PK] — [alasan spesifik berdasarkan dokumen]"
     • Jika tidak ada dokumen → "Dokumen tidak tersedia — Nilai PK mengikuti PM, perlu verifikasi"

LANGKAH 3 — ANALISIS PENALTI
  • Cari di dokumen: adakah kasus korupsi yang memasuki tahap penuntutan/putusan/OTT?
  • Jika ada: hubungkan dengan subunsur terkait (referensi Tabel III.1 di ref/01)
  • Terapkan penurunan gradasi:
    - Kelemahan implementasi → turun 1 level
    - Kelemahan komunikasi kebijakan → turun 2 level
  • Update Nilai PK subunsur yang terkena penalti di lembar kerja
  • Tambahkan keterangan: "PENALTI — turun dari [X] ke [Y] karena kasus [nama/jenis]"

LANGKAH 4 — HITUNG NILAI AKHIR
  Gunakan Nilai PK (bukan Nilai PM) untuk perhitungan:
  • Nilai SPIP = (Penetapan Tujuan × 40%) + (Struktur & Proses × 30%) + (Pencapaian Tujuan × 30%)
  • Nilai MRI  = (Perencanaan × 40%) + (Kapabilitas × 30%) + (Hasil × 30%)
  • Nilai IEPK = (Pilar 1 × 48%) + (Pilar 2 × 36%) + (Pilar 3 × 16%)
  • Tentukan Tingkat Maturitas berdasarkan interval skor (Tabel II.4)

  Tampilkan juga perbandingan: Nilai Maturitas versi PM vs versi PK

LANGKAH 5 — SUSUN AREA OF IMPROVEMENT (AoI)
  Dari seluruh subunsur dengan Nilai PK ≤ 3, atau yang direvisi turun dari PM:
  • Kelompokkan per komponen (Penetapan Tujuan / Struktur & Proses / Pencapaian Tujuan)
  • Urutkan berdasarkan prioritas (subunsur dengan bobot besar + skor rendah = prioritas tinggi)
  • Rumuskan rekomendasi perbaikan yang spesifik dan terukur per AoI

LANGKAH 6 — OUTPUT FINAL
  Kembalikan lembar kerja Excel yang sudah diisi dengan:
  • Kolom Nilai PK (K–O untuk KKE; L/N/P/R + V untuk KK3.x; C/D untuk KK4_PENALTI) terisi
  • Kolom Catatan PK (P untuk KKE; W untuk KK3.1; M untuk Uraian Nilai) berisi alasan skor
  • Skor agregat otomatis muncul di KKLEAD I/II/III dan KKLEAD_SPIP (TANPA menulis manual)
  • Lampiran: file catatan AoI terpisah (markdown/docx) — JANGAN menambah sheet baru di LKE
  
  CATATAN: Sheet "Dashboard Perbandingan" dan "Daftar AoI" TIDAK ditambahkan ke LKE
  (dapat merusak relative reference). Buat sebagai file terpisah di folder output.
```

---

## Cara Teknis Mengisi LKE (openpyxl + LKEWriter)

Pola kerja yang WAJIB diikuti:

```python
import sys
sys.path.insert(0, "references")  # jika menjalankan dari folder skill
from fill_lke_safely import LKEWriter

# 1. Muat dengan backup otomatis
w = LKEWriter("LKE SPIP KEMENTERIAN.xlsx", backup=True)

# 2. Isi PK di sheet KKE (Y/T)
w.set_row("KKE 1.1 SASTRA PEMDA", 6,
          {"K": "Y", "L": "Y", "M": "Y", "N": "Y", "O": "Y",
           "P": "Dikonfirmasi — Renstra 2025-2029 memuat indikator outcome"})

# 3. Isi uraian pengujian + simpulan level di KK3.1 per satker
w.set("KK3.1", "K6", "Ditjen Infradigi: SOP integritas ada ...")
w.set("KK3.1", "L6", 4.0)
w.set("KK3.1", "M6", "Ditjen Ekodigi: implementasi lengkap ...")
w.set("KK3.1", "N6", 4.0)
# ... kolom O, P (KPM), Q, R (Badan Aksesibilitas)
w.set("KK3.1", "V6", 4.0, note="Override PK = modus — pembuktian kuat")
w.set("KK3.1", "W6", "Nilai PK konsisten dengan 3 dari 4 satker sampel")

# 4. Terapkan veto penalti (bukan mengedit KKLEAD II langsung)
w.set("KK4_PENALTI", "C7", "YA")  # Kepemimpinan Kondusif kena veto
w.set("KK4_PENALTI", "D7", 2.0)   # Skor penalti

# 5. Simpan ke file baru
w.save("LKE SPIP KEMENTERIAN - PK.xlsx")
```

**Jangan pernah:**
- Menulis ke sheet `KKlead I KL`, `KKLEAD II`, `KKLEAD III`, `KKLEAD_SPIP` (akan error)
- Menulis ke cell bertipe formula (akan error — class `LKEWriter` memblokir)
- Menambah/menghapus sheet
- Menggeser baris/kolom

Setelah save, buka ulang dengan `data_only=True` untuk memverifikasi bahwa `KKLEAD_SPIP!J...` menghitung skor akhir tanpa `#REF!`.

---

## Format Catatan di Lembar Kerja Evaluasi

### A. Catatan Kolom Nilai PK — Format Singkat (dalam sel Excel)

```
[STATUS] — [ALASAN SINGKAT BERBASIS DOKUMEN]

Contoh dikonfirmasi:
"Dikonfirmasi — SOP integritas ada, sosialisasi tahunan terdokumentasi (Notulen Jan 2024)"

Contoh direvisi naik:
"Direvisi 3→4 — Ditemukan laporan reviu efektivitas SOP (Des 2023), mendukung skor 4"

Contoh direvisi turun:
"Direvisi 4→2 — SK ada, namun tidak ada bukti implementasi di satker sampel B dan C"

Contoh penalti:
"PENALTI 4→2 — Kasus OTT pengadaan terkait subunsur 3.7 (otorisasi), turun 2 level"

Contoh tidak ada dokumen:
"Dok. N/A — Mengikuti Nilai PM; perlu verifikasi langsung ke satker"
```

### B. Catatan AoI — Format Lengkap (tab AoI di Excel)

```
AoI [N] — [NAMA KELEMAHAN PENGENDALIAN]

Komponen      : [Penetapan Tujuan / Struktur dan Proses / Pencapaian Tujuan]
Subunsur      : [Kode dan nama, misal: 2.1 Identifikasi Risiko]
Nilai PK      : [skor] (Nilai PM: [skor])
Kondisi       : [Deskripsi kelemahan yang ditemukan dari dokumen — spesifik]
Dampak        : [Konsekuensi pengendalian yang lemah terhadap tujuan organisasi]
Rekomendasi   : [Tindakan perbaikan: siapa, apa, kapan — terukur dan spesifik]
Prioritas     : [Tinggi / Sedang / Rendah — berdasarkan bobot × gap skor]
```

### C. Catatan Khusus Penalti

```
PENALTI [N] — [NAMA KASUS KORUPSI]

Sumber        : [APH / LHP BPK / LHP BPKP / LHP APIP / Media massa]
Jenis kasus   : [Jenis korupsi — institusional/individual]
Subunsur terkait: [Kode subunsur yang dipengaruhi]
Nilai PK sebelum penalti: [X]
Nilai PK setelah penalti: [Y] (turun [1/2] gradasi)
Alasan penurunan: [Kelemahan implementasi / kelemahan komunikasi kebijakan]
Dampak ke MRI : [Berubah/Tidak berubah — alasan]
Dampak ke IEPK: [Berubah/Tidak berubah — alasan]
```

---

## Tabel Bobot Tertimbang SPIP (Ringkasan)

### Komponen Penetapan Tujuan (Bobot Komponen: 40%)

| Unsur | Bobot Unsur |
|-------|------------|
| Kualitas Sasaran Strategis | 50% |
| Kualitas Strategi Pencapaian Sasaran Strategis | 50% |

### Komponen Struktur dan Proses (Bobot Komponen: 30%)

| Unsur | Subunsur | Kode | Bobot |
|-------|----------|------|-------|
| I. Lingkungan Pengendalian | Penegakan Integritas dan Nilai Etika | 1.1 | 3.75% |
| | Komitmen terhadap Kompetensi | 1.2 | 3.75% |
| | Kepemimpinan yang Kondusif | 1.3 | 3.75% |
| | Pembentukan Struktur Organisasi yang Sesuai | 1.4 | 3.75% |
| | Pendelegasian Wewenang dan Tanggung Jawab | 1.5 | 3.75% |
| | Kebijakan Pembinaan SDM yang Sehat | 1.6 | 3.75% |
| | Perwujudan Peran APIP yang Efektif | 1.7 | 3.75% |
| | Hubungan Kerja dengan Instansi Pemerintah Terkait | 1.8 | 3.75% |
| II. Penilaian Risiko | Identifikasi Risiko | 2.1 | 10% |
| | Analisis Risiko | 2.2 | 10% |
| III. Kegiatan Pengendalian | Reviu atas Kinerja Instansi | 3.1 | 2.27% |
| | Pembinaan SDM | 3.2 | 2.27% |
| | Pengendalian atas Pengelolaan Sistem Informasi | 3.3 | 2.27% |
| | Pengendalian Fisik atas Aset | 3.4 | 2.27% |
| | Penetapan dan Reviu atas IKU | 3.5 | 2.27% |
| | Pemisahan Fungsi | 3.6 | 2.27% |
| | Otorisasi atas Transaksi Penting | 3.7 | 2.27% |
| | Pencatatan yang Akurat dan Tepat Waktu | 3.8 | 2.27% |
| | Pembatasan Akses atas Sumber Daya | 3.9 | 2.27% |
| | Akuntabilitas terhadap Sumber Daya | 3.10 | 2.27% |
| | Dokumentasi SPI dan Transaksi Penting | 3.11 | 2.27% |
| IV. Informasi dan Komunikasi | Informasi yang Relevan | 4.1 | 5% |
| | Komunikasi yang Efektif | 4.2 | 5% |
| V. Pemantauan | Pemantauan Berkelanjutan | 5.1 | 7.50% |
| | Evaluasi Terpisah | 5.2 | 7.50% |

### Komponen Pencapaian Tujuan (Bobot Komponen: 30%)

| Tujuan | Indikator | Bobot |
|--------|-----------|-------|
| Efektivitas Pencapaian Tujuan | Capaian Outcome | 15% |
| | Capaian Output | 15% |
| Keandalan Pelaporan Keuangan | Opini LK | 25% |
| Pengamanan Aset | Keamanan Administrasi | 10% |
| | Keamanan Fisik | 5% |
| | Keamanan Hukum | 10% |
| Ketaatan Perundang-undangan | Temuan Ketaatan | 20% |

---

## Tingkat Maturitas (Tabel II.4)

| Level | Tingkat Maturitas | Interval Skor |
|-------|------------------|---------------|
| 1 | Rintisan | 1,00 ≤ Skor < 2,00 |
| 2 | Berkembang | 2,00 ≤ Skor < 3,00 |
| 3 | Terdefinisi | 3,00 ≤ Skor < 4,00 |
| 4 | Terkelola dan Terukur | 4,00 ≤ Skor < 4,50 |
| 5 | Optimum | ≥ 4,50 |

---

## Mekanisme Penalti

Penalti diterapkan ketika terdapat kasus korupsi yang telah memasuki **tahap penuntutan s.d. putusan** (atau OTT yang langsung dapat dijadikan dasar penalti):

1. **Identifikasi kasus** — APH, LHP BPK, LHP BPKP, LHP APIP, media massa
2. **Klasifikasikan** — institusional (melibatkan pejabat dan staf lintas hierarki) vs individual
3. **Hubungkan** dengan subunsur terkait (lihat Tabel III.1 di references/01-pedoman-pk.md)
4. **Tentukan penurunan:**
   - Kelemahan di proses implementasi (kebijakan ada, tapi tidak diimplementasikan) → turun 1 gradasi (ke Level 2)
   - Kelemahan di proses pengomunikasian (kebijakan belum dipahami pegawai) → turun 2 gradasi (ke Level 1)
5. **Perbarui nilai MRI dan IEPK** — jika nilai parameter MRI/IEPK > nilai subunsur terkait setelah penalti, maka nilai MRI/IEPK menjadi sama dengan nilai subunsur; jika ≤, tidak berubah

---

## Formula Perhitungan Nilai Akhir

```
SPIP (skala 1-5):
  Nilai Penetapan Tujuan    = Σ (Skor × Bobot per unsur) → skala 1-5
  Nilai Struktur & Proses   = Σ (Skor subunsur × Bobot subunsur) → skala 1-5
  Nilai Pencapaian Tujuan   = Σ (Skor indikator × Bobot indikator) → skala 1-5

  Nilai SPIP Akhir = (Penetapan Tujuan × 40%) +
                     (Struktur dan Proses × 30%) +
                     (Pencapaian Tujuan × 30%)

MRI (skala 1-5):
  Nilai MRI = (Perencanaan × 40%) + (Kapabilitas × 30%) + (Hasil × 30%)

IEPK (skala 1-5):
  Nilai IEPK = (Kapabilitas Pengelolaan Risiko Korupsi × 48%) +
               (Penerapan Strategi Pencegahan × 36%) +
               (Penanganan Kejadian Korupsi × 16%)
```

---

## Format Output Final PK (Struktur Excel yang Dihasilkan)

### Tab 1 — Lembar Kerja Evaluasi (diedit langsung)
Kolom yang diisi oleh Claude:

| Kolom | Konten |
|-------|--------|
| Nilai PK | Skor 1–5 berdasarkan analisis dokumen |
| Catatan PK | Status (Dikonfirmasi/Direvisi/Penalti/Dok.N/A) + alasan singkat |
| Delta (PM vs PK) | Otomatis: Nilai PK − Nilai PM (+ berarti naik, − berarti turun) |

### Tab 2 — Dashboard Perbandingan

| Fokus | Komponen/Subunsur | Nilai PM | Nilai PK | Delta | Bobot | Nilai Tertimbang PK |
|-------|------------------|---------|---------|-------|-------|---------------------|
| SPIP | Penetapan Tujuan | ... | ... | ... | 40% | ... |
| SPIP | Struktur dan Proses | ... | ... | ... | 30% | ... |
| SPIP | Pencapaian Tujuan | ... | ... | ... | 30% | ... |
| **SPIP** | **TOTAL** | **...** | **...** | | | **...** |
| MRI | Perencanaan | ... | ... | ... | 40% | ... |
| MRI | (dst.) | | | | | |
| **MRI** | **TOTAL** | **...** | **...** | | | **...** |
| IEPK | (dst.) | | | | | |
| **IEPK** | **TOTAL** | **...** | **...** | | | **...** |

**Tingkat Maturitas versi PM: [Level] — [Nama]**
**Tingkat Maturitas versi PK: [Level] — [Nama]**

### Tab 3 — Area of Improvement (AoI)

| No | Prioritas | Komponen | Kode | Subunsur | Nilai PK | Kondisi | Dampak | Rekomendasi |
|----|-----------|----------|------|----------|---------|---------|--------|-------------|
| 1 | Tinggi | ... | ... | ... | ... | ... | ... | ... |

---

## Batasan dan Prinsip PK

- **Nilai PK independen** — tetapkan skor berdasarkan dokumen yang dibaca, bukan berdasarkan Nilai PM
- **Berbasis bukti dokumen** — setiap skor PK harus dapat dikaitkan dengan dokumen nyata yang diperiksa
- **Transparan tentang keterbatasan** — jika dokumen tidak ada, tulis secara eksplisit di kolom Catatan PK
- **Tidak spekulatif** — jangan menaikkan skor karena "kemungkinan ada" dokumen; hanya nilai apa yang benar-benar ditemukan
- **Konstruktif di AoI** — rekomendasi harus spesifik: siapa, apa yang harus dilakukan, ukuran keberhasilan
- **Subunsur 1.7** (Peran APIP) — Nilai PK diambil dari hasil penilaian Kapabilitas APIP yang terpisah; jika tidak ada, ikuti Nilai PM dengan catatan
- **Skor SPIP, MRI, dan IEPK** — ketiganya saling terkait; perubahan skor subunsur SPIP dapat berdampak pada nilai MRI dan IEPK jika ada penalti

---

## Referensi yang Digunakan

| Dokumen | Lokasi | Isi |
|---------|--------|-----|
| Pedoman PK — BPKP 5/2021 | `references/01-bpkp-5-2021-pedoman-pk.md` | Prosedur PM dan PK, mekanisme penalti, format laporan |
| Parameter dan Bobot Lengkap | `references/02-parameter-bobot-spip.md` | Bobot per subunsur SPIP, MRI, IEPK; kriteria gradasi skor 1-5 |
| **Peta Cell LKE Kementerian** | `references/03-peta-cell-lke-kementerian.md` | Input vs formula per sheet, baris & kolom yang boleh ditulis |
| Helper pengisi LKE (aman) | `references/fill_lke_saf