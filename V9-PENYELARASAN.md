# Audit AI v9 — Versi Penyelarasan dengan Juknis

Repo ini adalah **fork dari v8** (`sistem audit v8`, commit `e4c250e`) sebagai **lini versi v9**
yang difokuskan untuk **menyelaraskan sistem dengan Konsep SK Irjen "Standar Dokumen Penugasan
Pengawasan" (Juknis)** — dengan prinsip **SK mengikuti sistem (v8 sebagai jangkar)**, bukan sebaliknya.

## Prinsip pembatas
- **v8/v9 = mesin produksi substansi.** Garis finis = **laporan disetujui**.
- **Setelah laporan disetujui = ranah administrasi** (di luar fokus produksi).
- Bahan analisis & rencana lengkap untuk pimpinan: [`docs/penyelarasan-juknis-v8.html`](docs/penyelarasan-juknis-v8.html).

## Fokus pekerjaan v9 (backlog penyelarasan)
1. **Format laporan terpadu (KKSAR)** — shell seragam (Nota Dinas → Cover → Isi) + baku-kan istilah unsur
   (Analisis Penyebab→Sebab, Dampak/Risiko→Akibat) + tabel pengurangan unsur per jenis.
2. **Lembar Kendali Mutu Berjenjang** — gabung Reviu Supervisi + Daftar Periksa QA/QC + Sign-off (SDP-M).
3. **Tahapan 8 — Administrasi (peran TU baru)** — handoff + register ringkas; penomoran resmi/TTE/arsip tetap di SIMWAS.
4. **Auto-generate dokumen produksi** dari data terstruktur (Daftar Temuan & Rekomendasi, indeksasi KKP, dll).
5. **Proporsionalitas dokumen WAJIB per jenis penugasan** (audit/reviu/evaluasi/pemantauan/konsultansi).

## Catatan setup (repo baru, standalone)
- Repo ini **belum punya remote**. Tambahkan saat siap: `git remote add origin <url>`.
- Dependensi **tidak ikut** (regenerate): `cd frontend && npm install`; `cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- `.env` sudah disesuaikan ke path v9; vault lokal `llm-wiki/` sudah disalin (gitignored).
- `backend/data/` mulai kosong (data penugasan tidak ikut clone — gitignored).
