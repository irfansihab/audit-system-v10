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
- **Anti-halusinasi**: tiap temuan ber-`dokumen_sumber`; **unsur `sebab` diisi anti-mengarang untuk SEMUA jenis ber-KKSA** (audit/reviu/evaluasi non-LKE/pemantauan) — bila tak terbukti tulis "Tidak ditemukan penyebab"/"Tidak cukup data" (sejak 17 Juni). **KECUALI** evaluasi ber-LKE (RB/SAKIP/SPIP) & Konsultansi → tanpa Sebab. Lihat `panduan-format-umum/PANDUAN.md`.

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
- [x] **A2 — Identitas tetap** ✅ (16 Juni) — logo **∫** + palette ungu `#5C4FE7` dipertahankan; tak ada aset baru.
- [x] **A3 — Narasi dokumen** ✅ (16 Juni) — `README.md` ditulis ulang INTEGRAL-first (nama produk = INTEGRAL; "Audit AI" = engine internal; v8 = generasi codebase). `HANDOVER.md` sudah INTEGRAL.
- [x] **A4 — Versi internal v7→v8** ✅ (16 Juni) — FastAPI `title="INTEGRAL" v8.0.0` + root endpoint (`name:INTEGRAL, engine:Audit AI`); `package.json` → `integral-frontend@8.0.0`; header prompt agen AT/KT → "INTEGRAL (engine Audit AI)".
- [x] **A5 — Rapikan penamaan teknis** ✅ (16 Juni) — rename `docs/openapi-integral-v7.yaml`→`...-v8.yaml` + `kontrak-api-integral-v7.html`→`...-v8.html` + brand internal v8. *Sisa legacy `audit-system-v4` (bash/Task/_ROLE) di skill non-reviu → SELESAI di C4 (17 Juni).*
- [ ] **A6 — Arsip** (opsional): pindahkan docs rencana "fase INTEGRAL" usang ke `docs/archive/`. Ditunda — low value.
- [x] **A7 — Audit UI clean** (lihat Prinsip UX §2) — selesai (17 Juni):
  - [x] Audit semua layar utama: **tak ada tombol mati/duplikat** (TopBar/login/dashboard/penugasan/CACM/TLHP). Header penugasan + tombol sumber PKP sudah dirapikan.
  - [x] **Konsistensi dialog**: `alert()` native → `toast`; **SEMUA 13 `confirm()` native → modal INTEGRAL** (`lib/confirm.ts` + `ConfirmHost`, danger merah/primary, ESC/Enter). 0 confirm native tersisa. **Render visual terverifikasi (screenshot)** — modal terpusat, backdrop redup, tombol Batal/Hapus permanen.
  - [x] **Konsistensi warna tombol antar-halaman**: 8 tombol aksi + 1 caret yang masih hardcoded (`violet/indigo/sky/blue-500..700`) di `penugasan/[id]` & `knowledge` → distandarkan ke token brand `bg-primary` / `hover:bg-primary-dark`. Badge severity/status tetap semantik (CRITICAL merah, HIGH/MEDIUM amber, sukses hijau). 0 tombol aksi non-brand tersisa.

## Workstream B — Autentikasi username + password (BARU, fondasi v8)

> Saat ini login = prototype **role-only** (`POST /auth/login` pilih AT/KT/PT/PM tanpa password). v8 ganti ke kredensial nyata.

- [x] **B1 — Skema** ✅ (16 Juni) — `User` +`username` (unik) +`password_hash` (bcrypt). Migrasi kolom idempoten (`ALTER ... IF NOT EXISTS`) di `init_db.seed_auth` (startup).
- [x] **B2 — Backend auth** ✅ — `POST /auth/login` username+password → verifikasi bcrypt → JWT (role=role_default). 5 akun seed (sarah/citra AT, budi KT, inspektur PT, **doddy PM baru**), password dev `audit2026`. Legacy role-only dipertahankan TAPI dimatikan bila `APP_ENV=production`.
- [x] **B3 — Frontend** ✅ — `/login` form username+password + **"Login cepat (dev)"** 5 kartu per role yang **auto-isi** kredensial lalu masuk. Teruji (klik→dashboard, salah password→401).
- [x] **B4 — Keamanan login** ✅ (17 Juni) — semua teruji:
  - **Lockout brute-force** (`login_guard.py`, in-memory per-username): 5 gagal/15 mnt → kunci 15 mnt (429); pesan sisa-percobaan. Teruji curl: attempt 5→kunci, 6→429.
  - **Ganti password** `POST /auth/change-password` (perlu sesi; verifikasi pw lama, min 8 char, ≠ lama) + **modal INTEGRAL** di dropdown TopBar. Teruji: short/same/wrong-old→400, valid→204, login pw baru OK.
  - **Logout + expiry**: token JWT `SESSION_EXPIRE_HOURS` (default 12) konfigurabel; **handling 401 terpusat** di `api.request()` → auto-clear token + redirect `/login?expired=1` + notice "Sesi telah berakhir". Teruji E2E (token bogus → redirect+notice).
  - Semua ambang konfigurabel via `.env` (LOGIN_*, SESSION_EXPIRE_HOURS, PASSWORD_MIN_LENGTH). Lockout hanya kena jalur username+password (quick-login dev tak terdampak).
- [ ] **B5 — SSO SIMWAS koeksistensi**: login lokal + SSO JWKS SIMWAS v2; produksi → SSO. **Catatan produksi: matikan login cepat + ganti DEV_PASSWORD.**

## Workstream C — Fitur dipertahankan (verifikasi utuh pasca-rebrand + finalisasi)

- [~] **C1 — Workflow 7-tahapan**: Kartu Penugasan → PKP → KKP (AI+HITL) → LRS KK → Konsep LHP → LRS LHP → Laporan Hasil. Status-derivation + SasaranApprovalPanel + LhpFilesPanel jalan.
  - [x] **Lembar Reviu berjenjang KT & PT** ✅ (replikasi format INTEGRAL/SIMWAS) — `models.LembarReviu` + `routes/lembar_reviu.py` (aspek baku A–D per level: KT atas KKP, PT atas LHP + kolom Penyelesaian) + `LembarReviuPanel` di Tahapan 4 (KT) & 6 (PT): status per aspek + paraf (reviewer/NIP/tanggal). Role-gated. Teruji.
- [ ] **C2 — Integrasi SIMWAS v2**: finalisasi kontrak REST (`openapi`→v8), JWKS SSO, webhook; selaras dengan B5.
- [ ] **C3 — CACM/EWS**: modul `CACM/` + `CacmRun`/`EwsFinding` + halaman CACM dipertahankan & diverifikasi.
- [~] **C4 — Mutu agen & eval (lanjutan v7)**:
  - [x] **Orkestrasi seragam SEMUA skill** ✅ (17 Juni) — 13/13 skill non-reviu di-refactor ke pola v7 (blok "Eksekusi di v7" + tabel Tahap), selaras reviu (R0–R4): **AUDIT** A0–A4 (wajib Sebab; audit-pengadaan pakai tool `run_batch_audit_pbj`), **EVALUASI** E0–E4 (tanpa Sebab; criteria/LKE-driven manual), **PEMANTAUAN** P0–P4 (monitoring), **KONSULTANSI** K0–K3 (advisory). Legacy bash/Task/_ROLE/AskUserQuestion/Gate/audit-system-v4 dibuang. Substansi domain dipertahankan; registry 17 skill OK. Hanya 3 tool pipeline v7 ada (rka/pbj/audit_pbj).
  - [x] **Konsistensi doktrin Sebab + rezim LKE** ✅ (18 Juni) — bersihkan kontradiksi changelog-vs-body lintas skill; reviu (rka/pbj) hitungan rule & path diperbaiki; **trio LKE (RB/SAKIP/SPIP) = tanpa Sebab** (instrumen LKE + AoI, bukan KKSA) konsisten di prompt agen (klausul OVERRIDE dikecualikan) + PANDUAN + `render_kkp.py` (kolom Sebab dilepas utk trio LKE). Sumber: arahan user (SAKIP/SPIP punya LKE sendiri → ikut rezim RB).
  - [x] **SPIP/SAKIP/RB → 1-shot (buang gate bertahap)** ✅ (18 Juni) — evaluasi ber-LKE tak lagi gate-demi-gate (≈10 stop manual); kini auto-execute satu lintasan, HITL hanya KT-approve (selaras v8). **Infra gate dihapus tuntas**: `gate_registry.py`, `tools/gate_tools.py`, `tasks/*-bertahap.md`, endpoint `/gates`, GatePanel frontend, `api.ts` gate, config `tasks_path`. Backend & tsc verified.
  - [x] **KKP rekap skor LKE (pola RB)** ✅ (18 Juni) — tool baru `write_penilaian_lke` → `_KKP/penilaian-lke-<skill>.json`; `render_kkp.py` tampilkan tabel "Rekap Penilaian (LKE)" (komponen/bobot/Nilai PM/Nilai APIP/predikat) + AoI. Bug phantom `record_pkp_assessment` (dirujuk 14 skill, bukan tool) dibersihkan total.
  - [ ] **LHE SAKIP & SPIP — format laporan sendiri (BELUM)** — saat ini frontmatter `format_laporan: kksa`, padahal SAKIP/SPIP punya format LHE sendiri (seperti RB sudah `rb-4dim`). Buat profil render LHE khusus (mis. `lke-sakip`/`lke-spip`: rekap predikat per komponen + AoI + Pernyataan/simpulan kategori), tambah ke dispatcher `render_report` di `lhr_tools.py`, sesuaikan frontmatter & `ketua_tim.md`. *(Lingkup KKP sudah beres; ini level laporan/KT.)*
  - [ ] Lanjutan: PKP-di-feedback; `backend/eval` (rubrik, golden, judge, verification pass).
- [~] **C5 — TLHP sebagai pilar penuh (BARU)** — fase 1 & 2 ✅ (16 Juni):
  - [x] Backend `routes/tlhp.py`: `GET /tlhp` (list+filter) & `/tlhp/summary`; **umur/warna aging** (HIJAU/KUNING/ORANGE/MERAH) + flag **kritis** (>365 hari belum tuntas).
  - [x] UI: **menu "Tindak Lanjut"** + halaman `app/tlhp/page.tsx` + widget F4 dashboard.
  - [x] **Data model DB** `TlhpRekomendasi` (DB-backed; seed dummy idempoten saat startup).
  - [x] **Auto-ingest tutup-lingkaran** ✅ — saat konsep LHP **disetujui PT/PM** (`create_lhp_review` APPROVED) → `ingest_tlhp_from_penugasan` baca `_LHP/rekomendasi.json` → buat item TLHP (anti-dup via `no_rek`). Juga manual `POST /tlhp/ingest/{id}` (KT/PT/PM). Teruji: penugasan 51 → +6 (idempoten).
  - [ ] **Lanjutan TLHP — ⛔ PRIORITAS TERAKHIR** (ditunda atas arahan user 16 Juni): lengkapi `knowledge/skills/pemantauan-tindak-lanjut/references/` (4 file kosong) + agen pemantauan TLHP; derive satker/PIC lebih cerdas; sinkron status SIMWAS. Fungsi inti TLHP (data, aging, dashboard, tutup-lingkaran) sudah jalan — sisanya dikerjakan paling akhir.

## Workstream D — Infra & bootstrap v8

- [x] **D1 — Bootstrap dev** ✅ (16 Juni) — v8 jalan lokal: backend `.venv` **Python 3.12.13** (`/opt/homebrew/bin/python3.12` — sistem `python3` 3.9.6 TERLALU TUA, butuh ≥3.10) + `pip install -r requirements.txt`; frontend `npm install`. **Gotcha penting (untuk tim saat clone):** (1) `.env` & symlink `backend/.env` **gitignored → TIDAK ikut clone** — buat `.env` dari `.env.example` lalu `ln -sf ../.env backend/.env`; (2) `APP_*_PATH` di `.env` harus menunjuk path **absolut repo INI** (skills/wiki/templates/v6), kalau tidak skill 0/200-default. Backend :8000 + frontend :3000 verified 200, 17 skills.
- [ ] **D2 — Database v8**: putuskan DB terpisah `audit_v8` vs lanjut `audit_v7` (dev). Jalankan migrasi schema auth (B1). `.env` sudah disalin dari v7 (DATABASE_URL `localhost:5432/audit_v7`).
- [ ] **D3 — Deploy ke PDN (Pusat Data Nasional) — ⛔ PRIORITAS TERAKHIR** (arahan user 16 Juni): target deploy = PDN (bukan Fly.io/cloud lama). Sesuaikan `DEPLOY.md`, `docker-compose.yml`, Dockerfile untuk lingkungan PDN (kemungkinan on-prem/terbatas internet → cek implikasi: SDK Claude butuh akses API Anthropic, `digest_llm_fallback`, dll). Fly.io lama tidak dipakai. Dikerjakan paling akhir.
- [x] **D4 — Repo GitHub v8** ✅ (16 Juni) — **github.com/irfansihab/audit-system-v8** (PRIVATE), branch `v8-main`. Remote `origin` → repo ini, `v7source` → v7 lokal (cherry-pick). `.env` gitignored (tak ikut).

## Workstream E — Backlog warisan v7 (tetap berlaku — detail di arsip)

- [x] Konsistensi skill rumpun **audit/evaluasi/pemantauan** → pola Tahap ✅ (RESOLVED di C4, 17–18 Juni; termasuk doktrin Sebab, rezim LKE, gate→1-shot).
- [ ] Gap audit skill: `audit-kinerja` "research online" mengasumsikan AT punya WebSearch/WebFetch — pastikan tool web tersedia di runtime agen. (Unsur **Sebab** pada `evaluasi-mr`/`evaluasi-umum` → **RESOLVED di C4**: Sebab dihapus dari rumpun evaluasi. TLHP skeleton → **C5**.)
- [ ] Eval P3–P5: perkuat grounding+coverage; token logging (`agent_runs`) + instrumen HITL; ukur akurasi digest.
- [ ] **Uji kualitas skill SELAIN reviu-rka-kl & pengadaan** — yang sudah live-tervalidasi baru audit-pengadaan (pilot), reviu-pengadaan, reviu-rka-kl. Belum diuji live: `audit-kinerja`, `audit-umum`, rumpun `evaluasi-*` (sakip/spip/manajemen-risiko/reformasi-birokrasi/umum), rumpun `pemantauan-*` (pengadaan/tindak-lanjut/umum), `konsultansi-umum`, `konsultasi-pengadaan`, `reviu-umum`, `kepatuhan-saipi`. Untuk tiap skill: jalankan agen end-to-end, ukur **durasi + mutu temuan/KKP** (grounding ke bukti, pakai checklist SKILL & pattern, anti-mengarang Sebab), cek redundansi langkah (anti sapu-baca PDF), pastikan output sesuai format laporan jenisnya (LHA/LHR/LHE/LHP/Memo). Selaraskan ke baseline mutu pilot PBJ.
- [ ] **Cek kualitas Wiki** (pasca-sinkronisasi 18 Juni) — (a) **pattern temuan** (84 pattern/18 folder): validasi frontmatter (id/skill/severity unik & cocok folder), sitasi regulasi terverifikasi ke [[regulasi-kunci]], tidak ada pattern usang/duplikat, severity konsisten; (b) **konteks** (pola-temuan-berulang, glossary, regulasi-kunci): akurasi & kemutakhiran; (c) **vault llm-wiki** (217 catatan, gitignored): relevansi hasil `vault_search` untuk obyek penugasan, tidak ada catatan stale/kontradiktif yang menyesatkan preload_context; (d) **template KP/PKP v2.0** (36 file): konsistensi KP↔PKP, sasaran/langkah masih relevan per skill. Susun ceklist QA wiki yang bisa diulang tiap ingest baru.
- [ ] A3 laporan bespoke (dashboard pemantauan, tabel aspek evaluasi).
- [ ] Fix kosmetik: warning duplicate-key `Sidebar.tsx`; cap 14000 char `load_skill` untuk 2 skill pipeline besar.
- [ ] **Skill `reviu-keuangan` (BARU)** — pustaka pattern sudah ada (`temuan-patterns/reviu-keuangan/` RK-67/68/69, sinkron 18 Juni dari vault). Belum ada `knowledge/skills/reviu-keuangan/SKILL.md`; reviu LK sementara ditangani `reviu-umum` (criteria-driven). Scaffold skill penuh pola v7 (R0–R4) bila diputuskan jadi skill spesifik.

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

1. **D1 bootstrap** ✅ → v8 jalan lokal.
2. **B (auth username/password)** + **A (konsolidasi identitas, A1 ✅)** — fondasi v8.
3. **G (kinerja & skala, G1–G3 ✅)** — fondasi ringan untuk 80 user.
4. **F (dashboard beranda) ✅** + **C (fitur dipertahankan, +Lembar Reviu KT/PT ✅)**.
5. **D2 (DB v8/migrasi auth)**, lalu **E (backlog mutu)**.
6. **⛔ TERAKHIR (arahan user):** **Lanjutan TLHP** (references/agen/derive PIC/sinkron SIMWAS) · **D3 Deploy ke PDN** · D4 repo GitHub. Inti semua sudah jalan lokal; bagian ini paling akhir.

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
