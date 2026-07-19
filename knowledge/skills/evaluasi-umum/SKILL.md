---
name: evaluasi-umum
jenis: Evaluasi (umum — kriteria fleksibel)
format_laporan: kksa
dasar-hukum: Standar Audit Intern Pemerintah Indonesia (AAIPI); pedoman/juklak evaluasi sesuai objek
kode-surat: PW.04.05
tingkat-keyakinan: terbatas
version: "1.2"
changelog:
  - v1.2 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness uji: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: paradigma evaluasi (keyakinan terbatas), kerangka penilaian, kriteria/referensi, format temuan KKSAR, struktur LHE, materialitas. Frontmatter `model`/`output`/`fungsi` dirapikan; seksi "Eksekusi di v7" & tabel "Tahap E0–E4" + kolom Pelaku dibuang; nama tool v9 sebagai resep diganti bahasa tool-agnostik; seksi "Identitas" duplikat dihapus. **Sebab anti-mengarang (KKSAR) dipertahankan utuh.**
  - v1.1 (2026-06-17): Sebab diisi anti-mengarang (semua jenis sejak 17 Jun 2026 — bila tidak terbukti tulis "Tidak ditemukan penyebab"/"Tidak cukup data"). Substansi domain dipertahankan.
---

# Skill: Evaluasi Umum (Generic, Criteria-Driven)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **FORMAT** keluarannya. Evaluasi umum berbasis temuan **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat); **Rekomendasi dikompilasi di LHE, bukan di KKP**. (Catatan keluarga: evaluasi non-LKE ber-Sebab; evaluasi ber-LKE — SAKIP/SPIP/RB — memakai instrumen LKE tanpa Sebab.)

## Kapan Skill Ini Digunakan

Untuk evaluasi yang belum punya skill spesifik. Jika ada (evaluasi-sakip, evaluasi-spip, evaluasi-reformasi-birokrasi, evaluasi-manajemen-risiko), gunakan yang spesifik. Skill umum cocok untuk:

- Evaluasi efektivitas program/kegiatan baru
- Evaluasi kebijakan internal (Permen/Perdirjen baru)
- Evaluasi kinerja unit/satker dengan kerangka khusus
- Evaluasi kesesuaian implementasi dengan rencana strategis
- Evaluasi gabungan (mis. SAKIP + RB) dengan kriteria gabungan

**Jangan gunakan ketika:**
- Tujuannya menemukan penyimpangan dengan akar masalah → **audit-umum**
- Tujuannya hanya menelaah kepatuhan administratif → **reviu-umum**
- Tujuannya melaporkan status periodik → **pemantauan-umum**

## Lingkup & Paradigma

Kamu adalah evaluator Inspektorat II yang menilai **efektivitas, kinerja, atau kesesuaian** suatu objek terhadap kriteria evaluasi. Berbeda dari reviu (administratif) dan audit (kepatuhan terperinci), evaluasi bersifat **substantif** dan menilai apakah suatu sistem/program **berfungsi sebagaimana mestinya**. Tingkat keyakinan: **terbatas**. Kode nomor surat: **PW.04.05**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

Karakteristik:
- **Temuan dengan Sebab (anti-mengarang)** — Kondisi, Kriteria, Sebab, Akibat, Rekomendasi. Sebab diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data" (lingkup evaluasi terbatas → sering "tidak cukup data"). **Jangan mengarang.**
- Rekomendasi **dikompilasi terpisah di Bab G** LHE (bukan per temuan seperti audit pengadaan).
- Sering memakai **dimensi/skor** (mis. tertib administrasi 1–4, kualitas 1–5).
- Hasil dapat berbentuk **predikat/level** (mis. "Sangat Baik", "Baik", "Cukup", "Kurang").
- Dapat memakai **format dimensi khusus** seperti EvaRB jika kriteria mensyaratkan (lihat `panduan-format-umum/PANDUAN.md`). Bila kriteria mensyaratkan format dimensi khusus, **hormati format itu**.

## Sumber Fakta: Kriteria + Objek (Criteria-Driven)

Evaluasi umum bersifat **criteria-driven**: auditor mengunggah **kriteria evaluasi** (pedoman teknis + lembar kerja evaluasi/LKE + instrumen survei + data baseline) dan **dokumen objek** yang dievaluasi. Tidak ada pipeline rule deterministik — kamu **menilai sendiri** objek terhadap kriteria & rubrik (judgment), dengan keyakinan **terbatas**.

Struktur input tipikal:
```
input/
├── kriteria/        # ← pedoman evaluasi, juklak, instrumen LKE/rubrik skor
├── objek/           # ← dokumen + data objek yang dievaluasi
└── data-pendukung/
```

Kriteria evaluasi sering kompleks: pedoman teknis + LKE + instrumen survei + data baseline. Ekstraksi kriteria mengikuti `references/01-panduan-ekstraksi-kriteria.md` dengan tambahan deteksi instrumen (LKE.xlsx, kuesioner, rubrik skor).

**Hemat token:** baca fakta dari ringkasan/digest dokumen lebih dulu; buka halaman dokumen sumber **hanya** untuk verifikasi halaman yang dikutip atau konfirmasi fakta yang janggal — bukan untuk "memahami dokumen" secara menyeluruh.

## Kerangka Penilaian

Penilaian evaluasi disusun bertingkat: **Dimensi/Aspek → Sub-aspek → Indikator**, masing-masing dengan **bobot**, **sumber data**, **metode**, dan **rubrik/skor**.

- Untuk tiap indikator: kumpulkan bukti → nilai sesuai rubrik (skor + % capaian) → bila ada hal yang membutuhkan rekomendasi sistem, susun sebagai temuan (K/K/S/A, Sebab anti-mengarang).
- Skor di bawah ambang / temuan signifikan ditandai agar ditinjau saat persetujuan KKP.
- Rekapitulasi per dimensi menghasilkan **skor total** dan **predikat/level** sesuai metodologi.

> **⚡ Dekomposisi kriteria generik (WAJIB sebelum menilai).** Sasaran/kriteria evaluasi sering ditulis generik (mis. "menilai efektivitas program"). Jangan dijawab melebar. **Terjemahkan dulu jadi dimensi → indikator konkret** sesuai objek yang dievaluasi, lalu nilai **per indikator** terhadap rubrik. Jangan menyimpulkan predikat tanpa menelusuri tiap indikator satu per satu.

### Format LKE/Lembar Kerja Evaluasi

Bila kriteria menyertakan instrumen LKE (Excel), strukturkan penilaian sebagai matriks:

**Skor per Indikator:**

| ID | Aspek | Sub-aspek | Indikator | Bobot | Skor Maks | Skor Aktual | % Capaian | Bukti | Catatan |

**Rekapitulasi Dimensi:**

| Dimensi | Bobot | Skor | % | Predikat |

**Daftar Temuan** (untuk hal yang membutuhkan rekomendasi sistem — Sebab anti-mengarang):

| ID | Aspek | **Kondisi** | **Kriteria** | **Sebab** | **Akibat** | **Rekomendasi** | Bukti |

## Materialitas dalam Evaluasi

Tidak menggunakan ambang rupiah seperti audit. Evaluasi memakai:

| Level | Kriteria | Aksi |
|-------|----------|------|
| Catatan minor | Skor di bawah target tetapi bukan dimensi utama | Cantumkan di analisis dimensi (Bab E.3) |
| Temuan signifikan | Skor di bawah target di dimensi utama, **atau** indikasi sistem tidak berjalan | Temuan (K/K/S/A, Sebab anti-mengarang) + rekomendasi di Bab G |
| Temuan strategis | Mempengaruhi capaian misi/sasaran organisasi | Temuan (K/K/S/A, Sebab anti-mengarang) + eskalasi ke Inspektur |

## Penutupan Penilaian per Aspek (WAJIB — bukan exception-only)

Setelah menelusuri seluruh checklist/aspek di atas, **tutup TIAP butir** dengan kesimpulan eksplisit — jangan hanya melaporkan yang bermasalah. Untuk **setiap** butir/aspek yang relevan dengan sasaran, beri kesimpulan:

- **SESUAI** — butir memenuhi kriteria (direkam sebagai kesimpulan penilaian; tak perlu jadi temuan).
- **TIDAK SESUAI** — ada deviasi → rinci jadi **temuan** (K/K/S/A) sesuai Format Unsur Temuan.
- **TIDAK CUKUP DATA** — dokumen/data tak memadai untuk menyimpulkan → catat + (bila material) rekomendasikan langkah lanjut. **Jangan mengarang** kesimpulan.

Setiap butir sertakan **dasar** singkat (bukti dari dokumen — nama file + halaman/angka). Tujuannya agar **cakupan penilaian terdokumentasi** untuk Ketua Tim/Pengendali Teknis — terlihat apa yang sudah dinilai memadai, bukan sekadar daftar masalah. Terapkan **JUDGMENT substansi** (mutu, kelengkapan, konsistensi, kecukupan informasi), jangan berhenti di diskrepansi termudah (nomor/label/terbilang).

> Perekaman kesimpulan tiap aspek & render tabelnya diorkestrasikan oleh harness/INTEGRAL (di v7: tool `write_penilaian_aspek`, dipanggil sebelum render KKP). Skill ini menetapkan **substansinya**: butir apa yang dinilai & bagaimana menyimpulkannya.

## Format Unsur Temuan (KKSAR)

### Framework Elemen Isi

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Judul Temuan** | ✅ Wajib | Kalimat deskriptif menggambarkan kondisi: positif ("...telah efektif") atau negatif ("...belum berjalan", "terdapat ...") |
| **Kondisi** | ✅ Wajib | Fakta yang ditemukan — objek/indikator apa, capaian/skor, dokumen mana |
| **Kriteria** | ✅ Wajib | Pedoman/indikator/ketentuan yang menjadi tolok ukur penilaian |
| **Sebab** | ✅ Diisi (anti-mengarang) | Diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab"/"Tidak cukup data". Jangan mengarang (lingkup evaluasi terbatas, jadi sering "tidak cukup data") |
| **Akibat** | ✅ Wajib | Konsekuensi/risiko bila kondisi tidak sesuai; jika sudah sesuai: nyatakan tidak ada dampak negatif |
| **Rekomendasi** | ✅ Jika ada catatan | Tindakan perbaikan konkret — siapa, apa, kapan. Boleh kosong jika kondisi sudah sesuai. **Dikompilasi di LHE (Bab G), bukan di KKP** |

### Format Catatan/Temuan (per aspek)

```
**TEMUAN [NOMOR]  [JUDUL — kalimat deskriptif kondisi]**

Kondisi    : [Fakta yang ditemukan. Sebutkan: aspek/indikator + capaian/skor + dokumen/bukti.
              Jika efektif/sesuai: nyatakan bahwa kriteria telah terpenuhi.
              Jika tidak: sebutkan apa yang kurang/tidak sesuai secara spesifik.]

Kriteria   : [Pedoman/indikator/ketentuan acuan penilaian. Gunakan references/ untuk teks normatif.]

Sebab      : [Akar penyebab bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab" /
              "Tidak cukup data". Jangan mengarang.]

Akibat     : [Konsekuensi/risiko dari kondisi yang ditemukan.
              Jika sesuai: "Tidak ditemukan dampak negatif dari aspek ini."
              Jika tidak: uraikan risiko terhadap efektivitas/kinerja/capaian.]

Rekomendasi: [Tindakan perbaikan spesifik (sistem-level): apa, oleh siapa, kapan.
              Dikompilasi di LHE Bab G. Boleh kosong jika kondisi sudah sesuai.]
```

**Panduan Judul Temuan:**
- Kondisi sesuai → "...[Aspek] Telah Efektif/Sesuai dengan Kriteria"
- Kondisi kurang → "Terdapat [Masalah] pada [Aspek]" / "[Aspek] Belum [Berjalan/Efektif/Memadai]"
- Tidak dapat dinilai → "[Aspek] Belum Dapat Dinilai karena [Alasan]"

## Format Output Laporan (LHE)

Ikuti `panduan-format-umum/PANDUAN.md`. Struktur isi:

- **A. Dasar**
- **B. Tujuan & Ruang Lingkup**
- **C. Metodologi** (telaah dokumen, wawancara, observasi, analisis data)
- **D. Gambaran Umum Objek Evaluasi**
- **E. Hasil Evaluasi**
  - E.1 Skor per Dimensi (tabel rekapitulasi)
  - E.2 Predikat & Posisi (jika ada level/tingkat)
  - E.3 Analisis Per Dimensi (narasi)
- **F. Temuan & Catatan** — Kondisi/Kriteria/**Sebab**/Akibat/Rekomendasi per temuan (Sebab anti-mengarang: diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data" — jangan mengarang)
- **G. Rekomendasi** — kompilasi rekomendasi terpilih (sistem-level, bukan per temuan)
- **H. Simpulan**
- **I. Apresiasi**

### Bahasa Simpulan

**Predikat tinggi:**
> "Berdasarkan hasil evaluasi, [objek] memperoleh nilai [X] dari skor maksimal [Y] dengan predikat **[Sangat Baik/Baik]**. Rekomendasi yang diberikan bersifat penyempurnaan untuk peningkatan kualitas berikutnya."

**Predikat menengah:**
> "Berdasarkan hasil evaluasi, [objek] memperoleh nilai [X] dengan predikat **[Cukup]**. Untuk peningkatan ke predikat berikutnya, kami merekomendasikan [3–5 rekomendasi prioritas]."

**Predikat rendah:**
> "Berdasarkan hasil evaluasi, [objek] memperoleh nilai [X] dengan predikat **[Kurang]**. Diperlukan langkah perbaikan menyeluruh sebagaimana rekomendasi pada Bagian G."

## Struktur Keluaran (JSON KKP)

```json
{
  "skill": "evaluasi-umum",
  "kriteria_terindeks": [...],
  "instrumen": [
    {"id": "I01", "aspek": "...", "indikator": "...", "bobot": 0, "skor_maks": 0}
  ],
  "skor_per_indikator": [
    {"indikator_id": "I01", "skor": 0, "persen_capaian": 0, "bukti": [...]}
  ],
  "rekap_dimensi": [
    {"dimensi": "...", "skor": 0, "persen": 0, "predikat": "..."}
  ],
  "temuan": [
    {"id": "T01", "kondisi": "...", "kriteria": "...", "sebab": "... (anti-mengarang; 'Tidak cukup data' bila tak terbukti)", "akibat": "...", "rekomendasi": "..."}
  ],
  "predikat_total": "...",
  "skor_total": 0
}
```

## Referensi
- `references/01-panduan-ekstraksi-kriteria.md`
- `panduan-format-umum/PANDUAN.md` — matriks elemen (Kondisi/Kriteria/Sebab/Akibat/Rekomendasi, Sebab anti-mengarang, untuk evaluasi)

## Batasan
- **Sebab**: isi bila terbukti dari bukti; bila tidak, tulis "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang. Lingkup evaluasi terbatas, sehingga wajar bila banyak temuan ber-Sebab "tidak cukup data".
- Tidak menghitung kerugian negara — itu domain audit penuh.
- Tidak menelaah kepatuhan administratif terperinci — itu domain reviu; evaluasi menilai efektivitas/kinerja/kesesuaian secara substantif.
- Jangan memperluas lingkup di luar yang ditetapkan; bila kriteria mensyaratkan format dimensi khusus (mis. EvaRB), hormati format tersebut dan dokumentasikan deviasi format.

## Catatan Khusus

Jika kriteria evaluasi mensyaratkan **format dimensi khusus** (seperti PermenPAN-RB untuk EvaRB: Ketepatan/Ketercapaian/Kualitas/Kesesuaian) dan format itu **berbeda** dari format temuan standar, gunakan format yang dipersyaratkan kriteria dan dokumentasikan deviasinya pada penyusunan KP.

Untuk kasus yang sudah ada skill spesifik (SAKIP, SPIP, MR, RB), prioritaskan skill spesifik karena instrumen sudah disiapkan lengkap di references-nya masing-masing.

## Posisi dalam Keluarga Skill Evaluasi

> Semua skill evaluasi menilai efektivitas/kinerja/kesesuaian. Yang membedakan adalah instrumen, format unsur, dan ada/tidaknya LKE.

| | **Evaluasi Umum** (skill ini) | Eval SAKIP/SPIP/RB (ber-LKE) | Eval Manajemen Risiko |
|---|---|---|---|
| Tingkat keyakinan | **Terbatas** | Terbatas | Terbatas |
| Instrumen | **Kriteria fleksibel + rubrik bila ada** | LKE baku (instrumen standar) | Register risiko + kontrol |
| Format unsur | **K/K/S/A/R (ber-Sebab)** | Skor/predikat + AoI (tanpa Sebab) | K/K/S/A/R (ber-Sebab) |
| Output | KKE + LHE | LKE terisi + rekap predikat + LHE | KKE + LHE |
| Kapan | **Objek tanpa skill spesifik** | SAKIP/SPIP/RB | Profil & mitigasi risiko unit |

**Pilih evaluasi umum (skill ini) ketika** objek evaluasi belum punya skill spesifik dan kriteria bersifat fleksibel (pedoman/juklak/rubrik yang diunggah auditor). **Jangan gunakan** bila tersedia skill spesifik (SAKIP/SPIP/RB/MR) atau bila tujuannya audit (penyimpangan+akar)/reviu (kepatuhan administratif)/pemantauan (status periodik).
