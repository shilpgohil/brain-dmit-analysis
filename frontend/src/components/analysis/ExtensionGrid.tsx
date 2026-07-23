"use client";

import { useState } from "react";
import { cn, formatPercent, scoreBg } from "@/lib/utils";
import type { ExtensionResult } from "@/lib/types";
import { Card } from "@/components/ui/Card";

const CATEGORIES = [
  "All",
  "Intelligence",
  "Cognitive",
  "Emotional",
  "Career",
  "Leadership",
  "Learning",
  "Social",
  "Personality",
  "Wellness",
  "Creative",
  "Advanced",
];

interface ExtensionGridProps {
  extensions: ExtensionResult[];
}

export function ExtensionGrid({ extensions }: ExtensionGridProps) {
  const [activeCategory, setActiveCategory] = useState("All");

  const filtered =
    activeCategory === "All"
      ? extensions
      : extensions.filter((e) => e.category === activeCategory);

  const available = ["All", ...Array.from(new Set(extensions.map((e) => e.category)))];

  return (
    <div className="space-y-4">
      {/* Category filter */}
      <div className="flex gap-1.5 flex-wrap">
        {available.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={cn(
              "text-[10px] px-2.5 py-1 rounded font-medium uppercase tracking-wide transition-colors",
              activeCategory === cat
                ? "bg-blue-600/20 text-blue-400 border border-blue-800"
                : "bg-slate-900 text-slate-500 border border-slate-800 hover:text-slate-300 hover:border-slate-700"
            )}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {filtered.map((ext) => (
          <ExtensionCard key={ext.name} extension={ext} />
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="text-sm text-slate-600 py-4 text-center">
          No extensions in this category.
        </p>
      )}
    </div>
  );
}

function ExtensionCard({ extension }: { extension: ExtensionResult }) {
  const score = extension.primary_score;
  const pct = Math.round(score * 100);

  return (
    <div className="border border-slate-800 rounded-lg bg-slate-900 p-3 hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <p className="text-[11px] font-semibold text-slate-300 leading-tight pr-2">
          {extension.name}
        </p>
        <span className="text-[10px] text-slate-500 uppercase tracking-wide flex-shrink-0">
          {extension.category}
        </span>
      </div>

      {/* Score ring */}
      <div className="flex items-center gap-2.5 mb-2">
        <div className="relative w-10 h-10 flex-shrink-0">
          <svg viewBox="0 0 40 40" className="w-10 h-10 -rotate-90">
            <circle cx="20" cy="20" r="16" fill="none" stroke="#1e293b" strokeWidth="4" />
            <circle
              cx="20"
              cy="20"
              r="16"
              fill="none"
              stroke={score >= 0.75 ? "#10b981" : score >= 0.5 ? "#3b82f6" : score >= 0.25 ? "#f59e0b" : "#ef4444"}
              strokeWidth="4"
              strokeDasharray={`${score * 100.53} 100.53`}
              strokeLinecap="round"
            />
          </svg>
          <span className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-slate-300 font-mono">
            {pct}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          {Object.entries(extension.scores)
            .filter(([k]) => k !== "overall" && k !== "score")
            .slice(0, 3)
            .map(([k, v]) => (
              <div key={k} className="flex items-center gap-1 mb-0.5">
                <div className="flex-1 h-0.5 bg-slate-800 rounded overflow-hidden">
                  <div
                    className={cn("h-full rounded", scoreBg(v))}
                    style={{ width: `${v * 100}%` }}
                  />
                </div>
                <span className="text-[8px] text-slate-600 w-6 text-right font-mono">
                  {Math.round(v * 100)}
                </span>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
