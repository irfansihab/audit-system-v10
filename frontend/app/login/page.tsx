'use client';

/**
 * Login INTEGRAL (Workstream B) — username + password.
 * Plus "Login cepat (dev)": kartu per akun yang AUTO-ISI username+password
 * lalu masuk — untuk testing cepat berbagai role. Di produksi, matikan bagian dev.
 */
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, setToken, setSession, Role, User } from '@/lib/api';

// Password dev bersama (selaras backend init_db.DEV_PASSWORD). Hanya untuk dev.
const DEV_PASSWORD = 'audit2026';

const ROLE_META: Record<string, { label: string; cls: string }> = {
  PT: { label: 'Pengendali Teknis', cls: 'bg-purple-100 text-purple-800' },
  PM: { label: 'Pengendali Mutu', cls: 'bg-fuchsia-100 text-fuchsia-800' },
  KT: { label: 'Ketua Tim', cls: 'bg-emerald-100 text-emerald-800' },
  AT: { label: 'Anggota Tim', cls: 'bg-blue-100 text-blue-800' },
};

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    api.listUsers().then(setUsers).catch(() => setUsers([]));
  }, []);

  const doLogin = async (un: string, pw: string, tag: string) => {
    setLoading(tag);
    setError(null);
    try {
      const session = await api.login({ username: un, password: pw });
      setToken(session.token);
      setSession(session);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Gagal masuk');
    } finally {
      setLoading(null);
    }
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) { setError('Isi username dan password.'); return; }
    doLogin(username, password, 'form');
  };

  // Quick-login dev: isi form (auto-fill) lalu masuk.
  const quick = (u: User) => {
    const un = u.username || '';
    setUsername(un);
    setPassword(DEV_PASSWORD);
    doLogin(un, DEV_PASSWORD, un);
  };

  return (
    <main className="min-h-screen flex items-center justify-center px-6 bg-gradient-to-br from-primary-50 to-white">
      <div className="w-full max-w-md">
        <div className="flex items-center gap-3 mb-8 justify-center">
          <div className="w-14 h-14 rounded-xl bg-primary text-white font-bold text-2xl flex items-center justify-center shadow-lg">∫</div>
          <div>
            <h1 className="text-2xl font-bold text-primary-dark">INTEGRAL</h1>
            <p className="text-sm text-gray-500">Workspace Pengawasan · Inspektorat II Komdigi</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Masuk</h2>

          {error && (
            <div className="mb-4 p-3 rounded-md bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
          )}

          <form onSubmit={submit} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Username</label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/40 focus:border-primary outline-none"
                placeholder="mis. budi"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/40 focus:border-primary outline-none"
                placeholder="••••••••"
              />
            </div>
            <button
              type="submit"
              disabled={loading !== null}
              className="w-full py-2.5 rounded-lg bg-primary text-white font-semibold hover:bg-primary-dark transition disabled:opacity-50"
            >
              {loading === 'form' ? 'Memproses…' : 'Masuk'}
            </button>
          </form>

          {/* Login cepat (dev) — auto-isi username+password per role */}
          {users.length > 0 && (
            <div className="mt-6 pt-5 border-t border-gray-100">
              <p className="text-xs text-gray-400 mb-2">⚡ Login cepat (dev) — klik untuk masuk sebagai:</p>
              <div className="grid grid-cols-2 gap-2">
                {users.map((u) => {
                  const r = String(u.role_default);
                  const meta = ROLE_META[r] || { label: r, cls: 'bg-gray-100 text-gray-700' };
                  return (
                    <button
                      key={u.id}
                      onClick={() => quick(u)}
                      disabled={loading !== null || !u.username}
                      title={`@${u.username} · ${meta.label}`}
                      className="text-left px-3 py-2 border border-gray-200 rounded-lg hover:border-primary hover:bg-primary/5 transition disabled:opacity-40"
                    >
                      <div className="flex items-center gap-1.5 mb-0.5">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${meta.cls}`}>{r}</span>
                        <span className="text-[11px] text-gray-400">
                          {loading === u.username ? '⏳' : `@${u.username}`}
                        </span>
                      </div>
                      <div className="text-xs font-medium text-gray-800 truncate">{u.nama_lengkap}</div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          <p className="mt-5 text-xs text-gray-400 text-center">
            Produksi nanti via SSO Komdigi (OIDC). Login cepat dimatikan di produksi.
          </p>
        </div>
      </div>
    </main>
  );
}
