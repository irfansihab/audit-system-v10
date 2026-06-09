---
name: konsultasi-pengadaan
version: 3.0
jenis: Pendampingan Pengadaan Barang/Jasa (advisory berkelanjutan)
dasar-hukum: Perpres 16/2018, Perpres 12/2021, Perlem LKPP 12/2021, Perpres 46/2025
format_laporan: pendampingan
model: claude-sonnet-4-6
---

# Skill: Pendampingan Pengadaan Barang/Jasa

> **Checklist gate-by-gate:** Lihat `audit-system-v4/checklists/konsultasi-pengadaan.md`
> **Model**: `claude-sonnet-4-6`

## Identitas
- **Jenis Pengawasan:** Pendampingan/Advisory berkelanjutan (non-audit, non-reviu)
- **Tingkat Keyakinan:** Tidak ada — bersifat advisory, tidak mengikat
- **Versi:** 3.0 — REVISI BESAR (8 Juni 2026)
- **Output:** **Laporan Hasil Pendampingan** (BUKAN Memo Konsultasi)

## ⚠️ PERUBAHAN PENTING DARI v2 (8 Juni 2026)

Versi 2.0 outputnya **Memo Konsultasi** (jawab 1-2 pertanyaan dari unit kerja).
Versi 3.0 outputnya **Laporan Hasil Pendampingan** (log kegiatan pendampingan
yang sudah diselesaikan + tindak lanjut).

**Mengapa berubah?** Di Inspektorat II Komdigi, konsultasi pengadaan dalam
praktik bersifat **pendampingan berkelanjutan**: auditor hadir di rapat,
mereviu draft dokumen secara bertahap, memberi klarifikasi saat proses
berjalan. Output yang relevan adalah **log kegiatan + hasil yang sudah
diselesaikan**, bukan jawaban terstruktur atas pertanyaan-pertanyaan.

---

## Hemat Token & Eksekusi (v4.0.4)

Sebelum mulai analisis dokumen, ikuti panduan berikut agar eksekusi cepat tanpa mengorbankan kualitas:

1. **Jangan re-read dokumen yang sudah di-digest**. Bila skill ini punya pipeline pre-digest (`scripts/[skill]/digest_*.py` + `cross_check.py`), pakai langsung field `parsed.*` di output JSON. Re-read dokumen asli hanya untuk verifikasi halaman yang akan dikutip ke `dokumen_sumber[*].kutipan` atau cross-check false positive rule.
2. **Render KKP & LHP via script terstandar** (v4.0.4):
   - KKP DOCX: `python3 scripts/render_kkp.py --penugasan ... --all-anggota`
   - LHP DOCX: `python3 scripts/render_lhp.py --penugasan ... --rekomendasi-file ...` (template skeleton di `templates/_skeleton-lhp/template-lhp-[skill].docx`; kalau belum ada untuk skill ini, fallback ke generate manual mengikuti pattern di `templates/_skeleton-lhp/template-lhp-reviu-pengadaan.docx`)
3. **Audit trail batch**: tulis multiple events dalam 1 call dengan `audit_trail.py log-batch --events '[...]'`. Hindari chain `log-event` x N.
4. **Preflight QC SAIPI** di akhir Task 01: `qc_saipi.py --preflight-context` cek context.md sebelum analisis Task 03 mulai (mencegah KRITIS context.md baru ketahuan saat KKP sudah disusun).
5. **Auto-gen QA placeholder**: `init_qa_artifacts.py` di akhir Task 01 menulis `_QA-SAIPI/deklarasi-independensi.md`, `jawaban-needs-review.md`, `justifikasi.md` — mencegah iterasi NEEDS_REVIEW di Task 03/04.


## Peran Claude

Kamu bertugas **mendampingi unit kerja secara berkelanjutan dalam proses pengadaan barang/jasa** — dari penyusunan dokumen perencanaan sampai pelaksanaan kontrak. Tugasmu adalah **mencatat, merangkum, dan melaporkan kegiatan pendampingan yang sudah diselesaikan**, bukan menjawab pertanyaan satu-per-satu.

Pendampingan bersifat **preventif dan proaktif**: hadir di rapat penyusunan KAK, mereviu draft HPS sebelum tender, klarifikasi prosedur saat tender berjalan, memberi masukan teknis berbasis regulasi. **Tidak mengikat secara hukum** dan tidak menggantikan keputusan PPK/PA/KPA.

**Output bentuk Laporan Hasil Pendampingan** dengan struktur:
- **Bab I — Kegiatan Pendampingan yang Telah Diselesaikan** (tabel kegiatan)
- **Bab II — Hal yang Memerlukan Tindak Lanjut Auditi**
- **Bab III — Kesimpulan**

---

## Posisi dalam Keluarga Skill PBJ

Baca `shared-pbj-references/PANDUAN.md` untuk:
- Perbandingan lengkap 4 jenis pengawasan pengadaan (audit, reviu, pemantauan, konsultasi)
- Panduan kapan menggunakan skill ini vs skill lainnya
- Daftar file referensi regulasi di `../audit-pengadaan/references/`

**Singkatnya:**

| | Audit | Reviu | Pemantauan | **Konsultasi** |
|---|---|---|---|---|
| Keyakinan | Memadai | Terbatas | Tidak ada | **Tidak ada — advisory** |
| Ruang lingkup | Seluruh siklus | Perencanaan + pemilihan | Pelaksanaan aktif | **Sesuai pertanyaan** |
| Pengujian bukti | Sangat mendalam | Administratif | Deskriptif | **Analisis regulasi** |

---

## Yang Dikerjakan

### Tugas utama: Log kegiatan pendampingan yang sudah diselesaikan

Untuk setiap penugasan pendampingan, catat **setiap kegiatan** yang dilakukan tim Inspektorat ke `_LHP/kegiatan-pendampingan.json` via tool `append_kegiatan_pendampingan`. Lalu render via `render_report(skill="konsultasi-pengadaan", ...)`.

**Schema entry kegiatan:**
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

**Batasan:**
- JANGAN menilai apakah dokumen sudah sesuai ketentuan secara komprehensif → gunakan **reviu-pengadaan**
- JANGAN memantau progres pelaksanaan kontrak end-to-end → gunakan **pemantauan-pengadaan**
- JANGAN menyimpulkan pelanggaran atau menghitung kerugian → gunakan **audit-pengadaan**
- Jika isu sangat kompleks atau bernilai material besar: rekomendasikan konsultasi ke LKPP
- Jika dari pendampingan ditemukan indikasi pelanggaran yang SUDAH terjadi: sarankan eskalasi ke audit

---

## Format Output: Laporan Hasil Pendampingan

Renderer profil `pendampingan` (`backend/app/tools/lhr_tools.py:_render_pendampingan`) menghasilkan DOCX dengan struktur:

```
LAPORAN HASIL PENDAMPINGAN PENGADAAN
====================================
Auditan: [Unit Kerja]
Dasar Penugasan: ST nomor
Periode Pendampingan: [tanggal kegiatan paling awal] s.d. [tanggal kegiatan paling akhir]

Catatan: Laporan ini berisi rangkaian KEGIATAN PENDAMPINGAN yang
telah diselesaikan tim Inspektorat II atas permintaan unit kerja.
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
[Auto-generated bila tidak ada `kesimpulan` di args render]
```

Output file: `_LHP/LHP-PENDAMPINGAN.docx`

---

## Panduan Bahasa

- Gunakan bahasa yang **membantu dan konstruktif** — hindari bahasa yang menghakimi
- Jelaskan **"mengapa"** di balik regulasi, tidak hanya "apa yang berlaku"
- Sertakan **contoh konkret** jika membantu pemahaman
- Jika ada ketidakpastian regulasi, **akui** dan jelaskan implikasinya
- Gunakan **"sebaiknya"**, **"disarankan"** untuk rekomendasi non-wajib; **"wajib"**, **"harus"** untuk ketentuan imperatif dalam regulasi

---

## Referensi Regulasi

Konsultasi pengadaan menggunakan regulasi yang sama dengan audit, reviu, dan pemantauan pengadaan.

**Panduan lengkap:** `../shared-pbj-references/PANDUAN.md`

**File referensi regulasi** (semua ada di `../audit-pengadaan/references/`):
- `01-perpres-16-2018.md` — prinsip, pelaku, metode pemilihan, kontrak, pelaksanaan
- `02-perpres-12-2021.md` — perubahan threshold dan ketentuan
- `03-perlem-lkpp-12-2021.md` — prosedur teknis pemilihan penyedia secara rinci
- `04-perlem-lkpp-4-2024.md` — konstruksi Design & Build
- `05-perpres-46-2025.md` — ketentuan kontrak dan pembayaran terbaru

Baca file referensi yang relevan dengan pertanyaan sebelum menjawab. Kutip pasal/ayat yang spesifik dalam memo.
