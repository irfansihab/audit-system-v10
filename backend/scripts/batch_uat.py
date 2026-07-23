#!/usr/bin/env python3
"""Batch UAT harness — uji banyak skill sekaligus.

AUDITOR cukup menyiapkan DOKUMEN; script ini mengerjakan sisanya:
buat penugasan (PT) -> isi KP + sasaran/PKP (PT) -> upload dokumen (AT) ->
ingestion otomatis -> (opsional) jalankan agen analisis -> rekap hasil.

INTAKE (folder yang Anda siapkan):
  backend/data/uji-batch/
    <skill>__<objek bebas>/          # nama folder = skill + '__' + objek
        dokumen1.pdf                 # nama file jelas (KAK/HPS/TOR/RAB/LKE/...)
        dokumen2.xlsx
        [sasaran.txt]                # opsional: 1 sasaran per baris
        [bukti/ ...]                 # opsional (skill LKE): folder bukti dukung
  ATAU sediakan manifest.json (lihat --template).

MODE:
  python scripts/batch_uat.py scaffold   # buat penugasan + upload + ingest (cepat)
  python scripts/batch_uat.py run        # jalankan agen analisis (LAMBAT, per skill)
  python scripts/batch_uat.py report     # rekap temuan/aspek/LKE + cakupan
  python scripts/batch_uat.py clean      # hapus semua penugasan batch
  python scripts/batch_uat.py template   # tulis skeleton intake + manifest contoh
"""
from __future__ import annotations

import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

BASE = "http://localhost:8000"
ROOT = Path(__file__).resolve().parents[1]          # backend/
INTAKE = ROOT / "data" / "uji-batch"
STATE = INTAKE / ".batch-state.json"                # id penugasan yang dibuat batch
KODE_TAG = "uatbatch"                                # penanda di objek utk clean

TIM_KT = "Budi Santoso"
TIM_AT = "Sari Wijaya"


# ---------- HTTP ----------
def _call(method, path, token=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def _upload(token, penugasan_id, filepath: Path, jenis: str | None = None):
    """Multipart POST /dokumen (stdlib, tanpa requests)."""
    boundary = "----batchuat" + uuid.uuid4().hex
    ctype = mimetypes.guess_type(filepath.name)[0] or "application/octet-stream"
    parts: list[bytes] = []

    def field(name, value):
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())

    field("penugasan_id", str(penugasan_id))
    if jenis:
        field("jenis", jenis)
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filepath.name}\"\r\n"
        f"Content-Type: {ctype}\r\n\r\n".encode()
    )
    parts.append(filepath.read_bytes())
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    payload = b"".join(parts)

    req = urllib.request.Request(BASE + "/dokumen", data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def _login(role):
    st, res = _call("POST", "/auth/login", body={"role": role})
    assert st == 200, f"login {role} gagal: {res}"
    return res["token"]


# ---------- intake ----------
def _valid_skills() -> set[str]:
    sk = ROOT.parent / "knowledge" / "skills"
    return {p.name for p in sk.iterdir()
            if p.is_dir() and (p / "SKILL.md").exists()}


def _discover_tests() -> list[dict]:
    """Baca manifest.json bila ada; else derive dari subfolder <skill>__<objek>."""
    mf = INTAKE / "manifest.json"
    if mf.exists():
        data = json.loads(mf.read_text(encoding="utf-8"))
        return data.get("tests", [])
    skills = _valid_skills()
    tests = []
    if not INTAKE.exists():
        return tests
    for d in sorted(INTAKE.iterdir()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        if "__" not in d.name:
            continue
        skill, objek = d.name.split("__", 1)
        skill = skill.strip()
        if skill not in skills:
            print(f"  ! lewati '{d.name}': skill '{skill}' tak dikenal")
            continue
        files = [p for p in sorted(d.iterdir())
                 if p.is_file() and p.name not in ("sasaran.txt",) and not p.name.startswith(".")]
        # bukti/ (LKE) — sertakan rekursif
        bukti = d / "bukti"
        if bukti.is_dir():
            files += [p for p in sorted(bukti.rglob("*")) if p.is_file()]
        sasaran = []
        sf = d / "sasaran.txt"
        if sf.exists():
            sasaran = [ln.strip() for ln in sf.read_text(encoding="utf-8").splitlines() if ln.strip()]
        tests.append({"skill": skill, "objek": objek.replace("_", " ").strip(),
                      "folder": str(d), "files": [str(f) for f in files], "sasaran": sasaran})
    return tests


def _kp_md(objek, skill, sasaran):
    rows = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sasaran))
    return (f"# KARTU PENUGASAN\n\n**Judul**: Uji {skill} — {objek}\n"
            f"**Obyek**: {objek}\n**Jenis**: {skill}\n"
            f"**Dasar**: PKPT UAT batch\n\n## Sasaran Pengawasan\n{rows}\n")


def _load_state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def _save_state(s):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2))


# ---------- MODE: scaffold ----------
def scaffold():
    tests = _discover_tests()
    if not tests:
        print("Tidak ada test di intake. Jalankan: python scripts/batch_uat.py template")
        return
    pt = _login("PT")
    at = _login("AT")
    state = _load_state()
    print(f"Scaffold {len(tests)} penugasan uji...\n")
    for t in tests:
        skill, objek = t["skill"], t["objek"]
        sasaran = t.get("sasaran") or [f"Memastikan kesesuaian/kememadaian {objek} terhadap kriteria {skill}"]
        st, p = _call("POST", "/penugasan", pt, {"obyek": f"[{KODE_TAG}] {objek}", "skill": skill})
        if st != 201:
            print(f"  ✗ {skill}: create gagal — {p}")
            continue
        pid, kode = p["id"], p["kode"]
        _call("PUT", f"/penugasan/{pid}/kp-md", pt,
              {"content": _kp_md(objek, skill, sasaran), "sasaran": sasaran})
        n_ok = 0
        for fp in t.get("files", []):
            us, _ = _upload(at, pid, Path(fp))
            n_ok += 1 if us == 201 else 0
        state[str(pid)] = {"skill": skill, "objek": objek, "kode": kode, "n_files": n_ok}
        _save_state(state)
        print(f"  ✓ #{pid} {skill:<26} {n_ok} dok  · {objek[:40]}")
    print(f"\n{len(state)} penugasan siap. Tunggu ingestion selesai, lalu:  "
          f"python scripts/batch_uat.py run")


# ---------- MODE: run ----------
def _stream_run(token, pid, skill):
    prompt = (f"Mulai analisis {skill} untuk penugasan ini: susun konteks dari dokumen "
              f"yang diupload lalu lakukan analisis dan susun KKP.")
    url = (f"{BASE}/agen/anggota_tim/stream?penugasan_id={pid}"
           f"&prompt={urllib.parse.quote(prompt)}")
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            for raw in r:
                line = raw.decode("utf-8", "ignore").strip()
                if line.startswith("event:") and "done" in line:
                    return True, time.time() - t0
                if line.startswith("event:") and "error" in line:
                    return False, time.time() - t0
    except Exception as e:  # noqa: BLE001
        return None, f"{e}"
    return True, time.time() - t0


def run():
    state = _load_state()
    if not state:
        print("Belum ada penugasan. Jalankan 'scaffold' dulu.")
        return
    at = _login("AT")
    print(f"Menjalankan agen untuk {len(state)} penugasan (berurutan; tiap run ±10–15 mnt)...\n")
    for pid, info in state.items():
        print(f"  ▶ #{pid} {info['skill']} — mulai {time.strftime('%H:%M')}...", flush=True)
        ok, dt = _stream_run(at, pid, info["skill"])
        tag = "✓ selesai" if ok else ("✗ gagal" if ok is False else "? putus")
        dur = f"{dt:.0f}s" if isinstance(dt, float) else dt
        print(f"     {tag} ({dur})")
    print("\nSelesai. Rekap:  python scripts/batch_uat.py report")


# ---------- MODE: report ----------
def report():
    state = _load_state()
    if not state:
        print("Belum ada penugasan batch.")
        return
    tok = _login("PT")
    print(f"{'#id':<5}{'skill':<26}{'temuan':>7}{'aspek':>7}{'LKE':>5}  status")
    for pid, info in state.items():
        folder = ROOT.parent
        st, p = _call("GET", f"/penugasan/{pid}", tok)
        status_s = p.get("status", "?") if isinstance(p, dict) else "?"
        # baca artefak dari disk
        base = None
        st2, dl = _call("GET", "/penugasan", tok)
        # cari folder via kode
        pk = info["kode"]
        from glob import glob
        cand = glob(str(ROOT / "data" / "penugasan" / f"*{pk.split('-')[-1]}*"))
        n_tem = n_asp = n_lke = 0
        if cand:
            kkp = Path(cand[0]) / "_KKP"
            tj = kkp / "temuan.json"
            if tj.exists():
                try: n_tem = len(json.loads(tj.read_text()).get("temuan", []))
                except Exception: pass
            aj = kkp / "penilaian-aspek.json"
            if aj.exists():
                try: n_asp = len(json.loads(aj.read_text()).get("aspek", []))
                except Exception: pass
            for lk in kkp.glob("penilaian-lke-*.json"):
                try: n_lke += len(json.loads(lk.read_text()).get("komponen", []))
                except Exception: pass
        print(f"{pid:<5}{info['skill']:<26}{n_tem:>7}{n_asp:>7}{n_lke:>5}  {status_s}")


# ---------- MODE: clean ----------
def clean():
    state = _load_state()
    tok = _login("PT")
    st, plist = _call("GET", "/penugasan", tok)
    n = 0
    ids = set(state.keys())
    if st == 200 and isinstance(plist, list):
        for p in plist:
            if str(p["id"]) in ids or f"[{KODE_TAG}]" in (p.get("obyek") or ""):
                _call("DELETE", f"/penugasan/{p['id']}", tok)
                n += 1
                print(f"  hapus #{p['id']} {p.get('obyek','')[:40]}")
    if STATE.exists():
        STATE.unlink()
    print(f"{n} penugasan batch dihapus.")


# ---------- MODE: template ----------
def template():
    INTAKE.mkdir(parents=True, exist_ok=True)
    (INTAKE / "README.txt").write_text(
        "INTAKE UJI BATCH — cukup taruh dokumen di sini.\n\n"
        "1. Buat 1 subfolder per skill yang diuji, beri nama:  <skill>__<objek>\n"
        "   contoh:  reviu-pengadaan__Pengadaan CCTV TA2026\n"
        "2. Taruh dokumen di dalamnya (nama file jelas: KAK/HPS/TOR/RAB/LKE/dst).\n"
        "   - RKA: TOR & RAB (PDF/Word/Excel), beri penanda RO konsisten:\n"
        "       RO1-TOR-....pdf  RO1-RAB-....xlsx  RO2-TOR-....docx ...\n"
        "   - LKE (spip/sakip/rb/pipk): taruh file LKE .xlsx + folder 'bukti/'.\n"
        "3. (opsional) sasaran.txt — 1 sasaran per baris.\n\n"
        "Skill valid: " + ", ".join(sorted(_valid_skills())) + "\n\n"
        "Lalu beri tahu saya, atau jalankan sendiri:\n"
        "  python scripts/batch_uat.py scaffold   (buat penugasan + upload + ingest)\n"
        "  python scripts/batch_uat.py run        (jalankan agen analisis)\n"
        "  python scripts/batch_uat.py report     (rekap hasil)\n"
        "  python scripts/batch_uat.py clean      (hapus semua penugasan batch)\n",
        encoding="utf-8",
    )
    ex = INTAKE / "reviu-pengadaan__CONTOH Pengadaan CCTV TA2026"
    ex.mkdir(exist_ok=True)
    (ex / "TARUH-DOKUMEN-DI-SINI.txt").write_text(
        "Hapus file ini, taruh KAK/HPS/RAB pengadaan di folder ini.\n", encoding="utf-8")
    manifest = {
        "tim": {"kt": TIM_KT, "at": [TIM_AT]},
        "catatan": "Opsional. Bila tidak ada manifest.json, test diturunkan dari nama subfolder <skill>__<objek>.",
        "tests": [
            {"skill": "reviu-pengadaan", "objek": "Pengadaan CCTV TA2026",
             "folder": "reviu-pengadaan__CONTOH Pengadaan CCTV TA2026",
             "sasaran": ["Memastikan kelengkapan & kesesuaian dokumen perencanaan pengadaan"]},
        ],
    }
    (INTAKE / "manifest.template.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Skeleton intake dibuat di: {INTAKE}")
    print("  - README.txt, manifest.template.json, + folder contoh")


MODES = {"scaffold": scaffold, "run": run, "report": report, "clean": clean, "template": template}

if __name__ == "__main__":
    import urllib.parse  # noqa: F401 (dipakai di _stream_run)
    mode = sys.argv[1] if len(sys.argv) > 1 else "template"
    fn = MODES.get(mode)
    if not fn:
        print(f"mode tak dikenal: {mode}. Pilih: {', '.join(MODES)}")
        sys.exit(1)
    fn()
