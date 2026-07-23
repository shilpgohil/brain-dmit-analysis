"use client";

import { usePathname } from "next/navigation";
import { Bell, Search } from "lucide-react";

const TITLES: Record<string, string> = {
  "/": "Overview",
  "/analysis/new": "New Analysis",
  "/sessions": "Analysis Sessions",
  "/system": "System Status",
  "/settings": "Settings",
};

export function TopBar() {
  const pathname = usePathname();

  const titleKey = Object.keys(TITLES)
    .filter((k) => pathname.startsWith(k) && k !== "/")
    .sort((a, b) => b.length - a.length)[0];

  const title = pathname === "/" ? "Overview" : (TITLES[titleKey] ?? "Analysis");

  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-slate-800/60 bg-[#0a0a12]/80 backdrop-blur-sm">
      <h1 className="text-sm font-medium text-slate-300 tracking-wide">{title}</h1>
      <div className="flex items-center gap-2">
        <button className="w-8 h-8 flex items-center justify-center rounded-md text-slate-500 hover:text-slate-300 hover:bg-slate-800 transition-colors">
          <Search className="w-4 h-4" />
        </button>
        <button className="w-8 h-8 flex items-center justify-center rounded-md text-slate-500 hover:text-slate-300 hover:bg-slate-800 transition-colors">
          <Bell className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
