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
  const { access_token } = await apiPost<{ access_token: string }>(
    "/auth/login", { email, password }
  );
  // Fetch profile with the newly-issued token directly — authStore is still null at this point
  const res = await fetch(`${apiBase()}/auth/me`, {
    headers: { Authorization: `Bearer ${access_token}` },
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to load partner profile");
  const { user, features } = await res.json() as { user: UserProfile; features: FeatureMap };
  useAuthStore.getState().setAuth({ ...user, role: "partner" }, features, access_token, "partner");
  persistScopeHint("partner");
}

export async function logoutPartner(): Promise<void> {
  await fetch(`${apiBase()}/auth/logout`, {
    method: "POST",
    credentials: "include",
  }).catch(() => {});
  useAuthStore.getState().clearAuth();
  clearScopeHint();
}

// ── Admin auth ─────────────────────────────────────────────────────────────

export async function loginAdmin(email: string, password: string): Promise<void> {
  const { access_token } = await apiPost<{ access_token: string }>(
    "/admin/auth/login", { email, password }
  );
  const me = await (async () => {
    const res = await fetch(`${apiBase()}/admin/auth/me`, {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: "include",
    });
    return res.json() as Promise<UserProfile>;
  })();
  useAuthStore.getState().setAuth(
    { ...me, role: "admin" },
    {},    // admin has no feature map
    access_token,
    "admin",
  );
  persistScopeHint("admin");
}

export async function logoutAdmin(): Promise<void> {
  await fetch(`${apiBase()}/admin/auth/logout`, {
    method: "POST",
    credentials: "include",
  }).catch(() => {});
  useAuthStore.getState().clearAuth();
  clearScopeHint();
}

// ── Boot refresh (call once on app load) ──────────────────────────────────

export async function tryRefreshOnBoot(): Promise<boolean> {
  const scope = getScopeHint();
  if (!scope) {
    useAuthStore.getState().setLoading(false);
    return false;
  }
  const path = scope === "admin" ? "/admin/auth/refresh" : "/auth/refresh";
  const mePath = scope === "admin" ? "/admin/auth/me" : "/auth/me";
  try {
    const res = await fetch(`${apiBase()}${path}`, {
      method: "POST",
      credentials: "include",
    });
    if (!res.ok) throw new Error("refresh failed");
    const { access_token } = await res.json();
    const meRes = await fetch(`${apiBase()}${mePath}`, {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: "include",
    });
    if (!meRes.ok) throw new Error("/me failed after refresh");
    const me = await meRes.json();
    if (scope === "admin") {
      useAuthStore.getState().setAuth({ ...me, role: "admin" }, {}, access_token, "admin");
    } else {
      useAuthStore.getState().setAuth(
        { ...me.user, role: "partner" }, me.features, access_token, "partner"
      );
    }
    return true;
  } catch {
    useAuthStore.getState().setLoading(false);
    clearScopeHint();
    return false;
  }
}
