'use client';

// Chat AI berbasis pengetahuan wiki (RAG). Cikal bakal chatbot WA/Telegram.
// Pertanyaan bebas → jawaban ber-grounding wiki + daftar sumber. Anti-halusinasi.

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, getSession, Session } from '@/lib/api';
import { AppShell } from '@/components/AppShell';

type Msg = {
  role: 'user' | 'assistant';
  content: string;
  sources?: { jenis: string; nama: string; summary: string }[];
};

const CONTOH = [
  'Apa ambang nilai Pengadaan Langsung konstruksi menurut Perpres terbaru?',
  'Kapan RUP paling lambat diumumkan?',
  'Apa saja aspek pemeriksaan reviu RKA-K/L?',
  'Pattern temuan apa yang sering muncul di pengadaan e-katalog?',
];

export default function ChatPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setMounted(true);
    const s = getSession();
    setSession(s);
    if (!s) router.push('/login');
  }, [router]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [msgs, busy]);

  const send = async (q?: string) => {
    const question = (q ?? input).trim();
    if (!question || busy) return;
    setError(null);
    const history = msgs.map((m) => ({ role: m.role, content: m.content }));
    setMsgs((prev) => [...prev, { role: 'user', content: question }]);
    setInput('');
    setBusy(true);
    try {
      const r = await api.chatAsk(question, history);
      setMsgs((prev) => [...prev, { role: 'assistant', content: r.answer, sources: r.sources }]);
    } catch (e: any) {
      setError(e.message);
      setMsgs((prev) => [...prev, { role: 'assistant', content: '⚠ Maaf, gagal menjawab. ' + e.message }]);
    } finally {
      setBusy(false);
    }
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto p-6 flex flex-col" style={{ height: 'calc(100vh - 3rem)' }}>
        <h1 className="text-2xl font-bold text-primary-dark mb-1">🤖 Chat AI — Pengetahuan Wiki</h1>
        <p className="text-sm text-gray-500 mb-4">
          Tanya bebas; jawaban <b>ber-grounding wiki tim</b> (pattern temuan, regulasi terverifikasi, catatan)
          dengan sumber yang bisa ditelusuri. Bila info belum ada di wiki, AI menyatakannya jujur — tidak
          mengarang. <span className="text-gray-400">(Cikal bakal chatbot WA/Telegram.)</span>
        </p>

        <div className="flex-1 overflow-y-auto border border-gray-200 rounded-lg bg-gray-50/50 p-4 space-y-4">
          {msgs.length === 0 && (
            <div className="text-sm text-gray-500">
              <p className="mb-2">Contoh pertanyaan:</p>
              <div className="flex flex-wrap gap-2">
                {CONTOH.map((c) => (
                  <button
                    key={c}
                    onClick={() => send(c)}
                    className="text-left text-xs px-3 py-1.5 rounded-full border border-primary-200 text-primary hover:bg-primary-50"
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
          )}
          {msgs.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm whitespace-pre-wrap ${
                  m.role === 'user'
                    ? 'bg-primary text-white rounded-br-sm'
                    : 'bg-white border border-gray-200 text-gray-800 rounded-bl-sm'
                }`}
              >
                {m.content}
                {m.sources && m.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-100 flex flex-wrap gap-1">
                    <span className="text-[10px] text-gray-400 mr-1">Sumber wiki:</span>
                    {m.sources.map((s, j) => (
                      <span
                        key={j}
                        title={s.summary}
                        className={`text-[10px] px-1.5 py-0.5 rounded border ${
                          s.jenis === 'regulasi'
                            ? 'bg-amber-50 text-amber-700 border-amber-200'
                            : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                        }`}
                      >
                        {s.nama}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {busy && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-2.5 text-sm text-gray-400 italic">
                AI sedang mencari di wiki &amp; menyusun jawaban…
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {error && <div className="mt-2 text-xs text-red-600">{error}</div>}

        <form
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
          className="mt-3 flex gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tanya apa saja tentang pengawasan, regulasi, pattern temuan…"
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-primary"
            disabled={busy}
          />
          <button
            type="submit"
            disabled={busy || !input.trim()}
            className="px-5 py-2.5 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-primary-dark disabled:opacity-50"
          >
            Kirim
          </button>
        </form>
      </div>
    </AppShell>
  );
}
