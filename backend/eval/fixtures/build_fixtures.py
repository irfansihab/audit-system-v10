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


SCENARIOS = {"reviu-umum": scenario_reviu_umum}


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
