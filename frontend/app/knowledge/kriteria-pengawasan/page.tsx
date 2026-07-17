'use client';

// Knowledge > Kriteria Pengawasan — basis regulasi & pasal yang dipakai
// kriteria pengawasan.
// 1) "Dipakai kriteria CACM": daftar regulasi yang dirujuk kriteria aktif
//    (diturunkan dari registry — selalu sinkron, read-only).
// 2) "Regulasi wiki": kelola koleksi regulasi (upload PDF → auto-generate
//    draft, edit, hapus). HANYA Pengendali Teknis yang bisa mengelola.
//    File di wiki konteks/regulasi/*.md ikut dibaca agen via preload konteks.

import { useCallback, useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { api, getSession, Session } from '@/lib/api';
import { confirmDialog } from '@/lib/confirm';
import { AppShell } from '@/components/AppShell';

type RegulasiItem = Awaited<ReturnType<typeof api.listRegulasi>>['items'][number];

export default function KriteriaPengawasanPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  // Regulasi yang dipakai kriteria aktif (derivasi dari registry CACM)
  const [terpakai, setTerpakai] = useState<Array<{ regulasi: string; kriteria: string[] }>>([]);

  // Koleksi regulasi wiki
  const [items, setItems] = useState<RegulasiItem[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [content, setContent] = useState('');
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const isPT = session?.role_aktif === 'PT';

  const refresh = useCallback(async () => {
    try {
      const [reg, krit] = await Promise.all([api.listRegulasi(), api.listCacmKriteria()]);
      setItems(reg.items);
      // Group regulasi → kriteria yang merujuknya
      const map = new Map<string, string[]>();
      for (const k of krit.items) {
        for (const r of k.regulasi) {
          const cur = map.get(r) || [];
          cur.push(k.id);
          map.set(r, cur);
        }
      }
      setTerpakai(
        [...map.entries()]
          .map(([regulasi, kriteria]) => ({ regulasi, kriteria }))
          .sort((a, b) => a.regulasi.localeCompare(b.regulasi))
      );
    } catch (e: any) {
      setErr(e.message);
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
    refresh();
  }, [router, refresh]);

  const buka = async (slug: string) => {
    setSelected(slug);
    setEditing(false);
    setContent('');
    setErr(null);
    try {
      const r = await api.getRegulasi(slug);
      setContent(r.content);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  const upload = async (f: File) => {
    setBusy('upload');
    setErr(null);
    setMsg(null);
    try {
      const r = await api.uploadRegulasi(f);
      setMsg(
        `✓ ${r.file} dibuat dari "${f.name}" (${r.judul || 'judul tidak terdeteksi'}). ` +
          'Status DRAFT-OTOMATIS — pasal kunci masih kosong, lengkapi lewat Edit lalu verifikasi.'
      );
      await refresh();
      await buka(r.slug);
    } catch (e: any) {
      setErr(`Upload gagal: ${e.message}`);
    } finally {
      setBusy(null);
      if (fileRef.current) fileRef.current.value = '';
    }
  };

  const simpan = async () => {
    if (!selected) return;
    setBusy('simpan');
    setErr(null);
    try {
      await api.updateRegulasi(selected, content);
      setMsg(`✓ ${selected}.md tersimpan.`);
      setEditing(false);
      await refresh();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(null);
    }
  };

  const hapus = async (slug: string) => {
    if (
      !(await confirmDialog({
        message: `Hapus regulasi "${slug}" dari wiki? Agen tidak akan membacanya lagi di preload konteks.`,
        danger: true,
        confirmText: 'Hapus',
      }))
    )
      return;
    setBusy('hapus');
    setErr(null);
    try {
      await api.deleteRegulasi(slug);
      setMsg(`✓ ${slug} dihapus.`);
      if (selected === slug) {
        setSelected(null);
        setContent('');
      }
      await refresh();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(null);
    }
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-primary-dark mb-1">Kriteria Pengawasan</h1>
        <p className="text-sm text-gray-500 mb-5">
          Basis regulasi &amp; pasal yang menjadi kriteria pengawasan. Regulasi di wiki ikut dibaca
          agen (preload konteks anti-halusinasi) dan jadi bahan{' '}
          <Link href="/cacm/kriteria" className="text-primary hover:underline">
            usulan kriteria CACM
          </Link>
          .{' '}
          {isPT ? (
            <span>Anda Pengendali Teknis — bisa upload dokumen, edit, dan hapus regulasi.</span>
          ) : (
            <span className="text-gray-400">Hanya Pengendali Teknis yang dapat mengelola.</span>
          )}
        </p>

        {err && <div className="mb-3 p-3 rounded bg-red-50 border border-red-200 text-red-700 text-sm whitespace-pre-wrap">{err}</div>}
        {msg && <div className="mb-3 p-3 rounded bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">{msg}</div>}

        {/* ===== 1. Regulasi yang dipakai kriteria CACM aktif ===== */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
          <h2 className="font-semibold text-primary-dark mb-1">
            Dipakai kriteria CACM aktif <span className="text-xs font-normal text-gray-400">({terpakai.length} rujukan)</span>
          </h2>
          <p className="text-xs text-gray-500 mb-3">
            Diturunkan langsung dari kriteria aktif — selalu sinkron. Ubah lewat{' '}
            <Link href="/cacm/kriteria" className="text-primary hover:underline">CACM &gt; Kriteria CACM</Link>.
          </p>
          {terpakai.length === 0 ? (
            <p className="text-sm text-gray-400 italic">Belum ada kriteria aktif yang merujuk regulasi.</p>
          ) : (
            <table className="w-full text-xs">
              <thead>
                <tr className="text-left text-gray-500 border-b border-gray-200">
                  <th className="py-1.5 pr-2">Regulasi / pasal</th>
                  <th className="py-1.5 pl-2 w-64">Dipakai kriteria</th>
                </tr>
              </thead>
              <tbody>
                {terpakai.map((t, i) => (
                  <tr key={i} className="border-b border-gray-100 last:border-0 align-top">
                    <td className="py-1.5 pr-2 text-gray-700">{t.regulasi}</td>
                    <td className="py-1.5 pl-2">
                      {t.kriteria.map((k) => (
                        <span key={k} className="inline-block mr-1 mb-0.5 px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-700 font-mono text-[10px]">
                          {k}
                        </span>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* ===== 2. Koleksi regulasi wiki (kelola) ===== */}
        <div className="bg-white border border-gray-200 rounded-lg p-5">
          <div className="flex items-start justify-between flex-wrap gap-2 mb-1">
            <h2 className="font-semibold text-primary-dark">
              Regulasi wiki <span className="text-xs font-normal text-gray-400">({items.length} + cheat sheet inti)</span>
            </h2>
            {isPT && (
              <label className={`px-3 py-1.5 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark cursor-pointer ${busy === 'upload' ? 'opacity-50 pointer-events-none' : ''}`}>
                {busy === 'upload' ? 'Mengekstrak…' : '⬆ Upload dokumen (PDF)'}
                <input
                  ref={fileRef}
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) upload(f);
                  }}
                />
              </label>
            )}
          </div>
          <p className="text-xs text-gray-500 mb-3">
            Upload PDF regulasi → sistem mengekstrak judul/nomor secara deterministik (tanpa LLM) dan
            membuat draft markdown di wiki. Draft berstatus <b>DRAFT-OTOMATIS</b> — pasal kunci wajib
            dilengkapi &amp; diverifikasi auditor sebelum dipakai merujuk.
          </p>

          <div className="grid md:grid-cols-2 gap-4">
            {/* Daftar */}
            <div className="border border-gray-200 rounded max-h-[520px] overflow-y-auto divide-y">
              <button
                onClick={() => buka('regulasi-kunci')}
                className={`w-full text-left p-3 hover:bg-amber-50/40 ${selected === 'regulasi-kunci' ? 'bg-amber-50' : ''}`}
              >
                <div className="text-sm font-medium text-gray-800">📌 Regulasi &amp; Pasal Kunci (cheat sheet inti)</div>
                <div className="text-[11px] text-gray-400 mt-0.5">
                  konteks/regulasi-kunci.md · dibaca agen setiap penugasan · tidak bisa dihapus
                </div>
              </button>
              {items.length === 0 ? (
                <div className="p-3 text-xs text-gray-400 italic">
                  Belum ada regulasi tambahan. {isPT ? 'Upload PDF untuk menambah.' : ''}
                </div>
              ) : (
                items.map((r) => (
                  <button
                    key={r.slug}
                    onClick={() => buka(r.slug)}
                    className={`w-full text-left p-3 hover:bg-amber-50/40 ${selected === r.slug ? 'bg-amber-50' : ''}`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="text-sm font-medium text-gray-800">{r.judul}</span>
                      {r.status === 'DRAFT-OTOMATIS' && (
                        <span className="shrink-0 text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">DRAFT</span>
                      )}
                    </div>
                    <div className="text-[11px] text-gray-400 mt-0.5">
                      {r.slug}.md{r.sumber_file ? ` · dari ${r.sumber_file}` : ''} · {r.updated.slice(0, 10)}
                    </div>
                  </button>
                ))
              )}
            </div>

            {/* Isi / editor */}
            <div className="border border-gray-200 rounded p-3 bg-gray-50 min-h-[300px] max-h-[520px] overflow-y-auto">
              {!selected ? (
                <p className="text-xs text-gray-400 italic">Klik regulasi di kiri untuk membaca isinya.</p>
              ) : editing ? (
                <>
                  <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    spellCheck={false}
                    className="w-full h-[400px] border border-gray-300 rounded p-2 font-mono text-xs leading-5 bg-white"
                  />
                  <div className="mt-2 flex gap-2">
                    <button
                      onClick={simpan}
                      disabled={busy === 'simpan'}
                      className="px-3 py-1.5 text-xs rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50"
                    >
                      {busy === 'simpan' ? 'Menyimpan…' : 'Simpan'}
                    </button>
                    <button
                      onClick={() => setEditing(false)}
                      className="px-3 py-1.5 text-xs rounded border border-gray-300 text-gray-600 hover:bg-gray-50"
                    >
                      Batal
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-semibold text-gray-500">{selected}.md</span>
                    {isPT && (
                      <div className="flex gap-2">
                        <button
                          onClick={() => setEditing(true)}
                          className="text-xs px-2.5 py-1 rounded border border-primary text-primary hover:bg-primary-50"
                        >
                          ✎ Edit
                        </button>
                        {selected !== 'regulasi-kunci' && (
                          <button
                            onClick={() => hapus(selected)}
                            disabled={busy === 'hapus'}
                            className="text-xs px-2.5 py-1 rounded border border-red-300 text-red-600 hover:bg-red-50 disabled:opacity-50"
                          >
                            🗑 Hapus
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                  <pre className="text-xs whitespace-pre-wrap font-sans text-gray-800">{content || 'Memuat…'}</pre>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
