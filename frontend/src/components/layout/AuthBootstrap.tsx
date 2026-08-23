"use client";

import { useEffect } from "react";
import { tryRefreshOnBoot } from "@/lib/auth-api";

/** Attempt to restore auth from the httpOnly refresh token cookie on every cold boot. */
export function AuthBootstrap() {
  useEffect(() => {
    tryRefreshOnBoot().catch(() => {});
  }, []);
  return null;
}
