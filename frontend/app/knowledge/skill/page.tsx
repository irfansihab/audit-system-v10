'use client';

// Knowledge > Kelola Skill — satu tempat untuk seluruh pengelolaan skill:
// baca skill eksisting (SKILL.md + references), buat skill baru dari 0,
// edit skill, dan graduasi skill dari penugasan nyata.
// Baca: semua role. Edit/buat: HANYA Pengendali Teknis (dua lapis, UI + API).
// Graduasi: PT/PM (mengikuti aturan panel graduasi yang sudah ada).

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, getSession, Session, SkillInfo } from '@/lib/api';
import { AppShell } from '@/components/AppShell';
import { GraduasiPanel } from '../panels';

const TEMPLATE_SKILL = (slug: string) => `---
name: ${slug || 'nama-skill'}
jenis: Reviu (ganti — mis. "Audit (kinerja)" / "Evaluasi (LKE)" / "Pemantauan")
format_laporan: kksa
dasar-hukum: [DIISI — standar/pedoman yang jadi tulang punggung skill ini]
kode-surat: PW.04.04
tingkat-keyakinan: terbatas
version: "0.1"
changelog:
  - v0.1: draft awal dibuat dari template Kelola Skill.
---

# Skill: [Nama Skill]

> **Skill ini = substansi domain (portabel).** Cara menjalankan — urutan langkah,
> peran AT/KT/PM, titik HITL — diatur orkestrator, BUKAN di sini. Skill hanya
> menetapkan **APA** yang dinilai dan **FORMAT** keluarannya. Temuan direkam
> sebagai **K/K/S/A** (Sebab anti-mengarang: bila tak terbukti, tulis
> "Tidak ditemukan penyebab"/"Tidak cukup data" — jangan mengarang).

## Lingkup & Paradigma

[DIISI — siapa auditor-nya, apa yang direviu/diaudit, batas keyakinan.]

## Aspek yang Dinilai

1. [DIISI — aspek 1, diikat ke kriteria/pasal spesifik]
2. [DIISI — aspek 2]

## Kriteria & Dasar Hukum

[DIISI — daftar regulasi + pasal. JANGAN merujuk pasal yang belum diverifikasi;
tandai [VERIFIKASI AUDITOR] bila ragu.]

## Format Keluaran

[DIISI — struktur KKP/temuan dan laporan yang diharapkan.]

## Batasan

[DIISI — apa yang TIDAK dilakukan skill ini (mis. tidak menghitung kerugian
negara, tidak investigatif).]
`;

export default function KelolaSkillPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  const [skills, setSkills] = useState<SkillInfo[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [content, setContent] = useState('');
  const [references, setReferences] = useState<string[]>([]);
  const [refOpen, setRefOpen] = useState<string | null>(null);
  const [refContent, setRefContent] = useState('');

  // Mode kelola (PT): 'edit' skill terpilih, atau 'baru'.
  const [editing, setEditing] = useState<'edit' | 'baru' | null>(null);
  const [draft, setDraft] = useState('');
  const [newSlug, setNewSlug] = useState('');
  const [busy, setBusy] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  const isPT = session?.role_aktif === 'PT';
  const isPtPm = session?.role_aktif === 'PT' || session?.role_aktif === 'PM';

  const refresh = useCallback(async () => {
    try {
      setSkills(await api.getSkills());
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
    setEditing(null);
    setRefOpen(null);
    setRefContent('');
    setContent('');
    setErr(null);
    try {
      const r = await api.getSkillDetail(slug);
      setContent(r.content);
      setReferences(r.references);
    } catch (e: any) {
      setErr(e.message);
    }
  };

  const bukaRef = async (path: string) => {
    if (!selected) return;
    if (refOpen === path) {
      setRefOpen(null);
      return;
    }
    setRefOpen(path);
    setRefContent('Memuat…');
    try {
      const r = await api.getSkillReference(selected, path);
      setRefContent(r.content);
    } catch (e: any) {
      setRefContent(`Gagal memuat: ${e.message}`);
    }
  };

  const mulaiEdit = () => {
    setDraft(content);
    setEditing('edit');
    setMsg(null);
    setErr(null);
  };

  const mulaiBaru = () => {
    setSelected(null);
    setNewSlug('');
    setDraft(TEMPLATE_SKILL(''));
    setEditing('baru');
    setMsg(null);
    setErr(null);
  };

  const simpan = async () => {
    setBusy('simpan');
    setErr(null);
    try {
      if (editing === 'baru') {
        const r = await api.createSkill(newSlug.trim(), draft);
        setMsg(`✓ Skill '${r.slug}' dibuat (folder + SKILL.md + references/). Muncul di dropdown penugasan.`);
        setEditing(null);
        await refresh();
        await buka(r.slug);
      } else if (selected) {
        await api.updateSkillMd(selected, draft);
        setMsg(`✓ SKILL.md '${selected}' tersimpan — dipakai agen mulai run berikutnya.`);
        setEditing(null);
        await refresh();
        await buka(selected);
      }
    } catch (e: any) {
      setErr(`Ditolak (file TIDAK ditulis): ${e.message}`);
    } finally {
      setBusy(null);
    }
  };

  if (!mounted) return <main className="min-h-screen" />;
  if (!session) return null;

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-start mb-1 flex-wrap gap-2">
          <h1 className="text-2xl font-bold text-primary-dark">Kelola Skill</h1>
          {isPT && !editing && (
            <button
              onClick={mulaiBaru}
              className="px-3 py-2 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark"
            >
              ＋ Skill baru dari 0
            </button>
          )}
        </div>
        <p className="text-sm text-gray-500 mb-4">
          Skill = substansi pengawasan yang dijalankan agen (folder{' '}
          <code>knowledge/skills/&lt;slug&gt;/</code>).{' '}
          {isPT ? (
            <span>Anda Pengendali Teknis — bisa mengedit dan membuat skill. Perubahan langsung dipakai agen pada run berikutnya, jadi pastikan isinya sudah direviu.</span>
          ) : (
            <span className="text-gray-400">Hanya Pengendali Teknis yang dapat mengedit/membuat skill; role lain baca saja.</span>
          )}
        </p>

        {err && <div className="mb-3 p-3 rounded bg-red-50 border border-red-200 text-red-700 text-sm whitespace-pre-wrap">{err}</div>}
        {msg && <div className="mb-3 p-3 rounded bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">{msg}</div>}

        {editing ? (
          /* ===== Editor (PT) ===== */
          <div className="bg-white border border-amber-300 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
              <h2 className="font-semibold text-primary-dark text-sm">
                {editing === 'baru' ? 'Skill baru dari 0' : `Edit SKILL.md — ${selected}`}
              </h2>
              <span className="text-[11px] text-gray-500">
                Frontmatter wajib punya <code>name:</code> &amp; <code>jenis:</code> — divalidasi sebelum disimpan.
              </span>
            </div>
            {editing === 'baru' && (
              <div className="mb-2 flex items-center gap-2">
                <label className="text-xs text-gray-600">Slug folder:</label>
                <input
                  value={newSlug}
                  onChange={(e) => {
                    setNewSlug(e.target.value);
                    // sinkronkan name: di template bila belum diedit manual
                    setDraft((d) => d.replace(/^name: .*$/m, `name: ${e.target.value.trim() || 'nama-skill'}`));
                  }}
                  placeholder="mis. reviu-aset-tik"
                  className="border border-gray-300 rounded px-2 py-1 text-sm font-mono w-64"
                />
              </div>
            )}
            <textarea
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              spellCheck={false}
              className="w-full h-[480px] border border-gray-300 rounded p-3 font-mono text-xs leading-5 focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
            <div className="mt-3 flex gap-2">
              <button
                onClick={simpan}
                disabled={busy === 'simpan' || (editing === 'baru' && !newSlug.trim())}
                className="px-4 py-2 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50"
              >
                {busy === 'simpan' ? 'Menyimpan…' : 'Simpan'}
              </button>
              <button
                onClick={() => {
                  setEditing(null);
                  setErr(null);
                }}
                className="px-4 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50"
              >
                Batal
              </button>
            </div>
          </div>
        ) : (
          /* ===== Browser skill ===== */
          <div className="grid md:grid-cols-[280px_1fr] gap-4 mb-6">
            {/* Daftar skill */}
            <div className="bg-white border border-gray-200 rounded-lg max-h-[600px] overflow-y-auto divide-y">
              {skills.length === 0 ? (
                <div className="p-3 text-sm text-gray-400 italic">Memuat daftar skill…</div>
              ) : (
                skills.map((s) => (
                  <button
                    key={s.slug}
                    onClick={() => buka(s.slug)}
                    className={`w-full text-left p-2.5 hover:bg-blue-50/40 transition ${selected === s.slug ? 'bg-blue-50' : ''}`}
                  >
                    <div className="text-sm font-medium text-gray-800">{s.slug}</div>
                    <div className="text-[11px] text-gray-400 mt-0.5">{s.jenis || '—'}</div>
                  </button>
                ))
              )}
            </div>

            {/* Isi skill */}
            <div className="bg-white border border-gray-200 rounded-lg p-4 min-h-[320px] max-h-[600px] overflow-y-auto">
              {!selected ? (
                <p className="text-sm text-gray-400 italic">
                  Klik skill di kiri untuk membaca SKILL.md &amp; references-nya.
                </p>
              ) : (
                <>
                  <div className="flex items-center justify-between gap-2 mb-2 flex-wrap">
                    <span className="font-mono text-xs text-gray-500">{selected}/SKILL.md</span>
                    {isPT && (
                      <button
                        onClick={mulaiEdit}
                        className="text-xs px-2.5 py-1 rounded border border-primary text-primary hover:bg-primary-50"
                      >
                        ✎ Edit SKILL.md
                      </button>
                    )}
                  </div>

                  {references.length > 0 && (
                    <div className="mb-3 border border-gray-200 rounded p-2 bg-gray-50">
                      <div className="text-[11px] font-semibold text-gray-500 mb-1">
                        References ({references.length}) — klik untuk baca
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {references.map((r) => (
                          <button
                            key={r}
                            onClick={() => bukaRef(r)}
                            className={`text-[10px] px-1.5 py-0.5 rounded border font-mono ${
                              refOpen === r
                                ? 'border-primary bg-primary-50 text-primary'
                                : 'border-gray-300 bg-white text-gray-600 hover:border-primary'
                            }`}
                          >
                            {r}
                          </button>
                        ))}
                      </div>
                      {refOpen && (
                        <pre className="mt-2 text-[10px] bg-white border border-gray-200 rounded p-2 whitespace-pre-wrap font-mono text-gray-700 max-h-56 overflow-y-auto">
                          {refContent}
                        </pre>
                      )}
                    </div>
                  )}

                  <pre className="text-xs whitespace-pre-wrap font-sans text-gray-800">{content || 'Memuat…'}</pre>
                </>
              )}
            </div>
          </div>
        )}

        {/* ===== Graduasi skill (PT/PM) — suling skill baru dari penugasan nyata ===== */}
        {isPtPm && !editing && <GraduasiPanel />}
      </div>
    </AppShell>
  );
}
