# Rencana Implementasi — INTEGRAL AI Workspace (revisi)

> Revisi 2026-06-09. Mengikat 8 keputusan scope dari user. Menggantikan struktur tab
> generik (Dokumen/Setup/Agen/Output) dengan **workspace per-peran**.

Arah: **v7 = AI engine di balik SIMWAS v2**. SIMWAS = system of record + orkestrator;
v7 dipanggil per-tahap, mengembalikan data terstruktur. 4 peran: AT / KT / PT / PM.

---

## 1. Status 8 keputusan scope (jujur)

| # | Keputusan | Status | Catatan |
|---|-----------|--------|---------|
| 1 | Survey Pendahuluan **hanya** untuk jenis **audit-*** | ✅ Selesai | Stage 0 + jenis dokumen SURVEY + tool agen KT (S3.1) |
| 2 | **Bukti Cek AI dihapus** (KKP & LHP sudah AI + HITL + approval) | ✅ Selesai | Workflow jadi 7-tahap, tidak ada slot Bukti Cek AI |
| 3 | ST dibuat manual admin SIMWAS → **ditarik via API** ke v7 | ⏳ Belum | Endpoint `/api/simwas/st/sync` belum ada (stub sasaran sync sudah ada) |
| 4 | **KP** diisi **PT**, pakai **template wiki** | ⚠️ Parsial | Template wiki + picker ada; belum jadi form pengisian KP khusus PT |
| 5 | **PKP** diisi **KT** (detailkan KP), pakai **template wiki** | ⚠️ Parsial | Editor sasaran-assignment (inti PKP) + template ada; masih gabung di tab Setup |
| 6 | **KKP = 1 tab workspace AT**: konteks + upload + AI + HITL + approval AT | ❌ Belum konsolidasi | Sekarang tersebar di tab Dokumen + Setup + Agen + Output |
| 7 | **Konsep Laporan = workspace KT**: generate draft LHP + HITL + approval | ❌ Belum konsolidasi | Generate LHP & approval temuan ada di tab Agen; review LHP di tab Output |
| 8 | Tab Template+Kriteria → **CACM + Knowledge** | ✅ Selesai | Sidebar CACM + Knowledge; /knowledge sudah ditata (S3.4) |

**Inti pekerjaan tersisa = poin 6, 7 (konsolidasi tab per-peran), 3 (ST API), dan rapikan 4–5.**

---

## 2. Target struktur tab (final) — workspace per-peran

Satu halaman detail penugasan, tab yang tampil **disesuaikan peran**. Tidak ada lagi
tab "Agen" terpisah — chat agen menyatu ke dalam workspace peran terkait.

```
Hero (info ST + grid tahapan; klik kartu → buka tab terkait)
─────────────────────────────────────────────────────────────
Tab (per-peran):

  [Penugasan & KP]      semua lihat · PT isi KP dari template wiki
                        (sumber: ST ditarik dari SIMWAS — read-only)

  [PKP]                 KT isi · detailkan KP jadi sasaran + langkah kerja
                        (template wiki PKP; assign ke anggota tim)

  [KKP — Workspace AT]  AT · SATU tab berisi urutan:
                          1) Generate Konteks (context.md)
                          2) Upload dokumen bukti (+ Survey utk audit-*)
                          3) Analisis AI (chat agen AT) → produksi temuan
                          4) HITL: review + edit temuan
                          5) Approval AT (kunci temuan untuk KT)

  [Konsep Laporan — KT] KT · SATU tab berisi:
                          1) Lihat KKP/temuan yang sudah di-approve AT
                          2) Generate draft LHP (chat agen KT)
                          3) HITL approval temuan final
                          4) Approval / Minta Revisi draft LHP (PT/PM)

  [Output & Laporan]    semua · daftar file hasil + unduh (KKP/LHP/QC)
```

> CACM & Knowledge **tidak** jadi tab penugasan — tetap di sidebar (sudah benar).

Visibilitas tab per-peran (sembunyikan yang bukan urusannya, hindari kebingungan):

| Tab | PT | KT | AT | PM |
|-----|----|----|----|----|
| Penugasan & KP | ✏️ isi | 👁 | 👁 | 👁 |
| PKP | 👁 | ✏️ isi | 👁 | 👁 |
| KKP — Workspace AT | 👁 | 👁 | ✏️ kerja | 👁 |
| Konsep Laporan — KT | ✅ approval LHP | ✏️ kerja | 👁 | ✅ approval LHP |
| Output & Laporan | 👁 | 👁 | 👁 | 👁 |

---

## 3. Tahapan implementasi

### Fase A — Konsolidasi workspace (poin 6 & 7) **[prioritas, UI murni]**
Refactor `frontend/app/penugasan/[id]/page.tsx` (komponen yang sudah ada dipakai ulang,
hanya disusun ulang ke dalam workspace):

- **A1. KKP Workspace AT** — gabung dalam 1 tab, urut sebagai langkah ber-section:
  - section "Konteks" → tombol Generate Context + editor context.md (dari `SetupPenugasanTab`)
  - section "Dokumen" → komponen `DokumenTab` (upload + Survey banner audit-*)
  - section "Analisis AI" → `ChatTab` (agen AT) — embedded, bukan tab terpisah
  - section "Review & Approval" → `TemuanReviewPanel`
- **A2. Konsep Laporan KT** — gabung dalam 1 tab:
  - section "KKP disetujui" → ringkasan temuan approved AT (read `TemuanReviewPanel` filter APPROVED)
  - section "Generate LHP" → `ChatTab` (agen KT) embedded
  - section "Approval Draft LHP" → `LhpReviewPanel` (sudah ada, S3.2)
- **A3. Tab per-peran** — `tab` state + daftar tab dihitung dari `role_aktif`
  (mis. AT tidak melihat tab PKP sebagai editable, dll). Hapus tab "Agen" generik.
- **A4. Sinkron Hero** — `STAGE_TAB` (sudah ada) di-update ke struktur tab baru.

Regresi yang WAJIB tetap jalan: generate context, upload+digest, chat agen AT/KT,
HITL approve/reject/edit, render KKP filter APPROVED, LhpReviewPanel, GatePanel skill bertahap.

### Fase B — KP & PKP dari template (poin 4 & 5)
- **B1.** Tab "Penugasan & KP": PT pilih template KP (wiki, picker sudah ada) →
  form isi field → simpan. (Backend penyimpanan KP — bisa ke context.md/metadata penugasan.)
- **B2.** Tab "PKP": KT mulai dari template PKP → editor sasaran-assignment yang sudah ada
  (tinggal tambah tombol "Mulai dari template" yang prefill langkah kerja).
- Konten template KP/PKP perlu **divalidasi auditor senior** (workshop) — di luar koding.

### Fase C — Integrasi ST dari SIMWAS (poin 3)
- **C1.** Endpoint `POST /api/simwas/st/sync` (auth `X-SIMWAS-API-KEY` dari env).
  Payload ST SIMWAS → buat/update Penugasan (nomor_st, judul, jenis, pelaksana, periode).
  Mengisi **PELAKSANA** + tanggal mulai–selesai yang sekarang kosong di DataTable.
- **C2.** v7 berhenti `gen_kode_penugasan` untuk penugasan asal SIMWAS → pakai ID SIMWAS.
- Butuh kontrak API + SSO dari tim SIMWAS (rapat teknis).

### Fase D — Hardening & handover
- E2E regression seluruh fitur v7.
- OpenAPI + diagram alur SIMWAS↔v7 + panduan auth untuk tim SIMWAS.

---

## 4. Urutan disarankan

1. **Fase A** (konsolidasi tab) — paling terasa untuk user, UI murni, tanpa nunggu SIMWAS.
2. **Fase B** (KP/PKP template) — lengkapi alur isi.
3. **Fase C** (ST API) — begitu kontrak SIMWAS tersedia.
4. **Fase D** (handover).

## 5. Keputusan terbuka (perlu user/SIMWAS)
- Kontrak REST API + SSO SIMWAS (format token, endpoint ST, webhook).
- Egress LLM ke Anthropic untuk data audit sensitif (kepatuhan) — belum diputuskan.
- Validasi konten template KP/PKP oleh auditor senior.
