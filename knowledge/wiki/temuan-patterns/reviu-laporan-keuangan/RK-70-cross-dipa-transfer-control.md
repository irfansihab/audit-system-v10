---
id: RK-70
skill: reviu-keuangan
kategori: RK-KONTROL
severity: HIGH
judul: Cross-DIPA Budget Transfer — Kontrol & Dokumentasi Approval Lemah
kriteria_baku: PP 60/2008 Pengendalian Internal + PMK 107/2024 Pengelolaan DIPA
---

# RK-70: Cross-DIPA Budget Transfer — Kontrol & Dokumentasi Approval Lemah

## Kondisi

Pembebanan anggaran lintas-DIPA (transfer dari satu DIPA ke DIPA lainnya untuk kebutuhan multi-unit) dilaksanakan tanpa dokumentasi approval yang lengkap. Khususnya:
- Tidak ada SK KPA dari unit pemberi DIPA (yang mebebankan)
- Kronologi & justifikasi urgensi penggunaan PNBP tidak terdokumentasi
- Approval chain tidak jelas antara penerima & pemberi DIPA

Contoh konkret: Pembebanan Rp4.351.500.000 dari DIPA DJED untuk pembiayaan beasiswa BPSDM hanya didukung dokumen dari pihak penerima (BPSDM), tanpa SK KPA dari DJED sebagai approval formal.

## Kriteria (Standar Harapan)

Berdasarkan **PP 60/2008 Pasal 8** (Pengendalian Internal Pemerintah):

1. **Setiap transaksi keuangan harus didukung dokumen yang lengkap dan sah**
   - SK KPA dari UNIT PEMBERI DIPA (yang mebebankan) — WAJIB
   - SK KPA dari UNIT PENERIMA DIPA (yang menerima beban) — WAJIB
   - Kronologi/justifikasi urgensi transaksi — WAJIB
   - Verifikasi kebutuhan riil dari kedua belah pihak — WAJIB

2. **Koordinasi lintas-unit harus terstruktur & terdokumentasi**
   - Ada framework formal untuk cross-DIPA transfers
   - Approval chain jelas & documented
   - Quality control atas completeness dokumen

3. **Accountability trail harus utuh**
   - Setiap transfer harus traceable: siapa authorize, kapan, berapa, untuk apa

## Akibat (Dampak Risiko)

**🔴 Risk Level: HIGH**

1. **Compliance Risk**
   - Pembebanan tanpa SK KPA pemberi = potentially non-compliant dengan PP 60/2008
   - Risk audit eksternal (BPK) menolak transaksi atau merequire perbaikan

2. **Accountability Risk**
   - Approval trail incomplete → sulit track accountability jika ada dispute
   - KPA (Kepala DIPA) penerima beban bisa pertanyakan legalitas beban

3. **Financial Risk**
   - Transaksi bisa diminta untuk dibalik/dilaporkan sebagai kesalahan
   - Nilai Rp4.351.500.000 (case konkret) tidak terbayarkan atau delayed

4. **Governance Risk**
   - Koordinasi lintas-unit tidak terstruktur → inconsistency handling di masa depan
   - Precedent lemah untuk transaksi serupa lainnya

## Penyebab (Root Cause)

1. **Primary:** Tidak ada framework/prosedur standardisasi untuk cross-DIPA transfers
   - Setiap unit mengandalkan koordinasi informal
   - Approval requirement tidak jelas di mana-mana

2. **Secondary:** Quality control atas dokumentasi belum matang
   - Tidak ada checklist dokumentasi minimum untuk cross-DIPA transfers
   - Reviewer hanya fokus pada aspek finansial (nominal), bukan compliance (dokumen)

3. **Tertiary:** Gap awareness tentang PP 60/2008 requirement di level operasional

## Bukti Yang Harus Dicari

**Dalam setiap audit pembayaran lintas-DIPA, cek:**

1. ✓ **Kelengkapan SK KPA dari KEDUA belah pihak** (pemberi & penerima DIPA)
   - Cari: SK KPA pemberi DIPA sebagai approval formal pembebanan
   - If MISSING → finding applies

2. ✓ **Dokumentasi kronologi & justifikasi urgensi**
   - Cari: ND/surat yang menjelaskan MENGAPA transfer urgent & perlu
   - If MISSING atau VAGUE → finding applies

3. ✓ **Verification dari kedua unit** (evidence kesepakatan)
   - Cek: Apakah ada mutual agreement dokumen?
   - If NO → finding applies

4. ✓ **Nilai finansial** (nominal pembebanan)
   - Catat: Besarnya beban, sumber DIPA, tujuan

5. ✓ **Timeline** (kapan transfer terjadi, kapan dokumentasi lengkap)
   - Identifikasi: Apakah transaksi lebih dulu, dokumentasi belakangan?

**Red Flag Indicators:**
- Transfer terjadi tapi SK KPA pemberi belum ada (dokumentasi belakangan)
- Justifikasi urgensi tidak jelas ("perlu cepat" tanpa detail)
- Koordinasi verbal only (tidak ada dokumen formal)
- Dispute/keterlambatan pembayaran karena approval chain unclear

## Format Temuan JSON

```json
{
  "id": "RK-70-[NOMOR_TEMUAN]",
  "judul": "Cross-DIPA Transfer — Dokumentasi Approval Incomplete",
  "severity": "HIGH",
  "dipa_pemberi": "[UNIT & DIPA NUMBER]",
  "dipa_penerima": "[UNIT & DIPA NUMBER]",
  "nominal": "[RP. AMOUNT]",
  "tujuan_transfer": "[PURPOSE]",
  "gap_dokumentasi": [
    "SK KPA pemberi: [MISSING/INCOMPLETE]",
    "Kronologi urgensi: [MISSING/VAGUE]",
    "Mutual agreement: [MISSING/INFORMAL]"
  ],
  "status_tindak_lanjut": "[OPEN/CLOSED/PENDING]",
  "tanggal_finding": "[DATE]",
  "auditor": "[NAME]",
  "rekomendasi": [
    "Lengkapi SK KPA dari unit pemberi DIPA dengan detail approval formal",
    "Dokumentasi kronologi & justifikasi urgensi transfer secara formal",
    "Develop framework standardisasi cross-DIPA transfer procedures (per 31 Agustus 2026)"
  ]
}
```

## Contoh Kasus Historis

### **ND-196: Pembebanan Beasiswa BPSDM dari DIPA DJED (Rp4.351.500.000)**

**Context:**
- Periode: Tahun 2026 (sedang berjalan)
- Pemberi DIPA: Ditjen Ekosistem Digital (DJED)
- Penerima DIPA: BPSDM (Badan Pengembangan SDM Kominfo Digital)
- Nominal: Rp4.351.500.000 (untuk 322 mahasiswa beasiswa)
- Alasan: Pembiayaan beasiswa dari PNBP lintas-unit

**Finding Detail:**
- ✓ Dokumen yang ada: SK KPA BPSDM, ND timeline, ND Biro Perencanaan
- ❌ MISSING: SK KPA DJED (pemberi DIPA) sebagai approval formal pembebanan
- ❌ MISSING: Kronologi & justifikasi mengapa urgent
- ❌ MISSING: Mutual agreement dokumen antara DJED & BPSDM

**Dampak:**
- Pembayaran ditunda/tidak pasti hingga SK KPA DJED lengkap
- Compliance risk jika BPK audit

**Status Tindak Lanjut:**
- Status: **OPEN** (Dalam proses perbaikan)
- Deadline: 30 Juli 2026
- Action: Lengkapi SK KPA DJED + kronologi dokumentasi

**Sumber:** ND-196 (Catatan Hasil Reviu Pembiayaan Beasiswa BPSDM), Inspectorat II, 08 Juli 2026

---

## Catatan

**Scope Aplikasi:**
- Pattern ini berlaku untuk SEMUA cross-DIPA transfers, tidak hanya beasiswa
- Applicable ke lintas-departemen coordination mana pun yang melibatkan pembebanan DIPA

**Timeline Rekomendasi:**
- Short-term (immediate): Lengkapi dokumentasi untuk kasus ND-196 (30 Juli 2026)
- Medium-term (Agustus 2026): Develop framework standardisasi cross-DIPA procedure
- Long-term (Sep 2026 onwards): Monitor compliance & QA checklist

**Related Patterns:**
- [[RK-67]] — PNBP Overstating (accuracy aspect)
- [[RK-68]] — Piutang Lag Sinkronisasi (system sync aspect)
- [[RK-69]] — Payment Delay (timing aspect)
- [[SAIPI-65]] — KKP Tidak Standar (documentation methodology)

---

## Related Pages

- [[reviu-keuangan/README]] — Index pattern reviu-keuangan
- [[audit-om-tkppse-juli-2026]] — Related audit case
- [[penjaminan-materi-edukasi-antikorupsi-juli-2026]] — Related coordination case

