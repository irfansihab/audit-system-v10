# Backlog Hardening / Simplifikasi / Optimasi Engine — Audit 18 Skill + Agen + Tools (21 Jun 2026)

Konteks: sistem = **ENGINE** (skills + agen + tools + digest/render); **orkestrasi + UI → INTEGRAL**. Tujuan: skill jadi **substansi murni & portabel**, doktrin konsisten, ramping, hemat token. Hasil audit 5 subagen paralel.

Prioritas: **P0** salah-output/doktrin · **P1** portabilitas engine (pivot) · **P2** hardening konsistensi/reference · **P3** simplifikasi/dead-code · **P4** struktural.

> **Progres:** ✅ **P0 SELESAI** (21 Jun, commit `20ac200`) — doktrin Sebab/Akibat KKSAR konsisten lintas skill. ✅ **P3 #15 dead-code SELESAI** — `read_anomalies`/`build_draft_temuan_from_anomalies`/`read_draft_temuan` dicabut dari tool + `prefill_temuan.py` dihapus + prompt agen dibersihkan; `cross_check.py` (v6) dibiarkan (reproducibility, tak diekspos). ✅ **P3 #16 SELESAI** — evaluasi-spip 563→259 & evaluasi-manajemen-risiko 523→293 baris (mekanik/bobot/contoh dipindah ke references + pointer; contoh MR diperbaiki ke KKSAR ber-Sebab; ref baru `05-aoi-pattern-manajemen-risiko.md`). ✅ **P3 #17 SELESAI** — shared-pbj/kinerja PANDUAN diberi banner "sumber kebenaran = panduan-format-umum" (cegah drift). **P3 TUNTAS.** Catatan: FE/BE v9 **tetap dipakai sebagai harness uji-coba**. Berikutnya: **P1** (portabilitas engine) & **P2** (hardening reference/terminologi).

---

## P0 — Koreksi doktrin (output bisa salah)

1. **shared‑pbj‑references & shared‑kinerja‑references PANDUAN: kolom Sebab "❌" untuk Reviu → STALE.** Bertentangan dgn PANDUAN pusat (Sebab diisi semua jenis ber‑KKSA sejak 17 Jun, anti‑mengarang). File: `knowledge/skills/shared-pbj-references/PANDUAN.md` (b.47‑52,96), `shared-kinerja-references/PANDUAN.md` (b.36‑40). **Dampak besar** — menggerakkan output reviu‑pengadaan/rka‑kl. → samakan ke "✅ Diisi (anti‑mengarang)".
2. **3 skill PEMANTAUAN tak punya unsur Akibat** (langgar PANDUAN; `format_laporan: kksa`). `pemantauan-pengadaan` (tabel KKP b.189, ISU b.97‑112 pakai "Potensi Risiko"), `pemantauan-tindak-lanjut` (tabel b.61 tanpa KKSA), `pemantauan-umum` (sheet/JSON b.94/148 tanpa Akibat). → tambah kolom/field **Sebab + Akibat** (KKSAR), ganti "Potensi Risiko"→Akibat.
3. **Field Sebab hilang di struktur (tabel/JSON) walau prosa menyebutnya:** `evaluasi-manajemen-risiko` (contoh & format tanpa Sebab, b.141‑495), `evaluasi-umum` (KKE/LHE‑F/JSON), `reviu-umum` (KKR/JSON b.88‑160). → tambahkan field **Sebab** ke struktur.
4. **reviu-rka-kl: reference SBM keliru "belum tersedia"** padahal `references/02-sbm-2026-pmk-32-2025.md` (555 baris) ADA (SKILL b.370). → perbaiki rujukan; tanpa ini Aspek A (kewajaran biaya) mendorong "tidak cukup data" palsu.
5. **append_temuan contoh JSON tanpa `sebab`/`kode_*`** di `anggota_tim.md` (b.206‑219) — bisa bikin agen lupa Sebab utk skill ber‑KKSA. → tambah `sebab` + `kode_kondisi/penyebab/rekomendasi` di contoh.

## P1 — Portabilitas engine (inti pivot: lepas orkestrasi/UI dari skill)

6. **Cabut blok orkestrasi v7 dari SEMUA 18 SKILL.md** → INTEGRAL. Pola seragam: seksi **"Eksekusi di v7"**, tabel **Tahap X0–X4 + kolom Pelaku AT/KT/PT**, nama tool v9 (`run_batch_*`, `read_digest`, `read_ingested_digest`, `append_temuan`, `render_kkp_docx`, `run_qc_kkp`, `write_penilaian_lke`), `_PKP/sasaran-assignment.json`, rujuk `backend/app/prompts/anggota_tim.md`, frontmatter **`auto_execute`/`auto_execute_command`**. Sisakan: substansi (kriteria/aspek/checklist) + format unsur KKSAR. *(Skill terdampak: semua.)*
7. **`render_kkp_docx` terkopel DB** (`kkp_tools.py:388‑460,533` import `SessionLocal`+`TemuanReview`/`Penugasan`). → jadikan keputusan HITL **argumen input** (kontrak), INTEGRAL menyuplai; engine buta DB.
8. **De‑UI prompt agen** (`anggota_tim.md` b.12‑22; `ketua_tim.md` b.9‑11,89,106): "tab Setup", "via UI", status `DISETUJUI_KT`/`SELESAI_KKP`. → ganti jadi **kontrak file/data** ("sasaran di `_PKP/sasaran-assignment.json`; bila kosong STOP & lapor"), tanpa UI/tombol/endpoint. `read_preload_context`/`read_pdf_page` deskripsi sebut tombol/endpoint → netralkan.
9. **konsultasi-pengadaan sebut nama fungsi/ path backend** (`lhr_tools.py:_render_pendampingan`, `_LHP/...json`) di SKILL (b.124). → deskripsi output netral.

## P2 — Hardening konsistensi & reference

10. **Reference rusak/legacy:** `reviu-umum` & `graduasi` rujuk **`audit-system-v4/...`** (repo v4 tak ada) → `panduan-format-umum/PANDUAN.md`. `audit-kinerja` 7/8 reference TODO/absen (substansi RCA/3E tak ter‑ground). `kepatuhan-saipi` rujuk `scripts/qc_saipi.py` & `wiki/raw/*.pdf` (tak ada). `konsultasi-pengadaan/README` daftar 5 file TODO (tak ada) + format lama → tulis ulang. `reviu-pengadaan` rujuk `scripts/reviu-pengadaan/README.md` (tak ada).
11. **Terminologi unsur → baku KKSAR.** Skill audit pakai **"CCSAA"** (audit-kinerja/pengadaan/umum) → ganti **KKSAR**. `audit-kinerja` masih "**3E**" di beberapa tempat padahal lingkup **2E** → seragamkan.
12. **reviu-rka-kl konversi rule→checklist belum tuntas:** masih "40 rules", tabel "dulu rule", instruksi `cross_check.py`, benchmark wall‑clock (b.20,221‑281,237‑248). → buang jejak rule; checklist murni.
13. **Cek SAIPI 2320 (kepatuhan-saipi) lupa Sebab** (b.86 cek kondisi/kriteria/akibat saja). → tambah cek Sebab utk jenis ber‑KKSA.
14. **Versi tak konsisten** (frontmatter vs body vs changelog) di banyak skill (audit-pengadaan 2.4/2.0/3.0; reviu-pengadaan 1.6/1.5/1.7; reviu-rka-kl 3.2/3.0/3.3; dll) + **hapus `model: claude-sonnet-4-6`** dari frontmatter (pilihan model = INTEGRAL/harness). → satukan versi, buang `model`.

## P3 — Simplifikasi & dead code

15. **Buang dead code anomali (pasca digest‑only):** `read_anomalies` (`pipeline_tools.py:250‑294,466`), `build_draft_temuan_from_anomalies`+`read_draft_temuan` (`kkp_tools.py:855‑924,983`), `prefill_temuan.py` — tak pernah berhasil (anomalies tak ditulis di `--digest-only`). Juga buang promosi+larangan ganda di `anggota_tim.md` (b.42‑43 vs 189‑197). `cross_check.py` (3 file v6) tandai deprecated, jangan diekspos.
16. **Ramping­kan SKILL.md gemuk** → pindah mekanik/contoh ke references: `evaluasi-spip` (563→~250: openpyxl/cell‑map/bobot ke ref 02/03), `evaluasi-manajemen-risiko` (523→~250: blok format/contoh/batasan terduplikasi), `audit-pengadaan` (format CCSAA/KKP/LHP duplikat PANDUAN). Buang changelog naratif panjang.
17. **Satu sumber kebenaran matriks unsur‑per‑jenis** = `panduan-format-umum/PANDUAN.md`; shared‑pbj/kinerja cukup merujuk (hindari drift seperti P0‑1). `01-panduan-ekstraksi-kriteria.md` ter‑duplikasi di 5 skill *-umum → pertimbangkan 1 salinan kanonik.

## P4 — Struktural (keputusan)

18. **kepatuhan-saipi** = meta‑skill QA (qc_saipi/gate/exit‑code), bukan substansi domain → pindahkan logika QA ke INTEGRAL; sisakan *mapping standar SAIPI→kriteria* sebagai reference portabel.
19. **graduasi-skill-spesifik** = meta‑skill pengembangan (Gate‑based + "STOP & TANYA AUDITOR" + path v4 + CLI) → keluarkan dari `knowledge/skills/` ke tooling INTEGRAL, atau refactor total.

---

## Urutan eksekusi disarankan
**P0 dulu** (koreksi doktrin — cepat, dampak mutu langsung) → **P3 dead-code** (cepat, mengurangi noise) → **P1 portabilitas** (besar, sistematis: 1 pola dicabut dari 18 skill; bisa lewat template + subagen paralel) → **P2 hardening** → **P4 keputusan struktural**.

Catatan: P1 paling besar & paling sesuai pivot — sebaiknya dilakukan dengan **pola seragam** (definisikan struktur SKILL "engine‑ready": frontmatter minimal + Substansi + Checklist + Format KKSAR + References; tanpa orkestrasi) lalu replikasi.
