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

## 2. Prinsip UX v8 — UI clean & minim friksi (WAJIB di semua layar)

> Permintaan utama user: **"UI clean, tidak banyak tombol atau hal yang membingungkan."** Ini jadi pagar desain v8 — berlaku untuk setiap fitur baru (auth, TLHP, CACM, dsb).

- **Satu aksi utama per layar** — tombol primer jelas (1, paling banyak 2). Aksi lain disembunyikan di menu "⋯/Lainnya".
- **Progressive disclosure** — opsi lanjutan/teknis/dev disembunyikan di balik "Lanjutan"; default cerdas mengurangi pilihan.
- **Tanpa tombol mati/duplikat** — hapus kontrol yang tak berfungsi atau membingungkan (warisan v7: tombol tema & bell sudah dihapus). Tiap tombol harus punya aksi nyata.
- **Navigasi tunggal** — alur lewat **tahapan** (ala SIMWAS), bukan banyak tab bertumpuk. Auditor tahu "ada di tahap mana".
- **Bahasa manusia** — label aksi pakai kata kerja jelas ("Susun PKP", "Setujui Temuan"), hindari jargon teknis/nama tool di UI.
- **Konsistensi komponen** — satu set komponen (kartu tahapan, panel, tabel) dipakai ulang; hindari pola baru per halaman.
- **Status terlihat, bukan tersembunyi** — progres & status (hijau/kuning/merah) terbaca sekilas; user tak perlu menebak langkah berikutnya.
- **Acceptance tiap fitur UI**: "auditor non-teknis paham apa yang harus diklik dalam < 5 detik, tanpa pelatihan."

## 3. Prinsip kinerja & skala (target: ±80 pengguna, ringan & lancar)

> Sistem dipakai **~80 auditor**. Harus tetap **ringan & responsif** saat dipakai bersamaan. Patokan: dashboard buka **< 1,5 detik**, navigasi terasa instan.

- **Agregat dashboard di-precompute, bukan dihitung saat load** — angka EWS/PKPT/TLHP/kinerja disimpan sebagai ringkasan (tabel summary / cache, refresh terjadwal atau saat ada event), bukan query berat tiap kali halaman dibuka. Hindari N+1.
- **Agent run = sumber daya berat** (subprocess CLI + LLM + SSE). Wajib **antrian + batas konkurensi global** (mis. N run paralel; sisanya queued) + backpressure. 80 user ≠ 80 run serentak, tapi sistem tak boleh tumbang saat lonjakan. (Sudah ada cegah double-run per penugasan; tambahkan cap global.)
- **DB**: connection pool memadai + **indeks** pada kolom yang sering difilter (penugasan.status, temuan, TLHP aging, EWS). Query async, paginasi daftar panjang.
- **Frontend ringan**: bundle kecil, hindari re-render mahal, SSE hanya untuk run yang sedang aktif (bukan polling global), data dashboard via 1 endpoint ringkas (bukan banyak fetch).
- **Backend stateless** (sesi via JWT) → siap horizontal scaling bila perlu. Hindari state in-memory yang mengikat ke 1 worker.
- **Acceptance**: uji beban ringan (mis. 50–80 sesi simulasi membuka dashboard + beberapa run paralel) tanpa degradasi parah.

---

## Workstream A — Konsolidasi identitas INTEGRAL (hapus dualitas, BUKAN ganti nama)

> Nama tetap **INTEGRAL**. Tujuan: berhenti tampil seperti dua produk. "Audit AI v7/v8" turun jadi engine/versi internal.

- [x] **A1 — Hapus framing "Powered by Audit AI v7"** ✅ (16 Juni) — landing (`page.tsx`), login, `AppShell` footer, `Sidebar`, meta title (`layout.tsx`): kini "INTEGRAL — Workspace Pengawasan Inspektorat II Komdigi"; footer "Mesin AI: Claude Agent SDK". Verified SSR: 0 sisa "Powered by Audit AI v7".
- [ ] **A2 — Identitas tetap**: pertahankan logo **∫** + palette ungu `#5C4FE7`. Tidak ada aset baru. (Keputusan: nama tidak diganti.)
- [ ] **A3 — Satukan narasi dokumen**: `README.md` + `HANDOVER.md` ditulis ulang sebagai **dokumen INTEGRAL tunggal** — INTEGRAL = produk, Audit AI engine = bagian internal; bukan dua hal.
- [ ] **A4 — Versi internal v7→v8**: `config`, `package.json`, badge versi → v8 sebagai nomor build, tanpa menyentuh brand "INTEGRAL".
- [ ] **A5 — Rapikan penamaan teknis**: `docs/openapi-integral-v7.yaml`→`openapi-integral-v8.yaml`; konsisten "integral" di slug teknis. Lanjutkan pembuangan referensi legacy `audit-system-v4` (bash/Task/_ROLE) di skill non-reviu (reviu sudah R0–R4).
- [ ] **A6 — Arsip**: pindahkan docs rencana "fase INTEGRAL" yang sudah usang ke `docs/archive/` (riwayat, bukan acuan aktif).
- [ ] **A7 — Audit UI clean** (lihat Prinsip UX §2): telusuri tiap layar, hapus tombol/kontrol mati & membingungkan, terapkan "satu aksi utama per layar" + progressive disclosure. Buat checklist UX per halaman sebagai gate sebelum fitur dianggap selesai.

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
- [~] **C5 — TLHP sebagai pilar penuh (BARU)** — fase pertama ✅ (16 Juni):
  - [x] Backend `routes/tlhp.py`: `GET /tlhp` (list+filter) & `/tlhp/summary`; hitung **umur/warna aging** (HIJAU/KUNING/ORANGE/MERAH) + flag **kritis** (>365 hari belum tuntas). Data dummy `fixtures/tlhp-dummy.json` (10 rekomendasi).
  - [x] UI: **menu "Tindak Lanjut"** + halaman `app/tlhp/page.tsx` (tabel rekomendasi + aging + filter status) + widget F4 di dashboard.
  - [ ] **Lanjutan:** data model DB (`TlhpRekomendasi`) + **ingest rekomendasi dari LHP terbit (Tahapan 7)** → menutup lingkaran laporan→TLHP; lengkapi `pemantauan-tindak-lanjut/references/` + agen; sinkron SIMWAS.

## Workstream D — Infra & bootstrap v8

- [x] **D1 — Bootstrap dev** ✅ (16 Juni) — v8 jalan lokal: backend `.venv` **Python 3.12.13** (`/opt/homebrew/bin/python3.12` — sistem `python3` 3.9.6 TERLALU TUA, butuh ≥3.10) + `pip install -r requirements.txt`; frontend `npm install`. **Gotcha penting (untuk tim saat clone):** (1) `.env` & symlink `backend/.env` **gitignored → TIDAK ikut clone** — buat `.env` dari `.env.example` lalu `ln -sf ../.env backend/.env`; (2) `APP_*_PATH` di `.env` harus menunjuk path **absolut repo INI** (skills/wiki/templates/v6), kalau tidak skill 0/200-default. Backend :8000 + frontend :3000 verified 200, 17 skills.
- [ ] **D2 — Database v8**: putuskan DB terpisah `audit_v8` vs lanjut `audit_v7` (dev). Jalankan migrasi schema auth (B1). `.env` sudah disalin dari v7 (DATABASE_URL `localhost:5432/audit_v7`).
- [ ] **D3 — Deploy**: perbarui `DEPLOY.md`, `fly.toml`, `docker-compose.yml`, Dockerfile untuk identitas v8.
- [ ] **D4 — Repo GitHub v8** (opsional): saat ini folder lokal + branch `v8-main`, remote `v7source` → v7 lokal (untuk cherry-pick). Buat repo `audit-system-v8` bila user mau (butuh konfirmasi).

## Workstream E — Backlog warisan v7 (tetap berlaku — detail di arsip)

- [ ] Konsistensi skill rumpun **audit/evaluasi/pemantauan** → pola Tahap (lihat [[project-skill-orkestrasi-v7]] di memori).
- [ ] Gap audit skill: `audit-kinerja` wajib riset online tapi agen tak punya tool web; unsur **Sebab** pada `evaluasi-mr`/`evaluasi-umum` kontradiktif dgn aturan "sebab hanya audit". (TLHP skeleton → sudah diangkat ke **C5**.)
- [ ] Eval P3–P5: perkuat grounding+coverage; token logging (`agent_runs`) + instrumen HITL; ukur akurasi digest.
- [ ] A3 laporan bespoke (dashboard pemantauan, tabel aspek evaluasi).
- [ ] Fix kosmetik: warning duplicate-key `Sidebar.tsx`; cap 14000 char `load_skill` untuk 2 skill pipeline besar.

## Workstream F — Dashboard beranda (pusat informasi pimpinan & auditor)

> Beranda = ringkasan sekilas seluruh pengawasan. Mengikat 4 pilar (Wiki/EWS/Agen/TLHP). **Wajib ringan** (lihat §3): semua angka dari ringkasan precomputed, satu endpoint.

Status: **beranda 6-widget LIVE** ✅ (16 Juni) — `app/dashboard/page.tsx` konsumsi `/dashboard/summary`, desain clean (UX §2). F1/F2/F4/F6 + kartu Penugasan terisi data; F3/F5 placeholder jujur "segera hadir".

Widget (kartu) yang ditampilkan:
- [x] **F1 — Update informasi EWS** — peringatan terbaru dari CACM/EWS (per satker, severity), link ke detail. ✅
- [x] **F2 — Progres pemenuhan PKPT** ✅ — widget %, berjalan/rencana/tertunda dari fixture [`pkpt-dummy.json`](backend/app/fixtures/pkpt-dummy.json) (DUMMY; nanti sumber resmi/SIMWAS).
- [ ] **F3 — Permintaan pengawasan belum ditindaklanjuti** — placeholder "segera hadir" (perlu model permintaan). Belum dibangun.
- [x] **F4 — Progres TLHP** ✅ — rekap status + aging warna + kritis >365 hari, dari modul C5.
- [ ] **F5 — Tren temuan berulang** — placeholder "segera hadir" (perlu agregasi pola temuan). Belum dibangun.
- [x] **F6 — Capaian kinerja (scorecard)** ✅ — 6 indikator (SPIP/SAKIP/RB/IACM/PEKPP/temuan BPK) + tren, dari fixture [`capaian-kinerja.json`](backend/app/fixtures/capaian-kinerja.json) (MANUAL; nanti API kinerja).
- [x] **F7 — Satu endpoint ringkas** ✅ `GET /dashboard/summary` (= G1; cache TTL 30s).
- [x] **F8 — Desain clean** ✅ (Prinsip UX §2): kartu seragam, status warna sekilas, klik → detail. Diverifikasi via screenshot.

## Workstream G — Kinerja & skala (±80 pengguna)

> Operasionalisasi Prinsip §3. Fondasi agar sistem ringan saat dipakai banyak orang.

- [x] **G1 — Endpoint ringkas `GET /dashboard/summary`** ✅ (16 Juni) — `app/routes/dashboard.py`: agregat MURAH (penugasan GROUP BY status & EWS GROUP BY status, ber-indeks) + PKPT/kinerja dari fixture, di-**cache TTL 30 dtk** (ringan utk ±80 user). Stub jujur utk modul belum-ada (TLHP/permintaan/tren). *Lanjutan opsional: tabel materialized + refresh event-driven bila uji beban menuntut.*
- [x] **G2 — Cap konkurensi global agent run** ✅ (16 Juni) — `max_concurrent_agent_runs=6` (config) + cek di `stream_agent` → **429 backpressure** saat penuh; cegah lonjakan subprocess/LLM menumbangkan server. *Lanjutan: antrian "menunggu" sejati (kini ditolak sopan, belum di-queue).*
- [x] **G3 — Indeks DB** ✅ (16 Juni) — model + live DB: `penugasan(status, ketua_tim_id)`, `dokumen(penugasan_id)`, `agent_runs(penugasan_id)`, `ews_findings(satker_kode, status)`. `CREATE INDEX IF NOT EXISTS` idempotent.
- [ ] **G4 — Frontend ringan**: code-split, kurangi re-render, SSE hanya saat run aktif (sebagian sudah: SSE per-run), 1 fetch dashboard (endpoint G1 siap).
- [ ] **G5 — Uji beban ringan** 50–80 sesi simulasi (buka dashboard + beberapa run paralel) → ukur p95 latensi, tetapkan baseline.

---

## Urutan eksekusi yang disarankan

1. **D1 bootstrap** → pastikan v8 jalan lokal (npm/pip install) sebelum apa pun.
2. **B (auth username/password)** + **A (konsolidasi identitas)** — fondasi v8.
3. **G (kinerja & skala)** — tabel ringkasan, cap konkurensi agent, indeks DB. Fondasi agar ringan untuk 80 user; menopang dashboard.
4. **C (verifikasi fitur dipertahankan)** + **C5 (TLHP)**.
5. **F (dashboard beranda)** — setelah C5 (TLHP) & G1 (ringkasan) siap, rakit 6 widget di atas 1 endpoint ringkas.
6. **D2–D4 infra/deploy**, lalu **E (backlog mutu)**.

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
