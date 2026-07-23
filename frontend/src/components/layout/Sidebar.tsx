"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FolderOpen,
  PlusCircle,
  FileText,
  Settings,
  Activity,
  Fingerprint,
} from "lucide-react";

const NAV = [
  { label: "Overview", href: "/", icon: LayoutDashboard },
  { label: "New Analysis", href: "/analysis/new", icon: PlusCircle },
  { label: "Sessions", href: "/sessions", icon: FolderOpen },
  { label: "System", href: "/system", icon: Activity },
  { label: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-56 bg-[#0d0d14] border-r border-slate-800/60 flex flex-col z-30">
      {/* Brand */}
      <div className="h-14 flex items-center px-5 border-b border-slate-800/60">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 flex items-center justify-center">
            <Fingerprint className="w-5 h-5 text-blue-400" strokeWidth={1.5} />
          </div>
          <div>
            <span className="text-sm font-semibold text-slate-100 tracking-tight">DMIT</span>
            <span className="text-[10px] text-slate-500 block leading-none tracking-widest uppercase">
              Platform
            </span>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {NAV.map(({ label, href, icon: Icon }) => {
          const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors duration-100",
                active
                  ? "bg-blue-600/15 text-blue-400 font-medium"
                  : "text-slate-500 hover:text-slate-300 hover:bg-slate-800/50"
              )}
            >
              <Icon className="w-4 h-4 flex-shrink-0" strokeWidth={active ? 2 : 1.5} />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-slate-800/60">
        <p className="text-[10px] text-slate-600 leading-relaxed">
          DMIT Platform v3.2
          <br />
          Scientific Biometric Analysis
        </p>
      </div>
    </aside>
  );
}
