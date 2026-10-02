import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export interface UserProfile {
  id: string;
  email: string;
  name: string;
  centre_name?: string;
  phone?: string;
  city?: string;
  state?: string;
  public_slug?: string;
  plan_id?: string;
  onboarding_completed?: boolean;
  role?: "partner" | "admin";
}

export interface FeatureMap {
  pdf_report?: string;
  quotient_dashboard?: string;
  ai_consultant?: string;
  compare_sessions?: string;
  compatibility_report?: string;
  bulk_upload?: string;
  public_report_qr?: string;
  sessions_per_month?: string;
  report_validity_days?: string;
  white_label_branding?: string;
  api_direct_access?: string;
  export_raw_data?: string;
  palm_atd?: string;
  [key: string]: string | undefined;
}

interface AuthState {
  user: UserProfile | null;
  features: FeatureMap;
  accessToken: string | null;
  refreshToken: string | null;
  scope: "partner" | "admin" | null;
  isLoading: boolean;

  setAuth: (
    user: UserProfile,
    features: FeatureMap,
    token: string,
    scope: "partner" | "admin",
    refreshToken?: string | null
  ) => void;
  clearAuth: () => void;
  setToken: (token: string) => void;
  setRefreshToken: (token: string | null) => void;
  setLoading: (v: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      features: {},
      accessToken: null,
      refreshToken: null,
      scope: null,
      isLoading: false,

      setAuth: (user, features, accessToken, scope, refreshToken) =>
        set({
          user,
          features,
          accessToken,
          scope,
          refreshToken: refreshToken !== undefined ? refreshToken : get().refreshToken,
          isLoading: false,
        }),

      clearAuth: () =>
        set({
          user: null,
          features: {},
          accessToken: null,
          refreshToken: null,
          scope: null,
          isLoading: false,
        }),

      setToken: (accessToken) => set({ accessToken }),

      setRefreshToken: (refreshToken) => set({ refreshToken }),

      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: "dmit:auth-storage",
      storage: createJSONStorage(() => (typeof window !== "undefined" ? localStorage : ({} as Storage))),
      partialize: (state) => ({
        user: state.user,
        features: state.features,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        scope: state.scope,
      }),
    }
  )
);

/** Check if a feature is enabled for the current partner. */
export function useFeature(key: string): boolean {
  const features = useAuthStore((s) => s.features);
  const val = features[key];
  return val !== undefined && val !== "false" && val !== "0" && val !== "";
}

/** Get numeric quota value, or -1 for unlimited. */
export function useQuota(key: string): number {
  const features = useAuthStore((s) => s.features);
  const val = features[key];
  if (!val) return 0;
  const n = parseInt(val, 10);
  return isNaN(n) ? 0 : n;
}

/** Hint stored so boot-refresh knows which cookie path to call. */
const SCOPE_KEY = "dmit:last-scope";

export function persistScopeHint(scope: "partner" | "admin") {
  if (typeof window !== "undefined") localStorage.setItem(SCOPE_KEY, scope);
}

export function getScopeHint(): "partner" | "admin" | null {
  if (typeof window === "undefined") return null;
  const v = localStorage.getItem(SCOPE_KEY);
  return v === "partner" || v === "admin" ? v : null;
}

export function clearScopeHint() {
  if (typeof window !== "undefined") localStorage.removeItem(SCOPE_KEY);
}
