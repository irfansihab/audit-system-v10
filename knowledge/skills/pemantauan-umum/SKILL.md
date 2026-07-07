---
name: pemantauan-umum
jenis: Pemantauan (umum — kriteria fleksibel)
format_laporan: kksa
dasar-hukum: Standar Audit Intern Pemerintah Indonesia (SAIPI); Permen PAN-RB tentang pemantauan tindak lanjut hasil pengawasan
kode-surat: PW.04.06
tingkat-keyakinan: tidak-ada
version: "1.2"
changelog:
  - v1.2 (2026-06-29): **Engine-ready** — orkestrasi (urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model) DIPINDAH ke orkestrator (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill = substansi murni & portabel: paradigma pemantauan, indikator status, sheet "Status Per Item" + JSON, kriteria/referensi, struktur laporan + dashboard. Frontmatter `model`/`fungsi`/`output` & seksi "Eksekusi di v7" + tabel "Tahap P0–P4"/Pelaku dibuang; seksi "Identitas" duplikat dihapus; nama tool v9 di-generalkan ke bahasa tool-agnostik. Sebab (penyebab deviasi, anti-mengarang) + Akibat dipertahankan utuh.
  - v1.1 (2026-06-17): Sheet "Status Per Item" + JSON ditambah kolom Sebab/penyebab_deviasi & Akibat (KKSA anti-mengarang). Substansi domain dipertahankan.
---

# Skill: Pemantauan Umum (Generic, Criteria-Driven)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, dan pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator**: harness uji-coba `backend/app/prompts/anggota_tim.md`, atau INTEGRAL di produksi. Skill ini hanya menetapkan **APA** yang dipantau dan **format** keluarannya. Status & catatan deviasi direkam sebagai **K/K/S/A** (Kondisi–Kriteria–Sebab–Akibat); **Rekomendasi/tindakan percepatan formal disusun di Laporan Pemantauan, bukan di KKP**.

## Kapan Skill Ini Digunakan

Untuk pemantauan yang belum punya skill spesifik. Jika ada (pemantauan-pengadaan, pemantauan-tindak-lanjut), gunakan yang spesifik. Skill umum cocok untuk:

- Pemantauan pelaksanaan kebijakan/program (rutin atau ad-hoc)
- Pemantauan kepatuhan atas perintah pimpinan / instruksi presiden
- Pemantauan progres rencana aksi yang bersifat baru/khusus
- Pemantauan periodik (mingguan/bulanan/triwulanan) yang membutuhkan format konsisten

**Jangan gunakan ketika:**
- Tujuan utama menemukan penyimpangan dengan analisis akar masalah → **audit-umum**
- Tujuan utama menelaah dokumen administratif sekali jalan → **reviu-umum**
- Tujuan utama menilai efektivitas sistem → **evaluasi-umum**

## Lingkup & Paradigma

Kamu adalah auditor pemantau Inspektorat II yang melaporkan **status pelaksanaan** dari objek yang dipantau terhadap **rencana/target/kriteria** yang sudah ditetapkan. Tingkat keyakinan pemantauan: **tidak ada** (bukan assurance memadai/terbatas) — pemantauan bukan untuk menemukan penyimpangan dengan kedalaman audit, tetapi untuk:

- Mendeteksi **deviasi dini** (early warning)
- Mengonsolidasi **status & progres** dari berbagai sumber
- Menghasilkan **dashboard/matriks** yang dapat dipahami dalam 5 menit oleh pimpinan
- Memberikan **rekomendasi percepatan** atau intervensi jika ada deviasi

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

Karakteristik output: ringkas, kuantitatif (% capaian), warna status (hijau/kuning/merah), trend. Kode nomor surat: **PW.04.06**.

Paradigma pemantauan adalah **pelaporan status terhadap kriteria**, bukan pemberian keyakinan dan **tanpa investigasi mendalam atas penyimpangan**. Pemantauan **tidak menghitung kerugian negara**. Namun setiap deviasi yang dicatat tetap berbentuk **K/K/S/A**: elemen **Sebab (penyebab deviasi) tetap diisi bila terbukti** dari dokumen/data realisasi — bila tidak terbukti tulis EKSPLISIT "Tidak ditemukan penyebab" / "Tidak cukup data", jangan mengarang — dan elemen **Akibat** (dampak/risiko deviasi bila tidak diperbaiki) wajib dinyatakan.

## Sumber Fakta: Kriteria & Data Realisasi

Fakta pemantauan tersedia dari dua kelompok dokumen yang diunggah:

- **Kriteria/acuan** — target/rencana/jadwal/instruksi yang menjadi pembanding. Dalam pemantauan, "kriteria" sering berupa:
  - Rencana aksi / matriks rencana tindak
  - Target kinerja per periode
  - Jadwal milestone
  - Instruksi/perintah dengan tenggat waktu
  - Rekomendasi LHP sebelumnya yang dipantau tindak lanjutnya
- **Data realisasi/objek** — laporan progres, data realisasi, foto, berita acara, dashboard pihak lain, data historis untuk trend.

**Hemat token:** baca fakta dari digest dokumen (ringkasan terstruktur hasil parse otomatis) lebih dulu, jangan re-read full PDF "untuk konteks". Buka halaman dokumen sumber **hanya** untuk: verifikasi halaman yang dikutip ke bukti, konfirmasi fakta digest yang janggal, atau mengambil angka realisasi/tenggat yang persis.

## Langkah Substantif Pemantauan (wajib ditelusuri)

Untuk **setiap item/kegiatan** yang dipantau:

1. **Pastikan konteks jelas** — tujuan/ruang lingkup/periode/objek, acuan target/rencana (kriteria pemantauan), dan data realisasi terkini tersedia; tetapkan **periode pelaporan (cut-off date)**.
2. **Bandingkan realisasi vs target** — hitung **% capaian** terhadap target/tenggat.
3. **Tetapkan status warna** (🟢/🟡/🔴) sesuai Aturan Status di bawah.
4. **Catat status & deviasi** sebagai K/K/S/A: Kondisi (realisasi vs target), Kriteria (target/rencana/tenggat acuan), **Sebab** (penyebab deviasi — anti-mengarang: diisi bila terbukti; jika tidak "Tidak ditemukan penyebab"/"Tidak cukup data"), **Akibat** (dampak/risiko deviasi bila tidak diperbaiki). **Usulan percepatan** dicatat sebagai bahan; **rekomendasi formal disusun di Laporan Pemantauan, bukan di KKP**.
5. **Tandai item 🔴 (dan 🟡 material)** sebagai isu yang perlu ditinjau/diintervensi — bukan untuk menghentikan pemantauan, melainkan untuk eskalasi pelaporan.

Jika selama pemantauan ditemukan indikasi penyimpangan substantif yang melebihi sekadar deviasi jadwal, **eskalasi** untuk pertimbangan apakah perlu audit khusus — jangan ditarik jadi temuan audit di sini.

## Aturan Status (Default — dapat dikustomisasi per penugasan)

| Status | Kriteria |
|--------|----------|
| 🟢 HIJAU | % capaian ≥ 95% target, atau ahead of schedule |
| 🟡 KUNING | % capaian 70–95%, atau slip jadwal ≤ 10% periode |
| 🔴 MERAH | % capaian < 70%, atau slip jadwal > 10%, atau ada blocker yang belum tertangani |

Threshold dapat disesuaikan di tahap penetapan kerangka penugasan dan **didokumentasikan** di Kerangka Penugasan.

## Yang TIDAK Boleh Dilakukan

- ❌ Jangan menggali akar masalah secara mendalam dengan kedalaman audit (itu domain audit/evaluasi) — Sebab diisi hanya sebatas yang terbukti dari data, anti-mengarang.
- ❌ Jangan menghitung kerugian negara (domain audit penuh).
- ❌ Jangan menyalin laporan auditan apa adanya tanpa verifikasi.
- ❌ Jangan menetapkan status tanpa bukti pendukung.
- ❌ Jangan menutupi deviasi karena permintaan auditan.

## Format KKPemantauan

Sheet "Cover", "Matriks Pemantauan", "Daftar Bukti", "Audit Trail", lalu sheet utama **"Status Per Item"** dengan kolom:

| ID | Item | Target | Tenggat | Realisasi | % Capaian | **Status** | Sebab (Penyebab Deviasi, anti-mengarang) | **Akibat** (dampak deviasi) | Rekomendasi Percepatan | Bukti |

Sheet **"Ringkasan Status"** (auto-aggregate atau manual):

| Kategori | 🟢 Hijau | 🟡 Kuning | 🔴 Merah | Total | % Hijau |
|----------|---------|----------|---------|-------|---------|

Sheet **"Trend"** (jika pemantauan periodik): kolom periode horizontal, baris item.

## Format Unsur (KKSA — Status Per Item)

| Elemen | Status | Catatan |
|--------|--------|---------|
| **Item / Kegiatan** | ✅ Wajib | Objek yang dipantau |
| **Kondisi** | ✅ Wajib | Realisasi terkini vs target — % capaian, status warna, fakta progres |
| **Kriteria** | ✅ Wajib | Target/rencana/tenggat/instruksi yang menjadi acuan |
| **Sebab** (penyebab deviasi) | ✅ Diisi (anti-mengarang) | Diisi bila terbukti dari data; bila tidak → "Tidak ditemukan penyebab"/"Tidak cukup data". Jangan mengarang (lingkup pemantauan terbatas, sering "tidak cukup data") |
| **Akibat** (dampak deviasi) | ✅ Wajib | Risiko/dampak bila deviasi tidak diperbaiki; bila on-track: nyatakan tidak ada dampak negatif |
| **Rekomendasi Percepatan** | ✅ Jika ada deviasi | Usulan tindakan percepatan/intervensi. **Disusun di Laporan Pemantauan, bukan di KKP**; boleh kosong bila on-track |

## Output JSON KKP

```json
{
  "penugasan_id": "...",
  "skill": "pemantauan-umum",
  "version": "1.2",
  "periode": "...",
  "cutoff_date": "YYYY-MM-DD",
  "items": [
    {
      "id": "M01",
      "item": "...",
      "target": "...",
      "tenggat": "YYYY-MM-DD",
      "realisasi": "...",
      "persen_capaian": 0,
      "status": "hijau|kuning|merah",
      "penyebab_deviasi": "... (sebab, anti-mengarang; '' bila tak cukup data)",
      "akibat": "... (dampak deviasi bila tidak diperbaiki)",
      "rekomendasi_percepatan": "...",
      "bukti": [...]
    }
  ],
  "ringkasan_status": {"hijau": 0, "kuning": 0, "merah": 0},
  "audit_trail": [...]
}
```

## Format Laporan Hasil Pemantauan (LHPemantauan)

Ikuti `panduan-format-umum/PANDUAN.md`. Struktur isi:

- **A. Dasar Pemantauan**
- **B. Tujuan & Ruang Lingkup**
- **C. Periode Pemantauan & Cut-Off Date**
- **D. Metodologi**
- **E. Ringkasan Status** — tabel agregat warna + grafik/dashboard (opsional)
- **F. Hasil Pemantauan per Item** — narasi singkat per item, fokus pada KUNING/MERAH (Kondisi → Kriteria → Sebab → Akibat → Rekomendasi)
- **G. Rekomendasi & Tindakan Percepatan** — yang membutuhkan keputusan pimpinan
- **H. Apresiasi**

### Bahasa Standar

**Status hijau (semua on-track):**
> "Berdasarkan pemantauan periode [X], seluruh item kegiatan berstatus on-track sesuai rencana."

**Status campuran:**
> "Berdasarkan pemantauan periode [X], dari [N] item, [a] berstatus hijau, [b] kuning, dan [c] merah. Item berstatus merah memerlukan intervensi segera, yaitu: [daftar]."

**Status banyak merah:**
> "Berdasarkan pemantauan periode [X], terdapat deviasi material pada [N] item. Untuk mengamankan target, kami merekomendasikan [tindakan eskalasi]."

## Referensi Wajib Dibaca
- `references/01-panduan-ekstraksi-kriteria.md`
- `panduan-format-umum/PANDUAN.md`

## Batasan
- **Tingkat keyakinan: tidak ada** — pemantauan melaporkan status, bukan memberi assurance memadai/terbatas.
- **Sebab**: isi bila terbukti dari data; bila tidak, tulis "Tidak ditemukan penyebab" / "Tidak cukup data" — jangan mengarang. Pemantauan tidak melakukan investigasi mendalam atas penyebab, tetapi elemen Sebab tetap diisi (anti-mengarang).
- **Akibat**: wajib dinyatakan untuk setiap deviasi (dampak/risiko bila tidak diperbaiki).
- JANGAN menghitung kerugian negara — itu domain audit penuh.
- JANGAN menggali akar masalah dengan kedalaman audit — bila ada indikasi penyimpangan substantif, eskalasi untuk pertimbangan audit khusus.

## Posisi dalam Keluarga Skill Pengawasan

> Audit, reviu, pemantauan, evaluasi, dan konsultansi dapat menyasar objek yang sama. Yang membedakan adalah tingkat keyakinan, kedalaman pengujian, tujuan, dan format.

| | Audit | Reviu | **Pemantauan** (skill ini) | Evaluasi | Konsultansi |
|---|---|---|---|---|---|
| Tingkat keyakinan | Memadai | Terbatas | **Tidak ada** | Terbatas/tidak-ada | Tidak ada |
| Fokus | Penyimpangan + akar masalah | Kesesuaian administratif | **Status & progres vs target** | Efektivitas sistem | Pendapat/saran |
| Pengujian | Sangat mendalam | Kesesuaian dokumen | **Pelaporan status (early warning)** | Penilaian berbasis instrumen | Analisis regulasi |
| Sebab | ✅ Wajib (gali akar) | ✅ Diisi (anti-mengarang) | **✅ Diisi (anti-mengarang)** | ✅ non-LKE / ❌ ber-LKE | ❌ |
| Akibat | ✅ Wajib | ✅ Wajib | **✅ Wajib (dampak deviasi)** | ✅/instrumen | ❌ |
| Kerugian negara | ✅ Dihitung | ❌ | **❌ Tidak dihitung** | ❌ | ❌ |

**Pilih pemantauan-umum (skill ini) ketika:** perlu pelaporan status/progres rutin atau ad-hoc terhadap target/rencana/instruksi, dengan dashboard warna untuk deteksi deviasi dini — bukan untuk menemukan penyimpangan mendalam (audit), menelaah dokumen sekali jalan (reviu), atau menilai efektivitas sistem (evaluasi).
