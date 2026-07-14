# Survey Pendahuluan Audit Kinerja — Research Online & Template Memo SP

> Reference detail untuk tahap **Survey Pendahuluan** skill `audit-kinerja`. Substansi ringkas + langkah ada di `SKILL.md` (seksi "Survey Pendahuluan"); di sini **detail research online** (whitelist sumber, aturan anti-halusinasi) + **template Memo Survey Pendahuluan** lengkap. Baca via `read_skill_reference("audit-kinerja", "09-survey-pendahuluan-memo-research.md")`.

## Research Online — Benchmarking & Best Practice

> **Dasar:** Untuk menghindari audit kinerja yang self-referential (hanya mengacu pada dokumen internal), survey pendahuluan diperkaya dengan referensi eksternal. Karena kriteria utama tetap dari proses bisnis internal, research online hanya berfungsi sebagai **konteks pembanding & penajaman risiko** — **bukan** kriteria utama yang dipakai menjustifikasi temuan.

**Empat jenis research yang harus dicari:**

| Jenis | Contoh Query | Kegunaan |
|-------|-------------|----------|
| **Benchmark K/L lain di Indonesia** | "audit kinerja program [sejenis] BPK", "laporan kinerja [program sejenis] kementerian", "LKj [K/L sejenis] [tahun]" | Membandingkan target, realisasi, dan pendekatan K/L sejenis |
| **Best practice internasional** | "OECD best practice [sektor program]", "World Bank performance audit [topik]", "INTOSAI performance audit guideline [topik]" | Standar pembanding untuk menilai kewajaran target & proses |
| **Regulasi & pedoman teknis** | "Permen/SE [instansi pembina] [topik] [tahun]", "Pedoman teknis [program] Bappenas/KemenPAN-RB/Kemenkeu" | Memastikan kriteria internal tidak konflik dengan regulasi terbaru |
| **Hasil audit/riset akademis** | "temuan BPK [program sejenis]", "hasil audit BPKP [sektor]", "kajian [topik program] jurnal" | Dasar hipotesis risiko — area yang sudah terbukti bermasalah di tempat lain |

**Alur research:**

1. Dari konteks penugasan + TOR/KAK, identifikasi 3–5 kata kunci inti program (nama program, sektor, jenis output, instansi pembina).
2. Jalankan pencarian web untuk masing-masing dari 4 jenis di atas (minimal 1 query per jenis).
3. Untuk setiap hasil relevan, **baca sumber aslinya** — jangan menyimpulkan hanya dari snippet.
4. Catat untuk setiap temuan research: **Judul sumber** (lengkap) · **URL lengkap** · **Tanggal akses** · **Ringkasan faktual** (2–4 kalimat, tanpa interpretasi) · **Relevansi** (1 kalimat).
5. Filter: buang hasil tidak relevan, tidak bisa diakses penuh, atau dari sumber non-otoritatif (blog tanpa kredensial, situs komersial SEO).
6. Simpulkan sebagai input untuk pemetaan risiko & analytical review.

**Sumber dipercaya (whitelist indikatif):** `.go.id` (K/L, BPK, BPKP, Bappenas, KemenPAN-RB, Kemenkeu) · `bpk.go.id`, `bpkp.go.id` · `oecd.org`, `worldbank.org`, `un.org`, `intosai.org` · jurnal akademis (`doi.org`, `scholar.google`, repositori universitas).

**Sumber ditolak:** blog tanpa identitas penulis jelas · situs SEO/content farm · situs berita populer tanpa data primer · media sosial/forum.

**Aturan anti-halusinasi research online:**
- **Setiap klaim WAJIB disertai URL + tanggal akses** — tidak ada URL = tandai `[DIISI AUDITOR]`.
- **Jangan parafrasa angka tanpa sumber** — kutipan angka harus mencantumkan laporan sumber + halaman/bagian.
- **Sumber tidak dapat diakses penuh** (paywall, 403, PDF rusak) → jangan gunakan snippet sebagai basis klaim; tandai *"perlu verifikasi oleh auditor"*.
- **Research tidak menemukan sumber memadai** untuk salah satu jenis → nyatakan eksplisit di Memo SP *"Tidak ditemukan sumber memadai untuk [jenis]; auditor diminta memberi arahan"*.
- **Jangan jadikan hasil research kriteria tunggal** untuk temuan — hanya konteks pembanding; kriteria utama tetap dari proses bisnis/SOP/PK program.

## Output — Template Memo Survey Pendahuluan

Disusun sebelum KP + PKP. Struktur minimal:

```
MEMO SURVEY PENDAHULUAN
SP/[nomor-penugasan]/IJ.3/KP.01.06/[bulan]/[tahun]

A. Dasar Penugasan      : [Nomor ST]
B. Program yang Diaudit : [Nama program]
C. Unit Pelaksana       : [Unit]

1. GAMBARAN UMUM PROGRAM
   - Tujuan program (dari TOR/KAK)
   - Logika intervensi (Input → Proses → Output → Outcome)
   - Anggaran dan sumber daya
   - IKU utama dan target PK

2. BENCHMARKING & BEST PRACTICE (Research Online)
   2.1 Benchmark K/L Lain di Indonesia
       | No | Sumber | URL | Tgl Akses | Ringkasan Faktual | Relevansi |
       |----|--------|-----|-----------|-------------------|-----------|
   2.2 Best Practice Internasional (OECD / World Bank / INTOSAI / dll)
       | No | Sumber | URL | Tgl Akses | Ringkasan Faktual | Relevansi |
       |----|--------|-----|-----------|-------------------|-----------|
   2.3 Regulasi & Pedoman Teknis Terbaru (instansi pembina)
       | No | Sumber | URL | Tgl Akses | Ringkasan Faktual | Relevansi |
       |----|--------|-----|-----------|-------------------|-----------|
   2.4 Hasil Audit BPK/BPKP & Riset Akademis atas Program Sejenis
       | No | Sumber | URL | Tgl Akses | Ringkasan Faktual | Relevansi |
       |----|--------|-----|-----------|-------------------|-----------|
   2.5 Catatan sumber yang TIDAK ditemukan / perlu verifikasi auditor
       [daftar eksplisit jenis yang tidak bisa diisi — jangan kosongkan diam-diam]

3. PEMETAAN RISIKO KINERJA (per aspek)
   | No | Aspek (1–8) | Risiko Efektivitas | Risiko Efisiensi | Tingkat Risiko | Dasar Risiko (internal/benchmark) |
   |----|-------------|--------------------|-|----------------|-----------------------------------|

4. ANALYTICAL REVIEW AWAL
   - Target vs realisasi IKU (indikasi awal)
   - % serapan anggaran vs % capaian fisik
   - Perbandingan dengan benchmark K/L lain atau best practice (jika tersedia)
   - Anomali yang teridentifikasi

5. AREA FOKUS AUDIT (hasil prioritas risiko)
   [2–4 area terpilih, sebutkan referensi baris Bagian 2 yang mendukung jika relevan]

6. PENAJAMAN SASARAN AUDIT
   Sasaran dari ST (asli)        : [verbatim]
   Sasaran setelah penajaman     :
     1. [sasaran spesifik per area fokus]
     2. [sasaran spesifik per area fokus]
     ...

7. RUANG LINGKUP TERUKUR
   - Periode diaudit         : [tanggal]
   - Unit/lokasi sampel      : [daftar]
   - Aspek 2E yang diuji     : [Efektivitas / Efisiensi / keduanya]
   - Batasan audit           : [eksplisit]

8. HIPOTESIS AUDIT AWAL
   [dugaan temuan yang akan diuji → dasar langkah kerja PKP]

9. DOKUMEN YANG MASIH DIBUTUHKAN
   [daftar dokumen yang harus diminta sebelum pengujian]

Disusun oleh: [Ketua Tim]         Tanggal: [...]
Disetujui oleh: [Pengendali Teknis] Tanggal: [...]
```
