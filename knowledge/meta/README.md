# knowledge/meta — Meta-skill & reference (BUKAN jenis pengawasan)

Folder ini menampung **meta-skill**: aset yang menopang sistem tapi **bukan skill pengawasan** yang bisa dipilih auditor untuk penugasan. Dipindah dari `knowledge/skills/` pada **Fase 3.3 (P4)** agar `knowledge/skills/` hanya berisi jenis pengawasan asli (audit/reviu/evaluasi/pemantauan/konsultansi).

| Folder | Peran | Runtime |
|---|---|---|
| `kepatuhan-saipi/` | **Referensi standar SAIPI** (Standar Audit Intern Pemerintah Indonesia / AAIPI 2021) — SAIPI-1100/1200/2200/2300/2400 + checklist per penugasan. Bahan penjaminan mutu (QC). | **Enforcement QC deterministik** di `backend/v6/scripts/qc_saipi.py` (dipanggil tool `run_qc_kkp`/`run_qc_lhp` via subprocess) — **tidak** memuat folder ini saat runtime; folder = dokumentasi standar. |
| `graduasi-skill-spesifik/` | **Meta-skill pengembangan**: cara membangun sub-skill spesifik program (deteksi domain, ekstraksi red-flag, template). | Algoritmanya sudah **di-port** ke `backend/app/graduasi.py` (self-contained); folder = referensi asal (cowork orchestrator). |

**Konsekuensi engine:**
- `app.skills_registry._scan()` hanya memindai `knowledge/skills/` → kedua folder ini **tak lagi terpindai** sebagai skill (tak perlu `_EXCLUDE_DIRS`/`_HIDDEN_FROM_PICKER`).
- Tak ada alur runtime yang `load_skill('kepatuhan-saipi')`/`load_skill('graduasi-skill-spesifik')` — QC & graduasi berjalan lewat kode backend, bukan pemuatan SKILL.md.

Bila kelak dibutuhkan sebagai reference yang dapat dibaca agen, sediakan tool pembaca terpisah yang menunjuk ke `knowledge/meta/` (bukan mengembalikannya ke `skills/`).
