---
name: pemantauan-tindak-lanjut
jenis: Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)
format_laporan: kksa
dasar-hukum: PP 60/2008 Pasal 50, Standar Audit Intern Pemerintah Indonesia (SAIPI/AAIPI 2021)
kode-surat: PW.04.06
tingkat-keyakinan: tidak-ada
version: "0.3"
changelog:
  - v0.3 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Frontmatter `model`/`output`/`status` dihapus; seksi "Eksekusi di v7", tabel "Tahap P0–P4" + kolom Pelaku, seksi Identitas, dan resep nama tool v7 dibuang (substansi status TL dipertahankan utuh).
  - v0.2 (2026-06-17): Refactor orkestrasi P0–P4 seragam (legacy v7).
  - v0.1 (2026-04-19): Skeleton (upgrade sistem v2.8).
---

# Skill: Pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill ini menetapkan **APA** yang dinilai dan **FORMAT** keluarannya. Catatan direkam K/K/S/A; Rekomendasi disusun di laporan, bukan di KKP.

## Lingkup & Paradigma

Kamu memantau **status tindak lanjut (TL) rekomendasi** pengawasan eksternal (BPK) dan internal (BPKP, Itjen) — apakah ditindaklanjuti **tepat waktu dan tepat substansi** oleh unit kerja Kemkomdigi.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

Paradigma = **monitoring, bukan assurance**. Kamu **tidak memberi keyakinan** atas pengelolaan auditi; kamu mencatat **status TL apa adanya** berdasarkan bukti tindak lanjut yang diserahkan unit kerja. Pemantauan **tidak menghitung kerugian negara** dan tidak melakukan investigasi mendalam. Kode nomor surat: **PW.06**.

**Inti khas skill ini = pelacakan status TL per rekomendasi (matriks status TL), BUKAN tabel temuan KKSA biasa.** Artefak utama bukan "temuan", melainkan **matriks status** tiap rekomendasi (Tuntas/Dalam Proses/Belum/Tidak Dapat Ditindaklanjuti) plus analisis umur (aging). Bila perlu membuat catatan KKSA atas suatu kondisi pemantauan (mis. pola TL macet), **elemen Sebab diisi anti-mengarang** (lihat Batasan) — tetapi **jangan paksakan struktur KKSA penuh ke matriks status TL**; matriks adalah artefak tersendiri.

## Sumber Fakta

- **Daftar rekomendasi** yang dipantau (asal LHP/CHR sebelumnya, nomor rekomendasi, substansi, PIC, deadline, tanggal terbit LHP).
- **Bukti tindak lanjut** per rekomendasi (surat, dokumen pelaksanaan, SK, bukti perbaikan) yang diserahkan unit kerja.
- **Database/rekap TLHP** internal Itjen bila tersedia; bila tidak, rekap manual atau ekstrak rekomendasi dari berkas LHP.

**Anti-halusinasi:** setiap status TL harus mengutip **nama file bukti** (atau dinyatakan eksplisit "tidak ada file bukti"). Jangan menyimpulkan "Tuntas" tanpa bukti yang menutup seluruh item rekomendasi.

## Matriks Status Tindak Lanjut (artefak utama — pertahankan apa adanya)

Untuk SETIAP rekomendasi yang dipantau, isi baris matriks berikut:

| No | Asal LHP | No Rek | Substansi Rekomendasi | PIC | Deadline | Status TL | Umur (hari) | Bukti / Keterangan |
|----|----------|--------|-----------------------|-----|----------|-----------|-------------|--------------------|

### Kriteria Status TL (klasifikasi wajib)

- **Tuntas (Selesai)** — bukti tindak lanjut **lengkap dan memadai**, menutup **seluruh** item rekomendasi → rekomendasi ditutup.
- **Dalam Proses** — ada tindak lanjut **parsial** (≥1 bukti relevan & substansial), belum menutup seluruh item → perlu pendalaman.
- **Belum Ditindaklanjuti** — **tidak ada** bukti tindak lanjut.
- **Tidak Dapat Ditindaklanjuti** — ada **justifikasi kuat** mengapa rekomendasi tidak relevan lagi (mis. unit/program dibubarkan, dasar berubah); umumnya perlu SK penghapusan/penetapan.

### Analisis Umur (Aging)

**Umur (hari)** = jumlah hari sejak **tanggal terbit LHP** sampai **tanggal cut-off pemantauan**. Klasifikasikan ke kategori:

- 0–90 hari: 🟢 hijau
- 91–180 hari: 🟡 kuning
- 181–365 hari: 🟠 oranye
- >365 hari: 🔴 merah (kritis — wajib perhatian pimpinan/Menteri)

**Agregasi per PIC** (unit kerja):
```
PIC: [Unit Kerja]
  Total rekomendasi: [n]
  Tuntas: [n]   Dalam Proses: [n]   Belum: [n] (merah: [n], oranye: [n], kuning: [n])
  Tidak Dapat Ditindaklanjuti: [n]
  Aging rata-rata yang belum selesai: [hari]
```

**Daftar Rekomendasi Kritis** — rekomendasi dengan **umur >365 hari DAN status ≠ Tuntas** otomatis naik ke daftar kritis yang disorot di laporan + ringkasan eksekutif untuk pimpinan.

## Catatan Pemantauan (bila perlu KKSA — Sebab anti-mengarang)

Bila kondisi pemantauan perlu ditarik menjadi catatan formal (mis. pola TL macet berulang, rekomendasi kritis terbengkalai, justifikasi "Tidak Dapat Ditindaklanjuti" yang lemah), susun catatan dengan elemen **K/K/S/A** — **tanpa memaksakan ke matriks status TL** (matriks tetap artefak terpisah di atas):

| Elemen | Catatan |
|--------|---------|
| **Judul** | Kalimat deskriptif kondisi pemantauan (mis. "Sebagian rekomendasi BPK belum ditindaklanjuti melewati batas waktu") |
| **Kondisi** | Fakta status TL — runtutan: asal LHP, nomor rekomendasi, deadline, bukti yang ada/tidak ada, umur; lalu tunjukkan deviasinya |
| **Kriteria** | Kewajiban TLHP — PP 60/2008 Pasal 50, Standar Audit Intern Pemerintah Indonesia (SAIPI/AAIPI 2021), atau ketentuan TLHP terkait |
| **Sebab** | Diisi **bila terbukti** dari bukti (mis. penyebab keterlambatan TL). Bila tidak ditemukan / bukti tidak cukup → tulis EKSPLISIT "Tidak ditemukan penyebab" / "Tidak cukup data". **Jangan mengarang.** |
| **Akibat** | Risiko bila TL tidak dipercepat (mis. temuan berulang, akuntabilitas menurun) |
| **Rekomendasi** | Tindakan percepatan — **disusun di laporan, bukan di KKP** |

## Format Output Laporan

Struktur **Laporan Hasil Pemantauan TLHP** (ikuti panduan-format-umum untuk kop/Nota Dinas):

1. **Ringkasan Eksekutif** (1 halaman — untuk Menteri/Sekjen)
2. **Statistik Umum** — total rekomendasi, % Tuntas, distribusi per sumber (BPK/BPKP/APIP)
3. **Aging per PIC** — tabel + ranking unit dengan TL terlemah
4. **Daftar Rekomendasi Kritis** (umur >365 hari, status ≠ Tuntas)
5. **Rekomendasi Percepatan**
6. **Lampiran** — matriks status TL lengkap (Excel terpisah)

## Referensi

Kriteria kewajiban tindak lanjut hasil pengawasan: **PP 60/2008 Pasal 50** (kewajiban pimpinan instansi menindaklanjuti rekomendasi APIP) dan **Standar Audit Intern Pemerintah Indonesia (SAIPI/AAIPI 2021)** — bagian pemantauan tindak lanjut hasil audit; lihat frontmatter `dasar-hukum`. Klasifikasi status TL (Tuntas / Dalam Proses / Belum Ditindaklanjuti / Tidak Dapat Ditindaklanjuti) dan aging mengikuti definisi pada bagian pemantauan di atas. Format kop/Nota Dinas & struktur laporan mengikuti `../panduan-format-umum/PANDUAN.md`; matriks status TL lengkap dihasilkan sebagai lampiran Excel.

## Batasan

- **Monitoring, bukan assurance** — tingkat keyakinan: **tidak ada**. Catat status apa adanya berdasarkan bukti.
- **Sebab anti-mengarang** — saat membuat catatan KKSA, isi Sebab bila terbukti; bila tidak → "Tidak ditemukan penyebab" / "Tidak cukup data". Jangan mengarang.
- **JANGAN menghitung kerugian negara** — itu domain audit.
- **JANGAN memaksakan struktur KKSA penuh ke matriks status TL** — matriks status TL adalah artefak khas pemantauan, bukan tabel temuan.
- Setiap status TL **wajib** mengutip nama file bukti (atau "tidak ada file").

## Integrasi dengan Skill Lain

- **evaluasi-spip**: data TLHP bisa jadi bukti dukung Komponen IV (Informasi-Komunikasi) & V (Pemantauan).
- **evaluasi-sakip**: persentase penyelesaian TLHP dirujuk Komponen Evaluasi Akuntabilitas Internal.
- **audit-kinerja**: temuan berulang dari TLHP bisa jadi input Hipotesis Audit Awal di Memo SP.

## Posisi dalam Keluarga Skill

| | Audit | Reviu | **Pemantauan TL** (skill ini) | Konsultansi |
|---|---|---|---|---|
| Tingkat keyakinan | Memadai | Terbatas | **Tidak ada (monitoring)** | Tidak ada |
| Fokus | Seluruh siklus, gali akar | Kesesuaian administratif | **Status TL rekomendasi (matriks status)** | Sesuai pertanyaan |
| Artefak utama | Temuan KKSA | Catatan reviu KKSA | **Matriks status TL + aging** | Pendapat/Saran |
| Sebab | ✅ Wajib (akar) | ✅ Diisi (anti-mengarang) | **✅ Diisi bila buat catatan KKSA (anti-mengarang)** | ❌ |
| Kerugian negara | ✅ Dihitung | ❌ | **❌** | ❌ |

**Pilih pemantauan-tindak-lanjut ketika:** perlu melacak status penyelesaian rekomendasi LHP/CHR sebelumnya (BPK/BPKP/Itjen) secara periodik dan menyusun laporan status TL untuk pimpinan.

**Jangan gunakan ketika:** perlu menguji substansi pengelolaan baru (→ audit/reviu/evaluasi sesuai jenis) atau perlu memberi keyakinan/assurance (pemantauan tidak memberi keyakinan).
