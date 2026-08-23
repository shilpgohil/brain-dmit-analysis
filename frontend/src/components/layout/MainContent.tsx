"use client";
import { usePathname } from "next/navigation";

const AUTH_PATHS = new Set(["/login", "/request-access"]);

export function MainContent({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAuth = AUTH_PATHS.has(pathname);
  return (
    <main className={`relative z-10 ${isAuth ? "" : "pt-14"}`}>
      {children}
    </main>
  );
}
