---
name: graduasi-skill-spesifik
version: 1.0
jenis: Meta-skill — Auto-generate skill spesifik dari penugasan
fungsi: Pengembangan Sistem (bukan pengawasan)
output: Draft skill folder di `audit-system-v4/skills/_draft/[nama-skill]/`
trigger: Manual command auditor
---

# Skill: Graduasi Skill Spesifik (Meta-Skill)

## Identitas
- **Nama Skill:** graduasi-skill-spesifik
- **Versi:** 1.0 (Mei 2026)
- **Jenis:** Meta-skill — bukan untuk pengawasan, melainkan untuk **mengembangkan skill baru** berdasarkan pola penugasan yang sudah dilakukan
- **Trigger:** Manual — auditor jalankan saat dirasa cukup pola
- **Model AI:** Claude Sonnet 4.6 (via Cowork)

## Tujuan

Skill ini menyaring **pola berulang** dari satu atau lebih penugasan yang dikerjakan dengan **skill umum** (audit-umum, reviu-umum, dst) lalu menghasilkan **skill spesifik baru** dalam format draft. Tujuannya:

- Mempercepat skill spesifik baru: tidak perlu menulis SKILL.md dari nol
- Menangkap kearifan operasional yang muncul dari penugasan nyata (red flag, checklist, pola temuan)
- Konsolidasi kriteria yang dipakai berulang menjadi references yang siap pakai
- Menyiapkan template output (xlsx + docx) yang sudah disesuaikan dengan domain

## Trigger & Mode Operasional

**Manual, mode batch (Recommended: Jumat sore mingguan).**

Graduasi **dipisahkan dari workflow penugasan** agar penugasan tetap cepat. Auditor melakukan sesi graduasi terpisah, biasanya:
- **Mingguan** — setiap Jumat sore (default Inspektorat II)
- **Bulanan** — akhir bulan jika kandidat masih sedikit

### Workflow Sesi Batch (Recommended)

```
Setiap Jumat sore:
1. Scan kandidat
   python graduasi.py --candidates [--only-unscheduled]
   → Sistem tampilkan daftar penugasan yang sudah Gate 4 dengan skill umum,
     dikelompokkan per parent skill (audit/reviu/dll), urut tanggal selesai.

2. Pilih cluster yang siap digraduasi (≥3 penugasan dengan domain mirip)
3. Eksekusi graduasi untuk tiap cluster:
   graduasi-skill --penugasan ID1 ID2 ID3 --nama [usulan-nama]

4. Review draft di skills/_draft/ (boleh ditunda ke sesi berikutnya)
5. Promote / reject sesuai keputusan
```

### Trigger Eksekusi Manual

```
graduasi-skill --penugasan [ID-PENUGASAN-1] [ID-PENUGASAN-2 ...] --nama [usulan-nama-skill]
```

Atau berdialog dengan Claude:

> "Sekarang sesi batch Jumat. Tolong scan kandidat graduasi dulu, lalu graduate cluster yang siap."

### Kenapa Tidak Auto-Trigger di Akhir Penugasan

- ❌ Auto-trigger akan **memperlama proses penugasan** — auditor harus tunggu graduasi selesai sebelum lapor ke pimpinan
- ❌ Per-1-penugasan graduasi menghasilkan skill yang **belum stabil polanya** (data terlalu sedikit)
- ✅ Mode batch memberi waktu untuk **akumulasi pola** lintas penugasan
- ✅ Sesi batch terpisah memungkinkan **fokus penuh** pada review draft tanpa tekanan operasional

## Input Contract

```
Input minimum: ≥1 penugasan yang sudah selesai Gate 4 dengan skill umum
Input ideal:   ≥3 penugasan dengan domain yang sama
Input premium: ≥5 penugasan → ditambah pipeline script Python
```

Per penugasan, Claude akan baca:
- `00-surat-tugas/` → tipe penugasan, lingkup
- `input/kriteria/` → daftar regulasi yang dipakai
- `_KKP/matriks-kriteria.xlsx` → kriteria terindeks
- `_KKP/temuan.json` (atau equivalent) → pola temuan, red flag
- `_KKP/03-KKA-*.xlsx` (atau KKR/KKE/KKM/KKK) → checklist yang sudah teruji
- `_LHP/` → format laporan yang sudah disetujui

## Workflow Gate-Based

### Gate 0 — Validasi Input
1. Verifikasi setiap penugasan input sudah lengkap (Gate 4 done, ada `_KKP/` dan `_LHP/`)
2. Verifikasi semua memakai skill umum yang **sama** (mis. semua reviu-umum, atau semua audit-umum) — graduasi lintas-fungsi tidak diizinkan
3. Hitung kelengkapan data:
   - 1 penugasan → graduasi minimum (SKILL.md + references)
   - 2–4 penugasan → graduasi standar (+ checklist & red flags konsolidasi)
   - ≥5 penugasan → graduasi penuh (+ pipeline script Python)
4. **STOP & TANYA AUDITOR:**
   - Konfirmasi daftar penugasan input
   - Konfirmasi nama skill yang diusulkan (lihat references/02-pola-deteksi-domain.md)
   - Konfirmasi tingkat graduasi (minimum/standar/penuh)

### Gate 1 — Deteksi Domain & Penamaan
**Output:** `_skill-draft-meta/01-domain.md`

1. Baca `input/kriteria/` semua penugasan input
2. Identifikasi:
   - **Topik utama** dari frekuensi term di kriteria (mis. "frekuensi", "BHP", "telekomunikasi" → bantuan-frekuensi)
   - **Regulasi inti** (regulasi yang dipakai di **semua** penugasan input)
   - **Aspek pengawasan** dominan (perencanaan/pelaksanaan/keuangan/dll)
3. Usulkan nama skill: `[fungsi]-[topik]` (mis. `reviu-bantuan-frekuensi`, `audit-pemanfaatan-spektrum`)
4. **STOP & TANYA AUDITOR:** konfirmasi nama final + alasan pemilihan

### Gate 2 — Konsolidasi Kriteria
**Output:** `_skill-draft-meta/02-konsolidasi-kriteria.xlsx`

1. Gabungkan `matriks-kriteria.xlsx` dari semua penugasan input
2. Deduplikasi (sumber + pasal sama → satu entri)
3. Hitung **frekuensi pemakaian** (di berapa penugasan kriteria ini muncul?)
4. Klasifikasi:
   - **Core** — dipakai di ≥80% penugasan → masuk ke `references/01-regulasi-utama.md`
   - **Frequent** — dipakai di 50–80% → `references/02-regulasi-pendukung.md`
   - **Optional** — dipakai di <50% → catat tapi tidak masuk references skill baru
5. **STOP & TANYA AUDITOR:** konfirmasi pemisahan core/frequent/optional

### Gate 3 — Mining Pola Temuan & Red Flag
**Output:** `_skill-draft-meta/03-checklist-redflag.md`

1. Baca semua `temuan.json` dari penugasan input
2. Untuk setiap temuan, ekstrak pola:
   - **Aspek** yang ditemukan
   - **Kondisi pattern** (mis. "HPS ditetapkan setelah penawaran")
   - **Kriteria yang dilanggar** (link ke matriks)
3. Cluster pola yang mirip
4. Untuk cluster dengan ≥2 occurrences, jadikan **red flag built-in**
5. Susun checklist per aspek dengan format:
   ```
   ### [Aspek]
   - [ ] **[Kriteria singkat]** — [pertanyaan pengujian]
   - [ ] ...

   **Red Flag**:
   - [pola pattern yang muncul ≥2x]
   ```
6. **STOP & TANYA AUDITOR:** review red flags sebelum dimasukkan ke skill baru (red flag yang false positive harus dibuang)

### Gate 4 — Generate Skill Draft

**Output struktur di `audit-system-v4/skills/_draft/[nama-skill]/`:**

```
_draft/[nama-skill]/
├── SKILL.md                          # Frontmatter + identitas + workflow + format output
├── references/
│   ├── 01-regulasi-utama.md          # Core regulasi (≥80% pakai)
│   ├── 02-regulasi-pendukung.md      # Frequent regulasi
│   └── 03-checklist-redflag.md       # Mining hasil
├── templates/
│   ├── KKA-template.xlsx             # Template kertas kerja
│   └── LHA-skeleton.docx             # Skeleton laporan
├── scripts/                          # Hanya jika ≥5 penugasan
│   ├── digest.py                     # Skeleton script pre-digest
│   ├── cross_check.py                # Skeleton script rules
│   └── README.md                     # Cara pakai pipeline
└── METADATA.md                       # Origin, tanggal graduasi, penugasan sumber, status approval
```

**SKILL.md** dihasilkan dari template (lihat `references/01-template-skill-spesifik.md`) dengan field:
- `name:` = nama final dari Gate 1
- `version: 0.1` (draft)
- `status: draft-pending-approval`
- `derived_from:` = list ID penugasan input
- `parent_skill:` = skill umum asal
- `generated_at:` = ISO timestamp

**METADATA.md** wajib berisi:
- Tanggal graduasi
- Auditor yang melakukan graduasi
- Daftar penugasan sumber
- Statistik (jumlah kriteria core/frequent, jumlah red flag, dst)
- Status: `draft-pending-approval` | `approved-promoted` | `rejected`
- Reviewer + tanggal approval (kosong saat draft)

### Gate 5 — Review & Promote (Manual oleh Auditor)

Setelah Gate 4, Claude tampilkan ringkasan:

```
✅ Skill draft selesai dihasilkan: _draft/[nama-skill]/

Statistik:
- Penugasan sumber: N
- Regulasi core: x
- Regulasi pendukung: y
- Red flag built-in: z
- Pipeline script: ada/tidak ada

Lokasi: audit-system-v4/skills/_draft/[nama-skill]/

Langkah berikut (manual oleh auditor):
1. Review SKILL.md, references/, dan checklist red flag
2. Edit/refine jika perlu
3. Untuk promote ke skill aktif: pindahkan folder dari _draft/ ke skills/
   atau jalankan: graduasi-skill --promote [nama-skill]
4. Untuk reject: hapus folder atau jalankan: graduasi-skill --reject [nama-skill]
```

## Format Output Wajib di Setiap Tingkat Graduasi

| Output | Minimum (1 penugasan) | Standar (2-4) | Penuh (≥5) |
|--------|----------------------:|---------------:|-----------:|
| SKILL.md | ✅ | ✅ | ✅ |
| references/01-regulasi-utama.md | ✅ | ✅ | ✅ |
| references/02-regulasi-pendukung.md | (skip) | ✅ | ✅ |
| references/03-checklist-redflag.md | basic | ✅ konsolidasi | ✅ + frequency stats |
| templates/KKA-template.xlsx | ✅ | ✅ | ✅ |
| templates/LHA-skeleton.docx | ✅ | ✅ | ✅ |
| scripts/digest.py | (skip) | (skip) | ✅ skeleton |
| scripts/cross_check.py | (skip) | (skip) | ✅ skeleton |
| METADATA.md | ✅ | ✅ | ✅ |

## Yang TIDAK Dilakukan oleh Skill Ini

- ❌ Tidak menggantikan judgement auditor — graduasi adalah **draft** yang wajib direview
- ❌ Tidak otomatis promote — promote selalu butuh perintah manual auditor
- ❌ Tidak generate pipeline script untuk graduasi minimum/standar (data terlalu sedikit untuk pattern matching deterministik)
- ❌ Tidak mengubah skill umum atau skill spesifik yang sudah ada (operasinya read-only terhadap skills/ existing)
- ❌ Tidak melakukan graduasi lintas-fungsi (mis. menggabungkan pola audit-umum + reviu-umum jadi skill baru — itu beda assurance level)

## Pre-Conditions

Sebelum menjalankan graduasi, pastikan:
- [ ] Semua penugasan input sudah selesai Gate 4 (LHA/LHR/dll sudah dikirim)
- [ ] `_KKP/temuan.json` ada dan valid JSON
- [ ] `_KKP/matriks-kriteria.xlsx` ada
- [ ] Tidak ada penugasan yang masih dalam mode "draft revisi"
- [ ] Penugasan input semuanya pakai skill umum yang sama

Jika pre-condition tidak terpenuhi, **STOP** di Gate 0 dan beri daftar perbaikan.

## Audit Trail

Setiap graduasi dicatat di `audit-system-v4/feedback/graduasi-log.json`:

```json
[
  {
    "timestamp": "2026-05-05T14:30:00+07:00",
    "auditor": "Inspektorat II",
    "nama_skill": "reviu-bantuan-frekuensi",
    "parent_skill": "reviu-umum",
    "penugasan_sumber": ["2026-014", "2026-021", "2026-027"],
    "tingkat_graduasi": "standar",
    "status": "draft-pending-approval",
    "promoted_at": null,
    "promoted_to": null
  }
]
```

Saat di-promote/reject, log ini di-update.

## Referensi Wajib Dibaca
- `references/01-template-skill-spesifik.md` — skeleton SKILL.md hasil graduasi
- `references/02-pola-deteksi-domain.md` — algoritma deteksi nama & topik
- `references/03-ekstraksi-redflag.md` — algoritma mining red flag dari temuan
- `scripts/graduasi.py` — implementasi end-to-end (opsional jika manual)
