"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiBase } from "@/lib/api";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { useAuthStore } from "@/store/authStore";
import { logoutAdmin } from "@/lib/auth-api";
import {
  Users, LayoutDashboard, Package, FileText,
  LogOut, Bell, CheckCircle2, Loader2,
  TrendingUp, Clock, AlertCircle,
} from "lucide-react";
import { GOLD } from "@/lib/analysis-theme";

interface DashStats {
  total_partners: number;
  active_partners: number;
  total_sessions: number;
  pending_requests: number;
  today_sessions: number;
}

function StatCard({ label, value, sub, color = GOLD.primary }: {
  label: string; value: number | string; sub?: string; color?: string;
}) {
  return (
    <motion.div
      className="rounded-2xl p-5"
      style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}
      whileHover={{ y: -2 }}
    >
      <p className="text-[10px] text-white/35 font-mono uppercase tracking-widest mb-2">{label}</p>
      <p className="text-3xl font-serif-display" style={{ color }}>{value}</p>
      {sub && <p className="text-xs text-white/25 mt-1">{sub}</p>}
    </motion.div>
  );
}

export default function AdminDashboard() {
  const { user, isLoading } = useAuthGuard("admin");
  const accessToken = useAuthStore((s) => s.accessToken);
  const router = useRouter();
  const [stats, setStats] = useState<DashStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!accessToken) return;
    fetch(`${apiBase()}/admin/dashboard`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
      .then((r) => r.json())
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [accessToken]);

  const handleLogout = async () => {
    await logoutAdmin();
    router.push("/login");
  };

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" />
      </div>
    );
  }

  const nav = [
    { href: "/admin", label: "Dashboard", icon: LayoutDashboard },
    { href: "/admin/partners", label: "Partners", icon: Users },
    { href: "/admin/requests", label: "Requests", icon: Bell, badge: stats?.pending_requests },
    { href: "/admin/plans", label: "Plans", icon: Package },
  ];

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-56 flex-shrink-0 border-r border-white/[0.06] flex flex-col"
        style={{ background: "rgba(8,8,20,0.8)" }}>
        <div className="p-5 border-b border-white/[0.06]">
          <p className="text-[10px] font-mono uppercase tracking-widest text-white/30 mb-0.5">Platform</p>
          <p className="font-serif-display text-white">Admin Console</p>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {nav.map(({ href, label, icon: Icon, badge }) => (
            <Link key={href} href={href}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-white/60 hover:text-white hover:bg-white/[0.04] transition-all relative">
              <Icon className="w-4 h-4 flex-shrink-0" />
              {label}
              {badge ? (
                <span className="ml-auto text-[9px] font-mono px-1.5 py-0.5 rounded-full"
                  style={{ background: "rgba(196,165,116,0.2)", color: "#c4a574" }}>
                  {badge}
                </span>
              ) : null}
            </Link>
          ))}
        </nav>
        <div className="p-3 border-t border-white/[0.06]">
          <p className="text-xs text-white/40 px-3 mb-1 truncate">{user.email}</p>
          <button onClick={handleLogout}
            className="flex items-center gap-3 px-3 py-2 rounded-xl text-sm text-white/40 hover:text-rose-400 hover:bg-rose-950/20 w-full transition-all">
            <LogOut className="w-4 h-4" /> Sign out
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-y-auto p-8">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-serif-display text-2xl text-white mb-1">Dashboard</h1>
          <p className="text-white/30 text-sm mb-8">Platform overview</p>

          {loading ? (
            <div className="flex items-center gap-2 text-white/30">
              <Loader2 className="w-4 h-4 animate-spin" /> Loading stats…
            </div>
          ) : stats ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
              <StatCard label="Total Partners" value={stats.total_partners} />
              <StatCard label="Active Partners" value={stats.active_partners} color="#10b981" />
              <StatCard label="Total Sessions" value={stats.total_sessions} />
              <StatCard label="Today" value={stats.today_sessions} sub="analyses today" color="#00d4ff" />
              <StatCard label="Pending" value={stats.pending_requests} sub="partner requests"
                color={stats.pending_requests > 0 ? "#f59e0b" : "rgba(255,255,255,0.3)"} />
            </div>
          ) : null}

          {/* Quick actions */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { href: "/admin/partners", label: "Manage Partners", sub: "Create, activate, configure", icon: Users, color: GOLD.primary },
              { href: "/admin/requests", label: "Review Requests", sub: `${stats?.pending_requests ?? 0} pending applications`, icon: Bell, color: "#f59e0b" },
              { href: "/admin/plans", label: "Manage Plans", sub: "Edit features per plan", icon: Package, color: "#9d8bb5" },
            ].map(({ href, label, sub, icon: Icon, color }) => (
              <Link key={href} href={href}>
                <motion.div
                  className="p-5 rounded-2xl cursor-pointer"
                  style={{ background: "rgba(255,255,255,0.02)", border: `1px solid rgba(255,255,255,0.06)` }}
                  whileHover={{ y: -3, borderColor: `${color}40` }}
                >
                  <Icon className="w-6 h-6 mb-3" style={{ color }} />
                  <p className="text-sm font-medium text-white/80">{label}</p>
                  <p className="text-xs text-white/30 mt-0.5">{sub}</p>
                </motion.div>
              </Link>
            ))}
          </div>
        </motion.div>
      </main>
    </div>
  );
}
