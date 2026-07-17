'use client';

// Knowledge > Tulis-balik Wiki — hasil penugasan selesai (LHP_DONE) ditulis
// balik ke vault sebagai catatan riwayat pengawasan (dibaca agen di penugasan
// serupa berikutnya lewat preload konteks).

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getSession, Session } from '@/lib/api';
import { AppShell } from '@/components/AppShell';
import { WritebackPanel } from '../panels';

export default function KnowledgeWritebackPage() {
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

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-primary-dark mb-1">Tulis-balik Wiki</h1>
        <p className="text-sm text-gray-500 mb-5">
          Penugasan yang laporannya selesai ditulis balik ke vault sebagai catatan
          <code> pengawasan-*.md</code> — jadi riwayat yang dibaca agen saat menangani obyek serupa.
        </p>
        <WritebackPanel role={session.role_aktif} />
      </div>
    </AppShell>
  );
}
