"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";

type RequiredRole = "partner" | "admin" | "any";

/**
 * Route protection hook.
 * - Shows nothing / redirects to /login when not authenticated.
 * - Shows nothing / redirects when role doesn't match.
 * - Returns { user, features, isLoading } for convenience.
 *
 * Usage in a page:
 *   const { user } = useAuthGuard("partner");
 *   if (!user) return null;   // guard handles redirect
 */
export function useAuthGuard(requiredRole: RequiredRole = "any") {
  const { user, scope, features, isLoading } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    if (!user) {
      router.replace("/login");
      return;
    }

    if (requiredRole === "admin" && scope !== "admin") {
      router.replace("/sessions");
      return;
    }

    if (requiredRole === "partner" && scope !== "partner") {
      router.replace("/admin");
      return;
    }
  }, [user, scope, isLoading, requiredRole, router]);

  return { user, scope, features, isLoading };
}
