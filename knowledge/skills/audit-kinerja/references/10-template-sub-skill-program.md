# Template Membangun Sub-Skill Program (audit-kinerja-<program>)

> Reference untuk skill `audit-kinerja` — cara membangun **sub-skill spesifik program** (turunan skill induk). Baca via `read_skill_reference("audit-kinerja","10-template-sub-skill-program.md")`. Terkait meta-skill `knowledge/meta/graduasi-skill-spesifik/`.

## Panduan Membangun Sub-Skill Program

Ketika auditor akan membangun sub-skill baru untuk program tertentu, gunakan struktur berikut:

```
audit-kinerja-[nama-program]/
  SKILL.md               → Identitas + ref ke skill induk ini + kriteria spesifik program
  references/
    01-proses-bisnis.md  → Dikonversi dari dokumen proses bisnis yang diupload
    02-sop-[nama].md     → SOP atau juknis spesifik (jika ada, bisa lebih dari 1 file)
    03-target-iku.md     → IKU dan target dari PK tahun berjalan (opsional, bisa diupdate tiap tahun)
```

**Template SKILL.md sub-skill:**
```markdown
---
name: audit-kinerja-[nama-program]
version: "1.0"
parent-skill: audit-kinerja
---
# Audit Kinerja: [Nama Program]

## Identitas Program
- Nama program/kegiatan: [...]
- Unit pelaksana: [...]
- IKU utama: [...]
- Periode yang diaudit: [...]

## Kriteria Spesifik Program (organisir per aspek yang relevan dari 8 aspek)
[Diisi dari proses bisnis internal — tahapan kerja, standar output, target. Kelompokkan per aspek yang disasar program ini, mis. Kebijakan & Desain, Sistem-Proses-Teknologi, Pelaksanaan & Output, Outcome, Data Kinerja]

## Referensi
| Dokumen | File |
|---------|------|
| Proses bisnis internal | references/01-proses-bisnis.md |
| SOP [...] | references/02-sop-[nama].md |

## Catatan Khusus Program
[Hal-hal unik yang perlu diperhatikan auditor untuk program ini]
```
