"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { NavBrandMark } from "@/components/layout/NavBrandMark";
import { useAuthStore } from "@/store/authStore";
import { Plus, X, Menu, LogIn, LogOut } from "lucide-react";
import { logoutPartner, logoutAdmin } from "@/lib/auth-api";

// Always visible — marketing/educational pages, no login required
const PUBLIC_NAV = [
  { label: "Solutions", href: "/solutions" },
  { label: "Learn", href: "/learn" },
  { label: "Extensions", href: "/extensions" },
];

// Only shown to logged-in partners
const PARTNER_ONLY_NAV = [
  { label: "Analyze", href: "/analysis/new" },
  { label: "Sessions", href: "/sessions" },
];

const ADMIN_NAV = [
  { label: "Dashboard", href: "/admin" },
  { label: "Partners", href: "/admin/partners" },
  { label: "Requests", href: "/admin/requests" },
  { label: "Plans", href: "/admin/plans" },
];

export function CinematicNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, scope } = useAuthStore();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  // Hide entirely on auth-only pages
  const isAuthPage = pathname === "/login" || pathname === "/request-access";

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (isAuthPage) return null;

  const isLoggedIn = !!user;
  const isAdmin = scope === "admin";

  // Links shown in desktop bar and mobile drawer
  const navLinks = isAdmin
    ? ADMIN_NAV
    : isLoggedIn
      ? [...PUBLIC_NAV, ...PARTNER_ONLY_NAV]
      : PUBLIC_NAV;

  const handleLogout = async () => {
    if (scope === "admin") await logoutAdmin();
    else await logoutPartner();
    router.push("/login");
  };

  return (
    <>
      <motion.nav
        className={cn(
          "fixed top-0 left-0 right-0 z-50 h-14 flex items-center px-4 sm:px-6 transition-all duration-500",
          scrolled
            ? "bg-[rgba(2,2,8,0.9)] backdrop-blur-2xl border-b border-white/[0.06]"
            : "bg-gradient-to-b from-[rgba(2,2,8,0.6)] to-transparent"
        )}
        initial={{ y: -60, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      >
        {/* Brand */}
        <Link href={isAdmin ? "/admin" : "/"} className="flex items-center gap-3 group mr-4 sm:mr-6">
          <NavBrandMark />
          <div className="leading-none hidden sm:block">
            <p className="font-editorial text-[15px] tracking-[0.06em] text-white">DMIT</p>
            <p className="text-[8px] text-white/35 tracking-[0.22em] uppercase font-mono mt-0.5">
              Biometric Intelligence
            </p>
          </div>
        </Link>

        {/* Nav links — public links always visible; partner/admin links require login */}
        <div className="hidden lg:flex items-center gap-0.5 flex-1">
          {navLinks.map(({ label, href }) => {
            const active =
              href === "/"
                ? pathname === "/"
                : href === "/admin"
                  ? pathname === "/admin"
                  : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "relative px-3 py-1.5 text-xs font-medium rounded-md transition-colors duration-200",
                  active ? "text-[var(--accent-champagne)]" : "text-white/40 hover:text-white/75"
                )}
              >
                {active && (
                  <motion.div
                    layoutId="nav-pill"
                    className="absolute inset-0 rounded-md"
                    style={{ background: "rgba(196,165,116,0.08)", border: "1px solid rgba(196,165,116,0.2)" }}
                    transition={{ type: "spring", bounce: 0.2, duration: 0.5 }}
                  />
                )}
                <span className="relative z-10">{label}</span>
              </Link>
            );
          })}
        </div>

        {/* CTA / auth actions */}
        <div className="flex items-center gap-2 ml-auto">
          {isLoggedIn ? (
            <>
              {scope === "partner" && (
                <Link
                  href="/analysis/new"
                  className="hidden md:flex items-center gap-1.5 h-8 px-4 rounded-lg text-xs font-medium text-[#0a0a12] transition-all duration-200 hover:brightness-110"
                  style={{
                    background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 50%, #9d8bb5 100%)",
                    boxShadow: "0 0 24px rgba(196,165,116,0.25)",
                  }}
                >
                  <Plus className="w-3 h-3" />
                  New Analysis
                </Link>
              )}
              <div className="hidden md:flex items-center gap-1.5 text-xs text-white/30">
                <span
                  className="font-mono text-[10px] px-2 py-1 rounded"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}
                >
                  {user?.name?.split(" ")[0]}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="hidden md:flex items-center gap-1.5 h-8 px-3 rounded-lg text-xs text-white/30 hover:text-rose-400 transition-colors"
                title="Sign out"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </>
          ) : (
            <Link
              href="/login"
              className="hidden md:flex items-center gap-1.5 h-8 px-4 rounded-lg text-xs font-medium transition-all duration-200 hover:brightness-110"
              style={{
                background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 50%, #9a7b4f 100%)",
                color: "#1a1510",
                boxShadow: "0 0 20px rgba(196,165,116,0.2)",
              }}
            >
              <LogIn className="w-3.5 h-3.5" />
              Sign In
            </Link>
          )}
          <button
            className="lg:hidden w-8 h-8 flex items-center justify-center text-white/50 hover:text-white"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </motion.nav>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              className="fixed inset-0 bg-black/60 z-[60]"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
            />
            <motion.div
              className="fixed right-0 top-0 bottom-0 w-72 z-[70] flex flex-col"
              style={{ background: "rgba(4,4,15,0.98)", borderLeft: "1px solid rgba(196,165,116,0.15)" }}
              initial={{ x: 72, opacity: 0 }} animate={{ x: 0, opacity: 1 }} exit={{ x: 72, opacity: 0 }}
              transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            >
              <div className="flex items-center justify-between p-4 border-b border-white/[0.06]">
                <div className="flex items-center gap-2">
                  <NavBrandMark />
                  <span className="font-editorial text-white">DMIT</span>
                </div>
                <button onClick={() => setMobileOpen(false)} className="text-white/40 hover:text-white">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <nav className="p-4 space-y-1 flex-1">
                {navLinks.map(({ label, href }) => (
                  <Link
                    key={href}
                    href={href}
                    onClick={() => setMobileOpen(false)}
                    className="block px-3 py-2.5 rounded-lg text-sm text-white/60 hover:text-[var(--accent-champagne)] hover:bg-white/[0.04] transition-colors"
                  >
                    {label}
                  </Link>
                ))}
              </nav>
              <div className="p-4 border-t border-white/[0.06]">
                {isLoggedIn ? (
                  <>
                    <p className="text-xs text-white/30 mb-3 px-1">{user?.email}</p>
                    {scope === "partner" && (
                      <Link
                        href="/analysis/new"
                        onClick={() => setMobileOpen(false)}
                        className="flex items-center justify-center gap-2 w-full h-10 rounded-lg text-sm font-medium text-[#0a0a12] mb-2"
                        style={{ background: "linear-gradient(135deg, #e8dcc8, #c4a574)" }}
                      >
                        <Plus className="w-4 h-4" /> New Analysis
                      </Link>
                    )}
                    <button
                      onClick={() => { setMobileOpen(false); handleLogout(); }}
                      className="flex items-center justify-center gap-2 w-full h-10 rounded-lg text-sm text-rose-400 border border-rose-900/30 hover:bg-rose-950/20 transition-colors"
                    >
                      <LogOut className="w-4 h-4" /> Sign Out
                    </button>
                  </>
                ) : (
                  <Link
                    href="/login"
                    onClick={() => setMobileOpen(false)}
                    className="flex items-center justify-center gap-2 w-full h-10 rounded-lg text-sm font-medium text-[#0a0a12]"
                    style={{ background: "linear-gradient(135deg, #e8dcc8, #c4a574)" }}
                  >
                    <LogIn className="w-4 h-4" /> Sign In
                  </Link>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
