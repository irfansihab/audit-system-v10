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
}: {
  penugasanId: number;
  level: 'KT' | 'PT';
  canEdit: boolean;
}) {
  const [data, setData] = useState<any>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.getLembarReviu(penugasanId, level).then(setData).catch(() => {});
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

      <div className="px-5 py-3 border-t border-gray-100">
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
            <button onClick={() => save(true)} disabled={saving}
              className="px-4 py-1.5 text-sm rounded bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50">
              ✍ Paraf & Simpan
            </button>
          </div>
        ) : (
          <p className="text-xs text-gray-400">Read-only — diisi {level === 'KT' ? 'Ketua Tim' : 'Pengendali Teknis/Mutu'}.</p>
        )}
      </div>
    </div>
  );
}
