'use client';

/**
 * Dashboard beranda INTEGRAL — pusat informasi pengawasan (Workstream F).
 *
 * Satu fetch ke /dashboard/summary (di-cache backend ~30s, ringan utk ±80 user).
 * Widget: EWS (F1) · progres PKPT (F2) · permintaan belum ditindaklanjuti (F3) ·
 * progres TLHP (F4) · tren temuan berulang (F5) · scorecard kinerja (F6).
 * Desain clean (Prinsip UX §2): kartu seragam, status warna sekilas, klik → detail.
 */
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { api, getSession } from '@/lib/api';
import { AppShell } from '@/components/AppShell';

const WARNA: Record<string, string> = {
  HIJAU: 'bg-emerald-500',
  KUNING: 'bg-amber-400',
  ORANGE: 'bg-orange-500',
  MERAH: 'bg-rose-500',
};

function Card({ title, href, children }: { title: string; href?: string; children: React.ReactNode }) {
  const inner = (
    <div className={`h-full rounded-2xl border border-gray-200 bg-white p-5 shadow-sm ${href ? 'hover:shadow-md hover:border-primary/40 transition' : ''}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-700">{title}</h3>
        {href && <span className="text-xs text-primary">Lihat →</span>}
      </div>
      {children}
    </div>
  );
  return href ? <Link href={href} className="block h-full">{inner}</Link> : inner;
}

function Bar({ pct, color = 'bg-primary' }: { pct: number; color?: string }) {
  return (
    <div className="h-2 w-full rounded-full bg-gray-100 overflow-hidden">
      <div className={`h-full ${color}`} style={{ width: `${Math.min(100, Math.max(0, pct))}%` }} />
    </div>
  );
}

function Soon({ title, note }: { title: string; note: string }) {
  return (
    <Card title={title}>
      <div className="flex flex-col items-center justify-center py-6 text-center">
        <span className="text-2xl mb-2 opacity-40">🚧</span>
        <p className="text-xs text-gray-400">{note}</p>
      </div>
    </Card>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!getSession()) { router.push('/login'); return; }
    api.getDashboardSummary()
      .then(setData)
      .catch((e) => setErr(String(e?.message || e)))
      .finally(() => setLoading(false));
  }, [router]);

  return (
    <AppShell>
      <div className="mb-5">
        <h1 className="text-xl font-bold text-gray-800">Beranda</h1>
        <p className="text-sm text-gray-500">Ringkasan pengawasan Inspektorat II — sekilas semua pilar.</p>
      </div>

      {loading && <p className="text-sm text-gray-400">Memuat ringkasan…</p>}
      {err && <p className="text-sm text-rose-600">Gagal memuat: {err}</p>}

      {data && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

          {/* F1 — EWS */}
          <Card title="🔔 Early Warning (CACM)" href="/cacm">
            <div className="flex gap-4 mb-3">
              <div><div className="text-2xl font-bold text-rose-600">{data.ews?.merah ?? 0}</div><div className="text-xs text-gray-500">Merah</div></div>
              <div><div className="text-2xl font-bold text-amber-500">{data.ews?.kuning ?? 0}</div><div className="text-xs text-gray-500">Kuning</div></div>
            </div>
            <ul className="space-y-1">
              {(data.ews?.terbaru ?? []).slice(0, 3).map((e: any, i: number) => (
                <li key={i} className="text-xs text-gray-600 truncate">
                  <span className={`inline-block w-2 h-2 rounded-full mr-1 ${e.status === 'MERAH' ? 'bg-rose-500' : e.status === 'KUNING' ? 'bg-amber-400' : 'bg-gray-300'}`} />
                  {e.kode} · {e.satker}
                </li>
              ))}
            </ul>
          </Card>

          {/* F2 — PKPT */}
          <Card title="🎯 Pemenuhan PKPT" href="/penugasan">
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-3xl font-bold text-primary-dark">{data.pkpt?.persen_selesai ?? 0}%</span>
              <span className="text-xs text-gray-500">{data.pkpt?.selesai ?? 0}/{data.pkpt?.total ?? 0} selesai</span>
            </div>
            <Bar pct={data.pkpt?.persen_selesai ?? 0} />
            <div className="flex gap-3 mt-3 text-xs text-gray-500">
              <span>▶ Berjalan {data.pkpt?.berjalan ?? 0}</span>
              <span>◷ Rencana {data.pkpt?.rencana ?? 0}</span>
              <span>⏸ Tertunda {data.pkpt?.tertunda ?? 0}</span>
            </div>
          </Card>

          {/* F4 — TLHP */}
          <Card title="🔁 Tindak Lanjut (TLHP)" href="/tlhp">
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-3xl font-bold text-primary-dark">{data.tlhp?.persen_selesai ?? 0}%</span>
              <span className="text-xs text-gray-500">{data.tlhp?.selesai ?? 0}/{data.tlhp?.total ?? 0} tuntas</span>
            </div>
            <div className="flex h-2 w-full rounded-full overflow-hidden mb-2">
              {['HIJAU', 'KUNING', 'ORANGE', 'MERAH'].map((w) => {
                const n = data.tlhp?.by_warna?.[w] ?? 0;
                const total = data.tlhp?.total || 1;
                return <div key={w} className={WARNA[w]} style={{ width: `${(n / total) * 100}%` }} title={`${w}: ${n}`} />;
              })}
            </div>
            <p className="text-xs">
              <span className="font-semibold text-rose-600">{data.tlhp?.kritis_count ?? 0} kritis</span>
              <span className="text-gray-500"> (&gt;365 hari belum tuntas)</span>
            </p>
          </Card>

          {/* F6 — Scorecard capaian kinerja */}
          <Card title="📈 Capaian Kinerja Pengawasan">
            <div className="grid grid-cols-3 gap-2">
              {(data.capaian_kinerja?.indikator ?? []).map((k: any) => (
                <div key={k.kode} className="rounded-lg bg-gray-50 p-2 text-center">
                  <div className="text-[10px] text-gray-500">{k.kode}</div>
                  <div className="text-base font-bold text-primary-dark leading-tight">{k.nilai}</div>
                  <div className="text-[10px] text-gray-400 truncate" title={k.predikat}>
                    {k.tren === 'naik' ? '↑' : k.tren === 'turun' ? '↓' : '→'} {k.predikat}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-[10px] text-gray-400 mt-2">Sumber: {data.capaian_kinerja?.sumber === 'manual' ? 'entri manual' : data.capaian_kinerja?.sumber}</p>
          </Card>

          {/* Penugasan ringkas */}
          <Card title="🗂 Penugasan" href="/penugasan">
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-3xl font-bold text-primary-dark">{data.penugasan?.total ?? 0}</span>
              <span className="text-xs text-gray-500">total · {data.penugasan?.aktif ?? 0} aktif</span>
            </div>
            <div className="space-y-1">
              {Object.entries(data.penugasan?.by_status ?? {}).map(([s, n]: any) => (
                <div key={s} className="flex justify-between text-xs text-gray-600"><span>{s}</span><span className="font-semibold">{String(n)}</span></div>
              ))}
            </div>
          </Card>

          {/* F3 + F5 — belum dibangun (jujur) */}
          <Soon title="📥 Permintaan Belum Ditindaklanjuti" note="Modul F3 — segera hadir." />
          <Soon title="📊 Tren Temuan Berulang" note="Modul F5 — segera hadir." />
        </div>
      )}
    </AppShell>
  );
}
