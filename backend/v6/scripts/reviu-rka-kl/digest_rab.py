"""
digest_rab.py — Parser RAB RKA-K/L → JSON terstruktur.

Usage:
    python digest_rab.py <path-to-rab.pdf> [-o output.json]

Output schema:
    {
      "metadata": {...},
      "identitas_ro": {...},
      "total_pagu": int,
      "komponen": [
        { "kode": "7444.QDC.001.051", "nama": "Persiapan...", "total": 2000000000,
          "sumber_dana": "PNBP", "akun": [
            { "kode_akun": "521211", "nama_akun": "BELANJA BAHAN", "total": 82517200,
              "rincian": [
                {"deskripsi": "ATK", "volume": 8, "satuan": "PKT",
                 "harga_satuan": 1589650, "total": 12717200},
                ...
              ]
            }, ...
          ]
        }, ...
      ],
      "raw_text_pages": [...]
    }

Catatan: RAB dari SAKTI/Excel → PDF sering mengalami corruption kolom
(angka dengan trailing dash). Parser ini best-effort.
"""

from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _parse_number(s: str) -> int | None:
    """Parse '1,589,650' or '1,589,650-' or '625,000,000' → int."""
    if s is None:
        return None
    s = s.strip().rstrip("-").strip()
    s = s.replace(",", "").replace(".", "")
    if not s or not re.fullmatch(r"-?\d+", s):
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _pdftotext_pages(path: str | Path) -> list[str]:
    """Extract text per halaman pakai pdftotext -layout. Lebih cepat & robust dari pdfplumber.

    Fallback ke pdfplumber jika pdftotext tidak tersedia.
    """
    if not shutil.which("pdftotext"):
        # Fallback: pdfplumber legacy path
        try:
            import pdfplumber
        except ImportError:
            sys.exit("ERROR: pdftotext tidak tersedia di PATH dan pdfplumber tidak terinstall. "
                     "Install poppler-utils (Linux/macOS) atau pip install pdfplumber.")
        with pdfplumber.open(str(path)) as pdf:
            return [(p.extract_text() or "") for p in pdf.pages]
    # pdftotext -layout: page break sebagai \f (form feed)
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True, text=True, timeout=120,
        encoding="utf-8", errors="replace",
    )
    full = result.stdout or ""
    # Split per halaman by form feed
    pages = full.split("\f")
    # pdftotext biasanya append empty page di akhir — drop kalau kosong
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def _office_docx_pages(path) -> list[str]:
    try:
        import docx
        d = docx.Document(str(path))
    except Exception:  # noqa: BLE001
        return []
    parts = [p.text for p in d.paragraphs if p.text and p.text.strip()]
    for t in getattr(d, "tables", []):
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells if c.text and c.text.strip()]
            if cells:
                parts.append(" | ".join(cells))
    txt = "\n".join(parts).strip()
    return [txt] if txt else []


def _office_xlsx_pages(path) -> list[str]:
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    except Exception:  # noqa: BLE001
        return []
    pages = []
    for ws in wb.worksheets:
        rows = []
        for row in ws.iter_rows(values_only=True):
            cells = [str(c) for c in row if c is not None and str(c).strip() != ""]
            if cells:
                # TAB (bukan " | ") supaya baris komponen SAKTI tetap cocok dengan
                # regex parser yang berbasis whitespace (mis. `051  Nama  1,500,000`).
                rows.append("\t".join(cells))
        if rows:
            pages.append(f"[Sheet: {ws.title}]\n" + "\n".join(rows))
    try:
        wb.close()
    except Exception:  # noqa: BLE001
        pass
    return pages


def _extract_pages(pdf_path: Path) -> list[str]:
    """Return list of page texts. PDF → pdftotext; Word/.docx & Excel/.xlsx →
    ekstraktor Office (agar RAB dalam Word/Excel juga diterima)."""
    suf = Path(pdf_path).suffix.lower()
    if suf == ".docx":
        return _office_docx_pages(pdf_path)
    if suf in (".xlsx", ".xlsm"):
        return _office_xlsx_pages(pdf_path)
    return _pdftotext_pages(pdf_path)


def parse_identitas(pages: list[str]) -> dict:
    head = "\n".join(pages[:2])
    out = {}
    patterns = {
        "kementerian": r"Kementerian\s+Negara\s*/\s*Lembaga\s*:\s*(.+?)(?=\n)",
        "unit_eselon": r"Unit\s+Eselon\s+I\s*/\s*II\s*:?\s*(.+?)(?=\n)",
        "program": r"^Program\s*:\s*(.+?)(?=\n)",
        "sasaran_program": r"Sasaran\s+Program\s*:\s*(.+?)(?=\n)",
        "ikp": r"Indikator\s+Kinerja\s+Program\s*:\s*(.+?)(?=\n)",
        "kegiatan": r"^Kegiatan\s*:\s*(.+?)(?=\n)",
        "sasaran_kegiatan": r"Sasaran\s+Kegiatan\s*:?\s*(.+?)(?=\n)",
        "ikk": r"Indikator\s+Kinerja\s+Kegiatan\s*:?\s*(.+?)(?=\n)",
        "kro": r"Klasifikasi\s+Rincian\s+Output\s*\(?KRO\)?\s*:\s*(.+?)(?=\n)",
        "ikro": r"Indikator\s+Klasifikasi\s+Rincian\s+Output\s*\(?IKRO\)?\s*:?\s*(.+?)(?=\n)",
        "ro": r"^Rincian\s+Output\s*:\s*(.+?)(?=\n)",
        "iro": r"Indikator\s+Rincian\s+Output\s*\(?IRO\)?\s*:?\s*(.+?)(?=\n)",
        "volume": r"Volume\s*:\s*(.+?)(?=\n)",
        "satuan": r"Satuan\s+Ukur\s*:\s*(.+?)(?=\n)",
        "alokasi_dana": r"Alokasi\s+Dana\s*:\s*Rp\s*([\d\.,]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, head, re.M)
        if m:
            val = m.group(1).strip()
            if key == "alokasi_dana":
                out[key] = _parse_number(val)
            elif key == "volume":
                vm = re.search(r"(\d+)", val)
                out[key] = int(vm.group(1)) if vm else val
            else:
                out[key] = val
        else:
            out[key] = None
    return out


# --- Format SAKTI riil (RKA-K/L cetak DJA/SAKTI) ---
# Output header 6-segmen: "059.GK.7443.01.QDJ.001 STARTUP DIGITAL ... 54,450,000,000"
_OUTPUT_HEADER_RE = re.compile(
    r"^(\d{3}\.[A-Z]{2}\.\d{4}\.\d{2}\.[A-Z]{3}\.\d{3})\s+(.+?)\s+(\d{1,3}(?:,\d{3})+)\s*$",
    re.M,
)
# Komponen 3-digit telanjang: "051 Inkubasi Startup Digital 25,496,236,000"
_SAKTI_KOMP_RE = re.compile(r"^(\d{3})\s+([A-Za-z][^\n]*?)\s+(\d{1,3}(?:,\d{3})+)\s*$", re.M)
# Akun 6-digit: "521211 Belanja Bahan 351,122,000" (opsional prefix PNBP)
_SAKTI_AKUN_RE = re.compile(
    r"^(?:PNBP\s+)?(\d{6})\s+([Bb]elanja\s+[A-Za-z ]+?)\s+(\d{1,3}(?:,\d{3})+)\s*(?:-)?\s*$",
    re.M,
)
# Rincian: deskripsi diakhiri "<volume> <harga_satuan> <total> [referensi]"
_SAKTI_RINCIAN_RE = re.compile(
    r"^(.+?)\s+(\d+)\s+(\d{1,3}(?:,\d{3})+)\s+(\d{1,3}(?:,\d{3})+)(?:\s+referensi)?\s*$",
    re.M,
)


def _output_total(full_text: str) -> int | None:
    """Total pagu dari baris output header SAKTI (6-segmen dotted)."""
    m = _OUTPUT_HEADER_RE.search(full_text)
    return _parse_number(m.group(3)) if m else None


def _parse_komponen_sakti(full_text: str) -> list[dict]:
    """Fallback parser untuk format RAB SAKTI riil (komponen 3-digit telanjang).

    Dipakai bila komp_pattern format demo (kode dotted 4-segmen) tidak match.
    Menghasilkan skema yang sama: komponen → akun → rincian.
    """
    heads = list(_SAKTI_KOMP_RE.finditer(full_text))
    components: list[dict] = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(full_text)
        seg = full_text[start:end]
        akun_matches = list(_SAKTI_AKUN_RE.finditer(seg))
        akun_list = []
        for j, am in enumerate(akun_matches):
            ak_start = am.end()
            ak_end = akun_matches[j + 1].start() if j + 1 < len(akun_matches) else len(seg)
            ak_seg = seg[ak_start:ak_end]
            rincian_lines = []
            for rm in _SAKTI_RINCIAN_RE.finditer(ak_seg):
                harga = _parse_number(rm.group(3))
                tot = _parse_number(rm.group(4))
                if harga is None or tot is None:
                    continue
                rincian_lines.append({
                    "deskripsi": rm.group(1).strip().rstrip("-").strip(),
                    "volume": int(rm.group(2)),
                    "satuan": None,  # satuan majemuk SAKTI tetap di deskripsi
                    "harga_satuan": harga,
                    "total": tot,
                })
            akun_list.append({
                "kode_akun": am.group(1),
                "nama_akun": am.group(2).strip(),
                "total": _parse_number(am.group(3)),
                "rincian": rincian_lines,
                "jumlah_rincian": len(rincian_lines),
            })
        components.append({
            "kode": m.group(1),
            "nama": m.group(2).strip(),
            "total": _parse_number(m.group(3)),
            "akun": akun_list,
            "jumlah_akun": len(akun_list),
        })
    return components


def parse_komponen(pages: list[str]) -> list[dict]:
    """Parse struktur komponen → akun → rincian dari teks RAB.

    Dua format didukung: (1) demo/lama kode dotted 4-segmen `7444.QDC.001.051`;
    (2) SAKTI riil komponen 3-digit telanjang `051 Nama ...` — dipakai sebagai
    fallback bila format (1) tidak menghasilkan komponen.
    """
    full_text = "\n".join(pages)

    # Komponen header pattern: "7444.QDC.001.051 Nama Komponen  2,000,000,000"
    # v0.2: total dipastikan di posisi akhir baris. PDF extract sering menggabung
    # nama dan akun pertama di baris berikutnya — kita ambil angka terakhir
    # sebelum newline dengan format "X,XXX,XXX,XXX" (≥3 digit grup).
    komp_pattern = re.compile(
        r"(\d{4}\.[A-Z]+\.\d{3}\.\d{3})\s*(.+?)\s+(\d{1,3}(?:,\d{3}){2,})\s*$",
        re.M
    )

    # Temukan semua komponen + rentang posisi teksnya
    komp_matches = list(komp_pattern.finditer(full_text))
    components = []
    for i, m in enumerate(komp_matches):
        start = m.end()
        end = komp_matches[i + 1].start() if i + 1 < len(komp_matches) else len(full_text)
        segment = full_text[start:end]
        total = _parse_number(m.group(3))

        # Akun: 6-digit yang dikuti BELANJA ... dan total.
        # Pola: optional "PNBP " + 521211 + BELANJA BAHAN + total
        akun_pattern = re.compile(
            r"(?:PNBP\s+)?(\d{6})\s+(BELANJA\s+[A-Z][A-Za-z\s]*?)\s+([\d,\.]+)\s*(?:-)?\s*$",
            re.M
        )
        akun_matches = list(akun_pattern.finditer(segment))
        # Fallback: akun dengan case-insensitive "Belanja"
        if not akun_matches:
            akun_pattern_alt = re.compile(
                r"(?:PNBP\s+)?(\d{6})\s+([Bb]elanja\s+[A-Za-z\s]+?)\s+([\d,\.]+)\s*(?:-)?\s*$",
                re.M
            )
            akun_matches = list(akun_pattern_alt.finditer(segment))

        akun_list = []
        for j, am in enumerate(akun_matches):
            ak_start = am.end()
            ak_end = akun_matches[j + 1].start() if j + 1 < len(akun_matches) else len(segment)
            ak_seg = segment[ak_start:ak_end]
            akun_nama_raw = am.group(2) if len(am.groups()) >= 2 else ""
            akun_total_raw = am.group(3) if len(am.groups()) >= 3 else None

            # Rincian: baris dengan pola "deskripsi ... volume SATUAN harga_sat total"
            # Pola satuan umum: OH, OJ, OK, OP, ORG, PKT, KEG, HR, BLN, Unit, PCS, Kali
            rincian_lines = []
            for rm in re.finditer(
                r"^(.+?)\s+(\d+)\s+(OH|OJ|OK|OP|ORG|PKT|KEG|HR|BLN|[Uu]nit|PCS|Kali|KALI|[Kk]eg)\s+([\d,\.]+)\s+([\d,\.]+)(?:-)?\s*$",
                ak_seg, re.M
            ):
                desc = rm.group(1).strip().rstrip("-").strip()
                volume = int(rm.group(2))
                satuan = rm.group(3)
                harga = _parse_number(rm.group(4))
                total = _parse_number(rm.group(5))
                rincian_lines.append({
                    "deskripsi": desc,
                    "volume": volume,
                    "satuan": satuan,
                    "harga_satuan": harga,
                    "total": total,
                })

            akun_list.append({
                "kode_akun": am.group(1),
                "nama_akun": akun_nama_raw.strip() if akun_nama_raw else None,
                "total": _parse_number(akun_total_raw) if akun_total_raw else None,
                "rincian": rincian_lines,
                "jumlah_rincian": len(rincian_lines),
            })

        components.append({
            "kode": m.group(1),
            "nama": m.group(2).strip(),
            "total": total,
            "akun": akun_list,
            "jumlah_akun": len(akun_list),
        })

    # Fallback: format SAKTI riil (komponen 3-digit telanjang) bila format demo nihil.
    if not components:
        components = _parse_komponen_sakti(full_text)

    return components


def enumerate_keywords(komponen: list[dict], keyword_re: str) -> list[dict]:
    """Return list of rincian items whose deskripsi matches keyword regex."""
    out = []
    for k in komponen:
        for a in k.get("akun", []):
            for r in a.get("rincian", []):
                if re.search(keyword_re, r.get("deskripsi", ""), re.I):
                    out.append({
                        "komponen": k["kode"],
                        "akun": a["kode_akun"],
                        "nama_akun": a.get("nama_akun"),
                        "deskripsi": r["deskripsi"],
                        "volume": r["volume"],
                        "satuan": r["satuan"],
                        "harga_satuan": r["harga_satuan"],
                        "total": r["total"],
                    })
    return out


def digest_rab(pdf_path: str | Path) -> dict:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    pages = _extract_pages(pdf_path)
    identitas = parse_identitas(pages)
    komponen = parse_komponen(pages)

    # total_pagu: prioritas alokasi_dana identitas → total baris output header SAKTI
    # → jumlah total komponen. Header SAKTI dipakai agar RAB riil (yang tak punya
    # baris "Alokasi Dana") tetap punya total_pagu benar, bukan 0.
    total_pagu = (
        identitas.get("alokasi_dana")
        or _output_total("\n".join(pages))
        or sum((k.get("total") or 0) for k in komponen)
    )

    # Pre-computed indices untuk cross-check
    indices = {
        "sewa_iot_items": enumerate_keywords(komponen, r"sewa\s+(perangkat|sensor)\s*IoT|sewa\s+alat|sensor\s+IoT|perangkat\s+IoT"),
        "sewa_kendaraan_items": enumerate_keywords(komponen, r"sewa\s+kendaraan"),
        "menteri_dirjen_items": enumerate_keywords(komponen, r"\b(Menteri|Dirjen|Direktur\s+Jenderal)\b"),
        "konstruksi_items": enumerate_keywords(komponen, r"konstruksi|properti\s+panggung"),
        "tenaga_ahli_items": enumerate_keywords(komponen, r"tenaga\s+ahli"),
        "honor_output_items": enumerate_keywords(komponen, r"honor(?:arium)?\s+(pengarah|penanggung|ketua|wakil|sekretaris|anggota)"),
    }

    return {
        "metadata": {
            "source_file": pdf_path.name,
            "jenis_dokumen": "RAB",
            "total_pages": len(pages),
        },
        "identitas_ro": identitas,
        "total_pagu": total_pagu,
        "komponen": komponen,
        "indices": indices,
        "raw_text_pages": pages,
    }


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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="Path file RAB PDF")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--no-raw", action="store_true")
    args = ap.parse_args(argv)

    out = digest_rab(args.pdf)
    if args.no_raw:
        out.pop("raw_text_pages", None)

    out_path = args.output or str(Path(args.pdf).with_suffix(".rab.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"OK — written: {out_path}")
    print(f"   Identitas RO: {out['identitas_ro'].get('ro')}")
    print(f"   Total pagu: {out['total_pagu']:,}")
    print(f"   Komponen terdeteksi: {len(out['komponen'])}")
    for k in out["komponen"]:
        print(f"     - {k['kode']} {k['nama'][:50]} = Rp {(k['total'] or 0):,} ({k['jumlah_akun']} akun)")
    print(f"   Sewa IoT items: {len(out['indices']['sewa_iot_items'])}")
    print(f"   Sewa Kendaraan items: {len(out['indices']['sewa_kendaraan_items'])}")
    print(f"   Konstruksi/Properti items: {len(out['indices']['konstruksi_items'])}")
    print(f"   Tenaga Ahli items: {len(out['indices']['tenaga_ahli_items'])}")
    print(f"   Items Menteri/Dirjen: {len(out['indices']['menteri_dirjen_items'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
