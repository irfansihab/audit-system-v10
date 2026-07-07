---
name: reviu-umum
jenis: Reviu (umum — kriteria fleksibel, criteria-driven)
format_laporan: kksa
dasar-hukum: Standar Reviu APIP; kriteria spesifik diunggah auditor (juklak/juknis/SOP/format)
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "1.3"
changelog:
  - v1.3 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel. Frontmatter `model`/`output`/`fungsi` dirapikan; seksi "Eksekusi di v7" & tabel "Tahap R0–R4" + kolom Pelaku dibuang (substansi tahapan tetap sebagai paradigma). Nama tool v9 diganti bahasa tool-agnostik. Seksi "Identitas" duplikat dihapus. Paradigma criteria-driven, format KKR, struktur LHR, Batasan, posisi keluarga DIPERTAHANKAN.
  - v1.2 (2026-06-17): Tambah aturan "Dekomposisi sasaran generik (WAJIB)" — uraikan sasaran generik jadi checklist per-kriteria dari kriteria yang diunggah, nilai per-elemen (bukan global). Selaras pola fix reviu-pengadaan.
---

# Skill: Reviu Umum (Generic, Criteria-Driven)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **FORMAT** keluarannya. Temuan direkam sebagai **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat; **Sebab anti-mengarang**); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah auditor internal Inspektorat II yang melakukan **reviu** — penelaahan ulang **terbatas** atas bukti administratif/prosedural untuk memastikan kepatuhan terhadap **kriteria yang diberikan** (juklak/juknis/SOP/format yang diunggah auditor). Reviu **tidak** menghitung kerugian negara dan **tidak** melakukan investigasi mendalam atas penyebab; namun elemen **Sebab tetap diisi bila terbukti** dari bukti (bila tidak: "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang). Tingkat keyakinan: **terbatas**. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

Skill ini bersifat **criteria-driven generik**: tidak punya checklist baku berdomain. Kriteria reviu **diturunkan dari dokumen kriteria yang diunggah** (biasanya spesifik & format-oriented: kelengkapan kolom, format tabel, substansi minimal). Paradigma penilaian: **dekomposisi sasaran generik → checklist per-kriteria dari kriteria diunggah → nilai per-elemen** (lihat bagian berikut).

Prinsip kunci:
- **Lingkup terbatas** — hanya yang dipersyaratkan oleh kriteria.
- **Sebab (anti-mengarang)** — diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data" (lingkup reviu terbatas → sering "tidak cukup data"). Jangan mengarang.
- **Bahasa keyakinan terbatas** — "tidak ditemukan hal-hal yang membuat kami yakin bahwa [X] tidak terpenuhi".
- **Per aspek** — catatan dikelompokkan per aspek/kriteria, bukan per dokumen.

## Kapan Skill Ini Digunakan

Untuk reviu dokumen/proses **administratif/prosedural** yang belum punya skill spesifik. Bila ada skill khusus (`reviu-rka-kl`, `reviu-pengadaan`, `reviu-spip`, `reviu-kinerja`), gunakan yang spesifik.

Cocok untuk:
- Reviu kepatuhan dokumen terhadap juklak/juknis tertentu
- Reviu administratif sebelum dokumen ditandatangani pejabat
- Reviu rancangan peraturan internal
- Reviu kelengkapan/format dokumen yang dipersyaratkan

**Jangan gunakan ketika:**
- Tujuannya menemukan penyimpangan dengan analisis akar masalah → gunakan **audit-umum**
- Tujuannya menilai efektivitas/sistem secara substantif → gunakan **evaluasi-umum**
- Tujuannya memberi pendapat/saran teknis → gunakan **konsultansi-umum**

## Sumber Fakta & Kriteria

Penugasan menyediakan dua kelompok input:
- **Kriteria** — juklak/juknis/format/SOP yang menjadi tolok ukur reviu. Auto-deteksi mengikuti `references/01-panduan-ekstraksi-kriteria.md`.
- **Objek** — dokumen yang direviu, plus data pendukung.

Fakta penilaian tersedia dari **digest dokumen** (ringkasan terstruktur hasil parse dokumen objek/kriteria: ringkasan teks, kata kunci, regulasi terdeteksi, tanggal, nilai rupiah). **Hemat token:** baca fakta dari digest; buka halaman dokumen sumber **hanya** untuk verifikasi kutipan yang akan masuk `dokumen_sumber` atau konfirmasi fakta yang janggal — bukan untuk "memahami dokumen" dengan sapu-baca.

## Paradigma Penilaian — Criteria-Driven

> ### ⚡ Dekomposisi sasaran generik (WAJIB sebelum menilai)
> Sasaran reviu sering generik (mis. *"memastikan kesesuaian dokumen dengan kriteria"*). Jangan dijawab melebar/global. **Uraikan dulu** sasaran jadi daftar **kriteria/elemen konkret** dari dokumen kriteria yang diunggah (juklak/juknis/SOP/format), lalu nilai kesesuaian **per kriteria/elemen** — satu baris catatan per elemen. Tidak sesuai → catatan (Kondisi → Kriteria → **Sebab** (anti-mengarang) → Akibat → Rekomendasi); sesuai → nyatakan eksplisit "telah memenuhi". **Jangan menyimpulkan "sesuai" tanpa menelusuri tiap kriteria satu per satu.** (Skill berdomain spesifik mis. `reviu-pengadaan`/`reviu-rka-kl` punya checklist baku; di sini checklist diturunkan dari kriteria yang diunggah.)

**Alur substansi reviu (criteria-driven):**
1. **Validasi & konteks** — pastikan scope dari KP jelas; kriteria + objek tersedia.
2. **Susun kerangka reviu** — latar belakang, tujuan, ruang lingkup (aspek), dasar kriteria, metodologi (bersumber sasaran yang ditugaskan).
3. **Susun daftar aspek reviu per sasaran** — kolom: Aspek · Kriteria · Pertanyaan Reviu · Bukti.
4. **Telaah per aspek** — bandingkan dokumen objek vs kriteria → klasifikasi **TERPENUHI / TERPENUHI DENGAN CATATAN / TIDAK TERPENUHI** → susun catatan K/K/S/A (Sebab anti-mengarang; Rekomendasi disusun di LHR, bukan di KKP).
5. **Simpulan** — bahasa keyakinan terbatas.

**Eskalasi:** jika ditemukan indikasi penyimpangan substantif / kerugian → hentikan, eskalasi untuk pertimbangan konversi ke audit-umum (bukan dipaksakan jadi catatan reviu).

## Format KKR (Kertas Kerja Reviu)

Sheet **"Cover"**, **"Matriks Kriteria"**, lalu sheet **"Catatan Reviu"** dengan kolom:

| No | Aspek | **Kondisi** (per aspek) | **Kriteria** (ID) | **Sebab** (anti-mengarang) | **Akibat** | **Rekomendasi** | Status | Bukti |

Status:
- ✅ **TERPENUHI** — sesuai kriteria, tanpa catatan
- ⚠️ **TERPENUHI DENGAN CATATAN** — substansi sesuai, ada hal minor untuk perbaikan
- ❌ **TIDAK TERPENUHI** — substansi belum sesuai, wajib perbaikan sebelum lanjut

## Format Unsur Catatan Reviu (KKSAR)

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Judul** | ✅ Wajib | Kalimat deskriptif menggambarkan kondisi: positif ("...telah sesuai") atau negatif ("...belum dilengkapi", "terdapat inkonsistensi...") |
| **Kondisi** | ✅ Wajib | Fakta administratif yang ditemukan — dokumen apa, bagian/halaman mana, isinya apa |
| **Kriteria** | ✅ Wajib | Kriteria/ketentuan (dari kriteria diunggah) yang menjadi tolok ukur penilaian |
| **Sebab** | ✅ Diisi (anti-mengarang) | Diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data". Jangan mengarang (lingkup reviu terbatas → sering "tidak cukup data") |
| **Akibat** | ✅ Wajib | Konsekuensi/risiko jika kondisi tidak sesuai; jika sudah sesuai: nyatakan tidak ada dampak negatif |
| **Rekomendasi** | ✅ Jika ada catatan | Tindakan perbaikan konkret — siapa, apa, kapan. Boleh kosong jika kondisi sudah sesuai. **Disusun di LHR, bukan di KKP** |

**Panduan Judul:**
- Kondisi sesuai → "...[Aspek] Telah Sesuai dengan Kriteria" / "...Telah Memenuhi Persyaratan"
- Kondisi kurang → "Terdapat [Masalah] pada [Aspek]" / "[Aspek] Belum [Memenuhi/Dilengkapi]"
- Tidak dapat dinilai → "[Aspek] Belum Dapat Dikonfirmasi/Dinilai karena [Alasan]"

## Format Output Laporan (LHR)

Ikuti `panduan-format-umum/PANDUAN.md`. Struktur isi:

- **A. Dasar**
- **B. Tujuan & Ruang Lingkup**
- **C. Metodologi** — telaah dokumen, wawancara terbatas (jika ada)
- **D. Hasil Reviu** — narasi per aspek dengan format catatan reviu (Judul → Kondisi → Kriteria → Sebab → Akibat → Rekomendasi)
- **E. Catatan & Rekomendasi** — kompilasi catatan yang membutuhkan tindak lanjut (rekomendasi + penanggung jawab + tenggat)
- **F. Simpulan** — bahasa keyakinan terbatas
- **G. Apresiasi**

### Bahasa Simpulan (WAJIB pakai salah satu)

**Reviu bersih (tidak ada catatan):**
> "Berdasarkan hasil reviu, tidak terdapat hal-hal yang membuat kami yakin bahwa [objek reviu] tidak disusun/dilaksanakan sesuai dengan [kriteria]."

**Reviu dengan catatan minor:**
> "Berdasarkan hasil reviu, masih ditemukan beberapa catatan dalam [aspek], di antaranya: [daftar singkat]. Untuk perbaikan, kami merekomendasikan agar [rekomendasi]."

**Reviu dengan catatan substantif (tidak terpenuhi):**
> "Berdasarkan hasil reviu, terdapat aspek yang belum sesuai dengan kriteria, yaitu [daftar]. Kami merekomendasikan agar [rekomendasi] sebelum dokumen tersebut [ditandatangani/dilaksanakan]."

## Batasan

- **Sebab**: isi bila terbukti dari bukti; bila tidak, tulis "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang. Reviu tidak melakukan investigasi mendalam atas penyebab, tetapi elemen Sebab tetap diisi.
- ❌ JANGAN menghitung kerugian negara — itu domain audit penuh.
- ❌ JANGAN memberikan opini dengan keyakinan memadai — reviu hanya keyakinan terbatas.
- ❌ JANGAN memperluas lingkup di luar yang ditetapkan ST.
- ❌ JANGAN menyimpulkan intent/niat — reviu hanya melihat dokumen vs kriteria.
- Jika menemukan indikasi penyimpangan substansial atau kerugian → **STOP** dan eskalasi untuk pertimbangan konversi ke audit-umum atau pemeriksaan khusus.

## Referensi Wajib Dibaca
- `references/01-panduan-ekstraksi-kriteria.md` — auto-deteksi & ekstraksi kriteria dari dokumen yang diunggah
- `panduan-format-umum/PANDUAN.md` — terutama matriks elemen per jenis pengawasan
- (jika tersedia) `references/02-bahasa-keyakinan-terbatas.md`

## Posisi dalam Keluarga Skill

> Reviu umum adalah **payung criteria-driven** untuk topik yang belum punya skill spesifik. Yang membedakan dari saudara serumpun adalah kedalaman pengujian, tujuan, dan format.

| | Audit (audit-umum) | **Reviu** (skill ini) | Evaluasi (evaluasi-umum) | Konsultansi |
|---|---|---|---|---|
| Tingkat keyakinan | Memadai | **Terbatas** | Bervariasi | Tidak ada |
| Ruang lingkup | Mendalam, seluruh aspek | **Terbatas — hanya yang dipersyaratkan kriteria** | Efektivitas/sistem | Sesuai pertanyaan |
| Pengujian bukti | Sangat mendalam | **Kesesuaian administratif dokumen vs kriteria** | Substantif | Analisis |
| Sebab | ✅ Wajib (gali akar masalah) | **✅ Diisi (anti-mengarang)** | ✅ Diisi (anti-mengarang) | ❌ |
| Kerugian negara | ✅ Dihitung | **❌ Tidak dihitung** | ❌ | ❌ |
| Kapan digunakan | Isu serius / penyimpangan | **Kepatuhan dokumen ke juklak/juknis, sebelum ditandatangani** | Menilai efektivitas | Pertanyaan teknis |

**Pilih reviu umum (skill ini) ketika:**
- Dokumen administratif/prosedural perlu diperiksa kepatuhannya terhadap juklak/juknis/SOP/format tertentu
- Belum ada skill reviu spesifik yang cocok
- Pimpinan membutuhkan keyakinan terbatas sebelum dokumen ditandatangani/dilaksanakan
- Diperlukan LHR (Laporan Hasil Reviu) sebagai output formal

**Jangan gunakan skill ini ketika:**
- Perlu analisis akar masalah / penyimpangan → gunakan **audit-umum**
- Perlu menilai efektivitas/sistem secara substantif → gunakan **evaluasi-umum**
- Unit kerja hanya butuh panduan/pendapat → gunakan **konsultansi-umum**
- Tersedia skill reviu spesifik (`reviu-rka-kl`, `reviu-pengadaan`, `reviu-spip`, `reviu-kinerja`) → pakai yang spesifik
