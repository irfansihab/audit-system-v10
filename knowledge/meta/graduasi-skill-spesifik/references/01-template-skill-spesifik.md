# Template Skill Spesifik (Hasil Graduasi)

Template ini dipakai saat menghasilkan SKILL.md baru di `_draft/[nama-skill]/SKILL.md`. Variabel `{{...}}` diisi otomatis dari hasil Gate 1–3.

---

## Frontmatter Wajib

```yaml
---
name: {{nama_skill}}                    # contoh: reviu-bantuan-frekuensi
version: 0.1                            # selalu 0.1 untuk hasil graduasi
status: draft-pending-approval          # status awal — wajib
jenis: {{jenis_pengawasan}}             # contoh: Reviu (spesifik domain X)
fungsi: {{fungsi_apip}}                 # Assurance/Consulting (turun dari parent)
output: {{format_output}}               # turun dari parent skill
parent_skill: {{nama_skill_umum}}       # audit-umum/reviu-umum/dst
derived_from:                           # ID penugasan sumber
  - {{penugasan_id_1}}
  - {{penugasan_id_2}}
generated_at: {{ISO_timestamp}}
generated_by: graduasi-skill-spesifik v1.0
model: claude-sonnet-4-6
---
```

## Struktur Body SKILL.md Hasil Graduasi

```markdown
# Skill: {{Nama Skill — Title Case}}

> **⚠️ STATUS DRAFT** — Skill ini hasil graduasi otomatis dari skill umum {{parent_skill}}.
> Wajib direview oleh auditor sebelum di-promote ke `skills/`.

## Identitas
- **Nama Skill:** {{nama_skill}}
- **Versi:** 0.1 (draft hasil graduasi)
- **Jenis Pengawasan:** {{jenis_pengawasan_detail}}
- **Fungsi APIP:** {{fungsi_apip_label}}
- **Domain:** {{domain_topik}} (mis. "Bantuan Frekuensi Radio", "Pemanfaatan Spektrum", dst)
- **Format Output:** {{format_output_detail}}
- **Kode Surat:** {{kode_surat}}
- **Model AI:** Claude Sonnet 4.6

## Asal Skill (Audit Trail Graduasi)

Skill ini dihasilkan otomatis dari **{{N}} penugasan** yang dikerjakan dengan skill umum **{{parent_skill}}**:

| ID Penugasan | Tanggal | Objek |
|--------------|---------|-------|
| {{penugasan_1}} | {{tgl_1}} | {{objek_1}} |
| {{penugasan_2}} | {{tgl_2}} | {{objek_2}} |
| ... | ... | ... |

**Statistik graduasi:**
- Regulasi core (≥80% pakai): **{{n_core}}** kriteria
- Regulasi pendukung (50–80%): **{{n_frequent}}** kriteria
- Red flag built-in: **{{n_redflag}}** pola
- Pipeline script: **{{ada_tidak_ada}}**

## Kapan Skill Ini Digunakan

Skill ini cocok untuk pengawasan yang berkaitan dengan **{{domain_topik}}**, dengan ciri-ciri:
{{daftar_ciri_dari_penugasan_sumber}}

**Jangan gunakan ketika:**
- Topik di luar {{domain_topik}} → gunakan {{parent_skill}}
- Domain spesifik lain yang sudah punya skill khusus

## Peran Claude

{{turunkan_dari_parent_skill_dengan_kontekstualisasi_domain}}

Penekanan khusus untuk domain {{domain_topik}}:
{{penekanan_dari_pola_temuan_yang_dimining}}

## Input Contract

```
penugasan/[ID]/
├── 00-surat-tugas/
├── input/
│   ├── kriteria/        # ← Kriteria sudah ada built-in di references/
│   │                    #    Auditor boleh tambah regulasi spesifik
│   ├── objek/           # ← Dokumen objek
│   └── data-pendukung/
├── _KKP/
└── _LHP/
```

**Beda dari skill umum:** kriteria utama sudah built-in di `references/01-regulasi-utama.md` dan `references/02-regulasi-pendukung.md`. Auditor tidak perlu unggah ulang regulasi yang sama untuk setiap penugasan.

## Workflow Gate-Based (Turunan dari {{parent_skill}})

{{salin_workflow_dari_parent_dengan_perubahan_minor}}

**Perubahan vs skill umum:**
- Gate 0: validasi kriteria diganti dengan validasi dokumen objek (kriteria sudah built-in)
- Gate 1: KP otomatis pakai template domain — auditor lebih banyak edit, sedikit tulis dari nol
- Gate 3: pakai checklist & red flag built-in dari `references/03-checklist-redflag.md`
- {{tambahan_otomasi_jika_ada_pipeline_script}}

## Format Output

{{salin_dari_parent}}

**Tambahan domain-specific:**
{{format_khusus_yang_muncul_dari_penugasan_sumber}}

## Materialitas / Aturan Khusus Domain

{{turunkan_ambang_dari_temuan_yang_diobservasi}}

## Bahasa & Batasan

{{turunkan_dari_parent}}

**Spesifik domain:**
{{istilah_domain_yang_harus_dipakai_atau_dihindari}}

## Output JSON KKP

{{schema_json_dari_parent_dengan_field_domain}}

## Referensi Wajib Dibaca
- `references/01-regulasi-utama.md` — core regulasi domain {{domain_topik}}
- `references/02-regulasi-pendukung.md` — regulasi pendukung
- `references/03-checklist-redflag.md` — checklist & red flag built-in
- `audit-system-v4/skills/panduan-format-umum/PANDUAN.md`
- `audit-system-v4/skills/{{parent_skill}}/SKILL.md` — workflow dasar

## Catatan Promote

Saat skill ini di-promote ke `skills/`:
1. Hapus `> ⚠️ STATUS DRAFT` banner
2. Update `version: 0.1` → `version: 1.0`
3. Hapus `status: draft-pending-approval`
4. Update `audit-system-v4/skills/README-skills-umum.md` — tambah ke decision tree
5. Update `audit-system-v4/feedback/graduasi-log.json` (status: approved-promoted)
6. Update memory file user
```

## Aturan Pembentukan Konten

### Bagian Identitas
- `nama_skill` selalu lowercase, dash-separated, format `[fungsi]-[topik]`
- `domain_topik` Title Case, deskriptif (mis. "Bantuan Frekuensi Radio", bukan "frekuensi")
- `jenis_pengawasan_detail` turun dari parent + sufiks domain (mis. "Reviu Spesifik Domain Frekuensi Radio")

### Bagian Workflow
- Jangan ubah jumlah Gate dari parent (5 Gate untuk umum)
- Boleh tambah Gate 0a/0b sub-step jika domain butuh
- Boleh persempit lingkup di tiap Gate, tapi jangan hapus Gate

### Bagian References
- File 01 dan 02 harus berisi **kutipan langsung** dari regulasi (bukan paraphrase)
- File 03 harus dipisah per aspek (Perencanaan, Pelaksanaan, dst) sesuai pola di skill audit-pengadaan
- Setiap red flag harus ada **frekuensi** (mis. "muncul di 3 dari 5 penugasan sumber")

### Validasi Otomatis Sebelum Output

Sebelum menulis SKILL.md draft, verifikasi:
- [ ] Frontmatter valid YAML
- [ ] Field wajib ada (`name`, `version: 0.1`, `status: draft-pending-approval`, `parent_skill`, `derived_from`)
- [ ] Banner DRAFT ada di awal body
- [ ] Bagian "Asal Skill" terisi dengan ID penugasan sumber
- [ ] Bagian Referensi mencantumkan parent skill
- [ ] Tidak ada placeholder `{{...}}` yang belum diganti
