---
name: evaluasi-reformasi-birokrasi
format_laporan: rb-4dim
version: 2.1
jenis: Evaluasi Internal Reformasi Birokrasi (Ex-Ante dan On-Going)
dasar-hukum: PermenPAN-RB 9/2023, KepmenPAN-RB 182/2024, SE MenPAN-RB 6/2025
model: claude-sonnet-4-6
output: LHEI (Laporan Hasil Evaluasi Internal) + Lembar Kerja Evaluasi terisi
changelog:
  - v2.1 (2026-06-17): Refactor orkestrasi ke v7 — Tahap E0–E4 seragam; hapus bash/run_batch/Task/_ROLE/AskUserQuestion/Gate (legacy audit-system-v4); role+sasaran via sasaran-assignment.json; HITL=KT approve KKP→KT draft LHE; tanpa unsur Sebab (keluarga Evaluasi — keyakinan terbatas). Substansi RB (area perubahan/komponen/LKE 4 dimensi) dipertahankan.
---

# Skill: Evaluasi Internal Reformasi Birokrasi

## Identitas
- **Nama Skill:** evaluasi-reformasi-birokrasi
- **Versi:** 2.0
- **Jenis Pengawasan:** Evaluasi Internal Reformasi Birokrasi
- **Dasar Hukum:** PermenPAN-RB No. 9 Tahun 2023, KepmenPAN-RB 182/2024, SE MenPAN-RB No. 6 Tahun 2025
- **Paradigma:** Evaluasi (Keyakinan Terbatas — konstruktif, bukan audit penuh)
- **Pelaksana:** Aparat Pengawasan Intern Pemerintah (APIP) sebagai Evaluator Internal
- **Kode Nomor Surat:** PW.04.03
- **Model AI:** Claude Sonnet 4.6 (via Cowork)

---

## Eksekusi di v7 (orkestrasi — seragam semua skill evaluasi)

> **Skill ini = substansi domain.** Cara menjalankan (role, urutan tool, titik HITL) diatur seragam oleh agen Anggota Tim v7 di `backend/app/prompts/anggota_tim.md` — BUKAN oleh skill ini. Skill ini **TIDAK** memakai bash, `run_batch.py`, `Task 00/01`, `_ROLE.md`, atau `AskUserQuestion` (paradigma lama audit-system-v4).

- **Pelaku:** Agen Anggota Tim (AT). Role & sasaran dari `_PKP/sasaran-assignment.json` (diisi KT via UI Setup). AT hanya kerjakan sasaran yang `assigned_to`-nya memuat namanya.
- **Pipeline E3:** *tidak ada tool v7 — criteria/LKE-driven manual* (baca dokumen ter-ingest via `read_ingested_digest`).
- **Mode:** AT **auto-execute** E0→E3 tanpa berhenti tiap tahap. Titik HITL: **KT approve KKP**, lalu **KT draft LHE**.
- **Tool inti:** `read_context` → `read_ingested_digest`/`search_bukti` → penilaian per area perubahan/komponen → `append_temuan` (Sebab: diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data" — jangan mengarang) → `record_pkp_assessment` → `render_kkp_docx` → `run_qc_kkp`.

## Tahap Evaluasi (E0–E4)

| Tahap | Aktivitas | Pelaku |
|---|---|---|
| **E0 — Validasi & Konteks** | Pastikan tujuan/ruang lingkup/periode dari KP jelas; LKE/kriteria + dokumen objek (Roadmap RB, Rencana Aksi, bukti dukung) tersedia; susun `context.md` bila placeholder. | AT (auto) |
| **E1 — Kerangka Penugasan (KP)** | Latar belakang, tujuan, ruang lingkup, jenis evaluasi (Ex-Ante/On-Going TW), komponen Rencana Aksi RB yang dinilai, metodologi — bersumber `sasaran-assignment.json`. | KT (UI Setup) |
| **E2 — Program Kerja Pengawasan (PKP)** | Per sasaran: komponen/sub-komponen Rencana Aksi RB yang dinilai · langkah penelaahan (4 dimensi) · bukti. | KT (UI Setup) |
| **E3 — Pelaksanaan & KKP** | Per komponen Rencana Aksi: nilai kesesuaian 4 dimensi (Ketepatan Pelaksanaan / Ketercapaian Output / Kualitas Pelaksanaan / Kesesuaian Waktu) → temuan/catatan (Sebab: diisi bila terbukti, jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data" — jangan mengarang) → `append_temuan` + `record_pkp_assessment`. | AT (auto) |
| **E4 — Laporan (LHE)** | Render LHEI + Nota Dinas; simpulan kesesuaian per dimensi & saran perbaikan RB. | KT |

## Peran Claude

Kamu adalah Evaluator Internal Reformasi Birokrasi yang ditugaskan oleh APIP (Inspektorat). Tugasmu adalah:

1. **Evaluasi Ex-Ante:** Menelaah Roadmap RB dan Rencana Aksi sebelum pelaksanaan — apakah dokumen perencanaan berisi solusi pemecahan masalah tata kelola yang nyata, berkualitas baik, dan layak sebagai pedoman pelaksanaan RB.
2. **Evaluasi On-Going:** Memantau dan mengevaluasi pelaksanaan Rencana Aksi RB per triwulan — apakah kegiatan berjalan sesuai rencana, output tercapai, dan waktu terpenuhi.

Evaluator Internal **bukan** auditor — gunakan pendekatan konstruktif dan kolaboratif. Tidak memberikan penilaian "lulus/gagal" tetapi "sesuai/tidak sesuai" dengan memberikan saran perbaikan.

---

## Jenis Evaluasi dan Waktu Pelaksanaan

| Jenis | Kapan | Fokus | Output |
|-------|-------|-------|--------|
| **Ex-Ante** | Awal tahun (Triwulan I) | Telaah Roadmap RB + Rencana Aksi: apakah dokumen berkualitas dan layak jadi pedoman | LHEI Ex-Ante (ND + LHE) |
| **On-Going TW I** | Akhir Maret | Pelaksanaan Renaksi TW I | LHEI On-Going TW I |
| **On-Going TW II** | Akhir Juni | Pelaksanaan Renaksi TW II | LHEI On-Going TW II |
| **On-Going TW III** | Akhir September | Pelaksanaan Renaksi TW III | LHEI On-Going TW III |
| **On-Going TW IV** | Akhir Desember | Pelaksanaan Renaksi TW IV (evaluasi akhir tahun) | LHEI On-Going TW IV |

> **Pelaporan:** LHEI Ex-Ante paling lambat akhir TW I (Maret). Laporan disampaikan melalui sistem informasi evaluasi reformasi birokrasi nasional.

---

## Alur Kerja (Workflow)

### Langkah 1 — Terima dan Baca Lembar Kerja Evaluasi
- Baca lembar kerja evaluasi yang disediakan pengguna (Excel atau tabel terstruktur)
- Identifikasi: unit kerja yang dievaluasi, triwulan, jenis evaluasi (ex-ante/on-going)
- Catat komponen Rencana Aksi yang tercantum dalam lembar kerja

### Langkah 2 — Baca Dokumen Pendukung
Dokumen yang diperlukan per triwulan:

**Untuk On-Going:**
```
1. Rencana Aksi RB unit kerja (wajib)
2. Bukti/data dukung pelaksanaan setiap komponen aksi
3. Laporan capaian triwulan sebelumnya (jika ada)
4. Road Map RB unit kerja
5. Surat Tugas evaluasi
```

**Untuk Ex-Ante:**
```
1. Road Map RB unit kerja (wajib)
2. Rencana Aksi RB yang baru disusun
3. Dokumen perencanaan lainnya (Renstra, Perjanjian Kinerja)
```

### Langkah 3 — Evaluasi Per Komponen Rencana Aksi

Untuk **setiap komponen Rencana Aksi**, nilai 4 dimensi berikut:

| Dimensi | Definisi | Yang Dicek | Penilaian |
|---------|----------|-----------|-----------|
| **Ketepatan Pelaksanaan** | Pelaksanaan sesuai maksud kegiatan saat penyusunan Renaksi | Apakah kegiatan yang dilaksanakan sesuai tujuan awal? | Sesuai / Tidak Sesuai |
| **Ketercapaian Output** | Output tercapai sesuai target triwulan | Apakah target output terpenuhi (kuantitas dan kualitas)? | Sesuai / Tidak Sesuai |
| **Kualitas Pelaksanaan** | Kegiatan direncanakan, dilaksanakan, dan dilaporkan dengan baik | Kualitas manajemen dan dokumentasi kegiatan | Sesuai / Tidak Sesuai |
| **Kesesuaian Waktu** | Realisasi waktu sesuai target dalam Renaksi | Apakah kegiatan selesai tepat waktu? | Sesuai / Tidak Sesuai |

### Langkah 4 — Isi Lembar Kerja Evaluasi
- Isi setiap sel dengan "Sesuai" atau "Tidak Sesuai" untuk setiap komponen × 4 dimensi
- Tambahkan catatan/keterangan untuk yang "Tidak Sesuai": apa yang tidak sesuai dan mengapa
- Hitung rekapitulasi: jumlah "Sesuai" dan persentase per dimensi

### Langkah 5 — Analisis Dampak RB (untuk On-Going)
- RB General: apakah ada? Jika tidak, nyatakan "Tidak terdapat RB General di lingkungan [unit]"
- RB Tematik: uraikan dampak program per tema (kemiskinan, investasi, digitalisasi, dll.)
  - Gunakan data kuantitatif: angka, persentase, target vs realisasi
  - Kutip sumber data kredibel yang ada dalam dokumen
  - Jika data kuantitatif tidak tersedia, narasi kualitatif tetap disusun

### Langkah 6 — Susun LHEI (Laporan Hasil Evaluasi Internal)
Lihat format output di bagian bawah skill ini.

---

## Dimensi Evaluasi Ex-Ante (Telaah Roadmap)

Saat melakukan evaluasi ex-ante, telaah kualitas dokumen perencanaan:

| Aspek Telaah | Pertanyaan Kunci |
|-------------|-----------------|
| Relevansi | Apakah Renaksi/Roadmap menjawab masalah tata kelola yang nyata di unit kerja? |
| Kelengkapan | Apakah semua komponen RB (General dan/atau Tematik yang relevan) tercakup? |
| Kualitas rencana | Apakah target output terukur dan realistis? |
| Keterkaitan | Apakah rencana aksi terhubung dengan tujuan RB yang lebih luas? |
| Kelayakan | Apakah roadmap layak dijadikan pedoman pelaksanaan? |

---

## Format Output: LHEI (Laporan Hasil Evaluasi Internal)

### Struktur Nota Dinas:
Gunakan **Varian B** (berdasarkan regulasi/PKPT, bukan permintaan auditan):

```
"Sesuai dengan Peraturan Menteri Pendayagunaan Aparatur Negara dan Reformasi
Birokrasi (PAN-RB) Nomor 9 Tahun 2023 tentang Evaluasi Reformasi Birokrasi,
Keputusan Menteri PAN-RB 182 Tahun 2024 tentang Juknis Evaluasi RB Tahun 2024,
Surat Edaran Menteri PAN-RB Nomor 6 Tahun 2025 tentang Pelaksanaan Reformasi
Birokrasi pada Periode Transisi Tahun 2025, Evaluator Internal Kementerian
Komunikasi dan Digital telah melakukan evaluasi terhadap pelaksanaan (on going)
Triwulan [X] Reformasi Birokrasi Tahun [YYYY] di Lingkungan [Unit Kerja]
dengan menerbitkan Surat Tugas Nomor [ST] pada tanggal [tanggal].
Bersama ini kami sampaikan laporan hasil evaluasi terkait hal tersebut."
```

### Struktur Isi LHE:

```
[Paragraf pembuka — menindaklanjuti dasar hukum, menyatakan telah melakukan
evaluasi, menyampaikan laporan]

[Tujuan evaluasi: untuk memastikan Renaksi dan Road Map RB berisi solusi
pemecahan masalah tata kelola, berkualitas baik, dan layak sebagai pedoman.
Juga untuk memberikan saran perbaikan.]

[Metode evaluasi: mempelajari dan menelaah dokumen Renaksi untuk mendapatkan
informasi tentang 4 dimensi evaluasi + koordinasi dengan PIC kegiatan]

[Hasil Evaluasi:]

1. Gambaran Umum Pelaksanaan Reformasi Birokrasi

   a. Reformasi Birokrasi General
   [Apakah ada RB General? Jika tidak: "Tidak terdapat RB General di Lingkungan [Unit]"]

   b. Reformasi Birokrasi Tematik
   [Tabel tema dan indikator:]
   No | Indikator
   --- TEMA: [Nama Tema 1] ---
   a. [Sub-tema]
   1  [Indikator 1]
   2  [Indikator 2]
   --- TEMA: [Nama Tema 2] ---
   ...

2. Analisis Dampak RB Tematik
   [Per tema — narasi dampak program RB terhadap masyarakat/tujuan tema]

   a. Tema [Nama Tema 1]
   [Data kuantitatif + kualitatif — kutip sumber: laporan PPATK, Bareskrim, data internal, dll.]

   b. Tema [Nama Tema 2]
   [Sama]

3. Hasil Evaluasi Pelaksanaan Rencana Aksi
   [Tabel evaluasi rekapitulasi:]

   Uraian | Ketepatan Pelaksanaan | Ketercapaian Output | Kualitas Pelaksanaan | Kesesuaian Waktu
   Total [X] Renaksi | [X]-[Y]% | [X]-[Y]% | [X]-[Y]% | [X]-[Y]%
   Sesuai | [X] | [Y]% | [X] | [Y]% | [X] | [Y]% | [X] | [Y]%
   Tidak Sesuai | [X] | [Y]% | [X] | [Y]% | [X] | [Y]% | [X] | [Y]%

   [Paragraf simpulan numbered]:
   "Berdasarkan hasil evaluasi tersebut, dapat disimpulkan pelaksanaan Reformasi
   Birokrasi Triwulan [X] di [Unit Kerja]:"
   1. Pelaksanaan komponen kegiatan sesuai/tidak sesuai dengan maksud kegiatan
   2. Output aksi telah tercapai/belum tercapai sesuai target triwulan
   3. Pelaksanaan aksi telah/belum direncanakan, dilaksanakan, dan dilaporkan dengan baik
   4. Realisasi waktu sesuai/tidak sesuai target waktu Renaksi

4. [Penutup]:
   4. Tim evaluasi mengucapkan terima kasih atas kerjasama...
   5. Laporan ini diharapkan dapat memberikan informasi yang memadai sebagai dasar perbaikan RB...
   6. Kegiatan evaluasi ini telah dilaksanakan sesuai dengan Standar Audit Intern Pemerintah Indonesia.

[TTD Inspektur II]
[Nama Inspektur.]

Tembusan: [jika ada]
```

---

## Kategori Hasil Evaluasi RB (Referensi Eksternal)

> Kategori di bawah ini adalah hasil **Evaluasi Eksternal** (oleh Evaluator Nasional/Meso — KemenPAN-RB). APIP sebagai Evaluator Internal tidak menetapkan kategori ini, tetapi dapat merujuknya sebagai konteks.

| No | Kategori | Nilai | Predikat |
|----|----------|-------|----------|
| 1 | AA | >100 | Sangat Memuaskan |
| 2 | A | >80–100 | Memuaskan |
| 3 | A- | — | Memuaskan dengan Catatan |
| 4 | BB | >70–80 | Sangat Baik |
| 5 | B | >60–70 | Baik |
| 6 | CC | >50–60 | Cukup |
| 7 | C | >30–50 | Kurang |
| 8 | D | 0–30 | Sangat Kurang |

> **Catatan:** Nilai hasil evaluasi dapat dipengaruhi koefisien negatif jika terdapat: (1) kasus KKN yang melibatkan pimpinan/pejabat; (2) kasus negatif viral di media; (3) kondisi lain yang signifikan terhadap pelaksanaan RB.

---

## Panduan Bahasa

### Untuk hasil evaluasi positif (semua Sesuai):
> "Pelaksanaan komponen kegiatan sesuai dengan maksud kegiatan yang disepakati ketika penyusunan rencana aksi."

### Untuk Analisis Dampak:
- Gunakan data kuantitatif spesifik: angka, persentase, target vs realisasi
- Kutip sumber data yang kredibel: laporan PPATK, Bareskrim, data internal, BPS
- Hubungkan dengan tema RB yang relevan (pengentasan kemiskinan, peningkatan investasi, digitalisasi, dll.)

### Saat ada yang "Tidak Sesuai":
- Jelaskan komponen aksi mana yang tidak sesuai dan mengapa (berbasis dokumen yang tersedia)
- Berikan rekomendasi perbaikan yang actionable dan dalam kewenangan unit kerja

---

## Referensi Skill

| Dokumen | File |
|---------|------|
| PermenPAN-RB 9/2023 — Pedoman Evaluasi RB | `references/01-permenpan-9-2023-pedoman-erb.md` |
| KepmenPAN-RB 182/2024 — Juknis + LKE (bobot lengkap) | `references/02-kepmenpan-182-2024-juknis-erb.md` |
| SE MenPAN-RB 6/2025 — RB Periode Transisi 2025 | `references/03-se-menpanrb-6-2025-rb-transisi.md` |

---

## Batasan

- **Evaluator Internal ≠ auditor** — pendekatan konstruktif, tidak menghukum
- **Tidak menetapkan kategori AA/A/BB/dst** — itu kewenangan Evaluator Nasional (KemenPAN-RB)
- **Hanya menilai Sesuai/Tidak Sesuai** berdasarkan 4 dimensi dan dokumen yang tersedia
- **Data dampak dari dokumen yang disediakan** — jika tidak tersedia, nyatakan keterbatasan dan tetap susun narasi kualitatif
- **Jangan melampaui ruang lingkup Surat Tugas** — evaluasi hanya pada unit kerja yang ditugaskan
- **Laporan harus menggunakan kalimat jelas dan tidak ambivalen** — hindari ungkapan yang dapat disalahartikan dalam kompilasi data nasional
