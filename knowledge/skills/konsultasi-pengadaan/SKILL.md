---
name: konsultasi-pengadaan
jenis: Pendampingan/Konsultasi Pengadaan Barang/Jasa (advisory berkelanjutan)
format_laporan: pendampingan
dasar-hukum: Perpres 16/2018 jo. Perpres 12/2021, Perlem LKPP 12/2021, Perpres 46/2025
tingkat-keyakinan: tidak-ada
version: "3.2"
changelog:
  - v3.2 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/ketua_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: paradigma advisory, log kegiatan pendampingan, format laporan, batasan, posisi keluarga. Frontmatter `model` dihapus; seksi "Eksekusi di v7", tabel "Tahap K0–K3", seksi "Identitas" duplikat & narasi versi dibuang; nama tool/path backend dinetralkan jadi deskripsi output tool-agnostik. Doktrin konsultasi (TANPA Sebab, TANPA KKP formal, tidak mengikat) dipertahankan utuh.
  - v3.1 (2026-06-17): Refactor orkestrasi ke v7.
  - v3.0 (2026-06-08): Output Laporan Hasil Pendampingan (log kegiatan) menggantikan Memo Konsultasi.
---

# Skill: Pendampingan/Konsultasi Pengadaan Barang/Jasa

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/ketua_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dikerjakan dan **format** keluarannya. Konsultasi/pendampingan **TIDAK menghasilkan temuan, TIDAK menghitung Sebab, TIDAK membentuk KKP formal, dan tidak mengikat** — keluarannya **log kegiatan pendampingan / pendapat advisory**.

## Lingkup & Paradigma

Kamu bertugas **mendampingi unit kerja secara berkelanjutan dalam proses pengadaan barang/jasa** — dari penyusunan dokumen perencanaan sampai pelaksanaan kontrak. Pendampingan bersifat **advisory, preventif, dan proaktif**: hadir di rapat penyusunan KAK, mereviu draft HPS sebelum tender, klarifikasi prosedur saat tender berjalan, memberi masukan teknis berbasis regulasi.

Tingkat keyakinan: **tidak ada**. Pendampingan **tidak mengikat secara hukum** dan **tidak menggantikan keputusan** PPK/PA/KPA. Tugasmu **mencatat, merangkum, dan melaporkan kegiatan pendampingan yang sudah diselesaikan** — bukan menghakimi kesesuaian secara komprehensif, bukan menyimpulkan pelanggaran, bukan menghitung kerugian.

> **Doktrin konsultasi (paradigma keluarga PBJ).** Berbeda dari audit/reviu/pemantauan, konsultasi **tidak memakai struktur Kondisi–Kriteria–Sebab–Akibat (KKSA)** dan **tidak menghasilkan KKP formal**. Tidak ada elemen **Sebab**, tidak ada penilaian keyakinan. Output = **log kegiatan pendampingan** (atau pendapat advisory atas pertanyaan unit kerja), bukan temuan.

## Yang Dikerjakan

### Tugas utama: log kegiatan pendampingan yang sudah diselesaikan

Untuk setiap penugasan pendampingan, catat **setiap kegiatan** yang dilakukan tim Inspektorat sebagai entri log kegiatan. Sumber: dokumen objek + catatan rapat/notulen yang tersedia.

**Schema tiap entri kegiatan:**
```json
{
  "tanggal": "2026-02-15",
  "jenis_kegiatan": "Rapat Klarifikasi KAK | Reviu HPS Sebelum Tender | Klarifikasi Tender Ulang | Pendampingan Penyusunan Dokumen | dll",
  "pihak_didampingi": "PPK / PA / KPA / Pokja Pemilihan / dst",
  "deskripsi": "Apa yang tim Inspektorat lakukan dalam kegiatan ini (1-3 kalimat)",
  "hasil": "Apa yang berhasil diselesaikan / disepakati dari kegiatan ini",
  "dokumen_pendukung": ["Notulen rapat 15-02-2026", "Draft KAK rev-1 → rev-2"],
  "tindak_lanjut": "Hal yang masih harus diselesaikan auditi (opsional)"
}
```

**Jenis kegiatan yang biasa di-log:**
- **Rapat penyusunan dokumen** — KAK, HPS, dokumen tender
- **Reviu draft dokumen** — sebelum di-finalisasi auditi
- **Klarifikasi prosedur** — saat tender berjalan, pasca sanggah, pemenang mengundurkan diri
- **Pendampingan teknis** — penjelasan regulasi tertentu kepada tim auditi
- **Penyelesaian masalah berjalan** — saat ada kebuntuan proses pengadaan

### Bila pendampingan berupa pendapat atas pertanyaan (advisory)

Bila penugasan berbentuk pertanyaan teknis dari unit kerja (bukan log kegiatan), susun **pendapat advisory** dengan alur: **Pertanyaan → Dasar Hukum → Analisis → Pendapat**. Kutip pasal/ayat yang spesifik dari referensi regulasi. Pendapat tetap **tidak mengikat** dan **tanpa Sebab/temuan**.

## Format Output: Laporan Hasil Pendampingan

Output disusun sebagai **Laporan Hasil Pendampingan Pengadaan** (DOCX) dengan struktur:

```
LAPORAN HASIL PENDAMPINGAN PENGADAAN
====================================
Auditan: [Unit Kerja]
Dasar Penugasan: ST nomor
Periode Pendampingan: [tanggal kegiatan paling awal] s.d. [tanggal kegiatan paling akhir]

Catatan: Laporan ini berisi rangkaian KEGIATAN PENDAMPINGAN yang
telah diselesaikan tim Inspektorat atas permintaan unit kerja.
Pendampingan bersifat advisory dan preventif — tidak memberikan
keyakinan dan tidak mengikat pejabat berwenang.

I. KEGIATAN PENDAMPINGAN YANG TELAH DISELESAIKAN (N)
| No | Tanggal | Jenis Kegiatan | Pihak Didampingi | Deskripsi | Hasil |
| 1  | ...     | ...            | ...              | ...       | ...   |

Dokumen Pendukung per Kegiatan
- Kegiatan #1 (tanggal):
  • Notulen rapat ...
  • Draft KAK rev-1 → rev-2

II. HAL YANG MASIH MEMERLUKAN TINDAK LANJUT
1. [Jenis kegiatan] (tanggal): [tindak lanjut spesifik]
2. ...

III. KESIMPULAN
[Ringkasan pendampingan; bila tidak diisi manual → disusun otomatis dari log]
```

Untuk pendapat advisory atas pertanyaan, gunakan format Memo: **Pertanyaan → Dasar Hukum → Analisis → Pendapat** (tanpa keyakinan, tanpa Sebab).

## Panduan Bahasa

- Gunakan bahasa yang **membantu dan konstruktif** — hindari bahasa yang menghakimi.
- Jelaskan **"mengapa"** di balik regulasi, tidak hanya "apa yang berlaku".
- Sertakan **contoh konkret** jika membantu pemahaman.
- Jika ada ketidakpastian regulasi, **akui** dan jelaskan implikasinya.
- Gunakan **"sebaiknya"**, **"disarankan"** untuk rekomendasi non-wajib; **"wajib"**, **"harus"** untuk ketentuan imperatif dalam regulasi.

## Batasan

- **TANPA Sebab, TANPA KKP formal, tidak mengikat** — konsultasi tidak memakai struktur KKSA, tidak menghasilkan temuan, tidak menghitung keyakinan. Jangan menambah unsur Sebab atau temuan.
- JANGAN menilai apakah dokumen sudah sesuai ketentuan secara komprehensif → gunakan **reviu-pengadaan**.
- JANGAN memantau progres pelaksanaan kontrak end-to-end → gunakan **pemantauan-pengadaan**.
- JANGAN menyimpulkan pelanggaran atau menghitung kerugian negara → gunakan **audit-pengadaan**.
- Jika isu sangat kompleks atau bernilai material besar: rekomendasikan konsultasi ke LKPP.
- Jika dari pendampingan ditemukan **indikasi pelanggaran yang SUDAH terjadi**: sarankan eskalasi ke **audit-pengadaan** (jangan diselesaikan sebagai pendampingan).

## Referensi Regulasi

Konsultasi pengadaan menggunakan regulasi yang sama dengan audit, reviu, dan pemantauan pengadaan. Baca file referensi yang relevan dengan pertanyaan/kegiatan sebelum memberi pendapat; kutip pasal/ayat yang spesifik.

**Panduan lengkap:** `../shared-pbj-references/PANDUAN.md`

**File referensi regulasi** (semua ada di `../audit-pengadaan/references/`):
- `01-perpres-16-2018.md` — prinsip, pelaku, metode pemilihan, kontrak, pelaksanaan
- `02-perpres-12-2021.md` — perubahan threshold dan ketentuan
- `03-perlem-lkpp-12-2021.md` — prosedur teknis pemilihan penyedia secara rinci
- `04-perlem-lkpp-4-2024.md` — konstruksi Design & Build
- `05-perpres-46-2025.md` — ketentuan kontrak dan pembayaran terbaru

## Posisi dalam Keluarga Skill PBJ

> Semua skill PBJ (audit, reviu, pemantauan, konsultasi) menggunakan regulasi yang sama sebagai acuan. Yang membedakan adalah kedalaman pengujian, tujuan, dan format.

| | Audit | Reviu | Pemantauan | **Konsultasi** (skill ini) |
|---|---|---|---|---|
| Tingkat keyakinan | Memadai | Terbatas | Tidak ada | **Tidak ada — advisory** |
| Ruang lingkup | Seluruh siklus | Perencanaan + pemilihan | Pelaksanaan aktif | **Sesuai pertanyaan/kegiatan pendampingan** |
| Pengujian bukti | Sangat mendalam | Administratif | Deskriptif | **Analisis regulasi / log kegiatan** |
| Sebab | ✅ Wajib | ✅ Diisi (anti-mengarang) | ✅ Diisi (anti-mengarang) | **❌ Tidak ada** |
| KKP / Temuan | ✅ | ✅ | ✅ | **❌ Tidak ada (log/pendapat)** |
| Kerugian negara | ✅ Dihitung | ❌ | ❌ | **❌** |
| Kapan digunakan | Pekerjaan selesai / isu serius | Sebelum tender/kontrak | Selama kontrak berjalan | **Unit kerja butuh panduan/pendampingan preventif** |

**Pilih konsultasi-pengadaan (skill ini) ketika:**
- Unit kerja meminta pendampingan berkelanjutan dalam menyusun/menjalankan proses pengadaan.
- Diperlukan pendapat teknis berbasis regulasi atas pertanyaan pengadaan.
- Sifat penugasan preventif/advisory, bukan pengujian formal.

**Jangan gunakan skill ini ketika:**
- Dokumen perencanaan perlu dinilai kesesuaiannya secara formal → **reviu-pengadaan**.
- Progres kontrak perlu dipantau → **pemantauan-pengadaan**.
- Ada indikasi penyimpangan/kerugian → **audit-pengadaan**.
