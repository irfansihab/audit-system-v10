# Pattern Temuan — Katalog Sistem Audit Inspektorat II

**Summary**: Katalog terstruktur **30 pattern temuan berulang** yang disintesis dari ~290 temuan substantif lintas **80+ ekstrak surat resmi** di wiki Inspektorat II (LHP/LHA/LHR/LHE/CHR/DHA/KHA/Notisi/Atensi/ADTT/Nota Dinas/TLHP/BPK). Setiap pattern dilengkapi: kategori, severity, frekuensi kemunculan, trigger indicators (sinyal awal untuk auditor), prosedur audit yang direkomendasikan, template rekomendasi, dan link ke sumber bukti. **Fungsi utama**: dasar perencanaan audit preventif, query knowledge base untuk PKPT/Audit AI, briefing tim, dan input *fraud risk assessment* sesuai strategi 3.2.1.d [[renstra-itjen-2025-2029]].

**Sources**: Sintesis lintas 80+ wiki page hasil ekstrak surat — lihat tabel index pattern per kategori untuk daftar sumber per pattern. Menggantikan dan memperluas [[pola-temuan-berulang]] (versi 2026-04-24 yang hanya mencakup 9 pattern dari 11 LHP).

**Last updated**: 2026-05-18

---

## Tentang Katalog

### Tujuan

Katalog ini dirancang sebagai **knowledge base struktural** untuk:

1. **Audit preventif** — auditor dapat mengantisipasi pola temuan sebelum penugasan, mempersiapkan checklist khusus.
2. **Query oleh Audit AI** — setiap pattern punya kode (P-XX), kategori, trigger indicator yang machine-readable untuk integrasi ke sistem (Trello, CACM, TERRA).
3. **Risk assessment** — input untuk Form II MR ([[piagam-mr-ir2-2026]]) dan penyusunan PKPT ([[pkpt-2026]]).
4. **Onboarding** — anggota tim baru dapat memahami "DNA temuan" IR II dalam 1 dokumen.
5. **Tindak Lanjut** — pattern terkait TLHP outstanding (P-25 s.d. P-27) memudahkan eskalasi.

### Skema Severity

| Severity | Kriteria |
|----------|----------|
| **🔴 Tinggi** | Berulang ≥3 satker × 2 TA, ATAU dampak finansial ≥Rp10M, ATAU temuan BPK eksternal |
| **🟡 Sedang** | Berulang ≥3 dokumen ATAU dampak finansial Rp1–10M ATAU isu struktural |
| **🟢 Rendah** | Insidental ATAU dampak finansial <Rp1M ATAU sudah dimitigasi |

### Skema Kategori

11 kategori yang menutupi seluruh ruang audit Inspektorat II:

| Kode | Kategori | Definisi singkat |
|------|----------|------------------|
| A | PBJ & Kontrak | Pengadaan barang/jasa, kontrak, penagihan, pembayaran |
| B | PNBP & Pendapatan | Pungutan, koreksi, pengembalian, piutang BHP/IPP |
| C | Anggaran & Perencanaan | Renja, RKA-K/L, revisi, relaksasi, restrukturisasi |
| D | Aset BMN | Inventarisasi, alih status, pemeliharaan, idle asset |
| E | Tata Kelola Pasca-SOTK | Transisi Kominfo→Komdigi, SOP usang, ownership warisan |
| F | Sistem Informasi & Infrastruktur TI | TKPPSE, CSE, PDNS, SATRIA, SIMR, Ev-SAKIP, TERRA |
| G | SPI / MR / AKIP / RB / ZI | Maturitas governance internal |
| H | TLHP / Pengawasan Internal | Tindak lanjut rekomendasi BPK + internal |
| I | Layanan Publik & Operasional | Kontinuitas layanan (TKPPSE, LPU, konten ilegal) |
| J | SDM & Personalia | Kompetensi, turnover, sertifikasi |
| K | Regulasi & Koordinasi Lintas K/L | PDP, MoU APJII/BSSN/OJK/Polri/PPATK/LKPP |

---

## Daftar Pattern (Index)

| # | Pattern | Kat | Severity | Freq |
|---|---------|-----|----------|------|
| P-01 | Kontrak Retroaktif Pasca-SOTK (Pekerjaan Tanpa Kontrak) | A,E | 🔴 | 8+ |
| P-02 | SLA Tidak Termonitor / Kapasitas Layanan Jauh di Bawah Target | A,F | 🔴 | 7 |
| P-03 | Vendor Lock-in pada Infrastruktur Kritis | A,F | 🔴 | 5 |
| P-04 | Data Prestasi Kerja Tidak Memadai / Backfilling Monitoring | A | 🟡 | 5 |
| P-05 | Adendum Kontrak Inkonsisten (Nomor Ganda, Tanggal Tidak Berurutan) | A | 🟡 | 2 |
| P-06 | SBK Belanja Melewati Standar Biaya (Tanpa Justifikasi) | A,C | 🟡 | 3+ |
| P-07 | Pembayaran Retroaktif Tidak Memenuhi Syarat LKPP 22441 | A,K | 🔴 | 3 |
| P-08 | Klasifikasi Akun Belanja Salah (Belanja Barang vs Aset Tetap) | A,D | 🟡 | 2 |
| P-09 | Penagihan Lewat Bukti / Invoice Tidak Detail | A | 🟡 | 4 |
| P-10 | Koreksi PNBP Ditolak karena Tafsir Regulasi (BHP Telekomunikasi) | B,K | 🟡 | 4 |
| P-11 | Pengembalian Lebih Bayar PNBP — SOP Penelitian Tidak Substantif | B | 🟡 | 2 |
| P-12 | Penerimaan PNBP "No Name" (Setoran Tanpa Wajib Bayar) | B | 🟢 | 2 |
| P-13 | Piutang Macet KPBU/Homologasi (Sengketa Multi-Tahun) | B,K | 🔴 | 3+ |
| P-14 | PPN Tidak Dipungut karena Misinterpretasi Klasifikasi Transaksi | B | 🟡 | 1 |
| P-15 | Revisi Anggaran Cascade (≥4 Iterasi per TA) | C,E | 🔴 | 6+ |
| P-16 | Relaksasi/Tambahan Anggaran Flash-Cash Q3-Q4 | C | 🟡 | 4 |
| P-17 | Penamaan RO Tidak Sesuai Substansi Anggaran | C | 🟡 | 2 |
| P-18 | Pagu vs Kebutuhan Bare Minimum Gap Signifikan (>50%) | C | 🔴 | 1 |
| P-19 | SIRUP Pagu Draft Tinggi (>50%) Menjelang Akhir TW I | A,C | 🟡 | 1 |
| P-20 | Aset BMN Tertahan Alih Status Antar-Entitas (Likuidasi/SOTK) | D,E | 🔴 | 3+ |
| P-21 | Aset BMN Idle Risk (Investasi Besar Tanpa Sustainability Plan) | D,F | 🔴 | 2 |
| P-22 | Aset Kendaraan / SITAC Penatausahaan Tidak Sesuai | D | 🟡 | 2 |
| P-23 | Pedoman/SOP Usang (Nomenklatur Pra-SOTK, Regulasi Pengganti Belum) | E,K | 🔴 | 6+ |
| P-24 | Warisan Aptaka — Ownership Rekomendasi/Aset Fragmen Pasca-Likuidasi | E,H | 🔴 | 4 |
| P-25 | TLHP Outstanding Struktural (>2 Tahun, Butuh Regulasi/MoU) | H,K | 🔴 | 5+ |
| P-26 | Asymmetric TL Eksternal vs Internal antar-Ditjen | H | 🟡 | 1 |
| P-27 | JAR (Jaminan Pengambil Alih) Verifikasi Tidak Tuntas | A,H | 🔴 | 1 |
| P-28 | Sistem TI Belum Early Warning (Repositori, Bukan Decision Support) | F,G | 🟡 | 3 |
| P-29 | Sistem TI Outdated / Topologi Bypass-able (HTTPS, DoH, VPN) | F | 🔴 | 4 |
| P-30 | Layanan Baru Diluncurkan dengan Kelemahan Tata Kelola & Keamanan | F,I | 🟡 | 2 |
| P-31 | Kajian Teknis Tanpa Implementasi (Dokumen Mati) | C,F | 🟡 | 2 |
| P-32 | Insiden Siber Tanpa Adjustment Kontrak/Pembayaran (Brain Cipher) | F,A | 🔴 | 1 |
| P-33 | SPIP / MR / RB Maturitas Stagnan (Gap Target Konsisten) | G | 🔴 | 6+ |
| P-34 | Zona Integritas Flat 2 Tahun (16,67%) | G | 🔴 | 2 |
| P-35 | LKj / IKU Data Tidak Traceable Sumbernya | G | 🟡 | 3 |
| P-36 | Turnover Pimpinan Tinggi pada Periode Kritis | E,J | 🟡 | 2 |
| P-37 | Kontinuitas Layanan Publik Terancam Akibat Tunggakan Pembayaran | I | 🔴 | 2 |
| P-38 | Realisasi Belanja Sangat Rendah (<20%) di Q3 — Lag Pasca-Restrukturisasi | C,E | 🟡 | 3 |
| P-39 | MoU Lintas K/L Belum Ada untuk Isu yang Membutuhkan Koordinasi (PDP, ISP, Konten) | K | 🔴 | 5+ |
| P-40 | Tumpang Tindih Infrastruktur Operasional (TKPPSE vs RTBH vs TrustNG vs RPZ) | F,C | 🔴 | 1 |

**Total**: 40 pattern. Sebagian besar bersifat **lintas-kategori** — kode kategori utama ditampilkan pertama.

---

## A. PBJ & Kontrak

### P-01 | Kontrak Retroaktif Pasca-SOTK (Pekerjaan Tanpa Kontrak) 🔴

**Pola**: Pekerjaan layanan terus berjalan (telekomunikasi, colocation, ISP, OM) tetapi kontrak belum ditandatangani karena DIPA terlambat akibat perubahan SOTK Kominfo→Komdigi. Kontrak retroaktif dilegalisasi via **Perpres 46/2025 Pasal 9(1)f²**.

**Trigger Indicators**:
- DIPA terbit setelah Maret pada TA berjalan
- Layanan kontinyu (telekomunikasi, hosting, langganan) tetap aktif
- Tagihan masuk tanpa nomor kontrak referensi
- Ada *Surat Perintah Kelanjutan Pekerjaan* tanpa dasar kontrak formal

**Akar Masalah**:
- Transisi SOTK menyebabkan DIPA terlambat 3–6 bulan
- Belum ada playbook transisi kontrak lintas Ditjen lama→baru
- Vendor tetap bekerja karena layanan bersifat *continuous*

**Audit Procedure**:
1. Cek tanggal DIPA vs tanggal mulai pekerjaan riil (gap = window risk)
2. Cek apakah ada *Surat Perintah Kelanjutan*, BAUP, atau dokumen interim lain
3. Cek pemenuhan 3 syarat LKPP 22441 untuk pembayaran retroaktif (lihat P-07)
4. Verifikasi data prestasi kerja periode tanpa-kontrak (lihat P-04)
5. Hitung kelebihan/kekurangan pembayaran vs SLA aktual

**Recommendation Template**:
- Susun SOP transisi kontrak untuk TA berikutnya
- Hindari pekerjaan berjalan tanpa payung hukum: pra-DIPA → *letter of intent* atau MoU jangka pendek
- Wajibkan analisis urgensi sebelum melanjutkan pekerjaan tanpa kontrak

**Sumber Bukti**: [[lhr-kontrak-aptika-2025]] (Rp6,11M), [[lhr-kontrak-pembayaran-pste-2025]] (Rp2,13M PSTE), [[lhr-pemblokiran-rtbh-trustng-2025]] (Rp400jt), [[lha-om-tkppse-2024]] (Rp78,56M), [[lha-om-tkppse-2025]] (Rp2,69M Des 2025), [[lhp-pengadaan-redesain-tkppse-2026]] (6 PJT), [[bpk-spi-lk-kominfo-2024]] (TKPPSE Rp4,66M + utang Rp57,28M), [[bpk-temuan-pdns-satria-2024]] (PDNS Rp110,41M)

---

### P-02 | SLA Tidak Termonitor / Kapasitas Layanan Jauh di Bawah Target 🔴

**Pola**: SLA kontrak menargetkan ≥99,5% uptime, realisasi 50,12% (TKPPSE) atau 52,82% (KOS Smartfren). Metro-E lokasi tertentu mati 1 tahun tanpa ditindaklanjuti.

**Trigger Indicators**:
- Laporan bulanan SLA tidak ditampilkan secara konsisten
- Tidak ada *escalation matrix* saat SLA breach
- Vendor sub-penyedia (PJT) tidak laporan ke prime contractor (PT SUFI) atau prime tidak laporan ke PA/KPA

**Audit Procedure**:
1. Minta dashboard SLA bulanan; cek gap antara reported vs measured
2. Sampling ≥3 lokasi untuk uji fisik konektivitas Metro-E
3. Cek Berita Acara Pemeliharaan vs ticket Zabbix/Log Server (lihat P-04)
4. Hitung *liquidated damages* yang seharusnya dikenakan

**Recommendation Template**:
- Wajibkan dashboard SLA real-time (tidak hanya bulanan)
- Klausul *liquidated damages* harus eksplisit dan terhitung otomatis
- Audit IT framework "5 area sasaran IGRS" (lihat [[sasaran-audit-igrs]])

**Sumber Bukti**: [[lha-om-tkppse-2024]] (SLA 50,12%), [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]], [[lha-om-tkppse-2025]] (Rp470jt selisih data), [[dha-tahap2-om-tkppse-2024]] (KOS Smartfren 52,82%), [[bpk-laporan-hasil-pemeriksaan]] (TKPPSE eff 22,44%), [[bpk-kinerja-pste-2024]]

---

### P-03 | Vendor Lock-in pada Infrastruktur Kritis 🔴

**Pola**: Satu vendor menguasai infrastruktur fundamental tanpa alternatif. Contoh: PT SUFI menguasai 187 titik TKPPSE + Metro-E Secure; PT Moratel topologi terenkripsi; PT Lintasarta di DC SUFI; BAKTI BTS 4G ke PT TKS.

**Trigger Indicators**:
- Pengadaan menggunakan *Surat Perintah Kelanjutan* (bukan tender)
- Vendor mengontrol topologi/konfigurasi yang tidak dapat di-handover
- Tidak ada *right to audit clause* di kontrak
- Sub-kontraktor (PJT) menggantungkan setoran ke prime

**Audit Procedure**:
1. Pemetaan vendor: identifikasi siapa kontrol infrastruktur kritis
2. Cek klausul *exit strategy* dan *vendor transition* di kontrak
3. Cek *right to audit* (auditor/Itjen berhak akses log/metadata)
4. Identifikasi alternatif teknologi (mis. PSrE root CA vs vendor proprietary)

**Recommendation Template**:
- *Cost-benefit analysis* vendor besar vs vendor alternatif sebelum perpanjangan
- Klausul *audit trail* wajib eksplisit di KAK
- Strategi diversifikasi vendor untuk infrastruktur kritis (minimal 2 sumber)

**Sumber Bukti**: [[lha-om-tkppse-2024]], [[lhp-pengadaan-redesain-tkppse-2026]] (Moratel/Lintasarta), [[bpk-lhp-lk-kominfo-2023]] (BTS 4G PT TKS), [[bpk-spi-lk-kominfo-2024-detail]] (Piutang Homologasi BAKTI)

---

### P-04 | Data Prestasi Kerja Tidak Memadai / Backfilling Monitoring 🟡

**Pola**: Pekerjaan berjalan tetapi sistem monitoring (Zabbix, Log Server, BKU) belum aktif/tidak lengkap. Audit harus backfill data prestasi secara manual, menghasilkan **Rp4,66M–Rp49,06M** tidak dapat dinilai.

**Trigger Indicators**:
- Pekerjaan dimulai sebelum sistem monitoring di-deploy
- Data BAPL/BAUP tidak ada untuk periode tertentu
- 20 dari 58 site tanpa data (sample TKPPSE 2024)

**Audit Procedure**:
1. Inventarisasi sistem monitoring vs tanggal mulai pekerjaan
2. Sampling 20% lokasi/transaksi untuk uji backfill capability
3. Tentukan threshold "dapat diyakini" vs "tidak dapat dinilai"

**Recommendation Template**:
- Investasi monitoring **bersamaan** dengan start layanan (bukan setelah)
- Kontrak mewajibkan delivery monitoring data sebagai prasyarat penagihan

**Sumber Bukti**: [[lha-om-tkppse-2024]], [[dha-tahap2-om-tkppse-2024]], [[kha-revisi2-om-tkppse-2024-rp16-rp57]], [[bpk-spi-lk-kominfo-2024]] (PDNS adjustment), [[bpk-temuan-pdns-satria-2024]]

---

### P-05 | Adendum Kontrak Inkonsisten (Nomor Ganda, Tanggal Tidak Berurutan) 🟡

**Pola**: Inkonsistensi administratif dokumen kontrak yang baru terlihat saat reviu detail. Contoh: server crawling CSE Rp40,1M — 2 adendum nomor sama (AD01) isi berbeda.

**Trigger Indicators**:
- Adendum lebih dari satu pada tanggal sama
- Nomor adendum tidak sequential
- Versi dokumen ganda tanpa watermark/identifier

**Audit Procedure**:
1. Mintakan log adendum terurut tanggal
2. Cek versi via metadata file (created/modified)
3. Cek BA penandatanganan adendum

**Recommendation Template**:
- Sistem nomenklatur adendum terpusat (otomatis incremental)
- Pembatalan resmi adendum yang tidak digunakan

**Sumber Bukti**: [[lhr-server-crawling-2025]]

---

### P-06 | Belanja Melewati Standar Biaya (SBK) tanpa Justifikasi 🟡

**Pola**: Tambahan anggaran mencatat belanja yang melampaui SBK Permenkeu signifikan (mis. Pemantauan Rp5,8M vs SBK Rp240jt; SDM Rp8,1M).

**Trigger Indicators**:
- Belanja non-operasional jauh lebih besar dari pos sejenis di TA sebelumnya
- TOR tidak mencantumkan komparasi dengan SBK
- Komponen biaya pegawai non-operasional di-bundling ke kontrak vendor

**Audit Procedure**:
1. Cross-check belanja dengan SBK Permenkeu untuk pos sejenis
2. Cek justifikasi tertulis untuk *overshoot* >20%
3. Identifikasi *bundling* yang menyembunyikan komponen non-operasional

**Recommendation Template**:
- Wajibkan justifikasi *overshoot* SBK ≥20% di TOR
- Audit reviu tambahan/relaksasi anggaran fokus pos *overshoot*

**Sumber Bukti**: [[chr-tambahan-anggaran-wasdig-2025]] (Rp414,7M), [[bpk-lk-ba-999-08-kominfo-2024]] (LTK Rp1M, sopir Rp21,49M)

---

### P-07 | Pembayaran Retroaktif Tidak Memenuhi 3 Syarat LKPP 22441 🔴

**Pola**: Framework retroaktif Perpres 46/2025 Pasal 9(1)f² mewajibkan 3 syarat: **analisis urgensi**, **reviu APIP**, dan **audit BPKP**. Pada kasus OM TKPPSE Rp57,34M, ketiganya gagal.

**Trigger Indicators**:
- Tidak ada *memo analisis urgensi* dari PA/KPA
- APIP belum issue Laporan Hasil Verifikasi
- BPKP menolak/belum issue audit

**Audit Procedure**:
1. Cek dokumen 3 syarat secara berurutan
2. Verifikasi tanggal masing-masing dokumen vs tanggal pembayaran
3. Jika ada syarat gagal: rekomendasikan **TIDAK menarik pembayaran** atau cari payung hukum lain

**Recommendation Template**:
- Catatan: APIP harus issue Laporan Hasil Verifikasi sebelum bayar
- Eskalasi ke BPKP jika nilai >Rp10M

**Sumber Bukti**: [[kha-revisi2-om-tkppse-2024-rp16-rp57]] (Rp57,34M), [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]]

---

### P-08 | Klasifikasi Akun Belanja Salah (Belanja Barang vs Aset Tetap) 🟡

**Pola**: Pengadaan yang seharusnya akun **53 (Belanja Modal/Aset)** salah dianggarkan ke **akun 52 (Belanja Barang & Jasa)**. Contoh: Jasa Konsultansi Pengawasan Konstruksi, Helikopter BTS 4G, PMO BTS 4G — Rp84,95M.

**Trigger Indicators**:
- Belanja "Jasa" tetapi outputnya aset fisik
- KDP tidak ada padahal pekerjaan multi-tahun
- Aset Lain-Lain bertambah tanpa BAPL formal

**Audit Procedure**:
1. Cross-check akun di RKA vs sifat output (jasa habis pakai vs aset)
2. Cek pencatatan KDP dan BAPL closure
3. Verifikasi penyusutan/depresiasi

**Recommendation Template**:
- Pelatihan klasifikasi akun untuk Tim Perencanaan
- Reviu RKA-K/L wajib menguji konsistensi akun vs output

**Sumber Bukti**: [[bpk-spi-lk-kominfo-2024]], [[bpk-spi-lk-kominfo-2024-detail]] (Aset BTS 4G SITAC Rp1,32M)

---

### P-09 | Penagihan Lewat Bukti / Invoice Tidak Detail 🟡

**Pola**: Tagihan tidak detail per lokasi/bulan, perhitungan prorata tidak konsisten, invoice tidak mencantumkan SLA achieved.

**Trigger Indicators**:
- Tagihan agregat tanpa breakdown
- Selisih perhitungan prime contractor (SUFI) vs sub (PJT) >10%
- Invoice tidak mencantumkan kurs/tanggal rekonsiliasi

**Audit Procedure**:
1. Minta breakdown per item/lokasi
2. Rekonsiliasi data prime vs sub
3. Cek konversi kurs (gunakan kurs tanggal penerbitan tagihan, bukan rekonsiliasi)

**Recommendation Template**:
- Template invoice wajib mencantumkan: lokasi, periode, SLA achieved, kurs (jika valas)
- Klausul *invoice rejection* untuk invoice tidak detail

**Sumber Bukti**: [[kha-revisi2-om-tkppse-2024-rp16-rp57]] (Rp4,78M), [[bpk-temuan-pdns-satria-2024]] (SATRIA kurs Rp1,51M), [[lha-om-tkppse-2025]]

---

## B. PNBP & Pendapatan Negara

### P-10 | Koreksi PNBP Ditolak karena Tafsir Regulasi (BHP Telekomunikasi) 🟡

**Pola**: Wajib bayar mengajukan koreksi PNBP, BUKAN karena kesalahan matematis tetapi karena keberatan tafsir regulasi (SIP Trunk / SMS Notifikasi / Availability Payment apakah termasuk pendapatan telko). APIP konsisten **menolak** koreksi.

**Trigger Indicators**:
- Wajib bayar mengirim surat keberatan substantif (bukan minta restitusi karena salah hitung)
- Klaim diasumsikan "bukan pendapatan telko" untuk komponen tertentu
- Bukti pendukung berupa kontrak komersial wajib bayar (bukan dokumen Direktorat)

**Audit Procedure**:
1. Cek dasar hukum (PM Kominfo 5/2021, PP terkait)
2. Konfirmasi tafsir ke Biro Hukum Kemkomdigi
3. Reviu rekomendasi APIP konsisten lintas wajib bayar

**Recommendation Template**:
- Sosialisasi PM Kominfo 5/2021 ke wajib bayar (cegah dispute)
- Pedoman tafsir spesifik untuk komponen kontroversial (SIP Trunk, SMS, AP)

**Sumber Bukti**: [[lhr-koreksi-pnbp-atlasat-2025]] (SIP Trunk Rp65,75jt), [[lhr-koreksi-pnbp-dalnet-2025]] (SIP Trunk Rp329,64jt), [[lhr-koreksi-pnbp-satkomindo-2025]] (SMS Rp507,81jt), [[lhr-koreksi-pnbp-lti-palapa-ring-2025]] (AP Rp9,61M kumulatif), [[lhr-koreksi-pnbp-artacomindo-2025]] (deadline VSAT Rp130jt)

---

### P-11 | Pengembalian Lebih Bayar PNBP — SOP Penelitian Tidak Substantif 🟡

**Pola**: Permohonan pengembalian PNBP TB 2023 diproses tanpa analisis substantif penyebab (kelemahan SOP).

**Trigger Indicators**:
- Berita acara penelitian hanya mencatat verifikasi nominal
- Tidak ada analisis penyebab lebih bayar
- Pola serupa berulang lintas wajib bayar (MitraComm + UnggulCipta)

**Audit Procedure**:
1. Cek SOP penelitian pengembalian PNBP
2. Sampling 20% kasus untuk uji substansi analisis
3. Korelasi dengan SOP wajib bayar (apakah perhitungan PNBP standar)

**Recommendation Template**:
- Bangun SOP baku penelitian pengembalian PNBP
- Wajibkan analisis penyebab di setiap LHR pengembalian

**Sumber Bukti**: [[lhr-pnbp-mitracomm-2025]] (Rp98,74jt), [[lhr-pnbp-unggulcipta-2025]] (Rp1,89jt)

---

### P-12 | Penerimaan PNBP "No Name" (Setoran Tanpa Wajib Bayar) 🟢

**Pola**: Setoran PNBP via teller BRI tanpa keterangan wajib bayar — tidak dapat ditelusuri ke perizinan.

**Trigger Indicators**:
- Buku Kas Pembantu mencatat setoran "Tn/Ny" atau "tanpa nama"
- Tidak ada virtual account wajib untuk pembayaran perizinan
- Selisih antara setoran IPP vs jumlah perizinan terbit

**Audit Procedure**:
1. Cek mekanisme pembayaran perizinan (apakah virtual account wajib)
2. Sampling setoran no-name di BKU
3. Rekonsiliasi setoran vs database perizinan

**Recommendation Template**:
- Implementasi virtual account wajib untuk semua perizinan PNBP
- Pelatihan teller BRI untuk mewajibkan keterangan

**Sumber Bukti**: [[lhr-lk-ppi-2024]] (Rp1,15M), [[lhr-lk-ppi-sem1-2025]] (Rp57,58jt)

---

### P-13 | Piutang Macet KPBU/Homologasi (Sengketa Multi-Tahun) 🔴

**Pola**: 3 BUP Palapa Ring piutang macet Rp47,75M (sengketa KPBU 6 tahun, PTUN menang pemerintah tapi kasasi MA pending); piutang homologasi BAKTI ongoing.

**Trigger Indicators**:
- Status piutang "macet" di buku piutang
- Putusan PTUN/MA pending
- Tidak ada rencana eksekusi penagihan

**Audit Procedure**:
1. Cek status putusan pengadilan terkini
2. Verifikasi cadangan kerugian piutang (CKP)
3. Identifikasi opsi penghapusan/restrukturisasi

**Recommendation Template**:
- Update CKP sesuai expected loss
- Koordinasi Biro Hukum + Direktorat Pengendalian untuk eksekusi

**Sumber Bukti**: [[lhr-lk-ppi-sem1-2025]] (Rp47,75M Palapa Ring), [[lhr-koreksi-pnbp-lti-palapa-ring-2025]], [[bpk-spi-lk-kominfo-2024-detail]] (Homologasi BAKTI)

---

### P-14 | PPN Tidak Dipungut karena Misinterpretasi Klasifikasi Transaksi 🟡

**Pola**: Bendahara BAKTI tidak memungut PPN Rp80,04M atas pengadaan IP HUB SATRIA-1 karena salah interpretasi surat KPP (mengira jasa telekomunikasi padahal pengadaan barang).

**Trigger Indicators**:
- Tarif PPN 0% atau exempted untuk pengadaan barang
- Bendahara hanya mengandalkan satu surat KPP tanpa konfirmasi
- Surat KPP terkait jasa telko di-apply ke pengadaan barang

**Audit Procedure**:
1. Cek surat KPP yang menjadi dasar
2. Konfirmasi ke Ditjen Pajak untuk klasifikasi
3. Hitung kekurangan PPN + sanksi administratif

**Recommendation Template**:
- Wajibkan konfirmasi tertulis Ditjen Pajak untuk transaksi >Rp10M
- Pelatihan klasifikasi PPN untuk bendahara

**Sumber Bukti**: [[adtt-ip-hub-bakti-2025]] (Rp80,04M)

---

## C. Anggaran & Perencanaan

### P-15 | Revisi Anggaran Cascade (≥4 Iterasi per TA) 🔴

**Pola**: Satu Ditjen mengalami ≥4 iterasi revisi anggaran dalam satu TA (Renja → realokasi → restrukturisasi → cut-off → relaksasi). Indikator perencanaan awal **tidak matang**.

**Trigger Indicators**:
- ≥3 LHR revisi anggaran untuk satu Ditjen dalam TA
- Pagu DIPA berubah ≥10% dari pagu awal
- RO baru muncul mid-year

**Audit Procedure**:
1. Timeline revisi: tanggal Renja → setiap revisi
2. Cek triger setiap revisi (SOTK? force majeure? underestimate?)
3. Hitung *revision velocity* per unit

**Recommendation Template**:
- Lock Renja/RKA-K/L pasca-Maret; revisi hanya untuk force majeure
- Wajibkan analisis akar penyebab setiap revisi

**Sumber Bukti**: [[lhr-revisi-renja-ekosistem-digital-2025]], [[lhr-perubahan-renja-ekdig-2025]], [[lhr-restrukturisasi-ekdig-2025]], [[lhr-restrukturisasi-ekdig-juni-2025]], [[lhr-revisi-relaksasi-anggaran-ekdig-2025]] (EkDig 4 iterasi); [[lhr-relaksasi-anggaran-wasdig-2025]], [[lhr-revisi-anggaran-wasdig-oktober-2025]], [[chr-tambahan-anggaran-wasdig-2025]] (Wasdig 5+ iterasi)

---

### P-16 | Relaksasi/Tambahan Anggaran Flash-Cash Q3-Q4 🟡

**Pola**: Tiga gelombang relaksasi: April (buka blokir), Juli (antar-UKE1), Oktober (Setjen+KPM + PNBP). Pola flash-cash menjelang akhir TA mengindikasikan perencanaan awal underestimate.

**Trigger Indicators**:
- Relaksasi nominal besar (≥Rp100M) di Q3-Q4
- Sumber dana dari unit lain (cross-UKE1)
- Tidak ada *cash-flow projection* yang justifikasi kebutuhan

**Audit Procedure**:
1. Cek *cash-flow projection* awal TA vs realisasi
2. Audit alasan blokir (apakah valid?)
3. Cek output realisasi pasca-relaksasi (apakah tepat sasaran?)

**Recommendation Template**:
- Wajibkan *cash-flow projection* di KAK
- Audit *output realization rate* pasca-relaksasi

**Sumber Bukti**: [[lhr-relaksasi-anggaran-wasdig-2025]] (Rp100,81M), [[lhr-revisi-relaksasi-anggaran-ekdig-2025]] (Rp233,74M), [[lhr-relaksasi-pnbp-wasdig-oktober-2025]] (Rp217,01M), [[lhr-revisi-anggaran-wasdig-oktober-2025]] (Rp41,63M)

---

### P-17 | Penamaan RO Tidak Sesuai Substansi Anggaran 🟡

**Pola**: RO "Layanan Perencanaan" Wasdig naik 61× lipat dari Rp692jt → Rp42,3M tetapi substansinya OM TKPPSE (sewa Colocation). Audit trail menjadi kurang transparan.

**Trigger Indicators**:
- RO meningkat ekstrem (>10×) tanpa perubahan ruang lingkup
- Nomenklatur RO tidak match dengan komponen belanja terbesar
- Ada *renaming* RO mid-year

**Audit Procedure**:
1. Bandingkan nomenklatur RO dengan top-3 komponen belanja
2. Audit perubahan nomenklatur (apakah ada justifikasi?)
3. Reklasifikasi RO jika substansi tidak match

**Recommendation Template**:
- RO name harus match substansi anggaran (audit trail transparansi)
- Wajibkan persetujuan APIP untuk rename RO mid-year

**Sumber Bukti**: [[lhr-revisi-anggaran-wasdig-oktober-2025]], [[lhr-revisi-anggaran-dbs-ekdig-2025]]

---

### P-18 | Pagu vs Kebutuhan Bare Minimum Gap Signifikan (>50%) 🔴

**Pola**: RKA-K/L Wasdig TA 2026 pagu Rp134,82M vs kebutuhan bare minimum Rp542M = gap **Rp407M (75%)**. Risiko operasional inti (TKPPSE, Penyidikan, PSrE, moderasi konten) berhenti.

**Trigger Indicators**:
- TOR mencantumkan *bare minimum requirement*
- Pagu disetujui jauh di bawah TOR
- Surat usulan tambahan/relaksasi sudah masuk pra-TA

**Audit Procedure**:
1. Cek *bare minimum requirement* di TOR
2. Identifikasi layanan kritis yang berisiko jika tidak dipenuhi
3. Hitung *fiscal gap* dan rekomendasi mitigasi

**Recommendation Template**:
- Eskalasi ke pimpinan + DJA jika gap >30%
- Strategi *de-scoping* layanan non-kritis

**Sumber Bukti**: [[chr-rka-kl-wasdig-2026]] (gap Rp407M)

---

### P-19 | SIRUP Pagu Draft Tinggi (>50%) Menjelang Akhir TW I 🟡

**Pola**: 68,36% pagu masih berstatus *draft* di SIRUP per 27 Januari 2026 (Rp236,7M Wasdig). 3 paket risiko tinggi Rp95M (TKPPSE Rp76M, CSE Rp6,9M, ISP Rp12M).

**Trigger Indicators**:
- Persentase draft di SIRUP >50% di akhir TW I
- Paket pengadaan tinggi belum finalisasi
- Tidak ada milestone tracking di Tim Perencanaan

**Audit Procedure**:
1. Reviu RKA-K/L vs SIRUP — konsistensi
2. Cek paket risiko tinggi yang masih draft
3. Identifikasi *crunch time* risiko mundur ke TW III/IV

**Recommendation Template**:
- *Early flag* TW I untuk paket draft >50%
- Sinkronisasi SIRUP dengan RKA-K/L wajib di TW I

**Sumber Bukti**: [[lhp-pengadaan-program-prioritas-wasdig-2026]]

---

## D. Aset BMN

### P-20 | Aset BMN Tertahan Alih Status Antar-Entitas (Likuidasi/SOTK) 🔴

**Pola**: Sarpras DBS Ditjen PPI Rp93,49M + KDP Rp1,40M = Rp94,89M tertahan alih status ke LPP TVRI selama 3 periode laporan berturut-turut (2024 LK, 2025 Sem 1, 2025 TW 3). Neraca overstated.

**Trigger Indicators**:
- Aset bertahan di entitas lama setelah SOTK >6 bulan
- BA serah terima tidak ditandatangani
- KDP masih tercatat di entitas lama padahal output sudah beralih

**Audit Procedure**:
1. Identifikasi semua aset terdampak SOTK
2. Cek dasar hukum alih status (SK Menteri, BAPL)
3. Hitung *carrying cost* aset tertahan

**Recommendation Template**:
- Deadline tegas alih status (mis. 31 Des TA SOTK)
- Provisi penurunan nilai jika tidak dialih dalam 12 bulan

**Sumber Bukti**: [[lhr-lk-ppi-2024]] (Rp93,22M), [[lhr-lk-ppi-sem1-2025]] (Rp96,29M), [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]] (Rp94,89M)

---

### P-21 | Aset BMN Idle Risk (Investasi Besar Tanpa Sustainability Plan) 🔴

**Pola**: Aset BMN TKPPSE senilai **Rp1.591 miliar** terancam idle jika TKPPSE dihentikan. IP Hub SATRIA-1 potensi pemborosan Rp216,86M.

**Trigger Indicators**:
- Aset infrastruktur kritis dengan masa hidup ≥5 tahun
- Tidak ada rencana sustainability/redesain
- Teknologi outdated (mis. Oracle Linux 7 EOL)

**Audit Procedure**:
1. Pemetaan aset BMN dengan nilai >Rp100M
2. Cek rencana sustainability/redesain
3. Identifikasi *exit strategy* jika layanan dihentikan

**Recommendation Template**:
- Wajibkan *sustainability plan* untuk aset >Rp100M
- Penyusutan dipercepat jika tidak ada rencana lanjut

**Sumber Bukti**: [[notisi-tata-kelola-konten-negatif-2025]] (Rp1,59T TKPPSE), [[bpk-lhp-lk-kominfo-2023]] (IP Hub Rp216,86M), [[laporan-tata-kelola-konten-negatif-final-2025]]

---

### P-22 | Aset Kendaraan / SITAC Penatausahaan Tidak Sesuai 🟡

**Pola**: Saldo aset kendaraan Rp19,22 triliun (+30,31% vs 2023) dengan dokumen pendukung pemeliharaan tidak lengkap; SITAC BTS 4G 64 site Rp1,23M masih di Aset Lain-Lain.

**Trigger Indicators**:
- Kenaikan saldo aset ekstrem (>20% YoY) tanpa pengadaan jelas
- Pemeliharaan tidak ada BA
- KDP/SITAC bertahan >12 bulan tanpa closure

**Audit Procedure**:
1. Sampling fisik kendaraan vs DBR
2. Cek BA pemeliharaan vs setoran vendor
3. Closure KDP/SITAC sesuai SAP

**Recommendation Template**:
- Inventarisasi fisik tahunan dengan tagging digital
- Closure KDP/SITAC dengan deadline

**Sumber Bukti**: [[bpk-spi-lk-kominfo-2024-detail]] (Kendaraan Rp19,22T, SITAC Rp1,32M)

---

## E. Tata Kelola Pasca-SOTK

### P-23 | Pedoman/SOP Usang (Nomenklatur Pra-SOTK, Regulasi Pengganti Belum) 🔴

**Pola**: Pedoman MR masih **Permenkominfo 6/2017**; Pedoman AKIP **Permenkominfo 13/2015** belum diupdate ke Permenkomdigi 1/2025; SOP Wasdig nomenklatur Kominfo lama; Renstra Kemkomdigi 2025-2029 belum ditetapkan saat TW 1 2026.

**Trigger Indicators**:
- Pedoman terakhir direvisi >3 tahun lalu
- Pedoman merujuk SOTK/regulasi yang sudah dicabut
- "Akan direvisi" tanpa jadwal konkret

**Audit Procedure**:
1. Inventarisasi pedoman + tanggal revisi terakhir
2. Cross-check dengan regulasi pengganti
3. Jadwal revisi konkret (≤6 bulan)

**Recommendation Template**:
- *Policy refresh audit* per 3 tahun reguler
- Revisi pedoman dengan jadwal jelas (bukan "akan direvisi")

**Sumber Bukti**: [[lhe-manajemen-risiko-2026]] (PM 6/2017), [[lhr-lkj-wasdig-2025]] (SOP usang), [[laporan-sementara-spip-kemkomdigi-2025]] (Renstra belum), [[lhe-akip-internal-itjen-2023-2025]] (PM 13/2015), [[bpk-kinerja-konten-rencana-aksi-2025]] (regulasi konten belum lengkap)

---

### P-24 | Warisan Aptaka — Ownership Rekomendasi/Aset Fragmen Pasca-Likuidasi 🔴

**Pola**: Aptaka dilikuidasi 2024 → 5 UKE1 baru (DJID, DJTPD, DJED, DJKPM, DJPRD). Rekomendasi warisan (**JAR Rp27,6M + HUB.ID Rp2,66M**) ownership fragmen — PPK era Aptaka pindah unit, tidak ada PIC baru.

**Trigger Indicators**:
- Rekomendasi >2 tahun belum ditangani
- PPK lama tidak lagi di unit
- Tidak ada SK PIC baru

**Audit Procedure**:
1. Mapping ownership baru rekomendasi Aptaka → unit penerus
2. Identifikasi PIC + deadline konkret
3. Penetapan SK definitif

**Recommendation Template**:
- SK definitif PIC untuk setiap rekomendasi warisan
- Eskalasi ke Irjen jika tidak ada PIC dalam 3 bulan pasca-SOTK

**Sumber Bukti**: [[tlhp-internal-simwas-ir2]] (Rp30,27M outstanding), [[pemantauan-tlhp-ekdig-2025]] (HUB.ID + JAR), [[atensi-progres-spip-mr-2025]], [[pemantauan-tlhp-wasdig-november-2025]]

---

## F. Sistem Informasi & Infrastruktur TI

### P-28 | Sistem TI Belum Early Warning (Repositori, Bukan Decision Support) 🟡

**Pola**: SIMR Kemkomdigi tidak punya fitur *early warning*, belum terintegrasi; Aplikasi SPIP Kemkomdigi bermasalah teknis (7/13 KK kosong); Ev-SAKIP belum tuntas ke UPT.

**Trigger Indicators**:
- Aplikasi hanya untuk upload dokumen (tidak ada trigger/alert)
- Tidak ada integrasi antar modul
- 0% pengisian KK Lead II selama TW

**Audit Procedure**:
1. Test functional: apakah aplikasi memicu tindakan?
2. Cek interoperabilitas (API)
3. Audit *user adoption rate*

**Recommendation Template**:
- Audit IT fokus *fungsionalitas* (bukan ketersediaan)
- Wajibkan *trigger logic* untuk semua aplikasi governance

**Sumber Bukti**: [[lhe-manajemen-risiko-2026]] (SIMR), [[atensi-progres-spip-mr-2025]] (SPIP), [[lhe-akip-internal-itjen-2023-2025]] (Ev-SAKIP)

---

### P-29 | Sistem TI Outdated / Topologi Bypass-able (HTTPS, DoH, VPN) 🔴

**Pola**: TKPPSE menggunakan teknik TCP Reset yang dapat di-bypass oleh browser modern (Chrome/Edge/Firefox), DoH dengan public DNS, VPN enkripsi. **Uji laboratorium BPK: 0/40 akses berhasil murni TKPPSE**. Efektivitas hanya **22,44%** vs RPZ 79,60% & RTBH 81,45%.

**Trigger Indicators**:
- Teknologi >5 tahun tanpa upgrade (Oracle Linux 7 EOL 31 Des 2024)
- Hasil uji lab/sample menunjukkan bypass tinggi
- Tidak ada peer-review teknologi alternatif

**Audit Procedure**:
1. Uji lab sample (mis. 40 URL random) → success rate
2. Benchmark teknologi sejenis di K/L lain
3. Cek *roadmap upgrade* dengan milestone

**Recommendation Template**:
- *Sunset policy* untuk teknologi dengan efektivitas <50%
- Roadmap upgrade dengan kajian → eksekusi (lihat P-31)

**Sumber Bukti**: [[bpk-laporan-hasil-pemeriksaan]] (22,44%), [[bpk-kinerja-pste-2024]], [[laporan-pendampingan-konten-digital-final-2025]] (Oracle Linux 7 EOL), [[notisi-tata-kelola-konten-negatif-2025]]

---

### P-30 | Layanan Baru Diluncurkan dengan Kelemahan Tata Kelola & Keamanan 🟡

**Pola**: Sistem/layanan baru di-launch dengan kelemahan tata kelola di hulu (klasifikasi/verifikasi) dan kelemahan keamanan di hilir (API terbuka, data sensitif). Contoh: IGRS — inkonsistensi rating, RC tidak transparan, kebocoran data developer.

**Trigger Indicators**:
- Layanan launch tanpa *acceptance testing* publik
- API tidak ada *rate limiting* atau *auth*
- Data sensitif terekspos di response

**Audit Procedure**:
1. Framework **5 area sasaran IGRS** ([[sasaran-audit-igrs]]):
   - Kesiapan sistem
   - Akurasi klasifikasi
   - Mekanisme RC
   - Keamanan
   - Tata kelola kemitraan
2. Reusable untuk audit layanan baru K/L lain

**Recommendation Template**:
- Wajibkan UAT publik untuk layanan baru
- Pre-launch *security pen-test*

**Sumber Bukti**: [[isu-igrs]], [[audit-kinerja-layanan-klasifikasi-gim]], [[nota-dinas-764-permohonan-audit-igrs]], [[nodin-705-permohonan-audit-sistem-igrs-pdsi]]

---

### P-31 | Kajian Teknis Tanpa Implementasi (Dokumen Mati) 🟡

**Pola**: Kajian/redesain disusun tetapi tidak tertuang rencana aksi konkret → eksekusi tertunda ke TA berikutnya. Contoh: Redesain TKPPSE kajian baru TW II 2026, eksekusi TA 2027.

**Trigger Indicators**:
- Dokumen kajian ada, tetapi tidak ada *implementation plan*
- "Akan dilanjutkan TA berikutnya" tanpa milestone
- Kajian dilakukan oleh konsultan tanpa SK Tim Implementasi

**Audit Procedure**:
1. Cross-check kajian → rencana aksi → milestone
2. Identifikasi *implementation gap*
3. Wawancara PIC implementasi

**Recommendation Template**:
- Rekomendasi setingkat *rencana aksi dengan milestone* (bukan "dilakukan kajian")
- SK Tim Implementasi wajib di-issue bersamaan dengan kajian

**Sumber Bukti**: [[lhp-pengadaan-redesain-tkppse-2026]], [[laporan-pendampingan-konten-digital-final-2025]] (Kajian selesai 25 Okt 2025, eksekusi TBA)

---

### P-32 | Insiden Siber Tanpa Adjustment Kontrak/Pembayaran 🔴

**Pola**: PDNS mengalami ransomware **Brain Cipher** 20 Juni 2024 → downtime 6 bulan, namun pembayaran tetap Rp2,20M tanpa adjustment SLA. Insiden tidak memicu *contract review*.

**Trigger Indicators**:
- Insiden besar (downtime >24 jam) tetapi pembayaran continue
- Tidak ada *force majeure* clause yang trigger
- Recovery data tidak terdokumentasi

**Audit Procedure**:
1. Verifikasi *incident response* + *recovery log*
2. Cek klausul SLA adjustment di kontrak
3. Hitung kelebihan pembayaran selama incident

**Recommendation Template**:
- Klausul *SLA adjustment* untuk insiden siber wajib eksplisit
- Wajibkan *incident postmortem* untuk semua insiden besar

**Sumber Bukti**: [[bpk-temuan-pdns-satria-2024]] (Rp2,20M), [[bpk-spi-lk-kominfo-2024]]

---

### P-40 | Tumpang Tindih Infrastruktur Operasional 🔴

**Pola**: TKPPSE vs RTBH vs TrustNG vs RPZ — duplikasi fungsi pemblokiran konten. CNS (TKPPSE) OM Rp233,74M vs CSE-Rugos Rp5,11M = inefisiensi anggaran. RTBH+TrustNG sudah 935 titik (100% ISP).

**Trigger Indicators**:
- Multiple sistem dengan fungsi overlap
- Tidak ada *system inventory* terpusat
- Anggaran masing besar tanpa pemetaan komparatif

**Audit Procedure**:
1. Pemetaan sistem dengan fungsi sejenis
2. Cost-effectiveness per sistem
3. Rekomendasi *sunset* untuk yang dominan terbypass

**Recommendation Template**:
- System inventory tahunan dengan komparasi efektivitas/biaya
- Konsolidasi sistem tumpang tindih

**Sumber Bukti**: [[notisi-tata-kelola-konten-negatif-2025]]

---

## G. SPI / MR / AKIP / RB / ZI

### P-33 | SPIP / MR / RB Maturitas Stagnan 🔴

**Pola**: Maturitas SPIP Kemkomdigi **3,801 "Terdefinisi"** (turun dari PM 4,115); Wasdig **3,191** (terendah); EkDig **4,238** (tertinggi). Gap vs target Level 4 "Terkelola". Improvement marginal: 59,25% (2024) → 60,00% (2025), +0,75pp.

**Trigger Indicators**:
- Skor maturitas turun antara penilaian mandiri vs penjaminan
- 10 AoI dominan terkait MR strategis
- Register risiko strategis belum ada

**Audit Procedure**:
1. Cross-check skor PM vs Quality Assurance (gap = optimism bias)
2. Reviu register risiko strategis
3. Sampling implementasi rencana tindak pengendalian

**Recommendation Template**:
- Roadmap SPIP 2026 dengan milestone per AoI
- Training SPIP merata ke pegawai

**Sumber Bukti**: [[laporan-penjaminan-kualitas-spip-kemkomdigi-final-2025]] (3,801), [[penjaminan-kualitas-spip-wasdig-final-2025]] (3,191), [[penjaminan-kualitas-spip-itjen-2025]] (3,356), [[penjaminan-kualitas-spip-ekdig-final-2025]] (4,238), [[lke-rb-kemkomdigi-2024-2025]] (+0,75pp), [[lhe-manajemen-risiko-2026]]

---

### P-34 | Zona Integritas Flat 2 Tahun (16,67%) 🔴

**Pola**: Pembangunan ZI stuck di 16,67% selama 2 tahun berturut-turut (1 dari 6 unit berhasil). Bottleneck struktural: komitmen pimpinan belum penuh, mekanisme reward/punishment belum efektif.

**Trigger Indicators**:
- ZI flat lintas TA
- Tidak ada SK Tim Penilai Internal aktif
- Surveillance ZI tidak diregenerasi tahunan

**Audit Procedure**:
1. Cek SK Tim Penilai Internal (TPI) aktif
2. Reviu *survey integritas* pasca-pencanangan
3. Audit *acceleration plan*

**Recommendation Template**:
- Akselerasi via SK TPI baru + mekanisme insentif
- ND-130 Tim Penilai Internal ZI 2026 sebagai *circuit breaker*

**Sumber Bukti**: [[lke-rb-kemkomdigi-2024-2025]] (16,67%), [[penilaian-internal-zi-2026]]

---

### P-35 | LKj / IKU Data Tidak Traceable Sumbernya 🟡

**Pola**: LKj Kemkomdigi 2025 — data pendukung tidak dapat diverifikasi sumbernya; belum ada analisis efisiensi SDM. LKj Wasdig — SOP gunakan nomenklatur lama, belum ada Renstra baru, belum ada benchmark.

**Trigger Indicators**:
- Indikator capaian tinggi tetapi sumber data "olahan internal"
- Tidak ada lampiran/sitasi
- Tidak ada *baseline analysis*

**Audit Procedure**:
1. Wajibkan *source of truth* untuk setiap indikator (aplikasi, spreadsheet, BA)
2. Sampling *traceability* 10% indikator
3. Flag indikator tanpa referensi

**Recommendation Template**:
- Reviu LKj dengan uji *traceability* sumber data
- Wajibkan dokumen sumber data dilampirkan di LKj

**Sumber Bukti**: [[lhr-lkj-kemkomdigi-2025]], [[lhr-lkj-wasdig-2025]], [[lhe-akip-internal-itjen-2023-2025]], [[lhr-lkj-itjen-2024]]

---

### P-38 | Realisasi Belanja Sangat Rendah (<20%) di Q3 — Lag Pasca-Restrukturisasi 🟡

**Pola**: Realisasi belanja EkDig TW III 2025 hanya **9,88%** (Rp47,25M dari Rp478,2M); Wasdig **7,05%** (Rp14,05M dari Rp199,2M); LPU **0%** Sem 1 2025 (Rp385,2M pagu).

**Trigger Indicators**:
- Realisasi <20% di Q3
- Penjelasan: "PKS belum ada" / "transisi SOTK"
- Tidak ada *catch-up plan* Q4

**Audit Procedure**:
1. Cek *catch-up plan* Q4
2. Identifikasi *root cause* penundaan (PKS? regulasi? procurement?)
3. Hitung *carry-over risk*

**Recommendation Template**:
- Mandatory *catch-up plan* jika realisasi <30% di Q3
- Eskalasi ke Irjen jika realisasi <20% di Q3

**Sumber Bukti**: [[lhr-lk-bun-lpu-2025-sem1]] (Rp0), [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]] (EkDig 9,88%, Wasdig 7,05%)

---

## H. TLHP / Pengawasan Internal

### P-25 | TLHP Outstanding Struktural (>2 Tahun, Butuh Regulasi/MoU) 🔴

**Pola**: Rekomendasi BPK sulit (TL ≥7×): arsitektur TKPPSE, regulasi+MoU lintas K/L, sanksi ISP/MUX/PSE, pertanggungjawaban JAR/SPBE, sistem deteksi crawling CSE. Outstanding finansial **Rp200,89M** (BPK Eksternal SIMWAS).

**Trigger Indicators**:
- TL ≥7× untuk satu rekomendasi
- Status "Belum Sesuai" >2 tahun
- Rekomendasi bersifat struktural (butuh MoU/regulasi)

**Audit Procedure**:
1. Identifikasi rekomendasi yang TL ≥7×
2. Klasifikasi: solvable internal vs butuh MoU/regulasi
3. Eskalasi ke level Menteri untuk yang struktural

**Recommendation Template**:
- *Escalation matrix* by complexity (internal/lintas-K-L)
- Konsolidasi rekomendasi sejenis untuk koordinasi terpadu

**Sumber Bukti**: [[tlhp-eksternal-simwas-ir2]] (Rp200,89M, 38 BS), [[tlrhp-bpk-semester-2-2025]] (71 rek belum), [[bpk-kinerja-konten-rencana-aksi-2025]] (15 SS / 19 BS), [[pemantauan-tlhp-wasdig-november-2025]] (17,07%)

---

### P-26 | Asymmetric TL Eksternal vs Internal antar-Ditjen 🟡

**Pola**: Wasdig Nov 2025: **17,07%** TLHP eksternal sesuai (7/41 rek) vs EkDig **83,33%** (15/18 rek). Asimetri ekstrem mengindikasikan kompleksitas rekomendasi struktural Wasdig.

**Trigger Indicators**:
- Gap pencapaian TL >50 pp antar-Ditjen sejenis
- Rekomendasi Wasdig: 34/35 belum = BPK TKPPSE struktural
- Rekomendasi EkDig: operasional, cepat selesai

**Audit Procedure**:
1. Klasifikasi rekomendasi: operasional vs struktural
2. Resource alocation per kompleksitas
3. Akselerasi MoU lintas K/L untuk yang struktural

**Recommendation Template**:
- Resource khusus untuk rekomendasi struktural
- MoU prioritas: BSSN, LKPP, APJII, OJK, Polri, PPATK

**Sumber Bukti**: [[pemantauan-tlhp-wasdig-november-2025]] (17,07%), [[pemantauan-tlhp-ekdig-november-2025]] (83,33%)

---

### P-27 | JAR (Jaminan Pengambil Alih) Verifikasi Tidak Tuntas 🔴

**Pola**: JAR TA 2022–2024 senilai **Rp171,59M** belum sepenuhnya diverifikasi; Itjen belum selesai reviu untuk 3 site Rp3,15M; rekomendasi TL belum diselesaikan Aptika (penerus: Ditjen Infrastruktur Digital).

**Trigger Indicators**:
- BPK minta verifikasi total tetapi reviu Itjen incomplete
- 3 site terlewat tanpa justifikasi
- Rekomendasi TL berlangsung >20 bulan

**Audit Procedure**:
1. Cek scope reviu Itjen vs scope mandat BPK
2. Verifikasi 3 site outstanding
3. Hand-off ke Ditjen Infrastruktur Digital sebagai penerus

**Recommendation Template**:
- Reviu lengkap mandat BPK (no gap)
- SK PIC definitif di Ditjen Infrastruktur Digital

**Sumber Bukti**: [[tlhp-eksternal-simwas-ir2]] (Rp171,59M), [[tlrhp-bpk-semester-2-2025]]

---

## I. Layanan Publik & Operasional

### P-37 | Kontinuitas Layanan Publik Terancam Akibat Tunggakan Pembayaran 🔴

**Pola**: TKPPSE kapasitas turun 33% (27,55 Gbps dari 83,4 Gbps) akibat tunggakan OM yang tidak dibayar. PJT (XL, Indosat) rencana pemutusan akhir Mei 2025 → kapasitas tersisa hanya 34,21 Gbps (59% penurunan). Dampak: pemblokiran konten negatif terancam berhenti.

**Trigger Indicators**:
- PJT/vendor mengirim surat ancaman pemutusan
- Tunggakan >Rp50M tanpa rencana pembayaran konkret
- Kapasitas layanan menurun terdokumentasi

**Audit Procedure**:
1. Inventarisasi tunggakan dengan vendor kritis
2. Identifikasi *alternate path* layanan
3. Eskalasi ke Menteri jika kapasitas <70%

**Recommendation Template**:
- Cadangan anggaran *contingency* untuk vendor kritis
- *Alternate path* wajib untuk layanan publik kritis

**Sumber Bukti**: [[atensi-pemutusan-tkppse-2025]], [[lhr-lk-bun-lpu-2025-sem1]] (LPU Rp0)

---

## J. SDM & Personalia

### P-36 | Turnover Pimpinan Tinggi pada Periode Kritis 🟡

**Pola**: 4 dirjen/plt Aptika dalam 1 tahun (Mar–Des 2024) → kontinuitas governance putus pada periode tagihan OM TKPPSE; PPK Aries Kusdaryono jadi titik kontinuitas tunggal.

**Trigger Indicators**:
- ≥3 pejabat definitif/plt dalam 12 bulan di posisi sama
- PPK/KPA tidak dievaluasi pasca-rotasi
- Tidak ada *handover document* formal

**Audit Procedure**:
1. Cek SK pejabat + tanggal mulai/berakhir
2. Verifikasi *handover document* setiap rotasi
3. Identifikasi *single point of failure*

**Recommendation Template**:
- Wajib *handover document* formal di setiap rotasi
- Cadangan PPK/KPA untuk periode kritis

**Sumber Bukti**: [[dha-tahap2-om-tkppse-2024]] (4 dirjen 1 tahun)

---

## K. Regulasi & Koordinasi Lintas K/L

### P-39 | MoU Lintas K/L Belum Ada untuk Isu yang Membutuhkan Koordinasi 🔴

**Pola**: Pemutusan konten ilegal butuh koordinasi **BSSN, LKPP, APJII, OJK, Polri, PPATK** — MoU belum ditandatangani. Regulasi PDP belum integratif (PP 71/2019 + Perpres 95/2018). 798 dari 1.188 ISP belum patuh; SE Menteri reward/punishment belum diterbitkan.

**Trigger Indicators**:
- Rekomendasi BPK butuh K/L eksternal
- Daftar MoU dengan K/L kosong/usang
- Regulasi pengganti tidak komprehensif

**Audit Procedure**:
1. Inventarisasi MoU yang dibutuhkan
2. Mapping wewenang per K/L
3. Prioritas MoU berdasar dampak temuan

**Recommendation Template**:
- Roadmap MoU dengan deadline per K/L
- Eskalasi ke Menteri untuk MoU strategis

**Sumber Bukti**: [[bpk-kinerja-pste-2024]], [[bpk-kinerja-konten-rencana-aksi-2025]], [[tlhp-eksternal-simwas-ir2]] (keamanan siber BSSN 2 BS), [[notisi-tata-kelola-konten-negatif-2025]], [[pemantauan-tlhp-wasdig-november-2025]]

---

## Cross-Domain Mega-Patterns

Pattern individual di atas mengelompok menjadi **5 mega-pattern** lintas-kategori — yang menjadi *root cause* tematik bagi sebagian besar temuan:

### M1 — SOTK Transition Fallout

Mempengaruhi: P-01, P-15, P-20, P-23, P-24, P-38. Kunci penyebab:
- DIPA terlambat → kontrak retroaktif (P-01)
- Pedoman/SOP usang (P-23)
- Aset/rekomendasi warisan ownership fragmen (P-20, P-24)
- Renstra Kemkomdigi 2025-2029 belum ditetapkan
- Realisasi belanja sangat rendah di Q3 (P-38)
- Revisi anggaran cascade (P-15)

**Mitigasi sistemik**: *SOTK transition playbook* mandatory + deadline stabilisasi 6 bulan.

### M2 — TKPPSE Sistemik

Mempengaruhi: P-01, P-02, P-03, P-04, P-07, P-21, P-25, P-27, P-29, P-37, P-40. Kunci penyebab:
- Vendor lock-in PT SUFI (P-03)
- Teknologi outdated (Oracle Linux 7 EOL) (P-29)
- Tumpang tindih dengan RTBH/TrustNG/RPZ (P-40)
- Aset BMN Rp1,59T idle risk (P-21)
- Outstanding finansial Rp57M + Rp16,56M verifikasi (P-07, P-27)
- Kontinuitas layanan terancam (P-37)

**Mitigasi sistemik**: Redesain TKPPSE TA 2027 + tunda pengadaan baru sampai kajian implementasi.

### M3 — PNBP Governance Gap

Mempengaruhi: P-10, P-11, P-12, P-13, P-14. Kunci penyebab:
- Tafsir regulasi BHP Telekomunikasi belum baku (P-10)
- SOP pengembalian PNBP belum substantif (P-11)
- Virtual account wajib belum di-implementasi (P-12)
- Piutang macet KPBU multi-tahun (P-13)
- Klasifikasi PPN salah (P-14)

**Mitigasi sistemik**: Pedoman tafsir spesifik komponen kontroversial + sosialisasi PM Kominfo 5/2021.

### M4 — Sistem TI Belum Dewasa

Mempengaruhi: P-21, P-28, P-29, P-30, P-31, P-40. Kunci penyebab:
- Sistem belum *early warning* (P-28)
- Teknologi outdated dapat di-bypass (P-29)
- Kajian tanpa implementasi (P-31)
- Layanan baru tanpa UAT (P-30)
- Aset idle risk (P-21)
- Tumpang tindih sistem (P-40)

**Mitigasi sistemik**: Roadmap TERRA (lihat [[renstra-itjen-2025-2029]] Gambar 3.2) + *sunset policy* sistem outdated.

### M5 — Governance Maturity Stagnasi

Mempengaruhi: P-23, P-33, P-34, P-35, P-39. Kunci penyebab:
- Pedoman usang (P-23)
- SPIP/MR/RB maturitas stagnan (P-33)
- Zona Integritas flat 2 tahun (P-34)
- LKj data tidak traceable (P-35)
- MoU lintas K/L belum ada (P-39)

**Mitigasi sistemik**: Roadmap governance 2026-2029 + akselerasi MoU strategis.

---

## Severity & Frequency Matrix

| Severity / Frekuensi | 🔴 Tinggi (≥3 satker × 2 TA) | 🟡 Sedang (≥3 dokumen) | 🟢 Rendah (insidental) |
|----------------------|-------------------------------|-------------------------|------------------------|
| **Frekuensi Sangat Tinggi (≥5)** | P-01, P-02, P-03, P-23, P-24, P-25, P-29, P-33, P-39 | P-04, P-09, P-15, P-28 | – |
| **Frekuensi Tinggi (3–4)** | P-07, P-13, P-20, P-21, P-26, P-32, P-37 | P-06, P-10, P-16, P-22, P-31, P-35, P-38 | – |
| **Frekuensi Sedang (2)** | P-27, P-34, P-40 | P-05, P-08, P-11, P-17, P-30, P-36 | P-12 |
| **Frekuensi Rendah (1)** | P-18 | P-14, P-19 | – |

**13 pattern 🔴 Tinggi** menjadi *core risk universe* IR II. **24 pattern 🟡/🟢** sebagai *secondary risk*.

---

## Trigger Indicators — Early Warning Auditor

Konsolidasi sinyal awal yang harus diperhatikan auditor saat dokumen masuk untuk reviu:

### Sinyal Dokumen Anggaran (Renja/RKA-K/L/Revisi)

| Sinyal | Pattern |
|--------|---------|
| ≥3 LHR revisi anggaran untuk satu Ditjen dalam TA | P-15 |
| Relaksasi ≥Rp100M di Q3-Q4 | P-16 |
| RO meningkat >10× tanpa perubahan ruang lingkup | P-17 |
| Pagu disetujui jauh di bawah TOR bare-minimum | P-18 |
| SIRUP draft >50% di akhir TW I | P-19 |
| Belanja >SBK >20% tanpa justifikasi | P-06 |

### Sinyal Dokumen Kontrak/PBJ

| Sinyal | Pattern |
|--------|---------|
| Tagihan masuk tanpa nomor kontrak referensi | P-01 |
| Surat Perintah Kelanjutan tanpa dasar kontrak | P-01, P-03 |
| Adendum >1 pada tanggal sama | P-05 |
| SLA reported >95% padahal lokasi tertentu mati >30 hari | P-02 |
| Invoice agregat tanpa breakdown per item/lokasi | P-09 |
| Belanja "Jasa" tetapi output aset fisik | P-08 |
| Insiden siber tanpa adjustment SLA/pembayaran | P-32 |

### Sinyal Dokumen LK/SPI

| Sinyal | Pattern |
|--------|---------|
| Aset sub-judul "Aset Lain-Lain" bertambah | P-22 |
| Sarpras/KDP tertahan alih status >6 bulan | P-20 |
| Setoran "Tn/Ny" tanpa nama di BKU | P-12 |
| Piutang macet >1 tahun tanpa eksekusi | P-13 |
| PPN tidak dipungut untuk pengadaan barang | P-14 |
| Skor maturitas PM > QA dengan gap >0,3 | P-33 |

### Sinyal Dokumen Kinerja (LKj/AKIP/RB)

| Sinyal | Pattern |
|--------|---------|
| Indikator tinggi sumber data "olahan internal" | P-35 |
| Pedoman terakhir direvisi >3 tahun | P-23 |
| Pedoman merujuk regulasi yang sudah dicabut | P-23 |
| ZI flat lintas TA tanpa akselerasi | P-34 |
| Realisasi belanja <20% di Q3 | P-38 |
| Aplikasi governance 0% pengisian KK | P-28 |

### Sinyal Dokumen TLHP

| Sinyal | Pattern |
|--------|---------|
| TL ≥7× untuk satu rekomendasi | P-25 |
| Gap pencapaian TL >50pp antar-Ditjen sejenis | P-26 |
| PPK era lama tidak lagi di unit | P-24 |
| Rekomendasi butuh MoU lintas K/L belum ada | P-39 |
| Outstanding finansial >Rp100M >2 tahun | P-27 |

---

## Rekomendasi Template per Kategori

### Kategori A — PBJ & Kontrak

1. **SOP Transisi Kontrak Lintas Ditjen** — wajibkan playbook setiap SOTK
2. **Klausul Audit Trail Eksplisit** — auditor/Itjen berhak akses log/metadata
3. **Template Invoice Standar** — wajib breakdown per item/lokasi + SLA achieved + kurs
4. **Liquidated Damages Otomatis** — klausul SLA breach harus terhitung otomatis
5. **3 Syarat LKPP 22441 Sebelum Pembayaran Retroaktif** — analisis urgensi + reviu APIP + audit BPKP

### Kategori B — PNBP

1. **Pedoman Tafsir Komponen Kontroversial** — SIP Trunk, SMS, AP wajib BHP
2. **Virtual Account Wajib** — semua perizinan PNBP
3. **SOP Penelitian Pengembalian PNBP** — wajib analisis penyebab
4. **CKP Update Tahunan** — sesuai expected loss piutang macet

### Kategori C — Anggaran

1. **Lock Renja/RKA-K/L Pasca-Maret** — revisi hanya force majeure
2. **Cash-Flow Projection Wajib di KAK** — cegah flash-cash Q3-Q4
3. **RO Name Match Substansi** — audit trail transparansi
4. **Mandatory Catch-up Plan** jika realisasi <30% di Q3

### Kategori D — Aset BMN

1. **Deadline Alih Status Tegas** (31 Des TA SOTK) — provisi penurunan nilai jika lebih
2. **Sustainability Plan Wajib** untuk aset >Rp100M
3. **Closure KDP/SITAC dengan Deadline** — penyusutan dipercepat jika tidak closure

### Kategori E — Pasca-SOTK

1. **SOTK Transition Playbook** — mandatory untuk setiap transisi
2. **SK Definitif PIC Rekomendasi Warisan** — eskalasi Irjen jika tidak ada PIC <3 bulan
3. **Policy Refresh Audit per 3 Tahun** — pedoman/SOP

### Kategori F — Sistem TI

1. **Sunset Policy** untuk teknologi efektivitas <50%
2. **Trigger Logic Wajib** untuk semua aplikasi governance (tidak hanya repositori)
3. **Pre-launch Security Pen-test** untuk layanan baru
4. **Framework 5-area IGRS** sebagai reusable template

### Kategori G — Governance Internal

1. **Roadmap SPIP 2026** dengan milestone per AoI
2. **Source of Truth Wajib** untuk setiap indikator LKj
3. **SK TPI ZI Tahunan** — circuit breaker stagnasi
4. **Training MR Merata** ke pegawai

### Kategori H — TLHP

1. **Escalation Matrix by Complexity** — operasional vs struktural
2. **Resource Khusus** untuk rekomendasi struktural
3. **Scope Reviu = Mandat BPK** — no gap
4. **MoU Prioritas** untuk rekomendasi butuh lintas K/L

### Kategori I — Layanan Publik

1. **Anggaran Contingency** untuk vendor kritis
2. **Alternate Path Wajib** untuk layanan publik kritis
3. **Eskalasi ke Menteri** jika kapasitas <70%

### Kategori J — SDM

1. **Handover Document Formal** di setiap rotasi pejabat
2. **Cadangan PPK/KPA** untuk periode kritis

### Kategori K — Regulasi & Koordinasi

1. **Roadmap MoU** dengan deadline per K/L
2. **Eskalasi ke Menteri** untuk MoU strategis
3. **Sosialisasi PM Kominfo 5/2021** ke wajib bayar

---

## Penggunaan Katalog di Sistem Audit

### Untuk Auditor (Manual)

Saat menerima penugasan, identifikasi:
1. Jenis penugasan (Audit / Reviu / Evaluasi / Atensi)
2. Auditi (Ditjen mitra)
3. Tema (PBJ / Anggaran / LK / Kinerja / dll.)

Lalu **filter pattern relevan** dari katalog ini — gunakan sebagai *pre-audit checklist*. Cek minimal **trigger indicators** untuk semua pattern dengan severity 🔴.

### Untuk Audit AI (Otomatis)

Pattern punya kode P-XX yang machine-readable. Integrasi ke:
- **CACM**: trigger alert jika dokumen baru cocok pattern indikator
- **Trello**: card "Pattern Risk" auto-link ke pattern relevan
- **TERRA** (rencana 2026–2029, lihat [[renstra-itjen-2025-2029]]): query pattern via API saat menyusun KKP

### Untuk Tindak Lanjut

Pattern P-24 s.d. P-27 (TLHP-related) menyediakan *playbook* eskalasi untuk rekomendasi outstanding. Cross-link ke [[tlhp-internal-simwas-ir2]] dan [[tlhp-eksternal-simwas-ir2]].

### Untuk PKPT TA Berikutnya

Pattern severity 🔴 dengan frekuensi tinggi (P-01, P-02, P-03, P-23, P-24, P-25, P-29, P-33, P-39) **wajib** menjadi tema PKPT. Lihat [[pkpt-2026]] / [[pkpt-ir2-rev1-2026]] untuk operasionalisasi.

### Untuk Form II MR

Pattern severity 🔴 menjadi *input* untuk Form II Profil Risiko di [[piagam-mr-ir2-2026]]. Bandingkan 40 pattern di sini dengan 26 risiko Form II IR II — gap analysis perlu dilakukan.

---

## Statistik Katalog

- **Total pattern**: 40 (vs 9 di versi lama [[pola-temuan-berulang]])
- **Source dokumen**: 80+ ekstrak surat (LHP, LHR, LHE, LHA, CHR, DHA, KHA, BPK, Notisi, Atensi, ADTT, Nota Dinas, TLHP)
- **Total temuan dimining**: ~290 substantive findings
- **Distribusi severity**: 🔴 Tinggi 13 (33%) | 🟡 Sedang 24 (60%) | 🟢 Rendah 3 (7%)
- **Distribusi kategori dominan**:
  - PBJ & Kontrak (A): 9 pattern
  - Anggaran (C): 5 pattern
  - Tata Kelola Pasca-SOTK (E): 2 pattern (cross-cut ke 6 lainnya)
  - Sistem TI (F): 5 pattern
  - Governance Internal (G): 3 pattern
  - PNBP (B): 5 pattern
  - TLHP (H): 3 pattern
  - Aset BMN (D): 3 pattern

---

## Catatan Pemeliharaan

Katalog ini **bersifat hidup** — perlu update setiap:
1. Ada **ingest LHP/LHR/LHE baru** → cek apakah temuan fit pattern existing atau perlu pattern baru
2. **Tahunan** (Desember) — lint pattern: severity, frekuensi, status mitigasi
3. Saat **revisi MR Form II** — sinkronisasi pattern ↔ risiko
4. Saat **revisi PKPT** — pattern severity 🔴 wajib dipertimbangkan

Versi sebelumnya: [[pola-temuan-berulang]] (9 pattern, 2026-04-24) — sebagian besar telah diserap ke katalog ini dengan kode baru.

---

## Related pages

- [[index]] — daftar isi wiki
- [[pola-temuan-berulang]] — versi awal (9 pattern dari 11 LHP)
- [[dashboard]]
- [[inspektorat-ii]] — profil IR II
- [[piagam-mr-ir2-2026]] — Form II MR (26 risiko) untuk gap analysis
- [[piagam-mr-itjen-2026]] — Form II MR level Itjen (16 risiko)
- [[pkpt-2026]] / [[pkpt-ir2-rev1-2026]] — operasionalisasi pattern via PKPT
- [[renstra-itjen-2025-2029]] — strategi 3.2.1.d *fraud risk assessment* + TERRA roadmap
- [[manual-pk-itjen-2026]] — target IKSK terkait
- [[tlhp-internal-simwas-ir2]] — pemantauan TLHP internal
- [[tlhp-eksternal-simwas-ir2]] — pemantauan TLHP eksternal BPK
- [[tlrhp-bpk-semester-2-2025]] — status terkini TLHP BPK
- [[sop-ingest-lhp-ke-wiki]] — proses ingest dokumen
- [[peta-risiko-wasdig-2026]] / [[peta-risiko-ekosistem-digital-2026]] — peta risiko mitra
- [[isu-igrs]] / [[sasaran-audit-igrs]] — framework reusable layanan baru
- [[notisi-tata-kelola-konten-negatif-2025]] — TKPPSE inefisiensi
- [[lhe-manajemen-risiko-2026]] — pedoman MR usang
