# Template Skill "Engine-Ready" (P1a)

Acuan menyeragamkan 18 SKILL.md jadi **substansi murni & portabel**. Pilot: `reviu-pengadaan` (commit P1a). Orkestrasi tidak dihapus dari sistem — **direlokasi** ke orkestrator (harness uji: `backend/app/prompts/anggota_tim.md` / `ketua_tim.md`; produksi: INTEGRAL).

## Prinsip pemisah
- **Skill menjawab "APA" + "FORMAT"** — lingkup, kriteria/aspek, checklist substantif, format unsur (KKSAR/LKE/memo), struktur laporan.
- **Orkestrator menjawab "BAGAIMANA/SIAPA/KAPAN"** — urutan tool, peran AT/KT/PM, titik HITL, auto-eksekusi, pilihan model, UI/endpoint.

## Yang DICABUT dari SKILL.md
1. Frontmatter: `model:`, `auto_execute:`, `auto_execute_command:` → **dead metadata** (tak dikonsumsi backend; `routes/skills.py` hanya expose slug/name/jenis/output/has_pipeline). Hapus.
2. Seksi orkestrasi: "**Eksekusi di v7**", tabel "**Tahap X0–X4**" dengan kolom **Pelaku AT/KT/PT**, "Mode auto-execute", titik HITL.
3. Nama tool v9 sebagai resep langkah: `run_batch_*`, `read_digest`, `read_ingested_digest`, `append_temuan`, `render_kkp_docx`, `run_qc_kkp`, `write_penilaian_lke`, `read_pdf_page`. → ganti bahasa **tool-agnostik** ("baca fakta dari digest", "catat temuan K/K/S/A dengan dokumen_sumber").
4. Direktif UX agen: "jangan tanya Mau saya lanjut", "via UI/tab Setup", status `DISETUJUI_KT`/`SELESAI_KKP`.
5. Drift versi: satukan jadi satu `version`; buang seksi "Identitas" yang menduplikasi frontmatter + changelog naratif berlebih.

## Yang DIPERTAHANKAN (substansi)
Peran/paradigma · sumber fakta (digest, deskriptif) · **Checklist Pemeriksaan** · **Analisis Substantif** · **Aspek & Kriteria** · Scope/Ruang Lingkup · **Format unsur (KKSAR)** + Format Catatan + struktur Laporan · Referensi · Batasan · Posisi dalam keluarga skill.

## Header wajib (template)
```
> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah, peran AT/KT/PM,
> titik HITL, auto-eksekusi, pilihan model — bukan bagian skill ini; diatur oleh orkestrator
> (harness: backend/app/prompts/anggota_tim.md; produksi: INTEGRAL). Skill ini menetapkan APA yang
> dinilai dan FORMAT keluarannya. Temuan direkam K/K/S/A; Rekomendasi disusun di laporan, bukan KKP.
```

## Frontmatter minimal (template)
```yaml
---
name: <slug>
jenis: <kalimat jenis pengawasan>
format_laporan: kksa | lke | memo
dasar-hukum: <ringkas>
kode-surat: <PW.xx.xx>            # bila ada
tingkat-keyakinan: memadai | terbatas | tidak-ada
version: "<x.y>"
changelog: [ ... ]                # ringkas, opsional
---
```

## Gate sebelum mencabut per skill
- Pastikan urutan/peran skill-spesifik **sudah ada di `anggota_tim.md`** sebelum dibuang dari skill (cek per skill; reviu-rka-kl punya loop per-RO, evaluasi ber-LKE punya alur `write_penilaian_lke`).
- Jangan ubah doktrin unsur (LKE tanpa-Sebab tetap; KKSA ber-Sebab anti-mengarang).
- Verifikasi: registry tetap kenal skill (`list_skills`), `get_skill_md` non-null, grep residu orkestrasi = 0 (kecuali changelog).

## Catatan harness
FE/BE v9 tetap jalan sebagai harness — pencabutan ini markdown-only, dibaca runtime (tanpa restart). Lapis tool-DB (`render_kkp_docx`/`read_context` baca DB) ditangani terpisah di **P1c**, bukan di P1a.
