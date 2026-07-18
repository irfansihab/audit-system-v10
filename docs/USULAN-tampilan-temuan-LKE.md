# USULAN — Tampilan Temuan untuk Penugasan Evaluasi ber-LKE

Status: **USULAN (belum dieksekusi — menunggu persetujuan)**
Skill terdampak: `evaluasi-spip`, `evaluasi-sakip`, `evaluasi-reformasi-birokrasi` (rezim LKE).

## Masalah

Penugasan LKE menghasilkan **dua** artefak yang berbeda sifat dari temuan KKSA biasa:
1. **Rekap Penilaian LKE** — skor & predikat per komponen/unsur: `nilai_pm` (penilaian mandiri auditee) vs `nilai_apip` (penjaminan APIP), bobot, predikat, + total & predikat akhir. Disimpan di `_KKP/penilaian-lke-<skill>.json`.
2. **Area of Improvement (AoI)** — catatan perbaikan per unsur, **tanpa** struktur K/K/S/A dan **tanpa** Sebab (bukan temuan audit). Disimpan sebagai `temuan` biasa (dengan `sebab` kosong).

**KKP (.docx)** sudah benar: `render_lke_recap` menampilkan tabel "REKAP PENILAIAN (LKE)" lalu daftar AoI.

**Tetapi di UI** (`TemuanReviewPanel` / tahap KKP): item ditampilkan sebagai **kartu KKSA generik** (Judul · Kondisi · Kriteria · Akibat). Untuk LKE ini keliru:
- Skor/predikat per unsur (inti hasil LKE) **tidak muncul sama sekali** di UI.
- AoI dipaksa masuk format Kondisi/Kriteria/Akibat → kolom Sebab kosong, "Kriteria" janggal, seolah temuan audit.

## Usulan

**Deteksi rezim LKE di UI** (skill ∈ `_LKE_SKILLS`) → ganti tampilan panel jadi 2 bagian:

### Bagian 1 — Rekap Penilaian LKE (BARU, read-only)
Tabel: `Komponen/Unsur | Bobot | Nilai PM | Nilai APIP | Δ | Predikat`, plus baris total & **Predikat Akhir** (badge warna: mis. hijau "Baik", kuning "Cukup", merah "Kurang"). Kolom Δ (selisih PM−APIP) menyorot di mana auditee menilai lebih tinggi dari APIP.
- Sumber: endpoint baru `GET /penugasan/{id}/penilaian-lke` yang membaca `_KKP/penilaian-lke-<skill>.json`.

### Bagian 2 — Area of Improvement (AoI)
Daftar kartu AoI per unsur: `Unsur (sasaran_id) · Kondisi/observasi · Rekomendasi perbaikan`. **Tanpa** kolom Kriteria/Sebab/Akibat KKSA. Label "Temuan" → "Area of Improvement". HITL (setujui/tolak/edit) tetap ada, tapi form edit menyesuaikan field LKE (observasi + rekomendasi), bukan K/K/S/A.

### Pembeda perilaku
- Skill KKSA (audit/reviu/pemantauan) → panel seperti sekarang (tak berubah).
- Skill LKE → tampilan 2-bagian di atas.
- Deteksi via `skill` penugasan (sudah tersedia di frontend).

## Lingkup pekerjaan (estimasi)
| Bagian | Perubahan |
|---|---|
| Backend | 1 endpoint `GET /penugasan/{id}/penilaian-lke` (baca JSON rekap). Kecil. |
| Frontend | Cabang render di `TemuanReviewPanel` untuk LKE: komponen tabel rekap + daftar AoI; sesuaikan form edit. Sedang. |
| Doktrin agen | Tidak berubah (agen sudah memisahkan rekap vs AoI). |
| KKP docx | Tidak berubah (sudah benar). |

## Keputusan yang diminta
1. Setuju arah 2-bagian (Rekap LKE + AoI) di UI? 
2. Predikat akhir perlu badge warna berambang (mis. ambang SPIP level 1–5 / SAKIP AA–D)? Bila ya, mohon ambang/mapping warnanya (atau saya pakai netс abu-abu dulu).
3. Untuk **reviu-pipk** (bukan di `_LKE_SKILLS` tapi juga ber-nuansa penilaian efektivitas): ikut pola LKE atau tetap KKSA? (perlu konfirmasi Anda).

> Setelah Anda setujui, saya eksekusi: endpoint + cabang UI + form edit LKE + verifikasi render.
