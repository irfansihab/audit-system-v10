'use client';

// Knowledge / Wiki — halaman induk.
// Fokus Knowledge ada di 4 submenu (halaman sendiri, bukan anchor):
//   /knowledge/pattern             — Pattern Temuan (+ promosi & graduasi PT/PM)
//   /knowledge/template            — Template KP/PKP
//   /knowledge/kriteria-pengawasan — Regulasi & pasal yang dipakai kriteria (kelola PT)
//   /knowledge/writeback           — Tulis-balik hasil pengawasan ke wiki
// Halaman induk ini: kartu navigasi + Cari Wiki (pencarian vault organisasi).

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { api, getSession, Session } from '@/lib/api';
import { AppShell } from '@/components/AppShell';

type SearchResult = {
  name: string;
  section: string;
  summary: string;
  path: string;
  score: number;
  snippet: string;
};

const SUBMENU = [
  {
    href: '/knowledge/pattern',
    icon: '🧩',
    judul: 'Pattern Temuan',
    desc: 'Pattern terkurasi acuan agen menyusun temuan. PT/PM: promosi pattern baru & graduasi skill.',
  },
  {
    href: '/knowledge/template',
    icon: '📇',
    judul: 'Template KP/PKP',
    desc: 'Template Kartu Penugasan & Program Kerja Pengawasan per skill (tahapan 1–2 INTEGRAL).',
  },
  {
    href: '/knowledge/kriteria-pengawasan',
    icon: '⚖️',
    judul: 'Kriteria Pengawasan',
    desc: 'Daftar regulasi & pasal yang dipakai kriteria. Upload dokumen → auto-generate regulasi ke wiki (PT).',
  },
  {
    href: '/knowledge/writeback',
    icon: '↩️',
    judul: 'Tulis-balik Wiki',
    desc: 'Hasil penugasan selesai ditulis balik ke vault sebagai catatan riwayat pengawasan.',
  },
];

export default function KnowledgePage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  const [q, setQ] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [notConfigured, setNotConfigured] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [pageContent, setPageContent] = useState<string>('');
  const [loadingPage, setLoadingPage] = useState(false);

  useEffect(() => {
    setMounted(true);
    const s = getSession();
    setSession(s);
    if (!s) router.push('/login');
  }, [router]);

  const runSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!q.trim()) return;
    setSearching(true);
    setError(null);
    setNotConfigured(null);
    setSelected(null);
    setPageContent('');
    try {
      const res = await api.searchWiki(q.trim(), 20);
      if (!res.configured) {
        setNotConfigured(res.message || 'Vault tidak dikonfigurasi (set APP_VAULT_PATH).');
        setResults([]);
      } else {
        setResults(res.results);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSearching(false);
    }
  };

  const openPage = async (name: string) => {
    setSelected(name);
    setLoadingPage(true);
    setPageContent('');
    try {
      const res = await api.getWikiPage(name);
      setPageContent(res.found ? (res.content || '') : (res.message || 'Catatan tidak ditemukan.'));
    } catch (err: any) {
      setPageContent(`Gagal memuat: ${err.message}`);
    } finally {
      setLoadingPage(false);
    }
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-primary-dark mb-1">Knowledge / Wiki</h1>
        <p className="text-sm text-gray-500 mb-5">
          Pusat pengetahuan tim Inspektorat II — pattern temuan, template KP/PKP, basis regulasi
          kriteria, dan tulis-balik hasil pengawasan.
        </p>

        {/* Kartu navigasi 4 fokus */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          {SUBMENU.map((m) => (
            <Link
              key={m.href}
              href={m.href}
              className="bg-white border border-gray-200 rounded-lg p-4 hover:border-primary hover:shadow-sm transition group"
            >
              <div className="text-2xl mb-2">{m.icon}</div>
              <div className="font-semibold text-primary-dark group-hover:text-primary">{m.judul}</div>
              <div className="text-xs text-gray-500 mt-1">{m.desc}</div>
            </Link>
          ))}
        </div>

        {/* Cari Wiki (vault organisasi) */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
          <h2 className="font-semibold text-primary-dark mb-1">Cari Wiki (vault organisasi)</h2>
          <p className="text-xs text-gray-500 mb-3">
            Pencarian luas di catatan vault <code>llm-wiki</code> (profil auditi, riwayat BPK, vendor,
            regulasi). Agen juga memanggil pencarian ini saat bekerja.
          </p>
          <form onSubmit={runSearch} className="flex gap-2">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="mis. temuan BPK PSTE, profil Ditjen Ekosdig, vendor …"
              className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm"
            />
            <button
              type="submit"
              disabled={searching || !q.trim()}
              className="px-4 py-2 rounded bg-primary text-white text-sm font-semibold hover:bg-primary-dark disabled:opacity-40"
            >
              {searching ? 'Mencari…' : 'Cari'}
            </button>
          </form>

          {error && (
            <div className="mt-3 p-2 rounded bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
          )}
          {notConfigured && (
            <div className="mt-3 p-2 rounded bg-amber-50 border border-amber-200 text-amber-800 text-sm">
              {notConfigured}
            </div>
          )}

          {results && (
            <div className="mt-4 grid md:grid-cols-2 gap-4">
              <div className="space-y-2 max-h-[460px] overflow-y-auto">
                {results.length === 0 && !notConfigured ? (
                  <p className="text-sm text-gray-400 italic">Tidak ada hasil untuk "{q}".</p>
                ) : (
                  results.map((r) => (
                    <button
                      key={r.path}
                      onClick={() => openPage(r.name)}
                      className={`w-full text-left border rounded p-3 hover:bg-gray-50 transition ${
                        selected === r.name ? 'border-primary bg-blue-50/40' : 'border-gray-200'
                      }`}
                    >
                      <div className="flex justify-between items-baseline gap-2">
                        <span className="font-medium text-sm text-primary-dark">{r.name}</span>
                        {r.section && (
                          <span className="text-[11px] text-gray-400 shrink-0">{r.section}</span>
                        )}
                      </div>
                      {r.summary && <div className="text-xs text-gray-600 mt-0.5">{r.summary}</div>}
                      {r.snippet && (
                        <div className="text-xs text-gray-400 mt-1 line-clamp-2">…{r.snippet}</div>
                      )}
                    </button>
                  ))
                )}
              </div>

              <div className="border border-gray-200 rounded p-3 bg-gray-50 max-h-[460px] overflow-y-auto">
                {!selected ? (
                  <p className="text-sm text-gray-400 italic">Klik salah satu hasil untuk membaca isinya.</p>
                ) : loadingPage ? (
                  <p className="text-sm text-gray-400 italic">Memuat {selected}…</p>
                ) : (
                  <>
                    <div className="text-xs font-semibold text-gray-500 mb-2">{selected}.md</div>
                    <pre className="text-xs whitespace-pre-wrap font-sans text-gray-800">{pageContent}</pre>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
