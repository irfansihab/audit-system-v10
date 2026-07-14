# Pola Deteksi Domain & Penamaan Skill

Panduan algoritma untuk Gate 1 graduasi: bagaimana sistem mendeteksi **topik/domain** dari kriteria penugasan dan menyusun **nama skill** yang konsisten.

---

## Algoritma Deteksi Domain

### Langkah 1 — Term Frequency dari Kriteria

Untuk semua file di `input/kriteria/` semua penugasan input:

1. Ekstrak teks (lihat `01-panduan-ekstraksi-kriteria.md`)
2. Tokenisasi (lowercase, hapus stopword bahasa Indonesia)
3. Hitung **term frequency (TF)** kata bermakna ≥3 huruf
4. Hitung **inverse document frequency (IDF)** terhadap corpus skill umum lainnya
5. Ambil **top-20 term TF-IDF** sebagai kandidat domain term

**Stopword bahasa Indonesia** yang harus dibuang minimal:
```
yang, dan, di, ke, dari, untuk, dengan, atau, adalah, akan, telah,
pada, oleh, dalam, sebagai, tidak, ini, itu, juga, dapat, wajib,
harus, sebagaimana, dimaksud, dimaksudkan, tersebut, sebagai berikut,
bagi, kepada, atas, agar, supaya, jika, apabila, demikian, maka,
peraturan, pemerintah, menteri, undang, pasal, ayat, butir, huruf
```

### Langkah 2 — Identifikasi Regulasi Inti

1. Hitung untuk setiap regulasi: **berapa banyak penugasan input yang memakainya** (dari `matriks-kriteria.xlsx`)
2. Sortir desc berdasarkan jumlah pemakaian
3. **Regulasi inti** = top-3 regulasi yang muncul di **≥80%** penugasan input

Contoh hasil:
```
Regulasi inti penugasan-2026-014, 2026-021, 2026-027:
- Permen Komdigi Nomor X Tahun 2024 (3/3 = 100%) ← inti
- PP 53/2000 tentang Penggunaan Spektrum (3/3 = 100%) ← inti
- UU 36/1999 tentang Telekomunikasi (3/3 = 100%) ← inti
- Perdirjen Y/2025 (2/3 = 67%) — pendukung, bukan inti
```

### Langkah 3 — Sintesis Domain dari Regulasi Inti

Kombinasikan:
- **Term TF-IDF** dari Langkah 1
- **Subjek matter** regulasi inti dari Langkah 2

Cocokkan dengan tabel domain berikut (perluas seiring waktu):

| Pola Term/Regulasi | Domain | Topik Tag |
|--------------------|--------|-----------|
| frekuensi, spektrum, BHP, telekomunikasi + UU 36/1999 / PP 53/2000 | frekuensi-spektrum | bantuan-frekuensi, izin-frekuensi |
| pos, persuratan, jasa kurir + UU 38/2009 | pos-logistik | jasa-pos, kurir |
| siber, keamanan, insiden + UU 27/2022 / PP 71/2019 | keamanan-siber | siber, perlindungan-data |
| siaran, lembaga penyiaran + UU 32/2002 | penyiaran | konten-siaran, frekuensi-siaran |
| BAKTI, USO, daerah 3T + Perpres BAKTI | bakti-uso | layanan-3T, infrastruktur-tertinggal |
| literasi digital, talenta digital + Permen Komdigi terkait | literasi-digital | talenta-digital, sdm-tik |
| data center, PSrE, sertifikat elektronik + UU ITE | infrastruktur-tik | psre, data-center |
| bantuan, hibah, BAST + PMK 168/2023 | hibah-bantuan | bantuan-pemerintah |
| TIK pemerintahan, SPBE + Perpres 95/2018 | spbe | aplikasi-pemerintahan |

Jika tidak ada pola yang cocok dengan ≥3 term inti, masukkan ke kategori **"general"** dan minta auditor input nama domain manual.

## Algoritma Penamaan Skill

### Format Wajib

```
{fungsi}-{topik-singkat}
```

Aturan:
- `fungsi` = `audit | reviu | pemantauan | evaluasi | konsultansi` (turun dari parent skill)
- `topik-singkat` = lowercase, dash-separated, **2–4 kata**, deskriptif

### Aturan Penamaan

**WAJIB:**
- Lowercase semua
- Pisah kata dengan `-` (dash), bukan `_` atau spasi
- Maksimal 4 kata di bagian topik
- Bahasa Indonesia (kecuali istilah teknis yang baku)
- Tidak ambigu — orang yang baca nama harus paham domain

**HINDARI:**
- Singkatan yang tidak umum (mis. `audit-pemf-spek` → bingung)
- Nama generik (`audit-khusus`, `reviu-umum-tahap2`)
- Nama yang terlalu panjang (>30 karakter)
- Nama yang konflik dengan skill spesifik existing

### Contoh Penamaan Baik vs Buruk

| Buruk | Baik | Alasan |
|-------|------|--------|
| `audit-frek` | `audit-bantuan-frekuensi` | "frek" terlalu singkat, ambigu |
| `reviu-bakti-2026` | `reviu-pengadaan-bakti` | tahun bukan bagian domain |
| `evaluasi-permen-12` | `evaluasi-implementasi-permen-pdp` | nomor permen bukan domain |
| `pemantauan-kegiatan-direktif-presiden-q1-2026` | `pemantauan-direktif-presiden` | terlalu panjang |
| `konsultansi-it` | `konsultansi-pengadaan-tik` | "IT" terlalu generik |

### Cek Konflik Nama

Sebelum menyusun draft, jalankan cek:

```python
existing_skills = list_dir("audit-system-v4/skills/")
existing_drafts = list_dir("audit-system-v4/skills/_draft/")
nama_diusulkan = f"{fungsi}-{topik_singkat}"

if nama_diusulkan in existing_skills + existing_drafts:
    raise NameConflict(f"{nama_diusulkan} sudah ada — pilih nama lain atau gabung dengan yang ada")
```

Jika konflik, opsi:
1. Beri sufiks pembeda yang bermakna (mis. `reviu-bantuan-frekuensi` vs `reviu-bantuan-frekuensi-pita-rendah`)
2. Konsultasi dengan auditor — apakah graduasi ini sebaiknya **memperkaya skill yang ada** alih-alih buat baru?

### Konfirmasi ke Auditor (Wajib)

Sebelum melanjut ke Gate 2, tampilkan:

```
🎯 Deteksi Domain Selesai

Penugasan input:
- 2026-014 (Reviu Bantuan Frekuensi Pita 800 MHz)
- 2026-021 (Reviu Bantuan Frekuensi Pita 1800 MHz)
- 2026-027 (Reviu Bantuan Frekuensi Pita 2300 MHz)

Domain terdeteksi: **bantuan-frekuensi**

Regulasi inti (≥80% pakai):
- UU 36/1999 tentang Telekomunikasi
- PP 53/2000 tentang Penggunaan Spektrum Radio
- Permen Komdigi Nomor 12/2024 tentang Bantuan Frekuensi

Term inti (top-10 TF-IDF):
- frekuensi (87 occ)
- spektrum (54 occ)
- BHP (42 occ)
- ...

Usulan nama skill: **reviu-bantuan-frekuensi**

Apakah disetujui?
[YA — lanjut Gate 2] / [TIDAK — saya input nama lain] / [BATAL]
```

## Catatan Penting

- Domain yang diberi nama generik ("audit-umum-x") akan ditolak — auditor harus input nama yang lebih spesifik
- Jika auditor 3x menolak usulan domain, sistem ber-fallback ke mode "manual input nama" — auditor mengetik nama final
- Nama yang diberikan auditor tetap divalidasi terhadap aturan format (lowercase, dash-separated, dst) — sistem auto-correct dan konfirmasi sebelum melanjut
