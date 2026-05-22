'use client';

// Halaman Knowledge / Wiki — SCAFFOLDING. Substansi (daftar pattern temuan dari
// wiki, editor konteks, pemantauan usulan pattern dari feedback agen) akan diisi
// kemudian. Terhubung ke folder wiki/ (temuan-patterns + konteks) dan ke usulan
// pattern yang muncul di dashboard feedback agen.

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { clearToken, getSession, Session } from '@/lib/api';

const SECTIONS = [
  {
    title: 'Pattern Temuan (wiki)',
    desc: 'Daftar pattern temuan reviu-pengadaan & reviu-rka-kl dari wiki/temuan-patterns/ — tambah, edit, kalibrasi severity.',
  },
  {
    title: 'Konteks Pendukung',
    desc: 'Pola temuan berulang, glossary istilah Komdigi, dan regulasi kunci (wiki/konteks/) yang dibaca agen untuk anti-halusinasi.',
  },
  {
    title: 'Pemantauan Usulan Pattern',
    desc: 'Pantau usulan pattern baru yang dilaporkan agen lewat feedback — promosikan yang berulang menjadi pattern wiki resmi.',
  },
];

export default function KnowledgePage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    setMounted(true);
    const s = getSession();
    setSession(s);
    if (!s) router.push('/login');
  }, [router]);

  const handleLogout = () => {
    clearToken();
    router.push('/login');
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <main className="min-h-screen">
      <header className="bg-primary text-white px-6 py-3 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Link href="/penugasan" className="text-white/80 hover:text-white text-sm">
            ← Penugasan
          </Link>
          <span className="text-white/40">|</span>
          <span className="font-semibold text-sm">Knowledge — Wiki & Pattern Temuan</span>
        </div>
        <div className="text-right text-xs">
          <div>{session.user.nama_lengkap}</div>
          <div className="opacity-80">
            <span className="px-2 py-0.5 rounded bg-white/15 ml-2">{session.role_aktif}</span>
            <button onClick={handleLogout} className="ml-3 underline">
              Keluar
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-center mb-5">
          <h1 className="text-2xl font-bold text-primary-dark">Knowledge / Wiki</h1>
          <Link
            href="/feedback"
            className="px-3 py-2 text-sm border border-gray-300 rounded hover:bg-gray-50 text-gray-700"
            title="Usulan pattern dari agen muncul di dashboard feedback"
          >
            📊 Feedback Agen
          </Link>
        </div>

        <div className="mb-6 p-4 rounded bg-amber-50 border border-amber-200 text-amber-900 text-sm">
          <strong>🚧 Segera hadir.</strong> Kerangka fitur Knowledge sudah disiapkan; substansi
          (sinkron wiki, editor pattern/konteks, pemantauan usulan pattern) akan diisi kemudian.
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {SECTIONS.map((s) => (
            <div
              key={s.title}
              className="bg-white border border-dashed border-gray-300 rounded-lg p-5"
            >
              <h2 className="font-semibold text-primary-dark mb-2">{s.title}</h2>
              <p className="text-sm text-gray-500">{s.desc}</p>
              <div className="mt-3 text-xs text-gray-400 italic">Substansi menyusul.</div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
