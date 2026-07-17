'use client';

// Knowledge > Pattern Temuan.
// Semua role: jelajah pattern terkurasi. PT/PM: promosi pattern baru dari
// feedback agen + graduasi skill dari penugasan sejenis (pengelolaan pattern).

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getSession, Session } from '@/lib/api';
import { AppShell } from '@/components/AppShell';
import { PatternLibraryPanel, PatternMonitorPanel } from '../panels';

export default function KnowledgePatternPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    setMounted(true);
    const s = getSession();
    setSession(s);
    if (!s) router.push('/login');
  }, [router]);

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  const isPtPm = session.role_aktif === 'PT' || session.role_aktif === 'PM';

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-primary-dark mb-1">Pattern Temuan</h1>
        <p className="text-sm text-gray-500 mb-5">
          Pattern terkurasi yang dipakai agen sebagai acuan menyusun temuan.
          {isPtPm
            ? ' Pengelolaan (promosi pattern baru & graduasi skill) ada di bawah.'
            : ' Promosi pattern baru dilakukan Pengendali Teknis/Mutu.'}
        </p>

        <PatternLibraryPanel />

        {isPtPm && <PatternMonitorPanel />}
        {/* Graduasi skill pindah ke Knowledge > Kelola Skill (satu rumah dgn
            baca/buat/edit skill). */}
      </div>
    </AppShell>
  );
}
