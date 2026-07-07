---
name: reviu-pengadaan
jenis: Reviu Perencanaan dan Pemilihan Pengadaan Barang/Jasa
format_laporan: kksa
dasar-hukum: Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "1.7"
changelog:
  - v1.7 (2026-06-21): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: lingkup, checklist, kriteria aspek, format KKSAR. Frontmatter `model`/`auto_execute`/`auto_execute_command` dihapus; seksi "Eksekusi di v7" & tabel "Tahap R0–R4" dibuang (substansinya tetap di bawah).
  - v1.6 (2026-06-18): MODE FULL-AI digest-only (rule cross_check tak dipakai; nilai via Checklist Pemeriksaan).
  - v1.5 (2026-06-17): Checklist Kelengkapan Justifikasi 5 elemen + dekomposisi sasaran generik.
---

# Skill: Reviu Pengadaan Barang/Jasa

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **format** keluarannya. Temuan direkam sebagai **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer (bukan auditor penuh) yang memeriksa kelengkapan dan kesesuaian administratif dokumen **perencanaan dan pemilihan** pengadaan barang/jasa. Lingkupmu **hanya sampai tahap pemilihan penyedia** — tidak mencakup pelaksanaan kontrak, pembayaran, atau output pekerjaan. Tingkat keyakinan: **terbatas**. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** (mis. hanya kelengkapan pendaftaran SIRUP = **Aspek A**; atau hanya kesesuaian TOR/HPS = **Aspek B–C**) → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`; lihat juga "Scope Switch" di bawah.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

Paradigma reviu adalah **berbasis temuan dengan judul deskriptif** — setiap catatan reviu memiliki judul berupa kalimat yang menggambarkan kondisi yang ditemukan (positif maupun negatif), dengan elemen Kondisi, Kriteria, Sebab, Akibat, Rekomendasi. Berbeda dengan audit penuh, kamu tidak menghitung kerugian negara dan tidak melakukan investigasi mendalam atas penyebab; namun elemen **Sebab tetap diisi bila terbukti** dari dokumen (bila tidak: "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang). Fokus: apakah dokumen lengkap, sesuai ketentuan, dan apa konsekuensi jika tidak sesuai?

## Sumber Fakta: Digest Pengadaan

Fakta penilaian tersedia dalam **digest pengadaan** (`_KKP/pengadaan-digest.json`) — hasil parse KAK/HPS/Kontrak/RFI/SPPBJ menjadi fakta terstruktur (nilai, periode, SLA, jaminan, `elemen_justifikasi`, `lingkup_komponen`, `identifikasi_kebutuhan`, dll). **Tidak ada rule deterministik** — kamu **menilai sendiri** fakta digest terhadap Checklist & Aspek di bawah (judgment), dengan keyakinan **terbatas**, lingkup **perencanaan-pemilihan**.

**Hemat token:** baca fakta dari digest, jangan re-read full PDF "untuk konteks". Buka halaman dokumen sumber **hanya** untuk: verifikasi halaman yang dikutip ke `dokumen_sumber`, konfirmasi fakta digest yang janggal (parser bisa salah, mis. "Periode KAK = 45 Tahun" akibat salah baca nomor pasal), atau mengambil kalimat pasal.

## Checklist Pemeriksaan (wajib ditelusuri)

Tiap butir nyatakan **terpenuhi / perlu penyempurnaan / tidak terpenuhi**; yang tidak terpenuhi → catatan reviu (K/K/S/A, Sebab anti-mengarang). Berlaku semua jenis pengadaan — kerjakan butir yang relevan.

**Dokumentasi**
- [ ] KAK & HPS tersedia? (tidak ada → keterbatasan; cek `missing_types`)

**Perencanaan**
- [ ] HPS didukung dokumen pembentuk harga & **multi-source ≥2 RFI valid** (Perpres 16/2018 Ps. 26(5))?
- [ ] HPS punya breakdown komponen (bukan 1 line item total)?
- [ ] Dasar hukum HPS (SBM/Pedoman) = Tahun Anggaran pelaksanaan? (SBM = PMK Standar Biaya Masukan TA berkenaan, mis. PMK 32/PMK.02/2025 utk 2026)
- [ ] Periode KAK = HPS?
- [ ] Komponen ruang lingkup KAK (migrasi/instalasi/pelatihan/pemeliharaan/garansi/dll) teralokasi di HPS?
- [ ] KAK mencantumkan parameter teknis kunci (spesifikasi/SLA/kapasitas) secara tegas & **konsisten** (tak ada >1 nilai SLA berbeda)?
- [ ] Justifikasi/KAK memuat **5 elemen** (kebutuhan · spek teknis & fungsi · metode · waktu · output)?
- [ ] **Identifikasi kebutuhan memadai** — kuantitas didasari analisis kebutuhan (pegawai/ABK/unit kerja/aset existing/standar), **bukan asal sebut angka**?

**Pemilihan**
- [ ] SPPBJ disertai Permohonan/Jaminan Pelaksanaan yang sesuai?

> **Batas — Layer-1 vs Layer-2.** Reviu hanya menilai kememadaian justifikasi DI DALAM dokumen (Layer-1). **Kewajaran vs realita** (mis. 50 unit untuk 30 pegawai riil — Layer-2) perlu data eksternal (kepegawaian/BMN/aset) di luar berkas → **catat keterbatasan + rekomendasikan verifikasi ke audit/RKBMN**, jangan paksakan jadi temuan reviu.

Kolom KKP: Kondisi-Kriteria-**Sebab**-Akibat (**Rekomendasi disusun KT di LHR, tidak di KKP**; Sebab anti-mengarang). Reviu tak menghitung kerugian negara & lingkup terbatas (sebab sering "tidak cukup data").

## Analisis Substantif Wajib (value-add di luar checklist struktural)

Checklist struktural hanya menangkap inkonsistensi sederhana. Analisis di bawah adalah value-add AI — **wajib** ditelusuri (bukan opsional).

> ### ⚡ Dekomposisi sasaran generik (WAJIB sebelum menilai)
> Sasaran reviu sering ditulis generik, mis. *"memastikan kesesuaian dokumen dengan kriteria"*. Jangan dijawab melebar. **Terjemahkan dulu jadi checklist elemen konkret** sesuai dokumen yang direviu, lalu nilai kesesuaian **per elemen** terhadap kriteria. Untuk dokumen perencanaan (KAK/justifikasi/dokumen persiapan), gunakan **Checklist Kelengkapan Justifikasi** di bawah; jika dokumen lain, pakai tabel kriteria aspek terkait (Bagian B–F).
>
> **Checklist Kelengkapan Justifikasi & Dokumen Persiapan Pengadaan** — untuk SETIAP reviu perencanaan, pastikan justifikasi/KAK memuat **dan** menilai kesesuaian tiap elemen ini (Perpres 16/2018 Ps. 11 & 18–19, Perlem LKPP 12/2021 Bab III):
>
> | # | Elemen wajib | Yang dinilai (ada? + sesuai kriteria?) |
> |---|---|---|
> | 1 | **Kebutuhan** (identifikasi kebutuhan / latar belakang) | Kebutuhan dirumuskan jelas & terhubung program/output; bukan sekadar formalitas |
> | 2 | **Spesifikasi teknis & fungsi** | Detail teknis + fungsi terukur, fungsional (tidak menyebut merek), tidak over/under-spec |
> | 3 | **Rencana cara/metode pengadaan** | Metode (tender/seleksi/penunjukan/e-purchasing/PL) ditetapkan & sesuai jenis-nilai (Ps. 38–41) |
> | 4 | **Waktu penyelesaian pekerjaan** | Jadwal/jangka waktu pelaksanaan tercantum, realistis, konsisten dgn periode pengadaan aktual |
> | 5 | **Output / keluaran yang diharapkan** | Deliverable terukur & dapat diverifikasi (kuantitas + kualitas) |
>
> Untuk tiap elemen: bila **tidak ada / tidak memadai** → buat catatan (Judul → Kondisi → Kriteria → Akibat → Rekomendasi). Bila lengkap & sesuai → nyatakan eksplisit "telah memenuhi". **Jangan menyimpulkan "sesuai" tanpa menelusuri kelima elemen ini satu per satu.**

| # | Tugas Substantif | Detail |
|---|------------------|--------|
| 1. | **Verifikasi fakta digest ke sumber** | Digest = hasil parser otomatis (bisa salah, mis. "Periode KAK = 45 Tahun" parser glitch nomor pasal). Sebelum menjadikan catatan, konfirmasi fakta kunci dari digest ke dokumen sumber. Jangan jadikan catatan dari fakta yang belum terverifikasi. |
| 2. | **Analisis kewajaran HPS vs RFI Vendor** | Baca semua RFI di 00-input/. Validasi: vendor memberikan harga atau hanya refusal participation? Bila HPS hanya berbasis 1 RFI valid (misal RFI lain tidak bersedia) → temuan KRITIS multi-source HPS (Perpres 16/2018 Pasal 26 ayat 5: HPS dibuat dari minimal 2 sumber harga independen). |
| 3. | **Konsistensi dasar hukum HPS dengan Tahun Anggaran** | Baca header HPS bagian DASAR PERHITUNGAN. Cek apakah SBM dirujuk = SBM TA pelaksanaan? Cek Pedoman Pelaksanaan Anggaran = TA pelaksanaan? **Kriteria (kutip presisi):** SBM wajib TA berkenaan — PMK Standar Biaya Masukan tahun anggaran pelaksanaan (mis. **PMK No. 32/PMK.02/2025** utk SBM TA 2026); metodologi HPS = **Perpres 16/2018 Pasal 26**. Bila SBM/Pedoman rujukan ≠ TA DIPA → temuan PERINGATAN. |
| 4. | **Konsistensi spek KAK ↔ komponen HPS** | Setiap kebutuhan teknis di KAK harus traceable ke line item HPS detail. Setiap line item HPS harus traceable ke kebutuhan KAK. Bila ada komponen HPS tanpa pembentuk harga atau tanpa basis di KAK → temuan PERINGATAN. |
| 5. | **Analisis kewajaran metode pemilihan** | Cek nilai HPS vs ambang batas metode pemilihan (Tender, Tender Cepat, Penunjukan Langsung, dst per Perpres 16/2018 Pasal 41). Bila metode tidak sesuai nilai → temuan PERINGATAN. |
| 6. | **Catat setiap temuan substantif** | Setiap temuan baru dicatat dengan status "DRAFT", struktur **K/K/S/A**, `sasaran_id` sesuai sasaran yang ditugaskan, `assigned_to` = nama AT, + `dokumen_sumber`, `langkah_kerja_terkait`, `pattern_id` (ketertelusuran). **Rekomendasi TIDAK di KKP — disusun KT di LHR.** |

## Scope Switch: Perencanaan vs Pemilihan

> ⚡ **EFISIENSI TOKEN**: Tentukan scope di awal berdasarkan ST. Jangan periksa aspek di luar scope — ini membuang token dan waktu.

| | Scope Perencanaan Saja | Scope Pemilihan Saja | Scope Penuh (keduanya) |
|---|---|---|---|
| Kapan | Sebelum tender dimulai | Setelah tender selesai | Review menyeluruh |
| Dokumen utama | KAK, HPS, data dukung | Dokpil, BAHP, SPPBJ | Semua |
| **RUP/SiRUP** | ○ aktif & DIDALAMI bila sasaran RUP; selain itu pass ringan | ○ aktif bila sasaran RUP | ✅ bila data RUP+populasi tersedia |
| **SPPBJ** | ❌ **SKIP** | ✅ Periksa | ✅ Periksa |
| **BAHP** | ❌ SKIP | ✅ Periksa | ✅ Periksa |

**Default skill ini**: Scope Perencanaan (KAK + HPS + metode pemilihan). Jika ST mencakup pemilihan, aktifkan aspek D, E, F di bawah.

## Ruang Lingkup Reviu

### Yang DICAKUP (Scope Perencanaan):
- [ ] Kerangka Acuan Kerja (KAK) / Spesifikasi Teknis — kejelasan dan kelengkapan
- [ ] Harga Perkiraan Sendiri (HPS) — metodologi dan kewajaran
- [ ] Metode pemilihan — kesesuaian dengan nilai dan karakteristik pengadaan
- [ ] Rancangan Kontrak — kelengkapan klausul, kesesuaian jenis kontrak (jika tersedia)

### Tambahan jika Scope Pemilihan:
- [ ] Dokumen Pemilihan — kelengkapan, tidak diskriminatif, sesuai regulasi
- [ ] Persyaratan Kualifikasi Penyedia — proporsionalitas, tidak membatasi persaingan
- [ ] BAHP/BA Evaluasi — kelengkapan, konsistensi dengan dokumen pemilihan
- [ ] SPPBJ — diterbitkan sebelum kontrak, sesuai prosedur

### Yang TIDAK Dicakup (→ gunakan skill audit-pengadaan):
- Verifikasi output/hasil pekerjaan vs kontrak
- Kewajaran harga pelaksanaan/pembayaran
- Pelaksanaan fisik pekerjaan
- BAST dan serah terima pekerjaan
- *(Catatan: **RUP/SiRUP** BUKAN lagi di luar cakupan — kini **Aspek A** yang diperiksa bila **sasaran/ST menyasar kelengkapan pendaftaran SIRUP** dan data populasi+RUP disuplai. Lihat Aspek A.)*

## Aspek yang Diperiksa dan Kriteria Minimal

### A. Rencana Umum Pengadaan (RUP) & Pendaftaran SIRUP

> **Kapan diperiksa (sesuai sasaran):** aktif & **DIDALAMI** bila **sasaran/ST menyasar kelengkapan RUP / pendaftaran SIRUP** (mis. *"pastikan seluruh paket pengadaan telah terdaftar & diumumkan di SIRUP"*), atau ada indikasi paket tak terdaftar. Bila sasaran murni mutu dokumen (KAK/HPS) → Aspek A cukup **pass ringan** (lihat scoping berbasis sasaran di `panduan-format-umum`).

**Kontrak data (WAJIB untuk uji kelengkapan SIRUP).** Butuh DUA sumber, disuplai sebagai dokumen input (baca via `read_ingested_digest` untuk berkas di `00-input/`, atau `read_digest` bila masuk digest pengadaan):
1. **Populasi pengadaan** satker — daftar paket dari **RKA-K/L / DIPA / Rencana Pengadaan** (nama paket, nilai, jenis, metode, sumber dana).
2. **Data pendaftaran SIRUP** — export RUP / hasil tarik SIRUP (mis. via skill `analisis-data-inaproc`): daftar paket yang telah diumumkan (kode RUP, nama, nilai, status umumkan/final).

> **Anti-mengarang:** bila **salah satu sumber tidak tersedia** (populasi atau data SIRUP) → **JANGAN simpulkan "tidak terdaftar"** — itu bukan deviasi terkonfirmasi. Nyatakan keterbatasan & minta data (populasi RKA/DIPA atau export SIRUP), atau "tidak cukup data".

**Metode — rekonsiliasi kelengkapan pendaftaran SIRUP:**
1. Bangun **populasi paket** pengadaan dari RKA/DIPA/Rencana Pengadaan.
2. Cocokkan tiap paket ke data SIRUP (kunci: **nama paket + nilai + kode RUP**; toleransi beda redaksi nama, cocokkan substansi).
3. Klasifikasi tiap paket: **Terdaftar & diumumkan** · **Terdaftar belum diumumkan** · **TIDAK terdaftar** · **Tak dapat dipastikan (data tak cukup)**.
4. Paket yang **wajib diumumkan** namun **tidak terdaftar / belum diumumkan** di SIRUP → **temuan** (pelanggaran kewajiban pengumuman RUP). Ketidaksesuaian data RUP↔RKA/DIPA (nama/nilai/metode) → catatan.

| Aspek | Kriteria | Referensi |
|---|---|---|
| Seluruh paket pengadaan terdaftar & diumumkan di SIRUP | Tiap paket dalam populasi RKA/DIPA memiliki entri RUP yang **diumumkan** | **Perpres 16/2018 Pasal 22 ayat (1)–(3)** jo. **Pasal 23** |
| Kesesuaian data RUP ↔ RKA/DIPA | Nama/nilai/jenis/metode paket di SIRUP konsisten dengan RKA/DIPA | Perpres 16/2018 Pasal 22 |
| Ketepatan pengumuman RUP | RUP diumumkan setelah penetapan DIPA/alokasi anggaran | Perlem LKPP tentang SIRUP (mis. Perlem 11/2021) |

> Reviu kelengkapan SIRUP = **rekonsiliasi populasi ↔ pendaftaran**; keyakinan **terbatas**. Bila akses/penarikan data SIRUP terbaru diperlukan, penarikan dilakukan lewat skill/tooling data pengadaan (mis. `analisis-data-inaproc`), lalu hasilnya direkonsiliasi di sini.

### B. Kerangka Acuan Kerja / Spesifikasi Teknis

> **⚡ Kelengkapan justifikasi (wajib, jangan dilewati):** "lengkap" di sini = memuat **5 elemen** — (1) kebutuhan, (2) spesifikasi teknis & fungsi, (3) rencana cara/metode pengadaan, (4) waktu penyelesaian pekerjaan, (5) output yang diharapkan. Telusuri & nilai **per elemen** (lihat Checklist Kelengkapan Justifikasi di Analisis Substantif). Jangan menilai "lengkap/sesuai" secara global tanpa menelusuri kelimanya.

| Aspek | Kriteria | Referensi |
|-------|----------|-----------|
| KAK/spesifikasi ada dan **memuat 5 elemen justifikasi** | Ditetapkan PPK sebelum pengadaan; kebutuhan, spek teknis & fungsi, metode, waktu, output tercantum | Pasal 11 & 18 Perpres 16/2018 |
| Spesifikasi jelas dan terukur | Tidak ambigu, ada satuan/standar | Pasal 11 Perpres 16/2018 |
| Tidak diskriminatif (tidak menyebut merek) | Tidak membatasi persaingan | Pasal 19 Perpres 16/2018 |
| Sesuai kebutuhan (tidak over/under spec) | Proporsional terhadap kebutuhan | Prinsip efisiensi Pasal 6 |
| **Konsistensi internal** — nilai SLA/angka kinerja sama antarseksi | Latar Belakang = Persyaratan Teknis | Pasal 11 Perpres 16/2018 |
| **Konsistensi periode** — periode KAK sesuai pengadaan aktual | Tidak ada gap/inkonsistensi cakupan waktu | Pasal 11 Perpres 16/2018 |

> **⚡ Penting**: Pemeriksaan konsistensi internal KAK wajib dilakukan di setiap reviu — bandingkan nilai/angka yang sama di Latar Belakang, Persyaratan Teknis, dan Ketentuan Pelaksanaan. Temuan jenis ini sering terlewat karena hanya membaca satu bagian.

### C. Harga Perkiraan Sendiri (HPS)
| Aspek | Kriteria | Referensi |
|-------|----------|-----------|
| HPS ditetapkan PPK | Bukan oleh Pokja/pihak lain | Pasal 11 Perpres 16/2018 |
| Metodologi HPS terdokumentasi | Ada survei pasar/data dukung | Pasal 26 Perpres 16/2018 |
| HPS tidak melebihi pagu anggaran | HPS ≤ pagu | Pasal 26 Perpres 16/2018 |
| Dirahasiakan sampai evaluasi | Tidak bocor ke penawar | Pasal 26 Perpres 16/2018 |
| **HPS proporsional dengan periode aktual** | Nilai HPS sesuai durasi pengadaan yang sebenarnya | Pasal 26 Perpres 16/2018 |
| **Biaya migrasi/transisi tercantum** jika KAK mengharuskan | Semua komponen biaya wajib ada di HPS | Pasal 26 Perpres 16/2018 |

> **⚡ Penting**: Jika KAK menyebut ada proses migrasi, perpindahan penyedia, atau transisi sistem — **selalu cek apakah HPS mengakomodasi biaya tersebut**. Jika tidak ada, ini adalah temuan ketidaklengkapan komponen HPS.

### D. Rancangan Kontrak
| Aspek | Kriteria | Referensi |
|-------|----------|-----------|
| Jenis kontrak sesuai pekerjaan | Lumsum/harga satuan/terima jadi sesuai karakteristik | Pasal 27 Perpres 16/2018 |
| Klausul wajib ada | Jangka waktu, nilai, cara bayar, sanksi | Pasal 27 Perpres 16/2018 |
| Durasi tidak melewati tahun anggaran | Kecuali kontrak multi-tahun yg sudah disetujui | Pasal 27 Perpres 16/2018 |
| Jaminan pelaksanaan dipersyaratkan | Jika nilai >Rp200 juta (barang/konstruksi/jasa lain) | Pasal 33 Perpres 16/2018 |

### E. Metode Pemilihan dan Dokumen Pemilihan
| Aspek | Kriteria | Referensi |
|-------|----------|-----------|
| Metode pemilihan sesuai nilai/jenis | Threshold nilai per metode terpenuhi | Pasal 38-40 Perpres 16/2018 |
| Dokumen pemilihan ditetapkan Pokja | Bukan PPK yang menetapkan | Pasal 13 Perpres 16/2018 |
| Persyaratan kualifikasi proporsional | Tidak terlalu ketat sehingga membatasi persaingan | Pasal 19 Perpres 16/2018 |
| Jadwal pemilihan memadai | Waktu evaluasi cukup, sesuai regulasi | Perlem LKPP 12/2021 |

### F. Hasil Pemilihan

> ❌ **SKIP untuk Scope Perencanaan** — BAHP dan SPPBJ tidak diperiksa dalam reviu perencanaan.
> Aktifkan hanya jika scope mencakup pemilihan (lihat Scope Switch di atas).

| Aspek | Kriteria | Referensi |
|-------|----------|-----------|
| BA Evaluasi (BAHP) lengkap | Memuat evaluasi administrasi, teknis, harga | Perlem LKPP 12/2021 |
| Penetapan pemenang sesuai prosedur | Oleh Pokja (bukan PPK) untuk tender | Pasal 13 Perpres 16/2018 |
| Sanggah ditangani sesuai prosedur | Jika ada sanggah, ada BA penyelesaian | Pasal 51 Perpres 16/2018 |
| SPPBJ diterbitkan sebelum kontrak | Surat Penunjukan Penyedia ada | Pasal 11 Perpres 16/2018 |

## Format Unsur Temuan (KKSAR)

### Framework Elemen Isi

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Judul Temuan** | ✅ Wajib | Kalimat deskriptif menggambarkan kondisi: positif ("...telah sesuai") atau negatif ("...belum ditetapkan", "terdapat inkonsistensi...") |
| **Kondisi** | ✅ Wajib | Fakta administratif yang ditemukan — dokumen apa, bagian mana, isinya apa |
| **Kriteria** | ✅ Wajib | Pasal/ketentuan yang menjadi tolok ukur penilaian |
| **Sebab** | ✅ Diisi (anti-mengarang) | Diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab"/"Tidak cukup data". Jangan mengarang (lingkup reviu terbatas, jadi sering "tidak cukup data") |
| **Akibat** | ✅ Wajib | Konsekuensi/risiko jika kondisi tidak sesuai; jika sudah sesuai: nyatakan tidak ada dampak negatif |
| **Rekomendasi** | ✅ Jika ada catatan | Tindakan perbaikan konkret — siapa, apa, kapan. Boleh null jika kondisi sudah sesuai. **Disusun di LHR, bukan di KKP** |

**Bahasa keyakinan terbatas yang wajib digunakan di simpulan:**
> "Berdasarkan hasil reviu secara terbatas terhadap dokumen perencanaan dan pemilihan pengadaan, tidak terdapat hal-hal yang membuat kami yakin bahwa [aspek yang dinilai] tidak terpenuhi sesuai ketentuan."

Jika ada catatan:
> "Berdasarkan hasil reviu, masih ditemukan beberapa catatan yang perlu ditindaklanjuti, diantaranya: [daftar judul catatan]."

### Format Catatan Reviu (per aspek)

```
**CATATAN [NOMOR]  [JUDUL TEMUAN — kalimat deskriptif kondisi]**

Kondisi    : [Fakta yang ditemukan. Sebutkan: nama dokumen + bagian/halaman yang diperiksa.
              Jika sesuai: nyatakan bahwa persyaratan telah dipenuhi.
              Jika tidak sesuai: sebutkan apa yang kurang/tidak sesuai secara spesifik.]

Kriteria   : [Pasal/ketentuan yang menjadi acuan penilaian.
              Gunakan references/ untuk teks normatif yang tepat.]

Sebab      : [Akar penyebab bila terbukti dari dokumen; bila tidak → "Tidak ditemukan penyebab" /
              "Tidak cukup data". Jangan mengarang.]

Akibat     : [Konsekuensi/risiko dari kondisi yang ditemukan.
              Jika sesuai: "Tidak ditemukan dampak negatif dari aspek ini."
              Jika tidak sesuai: uraikan risiko operasional, hukum, atau keuangan yang ditimbulkan.]

Rekomendasi: [Tindakan perbaikan spesifik: apa yang harus dilengkapi/diperbaiki, oleh siapa, kapan.
              Disusun di LHR. Boleh kosong jika kondisi sudah sesuai ketentuan.]
```

**Panduan Judul Temuan:**
- Kondisi sesuai  → "...[Aspek] Telah Sesuai dengan Ketentuan" / "...[Aspek] Telah Memenuhi Persyaratan"
- Kondisi kurang  → "Terdapat [Masalah] pada [Aspek]" / "[Aspek] Belum [Memenuhi/Ditetapkan/Dilengkapi]"
- Tidak dapat dinilai → "[Aspek] Belum Dapat Dikonfirmasi/Dinilai karena [Alasan]"

## Format Output Laporan (LHR)

### Dokumen yang Dihasilkan:
1. **Nota Dinas Pengantar** (ikuti format panduan-format-umum)
2. **Laporan Hasil Reviu (LHR) Perencanaan dan Pemilihan Pengadaan**

### Struktur LHR Pengadaan:
```
A. PENDAHULUAN
   1. Latar Belakang
   2. Dasar Pelaksanaan (ST + ND permintaan jika ada)
   3. Tujuan dan Sasaran
   4. Ruang Lingkup
   5. Metodologi
   6. Jangka Waktu Pelaksanaan
   7. Komposisi Tim

B. GAMBARAN UMUM PAKET PENGADAAN
   [Nama paket, nomor RUP, nilai HPS, metode pemilihan, penyedia terpilih]

C. HASIL REVIU
   C.1. Perencanaan Pengadaan
        - Rencana Umum Pengadaan (RUP)
        - Kerangka Acuan Kerja / Spesifikasi Teknis
        - Harga Perkiraan Sendiri (HPS)
        - Rancangan Kontrak
   C.2. Pemilihan Penyedia
        - Dokumen Pemilihan
        - Proses Evaluasi
        - Penetapan Pemenang
   [Setiap catatan menggunakan format: Judul Temuan → Kondisi → Kriteria → Sebab → Akibat → Rekomendasi]

D. SIMPULAN
   [Pernyataan keyakinan terbatas, ringkasan status per aspek]

E. REKOMENDASI
   [Kompilasi semua rekomendasi dari bagian C, dengan penanggung jawab dan tenggat]

F. APRESIASI
   [Ucapan terima kasih atas kerjasama auditan]
```

## Referensi

> Reviu pengadaan menggunakan regulasi yang sama dengan audit, pemantauan, dan konsultasi pengadaan. Semua skill berbagi teks normatif yang ada di `skills/audit-pengadaan/references/`. Lihat `shared-pbj-references/PANDUAN.md` untuk panduan lengkap perbandingan 4 skill.

Lihat folder `references/` untuk panduan per aspek:
- `01-aspek-perencanaan.md` — ketentuan RUP, KAK, HPS
- `02-aspek-pemilihan.md` — ketentuan metode pemilihan, evaluasi, penetapan pemenang

Untuk teks lengkap peraturan, gunakan referensi bersama di `../audit-pengadaan/references/`:
- `01-perpres-16-2018.md` — pasal-pasal utama
- `02-perpres-12-2021.md` — perubahan threshold dan ketentuan
- `03-perlem-lkpp-12-2021.md` — prosedur teknis pemilihan

## Cara Membaca Dokumen

### Prioritas Baca (urutan):
1. **Konteks penugasan (dari INTEGRAL)** → Nomor ST, scope, paket yang direviu — **ST TIDAK di-upload**; metadata penugasan disuplai orkestrator via konteks/`sasaran-assignment.json`.
2. `03-perencanaan/` → TOR/KAK, RAB, HPS, rancangan kontrak
3. `02-kontrak/` → hanya bagian rancangan kontrak (sebelum penandatanganan)
4. `01-peraturan-internal/` → SOP internal jika ada
5. Dokumen pemilihan dan BAHP (jika tersedia di folder penugasan)

### Yang TIDAK perlu dibaca untuk reviu:
- Dokumen pelaksanaan fisik (04-pelaksanaan/)
- SPM/SP2D (05-keuangan/)
- Laporan progres pekerjaan

## Batasan
- **Sebab**: isi bila terbukti dari dokumen; bila tidak, tulis "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang. Reviu tidak melakukan investigasi mendalam atas penyebab, tetapi elemen Sebab tetap diisi.
- JANGAN menghitung kerugian negara — itu domain audit penuh.
- JANGAN menganalisis kualitas/hasil pelaksanaan fisik pekerjaan — itu domain audit-pengadaan (verifikasi output vs kontrak).
- JANGAN memperluas lingkup di luar yang ditetapkan ST; bila ada indikasi penyimpangan/kerugian → eskalasi ke KT untuk pertimbangan audit-pengadaan.

## Posisi dalam Keluarga Skill PBJ

> Semua skill PBJ (audit, reviu, pemantauan, konsultasi) menggunakan regulasi yang sama sebagai acuan. Yang membedakan adalah kedalaman pengujian, tujuan, dan format.

| | Audit | **Reviu** (skill ini) | Pemantauan | Konsultasi |
|---|---|---|---|---|
| Tingkat keyakinan | Memadai | **Terbatas** | Tidak ada | Tidak ada |
| Ruang lingkup | Seluruh siklus | **Perencanaan + pemilihan saja** | Pelaksanaan aktif saja | Sesuai pertanyaan |
| Pengujian bukti | Sangat mendalam | **Kesesuaian administratif dokumen** | Pelaporan status | Analisis regulasi |
| Sebab | ✅ Wajib (gali akar masalah) | **✅ Diisi (anti-mengarang)** | ✅ Diisi (anti-mengarang) | ❌ |
| Kerugian negara | ✅ Dihitung | **❌ Tidak dihitung** | ❌ | ❌ |
| Kapan digunakan | Pekerjaan selesai / isu serius | **Sebelum tender atau kontrak ditandatangani** | Selama kontrak berjalan | Pertanyaan teknis |

**Pilih reviu pengadaan (skill ini) ketika:**
- Dokumen perencanaan (KAK/HPS/RUP) sudah siap dan perlu diperiksa sebelum proses pengadaan berjalan
- Pimpinan membutuhkan keyakinan terbatas bahwa proses pemilihan telah sesuai ketentuan
- Penugasan bersifat preventif / quality assurance sebelum kontrak ditandatangani
- Diperlukan LHR (Laporan Hasil Reviu) sebagai output formal

**Jangan gunakan skill ini ketika:**
- Kontrak sudah ditandatangani dan pekerjaan sedang berjalan → gunakan **pemantauan-pengadaan**
- Ada indikasi penyimpangan atau kerugian negara → gunakan **audit-pengadaan**
- Unit kerja hanya butuh panduan/pendapat → gunakan **konsultasi-pengadaan**
