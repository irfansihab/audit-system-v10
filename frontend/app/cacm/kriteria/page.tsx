'use client';

// Kriteria CACM — halaman khusus (menu CACM > Kriteria CACM).
// Menggantikan panel lama di /knowledge#kriteria-cacm (anchor scroll rapuh +
// konten dobel di dua menu). Semua role bisa baca; HANYA Pengendali Teknis
// yang bisa kelola (edit/hapus/tambah). File YAML tetap sumber kebenaran —
// perubahan lewat UI divalidasi penuh di backend sebelum ditulis.

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, getSession, Session } from '@/lib/api';
import { confirmDialog } from '@/lib/confirm';
import { AppShell } from '@/components/AppShell';

type Kriteria = Awaited<ReturnType<typeof api.listCacmKriteria>>['items'][number];

const STATUS_COLOR: Record<string, string> = {
  MERAH: 'bg-red-100 text-red-800 border-red-300',
  KUNING: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  HIJAU: 'bg-green-100 text-green-800 border-green-300',
  INFO: 'bg-gray-100 text-gray-600 border-gray-300',
};

const TEMPLATE_BARU = `# Kriteria baru — ganti id/nama/dimensi sesuai kebutuhan.
id: ANG-CONTOH-BARU
revisi: "2026-Q3"
nama: "Nama kriteria yang menjelaskan sinyalnya"

tipe: numeric_threshold
dimensi: ANGGARAN            # PENGADAAN_RENCANA | PENGADAAN_REALISASI | ANGGARAN | KINERJA
sumber_data: dipa            # sirup | spse | dipa | kinerja_eperformance | kinerja_integral | kinerja_other
satker_terapkan: [itjen, ekosdig, wasdig]

regulasi:
  - "[VERIFIKASI AUDITOR] dasar hukum ambang ini"

metric:
  expression: "ratio(sum(data.realisasi), sum(data.pagu)) * 100"
  satuan: persen
  format_display: "{:.1f}%"

thresholds:
  - status: MERAH
    condition: "<50"
    catatan: "Penjelasan kenapa merah"
  - status: KUNING
    condition: ">=50 AND <75"
    catatan: "Penjelasan kenapa kuning"
  - status: HIJAU
    condition: ">=75"
    catatan: "Penjelasan kenapa hijau"

evidence_fields:
  - data.satker
`;

export default function CacmKriteriaPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  const [items, setItems] = useState<Kriteria[]>([]);
  const [dimensions, setDimensions] = useState<string[]>([]);
  const [dimensi, setDimensi] = useState('');
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Kriteria | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  // Mode kelola (PT): edit YAML kriteria terpilih, atau buat baru.
  const [editing, setEditing] = useState<'edit' | 'baru' | null>(null);
  const [yamlText, setYamlText] = useState('');
  const [saving, setSaving] = useState(false);

  const isPT = session?.role_aktif === 'PT';

  const refresh = useCallback(async (dim: string) => {
    setLoading(true);
    setErr(null);
    try {
      const r = await api.listCacmKriteria(dim || undefined);
      setItems(r.items);
      setDimensions(r.dimensi_available);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setMounted(true);
    const s = getSession();
    setSession(s);
    if (!s) {
      router.push('/login');
      return;
    }
    refresh('');
  }, [router, refresh]);

  useEffect(() => {
    if (!mounted) return;
    refresh(dimensi);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dimensi]);

  const mulaiEdit = async (k: Kriteria) => {
    setMsg(null);
    setErr(null);
    try {
      const r = await api.getCacmKriteriaYaml(k.id);
      setYamlText(r.yaml);
      setEditing('edit');
    } catch (e: any) {
      setErr(`Gagal memuat YAML: ${e.message}`);
    }
  };

  const mulaiBaru = () => {
    setSelected(null);
    setYamlText(TEMPLATE_BARU);
    setEditing('baru');
    setMsg(null);
    setErr(null);
  };

  const simpan = async () => {
    setSaving(true);
    setErr(null);
    setMsg(null);
    try {
      const r =
        editing === 'baru'
          ? await api.createCacmKriteria(yamlText)
          : await api.updateCacmKriteria(selected!.id, yamlText);
      setMsg(`✓ ${r.file} tersimpan. Registry evaluator dimuat ulang — run lama bisa dihitung ulang via "Re-evaluate" di Run CACM.`);
      setEditing(null);
      await refresh(dimensi);
      setSelected(null);
    } catch (e: any) {
      // 422 backend membawa daftar error validasi — tampilkan apa adanya.
      setErr(`Ditolak validator (file TIDAK ditulis): ${e.message}`);
    } finally {
      setSaving(false);
    }
  };

  const hapus = async (k: Kriteria) => {
    if (
      !(await confirmDialog({
        message: `Hapus kriteria ${k.id} — "${k.nama}"? File YAML-nya dihapus dan kriteria berhenti dipakai run baru. Finding lama di DB tetap tersimpan.`,
        danger: true,
        confirmText: 'Hapus',
      }))
    )
      return;
    setErr(null);
    setMsg(null);
    try {
      await api.deleteCacmKriteria(k.id);
      setMsg(`✓ ${k.id} dihapus.`);
      setSelected(null);
      setEditing(null);
      await refresh(dimensi);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-start mb-1 flex-wrap gap-2">
          <h1 className="text-2xl font-bold text-primary-dark">Kriteria CACM</h1>
          {isPT && (
            <button
              onClick={mulaiBaru}
              className="px-3 py-2 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark"
            >
              ＋ Kriteria baru
            </button>
          )}
        </div>
        <p className="text-sm text-gray-500 mb-4">
          Definisi MERAH/KUNING/HIJAU yang dipakai mesin evaluator atas data pengadaan/anggaran/kinerja.
          Sumber: <code>knowledge/cacm/kriteria/&lt;id&gt;.yaml</code>.{' '}
          {isPT ? (
            <span>Anda Pengendali Teknis — bisa mengubah, menambah, dan menghapus kriteria di sini (perubahan tervalidasi sebelum disimpan).</span>
          ) : (
            <span className="text-gray-400">Hanya Pengendali Teknis yang dapat mengelola kriteria; role lain baca saja.</span>
          )}
        </p>

        {err && <div className="mb-3 p-3 rounded bg-red-50 border border-red-200 text-red-700 text-sm whitespace-pre-wrap">{err}</div>}
        {msg && <div className="mb-3 p-3 rounded bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">{msg}</div>}

        {editing ? (
          /* ===== Mode kelola (PT) — edit YAML langsung, validasi di backend ===== */
          <div className="bg-white border border-amber-300 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
              <h2 className="font-semibold text-primary-dark text-sm">
                {editing === 'baru' ? 'Kriteria baru' : `Edit ${selected?.id}`}
              </h2>
              <span className="text-[11px] text-gray-500">
                Disimpan hanya bila lolos validasi skema + parser DSL (metric &amp; threshold).
              </span>
            </div>
            <textarea
              value={yamlText}
              onChange={(e) => setYamlText(e.target.value)}
              spellCheck={false}
              className="w-full h-[460px] border border-gray-300 rounded p-3 font-mono text-xs leading-5 focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
            <div className="mt-3 flex gap-2">
              <button
                onClick={simpan}
                disabled={saving}
                className="px-4 py-2 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50"
              >
                {saving ? 'Menyimpan…' : 'Simpan'}
              </button>
              <button
                onClick={() => {
                  setEditing(null);
                  setErr(null);
                }}
                disabled={saving}
                className="px-4 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-50"
              >
                Batal
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="mb-3 flex items-center gap-3">
              <select
                value={dimensi}
                onChange={(e) => setDimensi(e.target.value)}
                className="border border-gray-300 rounded px-2 py-1.5 text-sm"
              >
                <option value="">Semua dimensi ({dimensions.length})</option>
                {dimensions.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
              <span className="text-xs text-gray-500">{items.length} kriteria</span>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {/* Daftar */}
              <div className="bg-white border border-gray-200 rounded-lg max-h-[560px] overflow-y-auto divide-y">
                {loading ? (
                  <div className="p-3 text-sm text-gray-400 italic">Memuat kriteria…</div>
                ) : items.length === 0 ? (
                  <div className="p-3 text-sm text-gray-400 italic">
                    Belum ada kriteria. {isPT ? 'Klik "＋ Kriteria baru" untuk membuat.' : ''}
                  </div>
                ) : (
                  items.map((k) => (
                    <button
                      key={k.id}
                      onClick={() => setSelected(k)}
                      className={`w-full text-left p-3 hover:bg-amber-50/40 transition ${selected?.id === k.id ? 'bg-amber-50' : ''}`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <span className="font-mono text-[11px] text-gray-500 shrink-0">{k.id}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 text-gray-600 shrink-0">{k.revisi}</span>
                      </div>
                      <div className="text-sm font-medium text-gray-800 mt-0.5">{k.nama}</div>
                      <div className="text-[11px] text-gray-400 mt-0.5">
                        <span className="uppercase">{k.dimensi}</span>
                        <span> · {k.sumber_data}</span>
                        <span> · {k.satker_terapkan.join(', ')}</span>
                      </div>
                    </button>
                  ))
                )}
              </div>

              {/* Detail */}
              <div className="bg-white border border-gray-200 rounded-lg p-4 min-h-[320px] max-h-[560px] overflow-y-auto">
                {!selected ? (
                  <p className="text-sm text-gray-400 italic">Klik salah satu kriteria di kiri untuk baca detail.</p>
                ) : (
                  <>
                    <div className="flex items-center justify-between gap-2 mb-2 flex-wrap">
                      <span className="font-mono text-xs text-gray-500">{selected.id}</span>
                      {isPT && (
                        <div className="flex gap-2">
                          <button
                            onClick={() => mulaiEdit(selected)}
                            className="text-xs px-2.5 py-1 rounded border border-primary text-primary hover:bg-primary-50"
                          >
                            ✎ Edit
                          </button>
                          <button
                            onClick={() => hapus(selected)}
                            className="text-xs px-2.5 py-1 rounded border border-red-300 text-red-600 hover:bg-red-50"
                          >
                            🗑 Hapus
                          </button>
                        </div>
                      )}
                    </div>
                    <div className="text-base font-semibold text-gray-800 mb-1">{selected.nama}</div>
                    <div className="text-xs text-gray-500 mb-2">
                      <b>Dimensi:</b> {selected.dimensi} · <b>Sumber:</b> {selected.sumber_data} · <b>Revisi:</b> {selected.revisi}
                    </div>
                    {selected.regulasi.length > 0 && (
                      <div className="text-xs text-gray-600 mb-2">
                        <b>Regulasi:</b>
                        <ul className="list-disc list-inside ml-2">
                          {selected.regulasi.map((r, i) => (
                            <li key={i}>{r}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div className="text-xs text-gray-600 mb-2">
                      <b>Metric:</b> {selected.metric.satuan && <span className="text-gray-500">({selected.metric.satuan})</span>}
                      <pre className="text-[11px] bg-gray-50 border border-gray-200 rounded p-2 mt-1 whitespace-pre-wrap font-mono text-gray-800">
                        {selected.metric.expression}
                      </pre>
                    </div>
                    <div className="text-xs text-gray-600 mb-2">
                      <b>Thresholds:</b>
                      <table className="w-full text-[11px] mt-1 border border-gray-200 rounded overflow-hidden">
                        <thead>
                          <tr className="bg-gray-100">
                            <th className="px-1.5 py-1 text-left">Status</th>
                            <th className="px-1.5 py-1 text-left">Condition</th>
                            <th className="px-1.5 py-1 text-left">Catatan</th>
                          </tr>
                        </thead>
                        <tbody>
                          {selected.thresholds.map((t, i) => (
                            <tr key={i} className="border-t border-gray-200">
                              <td className="px-1.5 py-1">
                                <span className={`px-1 py-0.5 rounded border ${STATUS_COLOR[t.status] || 'bg-gray-100 text-gray-500 border-gray-300'}`}>
                                  {t.status}
                                </span>
                              </td>
                              <td className="px-1.5 py-1 font-mono">{t.condition}</td>
                              <td className="px-1.5 py-1 text-gray-500">{t.catatan || '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    {selected.evidence_fields.length > 0 && (
                      <div className="text-xs text-gray-500 mb-1">
                        <b>Evidence fields:</b> {selected.evidence_fields.join(', ')}
                      </div>
                    )}
                    {selected.satker_terapkan.length > 0 && (
                      <div className="text-xs text-gray-500 mb-1">
                        <b>Berlaku utk satker:</b> {selected.satker_terapkan.join(', ')}
                      </div>
                    )}
                    {selected.catatan_revisi && (
                      <div className="text-xs text-gray-500 mt-2 border-t border-gray-100 pt-2 whitespace-pre-wrap">
                        <b>Catatan revisi:</b> {selected.catatan_revisi}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
