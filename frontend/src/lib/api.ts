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
 * Download the PDF report with the Bearer token attached.
 * A plain <a href> navigation can't send Authorization headers, so the
 * protected download endpoint would always return 401 — fetch it as a
 * blob instead and trigger the save from an object URL.
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
    // Dynamic import avoids circular deps; Zustand state is readable outside React
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const { useAuthStore } = require("@/store/authStore");
    return useAuthStore.getState().accessToken as string | null;
  } catch {
    return null;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const authHeader: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {};

  const res = await fetch(`${apiBase()}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader,
      ...init?.headers,
    },
    credentials: "include",
    ...init,
  });
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

/** Upload with L1–R5 slot names so the pipeline maps fingers correctly. */
export async function uploadImagesWithSlots(
  sessionId: string,
  slots: UploadSlot[]
): Promise<{ uploaded: number; total: number }> {
  const form = new FormData();
  const positions: string[] = [];

  for (const { slotId, file } of slots) {
    const ext = file.name.includes(".") ? file.name.split(".").pop() : "bmp";
    const renamed = new File([file], `${slotId}.${ext}`, { type: file.type || "image/bmp" });
    form.append("files", renamed);
    positions.push(slotId);
  }
  form.append("finger_positions", positions.join(","));

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
