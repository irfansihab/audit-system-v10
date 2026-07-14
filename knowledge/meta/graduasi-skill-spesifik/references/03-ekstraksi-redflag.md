# Ekstraksi Pola Temuan & Red Flag (Mining)

Panduan algoritma untuk Gate 3 graduasi: bagaimana sistem menambang pola **kondisi yang sering muncul** dari penugasan-penugasan sebelumnya, lalu menyusunnya jadi **checklist & red flag built-in** untuk skill spesifik baru.

---

## Sumber Data

Untuk setiap penugasan input, baca:

1. `_KKP/temuan.json` (atau `catatan_reviu` / `items` / `pendapat` sesuai parent skill)
2. `_KKP/03-KKA-*.xlsx` sheet "Temuan" (atau equivalent)
3. `_LHP/LHA-[ID].docx` Bab Temuan (verifikasi konsistensi dengan KKP)

Field yang dipakai per temuan:
- `kondisi` — fakta yang ditemukan
- `kriteria_ids` — link ke matriks kriteria
- `aspek_terkait` (jika ada di matriks-kriteria)
- `level_risiko` — material/reguler/catatan
- `nilai_rp` (jika audit/evaluasi)

## Algoritma Mining

### Langkah 1 — Normalisasi Kondisi

Setiap teks `kondisi` di-normalisasi:

1. Lowercase
2. Hapus angka spesifik dan rupiah (mis. "Rp 245.000.000" → `<NILAI>`)
3. Hapus nama dokumen spesifik (mis. "Kontrak-PSrE-2026.pdf" → `<DOKUMEN>`)
4. Hapus tanggal (mis. "14 Februari 2026" → `<TANGGAL>`)
5. Stem kata kerja Indonesia (sederhana — pakai library Sastrawi atau equivalent jika ada)

Tujuan: kondisi yang berbeda nilai/dokumen/tanggal tetapi pola sama akan match.

Contoh:
```
Kondisi 1 (asli): "HPS pengadaan PSrE Induk ditetapkan tanggal 14 Februari 2026 sebesar Rp 12.500.000.000, namun penawaran dari penyedia masuk pada 5 Februari 2026."

Kondisi 1 (normalisasi): "hps pengadaan <DOKUMEN> tetap tanggal <TANGGAL> sebesar <NILAI>, namun penawaran dari penyedia masuk pada <TANGGAL>"

Kondisi 2 (asli): "HPS untuk pengadaan Data Center DRC ditetapkan 22 Januari 2026 nilai Rp 8.700.000.000, sementara penawaran sudah dimasukkan pada 18 Januari 2026."

Kondisi 2 (normalisasi): "hps untuk pengadaan <DOKUMEN> tetap <TANGGAL> nilai <NILAI>, sementara penawaran sudah masuk pada <TANGGAL>"

→ Pola yang sama: HPS ditetapkan SETELAH penawaran masuk
```

### Langkah 2 — Clustering Pola

Pakai pendekatan **lexical similarity** sederhana (tidak perlu ML):

1. Untuk setiap pasang kondisi normalisasi, hitung **token overlap ratio**:
   ```
   overlap = |intersection(tokens_A, tokens_B)| / |union(tokens_A, tokens_B)|
   ```
2. Gunakan **threshold 0.5** — pasangan dengan overlap ≥0.5 dianggap pola sama
3. Bangun cluster transitif (A∼B, B∼C → A∼C)

Alternatif (jika library tersedia): pakai TF-IDF + cosine similarity, threshold 0.6.

### Langkah 3 — Frekuensi & Filter

Untuk setiap cluster:
- Hitung jumlah **occurrences** (berapa kali pola muncul lintas penugasan)
- Hitung jumlah **distinct penugasan** yang punya pola ini
- Klasifikasi:

| Frekuensi | Klasifikasi | Aksi |
|-----------|-------------|------|
| ≥3 distinct penugasan | **Red Flag wajib** | Masuk checklist built-in |
| 2 distinct penugasan | **Pola berulang** | Masuk checklist sebagai catatan |
| 1 penugasan saja | **Pola tunggal** | Tidak masuk built-in (terlalu spesifik) |

### Langkah 4 — Penyusunan Pernyataan Red Flag

Untuk setiap cluster red flag, susun pernyataan generik:

**Template:**
```
[Aspek dominan dari kriteria yang dilanggar]:
- Indikasi: [pola dalam bahasa pengamatan, tanpa nilai/tanggal spesifik]
- Frekuensi sumber: [N] dari [M] penugasan
- Kriteria yang biasanya dilanggar: [daftar kriteria_id]
- Akibat khas: [pola akibat dari temuan-temuan dalam cluster]
```

**Contoh hasil:**
```
### A. Perencanaan / HPS

**Red Flag**: HPS ditetapkan setelah penawaran masuk
- Indikasi: tanggal penetapan HPS lebih lambat dari tanggal penawaran masuk yang pertama
- Frekuensi sumber: 3 dari 3 penugasan (100%)
- Kriteria biasa dilanggar: Perlem LKPP 12/2021 Pasal 26 ayat (5)
- Akibat khas: nilai HPS yang dapat di-back-engineering dari penawaran, kewajaran harga tidak dapat diuji
- Bukti yang harus dikumpulkan: dokumen pembentuk harga + tanggal-stamp HPS + tanggal-stamp penawaran terawal
```

### Langkah 5 — Pengelompokan per Aspek

Aspek diturunkan dari `aspek_terkait` di matriks-kriteria. Aspek standar:

- A. Perencanaan
- B. Pemilihan / Eligibility
- C. Kontrak / Komitmen
- D. Pelaksanaan / Operasional
- E. Pembayaran / Keuangan
- F. Serah Terima / Output
- G. Dokumentasi / Administrasi
- H. Lain-lain

Susun file `references/03-checklist-redflag.md` urut per aspek.

## Format Output `03-checklist-redflag.md`

```markdown
# Checklist & Red Flag Built-in — {{nama_skill}}

**Sumber:** Mining dari {{N}} penugasan ({{daftar_id}})
**Generated:** {{ISO_timestamp}}

---

## A. {{Aspek_1}}

### Checklist
- [ ] {{checklist_item_1}}
- [ ] {{checklist_item_2}}
- [ ] ...

### Red Flag

**RF-A1: {{judul_red_flag}}**
- **Indikasi**: {{pola_pengamatan}}
- **Frekuensi sumber**: {{N}} dari {{M}} penugasan ({{persen}}%)
- **Kriteria biasa dilanggar**: {{daftar_kriteria_id}} — {{ringkasan_pasal}}
- **Akibat khas**: {{pola_akibat}}
- **Bukti yang harus dikumpulkan**: {{daftar_bukti}}

**RF-A2: ...**
- ...

---

## B. {{Aspek_2}}

...
```

## Validasi Sebelum Output

Sebelum menulis `03-checklist-redflag.md`, lakukan:

- [ ] **Auditor review** — STOP & TANYA: tampilkan ringkasan red flag dan minta auditor approve/reject per item. Auditor boleh:
  - Approve (masuk file)
  - Reject (false positive, jangan masuk)
  - Edit (ubah pernyataan/akibat)
- [ ] **Konsistensi kriteria** — pastikan semua `kriteria_ids` yang dirujuk ada di matriks kriteria yang akan masuk skill baru
- [ ] **Tidak ada PII** — pastikan kondisi yang dinormalisasi tidak mengandung nama orang/penyedia spesifik yang tersisa
- [ ] **Bahasa generik** — pastikan teks red flag tidak menyebut penugasan asal (mis. "ini terjadi pada penugasan 2026-014")

## Khusus untuk Reviu/Konsultansi

- **Reviu**: tidak ada kolom Sebab → red flag fokus pada **kondisi yang tidak sesuai kriteria** (administratif/format), tanpa analisis akar masalah
- **Konsultansi**: tidak ada "temuan" sebab konsultansi tidak memberikan keyakinan. Mining mengambil dari `pendapat[].pertanyaan_id` yang **berulang lintas penugasan** → menjadi **FAQ built-in** alih-alih red flag

## Khusus untuk Pemantauan

Mining dilakukan terhadap `items[]` dengan status MERAH atau KUNING:
- Cluster pola **penyebab deviasi** yang berulang
- Cluster pola **rekomendasi percepatan** yang berulang
- Output: bukan red flag, melainkan **template item pemantauan** yang sudah punya kategori penyebab dan template intervensi

## Khusus untuk Evaluasi

Selain temuan KKSA, mining juga dilakukan terhadap **pola skoring**:
- Indikator yang sering dapat skor rendah → masuk **fokus pengujian** built-in
- Pola praktek terbaik dari penugasan dengan skor tinggi → masuk **benchmark** di references

## Catatan Implementasi

Untuk graduasi minimum (1 penugasan), semua "pola" sebenarnya frekuensi 1 — checklist & red flag dimasukkan dengan kualifikasi "**observasi tunggal — perlu validasi pada penugasan berikutnya**". Auditor akan tahu ini bukan pola statistik melainkan starting point yang akan diperkaya.
