---
name: evaluasi-spip
jenis: Penjaminan Kualitas Penilaian Maturitas Penyelenggaraan SPIP Terintegrasi
format_laporan: lke
dasar-hukum: Peraturan BPKP Nomor 5 Tahun 2021
tingkat-keyakinan: penjaminan
template: references/templates/lke-spip-kementerian.xlsx
version: "1.8"
changelog:
  - v1.8 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel. Frontmatter `model`/`auto_execute`/`output` dihapus; seksi "Eksekusi di v7" & tabel "Tahap E0–E4" dibuang (substansi penilaian tetap di bawah). **Doktrin TANPA unsur Sebab** + pointer references P3 (`02`/`03`/`fill_lke_safely.py`) dipertahankan utuh.
  - v1.7: doktrin evaluasi ber-LKE TANPA unsur Sebab + AoI; perampingan ke references/02, references/03, fill_lke_safely.py.
---

# Skill: Evaluasi SPIP — Penjaminan Kualitas (PK) oleh APIP

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **format** keluarannya.
>
> **Doktrin penilaian: evaluasi ber-LKE, TANPA unsur Sebab.** Penilaian = **Nilai PK** (skor maturitas LKE per unsur/sub-unsur) + **AoI**, BUKAN KKSA. **Jangan menambah unsur Sebab** (rezim seperti Eval RB — lihat `panduan-format-umum/PANDUAN.md`). AoI **wajib** untuk setiap subunsur dengan Nilai PK ≤ 3 atau direvisi turun dari PM.

## Peran Claude sebagai APIP Penjamin Kualitas

Kamu adalah APIP yang mengisi kolom **Nilai PK** pada LKE secara mandiri berdasarkan analisis dokumen. Lembar kerja sudah berisi kolom **Nilai PM** (asesor manajemen) + kolom **Nilai PK** kosong. Objek = **PM maturitas SPIP**; keyakinan = **Penjaminan (validasi PM)**; periode = **Jul tahun n-1 – Jun tahun n**; output = **Catatan PK + Nilai + AoI**.

### Tujuh Tugas Utama

1. **Pastikan konfirmasi awal** — SEBELUM menilai, pastikan 4 hal kritis dari KP/`context.md` (lihat "Konfirmasi Awal Penugasan").
2. **Baca LKE** — identifikasi subunsur yang perlu dinilai; baca Nilai PM sebagai referensi (bukan patokan).
3. **Analisis dokumen per unsur** — SOP, SK, laporan, notulen, data kinerja untuk memahami kondisi nyata pengendalian (baca cuplikan bukti yang relevan, bukan seluruh PDF).
4. **Isi kolom Nilai PK (1–5)** per subunsur/parameter berdasarkan bukti + catatan singkat alasan skor.
5. **Identifikasi penalti** — kasus korupsi yang memengaruhi skor (hanya jika dikonfirmasi pada KP); terapkan via veto `KK4_PENALTI`.
6. **Susun AoI (WAJIB)** — untuk setiap subunsur dengan Nilai PK ≤ 3 atau direvisi turun dari PM. AoI menjadi acuan LHE. **Catatan/AoI TANPA unsur Sebab** (isi Kondisi/Kriteria/Dampak/Rekomendasi + sumber).
7. **Hitung nilai akhir** — nilai tertimbang setelah seluruh komponen dinilai, tentukan tingkat maturitas, susun ringkasan eksekutif.

> Hemat token: catat penilaian per cell LKE dan rekap skor; catat catatan/AoI **tanpa unsur Sebab** — hindari menulis ulang JSON/Excel manual. Jangan re-read dokumen yang sudah di-ingest.

## Posisi dalam Keluarga Skill Kinerja

Termasuk dalam keluarga skill kinerja (audit-kinerja, evaluasi-sakip, evaluasi-spip, reviu-rka-kl). Karakter pembeda skill ini: objek = **PM maturitas SPIP**; keyakinan = **Penjaminan (validasi PM)**; periode = **Jul tahun n-1 – Jun tahun n**; output = **Catatan PK + Nilai + AoI**. Perbandingan lengkap dasar hukum/terminologi/format antar skill kinerja: `shared-kinerja-references/PANDUAN.md`.

**Gunakan skill ini ketika:** APIP melakukan PK atas PM maturitas SPIP yang telah dilakukan manajemen; auditor menyerahkan LKE Excel (kolom Nilai PM terisi, Nilai PK kosong) + folder dokumen pendukung per unsur untuk dianalisis.

**Jangan gunakan ketika:** APIP melakukan PM sendiri (bukan PK); evaluasi oleh BPKP (bukan PK oleh APIP K/L/D); dokumen pendukung belum tersedia (tunda).

## Konfirmasi Awal Penugasan (4 hal yang dipastikan dari KP)

Sebelum mengisi LKE, pastikan 4 hal kritis dari Kartu Penugasan / `sasaran-assignment.json` / `context.md`. Bila salah satu belum jelas, pakai *default* di bawah dan catat sebagai keterbatasan — bukan menghentikan pengisian untuk bertanya interaktif.

1. **Status Nilai PM** — Default: PM sudah diisi manajemen, dibaca sebagai referensi (bukan patokan). Jika sebagian kosong: hanya kolom PK diisi, kolom PM dibiarkan kosong dengan catatan.
2. **Cakupan Satker** — Default (Inspektorat II Komdigi): **semua 4 satker** (Ditjen Infradigi, Ditjen Ekodigi, Ditjen KPM, Badan Aksesibilitas) wajib dinilai. **Aturan bukti parsial:** jika bukti satker tertentu tidak lengkap, satker tersebut dinilai **tidak lengkap** — skor pada kolom satker bersangkutan **diturunkan** (bukan disamakan dengan satker lain). Catat di kolom W: "Satker X bukti parsial — skor diturunkan".
3. **Subunsur tanpa bukti dukung** — Default: ikut Nilai PM dengan catatan "Bukti dukung tidak tersedia di folder — mengikuti Nilai PM, perlu verifikasi langsung ke satker/unit."
4. **Kasus Korupsi untuk Penalti** — Default: **Tidak ada** → `KK4_PENALTI` kolom C seluruhnya "TIDAK". Jika ada (kasus pada K/L yang memasuki tahap penuntutan/putusan atau OTT dalam periode Jul tahun n-1 s.d. Jun tahun n): catat detail (nama, jenis institusional/individual, subunsur terkait) lalu isi `KK4_PENALTI!C[baris]="YA"` + `D[baris]=skor penalti`.

Hasil keempat hal dicatat di `context.md` dan/atau kolom W KK3.1 baris pertama relevan sebagai jejak audit trail.

### Prinsip Penetapan Nilai PK

> **Nilai PK bersifat independen.** Nilai PM dibaca sebagai informasi, bukan patokan. Nilai PK ditetapkan murni berdasarkan dokumen yang dianalisis.

> **Bukti parsial per satker:** jika bukti satu dari 4 satker tidak lengkap, skor satker itu **diturunkan satu level**, dengan catatan eksplisit di kolom W KK3.1. JANGAN meratakan skor ke satker lain.

Format catatan singkat di kolom Nilai PK (status — alasan berbasis dokumen):
- **PK = PM** → "Dikonfirmasi — [alasan singkat berdasarkan dokumen]"
- **PK ≠ PM** → "Direvisi [skor PM] → [skor PK] — [bukti yang mendukung/tidak mendukung]"
- **Dok. N/A** → "Dokumen tidak tersedia — Nilai PK mengikuti PM; perlu verifikasi langsung ke satker/unit."
- **Penalti** → "PENALTI [X]→[Y] — Kasus [nama/jenis] terkait subunsur [kode], turun [1/2] level."

## Tiga Fokus Penilaian Maturitas SPIP

```
SPIP : Penetapan Tujuan (40%) + Struktur dan Proses (30%) + Pencapaian Tujuan (30%)
       25 subunsur dalam 5 unsur. Subunsur 1.7 (Peran APIP) memakai skor Kapabilitas APIP.
MRI  : Perencanaan (40%) + Kapabilitas (30%) + Hasil (30%) — terintegrasi dengan SPIP.
IEPK : Kapabilitas Pengelolaan Risiko Korupsi (48%) + Strategi Pencegahan (36%)
       + Penanganan Kejadian Korupsi (16%) — ada mekanisme penalti atas kasus korupsi aktual.
```

> **Detail bobot per sub-unsur/area/pilar (SPIP, MRI, IEPK), kriteria validasi skor 1–5 per skor, kriteria skor Pencapaian Tujuan (opini LK/capaian/ketaatan/aset), red flag validasi, dan formulir kalkulasi nilai akhir: baca `references/02-parameter-bobot-spip.md`.**

## Cakupan Penilaian per Komponen (peta blok LKE)

Penilaian mencakup **25 subunsur dalam 5 unsur**, dikelompokkan ke tiga komponen berbobot:

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

## Struktur LKE & Pengisian (peta cell)

LKE memakai template `references/templates/lke-spip-kementerian.xlsx` (**24 sheet** berlapis): **sheet input** yang diisi APIP (KKE 1.x/2.x, KK3.1–3.4, KK 5.x, KK 6–8, KK4_PENALTI, qa 3.1 8 satker, kolom M `Uraian NIlai Setiap Unsur`) vs **sheet agregator** yang **HANYA BACA** (`KKlead I KL`, `KKLEAD II`, `KKLEAD III`, `KKLEAD_SPIP`).

> **Peta cell lengkap per sheet (baris input, kolom PM vs PK, kolom formula yang dilarang), mapping sheet ↔ bagian penilaian, dan aturan penulisan: baca `references/03-peta-cell-lke-kementerian.md`. Daftar pasti semua cell formula: `references/templates/cell-map-formulas.json`.**

### Prinsip Anti-Rusak Rumus (dijamin tool `fill_lke` — konteks, bukan langkah manual agen)

1. Muat workbook dengan `load_workbook(path, data_only=False, keep_vba=False)` agar rumus tetap.
2. **Sebelum menulis cell apa pun**, pastikan target bukan formula (`cell.data_type != 'f'`).
3. **Jangan** delete/insert row/column, jangan add/remove/rename sheet, jangan geser baris/kolom.
4. Selalu backup file asli (`*.bak`) dan tulis hasil PK sebagai **salinan kerja `_KKP/LKE-terisi-evaluasi-spip.xlsx`** (file asli/template tidak diubah).
5. Setelah save, buka ulang dengan `data_only=True` untuk verifikasi `KKLEAD_SPIP!J...` menghitung skor akhir tanpa `#REF!`.

### Cara mengisi LKE — tool `fill_lke` (bukan Excel/Python mentah)

Pengisian kolom PK/APIP dilakukan lewat **tool `fill_lke(penugasan_folder, skill="evaluasi-spip", entries=[...])`** — bukan menulis openpyxl/Python langsung. Tool memakai template SPIP (`references/templates/lke-spip-kementerian.xlsx`) dan menerapkan **tiga lapis guard anti-rumus** secara internal (implementasi `references/fill_lke_safely.py` / `LKEWriter`): blokir sheet agregator (`KKLEAD_*`), blokir cell formula (dari `cell-map-formulas.json`), blokir cell bertipe formula saat runtime; plus backup otomatis. **Output = salinan kerja `_KKP/LKE-terisi-evaluasi-spip.xlsx`** (file asli/template tak diubah); cell yang ditolak dilaporkan di field `refused`.

`entries` = daftar `{sheet, coord, value, note?}` — mis. isi kolom PK per subunsur, override skor di `KK3.x`, veto penalti di `KK4_PENALTI` (`C[baris]="YA"` + `D[baris]=`skor). Baca nilai LKE terkini via tool **`read_lke`**.

> **Gate deliverable:** `_KKP/LKE-terisi-evaluasi-spip.xlsx` WAJIB ada sebelum render KKP/LHE — render menolak bila LKE belum diisi via `fill_lke`. Kontrak `entries` & guard lengkap: docstring `references/fill_lke_safely.py` (implementasi yang dibungkus tool).

### Veto Penalti di Excel (ringkas)

Jangan menurunkan skor manual di KK3.x. Terapkan veto via `KK4_PENALTI`: tulis `C[baris]="YA"` (persis, case-sensitive) + `D[baris]=` skor penalti. Rumus di `KKLEAD II` (M/N) otomatis meng-cap skor subunsur terkait.

> Detail formula cap (`KKLEAD II!N6=IF(M6="YA",...)`, `N7=IF(AND($M$6="YA",...))`) dan pemetaan baris: `references/03-peta-cell-lke-kementerian.md` seksi "Veto Penalti".

## Alur Penilaian PK (fill_lke — konseptual)

```
LANGKAH 1 — TERIMA & BACA INPUT
  a) Buka LKE: identifikasi sheet input vs agregator; catat baris/kolom PK yang perlu diisi
     (per peta cell di references/03); baca Nilai PM sebagai referensi awal (BUKAN patokan).
  b) Baca folder dokumen pendukung per unsur (SOP, SK, laporan, notulen, data kinerja);
     catat dokumen yang ada vs tidak ada.

LANGKAH 2 — ANALISIS PER SUBUNSUR & TETAPKAN NILAI PK
  a) Kumpulkan bukti: ada kebijakan/SOP tertulis? bukti implementasi? bukti evaluasi
     efektivitas? bukti adaptasi terhadap perubahan?
  b) Cocokkan dengan kriteria gradasi (references/02 seksi D):
     1 Tidak ada kebijakan/implementasi · 2 Kebijakan ada, implementasi parsial/formalitas
     · 3 Kebijakan lengkap, implementasi menyeluruh, belum dievaluasi
     · 4 Implementasi efektif & dievaluasi, belum adaptif · 5 Efektif, dievaluasi, adaptif.
  c) Isi kolom Nilai PK + catatan (format: Dikonfirmasi / Direvisi / Dok. N/A — lihat atas).

LANGKAH 3 — ANALISIS PENALTI
  • Cari kasus korupsi tahap penuntutan/putusan/OTT → hubungkan ke subunsur (Tabel III.1, ref/01).
  • Penurunan: kelemahan implementasi → turun 1 level; kelemahan komunikasi kebijakan → turun 2.
  • Terapkan via KK4_PENALTI (bukan edit KKLEAD II); keterangan "PENALTI — turun [X]→[Y] karena ...".

LANGKAH 4 — HITUNG NILAI AKHIR (pakai Nilai PK, bukan PM)
  • Nilai SPIP = (Penetapan Tujuan ×40%) + (Struktur & Proses ×30%) + (Pencapaian Tujuan ×30%)
  • Nilai MRI  = (Perencanaan ×40%) + (Kapabilitas ×30%) + (Hasil ×30%)
  • Nilai IEPK = (Pilar 1 ×48%) + (Pilar 2 ×36%) + (Pilar 3 ×16%)
  • Tentukan Tingkat Maturitas (Tabel II.4 di bawah). Tampilkan perbandingan PM vs PK.
  (Rincian formula & formulir kalkulasi: references/02 seksi G.)

LANGKAH 5 — SUSUN AREA OF IMPROVEMENT (AoI)
  Dari subunsur dengan Nilai PK ≤ 3 atau direvisi turun: kelompokkan per komponen, urutkan
  prioritas (bobot besar + skor rendah = prioritas tinggi), rumuskan rekomendasi spesifik & terukur.
  Catatan/AoI TANPA unsur Sebab (isi Kondisi/Kriteria/Dampak/Rekomendasi + sumber).

LANGKAH 6 — OUTPUT FINAL
  • Kolom Nilai PK + Catatan PK terisi; skor agregat muncul otomatis di KKLEAD I/II/III & KKLEAD_SPIP.
  • Lampiran AoI sebagai file terpisah (markdown/docx). JANGAN menambah sheet baru di LKE
    ("Dashboard"/"Daftar AoI" dapat merusak relative reference).
```

## Format Catatan AoI (file terpisah, bukan sheet baru)

```
AoI [N] — [NAMA KELEMAHAN PENGENDALIAN]
Komponen      : [Penetapan Tujuan / Struktur dan Proses / Pencapaian Tujuan]
Subunsur      : [Kode dan nama, mis. 2.1 Identifikasi Risiko]
Nilai PK      : [skor] (Nilai PM: [skor])
Kondisi       : [kelemahan yang ditemukan dari dokumen — spesifik]
Dampak        : [konsekuensi pengendalian lemah terhadap tujuan organisasi]
Rekomendasi   : [tindakan perbaikan: siapa, apa, kapan — terukur]
Prioritas     : [Tinggi / Sedang / Rendah — berdasarkan bobot × gap skor]
```

> **TANPA unsur Sebab** — rezim LKE. Jangan menambahkan baris "Sebab" pada catatan/AoI.

Catatan khusus penalti (bila ada): cantumkan Sumber (APH/LHP BPK/BPKP/APIP/media), Jenis kasus (institusional/individual), Subunsur terkait, Nilai PK sebelum→sesudah penalti, alasan penurunan (kelemahan implementasi/komunikasi), dan dampak ke MRI/IEPK.

## Tingkat Maturitas (Tabel II.4)

| Level | Tingkat Maturitas | Interval Skor |
|-------|------------------|---------------|
| 1 | Rintisan | 1,00 ≤ Skor < 2,00 |
| 2 | Berkembang | 2,00 ≤ Skor < 3,00 |
| 3 | Terdefinisi | 3,00 ≤ Skor < 4,00 |
| 4 | Terkelola dan Terukur | 4,00 ≤ Skor < 4,50 |
| 5 | Optimum | ≥ 4,50 |

## Mekanisme Penalti (ringkas)

Diterapkan saat ada kasus korupsi tahap **penuntutan s.d. putusan** atau **OTT**. Langkah: (1) identifikasi kasus dari APH/LHP BPK/BPKP/APIP/media; (2) klasifikasi institusional vs individual; (3) hubungkan dengan subunsur terkait (Tabel III.1, ref/01); (4) tentukan penurunan — kelemahan implementasi → turun 1 gradasi (ke Level 2), kelemahan pengomunikasian → turun 2 gradasi (ke Level 1); (5) perbarui MRI/IEPK — jika nilai parameter MRI/IEPK > nilai subunsur setelah penalti, ikut turun; jika ≤, tidak berubah.

> Penurunan hanya untuk subunsur yang sebelumnya bernilai ≥ 3. **Detail kasus, 6 dimensi analisis, Tabel III.1 (hubungan subunsur ↔ kasus institusional/individual), dan prosedur PK per komponen & pelaporan PK: `references/01-bpkp-5-2021-pedoman-pk.md`.**

## Struktur Laporan Hasil Evaluasi (LHE)

Output formal PK adalah **LHE** (bukan KKSA). Strukturnya bertumpu pada hasil penilaian LKE + AoI:

```
A. PENDAHULUAN
   1. Latar Belakang & Dasar Pelaksanaan (ST/KP)
   2. Tujuan & Ruang Lingkup PK (komponen/unsur SPIP yang dinilai)
   3. Metodologi (PK atas PM — validasi self-assessment manajemen)
   4. Periode & Komposisi Tim

B. GAMBARAN UMUM
   [Objek PK, cakupan satker, status Nilai PM yang divalidasi]

C. HASIL PENILAIAN MATURITAS
   - Perbandingan Nilai PM vs Nilai PK per komponen (Penetapan Tujuan, Struktur & Proses,
     Pencapaian Tujuan) dan nilai SPIP/MRI/IEPK tertimbang
   - Tingkat Maturitas final (Level 1–5, Tabel II.4)
   - Penalti yang diterapkan (bila ada)

D. AREA OF IMPROVEMENT (AoI)
   [Daftar AoI prioritas — format Catatan AoI di atas; TANPA unsur Sebab]

E. SIMPULAN
   [Pernyataan tingkat maturitas SPIP terintegrasi hasil PK]

F. APRESIASI
```

## Batasan dan Prinsip PK

- **TANPA unsur Sebab** — rezim LKE; penilaian = Nilai PK + AoI, bukan KKSA. Jangan menambah unsur Sebab.
- **Nilai PK independen** — berdasarkan dokumen yang dibaca, bukan Nilai PM.
- **Berbasis bukti dokumen** — setiap skor PK dapat dikaitkan dengan dokumen nyata.
- **Transparan tentang keterbatasan** — jika dokumen tidak ada, tulis eksplisit di Catatan PK.
- **Tidak spekulatif** — jangan menaikkan skor karena "kemungkinan ada" dokumen; hanya nilai yang benar-benar ditemukan.
- **Konstruktif di AoI** — rekomendasi spesifik: siapa, apa, ukuran keberhasilan.
- **Subunsur 1.7** (Peran APIP) — Nilai PK dari hasil penilaian Kapabilitas APIP terpisah; jika tidak ada, ikuti Nilai PM dengan catatan.
- **SPIP, MRI, IEPK saling terkait** — perubahan skor subunsur SPIP dapat berdampak ke MRI/IEPK jika ada penalti.

## Referensi yang Digunakan

| Dokumen | Lokasi | Isi |
|---------|--------|-----|
| Pedoman PK — BPKP 5/2021 | `references/01-bpkp-5-2021-pedoman-pk.md` | Prosedur PM & PK, KK LEAD I, mekanisme penalti + Tabel III.1, pelaporan PK, karakteristik maturitas, waktu pelaksanaan |
| Parameter & Bobot Lengkap | `references/02-parameter-bobot-spip.md` | Bobot per subunsur SPIP/MRI/IEPK; kriteria validasi gradasi skor 1–5; kriteria skor Pencapaian Tujuan; red flag; formulir kalkulasi |
| Peta Cell LKE Kementerian | `references/03-peta-cell-lke-kementerian.md` | Input vs formula per sheet, baris & kolom yang boleh ditulis, mekanisme veto |
| Helper pengisi LKE (aman) | `references/fill_lke_safely.py` | Class `LKEWriter` — guard sheet/cell formula, backup otomatis |
| Daftar cell formula (guard) | `references/templates/cell-map-formulas.json` | Daftar pasti semua cell formula per sheet |
