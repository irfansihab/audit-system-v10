# Penyelarasan Workflow dengan Pedoman Pengawasan — Status v10 (Fase 2)

**Prinsip (tetap):** SK/Juknis **mengikuti sistem** (engine = jangkar); engine = mesin produksi substansi, **garis finis = laporan disetujui**, setelahnya = administrasi (Tahapan 8, TU). Analisis rinci 36 SDP + 13 errata + matriks proporsionalitas: [`USULAN-REVISI-SK.md`](USULAN-REVISI-SK.md) (basis v9). Ringkasan pimpinan: [`penyelarasan-juknis-v8.html`](penyelarasan-juknis-v8.html). Pedoman asli: `llm-wiki/wiki/pedoman-pengawasan-buku-i/ii/iii.md` + `pedoman-umum-pengawasan.md` (vault).

Dokumen ini = **re-validasi konformansi engine v10** setelah **hardening (Fase 1)** + **merge subsistem laporan v8.8** + **portabilitas P1** — perubahan yang terjadi SETELAH analisis v9 ditulis.

## 1. Konformansi engine terhadap Pedoman — TERVERIFIKASI ✅

Errata pedoman **sisi-engine** (bukan sisi-draft-SK) dicek pada engine v10 terkini:

| Errata (§4 USULAN) | Status engine v10 | Bukti |
|---|---|---|
| **#1** Shell laporan konsisten | ✅ | render_lhp per-jenis; skeleton non-audit tanpa BAB-campur/audit-leak |
| **#2** Unsur baku **KKSAR** | ✅ (Fase 1 hardening) | CCSAA→KKSAR di skill audit; PANDUAN mengunci KKSAR; QC SAIPI 2320 cek Sebab jenis-aware |
| **#4** "audit"/"Tim Audit" bocor lintas-jenis | ✅ | `replace_label_in_doc(_label_pairs(verb))` substitusi label per-jenis (Audit/Reviu/Evaluasi/Pemantauan); skeleton pemantauan/konsultansi/evaluasi/reviu **0 audit-leak** |
| **#5** Ringkasan Eksekutif frasa per-jenis | ✅ | simpulan per-jenis: audit=keyakinan **memadai**; reviu/evaluasi=**terbatas**; pemantauan/konsultansi=**non-assurance** |
| **#6** Survei Pendahuluan wajib audit saja | ✅ | `survey_pendahuluan.py` guard `is_audit_skill` (raise bila non-audit); Tahapan 0 audit-only |

**Merge v8.8 justru MEMPERKUAT penyelarasan:** laporan kini **faithful per-jenis** (skeleton + render_lhp per-seksi), bukan generik — persis yang dituntut Pedoman (struktur & assurance sesuai jenis pengawasan).

Errata sisa (#3 ADTT/PDTT, #7 anggaran 3×, #8 penomoran KP/PKP, #9-#13) = ranah **draft SK/dokumen birokrasi**, bukan engine — dibawa ke rapat revisi SK (rekomendasi §6 USULAN).

## 2. Pemetaan SDP produksi ↔ v10 (update dari v9)

Semua artefak produksi WAJIB **ADA & terverifikasi** di v10:

| SDP | Artefak | v10 |
|---|---|---|
| P.05 Survei Pendahuluan (audit) | `survey_pendahuluan.py` + route + tombol UI | ✅ **BARU di v10** (merge v8.8 Fase 2) — sebelumnya konsep |
| P.02 Kartu Penugasan | tab KP + template | ✅ |
| P.06 PKP | `_PKP/sasaran-assignment.json` (kontrak, disuplai orkestrator) | ✅ (P1#8: UI-agnostik) |
| PL.08 KKP & Temuan | `temuan.json` + `render_kkp` (KKSAR jenis-aware) + gate LKE SPIP/SAKIP | ✅ (gate LKE **BARU** merge Fase 3) |
| M.01-03 Kendali Mutu Berjenjang | `lembar_reviu.py` (KT→PT→PM QA/QC 14 butir) | ✅ |
| L.01-06 Laporan + Ringkasan Eksekutif | `render_report`→`render_lhp` (per-seksi, per-jenis) | ✅ **DITINGKATKAN** (merge v8.8 Fase 1) |
| K.01 Daftar Temuan & Rekomendasi (ekspor) | `export_dhp.py` + `render_daftar_temuan` | ✅ |
| K.02 Surat Penyampaian | `export_surat.py` (Tahapan 8) | ✅ |
| Tahapan 8 Administrasi (TU) | `routes/administrasi.py` | ✅ |

**Proporsionalitas per-jenis (§3 USULAN):** diterapkan emergen — Survei hanya audit; Daftar Temuan hanya bila ada temuan; kolom KKP & paradigma laporan menyesuaikan jenis; Sebab per doktrin (KKSA vs LKE vs konsultansi). *Diperkuat Fase 1 hardening (QC Sebab jenis-aware) + merge (render per-jenis).*

## 3. Batas produksi vs administrasi (garis serah) — tegas

- **Produksi (engine):** s.d. laporan disetujui → ekspor **LHP final + Daftar Temuan & Rekomendasi**.
- **Administrasi (Tahapan 8, TU / SIMWAS / INTEGRAL):** penomoran resmi, TTE, distribusi, arsip, pemantauan TL.
- **Portabilitas (P1):** engine kini **buta-DB & UI-agnostik** — orkestrator (INTEGRAL) menyuplai kontrak file (`sasaran-assignment.json`, `hitl-overlay.json`) & menangani administrasi. Penyelarasan ini konsisten dengan pivot engine-only.

## 4. Kesimpulan Fase 2

**Engine v10 SELARAS dengan Pedoman Pengawasan** — dan lebih kuat dari v9 (survei terimplementasi, laporan faithful per-jenis, gate LKE, portabilitas INTEGRAL). Tidak ada gap engine yang tersisa; penyelarasan berikutnya bersifat **draft-SK** (errata birokrasi §4 #3/#7-#13) yang dibawa ke tim penyusun SK, bukan pekerjaan engine.

**Tindak lanjut (non-engine):** sahkan matriks proporsionalitas (§3) + pemetaan SDP↔v10 (§2 di atas) + klausul digital-native sebagai lampiran SK; perbaiki errata draft di rapat revisi.
