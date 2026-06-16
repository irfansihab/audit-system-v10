'use client';

/**
 * Halaman TLHP — Tindak Lanjut Hasil Pengawasan (pilar ke-4, Workstream C5).
 * Daftar rekomendasi LHP/LHR + status + aging (warna). Klik filter status.
 * Desain clean (Prinsip UX §2): satu tabel, status & umur terbaca sekilas.
 */
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, getSession } from '@/lib/api';
import { AppShell } from '@/components/AppShell';

const STATUS_CLS: Record<string, string> = {
  SUDAH: 'bg-emerald-50 text-emerald-700',
  PROSES: 'bg-amber-50 text-amber-700',
  BELUM: 'bg-rose-50 text-rose-700',
  TIDAK_DAPAT: 'bg-gray-100 text-gray-600',
};
const WARNA_DOT: Record<string, string> = {
  HIJAU: 'bg-emerald-500', KUNING: 'bg-amber-400', ORANGE: 'bg-orange-500', MERAH: 'bg-rose-500',
};
const FILTERS = ['', 'BELUM', 'PROSES', 'SUDAH', 'TIDAK_DAPAT'];

export default function TlhpPage() {
  const router = useRouter();
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    if (!getSession()) { router.push('/login'); return; }
    setLoading(true);
    api.listTlhp(filter ? { status: filter } : undefined)
      .then((d) => setItems(d.items || []))
      .finally(() => setLoading(false));
  }, [router, filter]);

  const kritis = items.filter((i) => i.kritis).length;

  return (
    <AppShell>
      <div className="mb-4">
        <h1 className="text-xl font-bold text-gray-800">Tindak Lanjut Hasil Pengawasan</h1>
        <p className="text-sm text-gray-500">
          Status rekomendasi LHP/LHR sampai tuntas. {kritis > 0 && <span className="text-rose-600 font-semibold">{kritis} kritis (&gt;365 hari).</span>}
        </p>
      </div>

      <div className="flex gap-2 mb-4">
        {FILTERS.map((f) => (
          <button
            key={f || 'all'}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 rounded-full text-xs font-medium transition ${filter === f ? 'bg-primary text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
          >
            {f === '' ? 'Semua' : f}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-sm text-gray-400">Memuat…</p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-gray-200 bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-gray-500 border-b border-gray-100">
                <th className="px-4 py-3">No. Rek</th>
                <th className="px-4 py-3">Asal LHP</th>
                <th className="px-4 py-3">Satker</th>
                <th className="px-4 py-3">Substansi</th>
                <th className="px-4 py-3">PIC</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 whitespace-nowrap">Umur</th>
              </tr>
            </thead>
            <tbody>
              {items.map((r) => (
                <tr key={r.no_rek} className={`border-b border-gray-50 hover:bg-gray-50 ${r.kritis ? 'bg-rose-50/40' : ''}`}>
                  <td className="px-4 py-3 font-mono text-xs whitespace-nowrap">{r.no_rek}</td>
                  <td className="px-4 py-3 text-xs text-gray-600">{r.asal_lhp}</td>
                  <td className="px-4 py-3 text-xs text-gray-600">{r.satker}</td>
                  <td className="px-4 py-3 text-gray-700 max-w-xs">{r.substansi}</td>
                  <td className="px-4 py-3 text-xs text-gray-500">{r.pic}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_CLS[r.status] || 'bg-gray-100'}`}>{r.status}</span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-xs">
                    <span className={`inline-block w-2 h-2 rounded-full mr-1 ${WARNA_DOT[r.warna] || 'bg-gray-300'}`} />
                    {r.umur_hari != null ? `${r.umur_hari} hr` : '—'}
                  </td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr><td colSpan={7} className="px-4 py-8 text-center text-sm text-gray-400">Tidak ada rekomendasi.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </AppShell>
  );
}
