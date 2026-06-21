'use client';

/**
 * LembarReviuPanel — Lembar Reviu berjenjang (format INTEGRAL/SIMWAS).
 * level "KT" (atas Kertas Kerja, tahapan 4) / "PT" (atas Konsep LHP, tahapan 6).
 * Aspek A–D baku dari backend; reviewer isi Status (+ Penyelesaian utk PT) lalu paraf.
 */
import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { api } from '@/lib/api';

const STATUS_CLS: Record<string, string> = {
  Sesuai: 'bg-emerald-50 text-emerald-700 border-emerald-300',
  'Belum Sesuai': 'bg-rose-50 text-rose-700 border-rose-300',
};

export function LembarReviuPanel({
  penugasanId,
  level,
  canEdit,
  onReviewed,
}: {
  penugasanId: number;
  level: 'KT' | 'PT' | 'PM';
  canEdit: boolean;
  // Hanya level PT: keputusan reviu konsep LHP (Setujui / Minta Revisi).
  onReviewed?: (status: 'APPROVED' | 'NEEDS_REVISION' | null) => void;
}) {
  const [data, setData] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  // Keputusan reviu konsep LHP (level PT) — menggantikan panel approve lama.
  const [verdict, setVerdict] = useState<'APPROVED' | 'NEEDS_REVISION' | null>(null);
  const [catatan, setCatatan] = useState('');
  const [verdictBusy, setVerdictBusy] = useState(false);

  useEffect(() => {
    api.getLembarReviu(penugasanId, level).then(setData).catch(() => {});
    if (level === 'PT') {
      api.listLhpReview(penugasanId).then((r) => setVerdict(r.latest_status)).catch(() => {});
    }
  }, [penugasanId, level]);

  if (!data) return <p className="text-sm text-gray-400">Memuat lembar reviu…</p>;

  const setAspek = (kode: string, patch: any) =>
    setData((d: any) => ({
      ...d,
      aspek: d.aspek.map((a: any) => (a.kode === kode ? { ...a, ...patch } : a)),
    }));

  const save = async (paraf: boolean) => {
    setSaving(true);
    try {
      const body = {
        items: data.aspek.map((a: any) => ({
          kode: a.kode,
          status: a.status,
          penyelesaian: data.has_penyelesaian ? a.penyelesaian : undefined,
        })),
        catatan: data.catatan || null,
        diparaf: paraf,
      };
      const res = await api.saveLembarReviu(penugasanId, level, body);
      setData(res);
      toast.success(paraf ? 'Lembar reviu diparaf & disimpan.' : 'Lembar reviu disimpan (draft).');
    } catch (e: any) {
      toast.error(`Gagal menyimpan: ${e?.message || e}`);
    } finally {
      setSaving(false);
    }
  };

  // Keputusan reviu konsep LHP (level PT) — menyatu dengan lembar reviu aspek.
  // APPROVED juga otomatis menarik rekomendasi LHP ke TLHP (backend).
  const submitVerdict = async (status: 'APPROVED' | 'NEEDS_REVISION') => {
    if (status === 'NEEDS_REVISION' && !catatan.trim()) {
      toast.error('Catatan revisi wajib diisi saat meminta revisi.');
      return;
    }
    setVerdictBusy(true);
    try {
      // Setuju = paraf lembar aspek sekaligus, lalu catat keputusan.
      if (status === 'APPROVED') await save(true);
      await api.createLhpReview(penugasanId, status, catatan.trim() || undefined);
      setVerdict(status);
      onReviewed?.(status);
      toast.success(
        status === 'APPROVED'
          ? 'Konsep LHP disetujui & diparaf. Rekomendasi otomatis ditarik ke TLHP.'
          : 'Revisi diminta — dikembalikan ke Ketua Tim.',
      );
    } catch (e: any) {
      toast.error(`Gagal: ${e?.message || e}`);
    } finally {
      setVerdictBusy(false);
    }
  };

  return (
    <div className="rounded-2xl border border-gray-200 bg-white overflow-hidden">
      <div className="px-5 py-3 border-b border-gray-100 flex items-center justify-between">
        <h3 className="text-sm font-bold text-primary-dark">» {data.judul}</h3>
        {data.diparaf && <span className="text-xs text-emerald-600 font-medium">✓ Sudah diparaf</span>}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-gray-500 bg-gray-50 border-b border-gray-100">
              <th className="px-3 py-2 w-8">No</th>
              <th className="px-3 py-2">Permasalahan</th>
              {data.has_penyelesaian && <th className="px-3 py-2">Penyelesaian</th>}
              <th className="px-3 py-2 w-36">Status</th>
            </tr>
          </thead>
          <tbody>
            {data.aspek.map((a: any) => (
              <tr key={a.kode} className="border-b border-gray-50 align-top">
                <td className="px-3 py-3 font-semibold text-gray-600">{a.kode}</td>
                <td className="px-3 py-3">
                  <div className="font-semibold text-gray-800">{a.aspek}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{a.deskripsi}</div>
                </td>
                {data.has_penyelesaian && (
                  <td className="px-3 py-3">
                    {canEdit && !data.diparaf ? (
                      <textarea
                        value={a.penyelesaian || ''}
                        onChange={(e) => setAspek(a.kode, { penyelesaian: e.target.value })}
                        className="w-full text-xs border border-gray-200 rounded p-1.5 min-h-[48px]"
                      />
                    ) : (
                      <span className="text-xs text-gray-700">{a.penyelesaian}</span>
                    )}
                  </td>
                )}
                <td className="px-3 py-3">
                  {canEdit && !data.diparaf ? (
                    <select
                      value={a.status}
                      onChange={(e) => setAspek(a.kode, { status: e.target.value })}
                      className={`text-xs border rounded px-2 py-1 ${STATUS_CLS[a.status] || 'border-gray-300'}`}
                    >
                      {data.status_options.map((s: string) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  ) : (
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_CLS[a.status] || 'bg-gray-100'}`}>{a.status}</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="px-5 py-3 border-t border-gray-100 space-y-3">
        {data.diparaf ? (
          <div className="text-xs text-gray-600">
            Disusun oleh <strong>{data.reviewer_nama || '—'}</strong>
            {data.reviewer_nip ? ` · NIP ${data.reviewer_nip}` : ''}
            {data.tanggal ? ` · ${data.tanggal}` : ''}
            {canEdit && (
              <button onClick={() => save(false)} disabled={saving}
                className="ml-3 text-primary hover:underline disabled:opacity-50">Buka kembali (edit)</button>
            )}
          </div>
        ) : canEdit ? (
          <div className="flex gap-2">
            <button onClick={() => save(false)} disabled={saving}
              className="px-3 py-1.5 text-sm rounded border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50">
              Simpan draft
            </button>
            {/* Paraf lembar aspek: KT (self-review) & PM (QA/QC) berdiri sendiri;
                untuk PT menyatu di tombol "Paraf & Setujui Konsep LHP" di bawah. */}
            {level !== 'PT' && (
              <button onClick={() => save(true)} disabled={saving}
                className="px-4 py-1.5 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50">
                ✍ Paraf & Simpan
              </button>
            )}
          </div>
        ) : (
          <p className="text-xs text-gray-400">Read-only — diisi {level === 'KT' ? 'Ketua Tim' : 'Pengendali Teknis/Mutu'}.</p>
        )}

        {/* Keputusan reviu konsep LHP — hanya PT/PM. Menggantikan panel approve
            terpisah (sebelumnya redundan): aspek + keputusan kini satu lembar. */}
        {level === 'PT' && (
          <div className="border-t border-dashed border-gray-200 pt-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-gray-700">Keputusan Reviu Konsep LHP</span>
              {verdict === 'APPROVED' && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-medium">✓ Konsep LHP Disetujui</span>
              )}
              {verdict === 'NEEDS_REVISION' && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 font-medium">⟳ Perlu Revisi</span>
              )}
            </div>
            {canEdit ? (
              <>
                <textarea
                  value={catatan}
                  onChange={(e) => setCatatan(e.target.value)}
                  placeholder="Catatan reviu (wajib bila minta revisi)"
                  className="w-full text-xs border border-gray-200 rounded p-2 min-h-[56px]"
                />
                <div className="flex flex-wrap gap-2 mt-2">
                  <button onClick={() => submitVerdict('APPROVED')} disabled={verdictBusy || saving}
                    className="px-4 py-1.5 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50">
                    ✍ Paraf &amp; Setujui Konsep LHP
                  </button>
                  <button onClick={() => submitVerdict('NEEDS_REVISION')} disabled={verdictBusy}
                    className="px-4 py-1.5 text-sm rounded border border-amber-400 text-amber-700 hover:bg-amber-50 disabled:opacity-50">
                    ⟳ Minta Revisi
                  </button>
                </div>
                <p className="text-[11px] text-gray-400 mt-1">
                  Setujui → lembar aspek diparaf, rekomendasi LHP otomatis ditarik ke TLHP, laporan lanjut ke finalisasi.
                </p>
              </>
            ) : (
              <p className="text-xs text-gray-400">
                {verdict === 'APPROVED'
                  ? 'Konsep LHP sudah disetujui PT/PM.'
                  : verdict === 'NEEDS_REVISION'
                    ? 'PT/PM meminta revisi konsep LHP.'
                    : 'Menunggu reviu Pengendali Teknis/Mutu.'}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
