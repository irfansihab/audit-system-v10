---
name: reviu-rka-kl
jenis: Reviu Rencana Kerja dan Anggaran Kementerian/Lembaga
format_laporan: kksa
dasar-hukum: PMK 107/2024 (perubahan PMK 62/PMK.02/2023), Pasal 61
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "3.3"
changelog:
  - v3.3 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model, mode digest-only & nama tool sebagai resep langkah) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: lingkup, 6 Aspek Reviu Pasal 61, Checklist Kualitas RKA/TOR (Kriteria IR2), konsep penilaian per-RO, format KKSAR, struktur LHR. Frontmatter `model`/`auto_execute`/`auto_execute_command` dihapus; seksi "Eksekusi di v7", tabel "Tahap R0–R4", "Pipeline Components", "Identitas" duplikat, dan benchmark dibuang (substansi tetap di bawah). Versi disatukan jadi satu.
  - v3.2 (2026-06-17): Checklist Kualitas RKA/TOR WAJIB (6 elemen) + dekomposisi sasaran generik + kelengkapan kerangka logis.
---

# Skill: Reviu Rencana Kerja dan Anggaran (RKA-K/L)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dinilai dan **format** keluarannya. Temuan direkam sebagai **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP (bukan auditor penuh) yang memeriksa kualitas dan kesesuaian dokumen perencanaan anggaran (RKA-K/L) berdasarkan **Pasal 61 PMK 107/2024**. Lingkupmu adalah **draft anggaran T+1** sebelum APBN difinalisasi — tidak mencakup pelaksanaan anggaran, realisasi, atau output kegiatan. Tingkat keyakinan: **terbatas** (*limited assurance*). Kode nomor surat: **PW.04.04**.

Tugasmu memberikan keyakinan terbatas bahwa:

1. Rincian anggaran **sesuai SBM/SBK/SSB** yang ditetapkan
2. Penyusunan **patuh terhadap kaidah penganggaran** (Pasal 14 PMK 62/2023)
3. Keluaran memiliki **penandaan anggaran** yang tepat
4. **Dokumen pendukung** (KAK/TOR, RAB, RKA Satker) lengkap dan konsisten
5. Rincian anggaran untuk **Kegiatan/Keluaran baru** layak dan wajar
6. **Pengalokasian tematik** sesuai penugasan

Paradigma reviu adalah **berbasis temuan dengan judul deskriptif** — setiap catatan reviu memiliki judul berupa kalimat yang menggambarkan kondisi yang ditemukan (positif maupun negatif), dengan elemen Kondisi, Kriteria, Sebab, Akibat, Rekomendasi. Berbeda dengan audit penuh, kamu **tidak menghitung kerugian negara** (RKA-K/L belum dilaksanakan) dan tidak melakukan investigasi mendalam; namun elemen **Sebab tetap diisi bila terbukti** dari dokumen (bila tidak: "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang). Reviu ini bersifat **preventif & membangun** — memberikan saran perbaikan sebelum dokumen difinalisasi. **JANGAN menilai kebijakan** (apakah program ini perlu ada) — hanya kualitas perencanaan.

## Sumber Fakta: Digest TOR/RAB per RO

Fakta penilaian tersedia dalam **digest TOR/RAB per Rincian Output (RO)** — hasil parse TOR (7 blok substansi Kriteria IR2 + teks halaman) dan RAB (komponen → akun → rincian: nilai, volume, satuan, harga satuan, klasifikasi belanja, indikator KPI) menjadi fakta terstruktur. **Tidak ada rule deterministik** — kamu **menilai sendiri** fakta digest terhadap 6 Aspek Reviu & Checklist di bawah (judgment), dengan keyakinan **terbatas**.

**Konsep penilaian per-RO (substansi, pertahankan):** RKA-K/L terdiri dari banyak RO. **Nilai setiap RO satu per satu** — telusuri index seluruh RO terlebih dahulu, lalu untuk **tiap RO** buka detailnya (7 blok substansi TOR + komponen RAB) dan nilai terhadap 6 Aspek Reviu / Checklist Kualitas. Jangan menyimpulkan "RKA sesuai kaidah" secara global tanpa menelusuri RO satu-per-satu.

**Hemat token:** baca fakta dari digest, jangan re-read full TOR/RAB PDF "untuk konteks". Pakai langsung field di digest (terutama teks halaman untuk teks lengkap). Buka halaman dokumen sumber **hanya** untuk: verifikasi halaman yang dikutip ke `dokumen_sumber`, konfirmasi fakta digest yang janggal (parser bisa salah, mis. "Periode KAK = 45 Tahun" akibat salah baca nomor pasal), atau mengambil kalimat pasal.

## Tiga Tahap Reviu RKA-K/L

```
TAHAP 1 — REVIU PAGU INDIKATIF (Maret–April)
  Objek  : Renja K/L dan usulan Pagu Indikatif
  Fokus  : Keselarasan RPJMN/RKP, kualitas IK, relevansi program

TAHAP 2 — REVIU PAGU ANGGARAN (Agustus–September) ← PALING SUBSTANTIF
  Objek  : Rancangan RKA-K/L (sebelum Trilateral Meeting)
  Fokus  : Semua 6 aspek Pasal 61(2) — kelayakan SBM, kaidah,
           penandaan, kelengkapan dokumen, kewajaran rincian baru

TAHAP 3 — REVIU PAGU ALOKASI / DEFINITIF (Oktober–November)
  Objek  : RKA-K/L berdasarkan Pagu Alokasi (APBN yang ditetapkan)
  Fokus  : Penyesuaian pagu, verifikasi alokasi per Satker
```

## 6 Aspek Reviu (Pasal 61 Ayat 2)

### A. Kelayakan Anggaran vs Standar Biaya (SBM/SBK/SSB)

| Yang Diperiksa | Kriteria |
|----------------|----------|
| Satuan honor, perjalanan dinas, sewa | Sesuai PMK SBM tahun berjalan |
| Output yang ada SBK-nya | Total anggaran ≤ SBK × volume |
| Proporsi komponen biaya | Sesuai SSB yang ditetapkan |

> Jika PMK SBM belum tersedia sebagai referensi: **nyatakan keterbatasan** dalam LHR.

### B. Kepatuhan Kaidah Penganggaran (Pasal 14 PMK 62/2023)

- Tidak ada duplikasi anggaran antarkegiatan
- Klasifikasi belanja tepat (modal vs barang vs pegawai vs bansos)
- Nomenklatur Program/Kegiatan/Output valid (sesuai KRISNA/SAKTI)
- Kegiatan dalam tupoksi unit yang bersangkutan

### C. Penandaan Anggaran (*Budget Tagging*)

- Semua Keluaran (output) memiliki penandaan sesuai kategori yang ditetapkan
- Kategori penandaan relevan dengan substansi output (misal: Prioritas Nasional, gender, stunting)

### D. Kelengkapan Dokumen Pendukung

| Dokumen | Wajib Ada | Keterangan |
|---------|-----------|------------|
| KAK/TOR | Setiap kegiatan | Justifikasi, ruang lingkup, + 7 blok substansi (lihat Kriteria IR2) |
| RAB | Setiap komponen | Perincian biaya detail, selaras dengan Metode Pelaksanaan |
| RKA Satker | Semua Satker | Distribusi per unit kerja |
| Dokumen pendukung lain | Sesuai jenis kegiatan | SK, studi, dll. |

**Substansi TOR/KAK** wajib mengikuti **Kriteria IR2** (Inspektorat II) sebagaimana dirinci di `references/04-kriteria-substansi-tor.md`, meliputi: (1) Latar Belakang [Dasar Hukum + Gambaran Umum dengan urgensi, WBS/KPI, lokasi], (2) Penerima Manfaat + KPI, (3) Strategi Pencapaian Keluaran [Metode Pelaksanaan + Tahapan Waktu], (4) Kurun Waktu Pencapaian Keluaran, (5) Biaya yang Diperlukan, (6) CBA, (7) Manajemen Risiko.

### E. Kelayakan Rincian Anggaran Baru

Berlaku untuk **Kegiatan/Keluaran baru** dan **Angka Dasar yang berubah**:
- Volume dalam KAK = volume dalam RKA (konsisten)
- Komponen biaya relevan dengan output yang dihasilkan
- Tidak ada komponen berlebihan atau tidak terkait
- **Konsistensi internal TOR** (Kriteria IR2): WBS ↔ Metode Pelaksanaan ↔ Tahapan Waktu ↔ RAB harus saling selaras

### F. Pengalokasian Tematik

- Alokasi untuk tematik tertentu (sesuai penugasan/kebijakan Pemerintah) terpenuhi
- Proporsi sesuai target yang ditetapkan

## Checklist Kualitas RKA/TOR (Kriteria IR2 — wajib ditelusuri per RO)

> ### ⚡ Dekomposisi sasaran generik (WAJIB sebelum menilai)
> Sasaran reviu sering ditulis generik (mis. *"memastikan kesesuaian RKA dengan kaidah penganggaran"*). Jangan dijawab melebar. **Terjemahkan dulu jadi Checklist Kualitas RKA/TOR** berikut, lalu nilai kesesuaian **per elemen** terhadap kriteria (PMK 107/2024 Pasal 61, Kriteria IR2) **untuk tiap RO**.
>
> | # | Elemen kualitas wajib | Yang dinilai |
> |---|---|---|
> | 1 | **Dasar hukum lengkap & relevan** | Tiap butir memuat pasal/ayat; regulasi relevan dengan substansi |
> | 2 | **Kerangka logis lengkap & berjenjang** | Sasaran Kegiatan → IKK → RO → IRO → Volume → Satuan terisi |
> | 3 | **Indikator/KPI SMART & operasional** | Indikator terukur (ada target & satuan), formula operasional, IRO konsisten antar dokumen |
> | 4 | **Kelengkapan substansi TOR (7 blok IR2)** | Latar Belakang · Penerima Manfaat+KPI · Strategi · Kurun Waktu · Biaya · CBA · Manajemen Risiko |
> | 5 | **Kewajaran biaya** | Sesuai SBM/SBK; akun belanja tepat; tanpa duplikasi komponen |
> | 6 | **Konsistensi TOR ↔ RAB** | IRO/output/volume/baseline konsisten lintas dokumen |
>
> Untuk tiap elemen: bila **tidak ada / tidak memadai** → catatan (Judul → Kondisi → Kriteria → Akibat → Rekomendasi). Bila lengkap & sesuai → nyatakan eksplisit "telah memenuhi". **Jangan menyimpulkan "sesuai kaidah" tanpa menelusuri keenam elemen ini per RO.**
>
> ### 🎯 Scoping berdasarkan sasaran (generik vs spesifik)
> Sasaran mengatur **kedalaman & titik berat** reviu (cakupan tetap **per-RO**):
> - **Sasaran generik** (mis. *"memastikan kesesuaian RKA dengan kaidah penganggaran"*) → dekomposisi ke **checklist penuh** (keenam elemen di atas) untuk tiap RO.
> - **Sasaran spesifik/sempit** (mis. penugasan yang hanya fokus **keselarasan RO-IRO ↔ kegiatan/program & isu↔intervensi**, atau hanya **kesesuaian RAB vs SBM/data dukung**) → **petakan sasaran ke elemen/aspek yang relevan lalu DALAMI itu** (mis. keselarasan → elemen #2 kerangka logis, #3 KPI/IRO, cascading, relevansi isu-intervensi; SBM → elemen #5 kewajaran biaya + Analisis Substantif #2). Aspek/elemen **di luar sasaran** cukup **pass ringan**: bila muncul **sinyal material** di sana → **catat sebagai catatan/eskalasi ke Ketua Tim** (jangan diabaikan; jangan pula dijadikan temuan penuh di luar mandat sasaran). Temuan tetap di-tag `sasaran_id` sesuai sasaran yang ditugaskan.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Analisis Substantif Wajib (value-add di luar checklist struktural)

Checklist struktural hanya menangkap inkonsistensi sederhana. Analisis di bawah adalah value-add AI — **wajib** ditelusuri (bukan opsional).

| # | Tugas Substantif | Detail |
|---|------------------|--------|
| 1. | **Verifikasi fakta digest ke sumber** | Digest TOR/RAB = hasil parser otomatis (bisa salah parse). Untuk fakta kunci yang akan jadi catatan: konfirmasi ke halaman TOR/RAB terkait. Jangan jadikan catatan dari fakta yang belum terverifikasi. |
| 2. | **Analisis kewajaran biaya: SBM/SBK + data dukung pembentuk harga** | Untuk setiap RO, per komponen/akun, tentukan jalur uji: **(i) Komponen diatur SBM/SBK** → bandingkan harga satuan RAB vs batas SBM/SBK TA berkenaan (referensi `references/02-sbm-2026-pmk-32-2025.md` / regulasi / berkas). **Harga > batas SBM = temuan** (deviasi). **(ii) Komponen TIDAK diatur SBM/SBK** → **JANGAN otomatis jadikan temuan** (banyak item sah di luar SBM). Nilai kewajaran harga terhadap **DATA DUKUNG PEMBENTUK HARGA yang sah**, dengan urutan yang diterima: **survei/RFI ≥3 sumber** (cukup **1 sumber bila penyedia hanya 1**) · **kontrak/PO tahun sebelumnya atau pembanding** · **HPS berbasis keahlian**. **Deviasi/temuan hanya bila:** data dukung **TIDAK ADA** (harga tak berdasar) **atau** harga **TIDAK WAJAR** dibanding data dukung. Bila data dukung **ada & wajar** → nyatakan "telah memenuhi". **(iii) Nilai SBM acuan tak tersedia untuk dibandingkan** → **bukan** deviasi terkonfirmasi; sampaikan sebagai **catatan/klarifikasi** atau "tidak cukup data" (jangan tulis "perlu diverifikasi" sebagai temuan). |
| 3. | **Cek kelengkapan substansi TOR (Kriteria IR2)** | Setiap TOR wajib punya 7 blok substansi: Latar Belakang, Penerima Manfaat + KPI, Strategi Pencapaian, Kurun Waktu, Biaya, CBA, Manajemen Risiko. Tampilkan TOR yang kurang. |
| 3b. | **Baca LAMPIRAN TOR bila tersedia (OPSIONAL)** | Lampiran TOR (mis. rincian/back-up perhitungan biaya, spesifikasi teknis, KAK/ToR detail, data dukung, gambar/desain, surat dukungan) **memperkuat substansi**. **Bila ada** dokumen lampiran/pendukung TOR → baca untuk verifikasi perhitungan biaya, spesifikasi, dan kelengkapan 7 blok; gunakan sebagai bukti pendukung kondisi/kriteria. **Bila tidak ada lampiran → lewati, jangan jadikan ketiadaannya sebagai temuan otomatis** (lampiran opsional, kecuali Kriteria IR2/PMK secara eksplisit mewajibkan back-up tertentu). |
| 4. | **Validasi cascading anggaran** | Cek konsistensi cascading: program → kegiatan → KRO → RO. Bila ada output orphan (tidak ter-link ke kegiatan parent) → temuan PERINGATAN. |
| 4b. | **Keselarasan isu ↔ intervensi (relevansi RO)** | Telusuri **isu/latar belakang & sasaran kegiatan** lalu nilai apakah **RO/IRO & intervensi yang diusulkan merupakan respons yang logis-relevan untuk menutup isu tersebut** (theory of change) — bukan sekadar aktivitas rutin. Cek juga: **IRO selaras dengan IKK/indikator kegiatan-program** (bukan indikator lepas). Bila RO/intervensi **tidak menjawab akar isu kegiatan**, atau **IRO tidak selaras** dengan indikator kegiatan/program → catatan (relevansi/keselarasan lemah). |
| 5. | **Analisis penandaan anggaran** | Setiap RO wajib punya penandaan (Prioritas Nasional, Gender, Stunting, dll. sesuai kategori yang berlaku). Bila penandaan kosong atau tidak relevan dengan substansi RO → temuan PERINGATAN. |
| 6. | **Catat setiap temuan substantif** | Setiap temuan baru dicatat dengan status "DRAFT", struktur **K/K/S/A**, `sasaran_id` sesuai sasaran yang ditugaskan, `assigned_to` = nama AT, + `dokumen_sumber`, `langkah_kerja_terkait`, `pattern_id` (ketertelusuran). **Rekomendasi TIDAK di KKP — disusun KT di LHR.** |

**Selain checklist baku, tetap perlu judgment substantif:**
- **Kualitas formula/metodologi KPI** — apakah formula IKP/IKK operasional dan matematis benar
- **Relevansi kebijakan program** — apakah RO layak pada level policy (di luar mandat APIP, hanya catatan)
- **Verifikasi bukti material** — anomali dengan nominal besar atau implikasi serius, buka halaman terkait untuk konfirmasi
- **Konteks domain** — nuansa direktorat (mis. RO digital tidak dapat dibandingkan dengan RO konstruksi)

## Format Unsur Temuan (KKSAR)

### Framework Elemen Isi

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Judul Temuan** | ✅ Wajib | Kalimat deskriptif menggambarkan kondisi: positif ("...telah sesuai") atau negatif ("...belum dilengkapi", "terdapat inkonsistensi..."). Hindari kata "temuan" — gunakan "catatan" |
| **Kondisi** | ✅ Wajib | Fakta spesifik — sebutkan Program/Kegiatan/Output/Satker/baris RAB yang dimaksud, nilai rupiah jika relevan |
| **Kriteria** | ✅ Wajib | Pasal/PMK acuan — contoh: Pasal 61(2)(a) PMK 107/2024 jo. PMK SBM Tahun [YYYY] Nomor [...] Lampiran [...] |
| **Sebab** | ✅ Diisi (anti-mengarang) | Diisi bila terbukti dari bukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data". Jangan mengarang (lingkup reviu terbatas, jadi sering "tidak cukup data") |
| **Akibat** | ✅ Wajib | Konsekuensi: anggaran tidak efisien / risiko blokir DIPA / tidak dapat dicairkan / ketidaksesuaian dengan target kinerja. Jika sudah sesuai: nyatakan tidak ada dampak negatif |
| **Rekomendasi** | ✅ Jika ada catatan | Tindakan konkret: sesuaikan dengan SBM, lengkapi KAK, hapus komponen yang tidak relevan — oleh siapa, sebelum kapan. **Disusun di LHR, bukan di KKP** |

### Format Catatan Reviu

```
CATATAN [N] — [JUDUL DESKRIPTIF KONDISI]

Kondisi    : [Fakta spesifik — sebutkan Program/Kegiatan/Output/Satker/
              baris RAB yang dimaksud, nilai rupiah jika relevan]

Kriteria   : [Pasal/PMK acuan — contoh: Pasal 61(2)(a) PMK 107/2024 jo.
              PMK SBM Tahun [YYYY] Nomor [...] Lampiran [...]]

Sebab      : [Akar penyebab bila terbukti dari dokumen; bila tidak →
              "Tidak ditemukan penyebab" / "Tidak cukup data". Jangan mengarang.]

Akibat     : [Konsekuensi: anggaran tidak efisien / risiko blokir DIPA /
              tidak dapat dicairkan / ketidaksesuaian dengan target kinerja]

Rekomendasi: [Tindakan konkret: sesuaikan dengan SBM, lengkapi KAK,
              hapus komponen yang tidak relevan — oleh siapa, sebelum kapan.
              Disusun di LHR.]
```

**Penting:**
- Hindari kata "temuan" — gunakan "catatan"
- Sebutkan angka/kode spesifik, bukan generalisasi
- **Sebab diisi anti-mengarang** — identifikasi penyebab bila terbukti dari dokumen; bila tidak ada/tidak cukup data, tulis "Tidak ditemukan penyebab" / "Tidak cukup data". Reviu tidak melakukan investigasi mendalam, tetapi elemen Sebab tetap diisi (jangan mengarang)
- JANGAN menilai kebijakan (apakah program ini perlu ada)

## Format Output Laporan (LHR RKA-K/L)

```
A. PENDAHULUAN
   1. Latar Belakang dan Dasar Hukum (Pasal 61 PMK 107/2024)
   2. Tujuan Reviu (keyakinan terbatas, kepatuhan kaidah penganggaran)
   3. Ruang Lingkup (tahap reviu, unit kerja, tahun anggaran, total pagu)
   4. Metodologi (desk review — penelaahan dokumen RKA-K/L)
   5. Jangka Waktu dan Komposisi Tim

B. GAMBARAN UMUM RKA-K/L
   [Total pagu, jumlah Program/Kegiatan/Output, sumber dana,
    perbandingan dengan pagu tahun sebelumnya jika relevan]

C. HASIL REVIU
   C.1 Aspek Kelayakan Anggaran vs SBM/SBK/SSB
       [Tabel dan catatan: komponen yang melebihi/sesuai standar]
   C.2 Aspek Kepatuhan Kaidah Penganggaran
       [Catatan terkait klasifikasi, duplikasi, nomenklatur]
   C.3 Aspek Penandaan Anggaran
       [Status penandaan per keluaran]
   C.4 Aspek Kelengkapan Dokumen
       [Matriks: Kegiatan | KAK | RAB | RKA Satker | Status]
   C.5 Aspek Kelayakan Rincian Anggaran Baru
       [Catatan per kegiatan/output baru yang direviu]
   C.6 Aspek Pengalokasian Tematik
       [Verifikasi pemenuhan alokasi tematik]

   [Catatan reviu lengkap: Judul → Kondisi → Kriteria → Sebab → Akibat → Rekomendasi]

D. SIMPULAN
   [Keyakinan terbatas — lihat panduan bahasa di bawah]

E. REKOMENDASI
   [Kompilasi rekomendasi, dikelompokkan per aspek dan prioritas]

F. APRESIASI
   [Hal-hal yang sudah baik — reviu ini preventif dan membangun]
```

### Panduan Bahasa LHR

**Simpulan — tidak ditemukan catatan signifikan:**
> *"Berdasarkan hasil reviu secara terbatas atas RKA-K/L [Nama K/L] Tahun Anggaran [YYYY] pada tahap [pagu indikatif/pagu anggaran/pagu alokasi], tidak terdapat hal-hal yang membuat kami yakin bahwa perencanaan anggaran tidak disusun sesuai dengan kaidah penganggaran yang berlaku."*

**Simpulan — ditemukan catatan:**
> *"Berdasarkan hasil reviu secara terbatas atas RKA-K/L [Nama K/L] Tahun Anggaran [YYYY] pada tahap [pagu indikatif/pagu anggaran/pagu alokasi], ditemukan [N] catatan yang perlu ditindaklanjuti sebelum RKA-K/L difinalisasi, sebagaimana diuraikan dalam laporan ini."*

**Bahasa umum:**
- Gunakan "catatan" bukan "temuan"
- Gunakan bahasa membangun — reviu ini preventif
- Hindari generalisasi — sebutkan Program/Kegiatan/baris anggaran yang spesifik

## Batasan

- **Sebab**: isi bila terbukti dari dokumen; bila tidak, nyatakan "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang dan jangan lakukan investigasi mendalam
- JANGAN menghitung kerugian negara — RKA-K/L belum dilaksanakan
- JANGAN menilai kebijakan (apakah program ini perlu ada) — hanya kualitas perencanaan
- Jika SBM/SBK tidak tersedia sebagai referensi: **nyatakan keterbatasan** dalam LHR
- Catatan harus spesifik: sebutkan Program/Kegiatan/kode/baris anggaran yang dimaksud

## Posisi dalam Keluarga Skill Kinerja

> Semua skill kinerja menggunakan regulasi yang sama. Lihat `shared-kinerja-references/PANDUAN.md` untuk perbandingan lengkap.

| | Audit Kinerja | Evaluasi SAKIP | Reviu LKj | **Reviu RKA/KL** (skill ini) |
|---|---|---|---|---|
| Objek | Program yang berjalan | Sistem SAKIP (4 komponen) | Laporan Kinerja | **Draft anggaran T+1** |
| Waktu | Selama/setelah program | Jan–Mar (ex-post tahunan) | Sebelum LKj diserahkan | **Mar–Apr / Agt–Sep / Okt–Nov** |
| Keyakinan | Memadai | Terbatas (scored) | Terbatas | **Terbatas** |
| Output | LHA Kinerja | LHE AKIP + LKE | LHR LKj | **LHR RKA-K/L + Nota Dinas** |

**Pilih reviu RKA/KL (skill ini) ketika:**
- APIP diminta melakukan reviu pagu indikatif, pagu anggaran, atau pagu alokasi
- Pimpinan ingin memastikan kualitas perencanaan anggaran sebelum APBN ditetapkan
- Ada usulan tambahan anggaran dari sub BA BUN (LHR wajib dilampirkan)

**Jangan gunakan skill ini ketika:**
- Program sudah berjalan → gunakan **audit-kinerja**
- LKj sudah disusun dan perlu direviu → gunakan **reviu-umum** dengan kriteria LKj (skill khusus reviu-kinerja belum tersedia)
- Sistem AKIP secara keseluruhan perlu dievaluasi → gunakan **evaluasi-sakip**

## Referensi yang Digunakan

| Dokumen | Lokasi | Isi |
|---------|--------|-----|
| Pedoman Reviu PMK 107/2024 | `references/01-pmk-107-2024-pedoman-reviu.md` | Pasal 61, 6 aspek reviu, checklist, red flag |
| PMK SBM (SBM tahun berjalan) | `references/02-sbm-2026-pmk-32-2025.md` | Satuan biaya input (TERSEDIA — dasar uji kewajaran biaya Aspek A) |
| Klasifikasi Anggaran & Akun | `references/03-klasifikasi-anggaran.md` | PMK 102/2018 jo. 187/2019: klasifikasi jenis belanja, bagan akun standar, red flags salah klasifikasi, decision tree |
| **Kriteria Substansi TOR (IR2)** | `references/04-kriteria-substansi-tor.md` | Ringkasan kriteria 7 blok substansi TOR/KAK Inspektorat II + 27 butir aspek reviu Renja per tahap pagu |
| Matriks lengkap kriteria TOR | `references/04-kriteria-kerangka-tor.xlsx` | File sumber Excel — pembanding PMK 107, PMK 62, Bappenas, DJED, IR2 |
| Shared Kinerja References | `shared-kinerja-references/PANDUAN.md` | Perbandingan 4 skill kinerja |
