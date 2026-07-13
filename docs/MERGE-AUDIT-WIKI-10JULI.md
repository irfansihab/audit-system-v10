# Rencana Merge + Audit Wiki — update `wiki_10 Juli`

> **Status: RENCANA + AUDIT (read-only). Belum ada perubahan pada wiki/engine.** Sumber: update vault `/Users/itjen/Downloads/wiki_10 Juli/` (315 catatan) dibanding `llm-wiki/wiki` (217) & `knowledge/wiki` (144, engine). Investigasi: 1 analisis struktural + 3 sub-audit paralel (hygiene, currency regulasi, pattern). Dibuat 10 Jul 2026.

---

## 0. Ringkasan eksekutif

- **Update bersifat ADITIF**: **+98 catatan, 0 dihapus** (vault 217 → 315). Aman.
- **Dua target merge** (arsitektur wiki v10 ganda):
  1. **`llm-wiki/wiki/`** (vault, *gitignored*) — sinkron penuh 98 catatan baru + update konten. **Dikonsumsi engine saat runtime** via `read_preload_context` → `vault_search` (APP_VAULT_PATH), jadi update vault langsung menaikkan mutu preload.
  2. **`knowledge/wiki/`** (di-git, engine) — hanya **delta pattern + konteks** yang direkonsiliasi (dua arah, bukan copy buta).
- **Delta engine kecil tapi bernilai tinggi**: 1 pattern baru (RK-70), 4 koreksi pattern (RK-67/68/69 + SAIPI-65), **1 master-index pattern baru** (`pattern-temuan.md`, P-01…P-40), **12 regulasi/pasal** untuk `regulasi-kunci.md`, + **1 konflik currency kritis** (Perpres 46/2025 vs 16/2018).
- **Hygiene**: 1 duplikat byte-identik, ~14 kelas wikilink rusak, 2 catatan stale-naming ("audit-system-v2"), beberapa stub, gap-list auditor 8 minggu basi.

**Prioritas #1 (mutu engine, cepat):** (a) reconcile **Perpres 46/2025 → primary PBJ TA 2025+** di `regulasi-kunci.md` (risiko anti-halusinasi nyata); (b) tambah **12 regulasi/pasal**; (c) tambah **RK-70** + adopsi koreksi RK-67/68/69/SAIPI-65; (d) tambah **`pattern-temuan.md`** ke `konteks/`.

---

## 1. Peta arsitektur & aliran merge

```
wiki_10 Juli/ (315, update auditor)
   │
   ├──► [Jalur A] llm-wiki/wiki/ (vault, gitignored)   ← sinkron PENUH (98 baru + update)
   │        └─ dibaca engine: read_preload_context → vault_search (objek/regulasi/riwayat)
   │
   └──► [Jalur B] knowledge/wiki/ (di-git, engine)     ← selektif & direkonsiliasi
            ├─ temuan-patterns/<skill>/  (pattern → list_temuan_patterns / preload)
            └─ konteks/  (regulasi-kunci · pola-temuan-berulang · pattern-temuan ·  glossary)
```

**Engine mengonsumsi wiki dari 4 sumber** (`backend/app/preload_context.py`): (1) `temuan-patterns`, (2) `konteks/*.md`, (3) **vault_search** atas APP_VAULT_PATH, (4) riwayat `pengawasan-*.md`. → Jalur A **dan** B keduanya menaikkan mutu agen.

---

## 2. Rencana merge bertahap

### Fase 0 — Pra-flight (wajib)
- Branch `feat/wiki-merge-10juli` di v10.
- **Backup** `llm-wiki/wiki/` (snapshot) & tag konteks/pattern engine saat ini.
- Konfirmasi arah dua-arah pada file yang **engine lebih maju** (pola-temuan-berulang) agar tak ter-downgrade.
- **DoD:** backup ada; daftar file target terkunci (dari §3–§5).

### Fase 1 — Sinkron vault (`llm-wiki/wiki/`) — *gitignored, risiko rendah*
- Salin **98 catatan baru** + terapkan update konten ke `llm-wiki/wiki/`.
- **JANGAN** bawa artefak: hapus/skip `reviu-rka-kl/RKA-05-…tahapan 1.md` (duplikat byte-identik).
- **DoD:** `llm-wiki/wiki` = 315 catatan bersih (tanpa duplikat); `vault_search` menemukan catatan baru.

### Fase 2 — Pattern engine (`knowledge/wiki/temuan-patterns/`)
- **TAMBAH** `reviu-keuangan/RK-70-cross-dipa-transfer-control.md` (baru) + baris index di `reviu-keuangan/README.md`.
- **ADOPSI koreksi vault→engine** (vault benar): RK-67/68/69 (perbaikan **SK→ND**: ND-156/ND-155) + `SAIPI-65` (tambah **Case 2 ND-195, 08 Jul 2026**).
- **JANGAN** timpa `konteks/pola-temuan-berulang.md` (engine lebih maju: cross-link RP/RKA + "Cara Pakai" — vault hanya enrich prosa; opsional graft kutipan `[[wikilink]]`).
- **DoD:** 1 pattern baru + 4 koreksi masuk; `list_temuan_patterns` reviu-keuangan = 4; tak ada regresi pattern lain.

### Fase 3 — Regulasi-kunci (anti-halusinasi) — *nilai tertinggi*
- **Reconcile currency Perpres 46/2025** (lihat §4.A): jadikan **Perpres 46/2025 = dasar utama PBJ TA 2025+**; scope tabel Perpres 16/2018 jo 12/2021 ke "TA ≤ 2024" atau petakan pasal lama→baru.
- **TAMBAH 12 regulasi/pasal** (lihat §4 tabel) — prioritas PNBP (PMK 206/2021, PMK 155 **Ps 91**, PM Kominfo 5/2021 Ps 205(3), UU 36/1999), PDP/IGRS (UU 27/2022 pasal, Permenkominfo 2/2024 pasal, Perpres 19/2024, PP 71/2019), SAKIP & RB (set PermenPAN-RB), LPU (PMK 72/2017).
- **DoD:** `regulasi-kunci.md` memuat pasal-pasal yang paling sering dirujuk LHR; tak ada sitasi superseded (16/2018) sebagai primary untuk TA 2025+.

### Fase 4 — Master index pattern (`konteks/pattern-temuan.md`)
- **TAMBAH** `pattern-temuan.md` (vault-only, ~56 KB, **P-01…P-40** + Mega-Pattern M1/M2, 11 domain) ke `knowledge/wiki/konteks/` sebagai **indeks lintas-skill** di atas `temuan-patterns/`.
- Pertimbangkan wiring ke preload (opsional) atau cukup sebagai referensi konteks.
- **DoD:** engine punya katalog pattern top-level; tak duplikatif dengan per-skill patterns.

### Fase 5 — Hygiene & currency vault (lihat §5)
- Hapus duplikat; perbaiki ~14 kelas **wikilink rusak**; perbarui **stale-naming** (`integrasi-audit-system.md`, `sop-ingest-lhp-ke-wiki.md`: "audit-system-v2" → v10/INTEGRAL); segarkan `dashboard.md` & gap-list.
- **DoD:** 0 duplikat; wikilink tinggi-frekuensi resolve; nama sistem konsisten.

### Fase 6 — Validasi
- `read_preload_context` untuk objek yang punya catatan baru → bundle memuat catatan+regulasi baru.
- Sanity: `list_temuan_patterns` semua skill (RK-70 muncul); regulasi-kunci ter-parse; tak ada broken-link di file yang di-git.
- **DoD:** preload hijau; engine bisa mengutip regulasi baru; commit Jalur B (git) — Jalur A tetap gitignored.

---

## 3. Delta engine (Jalur B) — ringkas

| Item | Aksi | Arah | Catatan |
|---|---|---|---|
| `reviu-keuangan/RK-70-cross-dipa-transfer-control.md` | **TAMBAH** | vault→engine | Pattern BARU (kontrol lintas-DIPA; PP 60/2008 Ps 8 + PMK 107/2024) |
| `reviu-keuangan/RK-67/68/69` | **ADOPSI** | vault→engine | Koreksi **SK→ND** (ND-156/ND-155) |
| `kepatuhan-saipi/SAIPI-65` | **ADOPSI** | vault→engine | Tambah **Case 2 (ND-195)** — lebih current |
| `reviu-keuangan/README.md` | update | vault→engine | +baris RK-70 |
| `konteks/pola-temuan-berulang.md` | **PERTAHANKAN engine** | — | Engine lebih maju; graft prosa opsional |
| `konteks/pattern-temuan.md` | **TAMBAH** | vault→engine | Master index P-01…P-40 (baru di engine) |
| `regulasi-kunci.md` | update besar | vault→engine | 12 regulasi + currency Perpres 46 (§4) |
| `reviu-rka-kl/RKA-05-…tahapan 1.md` | **ABAIKAN** | — | Duplikat byte-identik (artefak) |

---

## 4. AUDIT — Regulasi/info baru untuk engine (ekstraksi)

### 4.A ⚠ Konflik currency KRITIS — Perpres 46/2025
- `regulasi-kunci.md` masih memperlakukan **Perpres 16/2018 jo 12/2021** sebagai dasar utama PBJ (tabel Ps 6/18/22/26) dan **Perpres 46/2025** hanya sebagai "transisi/mendesak".
- Vault `regulasi-perpres-46-2025.md` tegas: **Perpres 46/2025 MENGGANTIKAN Perpres 16/2018 dst**, dasar utama PBJ **TA 2025+**.
- **Risiko:** agen mengutip pasal **superseded** untuk penugasan TA 2025+. **Wajib reconcile** (skope Perpres 16 ke TA ≤2024; petakan pasal lama→baru).
- Minor: **Kepmen LPU 442/2024** melengkapi/menggantikan **486/2023** — beri catatan supersession parsial + alias Kominfo/Komdigi.

### 4.B 12 regulasi/pasal untuk ditambah ke `regulasi-kunci.md` (ranked)

| # | Regulasi + pasal | Substansi (utk sitasi) | Skill |
|---|---|---|---|
| 1 | **PMK 206/PMK.02/2021** (Pengembalian Lebih Bayar PNBP) — Ps 68(2)c, 74(2) | Pemindahbukuan hanya bila WB tak berkewajiban PNBP sejenis berulang; wajib teliti **substansi**, bukan kelengkapan. Dirujuk 8+ LHR | reviu-pnbp |
| 2 | **PM Kominfo 5/2021 — Ps 205(3)** | Lebih bayar pokok BHP = pembayaran di muka tahun berikutnya (kompensasi, bukan tunai) | reviu-pnbp |
| 3 | **PMK 155/PMK.02/2021 — Ps 91(1)** | Koreksi substantif = perbaikan **kesalahan matematis/formula** saja (bukan tafsir/keberatan) — kunci Setuju vs Tolak | reviu-pnbp |
| 4 | **UU 27/2022 PDP — Ps 46, 35, 4, 57–67** | Notifikasi kebocoran **14 hari kerja**; kewajiban teknis; data sensitif; sanksi (denda ≤2% pendapatan / Rp4M, pidana ≤6 th) | audit-kinerja/Wasdig |
| 5 | **Permenkominfo 2/2024 — Ps 9–13** | Kriteria rating (3+/7+/…/RC); mekanisme 2 tahap; kategori RC; keberatan **7 hari** | audit-kinerja-klasifikasi-gim |
| 6 | **UU 36/1999 Telekomunikasi** | Definisi luas "telekomunikasi" → layanan baru (SIP Trunk/SMS) wajib BHP + KPU/USO | reviu-pnbp |
| 7 | **PermenPAN-RB 88/2021 + Perpres 29/2014 + PP 8/2006** | Pedoman Evaluasi AKIP (4 komponen 30/30/15/25, 79 kriteria, AA–E) | evaluasi-sakip |
| 8 | **PermenPAN-RB 9/2023 + KepmenPAN-RB 182/2024 + SE 6/2025** | Pedoman + Juknis + RB Transisi | evaluasi-reformasi-birokrasi |
| 9 | **Perpres 19/2024** (Percepatan Industri Gim) | Mandat IGRS (parent Permenkominfo 2/2024) | audit-kinerja IGRS |
| 10 | **PP 71/2019 PSTE — Ps 12** | PSE wajib jaga kerahasiaan/keutuhan/ketersediaan data | audit-kinerja/Wasdig |
| 11 | **PMK 72/PMK.02/2017 jo 82/2016** (Dana BO LPU) | Tata cara penyediaan/pencairan/pertanggungjawaban BO LPU — sebab LPU TA2025 realisasi 0% | reviu-LK/RKA BUN LPU |
| 12 | **PM Kominfo 13/2019 & Perdirjen PPI 1/2021·1/2023** | Definisi teleponi dasar/jasa telko (basis sengketa SIP Trunk/SMS) | reviu-pnbp |

> Selain hierarki peraturan: **ISO 31000:2018** (support MR) & **UU 25/2009 Pelayanan Publik / UU 28/1999** (angle transparansi IGRS) dirujuk sebagai kriteria — catat sebagai referensi pendukung, bukan "peraturan".

### 4.C Pattern/info baru
- **RK-70** (cross-DIPA transfer, HIGH): kontrol/kepatuhan lintas-DIPA tanpa SK KPA pemberi + justifikasi urgensi (kasus ND-196 Rp4,35 M). Melengkapi celah kontrol yang belum ada di set engine.
- **`pattern-temuan.md`** (master index P-01…P-40, 11 domain + Mega-Pattern **M1 SOTK Transition Fallout**, **M2 TKPPSE Sistemik**) — katalog lintas-skill; jadikan indeks top-level `konteks/`.

---

## 5. AUDIT — Optimasi wiki (hygiene, kosong, currency)

### 5.A Duplikat / artefak
- `reviu-rka-kl/RKA-05-…tahapan 1.md` — **byte-identik** ke versi tanpa " 1" → **hapus** (satu-satunya di vault).
- `pola-temuan-berulang.md` (159 br, Apr 24) vs `pattern-temuan.md` (1314 br, Mei 18) — tumpang tindih; **`pattern-temuan.md` = otoritatif**, `pola-…` superseded (di vault).
- `dashboard.md` vs `dashboard.html` — konten sama 2 format → risiko drift, jaga sinkron.

### 5.B Stale-naming / currency
- `integrasi-audit-system.md` & `sop-ingest-lhp-ke-wiki.md` — merujuk **"audit-system-v2"** (usang) → perbarui ke arsitektur v10/INTEGRAL (engine vs orkestrator).
- `wiki-info-yang-perlu-ditambahkan.md` (Last updated 2026-05-19) & `dashboard.md` (2026-04-26) — **basi ~8–11 minggu** → refresh.
- Kominfo→Komdigi: sebagian besar **historis/benar** (nama laporan BPK); tak ada mis-label entitas aktif. Cukup alias di `regulasi-permenkominfo-2-2024.md`.

### 5.C Wikilink rusak (~14 kelas, spot-check full-vault)
- Prefix salah: `[[wiki/log.md]]`, `[[wiki/index.md]]` (root vault = wiki; tak ada subfolder `wiki/`).
- Short-code → filename penuh: `[[RKA-04]]`, `[[RP-11]]`, `[[reviu-keuangan/RK-67]]` (aktual ber-slug penuh).
- Renamed/missing: `[[PTL-48-rekomendasi-outstanding-bpk]]`→`PTL-48-rekomendasi-struktural-outstanding`; `[[PTL-50-verifikasi-outstanding-finansial]]`→`…-belum-tuntas`; PTL-49/52 & SAIPI-66 tak ada.
- Typo: `[[survey-…]]`→`survei-…`; `[[lhr-koreksi-pnbp-mitracomm-2025]]`→`lhr-pnbp-mitracomm-2025`; `[[penjaminan-kualitas-spip-kemkomdigi-final-2025]]`→`laporan-penjaminan-…`.
- Placeholder tertinggal: `[[peta-risiko-*]]`, `[[progress-trello by pdf]]`.

### 5.D Stub / info kosong (di-vault, perlu diisi auditor)
`sonny-hendra-sudaryana.md` (22 br) · `peta-risiko-wasdig-2026.md` & `peta-risiko-ekosistem-digital-2026.md` (kolom "Progres Penanganan" kosong) · `pdsi.md` · `direktorat-pengembangan-ekosistem-digital.md` · `lhr-lkj-kemkomdigi-2025.md` · `lhe-manajemen-risiko-2026.md`.

### 5.E Peta info kosong (gap-list auditor, item OPEN)
> Dari `wiki-info-yang-perlu-ditambahkan.md` (per 19 Mei; kini ~8 mgg basi) — **backlog ingest auditor**, bukan tugas engine:
- **ST belum di-ingest**: ST-82 (Audit JAR), ST Survei Pendahuluan OM TKPPSE 2025, ST-83 revisi; nomor 70/77/84 (Apr), 88/91 (Mei).
- **Paket Audit IT PDSI** (paralel IGRS): ST + KKP/LHA + hasil koordinasi (🔴).
- **Trello tanpa detail wiki**: PSO POS, Perangkat/Pengadaan QoS, Garuda Spark, Homologasi Bakri, Bantuan IoT, PANDI, Revisi Anggaran Ekosdig-PNBP.
- **Dok eksternal**: KepMen Komdigi 79/2026 (pelimpahan PA→KPA, 🔴), BPK induk 83/T/S, Lampiran II Nodin 1633 (matriks TLRHP), LHE AKIP 2025 penuh.
- **Regulasi standalone**: PermenPAN-RB 88/2021, PP 60/2008, Permenkominfo 6/2017, RB PermenPAN-RB, Kepmenkominfo 757/2018 (Piagam Audit), SK Irjen 11/2025 (TERRA).
- **LHA/LHR/LHE pending**: Reviu LK BUN, Reviu PIPK, Reviu LAKIP, LHE PNBP, LH Asistensi SPIP, LHP Monitoring TLHP B05, LHA IGRS.
- **Akuntabilitas internal & rutin**: roster IR-II + sertifikasi auditor, PIC Trello, notulen Rapim, laporan WFH Jumat, loop maintenance Pattern-Temuan.

---

## 6. Risiko & gerbang validasi

| Risiko | Mitigasi |
|---|---|
| Timpa file engine yang lebih maju (pola-temuan-berulang) | Fase 0 kunci arah dua-arah; jangan blind-copy |
| Sitasi regulasi superseded (Perpres 16/2018) | Reconcile Perpres 46/2025 (Fase 3) sebelum publikasikan |
| Bawa duplikat/artefak ke git | Skip `…tahapan 1.md`; lint wikilink pada file yang di-git |
| Vault (gitignored) bocor ke git | Pastikan hanya `knowledge/wiki` di-commit; `llm-wiki/` tetap ignored |
| Info kosong dianggap "lengkap" | Peta §5.D/§5.E surface eksplisit sebagai backlog auditor |

**Gerbang sebelum commit Jalur B:** RK-70 muncul di `list_temuan_patterns`; regulasi-kunci ter-parse + tak ada primary superseded; 0 wikilink rusak di file git; preload bundle memuat konteks baru.

---

## 7. Rekomendasi prioritas (urutan eksekusi bila disetujui)
1. **Fase 3 (regulasi-kunci)** — nilai tertinggi utk mutu/anti-halusinasi (Perpres 46 + 12 regulasi). *Cepat, berdampak besar.*
2. **Fase 2 (RK-70 + koreksi)** — kecil, aman, langsung dipakai agen.
3. **Fase 4 (`pattern-temuan.md`)** — indeks pattern lintas-skill.
4. **Fase 1 (vault sync)** — 98 catatan (menaikkan preload).
5. **Fase 5 (hygiene)** — duplikat + wikilink + stale-naming.
6. **Gap §5.E** — backlog ingest auditor (di luar engine; untuk perencanaan tim).

> *Dokumen turunan: pola merge `docs/MERGE-PLAN-v8.1-INTEGRAL.md`. Investigasi read-only atas `wiki_10 Juli`, `llm-wiki/wiki`, `knowledge/wiki`, `preload_context.py`.*
