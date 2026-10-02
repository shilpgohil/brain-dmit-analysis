import { apiBase } from "./api";
import { useAuthStore, persistScopeHint, clearScopeHint, getScopeHint } from "@/store/authStore";
import type { FeatureMap, UserProfile } from "@/store/authStore";

// ── Helpers ───────────────────────────────────────────────────────────────

function authHeaders(): Record<string, string> {
  const token = useAuthStore.getState().accessToken;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function apiPost<T>(path: string, body: unknown, token?: string): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const t = token ?? useAuthStore.getState().accessToken;
  if (t) headers["Authorization"] = `Bearer ${t}`;
  const res = await fetch(`${apiBase()}${path}`, {
    method: "POST",
    headers,
    credentials: "include",  // include cookies for refresh token
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${apiBase()}${path}`, {
    headers: authHeaders(),
    credentials: "include",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

// ── Partner auth ──────────────────────────────────────────────────────────

export async function loginPartner(email: string, password: string): Promise<void> {
  const { access_token, refresh_token } = await apiPost<{ access_token: string; refresh_token?: string }>(
    "/auth/login", { email, password }
  );
  const res = await fetch(`${apiBase()}/auth/me`, {
    headers: { Authorization: `Bearer ${access_token}` },
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to load partner profile");
  const { user, features } = await res.json() as { user: UserProfile; features: FeatureMap };
  useAuthStore.getState().setAuth({ ...user, role: "partner" }, features, access_token, "partner", refresh_token);
  persistScopeHint("partner");
}

export async function logoutPartner(): Promise<void> {
  const token = useAuthStore.getState().refreshToken;
  await fetch(`${apiBase()}/auth/logout`, {
    method: "POST",
    headers: token ? { "X-Refresh-Token": token, "Content-Type": "application/json" } : {},
    body: JSON.stringify({ refresh_token: token || undefined }),
    credentials: "include",
  }).catch(() => {});
  useAuthStore.getState().clearAuth();
  clearScopeHint();
}

// ── Admin auth ─────────────────────────────────────────────────────────────

export async function loginAdmin(email: string, password: string): Promise<void> {
  const { access_token, refresh_token } = await apiPost<{ access_token: string; refresh_token?: string }>(
    "/admin/auth/login", { email, password }
  );
  const res = await fetch(`${apiBase()}/admin/auth/me`, {
    headers: { Authorization: `Bearer ${access_token}` },
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to load admin profile");
  const me = await res.json() as UserProfile;
  useAuthStore.getState().setAuth(
    { ...me, role: "admin" },
    {},
    access_token,
    "admin",
    refresh_token,
  );
  persistScopeHint("admin");
}

export async function logoutAdmin(): Promise<void> {
  const token = useAuthStore.getState().refreshToken;
  await fetch(`${apiBase()}/admin/auth/logout`, {
    method: "POST",
    headers: token ? { "X-Refresh-Token": token, "Content-Type": "application/json" } : {},
    body: JSON.stringify({ refresh_token: token || undefined }),
    credentials: "include",
  }).catch(() => {});
  useAuthStore.getState().clearAuth();
  clearScopeHint();
}

// ── Boot refresh (call once on app load) ──────────────────────────────────

export async function tryRefreshOnBoot(): Promise<boolean> {
  const currentState = useAuthStore.getState();
  const scope = currentState.scope || getScopeHint();
  if (!scope) {
    currentState.setLoading(false);
    return false;
  }

  const hasExistingSession = Boolean(currentState.user && currentState.accessToken);
  const path = scope === "admin" ? "/admin/auth/refresh" : "/auth/refresh";
  const mePath = scope === "admin" ? "/admin/auth/me" : "/auth/me";
  const storedRefreshToken = currentState.refreshToken;

  try {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (storedRefreshToken) {
      headers["X-Refresh-Token"] = storedRefreshToken;
    }

    const res = await fetch(`${apiBase()}${path}`, {
      method: "POST",
      headers,
      credentials: "include",
      body: JSON.stringify({ refresh_token: storedRefreshToken || undefined }),
    });

    if (!res.ok) {
      if (!hasExistingSession) {
        throw new Error("refresh failed");
      }
      useAuthStore.getState().setLoading(false);
      return true;
    }

    const { access_token, refresh_token: new_refresh } = await res.json();
    const meRes = await fetch(`${apiBase()}${mePath}`, {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: "include",
    });

    if (meRes.ok) {
      const me = await meRes.json();
      if (scope === "admin") {
        useAuthStore.getState().setAuth({ ...me, role: "admin" }, {}, access_token, "admin", new_refresh);
      } else {
        useAuthStore.getState().setAuth(
          { ...me.user, role: "partner" }, me.features, access_token, "partner", new_refresh
        );
      }
    } else {
      useAuthStore.getState().setToken(access_token);
      if (new_refresh) useAuthStore.getState().setRefreshToken(new_refresh);
    }
    useAuthStore.getState().setLoading(false);
    return true;
  } catch {
    useAuthStore.getState().setLoading(false);
    if (hasExistingSession) {
      return true;
    }
    clearScopeHint();
    return false;
  }
}
