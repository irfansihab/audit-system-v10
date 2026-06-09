# HANDOVER — INTEGRAL AI Workspace Sprint 3+4

> **Untuk sesi Claude berikutnya**: dokumen ini berisi konteks lengkap supaya bisa lanjut tanpa kehilangan progres.

**Update terakhir**: 2026-06-09 (Sprint 1+2 selesai, PR #9 merged)

---

## 🎯 Konteks Singkat

User (Inspektorat II Komdigi) sedang **mengintegrasikan Audit AI v7 ke SIMWAS v2 (simwasv2.komdigi.go.id)** — v7 menjadi **AI engine** di balik SIMWAS via REST API.

Visual rebrand: **"INTEGRAL AI Workspace · Powered by Audit AI v7"** dengan palette ungu `#5C4FE7`.

---

## ✅ Status: Sprint 1+2 SELESAI (PR #1-9 merged ke main)

| PR | Topik | Status |
|---|---|---|
| #1 | LiteParse + 3 hardcode deterministic | MERGED |
| #2 | HITL closure (filter+edit+auto-preload) | MERGED |
| #3 | CACM Fase 1 (diff UI + promote v7) | MERGED |
| #4 | Fix subprocess sys.executable | MERGED |
| #5 | Fix env ANTHROPIC_API_KEY | MERGED |
| #6 | Audit-pengadaan wire + Pendampingan format | MERGED |
| #7 | Digest generic 14 skill | MERGED |
| #8 | Workflow gap closure 17 skill | MERGED |
| #9 | **INTEGRAL AI Workspace Sprint 1+2** | MERGED |

---

## ⏸ Sprint 3-4 BELUM (sisa ~30 jam)

### S3.1 — Survey Pendahuluan section conditional (3 jam)
- Hanya muncul untuk skill `audit-pengadaan`, `audit-kinerja`, `audit-umum`
- UI: tahapan 0 di detail page → click → modal/section upload dokumen survey
- Backend: tool `read_survey_pendahuluan(folder)` + ekstensi prompt agen KT untuk extract risk profile
- Komponen: integrate dengan existing `HeroPenugasan.tsx`

### S3.2 — LRS LHP workflow (3 jam)
- DB model baru: `LhpReview(id, penugasan_id, reviewer_user_id, status: APPROVED|NEEDS_REVISION, catatan, reviewed_at)`
- Endpoint: `POST /penugasan/{id}/lhp-review` (PT/PM only)
- UI: panel di tab "Konsep Laporan" — tombol "Setujui sebagai PT" + "Minta Revisi" + textarea catatan
- Update HeroPenugasan `deriveStageStatus` untuk tahapan 6 (LRS LHP)

### S3.3 — Daftar Penugasan DataTable SIMWAS-style (4 jam)
- Install: `npm install @tanstack/react-table`
- Filter bar: Tahun (2026/2025/...) + Bulan + Pelaksana (multi) + tombol Export CSV
- Kolom: NO | JUDUL | PELAKSANA | JENIS | TANGGAL | (status per-tahapan ✓ icon)
- Search box + sort columns + pagination ("Show N entries")
- Title format SIMWAS: `Melakukan {jenis} atas {obyek} di Lingkungan {unit} TA {tahun} terhitung mulai tanggal {start} s.d. {end}`

### S3.4 — Menu CACM + Knowledge restructure (2 jam)
Sebagian sudah ke-handle di `Sidebar.tsx`. Sisa:
- Pisah `/knowledge` jadi 4 anchor: `#pattern`, `#kriteria-cacm`, `#template-kp`, `#writeback`
- Atau pisah jadi page baru: `/cacm/kriteria`, `/knowledge/templates`

### S4.1 — API endpoint `/api/simwas/st/sync` (4 jam)
```python
# backend/app/routes/simwas.py (file baru)
@router.post("/simwas/st/sync")
async def sync_st_from_simwas(payload: STSyncPayload, ...):
    # 1. Validate API key (header X-SIMWAS-API-KEY)
    # 2. Create/update Penugasan dengan field dari SIMWAS
    # 3. Return v7 penugasan_id untuk SIMWAS catat
```
- Auth middleware: API key dari env `SIMWAS_API_KEY` di `config.py`
- Field SIMWAS → v7 mapping (nomor_st, judul, jenis, pelaksana, periode)

### S4.2 — E2E regression test (4 jam)
Manual click-through atau pytest dengan dummy penugasan:
- [ ] LiteParse digest masih jalan (PR #1)
- [ ] HITL approve/reject/edit temuan (PR #2)
- [ ] Render KKP filter APPROVED-only (PR #2)
- [ ] Auto-preload context saat penugasan dibuat (PR #2)
- [ ] CACM diff EWS vs v7-native (PR #3)
- [ ] Promote v7 finding ke penugasan (PR #3)
- [ ] Subprocess pakai sys.executable (PR #4)
- [ ] ANTHROPIC_API_KEY auto-export (PR #5)
- [ ] Audit-pengadaan pipeline + kolom Sebab (PR #6)
- [ ] Pendampingan konsultasi-pengadaan format (PR #6)
- [ ] Digest generic untuk 14 skill criteria-driven (PR #7)
- [ ] 17 skill template + pattern + frontmatter (PR #8)

### S4.3 — Dokumentasi handover tim SIMWAS (2 jam)
- OpenAPI spec endpoint v7 untuk SIMWAS consume
- Diagram alur: SIMWAS → v7 (sync ST) → v7 jalankan agen → SIMWAS (status update)
- Auth setup guide
- Sample payload + response

---

## 🚀 Cara start environment

```bash
cd "/Users/itjen/Downloads/sistem audit v7"

# 1. Docker + DB
open -a Docker            # kalau Docker mati
docker compose up -d db
until docker exec sistemauditv7-db-1 pg_isready -U postgres >/dev/null 2>&1; do sleep 1; done

# 2. Backend
cd backend
lsof -ti:8000 | xargs kill 2>/dev/null
nohup .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/uvicorn.log 2>&1 &

# 3. Frontend — pakai Claude Preview MCP
# Tool: mcp__Claude_Preview__preview_start dengan name "frontend"
```

URLs:
- Backend: http://127.0.0.1:8000 ([docs](http://127.0.0.1:8000/docs))
- Frontend: http://localhost:3000

---

## 📚 Dokumen referensi

| File | Isi |
|---|---|
| `docs/rencana-integrasi-simwas-v2.html` | Plan implementasi lengkap (10 section) — buka di browser |
| `ROADMAP.md` | Roadmap v7 + adendum per sprint |
| `knowledge/wiki/templates/README.md` | Schema template KP+PKP |
| `.claude/settings.local.json` | Permission config Claude |
| `.claude/launch.json` | Preview server config (frontend) |

---

## 🎨 Komponen frontend siap pakai

| File | Fungsi |
|---|---|
| `frontend/components/AppShell.tsx` | Wrapper sidebar+topbar+main+footer+toaster |
| `frontend/components/Sidebar.tsx` | Menu collapsible 240px ungu |
| `frontend/components/TopBar.tsx` | Header SIMWAS-style dengan avatar role |
| `frontend/components/StageGrid.tsx` | 7/8 tahapan card grid |
| `frontend/components/HeroPenugasan.tsx` | Detail page hero |
| `frontend/components/EmptyState.tsx` | Empty state dengan icon+CTA |
| `frontend/components/TemplatePickerKpPkp.tsx` | Picker template KP/PKP |

---

## 🔧 Backend endpoints baru di Sprint 1+2

| Endpoint | Method | Fungsi |
|---|---|---|
| `/knowledge/templates/{kind}` | GET | List template KP atau PKP (filter by skill) |
| `/knowledge/templates/{kind}/{slug}` | GET | Full content template (meta + body) |

---

## 🛡 Fitur v7 yang HARUS tetap jalan (regression checklist)

Saat lanjut Sprint 3-4, JANGAN rusak ini:

1. **HITL approval/reject/edit temuan** (PR #2)
2. **Filter render_kkp APPROVED-only** (PR #2)
3. **Auto-preload context** saat penugasan dibuat (PR #2)
4. **CACM Fase 1**: diff UI + promote v7-native + auto-promote opt-in (PR #3)
5. **LiteParse + 3 hardcode**: context.md template, hybrid extract, prefill temuan (PR #1)
6. **Subprocess pakai sys.executable** (PR #4)
7. **ENV ANTHROPIC_API_KEY auto-export** di startup (PR #5)
8. **Audit-pengadaan pipeline + kolom Sebab** (PR #6)
9. **Pendampingan konsultasi-pengadaan format** (PR #6)
10. **Digest generic untuk 14 skill criteria-driven** (PR #7)
11. **Workflow 17 skill: template, pattern, frontmatter, prompt** (PR #8)

---

## ❓ Yang user perlu lakukan parallel

Sebelum Sprint 4 (API integration), user perlu:

1. **Schedule meeting tim teknis SIMWAS** untuk:
   - API key/OAuth untuk auth v7 → SIMWAS
   - Sandbox environment
   - Endpoint SIMWAS untuk push ST → v7
   - Format DOCX template (download dari Template Dokumen SIMWAS)
   - Webhook endpoint untuk status sync

2. **Validasi konten template KP+PKP** dengan auditor senior (workshop 1-2 jam)

3. **Konfirmasi domain deployment**: subdomain SIMWAS (mis. `ai.simwasv2.komdigi.go.id`) atau separate?

4. **SSO strategy**: OIDC integration atau API token sharing? (auditor jangan login 2x)

---

## 💡 Tip sesi baru

Saat mulai sesi Claude baru di project ini:
1. Auto-memory `project_simwas_integration.md` akan loaded — sudah update dengan progres Sprint 1+2
2. Baca `HANDOVER.md` ini untuk fast pickup
3. Buka `docs/rencana-integrasi-simwas-v2.html` di browser untuk detail rencana
4. Verifikasi state: `git log --oneline -5` (harus terlihat commits Sprint 1+2)
5. Start environment dengan langkah di section "Cara start environment" atas

Lanjut langsung ke Sprint yang Anda mau (rekomendasi urutan: S4.1 API → S3.1-S3.3 paralel → S4.2 regression).
