"""
cross_check.py — Rule-based cross-check untuk audit-pengadaan.

Usage:
    python cross_check.py <pengadaan-digest.json> [-o anomalies.json]

Kolom KKP audit-pengadaan (Keyakinan Memadai): No, Judul, Kondisi, Kriteria,
Sebab, Akibat. Rule ini memproduksi draft_catatan dengan 5 kolom tersebut
(Rekomendasi dirumuskan di LHA setelah gate auditor).
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

KRITIS = "KRITIS"
PERINGATAN = "PERINGATAN"
INFO = "INFO"


def _rule(rule_id, severity, aspek, judul, deskripsi, bukti=None, draft=None):
    return {
        "rule_id": rule_id,
        "severity": severity,
        "aspek": aspek,
        "judul": judul,
        "deskripsi": deskripsi,
        "bukti": bukti or {},
        "draft_catatan": draft,
    }


def _first(digest: dict, doc_type: str) -> dict | None:
    """Ambil entry pertama dari dokumen ber-tipe tertentu."""
    items = digest.get("dokumen", {}).get(doc_type, [])
    return items[0] if items else None


def _parsed(entry: dict | None) -> dict:
    return (entry or {}).get("parsed") or {}


# ============================================================
# RULES
# ============================================================

def rule_d1_dokumen_kunci_missing(digest: dict) -> dict | None:
    """D.1 — KAK/HPS/Kontrak tidak ditemukan di folder."""
    missing = digest.get("missing_types", [])
    if not missing:
        return None
    return _rule(
        "D.1", KRITIS if "kontrak" in missing else PERINGATAN, "Dokumentasi",
        f"Dokumen kunci tidak ditemukan: {', '.join(missing)}",
        f"Audit tidak dapat dilaksanakan penuh tanpa dokumen kunci {missing}.",
        bukti={"missing": missing},
        draft={
            "kondisi": f"Berdasarkan penelaahan folder penugasan, dokumen {', '.join(missing).upper()} "
                       f"tidak ditemukan. Tim audit telah meminta auditan untuk menyediakan dokumen, "
                       f"namun hingga batas waktu audit dokumen belum diterima.",
            "kriteria": "Perpres 16/2018 jo. Perpres 12/2021 Pasal 25 — dokumen perencanaan pengadaan "
                        "wajib tersedia dan terdokumentasi. Standar AAIPI terkait kecukupan bukti audit.",
            "sebab": "Pengelolaan dokumen pengadaan belum tertib — dokumen belum di-input ke sistem "
                     "penyimpanan terpusat atau berada di lokasi/folder yang tidak standar.",
            "akibat": "Auditor tidak dapat menguji aspek perencanaan/pemilihan/pembayaran secara penuh; "
                      "keyakinan memadai atas pengadaan ini tidak dapat diberikan tanpa dokumen "
                      "pendukung.",
        }
    )


def rule_p1_hps_tanpa_pembentuk_harga(digest: dict) -> dict | None:
    """P.1 — HPS tidak didukung dokumen pembentuk harga."""
    hps = _parsed(_first(digest, "hps"))
    if not hps:
        return None
    if hps.get("ada_dokumen_pembentuk_harga"):
        return None
    # cek HPS detail atau RFI ada terpisah
    if digest.get("dokumen", {}).get("rfi") or digest.get("dokumen", {}).get("hps_detail"):
        return None
    return _rule(
        "P.1", PERINGATAN, "Perencanaan",
        "HPS tidak didukung dokumen pembentuk harga yang lengkap",
        "HPS ditemukan namun tidak menyebut penawaran vendor/market research; RFI juga tidak ada di folder.",
        bukti={"hps_parsed": hps},
        draft={
            "kondisi": f"HPS bernilai Rp {hps.get('total') or '—'} tidak didukung dengan dokumen "
                       f"pembentuk harga (penawaran vendor, hasil RFI, atau market research) yang "
                       f"dapat ditelusuri di folder penugasan.",
            "kriteria": "Perpres 16/2018 jo. Perpres 12/2021 Pasal 26 — HPS disusun berdasarkan keahlian "
                        "dan data yang dapat dipertanggungjawabkan, antara lain harga pasar, informasi "
                        "biaya, atau harga kontrak sebelumnya.",
            "sebab": "Proses penyusunan HPS belum dokumentatif — dokumen pembentuk harga tidak "
                     "dilampirkan pada dossier pengadaan.",
            "akibat": "Kewajaran nilai HPS tidak dapat diverifikasi; berpotensi menimbulkan risiko "
                      "penetapan HPS yang tidak sesuai nilai pasar dan kerugian negara.",
        }
    )


def rule_p2_kak_hps_periode_beda(digest: dict) -> dict | None:
    """P.2 — Periode di KAK berbeda dengan di HPS."""
    kak = _parsed(_first(digest, "kak"))
    hps = _parsed(_first(digest, "hps"))
    if not (kak and hps):
        return None
    pk = kak.get("periode")
    ph = hps.get("periode")
    if not (pk and ph):
        return None
    if pk.strip() == ph.strip():
        return None
    return _rule(
        "P.2", PERINGATAN, "Perencanaan",
        f"Periode KAK ({pk}) berbeda dengan HPS ({ph})",
        "Inkonsistensi periode pengadaan antara KAK dan HPS.",
        bukti={"kak_periode": pk, "hps_periode": ph},
        draft={
            "kondisi": f"KAK menyebutkan periode pengadaan selama {pk}, sedangkan HPS menghitung "
                       f"komponen untuk periode {ph}.",
            "kriteria": "Perpres 16/2018 Pasal 26 — HPS dibuat sesuai KAK; Kriteria IR2 butir 3 "
                        "tentang konsistensi internal dokumen perencanaan.",
            "sebab": "Koordinasi antara unit penyusun KAK dan penyusun HPS belum memadai, atau "
                     "terdapat revisi periode yang tidak dikomunikasikan ulang antar dokumen.",
            "akibat": "Nilai HPS tidak proporsional dengan ruang lingkup di KAK; berisiko over/"
                      "under-budgeting dan pengaruhnya pada evaluasi pemilihan penyedia.",
        }
    )


def rule_p3_kak_hps_sla_beda(digest: dict) -> dict | None:
    """P.3 — SLA di KAK berbeda dengan di HPS."""
    kak = _parsed(_first(digest, "kak"))
    hps = _parsed(_first(digest, "hps"))
    if not (kak and hps):
        return None
    sk = kak.get("sla_value")
    sh = hps.get("sla_value")
    if not (sk and sh):
        return None
    if sk == sh:
        return None
    return _rule(
        "P.3", PERINGATAN, "Perencanaan",
        f"SLA berbeda antara KAK ({sk}) dan HPS ({sh})",
        "Inkonsistensi nilai SLA.",
        bukti={"kak_sla": sk, "hps_sla": sh},
        draft={
            "kondisi": f"KAK menetapkan SLA {sk}, namun HPS menghitung dengan asumsi SLA {sh}.",
            "kriteria": "Perpres 16/2018 Pasal 19 — persyaratan teknis barang/jasa harus konsisten "
                        "lintas dokumen perencanaan; Kriteria IR2 konsistensi internal.",
            "sebab": "Perubahan SLA pada salah satu dokumen tidak ditransmisikan ke dokumen lain, "
                     "atau perbedaan interpretasi antar unit penyusun.",
            "akibat": "Kewajiban kontraktual penyedia menjadi ambigu; berpotensi penalti SLA yang "
                      "tidak dapat ditegakkan atau penyedia keberatan atas tuntutan SLA lebih tinggi.",
        }
    )


# Label manusiawi komponen ruang lingkup (selaras digest_pengadaan._LINGKUP_LABEL).
_LINGKUP_LABEL = {
    "migrasi": "migrasi data/sistem", "instalasi": "instalasi/pemasangan",
    "pelatihan": "pelatihan/alih pengetahuan", "pemeliharaan": "pemeliharaan/perawatan",
    "garansi": "garansi/masa pemeliharaan", "pengujian": "pengujian/commissioning",
    "lisensi": "lisensi/langganan",
}


def rule_p4_lingkup_kak_tak_di_hps(digest: dict) -> dict | None:
    """P.4 — Komponen ruang lingkup signifikan disebut di KAK tapi tak teralokasi di HPS.

    UMUM lintas jenis pengadaan (barang/konstruksi/jasa/konsultansi): migrasi,
    instalasi, pelatihan, pemeliharaan, garansi, pengujian, lisensi. Heuristik
    presence-only — auditor wajib konfirmasi ke dokumen.
    """
    kak = _parsed(_first(digest, "kak"))
    hps = _parsed(_first(digest, "hps"))
    if not (kak and hps):
        return None
    kak_l = kak.get("lingkup_komponen") or {}
    hps_l = hps.get("lingkup_komponen") or {}
    if not kak_l:
        return None
    gap = [k for k, v in kak_l.items() if v and not hps_l.get(k)]
    if not gap:
        return None
    label_str = ", ".join(_LINGKUP_LABEL.get(k, k) for k in gap)
    return _rule(
        "P.4", PERINGATAN, "Perencanaan",
        f"Komponen ruang lingkup di KAK tak teralokasi di HPS: {label_str}",
        "Komponen biaya yang disyaratkan KAK tidak tercermin di HPS.",
        bukti={
            "komponen_gap": gap,
            "kak_komponen": [k for k, v in kak_l.items() if v],
            "hps_komponen": [k for k, v in hps_l.items() if v],
        },
        draft={
            "kondisi": f"KAK mencantumkan komponen ruang lingkup berikut sebagai bagian pekerjaan: "
                       f"{label_str}; namun HPS tidak memuat komponen biaya yang dapat dikenali untuk "
                       f"komponen tersebut.",
            "kriteria": "Perpres 16/2018 Pasal 26 — HPS harus mencakup seluruh komponen biaya yang "
                        "diperlukan untuk pelaksanaan pekerjaan sesuai KAK.",
            "sebab": "Komponen tersebut mungkin dianggap bagian dari pekerjaan utama, atau terdapat "
                     "misalignment ruang lingkup antara penyusun KAK dan penyusun HPS.",
            "akibat": "Biaya komponen berpotensi menjadi addendum yang membesarkan pagu, atau penyedia "
                      "menolak melaksanakannya karena tidak termasuk dalam nilai kontrak.",
        }
    )


def rule_k1_nilai_kontrak_vs_hps(digest: dict) -> dict | None:
    """K.1 — Nilai kontrak >= HPS (tidak wajar)."""
    kontrak = _parsed(_first(digest, "kontrak"))
    hps = _parsed(_first(digest, "hps"))
    if not (kontrak and hps):
        return None
    nk = kontrak.get("nilai_kontrak")
    nh = hps.get("total")
    if not (nk and nh):
        return None
    if nk < nh:
        return None
    return _rule(
        "K.1", PERINGATAN, "Kontrak",
        f"Nilai kontrak (Rp {nk:,}) ≥ HPS (Rp {nh:,})",
        "Nilai kontrak seharusnya lebih rendah atau sama dengan HPS setelah proses negosiasi/tender.",
        bukti={"nilai_kontrak": nk, "hps": nh, "selisih": nk - nh},
        draft={
            "kondisi": f"Nilai kontrak Rp {nk:,} sama dengan atau melebihi HPS Rp {nh:,} "
                       f"(selisih Rp {nk - nh:,}).",
            "kriteria": "Perpres 16/2018 Pasal 26 ayat (3) — nilai kontrak paling tinggi sama "
                        "dengan HPS; prinsip efisiensi pengadaan.",
            "sebab": "Proses negosiasi belum optimal, atau HPS ditetapkan kurang dari nilai pasar "
                     "sehingga tidak ada ruang negosiasi.",
            "akibat": "Tidak ada penghematan dari proses pengadaan; berpotensi menjadi temuan "
                      "pemeriksaan atas kewajaran nilai kontrak.",
        }
    )


def rule_k2_kontrak_tanpa_sla(digest: dict) -> dict | None:
    """K.2 — Kontrak tidak memuat klausul SLA untuk pekerjaan yang seharusnya SLA-based."""
    kontrak = _parsed(_first(digest, "kontrak"))
    kak = _parsed(_first(digest, "kak"))
    if not kontrak:
        return None
    if kontrak.get("sla_clause"):
        return None
    # flag jika KAK menyebut SLA tapi kontrak tidak
    if kak and kak.get("sla_disebut"):
        return _rule(
            "K.2", PERINGATAN, "Kontrak",
            "Kontrak tidak memuat klausul SLA padahal KAK mensyaratkan SLA",
            "Klausul SLA tidak terdeteksi di kontrak.",
            bukti={"kak_sla": kak.get("sla_value"), "kontrak_sla": None},
            draft={
                "kondisi": f"KAK mensyaratkan SLA {kak.get('sla_value') or '—'}, namun teks kontrak "
                           f"tidak memuat klausul SLA yang mengikat penyedia.",
                "kriteria": "Perpres 16/2018 Pasal 19 — kontrak harus memuat seluruh persyaratan "
                            "teknis sesuai KAK; Pasal 52 — klausul kinerja dan penalti.",
                "sebab": "Draf kontrak dibuat dari template standar tanpa menyesuaikan klausul SLA "
                         "dari KAK; atau klausul SLA dihapus saat negosiasi tanpa justifikasi.",
                "akibat": "K/L kehilangan dasar hukum untuk menuntut ganti rugi/penalti apabila "
                          "SLA tidak terpenuhi; risiko kerugian operasional dan keuangan.",
            }
        )
    return None


def rule_k3_kontrak_tanpa_jaminan(digest: dict) -> dict | None:
    """K.3 — Kontrak > Rp200 jt tanpa klausul Jaminan Pelaksanaan.

    Ber-guard AMBANG NILAI: Jaminan Pelaksanaan hanya WAJIB untuk pengadaan
    barang/konstruksi/jasa lainnya > Rp200 juta (Perpres 16/2018 Ps. 33).
    Bila nilai kontrak tak diketahui atau <= ambang → TIDAK di-flag (hindari
    false positive untuk kontrak kecil, jasa konsultansi, & e-purchasing yang
    dikecualikan dari kewajiban jaminan).
    """
    kontrak = _parsed(_first(digest, "kontrak"))
    if not kontrak:
        return None
    if kontrak.get("jaminan_pelaksanaan"):
        return None
    nilai = kontrak.get("nilai_kontrak")
    if not nilai or nilai <= 200_000_000:
        return None
    return _rule(
        "K.3", PERINGATAN, "Kontrak",
        f"Kontrak Rp {nilai:,} (> Rp200 jt) tanpa klausul Jaminan Pelaksanaan",
        "Jaminan Pelaksanaan (umumnya 5% nilai kontrak) tidak tercantum padahal nilai mewajibkan.",
        bukti={"nilai_kontrak": nilai, "kontrak": (kontrak or {}).get("nomor")},
        draft={
            "kondisi": f"Nilai kontrak Rp {nilai:,} melampaui ambang Rp200 juta, namun klausul "
                       f"persentase Jaminan Pelaksanaan tidak ditemukan di teks kontrak.",
            "kriteria": "Perpres 16/2018 Pasal 33 — Jaminan Pelaksanaan 5% nilai kontrak untuk "
                        "pengadaan barang/pekerjaan konstruksi/jasa lainnya > Rp200 juta "
                        "(dikecualikan antara lain jasa konsultansi & e-purchasing — auditor "
                        "konfirmasi jenis pengadaan).",
            "sebab": "Draf kontrak memakai template tanpa klausul jaminan, atau jaminan diserahkan "
                     "terpisah namun tidak dirujuk dalam kontrak.",
            "akibat": "K/L tidak memiliki jaminan finansial apabila penyedia wanprestasi; risiko "
                      "kesulitan pemulihan atas kerugian negara.",
        }
    )


def rule_pl1_bast_tidak_ditemukan(digest: dict) -> dict | None:
    """PL.1 — Kontrak jasa berjalan tapi BAST/rekonsiliasi tidak ada."""
    kontrak = _first(digest, "kontrak")
    bast = _first(digest, "ba_rekonsiliasi")
    pembayaran = _first(digest, "pembayaran_ls") or _first(digest, "sptb")
    if not kontrak:
        return None
    if bast:
        return None
    if not pembayaran:
        return None  # belum bayar, wajar BAST belum ada
    return _rule(
        "PL.1", PERINGATAN, "Pelaksanaan",
        "Pembayaran dilakukan namun BAST/BA Rekonsiliasi tidak ditemukan",
        "Dokumen BAST sebagai dasar pembayaran tidak tersedia di folder.",
        bukti={"pembayaran": pembayaran.get("filename") if pembayaran else None},
        draft={
            "kondisi": "Tim audit menemukan dokumen pembayaran (LS/SPTB), namun tidak ditemukan "
                       "BAST atau BA Rekonsiliasi sebagai dasar pembayaran.",
            "kriteria": "PMK 190/2012 tentang Pembayaran APBN — pembayaran atas jasa harus didukung "
                        "BAST/BA Rekonsiliasi; Perdirjen Perbendaharaan tentang mekanisme pembayaran.",
            "sebab": "BAST mungkin belum diterbitkan meskipun pembayaran sudah dilakukan; atau "
                     "dokumen BAST berada di folder lain yang tidak diinformasikan.",
            "akibat": "Pembayaran berisiko dikategorikan sebagai pembayaran tanpa dasar hukum; "
                      "berpotensi kerugian negara jika pekerjaan belum diselesaikan.",
        }
    )


def rule_pl2_pembayaran_tanpa_pemeriksaan(digest: dict) -> dict | None:
    """PL.2 — Pembayaran dilakukan tapi TIDAK ada dokumen pemeriksaan hasil pekerjaan.

    Pivot audit output-vs-kontrak: pemeriksaan oleh PPK/PPHP/PjPHP/tim teknis adalah
    verifikasi kuantitas & spesifikasi yang DITERIMA — dasar agar pembayaran sesuai
    output riil. Tanpa dokumen ini, kelebihan bayar atas output kurang (mis. kontrak
    20, diterima 18, dibayar penuh) lolos dari pengendalian. BAST saja tak cukup.
    """
    pembayaran = _first(digest, "pembayaran_ls") or _first(digest, "sptb")
    if not pembayaran:
        return None  # belum bayar — wajar belum ada pemeriksaan
    if _first(digest, "ba_pemeriksaan"):
        return None
    return _rule(
        "PL.2", KRITIS, "Pelaksanaan",
        "Pembayaran dilakukan tanpa dokumen pemeriksaan hasil pekerjaan (PPK/PPHP/tim teknis)",
        "Tidak ada dokumen pemeriksaan yang memverifikasi kuantitas & spesifikasi output yang diterima.",
        bukti={"pembayaran": pembayaran.get("filename")},
        draft={
            "kondisi": "Terdapat dokumen pembayaran, namun tidak ditemukan dokumen pemeriksaan/"
                       "penerimaan hasil pekerjaan (oleh PPK/PPHP/PjPHP/tim teknis) yang memverifikasi "
                       "kuantitas dan spesifikasi barang/jasa yang benar-benar diterima.",
            "kriteria": "Perpres 16/2018 Pasal 27 jo. Perlem LKPP 12/2021 — penerimaan hasil pekerjaan "
                        "didahului pemeriksaan kesesuaian kuantitas/spesifikasi/mutu terhadap kontrak; "
                        "PMK 190/2012 — pembayaran APBN atas prestasi yang telah diverifikasi.",
            "sebab": "[Auditor lengkapi] — pemeriksaan mungkin tidak didokumentasikan, atau dokumennya "
                     "berada di luar berkas yang diserahkan ke tim audit.",
            "akibat": "Pembayaran berisiko tidak sesuai output riil (dibayar penuh padahal kuantitas/"
                      "spesifikasi diterima kurang) tanpa terdeteksi — potensi kelebihan bayar & kerugian negara.",
        }
    )


def rule_pl3_pemeriksaan_tanpa_rincian(digest: dict) -> dict | None:
    """PL.3 — Dokumen pemeriksaan ADA tapi tanpa rincian kuantitas/spesifikasi (formalitas)."""
    pemeriksaan = _parsed(_first(digest, "ba_pemeriksaan"))
    if not pemeriksaan:
        return None
    if pemeriksaan.get("rincian_per_item"):
        return None
    return _rule(
        "PL.3", PERINGATAN, "Pelaksanaan",
        "Dokumen pemeriksaan hasil pekerjaan tanpa rincian kuantitas/spesifikasi",
        "Dokumen pemeriksaan tidak memuat rincian item yang diperiksa — indikasi pemeriksaan formalitas.",
        bukti={"pemeriksaan": pemeriksaan.get("nomor")},
        draft={
            "kondisi": "Dokumen pemeriksaan hasil pekerjaan ditemukan, namun tidak memuat rincian "
                       "kuantitas/spesifikasi per item yang diperiksa (hanya pernyataan/tanda tangan).",
            "kriteria": "Perpres 16/2018 Pasal 27 jo. Perlem LKPP 12/2021 — pemeriksaan hasil pekerjaan "
                        "wajib menguji kesesuaian kuantitas, spesifikasi, dan mutu terhadap kontrak.",
            "sebab": "[Auditor lengkapi] — pemeriksaan dilakukan administratif tanpa verifikasi fisik "
                     "per item, atau hasil verifikasi tidak dituangkan dalam berita acara.",
            "akibat": "Kekurangan kuantitas/penurunan spesifikasi dapat lolos tanpa terdeteksi; "
                      "pembayaran berpotensi tidak sesuai output yang benar-benar diterima.",
        }
    )


def rule_b1_pembayaran_tanpa_bukti_lengkap(digest: dict) -> dict | None:
    """B.1 — Pembayaran LS/SPTB tanpa kelengkapan bukti pendukung."""
    pembayaran = _parsed(_first(digest, "pembayaran_ls")) or _parsed(_first(digest, "sptb"))
    if not pembayaran:
        return None
    if pembayaran.get("bukti_pendukung_lengkap"):
        return None
    return _rule(
        "B.1", PERINGATAN, "Pembayaran",
        "Dokumen pembayaran tidak merujuk ke bukti pendukung (BAST/Invoice/Kwitansi)",
        "Teks dokumen pembayaran tidak menyebut BAST/BA/Invoice/Kwitansi sebagai bukti pendukung.",
        bukti={"pembayaran": pembayaran.get("nomor")},
        draft={
            "kondisi": "Dokumen pembayaran tidak memuat rujukan eksplisit ke BAST, Invoice, atau "
                       "Kwitansi sebagai bukti pendukung.",
            "kriteria": "PMK 190/2012 tentang Pembayaran APBN — pembayaran APBN harus didukung bukti "
                        "yang lengkap dan dapat diverifikasi.",
            "sebab": "Kelengkapan bukti pendukung tidak diperiksa saat penyusunan dokumen pembayaran, "
                     "atau rujukan bukti tidak eksplisit dalam teks dokumen.",
            "akibat": "Pembayaran berisiko tidak dapat dipertanggungjawabkan secara penuh; temuan "
                      "pemeriksaan BPK/BPKP atas kelengkapan bukti keuangan.",
        }
    )


def rule_d2_unclassified_banyak(digest: dict) -> dict | None:
    """D.2 — Banyak file di folder tidak terklasifikasi."""
    unc = digest.get("unclassified_files", [])
    if len(unc) < 5:
        return None
    return _rule(
        "D.2", INFO, "Dokumentasi",
        f"{len(unc)} file di folder penugasan tidak dikenali jenis dokumennya",
        "Banyak file belum terklasifikasi — perlu review manual.",
        bukti={"sample": unc[:8]},
        draft={
            "kondisi": f"Terdapat {len(unc)} file di folder penugasan yang tidak cocok dengan pola "
                       f"nama dokumen standar (KAK/HPS/Kontrak/BAST/Pembayaran).",
            "kriteria": "Standar pengarsipan dokumen pengadaan — penamaan file sesuai jenis dokumen.",
            "sebab": "Konvensi penamaan file belum seragam di tingkat unit kerja; atau file-file "
                     "tersebut adalah dokumen pendukung yang wajar (mis. notulen rapat, foto).",
            "akibat": "Kesulitan penelusuran dokumen saat reviu/audit; Claude tidak dapat melakukan "
                      "cross-check otomatis terhadap file yang tidak teridentifikasi.",
        }
    )


# ============================================================
# ENGINE
# ============================================================

_JUSTIFIKASI_LABEL = {
    "kebutuhan": "Kebutuhan (identifikasi kebutuhan/latar belakang)",
    "spesifikasi_teknis": "Spesifikasi teknis & fungsi",
    "metode_pengadaan": "Rencana cara/metode pengadaan",
    "waktu_penyelesaian": "Waktu penyelesaian pekerjaan",
    "output": "Output/keluaran yang diharapkan",
}


def rule_p5_kelengkapan_justifikasi(digest: dict) -> dict | None:
    """P.5 — Justifikasi/KAK belum memuat seluruh 5 elemen wajib dokumen persiapan.

    5 elemen (Perpres 16/2018 Ps. 11 & 18-19, Perlem LKPP 12/2021 Bab III):
    kebutuhan, spesifikasi teknis & fungsi, rencana metode pengadaan, waktu
    penyelesaian, output. Deteksi presence-only (heuristik keyword) →
    PERINGATAN; auditor wajib konfirmasi ke dokumen + isi Sebab substantif.
    """
    kak = _parsed(_first(digest, "kak"))
    if not kak:
        return None
    elemen = kak.get("elemen_justifikasi")
    if not isinstance(elemen, dict):
        return None
    missing = [_JUSTIFIKASI_LABEL[k] for k, v in elemen.items() if not v and k in _JUSTIFIKASI_LABEL]
    if not missing:
        return None
    return _rule(
        "P.5", PERINGATAN, "Perencanaan",
        f"Justifikasi/KAK belum memuat {len(missing)} dari 5 elemen wajib: {', '.join(missing)}",
        "Kelengkapan justifikasi (5 elemen dokumen persiapan) belum terpenuhi berdasarkan deteksi otomatis.",
        bukti={"elemen_terdeteksi": {k: v for k, v in elemen.items()}, "elemen_tidak_terdeteksi": missing},
        draft={
            "kondisi": (f"Dokumen perencanaan belum memuat/menyebut elemen justifikasi berikut: "
                        f"{', '.join(missing)}. (Deteksi otomatis — auditor wajib mengonfirmasi langsung "
                        f"ke dokumen sebelum menyimpulkan.)"),
            "kriteria": ("Perpres 16/2018 Pasal 11 & 18–19 jo. Perlem LKPP 12/2021 Bab III — dokumen persiapan/"
                         "KAK wajib memuat: identifikasi kebutuhan, spesifikasi teknis & fungsi, rencana cara/"
                         "metode pengadaan, waktu penyelesaian pekerjaan, dan output/keluaran yang diharapkan."),
            "sebab": "[Auditor lengkapi] — analisis mengapa elemen tidak tercantum (mis. KAK disusun terburu-buru, "
                     "ketidakpahaman PPK atas standar dokumen persiapan, atau template internal belum lengkap).",
            "akibat": ("Justifikasi tidak lengkap melemahkan dasar pengadaan: penyedia sulit memahami kebutuhan, "
                       "spesifikasi/penawaran berisiko tidak sesuai, dan pengendalian atas kewajaran pengadaan lemah."),
        }
    )


ALL_RULES = [
    rule_d1_dokumen_kunci_missing,
    rule_p1_hps_tanpa_pembentuk_harga,
    rule_p2_kak_hps_periode_beda,
    rule_p3_kak_hps_sla_beda,
    rule_p4_lingkup_kak_tak_di_hps,
    rule_p5_kelengkapan_justifikasi,
    rule_k1_nilai_kontrak_vs_hps,
    rule_k2_kontrak_tanpa_sla,
    rule_k3_kontrak_tanpa_jaminan,
    rule_pl1_bast_tidak_ditemukan,
    rule_pl2_pembayaran_tanpa_pemeriksaan,
    rule_pl3_pemeriksaan_tanpa_rincian,
    rule_b1_pembayaran_tanpa_bukti_lengkap,
    rule_d2_unclassified_banyak,
]


def run_checks(digest: dict) -> list[dict]:
    results = []
    for fn in ALL_RULES:
        try:
            r = fn(digest)
            if r:
                results.append(r)
        except Exception as e:
            results.append({"rule_id": fn.__name__, "severity": "ERROR", "error": str(e)})
    return results


def _self_check_ast() -> None:
    """Preflight: pastikan script ini sendiri syntactically valid sebelum run.
    Mencegah eksekusi dengan file korup (mis. akibat OneDrive sync artifact)."""
    import ast
    try:
        ast.parse(open(__file__, "r", encoding="utf-8").read())
    except SyntaxError as e:
        print(f"Self-check AST gagal di {__file__}: {e}", file=sys.stderr)
        print("   File mungkin korup. Lihat backup atau git restore.", file=sys.stderr)
        sys.exit(2)


def main(argv=None):
    _self_check_ast()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("digest_json", help="pengadaan-digest.json dari digest_pengadaan.py")
    ap.add_argument("-o", "--output", default="anomalies.json")
    args = ap.parse_args(argv)

    digest = json.loads(Path(args.digest_json).read_text(encoding="utf-8"))
    anomalies = run_checks(digest)

    out = {
        "metadata": {
            "digest_source": args.digest_json,
            "total_rules_tested": len(ALL_RULES),
            "total_anomalies_found": len(anomalies),
        },
        "summary_by_aspek": {},
        "summary_by_severity": {},
        "anomalies": anomalies,
    }
    for a in anomalies:
        out["summary_by_aspek"][a.get("aspek", "?")] = \
            out["summary_by_aspek"].get(a.get("aspek", "?"), 0) + 1
        out["summary_by_severity"][a.get("severity", "?")] = \
            out["summary_by_severity"].get(a.get("severity", "?"), 0) + 1

    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"=== CROSS-CHECK AUDIT-PENGADAAN ===")
    print(f"Tested: {len(ALL_RULES)} rules")
    print(f"Found: {len(anomalies)} anomalies")
    print(f"By Aspek: {out['summary_by_aspek']}")
    print(f"By Severity: {out['summary_by_severity']}")
    print()
    for a in anomalies:
        print(f"  [{a.get('severity', '?'):11s}] {a.get('rule_id', '?'):6s} ({a.get('aspek', '?')}) -- {a.get('judul', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
