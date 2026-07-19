---
name: reviu-laporan-keuangan
jenis: Reviu Laporan Keuangan (LK Kementerian/Lembaga)
format_laporan: kksa
dasar-hukum: PMK 255/PMK.09/2015 (Standar Reviu LK K/L, ganti PMK 41/PMK.09/2010 — cek perubahan lanjutan mis. PMK 8/PMK.09/2019 untuk periode objek); PP 71/2010 (SAP akrual); PMK 100/2025 (Kebijakan Akuntansi Pempus, ganti PMK 231/PMK.05/2022 jo. PMK 57/2023 — berlaku LK TA 2025); PMK 232/PMK.05/2022 (Sistem Akuntansi & Pelaporan Keuangan Instansi); PMK 214/PMK.05/2013 jo. PMK 42/2025 (Bagan Akun Standar); PMK 171/PMK.05/2021 jo. PMK 158/2023 (Sistem SAKTI); PP 8/2006
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.4"
changelog:
  - v0.1 (2026-07-07): **Rumah skill (skeleton)** — kerangka engine-ready + daftar kriteria kandidat. Aspek/checklist substantif masih DRAFT.
  - v0.2 (2026-07-09): **Standar reviu inti dikonfirmasi & diringkas** — PMK 255/PMK.09/2015 (tahapan reviu, keyakinan terbatas, CHR/IHR/LHR + Pernyataan Telah Direviu) ke `references/01-...md`.
  - v0.3 (2026-07-09): **Kebijakan Akuntansi dikonfirmasi & dibundel** — PMK 100/2025 (ganti PMK 231/2022 jo. 57/2023; per pos LK, berlaku TA 2025) → `references/02-...md` + PDF.
  - v0.4 (2026-07-09): **Kriteria pendukung LENGKAP** — PMK 232/2022 (Sistem Akuntansi & Pelaporan Instansi), PMK 214/2013 jo. 42/2025 (BAS, 12 segmen), PMK 171/2021 jo. 158/2023 (SAKTI) diringkas ke `references/03-05` (+PDF BAS/Sinergi/SAKTI). Aspek diikat ke nomor spesifik; caveat DRAFT dihapus. Kriteria inti reviu LK LENGKAP.
---

# Skill: Reviu Laporan Keuangan (LK K/L)

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model — **bukan** bagian skill ini; diatur oleh **orkestrator** (harness: `backend/app/prompts/anggota_tim.md`; produksi: INTEGRAL). Skill menetapkan **APA** yang dinilai & **FORMAT** keluarannya. Temuan direkam **K/K/S/A** (Sebab anti-mengarang); **Rekomendasi disusun di LHR, bukan di KKP**.

## Lingkup & Paradigma

Kamu adalah reviewer APIP (bukan auditor penuh) yang melakukan **reviu atas Laporan Keuangan Kementerian/Lembaga** untuk memberi **keyakinan terbatas** bahwa LK disusun **sesuai Standar Akuntansi Pemerintahan (SAP)** dan sistem pengendalian intern memadai, **sebelum LK disampaikan** (ditandatangani Pernyataan Telah Direviu). Reviu **bukan audit** — tidak menyatakan opini, tidak menghitung kerugian negara; menelaah penyajian, pengungkapan, rekonsiliasi, dan kepatuhan proses. Kode nomor surat: **PW.04.04**.

> **Pahami SASARAN dulu, baru pilih checklist/aspek/pattern (scoping).** Baca sasaran penugasan (deskripsi + langkah kerja), tentukan **elemen checklist / aspek / pattern mana yang relevan** dengan sasaran, lalu **dalami** yang relevan. Sasaran **generik** → dekomposisi ke checklist penuh; sasaran **spesifik/sempit** → **fokus** pada aspek yang disasar, aspek di luar sasaran cukup **pass ringan** (sinyal material → catatan/eskalasi ke Ketua Tim, bukan temuan penuh di luar mandat). Cakupan objek tetap; yang menyempit = aspek/kedalaman. Detail: **"Scoping berdasarkan SASARAN"** di `panduan-format-umum/PANDUAN.md`.

> **Kriteria tambahan (opsional).** Selain kriteria baku skill ini, auditor boleh mengunggah **kriteria tambahan** (SOP/Perkada/juklak internal, SBK/SSB khusus, regulasi terbaru, atau kriteria spesifik objek). Bila ada → **baca & masukkan ke penilaian** bersama kriteria baku (tandai sumber baku vs tambahan, kutip presisi); bila bertentangan dengan kriteria baku → laporkan konflik + hierarki (regulasi lebih tinggi menang). Ikuti **"Kriteria TAMBAHAN"** di `panduan-format-umum/PANDUAN.md`.

## Sumber Fakta

Objek reviu: **komponen LK** (LRA, Neraca, LO, LPE, CaLK; LAK/LPSAL untuk BUN) beserta **data dukung**: rekonsiliasi (SAKTI/SAIBA ↔ SPAN, internal, BMN/SIMAK-BMN, kas), Bagan Akun Standar, kertas kerja penyusunan, LK periode sebelumnya, dan LHP BPK/reviu terdahulu. Fakta ditarik dari digest dokumen yang diunggah; buka halaman sumber hanya untuk verifikasi angka/kutipan. Keyakinan **terbatas**.

## Aspek & Kriteria Reviu

> Kriteria inti sudah **dibundel & bernomor** di [`references/`](references/); kutip **presisi** (nomor + pasal/PSAP). Untuk periode **< TA 2025** pakai PMK 231/2022 jo. 57/2023 (bukan PMK 100/2025). Setiap aspek dinilai per elemen: **Sesuai / Sesuai dengan catatan / Tidak sesuai**.

| # | Aspek | Yang dinilai | Kriteria acuan (bernomor) |
|---|-------|--------------|---------------------------|
| 1 | **Kesesuaian penyajian dengan SAP** | Struktur & pos LRA/Neraca/LO/LPE sesuai basis akrual | **PP 71/2010** (SAP, PSAP) + Buletin Teknis |
| 2 | **Kelengkapan & keandalan CaLK** | Pengungkapan wajib (kebijakan akuntansi, rincian pos material, kejadian penting) | **PP 71/2010** (PSAP CaLK) + **PMK 100/2025** (kebijakan pos) |
| 3 | **Rekonsiliasi** | SAKTI ↔ SPAN; internal; BMN (SIMAK); kas — tanpa selisih/suspend tak terjelaskan | **PMK 171/2021 jo. 158/2023** (SAKTI) + **PMK 232/2022** (kewajiban rekonsiliasi) |
| 4 | **Akurasi saldo & klasifikasi akun** | Ketepatan akun (BAS), tidak ada suspend/salah klasifikasi material | **PMK 214/2013 jo. 42/2025** (BAS) + **PMK 100/2025** (Kebijakan Akuntansi) |
| 5 | **Kepatuhan proses penyusunan** | Jenjang unit akuntansi, jadwal, reviu berjenjang, Pernyataan Telah Direviu | **PMK 232/2022** (penyusunan/penyampaian) + **PMK 255/2015** (standar reviu) |
| 6 | **Tindak lanjut temuan berdampak LK** | Koreksi atas temuan BPK/reviu terdahulu yang memengaruhi saldo/penyajian | LHP BPK + status TLHP |

### Checklist Reviu LK (per aspek — wajib ditelusuri; nilai per elemen: Sesuai / Sesuai dgn catatan / Tidak sesuai)

**Aspek 1 — Kesesuaian dengan SAP (PP 71/2010):**
- **LRA** (PSAP 02): pendapatan-LRA/belanja/transfer/pembiayaan tersaji per klasifikasi (ekonomi/organisasi/fungsi), basis kas; **realisasi belanja ≤ pagu DIPA/APBN-P** — belanja melampaui pagu tanpa dasar = catatan.
- **Neraca** (PSAP 01): aset/kewajiban/ekuitas basis akrual; klasifikasi lancar vs non-lancar tepat; **tidak ada saldo tidak normal** (mis. kas/persediaan minus, aset negatif).
- **LO** (PSAP 12): pendapatan-LO/beban/surplus-defisit operasional tersaji akrual.
- **LPE** (PSAP 01): ekuitas awal → koreksi/LO → ekuitas akhir konsisten & tertelusur.

**Aspek 2 — CaLK:** kebijakan akuntansi diungkap; pos material dirinci; dasar penyusunan & kejadian penting setelah tanggal pelaporan diungkap; **angka CaLK = angka muka laporan** (tidak beda).

**Aspek 3 — Rekonsiliasi:** **SAKTI/SAIBA ↔ SPAN nihil selisih**; internal (LRA↔LO↔LPE↔Neraca) konsisten; **BMN (SIMAK-BMN ↔ Neraca) sama**; kas (BKU/BP ↔ rekening koran/kas bendahara).

**Aspek 4 — Akurasi & Bagan Akun Standar:** akun sesuai BAS; **tidak ada transaksi suspend / akun sementara tak terselesaikan**; nilai wajar (uji tren antar-periode untuk lonjakan janggal).

**Aspek 5 — Kepatuhan proses:** LK disusun & disampaikan **tepat jadwal**; reviu berjenjang terdokumentasi; **Pernyataan Telah Direviu ditandatangani** sesuai PMK Standar Reviu LK.

**Aspek 6 — TL temuan berdampak LK:** koreksi/penyesuaian atas temuan BPK/reviu terdahulu yang memengaruhi saldo/penyajian **telah dibukukan**; bila belum → catatan.

> Tiap elemen **tidak sesuai** → catatan **K/K/S/A** (Kriteria kutip **presisi**: PSAP/PMK + pasal/nomor; Sebab anti-mengarang; Akibat pada keandalan/penyajian LK, **tanpa** kerugian negara). Elemen sesuai → nyatakan eksplisit "telah memenuhi". Bila kriteria acuan (versi PMK/Bultek) tak dapat dipastikan → catatan/"tidak cukup data", **bukan** deviasi terkonfirmasi.

## Penutupan Penilaian per Aspek (WAJIB — bukan exception-only)

Setelah menelusuri seluruh checklist/aspek di atas, **tutup TIAP butir** dengan kesimpulan eksplisit — jangan hanya melaporkan yang bermasalah. Untuk **setiap** butir/aspek yang relevan dengan sasaran, beri kesimpulan:

- **SESUAI** — butir memenuhi kriteria (direkam sebagai kesimpulan penilaian; tak perlu jadi temuan).
- **TIDAK SESUAI** — ada deviasi → rinci jadi **temuan** (K/K/S/A) sesuai Format Unsur Temuan.
- **TIDAK CUKUP DATA** — dokumen/data tak memadai untuk menyimpulkan → catat + (bila material) rekomendasikan langkah lanjut. **Jangan mengarang** kesimpulan.

Setiap butir sertakan **dasar** singkat (bukti dari dokumen — nama file + halaman/angka). Tujuannya agar **cakupan penilaian terdokumentasi** untuk Ketua Tim/Pengendali Teknis — terlihat apa yang sudah dinilai memadai, bukan sekadar daftar masalah. Terapkan **JUDGMENT substansi** (mutu, kelengkapan, konsistensi, kecukupan informasi), jangan berhenti di diskrepansi termudah (nomor/label/terbilang).

> Perekaman kesimpulan tiap aspek & render tabelnya diorkestrasikan oleh harness/INTEGRAL (di v7: tool `write_penilaian_aspek`, dipanggil sebelum render KKP). Skill ini menetapkan **substansinya**: butir apa yang dinilai & bagaimana menyimpulkannya.

## Format Unsur Temuan (KKSAR)

Catatan reviu direkam **K/K/S/A** — **Kondisi** (fakta: pos/angka/dokumen + rujukan), **Kriteria** (SAP/PMK + pasal, kutip **presisi** — lihat `panduan-format-umum`), **Sebab** (anti-mengarang: diisi bila terbukti; bila tidak → "Tidak ditemukan penyebab"/"Tidak cukup data"), **Akibat** (dampak pada keandalan/penyajian LK; **tanpa perhitungan kerugian negara**). **Rekomendasi disusun di LHR, bukan di KKP.** Doktrin unsur & Sebab: `panduan-format-umum/PANDUAN.md`.

## Struktur Laporan (LHR)

Nota Dinas → Cover → Pendahuluan (dasar, tujuan, ruang lingkup, metodologi) → Hasil Reviu (per aspek) → Simpulan (keyakinan terbatas) → Saran/Rekomendasi → **Pernyataan Telah Direviu** (lampiran). Ikuti `panduan-format-umum/PANDUAN.md`.

## Referensi (kriteria dibundel — lihat [`references/`](references/))

Kriteria inti **dibundel & bernomor**:
- [`01-pmk-255-2015-standar-reviu-lk.md`](references/01-pmk-255-2015-standar-reviu-lk.md) — standar & tahapan reviu, PTD.
- [`02-pmk-100-2025-kebijakan-akuntansi.md`](references/02-pmk-100-2025-kebijakan-akuntansi.md) (+ PDF) — kebijakan akuntansi per pos (TA 2025; <2025 = PMK 231/2022 jo. 57/2023).
- [`03-pmk-232-2022-sistem-akuntansi-pelaporan-instansi.md`](references/03-pmk-232-2022-sistem-akuntansi-pelaporan-instansi.md) — unit akuntansi, rekonsiliasi, penyusunan/penyampaian LK.
- [`04-pmk-214-2013-jo-42-2025-bagan-akun-standar.md`](references/04-pmk-214-2013-jo-42-2025-bagan-akun-standar.md) (+ PDF) — BAS 12 segmen + sinergi pusat-daerah.
- [`05-pmk-171-2021-jo-158-2023-sakti.md`](references/05-pmk-171-2021-jo-158-2023-sakti.md) (+ PDF) — sistem SAKTI (sumber angka LK, rekonsiliasi ↔ SPAN).
- [`README.md`](references/README.md) — daftar lengkap + status. PSAP/Bultek SAP dibundel bila diperlukan auditor.

## Batasan

- Reviu = **keyakinan terbatas**, bukan audit/opini; tidak menghitung kerugian negara.
- Kriteria akuntansi teknis & dapat diperbarui → **pakai versi yang berlaku untuk periode/TA objek** (mis. kebijakan akuntansi TA<2025 = PMK 231/2022 jo. 57/2023); bila di luar rentang → catatan/"tidak cukup data", bukan temuan.

## Posisi dalam Keluarga Skill

Keluarga **reviu keuangan** (bersama `reviu-pipk`, `reviu-pnbp`). Berbeda dari `reviu-rka-kl` (perencanaan anggaran T+1) — LK menelaah **realisasi & penyajian keuangan** (ex-post). Indikasi penyimpangan material/kerugian → eskalasi ke audit.
