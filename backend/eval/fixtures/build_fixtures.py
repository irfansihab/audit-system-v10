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
KRITERIA YANG DIUNGGAH: (1) SOP Pembayaran Belanja Satker, (2) Standar Biaya Masukan (SBM) TA 2026.
SOP butir 5 — Sebelum penerbitan SPM, WAJIB dilakukan verifikasi berjenjang: verifikator (staf) →
PPK menguji kebenaran tagihan → PPSPM menerbitkan SPM. Verifikator dan PPSPM TIDAK boleh orang yang sama.
SOP butir 6 — Setiap pembayaran honorarium narasumber WAJIB dilampiri: undangan, daftar hadir asli,
materi/bahan, dan bukti transfer. SBM TA 2026 — honorarium narasumber eselon II setara: batas tertinggi
Rp 1.400.000/jam/orang; moderator Rp 1.000.000/kegiatan.
        """,
        kata_kunci=["SOP pembayaran", "SBM 2026", "verifikasi berjenjang", "honorarium narasumber"],
        regulasi=["PMK 83/PMK.02/2022 (SBM)", "PP 45/2013"],
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


SCENARIOS = {
    "reviu-umum": scenario_reviu_umum,
    "audit-umum": scenario_audit_umum,
    "evaluasi-umum": scenario_evaluasi_umum,
    "pemantauan-umum": scenario_pemantauan_umum,
    "evaluasi-manajemen-risiko": scenario_evaluasi_mr,
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
