# Audit AI v10 — Hardening, Penyelarasan Workflow, Simplifikasi

**Dibuat:** 1 Jul 2026 · **Fork dari:** v9 (`98e408a`, engine-ready 16/16) · **Repo:** https://github.com/irfansihab/audit-system-v10 (publik, riwayat v8→v9→v10 dipertahankan).

## Arah (pivot yang diwarisi dari v9)
Sistem AI = **ENGINE** (skills + agen + tools + digest/render). **Orkestrator + UI = INTEGRAL** (sistem terpisah). Skill = substansi murni & portabel. v10 melanjutkan pivot ini — bukan membangun UI/orkestrasi baru.

## Tiga fokus v10
1. **Hardening skill** — kualitas & ketahanan output tiap skill: reference yang benar (bukan rusak/legacy), terminologi baku (KKSAR), doktrin konsisten, checklist tajam, anti-halusinasi, uji kualitas terukur (eval harness + judge).
2. **Penyelarasan workflow dengan pedoman pengawasan** — tahapan/alur kerja diselaraskan ke Pedoman/Juknis Pengawasan (SK Standar Dokumen Penugasan Pengawasan). Prinsip v9 dipertahankan: **SK ikut sistem** (sistem = mesin produksi substansi), garis finis = **laporan disetujui**; setelah itu ranah administrasi.
3. **Simplifikasi fitur** — buang kompleksitas yang tak menambah nilai; kurangi dead code, konsolidasi tool/format, ramping-kan skill & prompt.

## Modal yang diwarisi dari v9 (sudah selesai)
- **Engine pivot** + **template engine-ready** (`docs/TEMPLATE-SKILL-ENGINE-READY.md`).
- **P0** doktrin Sebab/Akibat (KKSAR) konsisten lintas skill.
- **P3** dead-code dibuang (anomali pasca digest-only) + ramping SKILL gemuk + single-source matriks.
- **P1 strip skill TUNTAS — 16/16 skill substansi engine-ready** (orkestrasi direlokasi ke prompt/INTEGRAL): PBJ 4 + Kinerja 3 + Umum 9. Doktrin per-grup terjaga; pilot tervalidasi live + uji kualitas judge (precision 1.0, unsur 100%, kriteria 100%, narasi 1.0).

## Backlog awal v10 (lanjutan v9 — lihat `docs/SKILL-AUDIT-BACKLOG-v9.md`)
- **P1c** — lepas `render_kkp_docx` & `read_context` dari DB → kontrak file (`_KKP/hitl-overlay.json`) + hook backend materialisasi (hybrid file→fallback DB) + uji live. *Satu-satunya sisa P1 yang menyentuh backend.*
- **P1#8** — de-UI prompt agen (`anggota_tim.md`/`ketua_tim.md`): "tab Setup/via UI"/status → kontrak file.
- **P2** — terminologi (CCSAA→KKSAR, 3E→2E), reference rusak/legacy (`audit-system-v4`, TODO absen), reviu-rka-kl jejak rule→checklist, versi/frontmatter konsisten.
- **P4** — kepatuhan-saipi & graduasi = meta-skill → INTEGRAL/tooling.
- **BARU (fokus #2)** — audit workflow/tahapan vs Pedoman Pengawasan; petakan gap; selaraskan tanpa mengorbankan "mesin produksi".

## Setup lokal
- `.env` sudah di-rewrite path v9→v10 + DB `audit_v10`; `backend/.env` symlink → `../.env`; vault `llm-wiki/` (217 catatan, gitignored) disalin; DB `audit_v10` dibuat (container `sistemauditv7-db-1`).
- **Regenerate dependensi** (tidak ikut clone): `cd backend && python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt`; `cd frontend && npm install`.
- Jalankan: backend `uvicorn app.main:app --port 8001`, frontend `npm run dev` (:3000). FE/BE tetap **harness uji-coba** (bukan produk final — produksi pakai INTEGRAL).
