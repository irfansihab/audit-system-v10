'use client';

// Knowledge > Template KP/PKP — jelajah template Kartu Penugasan & Program
// Kerja Pengawasan per skill. File sumber: wiki/templates/{kp,pkp}/*.md
// (revisi via git/PR; dipakai form tahapan 1–2 INTEGRAL).

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getSession, Session } from '@/lib/api';
import { AppShell } from '@/components/AppShell';
import { TemplateKpPkpPanel } from '../panels';

export default function KnowledgeTemplatePage() {
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
        <h1 className="text-2xl font-bold text-primary-dark mb-1">Template KP/PKP</h1>
        <p className="text-sm text-gray-500 mb-5">
          Template Kartu Penugasan &amp; Program Kerja Pengawasan terkurasi per skill — dipakai form
          tahapan 1–2 di halaman penugasan. File di <code>wiki/templates/</code>, revisi via git.
        </p>
        <TemplateKpPkpPanel />
      </div>
    </AppShell>
  );
}
