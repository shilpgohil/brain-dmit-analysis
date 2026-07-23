const KEYS = {
  apiUrl: "dmit_api_url",
  generatePdf: "dmit_generate_pdf",
  usePreprocessing: "dmit_use_preprocessing",
} as const;

export interface AppPreferences {
  apiUrl: string;
  generatePdf: boolean;
  usePreprocessing: boolean;
}

export const DEFAULT_API_ORIGIN =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/api\/?$/, "") ?? "http://localhost:8001";

function read(key: string): string | null {
  if (typeof window === "undefined") return null;
  const value = window.localStorage.getItem(key);
  return value && value.trim() ? value.trim() : null;
}

export function getApiUrlOverride(): string | null {
  return read(KEYS.apiUrl);
}

export function getDefaultGeneratePdf(): boolean {
  return read(KEYS.generatePdf) !== "false";
}

export function getDefaultUsePreprocessing(): boolean {
  return read(KEYS.usePreprocessing) === "true";
}

export function loadPreferences(): AppPreferences {
  return {
    apiUrl: getApiUrlOverride() ?? DEFAULT_API_ORIGIN,
    generatePdf: getDefaultGeneratePdf(),
    usePreprocessing: getDefaultUsePreprocessing(),
  };
}

export function savePreferences(prefs: AppPreferences): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEYS.apiUrl, prefs.apiUrl.trim());
  window.localStorage.setItem(KEYS.generatePdf, String(prefs.generatePdf));
  window.localStorage.setItem(KEYS.usePreprocessing, String(prefs.usePreprocessing));
}
