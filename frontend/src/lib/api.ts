import type {
  AnalysisResult,
  AnalysisSession,
  SessionListItem,
  SystemStatus,
} from "./types";
import { getApiUrlOverride } from "./preferences";

const DEFAULT_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001/api";

function normalizeBase(raw: string): string {
  const trimmed = raw.trim().replace(/\/+$/, "");
  if (!trimmed) return DEFAULT_BASE;
  return /\/api$/.test(trimmed) ? trimmed : `${trimmed}/api`;
}

export function apiBase(): string {
  const override = getApiUrlOverride();
  return override ? normalizeBase(override) : DEFAULT_BASE;
}

export function getApiOrigin(): string {
  return apiBase().replace(/\/api\/?$/, "");
}

export function reportDownloadUrl(sessionId: string, reportUrl?: string | null): string {
  if (reportUrl?.startsWith("http")) return reportUrl;
  if (reportUrl?.startsWith("/")) return `${getApiOrigin()}${reportUrl}`;
  return `${apiBase()}/analysis/${sessionId}/report/download`;
}

/**
 * Download the PDF report.
 *
 * Two modes:
 *  1. Storage (B2/R2) mode — backend returns JSON {type:"redirect", url, filename}.
 *     We open the presigned URL directly via a hidden <a> click to avoid CORS
 *     issues that arise when fetch() follows a cross-origin redirect to B2/R2.
 *  2. Local/streaming mode — backend returns the PDF blob directly.
 *     We build an object URL and trigger the save as before.
 */
export async function downloadReport(
  sessionId: string,
  subjectName?: string | null
): Promise<void> {
  const token = getStoredToken();
  const res = await fetch(`${apiBase()}/analysis/${sessionId}/report/download`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error(`Download failed (${res.status}): ${await res.text()}`);
  }

  const contentType = res.headers.get("content-type") || "";

  // JSON response = presigned URL from B2/R2 — open directly, no CORS issue
  if (contentType.includes("application/json")) {
    const data = await res.json();
    if (data.type === "redirect" && data.url) {
      const a = document.createElement("a");
      a.href = data.url;
      a.download = data.filename || `dmit-report-${sessionId.slice(0, 8)}.pdf`;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      document.body.appendChild(a);
      a.click();
      a.remove();
      return;
    }
  }

  // PDF blob response = local filesystem (dev mode)
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  const safeName = (subjectName || "dmit-report").replace(/[^\w\- ]+/g, "").trim() || "dmit-report";
  a.download = `${safeName}-${sessionId.slice(0, 8)}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function mediaUrl(path?: string | null): string | undefined {
  if (!path) return undefined;
  if (path.startsWith("http")) return path;
  return `${getApiOrigin()}${path.startsWith("/") ? path : `/${path}`}`;
}

/** Read the current access token from the Zustand auth store without a hook. */
function getStoredToken(): string | null {
  try {
    const { useAuthStore } = require("@/store/authStore");
    const token = useAuthStore.getState().accessToken as string | null;
    if (token) return token;
  } catch {}

  if (typeof window !== "undefined") {
    try {
      const raw = localStorage.getItem("dmit:auth-storage");
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed?.state?.accessToken) {
          return parsed.state.accessToken as string;
        }
      }
    } catch {}
  }
  return null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const authHeader: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {};

  let res = await fetch(`${apiBase()}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader,
      ...init?.headers,
    },
    credentials: "include",
    ...init,
  });

  if (res.status === 401) {
    try {
      const { tryRefreshOnBoot } = require("@/lib/auth-api");
      const refreshed = await tryRefreshOnBoot();
      if (refreshed) {
        const newToken = getStoredToken();
        res = await fetch(`${apiBase()}${path}`, {
          headers: {
            "Content-Type": "application/json",
            ...(newToken ? { Authorization: `Bearer ${newToken}` } : {}),
            ...init?.headers,
          },
          credentials: "include",
          ...init,
        });
      }
    } catch {}
  }

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${res.status}: ${body}`);
  }
  return res.json() as Promise<T>;
}

// ── Sessions ──────────────────────────────────────────────────────────────────

export async function createSession(data: {
  subject_name?: string;
  subject_age?: number;
  subject_gender?: string;
  subject_dob?: string;
  school?: string;
  counsellor?: string;
  parent_name?: string;
  notes?: string;
}): Promise<AnalysisSession> {
  return request<AnalysisSession>("/sessions", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function listSessions(limit = 50, offset = 0): Promise<SessionListItem[]> {
  return request<SessionListItem[]>(`/sessions?limit=${limit}&offset=${offset}`);
}

export async function getSession(sessionId: string): Promise<AnalysisSession> {
  return request<AnalysisSession>(`/sessions/${sessionId}`);
}

export async function deleteSession(sessionId: string): Promise<void> {
  await request(`/sessions/${sessionId}`, { method: "DELETE" });
}

// ── Image Upload ──────────────────────────────────────────────────────────────

export interface UploadSlot {
  slotId: string;
  file: File;
}

/** Upload with L1–R5 slot names so the pipeline maps fingers correctly.
 *  Uploads ONE image at a time (sequential) to avoid multipart-body OOM
 *  on memory-constrained servers (Render free/starter tier).
 */
export async function uploadImagesWithSlots(
  sessionId: string,
  slots: UploadSlot[]
): Promise<{ uploaded: number; total: number }> {
  const token = getStoredToken();
  let lastResult = { uploaded: 0, total: 0 };

  for (const { slotId, file } of slots) {
    const form = new FormData();
    const ext = file.name.includes(".") ? file.name.split(".").pop() : "bmp";
    const renamed = new File([file], `${slotId}.${ext}`, { type: file.type || "image/bmp" });
    form.append("files", renamed);
    form.append("finger_positions", slotId);

    const res = await fetch(`${apiBase()}/analysis/${sessionId}/upload`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      credentials: "include",
      body: form,
    });
    if (!res.ok) throw new Error(`Upload failed for ${slotId}: ${await res.text()}`);
    lastResult = await res.json();
  }

  return lastResult;
}

/** Legacy bulk upload (filenames should contain L1/R1 etc. if possible). */
export async function uploadImages(
  sessionId: string,
  files: File[]
): Promise<{ uploaded: number; total: number }> {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  const token = getStoredToken();
  const res = await fetch(`${apiBase()}/analysis/${sessionId}/upload`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    credentials: "include",
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed: ${await res.text()}`);
  return res.json();
}

// ── Analysis ──────────────────────────────────────────────────────────────────

export async function runAnalysis(data: {
  session_id: string;
  use_preprocessing?: boolean;
  generate_pdf?: boolean;
}): Promise<{ session_id: string; status: string }> {
  return request("/analysis/run", {
    method: "POST",
    body: JSON.stringify({ use_preprocessing: false, generate_pdf: true, ...data }),
  });
}

export async function getAnalysis(sessionId: string): Promise<AnalysisResult> {
  return request<AnalysisResult>(`/analysis/${sessionId}`);
}

export interface ReportCustomization {
  analyst_name?: string;
  analyst_title?: string;
  analyst_id?: string;
  school_name?: string;
  franchise_code?: string;
  brand_color?: string;
  contact_phone?: string;
  contact_email?: string;
  website?: string;
  counselor_notes?: string;
  participant_comments?: string;
  candidate_signature?: string;
  counselor_signature?: string;
}

export interface GlobalStorageTelemetry {
  status: string;
  storage: {
    enabled: boolean;
    provider: string;
    bucket?: string | null;
    endpoint?: string | null;
    public_base_url?: string | null;
  };
  provider: string;
  bucket?: string | null;
  endpoint?: string | null;
  public_base_url?: string | null;
}

export interface ReportStorageStatus {
  session_id: string;
  storage: {
    enabled: boolean;
    provider: string;
    bucket?: string | null;
    endpoint?: string | null;
    public_base_url?: string | null;
  };
  r2_pdf_key?: string | null;
  in_object_storage: boolean;
  local_file_exists: boolean;
  local_file_size: number;
  presigned_url?: string | null;
  pages: number;
}

export function getReportInlineViewUrl(sessionId: string): string {
  const token = getStoredToken();
  const tokenParam = token ? `&token=${encodeURIComponent(token)}` : "";
  return `${apiBase()}/analysis/${sessionId}/report/download?inline=true${tokenParam}`;
}

export async function fetchReportPdfBlobUrl(sessionId: string): Promise<string> {
  const token = getStoredToken();
  const res = await fetch(`${apiBase()}/analysis/${sessionId}/report/download?inline=true`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error(`Report streaming failed (${res.status}): ${await res.text()}`);
  }
  const blob = await res.blob();
  return URL.createObjectURL(blob);
}

export async function getReportStorageStatus(sessionId: string): Promise<ReportStorageStatus> {
  return request<ReportStorageStatus>(`/analysis/${sessionId}/report/storage-status`);
}

export async function getStorageTelemetry(): Promise<GlobalStorageTelemetry> {
  return request<GlobalStorageTelemetry>("/analysis/storage/telemetry");
}

export async function getBrandingSettings(): Promise<ReportCustomization> {
  return request<ReportCustomization>("/analysis/settings/branding");
}

export async function updateBrandingSettings(settings: ReportCustomization): Promise<void> {
  return request("/analysis/settings/branding", {
    method: "POST",
    body: JSON.stringify(settings),
  });
}

export async function exportBatchZip(sessionIds: string[]): Promise<void> {
  const token = getStoredToken();
  const res = await fetch(`${apiBase()}/analysis/batch/export-zip`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    credentials: "include",
    body: JSON.stringify({ session_ids: sessionIds }),
  });
  if (!res.ok) {
    throw new Error(`Batch export failed (${res.status}): ${await res.text()}`);
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  const timestamp = new Date().toISOString().slice(0, 10);
  a.download = `DMIT_Cohort_Dossiers_${timestamp}.zip`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export async function getReportCustomization(sessionId: string): Promise<ReportCustomization> {
  return request<ReportCustomization>(`/analysis/${sessionId}/report/customization`);
}

export async function generateReport(
  sessionId: string,
  customization?: ReportCustomization
): Promise<{ status: string; session_id: string; report_url: string; pages: number; storage?: unknown }> {
  return request(`/analysis/${sessionId}/report/generate`, {
    method: "POST",
    body: customization ? JSON.stringify(customization) : undefined,
  });
}


// ── System ────────────────────────────────────────────────────────────────────

export async function getHealth(): Promise<SystemStatus> {
  return request<SystemStatus>("/health");
}

// ── Polling ───────────────────────────────────────────────────────────────────

export async function pollUntilComplete(
  sessionId: string,
  onUpdate: (result: AnalysisResult) => void,
  intervalMs = 1500
): Promise<AnalysisResult> {
  return new Promise((resolve, reject) => {
    const timer = setInterval(async () => {
      try {
        const result = await getAnalysis(sessionId);
        onUpdate(result);
        if (result.status === "completed") {
          clearInterval(timer);
          resolve(result);
        } else if (result.status === "failed") {
          clearInterval(timer);
          reject(new Error(result.error_message ?? "Analysis failed"));
        }
      } catch (err) {
        clearInterval(timer);
        reject(err);
      }
    }, intervalMs);
  });
}
