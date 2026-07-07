"""Bangun fixture sintetis ber-cacat untuk harness live (eval/live_measure.py).

Tiap skenario = satu skill. Emit ke `eval/fixtures/<skill>/`:
  00-input/<file>            — stub sumber (agar read_context.input_files mendaftarnya)
  _INGESTED/<jenis>-<nn>.json — digest generik (skema digest_generic: ringkasan_teks,
                                kata_kunci, regulasi_terdeteksi, tanggal/nilai) — SUMBER FAKTA agen
  _PKP/sasaran-assignment.json — sasaran DISETUJUI_KT untuk AT
  context.md                — lengkap (tanpa placeholder → agen tak perlu get_team_members/DB)

Cacat DITANAM di ringkasan_teks digest agar terdeteksi agen; cocok dgn golden
`expected_key_issues`. Jalankan: `.venv/bin/python -m eval.fixtures.build_fixtures [--skill reviu-umum|all]`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FIX_DIR = Path(__file__).parent


def _digest(file_rel: str, jenis: str, ringkasan: str, *, kata_kunci=None,
            regulasi=None, tanggal=None, nilai=None, halaman=1) -> dict:
    return {
        "file": file_rel,
        "jenis": jenis,
        "halaman_total": halaman,
        "halaman_total_chars": len(ringkasan),
        "ringkasan_teks": ringkasan.strip(),
        "kata_kunci": kata_kunci or [],
        "regulasi_terdeteksi": regulasi or [],
        "tanggal_terdeteksi": tanggal or [],
        "nilai_rupiah_terdeteksi": nilai or [],
        "_digest_meta": {"engine": "synthetic-fixture", "version": "1.0"},
    }


def _write(skill: str, *, at_name: str, sasaran: list[dict], context_md: str,
           inputs: dict[str, str], digests: list[tuple[str, dict]]) -> Path:
    root = FIX_DIR / skill
    if root.exists():
        import shutil
        shutil.rmtree(root)
    (root / "00-input").mkdir(parents=True)
    (root / "_INGESTED").mkdir()
    (root / "_PKP").mkdir()
    for fname, stub in inputs.items():
        (root / "00-input" / fname).write_text(stub, encoding="utf-8")
    for jenis_nn, d in digests:
        (root / "_INGESTED" / f"{jenis_nn}.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "_PKP" / "sasaran-assignment.json").write_text(
        json.dumps({"skill": skill, "sasaran": sasaran}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (root / "context.md").write_text(context_md.strip() + "\n", encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# Skenario: reviu-umum (criteria-driven, keyakinan terbatas, Sebab anti-mengarang)
# Reviu rancangan SOP sebelum ditetapkan; kriteria = juknis format + template baku.
# Cacat: Q2 kelengkapan (lampiran wajib absen + kolom Mutu Baku hilang),
# Q3 konsistensi (jumlah langkah 12 vs 9 vs 10; nomor SOP-03 vs SOP-05),
# Q4 kepatuhan prosedur (reviu hukum & uji coba dilewati). Q1 = dekomposisi sasaran.
# ---------------------------------------------------------------------------
def scenario_reviu_umum() -> Path:
    at = "Sarah Auditor"
    kriteria = _digest(
        "00-input/kriteria-01-juknis-format-sop.pdf", "kriteria",
        """
JUKNIS PENYUSUNAN & TATA NASKAH SOP UNIT KERJA (kriteria yang diunggah auditor).
Butir 3.1 — Setiap SOP WAJIB memuat lampiran: (a) Bagan Alir (flowchart) proses, dan
(b) Formulir Kendali/checklist pelaksanaan. SOP tanpa kedua lampiran dinyatakan BELUM LENGKAP.
Butir 3.2 — Tabel prosedur WAJIB memuat kolom: No; Aktivitas; Pelaksana; dan "Mutu Baku"
(Kelengkapan/persyaratan, Waktu, Output). Kolom Mutu Baku tidak boleh dihilangkan.
Butir 4.1 — Tahapan penyusunan yang WAJIB dilalui dan didokumentasikan berurutan:
(1) penyusunan draf, (2) REVIU HUKUM oleh Biro Hukum, (3) UJI COBA terbatas, (4) penetapan.
Butir 4.2 — Nomor dan tanggal SOP pada cover harus KONSISTEN dengan SK penetapan dan
seluruh dokumen rujukan. Jumlah langkah yang disebut pada bagian mana pun harus sama.
        """,
        kata_kunci=["SOP", "juknis", "tata naskah", "mutu baku", "reviu hukum", "lampiran"],
        regulasi=["PermenPANRB 35/2012", "Perki Tata Naskah Dinas"],
    )
    objek1 = _digest(
        "00-input/objek-01-rancangan-sop-pdn.pdf", "objek",
        """
RANCANGAN SOP PENGELOLAAN LAYANAN PUSAT DATA NASIONAL (PDN) — Nomor cover: SOP-03/PDN/2026.
Bagian Pendahuluan (hal. 1) menyatakan: "Prosedur ini terdiri dari 12 (dua belas) langkah".
Namun Tabel Prosedur (hal. 2) hanya memuat 9 baris aktivitas (langkah 1 s.d. 9).
Tabel Prosedur berkolom: No | Aktivitas | Pelaksana. TIDAK ada kolom "Mutu Baku"
(Kelengkapan/Waktu/Output) sebagaimana disyaratkan template.
Dokumen TIDAK menyertakan Lampiran Bagan Alir maupun Formulir Kendali.
Riwayat penyusunan (hal. 3): "Draf disusun tim teknis, langsung diajukan untuk penetapan".
Tidak ada catatan/berita acara reviu Biro Hukum maupun uji coba terbatas.
        """,
        kata_kunci=["SOP-03/PDN/2026", "12 langkah", "tabel prosedur", "PDN"],
        tanggal=["2026-01-20"],
    )
    objek2 = _digest(
        "00-input/objek-02-draft-sk-penetapan.pdf", "objek",
        """
DRAF SURAT KEPUTUSAN PENETAPAN SOP PDN. Menetapkan "Standar Operasional Prosedur
Pengelolaan Layanan PDN yang terdiri dari 10 (sepuluh) langkah" — berlaku sejak 1 Februari 2026.
SK merujuk SOP dengan nomor "SOP-05/PDN/2026". (Catatan pembanding: cover rancangan SOP
tertulis SOP-03/PDN/2026 dan menyebut 12 langkah, sedangkan tabelnya memuat 9 langkah.)
        """,
        kata_kunci=["SK penetapan", "SOP-05/PDN/2026", "10 langkah"],
        tanggal=["2026-02-01"],
    )
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Memastikan kesesuaian rancangan SOP Pengelolaan Layanan PDN dengan "
                     "kriteria yang diunggah (juknis format/tata naskah + template baku) sebelum ditetapkan.",
        "assigned_to": [at],
        "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Uraikan sasaran generik menjadi checklist per-elemen dari kriteria (kelengkapan lampiran, kolom tabel, tahapan penyusunan, konsistensi penomoran/jumlah langkah).",
            "Nilai kesesuaian tiap elemen: terpenuhi / terpenuhi dengan catatan / tidak terpenuhi.",
            "Catat ketidaksesuaian sebagai catatan reviu (K/K/S/A, Sebab anti-mengarang).",
        ],
    }]
    context = """
# Konteks Penugasan — Reviu Umum

Identitas: Reviu atas Rancangan SOP Pengelolaan Layanan Pusat Data Nasional (PDN)
Jenis Pengawasan: Reviu (keyakinan terbatas)
Auditi: Unit Kerja Pengelola PDN, Kementerian Komunikasi dan Digital
Periode: TA 2026
Tahun Anggaran: 2026

Tujuan: Menelaah kesesuaian rancangan SOP dengan kriteria yang diunggah auditor
(juknis penyusunan/tata naskah + template baku) sebelum SOP ditetapkan.

Ruang Lingkup: Dokumen objek = Rancangan SOP PDN (SOP-03/PDN/2026) dan Draf SK Penetapan.
Kriteria = Juknis Penyusunan & Tata Naskah SOP + template baku. Reviu tidak menghitung
kerugian negara dan tidak melakukan investigasi mendalam atas penyebab.

Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Penugasan reviu pra-penetapan untuk memastikan rancangan SOP memenuhi
kelengkapan, format, tahapan penyusunan, dan konsistensi penomoran sebagaimana kriteria.
"""
    inputs = {
        "kriteria-01-juknis-format-sop.pdf": "[stub] Juknis Penyusunan & Tata Naskah SOP — lihat _INGESTED/kriteria-01.json",
        "objek-01-rancangan-sop-pdn.pdf": "[stub] Rancangan SOP PDN — lihat _INGESTED/objek-01.json",
        "objek-02-draft-sk-penetapan.pdf": "[stub] Draf SK Penetapan SOP — lihat _INGESTED/objek-02.json",
    }
    digests = [("kriteria-01", kriteria), ("objek-01", objek1), ("objek-02", objek2)]
    return _write("reviu-umum", at_name=at, sasaran=sasaran, context_md=context,
                  inputs=inputs, digests=digests)


# ---------------------------------------------------------------------------
# Skenario: audit-umum (AUDIT, keyakinan memadai, Sebab WAJIB/RCA, hitung kerugian negara)
# Audit kepatuhan/kewajaran pembayaran belanja jasa. Cacat: Q2 inkonsistensi SPM/SPP,
# Q3 prosedur verifikasi dilewati, Q4 uji per-elemen, Q5 kelebihan bayar > SBM (kerugian
# negara terhitung + Sebab RCA), Q1 dokumen pendukung tak lengkap.
# ---------------------------------------------------------------------------
def scenario_audit_umum() -> Path:
    at = "Sarah Auditor"
    kriteria = _digest(
        "00-input/kriteria-01-sop-sbm-pembayaran.pdf", "kriteria",
        """
KRITERIA YANG DIUNGGAH: (1) SOP Pembayaran Belanja Satker Nomor 05/SOP/2025, (2) Standar Biaya Masukan
(SBM) TA 2026 = PMK No. 32/PMK.02/2025 tentang Standar Biaya Masukan.
SOP Nomor 05/SOP/2025 butir 5 — Sebelum penerbitan SPM WAJIB verifikasi berjenjang: verifikator (staf) →
PPK menguji kebenaran tagihan → PPSPM menerbitkan SPM. Verifikator dan PPSPM TIDAK boleh orang yang sama.
SOP butir 6 — Pembayaran honorarium narasumber WAJIB dilampiri: undangan, daftar hadir asli, materi, bukti transfer.
SOP butir 7 — Nilai SPM WAJIB SAMA dengan nilai SPP hasil verifikasi; tidak boleh ada selisih tanpa dasar/revisi resmi.
PMK No. 32/PMK.02/2025 (SBM), Lampiran butir honorarium narasumber/pembahas: batas tertinggi eselon II setara
Rp 1.400.000/jam/orang; moderator Rp 1.000.000/kegiatan.
        """,
        kata_kunci=["SOP 05/SOP/2025", "PMK 83/PMK.02/2022", "verifikasi berjenjang", "honorarium narasumber", "SPM=SPP"],
        regulasi=["PMK No. 32/PMK.02/2025", "PP 45/2013"],
    )
    objek1 = _digest(
        "00-input/objek-01-spp-spm-honor.pdf", "objek",
        """
BERKAS PEMBAYARAN HONORARIUM KEGIATAN SOSIALISASI (hal.1-4). SPP-LS Nomor 00123 tanggal 12 Mei 2026
senilai Rp 33.600.000. SPM Nomor 00201 tanggal 12 Mei 2026 senilai Rp 36.600.000 (SELISIH Rp 3.000.000
antara SPP dan SPM tidak dijelaskan). Rincian: honorarium 3 narasumber x 4 jam x Rp 2.000.000/jam =
Rp 24.000.000 (tarif Rp 2.000.000/jam MELEBIHI batas SBM Rp 1.400.000/jam → kelebihan Rp 600.000/jam x
4 jam x 3 = Rp 7.200.000). Moderator dibayar Rp 3.000.000 untuk 1 kegiatan (SBM Rp 1.000.000 →
kelebihan Rp 2.000.000). Lembar verifikasi (hal.4): kolom "verifikator" dan "PPSPM" ditandatangani
NAMA YANG SAMA (Sdr. A) — verifikasi berjenjang tidak berjalan. Daftar hadir narasumber TIDAK dilampirkan.
        """,
        kata_kunci=["SPP 00123", "SPM 00201", "honorarium", "Rp 2.000.000/jam", "verifikator"],
        tanggal=["2026-05-12"],
        nilai=["Rp 33.600.000", "Rp 36.600.000", "Rp 24.000.000"],
    )
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Menguji kepatuhan dan kewajaran pembayaran honorarium kegiatan terhadap kriteria "
                     "yang diunggah (SOP pembayaran + SBM TA 2026), termasuk kelengkapan bukti dan "
                     "kebenaran perhitungan.",
        "assigned_to": [at],
        "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Uraikan sasaran jadi checklist elemen: tarif vs SBM, kelengkapan bukti, verifikasi berjenjang, konsistensi SPP-SPM.",
            "Uji tiap elemen; hitung kelebihan bayar bila tarif > SBM; gali Sebab akar (RCA) atas kelemahan kontrol.",
            "Rekam temuan K/K/S/A dengan Sebab WAJIB (akar masalah) dan nilai indikasi kerugian negara.",
        ],
    }]
    context = """
# Konteks Penugasan — Audit Umum

Identitas: Audit Kepatuhan & Kewajaran Pembayaran Honorarium Kegiatan Sosialisasi
Jenis Pengawasan: Audit (keyakinan memadai)
Auditi: Satuan Kerja X, Kementerian Komunikasi dan Digital
Periode: TA 2026
Tahun Anggaran: 2026

Tujuan: Menilai kepatuhan dan kewajaran pembayaran honorarium terhadap SOP pembayaran dan SBM TA 2026.
Ruang Lingkup: Berkas pembayaran (SPP/SPM/lembar verifikasi) kegiatan sosialisasi Mei 2026.
Kriteria: SOP Pembayaran Belanja + SBM TA 2026. Audit penuh — dapat menghitung kerugian negara.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Audit atas satu berkas pembayaran honorarium untuk menguji kepatuhan tarif SBM,
kelengkapan bukti, dan efektivitas verifikasi berjenjang.
"""
    inputs = {
        "kriteria-01-sop-sbm-pembayaran.pdf": "[stub] SOP Pembayaran + SBM 2026 — lihat _INGESTED/kriteria-01.json",
        "objek-01-spp-spm-honor.pdf": "[stub] Berkas SPP/SPM honorarium — lihat _INGESTED/objek-01.json",
    }
    digests = [("kriteria-01", kriteria), ("objek-01", objek1)]
    return _write("audit-umum", at_name=at, sasaran=sasaran, context_md=context,
                  inputs=inputs, digests=digests)


# ---------------------------------------------------------------------------
# Skenario: evaluasi-umum (non-LKE, keyakinan terbatas, Sebab anti-mengarang, per dimensi/indikator)
# Evaluasi efektivitas program. Cacat: Q1 sasaran generik tak didekomposisi dimensi→indikator,
# Q2 dokumen pendukung tak lengkap, Q3 inkonsistensi data antar dokumen, Q4 SOP tak diikuti.
# ---------------------------------------------------------------------------
def scenario_evaluasi_umum() -> Path:
    at = "Sarah Auditor"
    kriteria = _digest(
        "00-input/kriteria-01-rubrik-evaluasi-program.pdf", "kriteria",
        """
KRITERIA/RUBRIK EVALUASI EFEKTIVITAS PROGRAM (diunggah auditor). Program dinilai pada 3 DIMENSI berbobot:
(A) Relevansi 30% — indikator: kesesuaian output dgn kebutuhan, target SMART; (B) Efektivitas 45% —
indikator: capaian outcome vs target, jangkauan penerima manfaat; (C) Keberlanjutan 25% — indikator:
kelembagaan, pembiayaan lanjutan. Tiap indikator diberi skor 1-4 terhadap bukti. SOP Program butir 4 —
monitoring & evaluasi triwulanan WAJIB didokumentasikan dan menjadi dasar perbaikan.
        """,
        kata_kunci=["rubrik", "dimensi", "indikator", "bobot", "efektivitas program"],
        regulasi=["Pedoman Evaluasi Program Internal Itjen II"],
    )
    objek1 = _digest(
        "00-input/objek-01-laporan-program.pdf", "objek",
        """
LAPORAN PELAKSANAAN PROGRAM PENINGKATAN LITERASI DIGITAL (hal.1-6). Ringkasan capaian menyatakan
"program berjalan efektif" TANPA menguraikan capaian per dimensi/indikator rubrik (tidak ada skor
Relevansi/Efektivitas/Keberlanjutan). Target outcome "meningkatnya literasi digital" tidak dinyatakan
angka target (tidak SMART). Data penerima manfaat: bagian Ringkasan menyebut 12.000 peserta, namun
Lampiran Daftar Peserta merekap 9.500 peserta (INKONSISTEN). Dokumen monitoring/evaluasi triwulanan
(disyaratkan SOP butir 4) TIDAK dilampirkan. Bukti pendukung capaian outcome (survei pra/pasca) tidak ada.
        """,
        kata_kunci=["literasi digital", "12.000 peserta", "9.500 peserta", "efektif"],
        tanggal=["2026-01-15"],
    )
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Menilai efektivitas Program Peningkatan Literasi Digital terhadap rubrik evaluasi "
                     "yang diunggah (dimensi Relevansi/Efektivitas/Keberlanjutan beserta indikator & bobot).",
        "assigned_to": [at],
        "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Dekomposisi sasaran generik 'menilai efektivitas' menjadi dimensi→indikator berbobot dari rubrik; nilai per indikator dengan bukti.",
            "Catat ketidaksesuaian per dimensi (K/K/S/A, Sebab anti-mengarang; boleh 'tidak cukup data'). Keyakinan terbatas.",
        ],
    }]
    context = """
# Konteks Penugasan — Evaluasi Umum

Identitas: Evaluasi Efektivitas Program Peningkatan Literasi Digital
Jenis Pengawasan: Evaluasi (non-LKE, keyakinan terbatas)
Auditi: Unit Pelaksana Program, Kementerian Komunikasi dan Digital
Periode: TA 2025 (evaluasi ex-post)
Tahun Anggaran: 2025

Tujuan: Menilai efektivitas program terhadap rubrik dimensi-indikator yang diunggah auditor.
Ruang Lingkup: Laporan pelaksanaan program + lampiran; dinilai per dimensi (Relevansi/Efektivitas/Keberlanjutan).
Kriteria: Rubrik Evaluasi Efektivitas Program + SOP Program. Evaluasi non-LKE (Sebab anti-mengarang).
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Evaluasi ex-post efektivitas program literasi digital berbasis rubrik berbobot,
menguji capaian per dimensi/indikator dan kelengkapan dokumentasi M&E.
"""
    inputs = {
        "kriteria-01-rubrik-evaluasi-program.pdf": "[stub] Rubrik evaluasi — lihat _INGESTED/kriteria-01.json",
        "objek-01-laporan-program.pdf": "[stub] Laporan program — lihat _INGESTED/objek-01.json",
    }
    digests = [("kriteria-01", kriteria), ("objek-01", objek1)]
    return _write("evaluasi-umum", at_name=at, sasaran=sasaran, context_md=context,
                  inputs=inputs, digests=digests)


# ---------------------------------------------------------------------------
# Skenario: pemantauan-umum (non-assurance, status warna KKSA, Sebab anti-mengarang)
# Pemantauan rencana aksi vs target/milestone. Cacat: Q1 fisik<target→MERAH, Q2 serapan>fisik,
# Q3 milestone slip+blocker, Q4 data tak lengkap → status tak dapat dipastikan (anti-mengarang).
# ---------------------------------------------------------------------------
def scenario_pemantauan_umum() -> Path:
    at = "Sarah Auditor"
    kriteria = _digest(
        "00-input/kriteria-01-rencana-aksi-target.pdf", "kriteria",
        """
RENCANA AKSI & TARGET PROGRAM (baseline pemantauan). Ambang status: 🔴 MERAH bila deviasi jadwal > 10%
periode; 🟡 KUNING bila 5-10%; 🟢 HIJAU bila on-track. Prinsip: realisasi pembayaran tidak boleh
melampaui progres fisik. Target cut-off Triwulan II: Kegiatan-1 fisik 90%; Kegiatan-2 milestone
"Uji Coba Sistem" selesai 30 Juni 2026; serapan mengikuti progres fisik.
        """,
        kata_kunci=["rencana aksi", "target", "milestone", "status", "cut-off TW II"],
        regulasi=["PP 39/2006"],
    )
    objek1 = _digest(
        "00-input/objek-01-laporan-progres.pdf", "objek",
        """
LAPORAN PROGRES PELAKSANAAN per cut-off 30 Juni 2026 (Triwulan II). Kegiatan-1: realisasi fisik 55%
terhadap target 90% (deviasi 35% > 10% → indikasi MERAH); serapan anggaran 80% sedangkan progres
fisik hanya 60% (bayar > fisik). Kegiatan-2: milestone "Uji Coba Sistem" tenggat 30 Juni 2026 BELUM
terealisasi (slip), blocker integrasi data belum tertangani. Kegiatan-3: laporan tidak menyertakan
data realisasi fisik maupun bukti progres (persentase capaian tidak dapat diverifikasi).
        """,
        kata_kunci=["progres fisik 55%", "serapan 80%", "milestone", "uji coba sistem", "blocker"],
        tanggal=["2026-06-30"],
    )
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Memantau status pelaksanaan rencana aksi program terhadap target & milestone per "
                     "cut-off Triwulan II 2026 dan menetapkan status (early warning) berbasis bukti.",
        "assigned_to": [at],
        "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Bandingkan realisasi vs target per kegiatan; tetapkan status warna sesuai ambang; catat deviasi K/K/S/A (Sebab anti-mengarang, Akibat/risiko).",
            "Bila data realisasi tidak lengkap → JANGAN tetapkan status pasti; nyatakan 'tidak dapat dipastikan / data tidak cukup'. Tanpa perhitungan kerugian negara.",
        ],
    }]
    context = """
# Konteks Penugasan — Pemantauan Umum

Identitas: Pemantauan Pelaksanaan Rencana Aksi Program (Triwulan II 2026)
Jenis Pengawasan: Pemantauan (non-assurance / early warning)
Auditi: Unit Pelaksana Program, Kementerian Komunikasi dan Digital
Periode: s.d. cut-off 30 Juni 2026
Tahun Anggaran: 2026

Tujuan: Memantau status pelaksanaan rencana aksi terhadap target & milestone; memberi peringatan dini.
Ruang Lingkup: Laporan progres per cut-off TW II vs rencana aksi/target. Tanpa keyakinan, tanpa kerugian negara.
Kriteria: Rencana Aksi & Target Program + ambang status. Sebab anti-mengarang.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Pemantauan status tiga kegiatan program terhadap target TW II dengan penetapan status
warna berbasis bukti dan penandaan item yang tak dapat dipastikan.
"""
    inputs = {
        "kriteria-01-rencana-aksi-target.pdf": "[stub] Rencana aksi & target — lihat _INGESTED/kriteria-01.json",
        "objek-01-laporan-progres.pdf": "[stub] Laporan progres — lihat _INGESTED/objek-01.json",
    }
    digests = [("kriteria-01", kriteria), ("objek-01", objek1)]
    return _write("pemantauan-umum", at_name=at, sasaran=sasaran, context_md=context,
                  inputs=inputs, digests=digests)


# ---------------------------------------------------------------------------
# Skenario: evaluasi-manajemen-risiko (non-LKE KKSAR, keyakinan terbatas, maturitas MR + AoI)
# Kriteria: Permenkominfo 6/2017 (primer) + ISO 31000:2018. Cacat: Q1 Formulir 4 pemantauan TW
# hanya sebagian, Q2 Piagam MR belum ditandatangani, Q3 Formulir 3 rencana penanganan kosong utk
# risiko tinggi, Q4 pedoman MR usang vs SOTK, Q5 UPR/pemilik risiko belum lengkap (Three Lines).
# ---------------------------------------------------------------------------
def scenario_evaluasi_mr() -> Path:
    at = "Sarah Auditor"
    kriteria = _digest(
        "00-input/kriteria-01-permenkominfo-6-2017-mr.pdf", "kriteria",
        """
KRITERIA: Peraturan Menkominfo No. 6 Tahun 2017 tentang Manajemen Risiko di Lingkungan Kementerian
(primer) + ISO 31000:2018 (pendukung). Ketentuan: (a) Piagam Manajemen Risiko WAJIB ditetapkan &
ditandatangani pimpinan sebagai komitmen kebijakan MR; (b) Struktur MR: Pemilik Risiko (UPR) & KMR
ditetapkan lengkap sesuai Three Lines Model; (c) Formulir 3 Rencana Penanganan Risiko WAJIB diisi untuk
risiko level sedang s.d. sangat tinggi; (d) Formulir 4 Pemantauan Risiko dilakukan & diinput SETIAP
TRIWULAN (4x setahun); (e) Pedoman/kerangka MR dimutakhirkan mengikuti SOTK & risk appetite terbaru.
        """,
        kata_kunci=["manajemen risiko", "Piagam MR", "UPR", "Three Lines", "Formulir 3", "Formulir 4"],
        regulasi=["Permenkominfo 6/2017", "ISO 31000:2018"],
    )
    objek1 = _digest(
        "00-input/objek-01-dokumen-mr-unit.pdf", "objek",
        """
DOKUMEN PENERAPAN MR UNIT AUDITAN TA 2025 (hal.1-8). Piagam Manajemen Risiko: tersedia draf namun BELUM
DITANDATANGANI pimpinan (belum diformalisasi). Struktur MR: UPR tingkat unit ditetapkan, namun Pemilik
Risiko tertinggi & sebagian KMR BELUM ditetapkan (pembagian Three Lines belum lengkap). Formulir 3
(Rencana Penanganan Risiko): untuk 5 risiko level tinggi–sangat tinggi (termasuk 1 risiko strategis),
kolom rencana aksi hanya diisi "monitoring berkala" tanpa rencana penanganan konkret; 3 dari 5 kosong.
Formulir 4 (Pemantauan Risiko Triwulanan): hanya tersedia untuk Triwulan I (April) dan Triwulan III
(Oktober) — TW II & TW IV tidak diinput (2 dari 4 triwulan). Pedoman MR unit masih mengacu SOTK lama
(belum dikinikan pasca reorganisasi; risk appetite statement belum ditinjau).
        """,
        kata_kunci=["Piagam MR", "belum ditandatangani", "Formulir 3", "Formulir 4", "Triwulan", "SOTK lama"],
        tanggal=["2025-04-15", "2025-10-20"],
    )
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Mengevaluasi penerapan Manajemen Risiko unit auditan terhadap Permenkominfo 6/2017 "
                     "(primer) dan ISO 31000:2018, meliputi kebijakan/piagam, struktur (UPR/Three Lines), "
                     "penilaian & penanganan risiko (Formulir 3), dan pemantauan triwulanan (Formulir 4).",
        "assigned_to": [at],
        "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Nilai kematangan/penerapan MR per area kriteria (kebijakan/piagam, struktur, penanganan, pemantauan, pemutakhiran).",
            "Catat gap sebagai Area of Improvement / temuan K/K/S/A (Sebab anti-mengarang; keyakinan terbatas). Rujuk pasal/formulir kriteria yang spesifik.",
        ],
    }]
    context = """
# Konteks Penugasan — Evaluasi Manajemen Risiko

Identitas: Evaluasi Penerapan Manajemen Risiko Unit Auditan
Jenis Pengawasan: Evaluasi Manajemen Risiko (keyakinan terbatas)
Auditi: Unit Auditan, Kementerian Komunikasi dan Digital
Periode: TA 2025
Tahun Anggaran: 2025

Tujuan: Menilai penerapan & kematangan MR terhadap Permenkominfo 6/2017 dan ISO 31000:2018.
Ruang Lingkup: Dokumen penerapan MR unit (Piagam, struktur UPR, Formulir 3 & 4, pedoman MR).
Kriteria: Permenkominfo 6/2017 (primer) + ISO 31000:2018 (pendukung). Evaluasi non-LKE; Sebab anti-mengarang.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Evaluasi penerapan MR unit auditan menyoroti kebijakan/piagam, struktur tata kelola risiko,
rencana penanganan risiko tinggi, dan konsistensi pemantauan risiko triwulanan.
"""
    inputs = {
        "kriteria-01-permenkominfo-6-2017-mr.pdf": "[stub] Permenkominfo 6/2017 + ISO 31000 — lihat _INGESTED/kriteria-01.json",
        "objek-01-dokumen-mr-unit.pdf": "[stub] Dokumen penerapan MR unit — lihat _INGESTED/objek-01.json",
    }
    digests = [("kriteria-01", kriteria), ("objek-01", objek1)]
    return _write("evaluasi-manajemen-risiko", at_name=at, sasaran=sasaran, context_md=context,
                  inputs=inputs, digests=digests)


# ---------------------------------------------------------------------------
# Helper ringkas untuk skenario criteria-driven 2-dokumen (kriteria + objek).
# ---------------------------------------------------------------------------
def _simple(skill: str, *, jenis: str, keyakinan: str, tujuan: str, ruang: str,
            kriteria_text: str, kriteria_reg: list[str], objek_text: str,
            sasaran_desc: str, langkah: list[str], objek_kata=None, objek_nilai=None,
            objek_tgl=None, doktrin_sebab: str = "anti-mengarang") -> Path:
    at = "Sarah Auditor"
    kd = _digest(f"00-input/kriteria-01-{skill}.pdf", "kriteria", kriteria_text,
                 kata_kunci=[skill, "kriteria"], regulasi=kriteria_reg)
    od = _digest(f"00-input/objek-01-{skill}.pdf", "objek", objek_text,
                 kata_kunci=objek_kata or [], nilai=objek_nilai or [], tanggal=objek_tgl or [])
    sasaran = [{
        "sasaran_id": "S-01", "deskripsi": sasaran_desc, "assigned_to": [at],
        "status": "DISETUJUI_KT", "langkah_kerja": langkah,
    }]
    context = f"""
# Konteks Penugasan — {jenis}

Identitas: {tujuan}
Jenis Pengawasan: {jenis} ({keyakinan})
Auditi: Unit Auditan, Kementerian Komunikasi dan Digital
Periode: TA 2025
Tahun Anggaran: 2025

Tujuan: {tujuan}
Ruang Lingkup: {ruang}
Doktrin Sebab: {doktrin_sebab}.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: {tujuan} berbasis kriteria yang diunggah; penilaian per elemen terhadap bukti.
"""
    inputs = {
        f"kriteria-01-{skill}.pdf": f"[stub] kriteria {skill} — lihat _INGESTED/kriteria-01.json",
        f"objek-01-{skill}.pdf": f"[stub] objek {skill} — lihat _INGESTED/objek-01.json",
    }
    return _write(skill, at_name=at, sasaran=sasaran, context_md=context, inputs=inputs,
                  digests=[("kriteria-01", kd), ("objek-01", od)])


# audit-kinerja (AUDIT, 2E, Sebab WAJIB/RCA, keyakinan memadai)
def scenario_audit_kinerja() -> Path:
    return _simple(
        "audit-kinerja", jenis="Audit Kinerja", keyakinan="keyakinan memadai; lingkup 2E",
        tujuan="Audit Kinerja Efektivitas & Efisiensi Program Pengawasan Konten Digital",
        ruang="Program pengawasan konten (sistem crawling/klasifikasi, tata kelola, anggaran O&M) TA 2025.",
        doktrin_sebab="Sebab WAJIB (root cause/RCA); lingkup 2E (ekonomisitas → audit-pengadaan)",
        kriteria_reg=["Perpres 29/2014", "PP 60/2008", "Renstra Komdigi", "SAIPI (AAIPI 2021)"],
        kriteria_text="""
KRITERIA AUDIT KINERJA: Renstra & Perjanjian Kinerja menetapkan target efektivitas sistem pengawasan
konten minimal 80% konten bermuatan negatif tertangani; setiap sistem/aplikasi WAJIB punya sumber data
tunggal (source of truth) yang dapat ditelusuri; anggaran O&M tidak boleh membiayai fungsi yang beririsan
(hindari duplikasi); hasil deteksi/crawling WAJIB ditindaklanjuti tuntas (verifikasi → takedown → closure).
Efektivitas = capaian outcome vs target; Efisiensi = biaya per output & bebas duplikasi.
        """,
        objek_text="""
LAPORAN KINERJA & DATA PROGRAM PENGAWASAN KONTEN TA 2025. (1) Efektivitas sistem klasifikasi konten
hanya 22,4% terhadap target 80% — sistem dapat di-bypass VPN, kontrol lemah. (2) Terdapat DUA sistem
(Sistem-A crawling & Sistem-B klasifikasi) menjalankan fungsi deteksi BERIRISAN; anggaran O&M keduanya
dibayar penuh (indikasi duplikasi/inefisiensi). (3) Hasil crawling 3,2 juta item terdeteksi, namun hanya
0,4 juta yang diverifikasi & ditindaklanjuti tuntas; 2,8 juta item menggantung tanpa closure. (4) LKj
melaporkan capaian "output tercapai 98%" namun sumber data capaian tidak dapat ditelusuri (tidak ada
source of truth; rekap manual berbeda antar unit). Riwayat: tidak ada integrasi sistem & tidak ada SOP closure.
        """,
        objek_kata=["efektivitas 22,4%", "target 80%", "duplikasi O&M", "3,2 juta item", "source of truth"],
        objek_tgl=["2025-12-31"],
        sasaran_desc="Menilai efektivitas & efisiensi (2E) program pengawasan konten terhadap target "
                     "kinerja; gali akar masalah (RCA) atas gap efektivitas, duplikasi sistem, tindak lanjut "
                     "deteksi yang tak tuntas, dan ketertelusuran data capaian.",
        langkah=[
            "Uji capaian tiap aspek 2E vs target/benchmark; identifikasi gap efektivitas & inefisiensi (duplikasi).",
            "Untuk tiap gap, gali Sebab sampai akar (why-tree/RCA) — WAJIB; nyatakan Akibat pada outcome.",
            "Rekam temuan K/K/S/A dengan Sebab akar; keyakinan memadai.",
        ],
    )


# pemantauan-tindak-lanjut (non-assurance, matriks status TL)
def scenario_pemantauan_tl() -> Path:
    return _simple(
        "pemantauan-tindak-lanjut", jenis="Pemantauan Tindak Lanjut", keyakinan="non-assurance",
        tujuan="Pemantauan Status Tindak Lanjut Rekomendasi Hasil Pengawasan (BPK/APIP)",
        ruang="Register rekomendasi BPK/APIP dan bukti tindak lanjut per PIC/Ditjen s.d. cut-off.",
        doktrin_sebab="Sebab anti-mengarang; status TL berbasis bukti",
        kriteria_reg=["PP 60/2008 Pasal 50", "SAIPI (AAIPI 2021)"],
        kriteria_text="""
KRITERIA PEMANTAUAN TL: status TL diklasifikasi Tuntas / Dalam Proses / Belum Ditindaklanjuti / Tidak
Dapat Ditindaklanjuti (TDD). Rekomendasi finansial (penyetoran ke kas negara) hanya Tuntas bila ada bukti
setor. Rekomendasi 'Belum Ditindaklanjuti' dengan umur > 365 hari = kritis. Status TDD hanya sah bila ada
dasar formal (mis. unit dibubarkan/SOTK berubah dengan SK). Rekomendasi WAJIB ditindaklanjuti (PP 60/2008 Ps.50).
        """,
        objek_text="""
REGISTER TINDAK LANJUT REKOMENDASI per cut-off 30 Juni 2026. (1) 4 rekomendasi struktural BPK (cluster
tata kelola) berstatus 'Belum Ditindaklanjuti', umur 410–520 hari (> 365 hari). (2) Rekomendasi penyetoran
ke kas negara Rp 91,9 miliar (kolokasi/Metro-E) berstatus 'Belum Ditindaklanjuti' — belum ada bukti setor.
(3) Rekomendasi verifikasi outstanding Rp 171,59 miliar berstatus 'Dalam Proses' — bukti TL baru parsial.
(4) Rate penyelesaian TL timpang antar-Ditjen: Ditjen-W 17,07% (7 dari 41) vs Ditjen-E 83,33% (15 dari 18).
(5) 2 rekomendasi atas unit yang telah berubah SOTK ditandai 'TDD' NAMUN tanpa melampirkan SK dasar formal.
        """,
        objek_kata=["Belum Ditindaklanjuti", "Rp 91,9 miliar", "Rp 171,59 miliar", "17,07%", "TDD"],
        objek_nilai=["Rp 91.900.000.000", "Rp 171.590.000.000"], objek_tgl=["2026-06-30"],
        sasaran_desc="Memantau status tindak lanjut rekomendasi hasil pengawasan (BPK/APIP) per cut-off "
                     "dan menandai deviasi (belum TL, TDD tanpa dasar, asimetri penyelesaian) berbasis bukti.",
        langkah=[
            "Klasifikasi status TL tiap rekomendasi (Tuntas/Proses/Belum/TDD) berbasis bukti; hitung umur (aging).",
            "Tandai deviasi: belum TL > 365 hari, finansial belum setor, TDD tanpa SK, asimetri rate. Sebab anti-mengarang.",
        ],
    )


# pemantauan-pengadaan (non-assurance, status pelaksanaan kontrak)
def scenario_pemantauan_pengadaan() -> Path:
    return _simple(
        "pemantauan-pengadaan", jenis="Pemantauan Pengadaan", keyakinan="non-assurance",
        tujuan="Pemantauan Pelaksanaan Kontrak Pengadaan (progres fisik, pembayaran, milestone)",
        ruang="Laporan progres kontrak, SPM/SP2D, jadwal & KAK per cut-off.",
        doktrin_sebab="Sebab anti-mengarang; status berbasis bukti",
        kriteria_reg=["Perpres 16/2018 jo. 12/2021 Pasal 78 (denda 1/1000)", "Perpres 46/2025"],
        kriteria_text="""
KRITERIA PEMANTAUAN PENGADAAN: progres fisik dibandingkan jadwal kontrak; pembayaran kumulatif TIDAK boleh
melampaui progres fisik; keterlambatan milestone dikenai denda 1/1000 per hari (Perpres 16/2018 jo 12/2021
Pasal 78); addendum kumulatif > 10% nilai kontrak = indikasi perencanaan lemah; deliverable/milestone
dinilai terhadap lingkup & jadwal KAK.
        """,
        objek_text="""
LAPORAN PROGRES KONTRAK per cut-off 30 Juni 2026 (nilai kontrak Rp 12.000.000.000). (1) Progres fisik
aktual 40% sedangkan target jadwal kontrak 70% (deviasi 30%). (2) Pembayaran kumulatif (SPM/SP2D) 55%
melampaui progres fisik 40% (bayar > fisik, risiko kelebihan bayar). (3) Milestone kritis 'Instalasi &
Uji Fungsi' tenggat 15 Juni 2026 TERLEWAT 15 hari — potensi denda 1/1000/hari belum dihitung/dikenakan.
(4) Terdapat 3 addendum kontrak kumulatif senilai 14% dari nilai kontrak (> 10%). (5) Dua deliverable yang
dijadwalkan selesai s.d. periode laporan belum tercapai.
        """,
        objek_kata=["progres fisik 40%", "pembayaran 55%", "milestone terlewat", "addendum 14%", "denda"],
        objek_nilai=["Rp 12.000.000.000"], objek_tgl=["2026-06-30", "2026-06-15"],
        sasaran_desc="Memantau pelaksanaan kontrak pengadaan terhadap jadwal, pembayaran, dan milestone KAK "
                     "per cut-off; menandai deviasi (fisik<jadwal, bayar>fisik, denda, addendum berlebih) berbasis bukti.",
        langkah=[
            "Bandingkan progres fisik vs jadwal, pembayaran vs fisik, milestone vs KAK; hitung indikasi denda 1/1000.",
            "Tandai deviasi K/K/S/A (Sebab anti-mengarang, Akibat/risiko). Non-assurance; tanpa hitung kerugian negara.",
        ],
    )


# evaluasi-spip (LKE, AoI tanpa Sebab, keyakinan penjaminan)
def scenario_evaluasi_spip() -> Path:
    return _simple(
        "evaluasi-spip", jenis="Evaluasi SPIP (Penjaminan Kualitas)", keyakinan="penjaminan (validasi PM)",
        tujuan="Penjaminan Kualitas Maturitas SPIP Unit (validasi penilaian mandiri)",
        ruang="LKE SPIP (nilai PM), Kertas Kerja, register risiko & RTP, bukti dukung per unsur.",
        doktrin_sebab="TANPA unsur Sebab (rezim LKE); gunakan Area of Improvement (AoI)",
        kriteria_reg=["PP 60/2008", "Peraturan BPKP 5/2021 (Pedoman Penilaian Maturitas SPIP)"],
        kriteria_text="""
KRITERIA SPIP (PK): penilaian mandiri (PM) unit divalidasi APIP (PK). Nilai PK yang LEBIH RENDAH dari PM
menandakan optimism bias → skor direvisi turun. Unsur II Penilaian Risiko (2.1 identifikasi, 2.2 analisis)
menuntut register risiko strategis & RTP tingkat strategis LENGKAP. Bukti/Kertas Kerja per sub-unsur WAJIB
terisi; aplikasi SPIP berfungsi. Unsur I Lingkungan Pengendalian menuntut kompetensi SDM penyelenggara SPIP
sesuai standar. Keluaran = skor maturitas + Area of Improvement (BUKAN temuan ber-Sebab).
        """,
        objek_text="""
LKE SPIP & KERTAS KERJA UNIT TA 2025. (1) Nilai PM unsur agregat 'Terkelola' (4,2) sedangkan bukti PK
hanya mendukung 'Terdefinisi' (3,1) — optimism bias, skor perlu direvisi TURUN. (2) Unsur II Penilaian
Risiko: register risiko strategis BELUM lengkap dan RTP tingkat strategis belum disusun (sub-unsur 2.1–2.2
gap). (3) Aplikasi SPIP bermasalah; sebagian Kertas Kerja (KK Lead II) tidak terisi (PM 0% tanpa bukti).
(4) Unsur I Lingkungan Pengendalian: kompetensi SDM penyelenggara SPIP/MR belum merata, standar kompetensi
belum dipenuhi. Tidak menghitung kerugian negara.
        """,
        objek_kata=["PM 4,2", "PK 3,1", "optimism bias", "register risiko", "Kertas Kerja"],
        sasaran_desc="Menjamin kualitas (validasi) penilaian mandiri maturitas SPIP unit terhadap Pedoman "
                     "BPKP 5/2021; identifikasi gap per unsur/sub-unsur sebagai Area of Improvement.",
        langkah=[
            "Validasi skor PM vs bukti (PK) per unsur/sub-unsur; turunkan skor bila optimism bias.",
            "Catat gap sebagai Area of Improvement (Kondisi-Kriteria-Akibat, TANPA Sebab); rujuk unsur/sub-unsur spesifik.",
        ],
    )


# evaluasi-sakip (LKE, AoI tanpa Sebab)
def scenario_evaluasi_sakip() -> Path:
    return _simple(
        "evaluasi-sakip", jenis="Evaluasi SAKIP/AKIP", keyakinan="terbatas (evaluatif); rezim LKE",
        tujuan="Evaluasi Implementasi SAKIP Unit (5 komponen)",
        ruang="Dokumen SAKIP: Renstra/PK/IKU, pengukuran kinerja, LKj, evaluasi internal.",
        doktrin_sebab="TANPA unsur Sebab (rezim LKE); gunakan Area of Improvement (AoI)",
        kriteria_reg=["PermenPANRB 88/2021 (Evaluasi AKIP)"],
        kriteria_text="""
KRITERIA SAKIP (PermenPANRB 88/2021): 5 komponen berbobot — Perencanaan Kinerja, Pengukuran, Pelaporan,
Evaluasi Internal, Capaian. Indikator/sasaran WAJIB SMART & berorientasi hasil (bukan proses/aktivitas);
penjenjangan (cascading) kinerja lengkap s.d. Eselon II/pegawai; hasil pengukuran DIPAKAI sebagai decision
tool (dimensi pemanfaatan). Keluaran = nilai/predikat AKIP + Area of Improvement (TANPA Sebab).
        """,
        objek_text="""
DOKUMEN SAKIP UNIT TA 2025. (1) Perencanaan Kinerja: sebagian IKU tidak SMART & berorientasi PROSES
(mis. '% kegiatan terlaksana'), bukan outcome. (2) Cascading kinerja belum lengkap sampai Eselon II/pegawai;
pohon kinerja terputus di level eselon I. (3) Komponen Pengukuran Kinerja bernilai TERENDAH; pengukuran
masih administratif, data kinerja belum andal. (4) Hasil pengukuran tersedia namun BELUM dipakai sebagai
decision tool (dimensi pemanfaatan lemah). (5) Predikat AKIP STAGNAN 'BB' tiga tahun berturut-turut
(nilai naik tipis 70,1→70,4→70,8; predikat tetap).
        """,
        objek_kata=["IKU tidak SMART", "cascading", "pengukuran terendah", "predikat BB stagnan"],
        sasaran_desc="Mengevaluasi implementasi SAKIP unit terhadap PermenPANRB 88/2021 (5 komponen); "
                     "identifikasi gap per komponen sebagai Area of Improvement.",
        langkah=[
            "Nilai tiap komponen SAKIP vs kriteria (SMART, cascading, pemanfaatan pengukuran, tren predikat).",
            "Catat gap sebagai Area of Improvement (Kondisi-Kriteria-Akibat, TANPA Sebab); rujuk komponen spesifik.",
        ],
    )


# evaluasi-reformasi-birokrasi (LKE 4-dimensi, AoI tanpa Sebab)
def scenario_evaluasi_rb() -> Path:
    return _simple(
        "evaluasi-reformasi-birokrasi", jenis="Evaluasi Reformasi Birokrasi", keyakinan="terbatas; rezim LKE",
        tujuan="Evaluasi Pelaksanaan Reformasi Birokrasi Unit",
        ruang="Rencana Aksi RB, data dukung capaian, dokumen Zona Integritas (ZI/WBK/WBBM).",
        doktrin_sebab="TANPA unsur Sebab (rezim LKE); gunakan Area of Improvement (AoI)",
        kriteria_reg=["KepmenPANRB 182/2024 (Juknis Evaluasi RB)", "PermenPANRB 9/2023"],
        kriteria_text="""
KRITERIA RB (KepmenPANRB 182/2024): dinilai 4 dimensi/lensa — Ketercapaian Output, Kesesuaian Waktu,
Kualitas Pelaksanaan, Ketepatan Pelaksanaan. Capaian RB dinilai sampai OUTCOME/dampak (bukan hanya
input-output); renaksi harus SESUAI JADWAL (justifikasi bila berubah); data dukung berupa LAPORAN HASIL
formal (bukan sekadar matriks/checklist); pembangunan Zona Integritas (WBK/WBBM) menunjukkan progres.
Keluaran = nilai RB + Area of Improvement (TANPA Sebab).
        """,
        objek_text="""
DOKUMEN PELAKSANAAN RB UNIT TA 2025. (1) Ketercapaian Output: Rencana Aksi RB dilaporkan 100% 'sesuai',
namun hanya level input-output; outcome/dampak (mis. indeks pelayanan, GEnerating impact) TIDAK diukur.
(2) Kesesuaian Waktu: timeline beberapa renaksi tidak sesuai jadwal; perubahan rencana aksi tanpa
justifikasi terdokumentasi. (3) Kualitas Pelaksanaan: data dukung capaian berupa matriks/checklist, BUKAN
Laporan Hasil formal; kertas kerja penilaian tidak lengkap. (4) Ketepatan Pelaksanaan: pembangunan Zona
Integritas menuju WBK/WBBM STAGNAN lintas tahun (persentase unit ber-ZI flat 12% tiga tahun).
        """,
        objek_kata=["100% output", "outcome tidak diukur", "matriks bukan laporan", "ZI stagnan 12%"],
        sasaran_desc="Mengevaluasi pelaksanaan Reformasi Birokrasi unit terhadap KepmenPANRB 182/2024 "
                     "(4 dimensi); identifikasi gap sebagai Area of Improvement.",
        langkah=[
            "Nilai tiap dimensi RB (output vs outcome, ketepatan waktu, kualitas bukti, progres ZI).",
            "Catat gap sebagai Area of Improvement (Kondisi-Kriteria-Akibat, TANPA Sebab); rujuk dimensi/indikator spesifik.",
        ],
    )


# ---------------------------------------------------------------------------
# Skenario: reviu-rka-kl (PBJ/RKA digest-only — stage _KKP/tor-*.json + rab-*.json;
# agen baca via read_digest, BUKAN read_ingested_digest). Cacat: P1 blok substansi TOR
# tak lengkap, P2 indikator tanpa target terukur, P3 RAB paket bulat tanpa rincian,
# P4 belanja modal besar tanpa spesifikasi teknis & metode pengadaan.
# ---------------------------------------------------------------------------
def scenario_reviu_rka_kl() -> Path:
    at = "Sarah Auditor"
    root = FIX_DIR / "reviu-rka-kl"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    (root / "_KKP").mkdir(parents=True)
    (root / "_PKP").mkdir()
    (root / "00-input").mkdir()
    tor = {
        "nama_ro": "RO Pembangunan Sistem Pemantauan Ruang Digital",
        "identitas_ro": {
            "kementerian": "Kementerian Komunikasi dan Digital",
            "unit_eselon_i": "Direktorat Jenderal Pengawasan Ruang Digital",
            "program_nama": "Program Pengawasan Ruang Digital",
            "kegiatan_nama": "Pengembangan Sistem Pengawasan Konten",
            "ro": "01", "volume": 1, "satuan": "Sistem",
        },
        "latar_belakang": "Kebutuhan sistem pemantauan konten bermuatan negatif yang terintegrasi.",
        "tujuan": "Membangun sistem pemantauan ruang digital untuk mendukung pengawasan konten.",
        # P2 — indikator tanpa target angka/parameter keberhasilan terukur:
        "output_indikator": "Indikator: tersedianya sistem pemantauan ruang digital. "
                            "(Tidak dinyatakan target angka capaian maupun parameter keberhasilan terukur.)",
        # P1 — blok substansi WAJIB TIDAK lengkap: metode pelaksanaan, jadwal/kurun waktu,
        # dan spesifikasi teknis SENGAJA tidak ada (hanya latar/tujuan/output yang ada).
        # P4 — belanja modal besar tanpa spesifikasi teknis & metode pengadaan:
        "komponen_belanja": "Termasuk belanja modal perangkat server & storage senilai Rp 5.200.000.000 "
                            "NAMUN tanpa spesifikasi teknis rinci dan tanpa metode pengadaan yang ditetapkan.",
        "dasar_hukum": [{"jenis_regulasi": "Perpres", "nomor": "29", "tahun": "2014"}],
        "biaya": {"total": 8500000000, "sumber_dana": "Rupiah Murni"},
        "_catatan_kelengkapan": "Blok yang ADA: latar_belakang, tujuan, output_indikator, komponen_belanja, "
                                "biaya, dasar_hukum. Blok WAJIB yang TIDAK ADA: metode pelaksanaan, "
                                "jadwal/kurun waktu, spesifikasi teknis komponen belanja modal.",
    }
    rab = {
        "nama_ro": "RO Pembangunan Sistem Pemantauan Ruang Digital",
        "total": 8500000000, "nilai_total": 8500000000, "komponen_count": 1,
        # P3 — RAB hanya paket bulat tanpa rincian harga satuan/volume:
        "komponen": [{
            "nama": "Paket Pembangunan Sistem Pemantauan (lumpsum)",
            "nilai": 8500000000, "volume": 1, "satuan": "paket",
            "rincian": "Tidak ada rincian harga satuan/volume per item — hanya paket bulat.",
        }],
    }
    (root / "_KKP" / "tor-01.json").write_text(json.dumps(tor, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "_KKP" / "rab-01.json").write_text(json.dumps(rab, ensure_ascii=False, indent=2), encoding="utf-8")
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": "Mereviu kualitas & kesesuaian TOR/RAB RO Pembangunan Sistem Pemantauan Ruang Digital "
                     "terhadap Kriteria IR2 (PMK 107/2024 Pasal 61): kelengkapan blok substansi, indikator "
                     "terukur, kewajaran/rincian biaya, dan konsistensi TOR↔RAB.",
        "assigned_to": [at], "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "read_digest (index) lalu read_digest(ro=01); telusuri tiap butir Checklist Kualitas RKA/TOR (Pasal 61).",
            "Catat ketidaksesuaian sebagai temuan K/K/S/A (Sebab anti-mengarang; keyakinan terbatas; Rekomendasi di LHR).",
        ],
    }]
    context = """
# Konteks Penugasan — Reviu RKA-K/L

Identitas: Reviu RKA-K/L RO Pembangunan Sistem Pemantauan Ruang Digital
Jenis Pengawasan: Reviu (keyakinan terbatas)
Auditi: Direktorat Jenderal Pengawasan Ruang Digital, Kementerian Komunikasi dan Digital
Periode: TA 2026 (reviu perencanaan)
Tahun Anggaran: 2026

Tujuan: Menelaah kualitas & kesesuaian TOR/RAB terhadap Kriteria IR2 PMK 107/2024 Pasal 61.
Ruang Lingkup: 1 RO (TOR + RAB) senilai Rp 8,5 miliar; digest tersedia di _KKP (tor-01.json, rab-01.json).
Doktrin Sebab: anti-mengarang. Reviu tidak menghitung kerugian negara.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Reviu perencanaan anggaran atas satu RO pembangunan sistem; menilai kelengkapan substansi
TOR, keterukuran indikator, rincian/kewajaran RAB, dan konsistensi TOR↔RAB.
"""
    (root / "_PKP" / "sasaran-assignment.json").write_text(
        json.dumps({"skill": "reviu-rka-kl", "sasaran": sasaran}, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "context.md").write_text(context.strip() + "\n", encoding="utf-8")
    (root / "00-input" / ".gitkeep").write_text("", encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# Skenario konsultansi (advisory — output PENDAPAT, bukan temuan). Dinilai
# judge_pendapat vs golden expected_pendapat (coverage + ketepatan + advisory_wajar).
# ---------------------------------------------------------------------------
def _konsultansi(skill: str, *, jenis: str, tujuan: str, pertanyaan: str,
                 material_text: str, material_reg: list[str], objek_kata=None) -> Path:
    at = "Sarah Auditor"
    md = _digest(f"00-input/permintaan-{skill}.pdf", "permintaan", material_text,
                 kata_kunci=objek_kata or [], regulasi=material_reg)
    sasaran = [{
        "sasaran_id": "S-01",
        "deskripsi": f"Menyusun PENDAPAT advisory (tidak mengikat) atas permintaan konsultansi: {pertanyaan}",
        "assigned_to": [at], "status": "DISETUJUI_KT",
        "langkah_kerja": [
            "Susun pendapat per pertanyaan dengan alur Pertanyaan → Dasar Hukum (pasal/ayat spesifik) → Analisis → Pendapat.",
            "Jaga sifat advisory: tidak mengikat, tidak memvonis pelanggaran, keputusan tetap pada pejabat berwenang; eskalasi bila ada indikasi pelanggaran material.",
        ],
    }]
    context = f"""
# Konteks Penugasan — {jenis}

Identitas: {tujuan}
Jenis Pengawasan: Konsultansi (advisory, non-assurance)
Auditi: Unit Kerja Peminta, Kementerian Komunikasi dan Digital
Periode: TA 2026 (pra-pelaksanaan)
Tahun Anggaran: 2026

Tujuan: {tujuan}
Pertanyaan konsultansi: {pertanyaan}
Ruang Lingkup: terbatas pada pertanyaan yang diajukan; TANPA Sebab/temuan; keputusan akhir pada pejabat berwenang.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Pendampingan/konsultansi pra-pelaksanaan; keluaran berupa pendapat advisory tidak mengikat.
"""
    inputs = {f"permintaan-{skill}.pdf": f"[stub] permintaan konsultansi {skill} — lihat _INGESTED/permintaan-{skill}.json"}
    return _write(skill, at_name=at, sasaran=sasaran, context_md=context, inputs=inputs,
                  digests=[(f"permintaan-{skill}", md)])


def scenario_konsultansi_umum() -> Path:
    return _konsultansi(
        "konsultansi-umum", jenis="Konsultansi Umum",
        tujuan="Pendapat APIP atas rancangan SOP Pengadaan Langsung unit kerja",
        pertanyaan="(1) Bolehkah paket Rp180 juta dipecah menjadi dua paket masing-masing di bawah ambang "
                   "agar masuk jalur Pengadaan Langsung? (2) Siapa yang berwenang menetapkan HPS dalam SOP? "
                   "(3) Dapatkah Inspektorat menandatangani persetujuan operasional atas rancangan SOP ini?",
        material_reg=["Perpres 16/2018 jo. 12/2021", "Perlem LKPP 12/2021"],
        material_text="""
NOTA DINAS PERMINTAAN PENDAPAT + RANCANGAN SOP PENGADAAN LANGSUNG. Unit kerja menanyakan: (1) rencana
memecah satu paket kebutuhan Rp180.000.000 menjadi 2 paket @ Rp90 juta agar keduanya masuk ambang
Pengadaan Langsung (< Rp200 juta) — apakah boleh? (2) rancangan SOP belum menyebut siapa penetap HPS
(ada usulan fungsi penyusun=penetap=pemeriksa dirangkap satu orang); (3) unit meminta Inspektorat ikut
menandatangani lembar persetujuan operasional SOP. Konteks: kebutuhan tunggal, spesifikasi sama, waktu bersamaan.
        """,
        objek_kata=["pemecahan paket", "Rp180 juta", "Pengadaan Langsung", "HPS", "persetujuan"],
    )


def scenario_konsultasi_pengadaan() -> Path:
    return _konsultansi(
        "konsultasi-pengadaan", jenis="Konsultasi Pengadaan",
        tujuan="Pendampingan pra-pengadaan perangkat lunak unit kerja",
        pertanyaan="Bolehkah paket pengadaan perangkat lunak senilai Rp2,4 miliar dilakukan melalui "
                   "Penunjukan Langsung / e-purchasing katalog, dan bagaimana urutan penetapan "
                   "pemaketan/spesifikasi/HPS/metode pemilihannya?",
        material_reg=["Perpres 16/2018 jo. 12/2021", "Perlem LKPP 12/2021", "Perlem LKPP 4/2024"],
        material_text="""
NOTA DINAS PENDAMPINGAN PRA-PENGADAAN (DJED.6). Unit berencana mengadakan perangkat lunak senilai
Rp2.400.000.000 dan mengusulkan Penunjukan Langsung / e-purchasing katalog sebagai jalur utama. Spesifikasi
teknis masih umum/ambigu (belum final); HPS belum disusun; terdapat >1 penyedia potensial di pasar/katalog.
Unit menanyakan kelayakan metode, urutan penetapan pemaketan-spesifikasi-HPS-metode, serta batas peran APIP.
        """,
        objek_kata=["Penunjukan Langsung", "e-purchasing", "Rp2,4 miliar", "spesifikasi", "HPS"],
    )


# ---------------------------------------------------------------------------
# Studi kasus hardening: DUA penugasan reviu-rka-kl, RKA SAMA, sasaran BEDA.
# P1 fokus keselarasan RO/IRO↔kegiatan/program + isu↔intervensi.
# P2 fokus kesesuaian RAB↔SBM + data dukung pembentuk harga (item di luar SBM).
# RKA menanam cacat kedua dimensi + 1 UMPAN PRESISI (item luar-SBM ber-data-dukung
# wajar yg TIDAK boleh dijadikan temuan).
# ---------------------------------------------------------------------------
def _rka_case(dirname: str, *, sasaran_id: str, sasaran_desc: str, langkah: list[str]) -> Path:
    at = "Sarah Auditor"
    root = FIX_DIR / dirname
    if root.exists():
        import shutil
        shutil.rmtree(root)
    (root / "_KKP").mkdir(parents=True)
    (root / "_PKP").mkdir()
    (root / "00-input").mkdir()
    tor = {
        "nama_ro": "RO Pengembangan Platform Literasi Digital",
        "identitas_ro": {
            "kementerian": "Kementerian Komunikasi dan Digital",
            "unit_eselon_i": "Direktorat Jenderal Ekosistem Digital",
            "program_nama": "Program Ekosistem Digital",
            "kegiatan_nama": "Peningkatan Literasi Digital Masyarakat",
            "ro": "01", "volume": 1, "satuan": "Platform",
        },
        "isu_latar_belakang": "Isu kegiatan: rendahnya tingkat literasi digital MASYARAKAT (indeks 3,2 dari 5); "
                              "akar masalah = minimnya akses edukasi/konten literasi & pendampingan untuk masyarakat.",
        "sasaran_kegiatan": "Meningkatnya literasi digital masyarakat.",
        "indikator_kegiatan_IKK": "Indeks Literasi Digital Masyarakat (baseline 3,2 → target 3,8).",
        "indikator_RO_IRO": "Jumlah kegiatan sosialisasi platform yang terlaksana (target 40 kegiatan).",
        "strategi_intervensi": "Komponen utama RO: pengadaan server, storage, dan lisensi perangkat lunak "
                               "platform (infrastruktur TI); pengembangan aplikasi platform.",
        "dasar_hukum": [{"jenis_regulasi": "PMK", "nomor": "107", "tahun": "2024"}],
        "biaya": {"total": 1650000000, "sumber_dana": "Rupiah Murni"},
        "_catatan": "IRO berupa hitung-aktivitas (jumlah sosialisasi) — bukan outcome; IKK berbasis outcome "
                    "(indeks literasi). Intervensi utama = infrastruktur TI, sedangkan akar isu = akses edukasi/konten "
                    "literasi masyarakat.",
    }
    rab = {
        "nama_ro": "RO Pengembangan Platform Literasi Digital",
        "total": 1650000000, "nilai_total": 1650000000, "komponen_count": 4,
        "komponen": [
            {"nama": "Honorarium narasumber sosialisasi", "akun": "521213", "volume": 40, "satuan": "jam",
             "harga_satuan": 2000000, "nilai": 80000000, "diatur_sbm": True,
             "data_dukung": "n/a (satuan diatur SBM honorarium narasumber)",
             "_catatan": "Rp 2.000.000/jam MELEBIHI batas SBM honorarium narasumber (Rp 1.400.000/jam)."},
            {"nama": "Jasa pengembangan aplikasi platform (software house)", "akun": "522191", "volume": 1,
             "satuan": "paket", "harga_satuan": 850000000, "nilai": 850000000, "diatur_sbm": False,
             "data_dukung": "ADA & WAJAR: survei/RFI 3 penyedia (Rp 820jt / 855jt / 880jt) + HPS berbasis keahlian; "
                            "harga RAB Rp 850jt berada di kisaran wajar data dukung.",
             "_catatan": "Di luar SBM, TAPI data dukung pembentuk harga lengkap & wajar → BUKAN deviasi (umpan presisi)."},
            {"nama": "Sewa infrastruktur cloud khusus", "akun": "522141", "volume": 12, "satuan": "bulan",
             "harga_satuan": 25000000, "nilai": 300000000, "diatur_sbm": False,
             "data_dukung": "TIDAK ADA — tidak dilampirkan survei/RFI, kontrak/PO pembanding, maupun HPS.",
             "_catatan": "Di luar SBM & tanpa data dukung pembentuk harga → harga tak berdasar (perlu jadi catatan)."},
            {"nama": "ATK & konsumsi rapat", "akun": "521211", "volume": 10, "satuan": "paket",
             "harga_satuan": 2000000, "nilai": 20000000, "diatur_sbm": True,
             "data_dukung": "n/a", "_catatan": "Dalam batas SBM → wajar."},
        ],
    }
    (root / "_KKP" / "tor-01.json").write_text(json.dumps(tor, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "_KKP" / "rab-01.json").write_text(json.dumps(rab, ensure_ascii=False, indent=2), encoding="utf-8")
    sasaran = [{"sasaran_id": sasaran_id, "deskripsi": sasaran_desc, "assigned_to": [at],
                "status": "DISETUJUI_KT", "langkah_kerja": langkah}]
    context = f"""
# Konteks Penugasan — Reviu RKA-K/L

Identitas: Reviu RKA-K/L RO Pengembangan Platform Literasi Digital
Jenis Pengawasan: Reviu (keyakinan terbatas)
Auditi: Direktorat Jenderal Ekosistem Digital, Kementerian Komunikasi dan Digital
Periode: TA 2026 (reviu perencanaan)
Tahun Anggaran: 2026

Tujuan: Reviu kualitas & kesesuaian RKA-K/L sesuai Kriteria IR2 PMK 107/2024 Pasal 61, DIFOKUSKAN pada sasaran penugasan.
Ruang Lingkup: 1 RO (TOR + RAB) senilai Rp 1,65 miliar; digest di _KKP (tor-01.json, rab-01.json).
Sasaran penugasan: {sasaran_desc}
Doktrin Sebab: anti-mengarang. Reviu tidak menghitung kerugian negara.
Tim: Sarah Auditor (Anggota Tim).

Gambaran Umum: Reviu perencanaan atas satu RO platform literasi digital; kedalaman & titik berat mengikuti sasaran penugasan.
"""
    (root / "_PKP" / "sasaran-assignment.json").write_text(
        json.dumps({"skill": "reviu-rka-kl", "sasaran": sasaran}, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "context.md").write_text(context.strip() + "\n", encoding="utf-8")
    (root / "00-input" / ".gitkeep").write_text("", encoding="utf-8")
    return root


def scenario_reviu_rka_kl_p1() -> Path:
    return _rka_case(
        "reviu-rka-kl-p1", sasaran_id="S-01",
        sasaran_desc="Menilai KESELARASAN RO & indikator RO (IRO) terhadap kegiatan & program, serta "
                     "keselarasan isu dan intervensi kegiatan yang diusulkan dalam RO (relevansi/theory of change).",
        langkah=[
            "Telusuri kerangka logis program → kegiatan → RO; nilai keselarasan IRO terhadap IKK/indikator kegiatan.",
            "Nilai apakah intervensi/komponen RO menjawab akar isu kegiatan; angkat ketidakselarasan sebagai catatan K/K/S/A.",
            "Aspek biaya/SBM di luar fokus sasaran → pass ringan; bila ada sinyal material, catat sebagai eskalasi ke KT.",
        ],
    )


def scenario_reviu_rka_kl_p2() -> Path:
    return _rka_case(
        "reviu-rka-kl-p2", sasaran_id="S-01",
        sasaran_desc="Menilai KESESUAIAN RAB terhadap SBM, dan kewajaran harga komponen yang TIDAK diatur SBM "
                     "berdasarkan data dukung pembentuk harga (survei/RFI, kontrak pembanding, HPS).",
        langkah=[
            "Untuk tiap komponen RAB: bila diatur SBM → uji harga vs batas SBM; bila di luar SBM → uji thd data dukung pembentuk harga.",
            "Deviasi/catatan hanya bila harga > SBM, atau (luar SBM) data dukung tidak ada / harga tidak wajar. Item luar-SBM ber-data-dukung wajar → 'telah memenuhi'.",
            "Aspek keselarasan/kerangka logis di luar fokus sasaran → pass ringan; bila ada sinyal material, catat sebagai eskalasi ke KT.",
        ],
    )


SCENARIOS = {
    "reviu-rka-kl": scenario_reviu_rka_kl,
    "reviu-rka-kl-p1": scenario_reviu_rka_kl_p1,
    "reviu-rka-kl-p2": scenario_reviu_rka_kl_p2,
    "konsultansi-umum": scenario_konsultansi_umum,
    "konsultasi-pengadaan": scenario_konsultasi_pengadaan,
    "reviu-umum": scenario_reviu_umum,
    "audit-umum": scenario_audit_umum,
    "evaluasi-umum": scenario_evaluasi_umum,
    "pemantauan-umum": scenario_pemantauan_umum,
    "evaluasi-manajemen-risiko": scenario_evaluasi_mr,
    "audit-kinerja": scenario_audit_kinerja,
    "pemantauan-tindak-lanjut": scenario_pemantauan_tl,
    "pemantauan-pengadaan": scenario_pemantauan_pengadaan,
    "evaluasi-spip": scenario_evaluasi_spip,
    "evaluasi-sakip": scenario_evaluasi_sakip,
    "evaluasi-reformasi-birokrasi": scenario_evaluasi_rb,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", default="all")
    a = ap.parse_args()
    todo = SCENARIOS if a.skill == "all" else {a.skill: SCENARIOS[a.skill]}
    for name, fn in todo.items():
        root = fn()
        print(f"✓ fixture: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
