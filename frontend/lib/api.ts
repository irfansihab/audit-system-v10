// API client untuk backend Audit AI v7.

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('audit_v7_token');
}

export function setToken(token: string): void {
  localStorage.setItem('audit_v7_token', token);
}

export function clearToken(): void {
  localStorage.removeItem('audit_v7_token');
  localStorage.removeItem('audit_v7_session');
}

export function getSession(): Session | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem('audit_v7_session');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Session;
  } catch {
    // Session korup/format lama — dulu throw di sini men-crash SELURUH halaman
    // (dipanggil saat render) sampai user membersihkan localStorage manual. (#F9)
    clearToken();
    return null;
  }
}

export function setSession(session: Session): void {
  localStorage.setItem('audit_v7_session', JSON.stringify(session));
}

async function request<T>(
  path: string,
  init: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(init.headers as Record<string, string>),
  };
  if (!(init.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
  });
  if (!res.ok) {
    const text = await res.text();
    // Sesi kedaluwarsa / token tak valid → bersihkan & arahkan ke login.
    // Dikecualikan: endpoint login (401 = kredensial salah, biar pesan tampil).
    if (
      res.status === 401 &&
      !path.startsWith('/auth/login') &&
      typeof window !== 'undefined' &&
      window.location.pathname !== '/login'
    ) {
      clearToken();
      window.location.href = '/login?expired=1';
    }
    throw new Error(`${res.status}: ${text}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

// ===== Types =====
export type Role = 'AT' | 'KT' | 'PT' | 'PM' | 'TU' | 'ADMIN';
// Skill kini folder-driven di backend (registry) — bukan enum tetap. Tetap
// alias `string` supaya komponen lama yang mereferensikan `Skill` tidak rusak.
export type Skill = string;

export interface SkillInfo {
  slug: string;
  name: string;
  jenis: string;
  output: string;
  has_pipeline: boolean;
}


export interface User {
  id: number;
  username?: string | null;
  email: string;
  nama_lengkap: string;
  nip: string;
  role_default: Role;
}

export interface Session {
  user: User;
  role_aktif: Role;
  token: string;
}

export interface Penugasan {
  id: number;
  kode: string;
  obyek: string;
  skill: Skill;
  nomor_st: string | null;
  tanggal_st: string | null;
  status: string;
  folder_path: string;
  created_at: string;
  updated_at: string;
}

export interface Dokumen {
  id: number;
  penugasan_id: number;
  nama_file: string;
  jenis: string | null;
  sha256: string;
  size_bytes: number;
  status: 'UPLOADED' | 'INGESTING' | 'READY' | 'FAILED';
  ingested_json_path: string | null;
  error_message: string | null;
  uploaded_at: string;
  ingested_at: string | null;
}

// ===== API =====
export const api = {
  /** Login (Workstream B): username + password. Jalur legacy {role,email} masih
   * didukung backend di dev (untuk transisi), tapi UI utama pakai username+password. */
  login: (body: { username?: string; password?: string; role?: Role; email?: string }) =>
    request<Session>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  /** Ganti password sendiri (B4). Perlu sesi aktif + password lama benar. */
  changePassword: (old_password: string, new_password: string) =>
    request<void>('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ old_password, new_password }),
    }),

  /** Daftar user seed (opsional filter role). Dipakai layar login untuk
   * memilih orang saat satu role punya >1 user (mis. beberapa Anggota Tim),
   * dan oleh KT untuk dropdown assignment sasaran. Publik (prototype). */
  listUsers: (role?: Role) =>
    request<User[]>(`/auth/users${role ? `?role=${role}` : ''}`),

  /** Daftar skill pengawasan terdaftar (folder-driven) untuk dropdown. */
  getSkills: () => request<SkillInfo[]>('/skills'),

  // ===== Kelola Skill (Knowledge > Kelola Skill) =====

  /** Detail 1 skill: isi SKILL.md + daftar reference. */
  getSkillDetail: (slug: string) =>
    request<{ slug: string; content: string; references: string[] }>(
      `/skills/${encodeURIComponent(slug)}`
    ),

  /** Baca isi 1 file reference skill (read-only). */
  getSkillReference: (slug: string, path: string) =>
    request<{ slug: string; path: string; binary: boolean; content: string }>(
      `/skills/${encodeURIComponent(slug)}/reference?path=${encodeURIComponent(path)}`
    ),

  /** Simpan perubahan SKILL.md — PT only (validasi frontmatter di backend). */
  updateSkillMd: (slug: string, content: string) =>
    request<{ ok: boolean; slug: string }>(`/skills/${encodeURIComponent(slug)}`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    }),

  /** Buat skill baru dari 0 — PT only. */
  createSkill: (slug: string, content: string) =>
    request<{ ok: boolean; slug: string; path: string }>('/skills', {
      method: 'POST',
      body: JSON.stringify({ slug, content }),
    }),

  /** Render Laporan Survei Pendahuluan (.docx) — HANYA skill audit (Fase 2 merge v8.8). */
  renderSurveyPendahuluan: (penugasanId: number) =>
    request<{ ok: boolean; path: string; name: string }>(
      `/penugasan/${penugasanId}/survey-pendahuluan`,
      { method: 'POST' },
    ),

  /** Ringkasan beranda (1 panggilan, di-cache backend ~30s) — widget dashboard. */
  getDashboardSummary: () => request<any>('/dashboard/summary'),

  /** Lembar Reviu berjenjang (level KT / PT) — aspek baku + isian + paraf. */
  getLembarReviu: (penugasanId: number, level: 'KT' | 'PT' | 'PM') =>
    request<any>(`/penugasan/${penugasanId}/lembar-reviu/${level}`),
  saveLembarReviu: (penugasanId: number, level: 'KT' | 'PT' | 'PM', body: any) =>
    request<any>(`/penugasan/${penugasanId}/lembar-reviu/${level}`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  // ===== Administrasi (Tahapan 8 — TU, pasca-persetujuan) =====
  getAdministrasi: (penugasanId: number) =>
    request<any>(`/penugasan/${penugasanId}/administrasi`),
  buatSuratPenyampaian: (
    penugasanId: number,
    body: { nomor?: string; tanggal?: string; tujuan?: string; perihal?: string; auditi?: string },
  ) =>
    request<{ ok: boolean; path: string; name: string }>(
      `/penugasan/${penugasanId}/administrasi/surat-penyampaian`,
      { method: 'POST', body: JSON.stringify(body) },
    ),
  uploadKelengkapan: (penugasanId: number, kode: string, file: File) => {
    const fd = new FormData();
    fd.append('kode', kode);
    fd.append('file', file);
    return request<{ ok: boolean; kode: string; name: string; path: string }>(
      `/penugasan/${penugasanId}/administrasi/kelengkapan`,
      { method: 'POST', body: fd },
    );
  },
  hapusKelengkapan: (penugasanId: number, path: string) =>
    request<{ ok: boolean }>(
      `/penugasan/${penugasanId}/administrasi/kelengkapan?path=${encodeURIComponent(path)}`,
      { method: 'DELETE' },
    ),

  /** Daftar rekomendasi TLHP (ber-aging). Filter opsional satker/status. */
  listTlhp: (params?: { satker_kode?: string; status?: string }) => {
    const qs = new URLSearchParams();
    if (params?.satker_kode) qs.set('satker_kode', params.satker_kode);
    if (params?.status) qs.set('status', params.status);
    const q = qs.toString();
    return request<{ total: number; items: any[] }>(`/tlhp${q ? `?${q}` : ''}`);
  },

  // ===== Graduasi (meta-skill) =====
  getGraduasiCandidates: () =>
    request<{ groups: { skill: string; penugasan: { kode: string; obyek: string; n_temuan: number }[] }[] }>(
      '/graduasi/candidates'
    ),
  getGraduasiDrafts: () =>
    request<{ drafts: { nama: string; fungsi?: string; skill_induk?: string; n_temuan?: number; generated_at?: string }[] }>(
      '/graduasi/drafts'
    ),
  runGraduasi: (penugasanKodes: string[], nama?: string) =>
    request<{ ok: boolean; nama: string; n_temuan: number; n_redflag: number; sumber_penugasan: string[] }>(
      '/graduasi/run',
      { method: 'POST', body: JSON.stringify({ penugasan_kodes: penugasanKodes, nama }) }
    ),
  promoteGraduasi: (nama: string) =>
    request<{ ok: boolean; nama: string; skill_terdaftar: boolean }>('/graduasi/promote', {
      method: 'POST',
      body: JSON.stringify({ nama }),
    }),
  rejectGraduasi: (nama: string) =>
    request<{ ok: boolean; nama: string }>('/graduasi/reject', {
      method: 'POST',
      body: JSON.stringify({ nama }),
    }),

  listPenugasan: () => request<Penugasan[]>('/penugasan'),

  getPenugasan: (id: number) => request<Penugasan>(`/penugasan/${id}`),

  /** Hapus penugasan + seluruh file di disk (hard delete). Hanya PT. */
  deletePenugasan: (id: number) =>
    request<{ ok: boolean; deleted: string; folder_removed: string }>(
      `/penugasan/${id}`,
      { method: 'DELETE' }
    ),

  createPenugasan: (payload: {
    obyek: string;
    skill: Skill;
    nomor_st?: string;
    tanggal_st?: string;
  }) =>
    request<Penugasan>('/penugasan', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  listDokumen: (penugasanId: number) =>
    request<Dokumen[]>(`/dokumen?penugasan_id=${penugasanId}`),

  uploadDokumen: async (penugasanId: number, file: File, jenis?: string) => {
    const fd = new FormData();
    fd.append('penugasan_id', String(penugasanId));
    fd.append('file', file);
    if (jenis) fd.append('jenis', jenis);
    return request<Dokumen>('/dokumen', { method: 'POST', body: fd });
  },

  /** Hapus 1 dokumen (file + hasil ingest) lalu reset analisis turunan. Hanya AT. */
  deleteDokumen: (dokumenId: number) =>
    request<{ ok: boolean; deleted: string; reset_downstream: string[] }>(
      `/dokumen/${dokumenId}`,
      { method: 'DELETE' }
    ),

  triggerIngestion: (penugasanId: number) =>
    request<{ penugasan_id: number; reset_downstream: string[]; dokumen_diproses: any[] }>(
      `/agen/ingest/${penugasanId}`,
      { method: 'POST' }
    ),

  /** URL untuk EventSource SSE — bukan fetch(). */
  agentStreamUrl: (
    agent: 'ingestion' | 'anggota_tim' | 'ketua_tim' | 'qc_saipi',
    penugasanId: number,
    prompt: string
  ) => {
    const token = getToken() || '';
    const qs = new URLSearchParams({
      penugasan_id: String(penugasanId),
      prompt,
    });
    // Token via query param (EventSource tidak mendukung custom headers di browser
    // standar). Untuk produksi, gunakan cookie session.
    return `${API_BASE}/agen/${agent}/stream?${qs.toString()}&_token=${encodeURIComponent(token)}`;
  },

  /** URL EventSource untuk RECONNECT ke run aktif (replay buffer + tail).
   * Bila tak ada run aktif, server kirim event `idle` lalu tutup. */
  agentAttachUrl: (
    agent: 'ingestion' | 'anggota_tim' | 'ketua_tim' | 'qc_saipi',
    penugasanId: number
  ) => {
    const token = getToken() || '';
    const qs = new URLSearchParams({ penugasan_id: String(penugasanId) });
    return `${API_BASE}/agen/${agent}/attach?${qs.toString()}&_token=${encodeURIComponent(token)}`;
  },

  /** Cek cepat (non-stream) apakah ada run agen aktif di backend. */
  getActiveRun: (
    agent: 'ingestion' | 'anggota_tim' | 'ketua_tim' | 'qc_saipi',
    penugasanId: number
  ) =>
    request<{ active: boolean; run_id?: number; text_so_far?: string }>(
      `/agen/${agent}/active?penugasan_id=${penugasanId}`
    ),
  /** History semua run agen pada penugasan ini, urutan oldest → newest.
   * Dipakai untuk persist percakapan lampau saat user login ulang. */
  getAgentHistory: (
    agent: 'ingestion' | 'anggota_tim' | 'ketua_tim' | 'qc_saipi',
    penugasanId: number
  ) =>
    request<{
      agent_name: string;
      penugasan_id: number;
      total: number;
      runs: Array<{
        id: number;
        status: string;
        input_summary: string;
        output_summary: string;
        tool_calls: Array<{ tool: string; input: any }>;
        tokens_in: number;
        tokens_out: number;
        started_at: string | null;
        ended_at: string | null;
        error_message: string | null;
      }>;
    }>(`/agen/${agent}/history?penugasan_id=${penugasanId}`),

  // ===== File output access =====

  listFiles: (penugasanId: number) =>
    request<{
      penugasan_id: number;
      folder_path: string;
      categories: Array<{
        key: string;
        label: string;
        files: Array<{
          name: string;
          path: string;
          size_bytes: number;
          mtime: string;
          ext: string;
        }>;
      }>;
    }>(`/penugasan/${penugasanId}/files`),

  /** Download file sebagai Blob — pakai untuk Save As / open. */
  downloadFile: async (penugasanId: number, path: string): Promise<Blob> => {
    const token = getToken() || '';
    const url = `${API_BASE}/penugasan/${penugasanId}/files/download?path=${encodeURIComponent(path)}`;
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
    return res.blob();
  },

  /** Preview text-based file (.md, .json, .txt). Return content string. */
  previewFile: (penugasanId: number, path: string, maxBytes = 50_000) =>
    request<{
      path: string;
      size_bytes: number;
      ext: string;
      truncated: boolean;
      content: string;
    }>(`/penugasan/${penugasanId}/files/preview?path=${encodeURIComponent(path)}&max_bytes=${maxBytes}`),

  // ===== Setup Penugasan (Ketua Tim only — endpoint return 403 untuk AT) =====

  getSasaranAssignment: (penugasanId: number) =>
    request<{
      penugasan_id: string;
      skill: string;
      schema_version: string;
      sasaran: Array<{
        sasaran_id: string;
        deskripsi: string;
        assigned_to: string[];
        langkah_kerja: string[];
        status: string;
        waktu?: string;
        no_kkp?: string;
      }>;
      // Meta PKP format INTEGRAL (opsional — file lama belum punya)
      nomor_pkp?: string;
      langkah_perencanaan?: Array<{ langkah: string; pelaksana: string; waktu: string }>;
      langkah_pelaporan?: Array<{ langkah: string; pelaksana: string; waktu: string }>;
    }>(`/penugasan/${penugasanId}/sasaran-assignment`),

  saveSasaranAssignment: (
    penugasanId: number,
    sasaran: Array<{
      sasaran_id: string;
      deskripsi: string;
      assigned_to: string[];
      langkah_kerja: string[];
      status: string;
      waktu?: string;
      no_kkp?: string;
    }>,
    meta?: {
      nomor_pkp?: string;
      langkah_perencanaan?: Array<{ langkah: string; pelaksana: string; waktu: string }>;
      langkah_pelaporan?: Array<{ langkah: string; pelaksana: string; waktu: string }>;
    }
  ) =>
    request<{ ok: boolean; total_sasaran: number; path: string }>(
      `/penugasan/${penugasanId}/sasaran-assignment`,
      { method: 'PUT', body: JSON.stringify({ sasaran, ...(meta || {}) }) }
    ),

  // ===== Preload Context Bundle (Prioritas 1 — peningkatan kualitas output agen) =====
  /** Bangun bundle konteks pra-loaded (vault + pattern + glossary + riwayat W3) */
  buildPreloadContext: (penugasanId: number) =>
    request<{
      ok: boolean;
      path: string;
      stats: {
        char_count: number;
        n_vault_notes: number;
        n_patterns: number;
        n_konteks: number;
        n_writeback_history: number;
        vault_keywords: string[];
      };
    }>(`/penugasan/${penugasanId}/preload-context`, { method: 'POST' }),

  /** Cek status bundle (apakah sudah dibangun + statistik). */
  getPreloadContextStatus: (penugasanId: number) =>
    request<{
      exists: boolean;
      size_bytes?: number;
      modified_at?: string;
      char_count?: number;
      preview_head?: string;
    }>(`/penugasan/${penugasanId}/preload-context/status`),

  // ===== Per-Temuan Review (Prioritas 2 — HITL per-temuan) =====
  /** List semua temuan + status review-nya. */
  listTemuanReview: (penugasanId: number) =>
    request<{
      total: number;
      counts: Record<string, number>;
      items: Array<{
        id_temuan: string;
        judul: string;
        sasaran_id: string;
        ro: string;
        kondisi: string;
        kriteria: string;
        akibat: string;
        anggota: string;
        dokumen_sumber_count: number;
        status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'EDITED';
        note: string | null;
        reviewed_at: string | null;
        reviewed_by_user_id: number | null;
        has_edits?: boolean;
        edited_fields?: {
          judul_temuan?: string;
          kondisi?: string;
          kriteria?: string;
          akibat?: string;
        } | null;
        edit_log?: Array<{
          at: string;
          by_nama?: string;
          by_role?: string;
          changes: Record<string, { from: string; to: string }>;
          note?: string | null;
        }> | null;
      }>;
    }>(`/penugasan/${penugasanId}/temuan-review`),

  /** Submit KKP ke Ketua Tim (AT) — tandai sasaran miliknya diajukan ke KT. */
  submitKkp: (penugasanId: number) =>
    request<{ ok: boolean; submitted_count: number; sasaran: string[]; message: string }>(
      `/penugasan/${penugasanId}/kkp/submit`,
      { method: 'POST' }
    ),

  /** Setujui 1 temuan (AT/KT/PT/PM). */
  approveTemuan: (penugasanId: number, temuanId: string, note?: string) =>
    request<{ ok: boolean; id_temuan: string; status: string; reviewed_at: string | null }>(
      `/penugasan/${penugasanId}/temuan-review/${encodeURIComponent(temuanId)}/approve`,
      { method: 'POST', body: JSON.stringify({ note: note ?? null }) }
    ),

  /** Tolak 1 temuan (KT/PT/PM). */
  rejectTemuan: (penugasanId: number, temuanId: string, note?: string) =>
    request<{ ok: boolean; id_temuan: string; status: string; reviewed_at: string | null }>(
      `/penugasan/${penugasanId}/temuan-review/${encodeURIComponent(temuanId)}/reject`,
      { method: 'POST', body: JSON.stringify({ note: note ?? null }) }
    ),

  /** Bulk approve semua temuan PENDING (KT/PT/PM). */
  bulkApproveTemuan: (penugasanId: number) =>
    request<{ ok: boolean; approved_count: number; total_temuan: number }>(
      `/penugasan/${penugasanId}/temuan-review/bulk-approve`,
      { method: 'POST' }
    ),

  /** Edit field temuan via overlay (KT/PT/PM). String "" eksplisit → hapus
   * overlay key (revert ke versi agen). Field undefined → tidak ubah. */
  editTemuan: (
    penugasanId: number,
    temuanId: string,
    edits: {
      judul_temuan?: string;
      kondisi?: string;
      kriteria?: string;
      akibat?: string;
      note?: string;
    }
  ) =>
    request<{
      ok: boolean;
      id_temuan: string;
      status: string;
      edited_fields: Record<string, string> | null;
      has_edits: boolean;
      reviewed_at: string | null;
    }>(
      `/penugasan/${penugasanId}/temuan-review/${encodeURIComponent(temuanId)}/edit`,
      { method: 'PUT', body: JSON.stringify(edits) }
    ),

  /** Hapus 1 temuan dari temuan.json (AT/KT/PT/PM). */
  deleteTemuan: (penugasanId: number, temuanId: string) =>
    request<{ ok: boolean; deleted: string; total_remaining: number }>(
      `/penugasan/${penugasanId}/temuan/${encodeURIComponent(temuanId)}`,
      { method: 'DELETE' }
    ),

  // ===== Reviu Konsep LHP (S3.2 — tahapan 6 LRS LHP, PT/PM) =====
  /** Riwayat reviu konsep LHP. latest_status: APPROVED | NEEDS_REVISION | null. */
  listLhpReview: (penugasanId: number) =>
    request<{
      total: number;
      latest_status: 'APPROVED' | 'NEEDS_REVISION' | null;
      items: Array<{
        id: number;
        status: 'APPROVED' | 'NEEDS_REVISION';
        catatan: string | null;
        reviewer_user_id: number | null;
        reviewer_role: string | null;
        reviewer_name: string | null;
        reviewed_at: string | null;
      }>;
    }>(`/penugasan/${penugasanId}/lhp-review`),

  /** Setujui / minta revisi konsep LHP (PT/PM only). */
  createLhpReview: (
    penugasanId: number,
    status: 'APPROVED' | 'NEEDS_REVISION',
    catatan?: string
  ) =>
    request<{
      ok: boolean;
      id: number;
      status: 'APPROVED' | 'NEEDS_REVISION';
      catatan: string | null;
      reviewer_role: string | null;
      reviewer_name: string | null;
      reviewed_at: string | null;
    }>(`/penugasan/${penugasanId}/lhp-review`, {
      method: 'POST',
      body: JSON.stringify({ status, catatan: catatan ?? null }),
    }),

  /** W1.1 — sync sasaran dari payload PKP SIMWAS (manual paste/upload hari ini;
   * source='api' placeholder 501 sampai kontrak API + SSO SIMWAS resmi). PT/KT. */
  syncSasaranFromSimwas: (
    penugasanId: number,
    payload: {
      source?: 'manual' | 'api';
      strategy?: 'replace' | 'append';
      pkp_rows: Array<{
        sasaran: string;
        langkah_kerja?: string;
        dilaksanakan_oleh?: string;
        waktu?: string;
        no_kkp?: string;
        sasaran_id?: string;
      }>;
    }
  ) =>
    request<{
      ok: boolean;
      source: string;
      strategy: string;
      total_input_rows: number;
      total_sasaran: number;
      added_sasaran: string[];
      added_count: number;
      skipped_duplicate: number;
    }>(`/penugasan/${penugasanId}/sasaran/sync-from-simwas`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getContextMd: (penugasanId: number) =>
    request<{ content: string; exists: boolean }>(
      `/penugasan/${penugasanId}/context-md`
    ),

  // ===== Kartu Penugasan (KP) — diisi PT, format INTEGRAL =====
  /** Baca Kartu Penugasan: markdown + nilai field form INTEGRAL + daftar sasaran. */
  getKpMd: (penugasanId: number) =>
    request<{
      content: string;
      exists: boolean;
      fields: Record<string, string> | null;
      sasaran: string[] | null;
      template_slug: string | null;
    }>(`/penugasan/${penugasanId}/kp-md`),

  /** Simpan Kartu Penugasan (PT/KT only). `sasaran` otomatis di-sync ke PKP
   * (sasaran-assignment) — meniru INTEGRAL: bagian II Pelaksanaan PKP dari sasaran KP. */
  saveKpMd: (
    penugasanId: number,
    content: string,
    fields?: Record<string, string>,
    sasaran?: string[],
    templateSlug?: string | null
  ) =>
    request<{ ok: boolean; size_bytes: number; path: string; sasaran_synced_to_pkp: number }>(
      `/penugasan/${penugasanId}/kp-md`,
      {
        method: 'PUT',
        body: JSON.stringify({
          content,
          fields: fields ?? null,
          sasaran: sasaran ?? null,
          template_slug: templateSlug ?? null,
        }),
      }
    ),

  /** Prasyarat Generate Context: sasaran (KT) + dokumen ter-digest (AT). */
  getContextReadiness: (penugasanId: number) =>
    request<{ ready: boolean; has_sasaran: boolean; has_ingested: boolean; reason: string }>(
      `/penugasan/${penugasanId}/context-readiness`
    ),

  saveContextMd: (penugasanId: number, content: string) =>
    request<{ ok: boolean; size_bytes: number; path: string }>(
      `/penugasan/${penugasanId}/context-md`,
      { method: 'PUT', body: JSON.stringify({ content }) }
    ),

  // ===== Knowledge / Wiki vault (W1 — baca vault pengetahuan) =====

  /** Cari catatan di vault pengetahuan organisasi (read-only). */
  // ===== Kriteria Pengawasan — regulasi wiki (konteks/regulasi/*.md) =====

  /** Daftar regulasi wiki (kelolaan Knowledge > Kriteria Pengawasan). */
  listRegulasi: () =>
    request<{
      items: Array<{
        slug: string;
        judul: string;
        nomor: string;
        tahun: string;
        status: string;
        sumber_file: string;
        updated: string;
        size_bytes: number;
      }>;
      total: number;
      kunci_ada: boolean;
    }>('/knowledge/regulasi'),

  /** Isi markdown 1 regulasi (slug 'regulasi-kunci' = cheat sheet inti). */
  getRegulasi: (slug: string) =>
    request<{ slug: string; content: string }>(`/knowledge/regulasi/${encodeURIComponent(slug)}`),

  /** Simpan perubahan regulasi — PT only. */
  updateRegulasi: (slug: string, content: string) =>
    request<{ ok: boolean; slug: string }>(`/knowledge/regulasi/${encodeURIComponent(slug)}`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    }),

  /** Hapus regulasi — PT only (regulasi-kunci dilindungi). */
  deleteRegulasi: (slug: string) =>
    request<{ ok: boolean; slug: string; deleted: boolean }>(
      `/knowledge/regulasi/${encodeURIComponent(slug)}`,
      { method: 'DELETE' }
    ),

  /** Upload PDF regulasi → auto-generate draft markdown ke wiki — PT only. */
  uploadRegulasi: (file: File) => {
    const fd = new FormData();
    fd.append('file', file);
    return request<{ ok: boolean; slug: string; judul: string; nomor: string; tahun: string; file: string }>(
      '/knowledge/regulasi/upload',
      { method: 'POST', body: fd }
    );
  },

  searchWiki: (q: string, limit = 12) =>
    request<{
      configured: boolean;
      total: number;
      message?: string;
      results: Array<{
        name: string;
        section: string;
        summary: string;
        path: string;
        score: number;
        snippet: string;
      }>;
    }>(`/knowledge/wiki/search?q=${encodeURIComponent(q)}&limit=${limit}`),

  /** Baca isi lengkap satu catatan vault by name. */
  getWikiPage: (name: string) =>
    request<{
      found: boolean;
      configured: boolean;
      message?: string;
      name?: string;
      path?: string;
      content?: string;
      truncated?: boolean;
    }>(`/knowledge/wiki/page?name=${encodeURIComponent(name)}`),

  // ===== Pattern Library Browser (W4) =====
  // Jelajah 65+ pattern temuan terkurasi di knowledge/wiki/temuan-patterns/<skill>/.
  // Semua role boleh baca (read-only). Lihat backend/app/knowledge_browse.py.

  /** List pattern terkurasi. Filter opsional: skill, severity, search. */
  listPatternLibrary: (params: { skill?: string; severity?: string; search?: string } = {}) => {
    const qs = new URLSearchParams();
    if (params.skill) qs.set('skill', params.skill);
    if (params.severity) qs.set('severity', params.severity);
    if (params.search) qs.set('search', params.search);
    const tail = qs.toString() ? `?${qs.toString()}` : '';
    return request<{
      skills_available: string[];
      severities_available: string[];
      categories_available: string[];
      total_all: number;
      total_filtered: number;
      items: Array<{
        id: string;
        skill: string;
        kategori: string;
        severity: string;
        judul: string;
        kriteria_baku: string;
        tags: string[];
        file: string;
      }>;
    }>(`/knowledge/patterns/library${tail}`);
  },

  /** Baca isi lengkap satu pattern (frontmatter + body markdown). */
  getPattern: (patternId: string) =>
    request<{
      id: string;
      skill: string;
      kategori: string;
      severity: string;
      judul: string;
      kriteria_baku: string;
      tags: string[];
      file: string;
      body_md: string;
    }>(`/knowledge/patterns/library/${encodeURIComponent(patternId)}`),

  // ===== Sasaran Template Suggestions =====
  // 3-sumber paralel untuk membantu KT setup penugasan tanpa start-from-zero.

  /** Saran template setup dari penugasan historis / skeleton pattern / catatan W3 vault. */
  getSasaranTemplates: (penugasanId: number, source: 'all' | 'historis' | 'patterns' | 'writeback' = 'all') =>
    request<{
      skill: string;
      obyek: string;
      historis?: Array<{
        kode: string;
        obyek: string;
        skill: string;
        status: string;
        similarity: number;
        total_sasaran: number;
        sasaran: Array<{
          sasaran_id: string;
          deskripsi: string;
          assigned_to: string[];
          langkah_kerja: string[];
        }>;
      }>;
      patterns?: {
        skill: string;
        total_patterns: number;
        sasaran: Array<{
          sasaran_id: string;
          deskripsi: string;
          langkah_kerja: string[];
          assigned_to: string[];
          kategori: string;
          pattern_ids: string[];
        }>;
      };
      writeback?: Array<{
        nama_file: string;
        judul: string;
        skill_label: string;
        obyek: string;
        jumlah_temuan: number;
        similarity: number;
      }>;
    }>(`/penugasan/${penugasanId}/sasaran/templates?source=${source}`),

  // ===== Promosi Pattern (W2) =====

  /** Agregasi usulan pattern dari feedback agen lintas penugasan (kandidat promosi). */
  getPatternMonitor: (days = 90) =>
    request<{
      days: number;
      total_feedback: number;
      total_suggestions: number;
      candidates: Array<{
        judul: string;
        id_proposed: string;
        count: number;
        rationales: string[];
        skills: Record<string, number>;
        suggested_skill: string;
        penugasan: Array<{ folder: string; obyek: string; skill: string }>;
        already_exists: boolean;
        existing_id: string | null;
      }>;
      missed_pattern_issues: Array<{
        description: string;
        suggested_action: string;
        severity: string;
        penugasan_folder: string;
        skill: string;
      }>;
    }>(`/knowledge/pattern-monitor?days=${days}`),

  /** Promote satu usulan jadi pattern wiki resmi (tulis file .md). PT/PM only. */
  promotePattern: (payload: {
    skill: string;
    pattern_id: string;
    judul: string;
    kategori?: string;
    severity?: string;
    kriteria_baku?: string;
    kondisi?: string;
    akibat?: string;
    rekomendasi?: string;
    bukti?: string;
    tags?: string[];
    sumber_penugasan?: string[];
  }) =>
    request<{
      ok: boolean;
      id: string;
      skill: string;
      kategori: string;
      severity: string;
      file: string;
      readme_updated: boolean;
    }>('/knowledge/patterns', { method: 'POST', body: JSON.stringify(payload) }),

  // ===== Tulis-balik Vault (W3) =====
  // Penugasan LHP_DONE → draft pengawasan-<kode>.md (Karpathy format) + delta
  // index/log. Auditor preview → Download .md (opsi A, Obsidian flow) atau Apply
  // ke vault (opsi B). Lihat backend/app/wiki_writeback.py.

  /** Daftar penugasan LHP_DONE + status proposal. Role-agnostik. */
  getWritebackCandidates: () =>
    request<{
      total: number;
      items: Array<{
        penugasan_id: number;
        kode: string;
        obyek: string;
        skill: string;
        lhp_done_at: string | null;
        proposal_status: 'NONE' | 'DRAFT' | 'APPLIED' | 'REJECTED';
        nama_file: string | null;
      }>;
    }>('/knowledge/writeback/candidates'),

  /** Generate (atau regenerate) draft proposal. PT/PM/KT only. */
  generateWritebackProposal: (penugasanId: number) =>
    request<{
      id: number;
      penugasan_id: number;
      nama_file: string;
      ringkasan: string | null;
      status: string;
      konten_md: string;
      delta_index: string | null;
      delta_log: string | null;
    }>(`/knowledge/writeback/${penugasanId}/generate`, { method: 'POST' }),

  /** Ambil proposal terkini (lengkap dengan konten). */
  getWritebackProposal: (penugasanId: number) =>
    request<{
      id: number;
      penugasan_id: number;
      nama_file: string;
      ringkasan: string | null;
      status: string;
      konten_md: string;
      delta_index: string | null;
      delta_log: string | null;
      dibuat_at: string | null;
      diupdate_at: string | null;
      applied_at: string | null;
    }>(`/knowledge/writeback/${penugasanId}/proposal`),

  /** URL unduh .md (mencegah CORS issue dgn fetch — pakai window.open). */
  getWritebackDownloadUrl: (penugasanId: number) => {
    const token = getToken() || '';
    return `${API_BASE}/knowledge/writeback/${penugasanId}/download?_token=${encodeURIComponent(token)}`;
  },

  /** Apply proposal ke vault. PT/PM only. */
  applyWritebackProposal: (penugasanId: number) =>
    request<{
      status: string;
      apply_result: {
        ok: boolean;
        path: string;
        index: { changed: boolean; reason: string };
        log: { changed: boolean; reason: string };
      };
    }>(`/knowledge/writeback/${penugasanId}/apply`, { method: 'POST' }),

  /** Tolak proposal (REJECTED). PT/PM only. */
  rejectWritebackProposal: (penugasanId: number) =>
    request<{ status: string }>(`/knowledge/writeback/${penugasanId}/reject`, { method: 'POST' }),

  // ===== CACM / EWS SIRUP (C1a — ingest offline + usulan penugasan) =====

  /** Ingest fixture contoh hasil EWS (demo tanpa deploy agent). PT only. */
  ingestCacmSample: () =>
    request<{ ok: boolean; id: number; run_id: string; summary: Record<string, number> }>(
      '/cacm/ingest-sample',
      { method: 'POST' }
    ),

  /** Ingest fixture DUMMY dimensi anggaran + kinerja saja (run tersendiri). PT only. */
  ingestCacmObservasiSample: () =>
    request<{
      ok: boolean;
      sample: boolean;
      dummy: boolean;
      id: number;
      run_id: string;
      summary: Record<string, number>;
      total_findings: number;
    }>('/cacm/observasi/ingest-sample', { method: 'POST' }),

  /** Muat SEMUA data contoh (pengadaan + anggaran + kinerja) ke SATU run. PT only. */
  loadCacmSampleAll: () =>
    request<{
      ok: boolean;
      sample: boolean;
      dimensi: string[];
      partial: string | null;
      id: number;
      run_id: string;
      summary: Record<string, number>;
      total_findings: number;
    }>('/cacm/sample/load-all', { method: 'POST' }),

  /** Daftar run EWS yang sudah masuk. */
  getCacmRuns: () =>
    request<{
      total: number;
      runs: Array<{
        id: number;
        run_id: string;
        source: string;
        tanggal_evaluasi: string | null;
        summary: Record<string, number>;
        total_findings: number;
        received_at: string | null;
      }>;
    }>('/cacm/runs'),

  /** Detail 1 run: rekap + findings. */
  getCacmRun: (id: number) =>
    request<{
      id: number;
      run_id: string;
      source: string;
      tanggal_evaluasi: string | null;
      summary: Record<string, number>;
      rekap: Array<Record<string, any>>;
      findings: Array<{
        id: number;
        kode: string;
        satker: string;
        satker_kode: string | null;
        status: string;
        judul: string | null;
        penjelasan: string | null;
        ringkasan: string | null;
        nilai_aktual: string | null;
        jumlah_paket_terdampak: number;
        total_nilai_terdampak: number;
        threshold: string | null;
        regulasi: string | null;
        rekomendasi: string | null;
        paket_detail: Array<Record<string, any>>;
        tindak_lanjut: string;
        penugasan_id: number | null;
        promotable: boolean;
      }>;
    }>(`/cacm/runs/${id}`),

  /** Jadikan finding usulan penugasan (status USULAN_CACM). PT only. */
  promoteFinding: (findingId: number) =>
    request<{ ok: boolean; penugasan_id: number; kode: string; obyek: string }>(
      `/cacm/findings/${findingId}/promote`,
      { method: 'POST' }
    ),

  /** Abaikan finding. PT only. */
  dismissFinding: (findingId: number) =>
    request<{ ok: boolean; finding_id: number; tindak_lanjut: string }>(
      `/cacm/findings/${findingId}/dismiss`,
      { method: 'POST' }
    ),

  /** Terima usulan CACM → penugasan jadi DRAFT (masuk alur normal). PT only. */
  acceptUsulan: (penugasanId: number) =>
    request<{ ok: boolean; penugasan_id: number; status: string }>(
      `/cacm/usulan/${penugasanId}/accept`,
      { method: 'POST' }
    ),

  /** Pull run terbaru dari agent EWS tim via REST (C1b). PT only. */
  syncCacm: () =>
    request<{ ok: boolean; id: number; run_id: string; summary: Record<string, number> }>(
      '/cacm/sync',
      { method: 'POST' }
    ),

  /** Minta agent EWS jalankan run baru (C1b). PT only. */
  triggerCacm: () =>
    request<{ ok: boolean; agent_response: any }>('/cacm/trigger', { method: 'POST' }),

  /** Jumlah usulan CACM yang menunggu review (status USULAN_CACM) — untuk badge. */
  getCacmPending: () =>
    request<{ count: number; items: Array<{ id: number; kode: string; obyek: string }> }>(
      '/cacm/usulan/pending'
    ),

  // ===== CACM Mesin Kriteria (Fase 1 — backend core wire-up commit-2) =====

  /** List kriteria CACM v7-native dari knowledge/cacm/kriteria/*.yaml. Semua role. */
  listCacmKriteria: (dimensi?: string) => {
    const qs = dimensi ? `?dimensi=${encodeURIComponent(dimensi)}` : '';
    return request<{
      total: number;
      dimensi_available: string[];
      items: Array<{
        id: string;
        revisi: string;
        nama: string;
        tipe: string;
        dimensi: string;
        sumber_data: string;
        satker_terapkan: string[];
        regulasi: string[];
        metric: { expression: string; satuan: string | null; format_display: string | null };
        thresholds: Array<{ status: string; condition: string; catatan: string | null }>;
        evidence_fields: string[];
        promote: { skill: string; pattern_ids_hint: string[]; prefilled_obyek_tpl: string | null; prefilled_dasar_permintaan: string | null } | null;
        catatan_revisi: string | null;
      }>;
    }>(`/cacm/kriteria/library${qs}`);
  },

  /** Daftar usulan kriteria dari wiki (menunggu keputusan PT). */
  listCacmUsulan: () =>
    request<{ total: number; items: Array<{ id: string; nama: string; dimensi: string; yaml: string }> }>(
      '/cacm/kriteria/usulan/list'
    ),

  /** Generate usulan kriteria dari basis regulasi wiki — PT only, deterministik. */
  generateCacmUsulan: () =>
    request<{ ok: boolean; dibuat: string[]; total_dibuat: number; dilewati: Array<{ nama: string; alasan: string }> }>(
      '/cacm/kriteria/usulan/generate',
      { method: 'POST' }
    ),

  /** Terima usulan → jadi kriteria aktif (PT only). */
  terimaCacmUsulan: (id: string) =>
    request<{ ok: boolean; id: string; aktif: boolean; catatan: string }>(
      `/cacm/kriteria/usulan/${encodeURIComponent(id)}/terima`,
      { method: 'POST' }
    ),

  /** Tolak (hapus) usulan — PT only. */
  tolakCacmUsulan: (id: string) =>
    request<{ ok: boolean; id: string; deleted: boolean }>(
      `/cacm/kriteria/usulan/${encodeURIComponent(id)}`,
      { method: 'DELETE' }
    ),

  /** Isi mentah file YAML 1 kriteria (untuk form edit). */
  getCacmKriteriaYaml: (id: string) =>
    request<{ id: string; yaml: string }>(`/cacm/kriteria/${encodeURIComponent(id)}/yaml`),

  /** Simpan perubahan YAML kriteria (PT only; divalidasi penuh di backend). */
  updateCacmKriteria: (id: string, yaml: string) =>
    request<{ ok: boolean; id: string; file: string }>(`/cacm/kriteria/${encodeURIComponent(id)}`, {
      method: 'PUT',
      body: JSON.stringify({ yaml }),
    }),

  /** Buat kriteria baru dari YAML (PT only; id diambil dari isi YAML). */
  createCacmKriteria: (yaml: string) =>
    request<{ ok: boolean; id: string; file: string }>(`/cacm/kriteria`, {
      method: 'POST',
      body: JSON.stringify({ yaml }),
    }),

  /** Hapus kriteria (PT only). Finding lama tetap tersimpan di DB. */
  deleteCacmKriteria: (id: string) =>
    request<{ ok: boolean; id: string; deleted: boolean }>(`/cacm/kriteria/${encodeURIComponent(id)}`, {
      method: 'DELETE',
    }),

  /** Detail 1 kriteria CACM. */
  getCacmKriteria: (id: string) =>
    request<{
      id: string;
      revisi: string;
      nama: string;
      tipe: string;
      dimensi: string;
      sumber_data: string;
      satker_terapkan: string[];
      regulasi: string[];
      metric: { expression: string; satuan: string | null; format_display: string | null };
      thresholds: Array<{ status: string; condition: string; catatan: string | null }>;
      evidence_fields: string[];
      promote: any;
      catatan_revisi: string | null;
    }>(`/cacm/kriteria/${encodeURIComponent(id)}`),

  /** List CacmFinding v7-native utk satu run (paralel dgn EwsFinding legacy). */
  getCacmV7Findings: (runId: number) =>
    request<{
      total: number;
      findings: Array<{
        id: number;
        kriteria_id: string;
        kriteria_revisi: string;
        status: string;
        metric_value: number | null;
        metric_display: string | null;
        metric_satuan: string | null;
        satker_kode: string | null;
        satker_nama: string;
        periode_label: string;
        dimensi: string;
        narasi: string;
        evidence: Record<string, any>;
        bukti_observasi_ids: number[];
        tindak_lanjut: string;
        penugasan_id: number | null;
        evaluated_at: string | null;
        // Narasi kaya dari agen EWS (hanya finding dimensi pengadaan yang punya
        // pasangan). null bila tak ada padanan legacy.
        ews: {
          kode: string;
          status: string;
          status_beda: boolean;
          judul: string | null;
          penjelasan: string | null;
          rekomendasi: string | null;
          nilai_aktual: string | null;
          threshold: string | null;
          regulasi: string | null;
          jumlah_paket_terdampak: number;
          total_nilai_terdampak: number;
        } | null;
      }>;
    }>(`/cacm/runs/${runId}/findings/v7-native`),

  /** Re-evaluate v7-native untuk satu run — PT/PM. Dipakai setelah revisi YAML. */
  reEvaluateCacmRun: (runId: number) =>
    request<{
      ok: boolean;
      run_id: number;
      removed_observasi: number;
      removed_findings_old: number;
      new_findings: number;
      note?: string;
    }>(`/cacm/runs/${runId}/re-evaluate`, { method: 'POST' }),

  /** Promote CacmFinding v7-native ke Penugasan USULAN_CACM (PT only).
   * Paralel dengan promote EwsFinding existing. */
  promoteCacmFinding: (findingId: number) =>
    request<{
      ok: boolean;
      penugasan_id: number;
      penugasan_kode: string;
      status: string;
    }>(`/cacm/cacm-findings/${findingId}/promote`, { method: 'POST' }),

  // ===== Feedback Aggregate Dashboard (Phase 2) =====

  /** Ringkasan agregat feedback agen cross-penugasan untuk N hari ke belakang. */
  getFeedbackAggregate: (days = 30) =>
    request<{
      days: number;
      total_feedback: number;
      by_agent: Record<string, number>;
      by_confidence: Record<string, number>;
      top_workflow_issues: Array<{
        category: string;
        severity: string;
        count: number;
        examples: string[];
      }>;
      top_substansi_issues: Array<{
        category: string;
        severity: string;
        count: number;
        examples: string[];
      }>;
      top_pattern_suggestions: Array<{
        id_proposed: string;
        judul: string;
        count: number;
        rationales: string[];
      }>;
      severity_heatmap: Record<string, Record<string, number>>;
      recent_files: Array<{
        path: string;
        full_path: string;
        agent: string;
        confidence: string;
        summary: string;
        penugasan_folder: string;
        timestamp: string | null;
        workflow_count: number;
        substansi_count: number;
        pattern_count: number;
      }>;
    }>(`/feedback/aggregate?days=${days}`),

  /** List file feedback mentah untuk drill-down. */
  listFeedback: (days = 30) =>
    request<{
      days: number;
      total: number;
      items: Array<{
        file: string;
        agent: string;
        confidence: string;
        summary: string;
        workflow_count: number;
        substansi_count: number;
        pattern_count: number;
        timestamp: string | null;
        penugasan_id: number | null;
        penugasan_obyek: string;
        penugasan_folder: string;
      }>;
    }>(`/feedback/list?days=${days}`),

  // ===== Templates KP & PKP (INTEGRAL workflow tahapan 1+2) =====

  /** List template KP/PKP dari wiki, filter by skill (optional).
   * Mengembalikan template `default` sebagai fallback jika skill tidak match. */
  listTemplates: (kind: 'kp' | 'pkp', skill?: string) => {
    const qs = skill ? `?skill=${encodeURIComponent(skill)}` : '';
    return request<{
      count: number;
      items: Array<{
        slug: string;
        judul: string;
        skill: string;
        jenis: string;
        field_required: string[];
        field_optional: string[];
        versi?: string;
      }>;
    }>(`/knowledge/templates/${kind}${qs}`);
  },

  /** Ambil isi lengkap 1 template KP/PKP (frontmatter + body markdown). */
  getTemplate: (kind: 'kp' | 'pkp', slug: string) =>
    request<{
      slug: string;
      kind: string;
      meta: Record<string, any>;
      body: string;
      raw: string;
    }>(`/knowledge/templates/${kind}/${encodeURIComponent(slug)}`),

  /** Buat/timpa template KP/PKP (PT only). */
  upsertTemplate: (kind: 'kp' | 'pkp', slug: string, raw: string) =>
    request<{ ok: boolean; slug: string; kind: string; action: string; skill: string }>(
      `/knowledge/templates/${kind}/${encodeURIComponent(slug)}`,
      { method: 'PUT', body: JSON.stringify({ raw }) }
    ),

  /** Hapus template KP/PKP (PT only; default dilindungi). */
  deleteTemplate: (kind: 'kp' | 'pkp', slug: string) =>
    request<{ ok: boolean; deleted: string; kind: string }>(
      `/knowledge/templates/${kind}/${encodeURIComponent(slug)}`,
      { method: 'DELETE' }
    ),

  /** Generate DRAFT template dari wiki oleh AI (PT only; tidak disimpan). */
  generateTemplate: (kind: 'kp' | 'pkp', skill: string, instruksi?: string) =>
    request<{ ok: boolean; kind: string; skill: string; draft: string; meta_terdeteksi: Record<string, any>; catatan: string }>(
      `/knowledge/templates/${kind}/generate`,
      { method: 'POST', body: JSON.stringify({ skill, instruksi: instruksi || '' }) }
    ),

  /** Rekap penilaian LKE (skor/predikat per unsur) untuk penugasan evaluasi ber-LKE. */
  getPenilaianLke: (penugasanId: number) =>
    request<{
      is_lke: boolean;
      skill: string;
      tersedia: boolean;
      komponen: { nama: string; bobot: any; nilai_pm: any; nilai_apip: any; delta: number | null; predikat: string; catatan?: string }[];
      total_pm: any;
      total_apip: any;
      predikat_akhir: any;
    }>(`/penugasan/${penugasanId}/penilaian-lke`),

  /** Chat bebas berbasis pengetahuan wiki (RAG). Semua role. */
  chatAsk: (question: string, history: { role: string; content: string }[]) =>
    request<{ answer: string; sources: { jenis: string; nama: string; summary: string }[]; n_sumber: number }>(
      `/chat/ask`,
      { method: 'POST', body: JSON.stringify({ question, history }) }
    ),
};
