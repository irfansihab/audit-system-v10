# Roadmap — INTEGRAL v8

> **Konsolidasi: INTEGRAL jadi satu produk tunggal (v8).**
> Nama produk **TETAP "INTEGRAL"** (logo ∫, palette ungu `#5C4FE7`). Yang dihapus adalah
> **dualitasnya** — selama ini terasa dua produk ("INTEGRAL AI Workspace · Powered by Audit AI v7").
> Di v8, "Audit AI" turun jadi **engine/versi internal**, bukan brand terpisah. Satu nama (INTEGRAL),
> satu UI, satu data model. **"v8" = nomor versi codebase, bukan nama baru.**

**Dibuat:** 16 Juni 2026 · **Basis:** clone Audit v7 `d0c8a81` (branch `v8-main`, folder `sistem audit v8`).
Roadmap v7 lama diarsipkan di [`docs/ROADMAP-v7-archive.md`](docs/ROADMAP-v7-archive.md) (backlog mutu & detail teknis tetap berlaku — lihat Workstream E).

---

## 0. Keputusan pendiri v8 (16 Juni 2026)

- **INTEGRAL bukan sistem terpisah** — ia lapisan branding/UX di atas codebase v7 yang sama. v8 = hapus **dualitasnya**, jadikan **INTEGRAL** satu produk tunggal (nama dipertahankan; "Audit AI" jadi engine internal).
- **Nama produk = INTEGRAL** (keputusan user 16 Juni: nama lama dipertahankan, hanya dualitas "powered by Audit v7" yang dibuang). v8 = versi codebase.
- **Clone, bukan merge dua repo** — tak ada repo "audit v7" kedua; v8 = salinan bersih repo ini.
- **Dipertahankan:** workflow 7-tahapan · integrasi SIMWAS v2 · CACM/EWS · eval harness + mutu agen (R0–R4, PKP-di-feedback).
- **Baru di v8:** **login username + password** (ganti prototype role-only) + **pemantauan Tindak Lanjut Hasil Pengawasan (TLHP)** sebagai pilar penuh.

### Visi produk: INTEGRAL = workspace utama auditor (4 pilar)

INTEGRAL adalah **satu tempat** auditor menjalankan seluruh pengawasan — dari informasi → deteksi → kerja → tindak lanjut:

| Pilar | Modul | Fungsi |
|---|---|---|
| 📚 **Pengetahuan** | **Wiki** (`knowledge/`) | Semua informasi: pattern temuan, regulasi, glossary, profil auditi/vendor, riwayat. |
| 🔔 **Deteksi dini** | **CACM / EWS** (`CACM/`) | Early Warning System: pantau kondisi anggaran/pengadaan/kinerja satker, picu usulan penugasan. |
| 🤖 **Mesin kerja** | **Agen** (AT/KT + skill R0–R4) | Eksekusi analisis: digest → temuan → KKP → LHR, dengan HITL. |
| 🔁 **Tindak lanjut** | **TLHP** (baru, kelas-satu) | Pantau status rekomendasi LHP/LHR sampai tuntas — menutup lingkaran pengawasan. |

Alur ideal: **EWS (CACM) menemukan risiko → penugasan dibuat → agen menganalisis (didukung Wiki) → laporan terbit → TLHP mengawal rekomendasi sampai selesai.**

## 1. Prinsip arsitektur (warisan v7, tetap berlaku)

- **`backend/v6/` READ-ONLY** — semua perubahan di app-layer (`backend/app`) + template. V6 (digest, cross-check, render) tak ditulis ulang.
- **2 agen Claude**: Anggota Tim (AT) & Ketua Tim (KT); ingestion & QC SAIPI = deterministik/sinkron (bukan agen).
- **Skill registry folder-driven** (`knowledge/skills`, `APP_SKILLS_PATH`); skill = substansi domain, orkestrasi di prompt agen (Tahap R0–R4).
- **Anti-halusinasi**: tiap temuan ber-`dokumen_sumber`; `sebab` hanya untuk skill AUDIT.

---

## Workstream A — Konsolidasi identitas INTEGRAL (hapus dualitas, BUKAN ganti nama)

> Nama tetap **INTEGRAL**. Tujuan: berhenti tampil seperti dua produk. "Audit AI v7/v8" turun jadi engine/versi internal.

- [ ] **A1 — Hapus framing "Powered by Audit AI v7"** dari UI (landing, `TopBar`, footer, meta title) → cukup **"INTEGRAL — Workspace Pengawasan Inspektorat II"**. "Audit AI" hanya muncul di About/teknis sebagai engine.
- [ ] **A2 — Identitas tetap**: pertahankan logo **∫** + palette ungu `#5C4FE7`. Tidak ada aset baru. (Keputusan: nama tidak diganti.)
- [ ] **A3 — Satukan narasi dokumen**: `README.md` + `HANDOVER.md` ditulis ulang sebagai **dokumen INTEGRAL tunggal** — INTEGRAL = produk, Audit AI engine = bagian internal; bukan dua hal.
- [ ] **A4 — Versi internal v7→v8**: `config`, `package.json`, badge versi → v8 sebagai nomor build, tanpa menyentuh brand "INTEGRAL".
- [ ] **A5 — Rapikan penamaan teknis**: `docs/openapi-integral-v7.yaml`→`openapi-integral-v8.yaml`; konsisten "integral" di slug teknis. Lanjutkan pembuangan referensi legacy `audit-system-v4` (bash/Task/_ROLE) di skill non-reviu (reviu sudah R0–R4).
- [ ] **A6 — Arsip**: pindahkan docs rencana "fase INTEGRAL" yang sudah usang ke `docs/archive/` (riwayat, bukan acuan aktif).

## Workstream B — Autentikasi username + password (BARU, fondasi v8)

> Saat ini login = prototype **role-only** (`POST /auth/login` pilih AT/KT/PT/PM tanpa password). v8 ganti ke kredensial nyata.

- [ ] **B1 — Skema**: tambah `username` (unik) + `password_hash` ke tabel `User`; migrasi data seed. Hash **argon2/bcrypt** (jangan plaintext).
- [ ] **B2 — Backend auth**: `POST /auth/login` (username+password → JWT), seeding akun admin awal, endpoint ganti password. Pertahankan klaim role di JWT (RBAC tetap AT/KT/PT/PM).
- [ ] **B3 — Frontend**: ganti kartu-peran di `/login` jadi form username+password; simpan token; guard route; halaman ganti password.
- [ ] **B4 — Keamanan**: rate-limit + lockout percobaan gagal, kebijakan password minimum, logout/expiry. (Catatan: pembuatan akun/isi kredensial dilakukan user sendiri — sistem hanya menyediakan mekanisme.)
- [ ] **B5 — SSO SIMWAS koeksistensi**: login lokal (username/pass) **dan** SSO JWKS SIMWAS v2 sebagai dua jalur; produksi → SSO, dev → lokal.

## Workstream C — Fitur dipertahankan (verifikasi utuh pasca-rebrand + finalisasi)

- [ ] **C1 — Workflow 7-tahapan**: Kartu Penugasan → PKP → KKP (AI+HITL) → LRS KK → Konsep LHP → LRS LHP → Laporan Hasil. Pastikan status-derivation (`PKP_DONE`/`KKP_DONE`/`LHP_DONE`), SasaranApprovalPanel, LhpFilesPanel tetap jalan setelah rebrand.
- [ ] **C2 — Integrasi SIMWAS v2**: finalisasi kontrak REST (`openapi`→v8), JWKS SSO, webhook; selaras dengan B5.
- [ ] **C3 — CACM/EWS**: modul `CACM/` + `CacmRun`/`EwsFinding` + halaman CACM dipertahankan & diverifikasi.
- [ ] **C4 — Mutu agen & eval (lanjutan v7)**: skill **R0–R4** untuk reviu sudah selesai → **lanjutkan ke rumpun audit/evaluasi/pemantauan** (hati-hati: paradigma stop-confirm berbeda per rumpun); PKP-di-feedback; `backend/eval` (rubrik, golden, judge, verification pass).
- [ ] **C5 — TLHP sebagai pilar penuh (BARU)** — naikkan `pemantauan-tindak-lanjut` dari skill skeleton jadi **modul produk**:
  - Data model: matriks rekomendasi (asal LHP/LHR, No rek, substansi, PIC, deadline, status SUDAH/PROSES/BELUM, bukti TL, umur/aging).
  - UI: dashboard TLHP (per satker/PIC, aging hijau→merah, daftar kritis >365 hari) sebagai menu utama (sejajar Penugasan/CACM/Wiki).
  - Backend: endpoint TLHP + ingest rekomendasi dari LHP terbit (auto dari Tahapan 7) → **menutup lingkaran** (laporan → TLHP).
  - Lengkapi `knowledge/skills/pemantauan-tindak-lanjut/references/` (4 file kosong) + agen pemantauan TLHP.
  - Integrasi SIMWAS: sinkron status TLHP bila SIMWAS jadi sumber/penampung.

## Workstream D — Infra & bootstrap v8

- [ ] **D1 — Bootstrap dev** (node_modules/.venv TIDAK ikut clone): `cd frontend && npm install`; `cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. (Lihat "Cara menjalankan" di bawah.)
- [ ] **D2 — Database v8**: putuskan DB terpisah `audit_v8` vs lanjut `audit_v7` (dev). Jalankan migrasi schema auth (B1). `.env` sudah disalin dari v7 (DATABASE_URL `localhost:5432/audit_v7`).
- [ ] **D3 — Deploy**: perbarui `DEPLOY.md`, `fly.toml`, `docker-compose.yml`, Dockerfile untuk identitas v8.
- [ ] **D4 — Repo GitHub v8** (opsional): saat ini folder lokal + branch `v8-main`, remote `v7source` → v7 lokal (untuk cherry-pick). Buat repo `audit-system-v8` bila user mau (butuh konfirmasi).

## Workstream E — Backlog warisan v7 (tetap berlaku — detail di arsip)

- [ ] Konsistensi skill rumpun **audit/evaluasi/pemantauan** → pola Tahap (lihat [[project-skill-orkestrasi-v7]] di memori).
- [ ] Gap audit skill: `audit-kinerja` wajib riset online tapi agen tak punya tool web; unsur **Sebab** pada `evaluasi-mr`/`evaluasi-umum` kontradiktif dgn aturan "sebab hanya audit". (TLHP skeleton → sudah diangkat ke **C5**.)
- [ ] Eval P3–P5: perkuat grounding+coverage; token logging (`agent_runs`) + instrumen HITL; ukur akurasi digest.
- [ ] A3 laporan bespoke (dashboard pemantauan, tabel aspek evaluasi).
- [ ] Fix kosmetik: warning duplicate-key `Sidebar.tsx`; cap 14000 char `load_skill` untuk 2 skill pipeline besar.

---

## Urutan eksekusi yang disarankan

1. **D1 bootstrap** → pastikan v8 jalan lokal (npm/pip install) sebelum apa pun.
2. **B (auth username/password)** + **A (rebrand)** — fondasi identitas v8.
3. **C (verifikasi fitur dipertahankan)** pasca-rebrand.
4. **D2–D4 infra/deploy**, lalu **E (backlog mutu)**.

## Cara menjalankan v8 (lokal)

```bash
# 1. Database (Docker) — pakai compose yang sama
cd "/Users/itjen/Downloads/sistem audit v8"
docker compose up -d db

# 2. Backend (perlu install dependency — tidak ikut clone)
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000   # ⚠ port bentrok bila v7 masih jalan

# 3. Frontend
cd ../frontend
npm install
npm run dev   # ⚠ port 3000 bentrok bila v7 masih jalan
```

> **Catatan port:** v7 dan v8 memakai port (8000/3000) & DB (`audit_v7`) yang sama. Untuk menjalankan v8 berdampingan dengan v7, ubah port + `DATABASE_URL` (→ `audit_v8`) di `.env` v8 (lihat D2). Untuk pindah total ke v8, matikan service v7 dulu.

## Apa yang sudah dikerjakan saat membuat v8

- ✅ Clone bersih v7 `d0c8a81` → `sistem audit v8` (96M; tanpa node_modules/.venv/data-besar), branch `v8-main`.
- ✅ Bawa `.env`, `frontend/.env.local`, dan `backend/data/` (2.8M) agar bisa langsung jalan setelah install dependency.
- ✅ Remote `origin` → di-rename `v7source` (sumber cherry-pick).
- ✅ Roadmap v7 diarsipkan; roadmap v8 ini dibuat.
