"use client";

import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Cell,
} from "recharts";
import type { ExtensionResult } from "@/lib/types";
import { GOLD, scoreToGoldTier, chartTooltipStyle, chartCursorStyle } from "@/lib/analysis-theme";
import { cn } from "@/lib/utils";
import { Search, Sparkles, ChevronDown, X } from "lucide-react";

const PLUM = "#9d8bb5";
const SAGE = "#6b9e8f";

const CATEGORY_COLORS: Record<string, string> = {
  Intelligence: GOLD.primary,
  Cognitive: "#8b9eb7",
  Emotional: "#b87d8a",
  Career: GOLD.bright,
  Leadership: "#d4a574",
  Learning: SAGE,
  Social: PLUM,
  Personality: "#a89b7c",
  Wellness: "#6b9e8f",
  Creative: "#9d8bb5",
  Advanced: "#7a9e6b",
  Brain: PLUM,
  Neurological: "#8b9eb7",
  General: "rgba(255,255,255,0.4)",
};

function subScores(ext: ExtensionResult) {
  return Object.entries(ext.scores)
    .filter(([k]) => !["overall", "score", "recommendations"].includes(k))
    .sort(([, a], [, b]) => b - a)
    .slice(0, 6);
}

function ExtensionDetailCard({
  ext,
  index,
  featured = false,
}: {
  ext: ExtensionResult;
  index: number;
  featured?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const safeScore = Math.min(1, Math.max(0, ext.primary_score));
  const pct = Math.round(safeScore * 100);
  const tier = scoreToGoldTier(safeScore);
  const accent = CATEGORY_COLORS[ext.category] ?? GOLD.primary;
  const subs = subScores(ext);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 16, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.96 }}
      transition={{ duration: 0.4, delay: Math.min(index * 0.02, 0.4), ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        "relative rounded-2xl overflow-hidden cursor-pointer group",
        featured ? "p-6" : "p-4"
      )}
      style={{
        background: `linear-gradient(160deg, ${accent}12 0%, rgba(8,8,20,0.85) 60%)`,
        border: `1px solid ${accent}35`,
      }}
      onClick={() => setOpen(!open)}
      whileHover={{ y: -3, boxShadow: `0 12px 40px ${accent}20` }}
    >
      <motion.div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at top right, ${accent}15 0%, transparent 60%)`,
        }}
      />

      <motion.div className="relative z-10">
        <motion.div className="flex items-start justify-between gap-3 mb-4">
          <motion.div className="flex-1 min-w-0">
            <span
              className="text-[8px] font-mono uppercase tracking-[0.2em] px-2 py-0.5 rounded-full inline-block mb-2"
              style={{ color: accent, background: `${accent}18`, border: `1px solid ${accent}30` }}
            >
              {ext.category}
            </span>
            <h4
              className={cn(
                "font-medium text-white/90 leading-snug",
                featured ? "text-base" : "text-sm"
              )}
            >
              {ext.name}
            </h4>
            <p className="text-[10px] text-white/25 mt-1">{tier.label} expression</p>
          </motion.div>

          <motion.div
            className="relative flex-shrink-0"
            initial={{ rotate: -90 }}
            animate={{ rotate: 0 }}
          >
            <svg width={featured ? 72 : 56} height={featured ? 72 : 56} className="-rotate-90">
              <circle
                cx={featured ? 36 : 28}
                cy={featured ? 36 : 28}
                r={featured ? 30 : 22}
                fill="none"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth={featured ? 4 : 3}
              />
              <motion.circle
                cx={featured ? 36 : 28}
                cy={featured ? 36 : 28}
                r={featured ? 30 : 22}
                fill="none"
                stroke={accent}
                strokeWidth={featured ? 4 : 3}
                strokeLinecap="round"
                strokeDasharray={2 * Math.PI * (featured ? 30 : 22)}
                initial={{ strokeDashoffset: 2 * Math.PI * (featured ? 30 : 22) }}
                animate={{
                  strokeDashoffset:
                    2 * Math.PI * (featured ? 30 : 22) * (1 - safeScore),
                }}
                transition={{ duration: 1, delay: index * 0.03, ease: [0.16, 1, 0.3, 1] }}
              />
            </svg>
            <span
              className="absolute inset-0 flex items-center justify-center font-mono font-bold tabular-nums"
              style={{ color: tier.color, fontSize: featured ? 14 : 11 }}
            >
              {pct}
            </span>
          </motion.div>
        </motion.div>

        <AnimatePresence>
          {(open || featured) && subs.length > 0 && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.35 }}
              className="overflow-hidden"
            >
              <motion.div className="space-y-2 pt-3 border-t border-white/[0.06]">
                {subs.map(([k, v], i) => (
                  <motion.div key={k} className="flex items-center gap-2">
                    <span className="text-[9px] text-white/35 w-24 truncate capitalize">
                      {k.replace(/_/g, " ")}
                    </span>
                    <motion.div
                      className="flex-1 h-1 rounded-full overflow-hidden"
                      style={{ background: "rgba(255,255,255,0.05)" }}
                    >
                      <motion.div
                        className="h-full rounded-full"
                        style={{ background: accent }}
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(100, v * 100)}%` }}
                        transition={{ delay: 0.1 + i * 0.04, duration: 0.6 }}
                      />
                    </motion.div>
                    <span className="text-[9px] font-mono w-8 text-right" style={{ color: accent }}>
                      {Math.round(Math.min(1, Math.max(0, v)) * 100)}
                    </span>
                  </motion.div>
                ))}
              </motion.div>

              {/* Description */}
              {ext.description && (
                <motion.div
                  className="mt-3 pt-3 border-t border-white/[0.05]"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.15 }}
                >
                  <p className="text-[9px] font-mono uppercase tracking-widest text-white/25 mb-1">About</p>
                  <p className="text-[10px] text-white/40 leading-relaxed">{ext.description}</p>
                </motion.div>
              )}

              {/* Recommendations */}
              {ext.recommendations && ext.recommendations.length > 0 && (
                <motion.div
                  className="mt-3 pt-3 border-t border-white/[0.05]"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <p className="text-[9px] font-mono uppercase tracking-widest mb-2"
                    style={{ color: accent }}>
                    Development Tips
                  </p>
                  <ul className="space-y-1.5">
                    {ext.recommendations.slice(0, 3).map((rec, i) => (
                      <li key={i} className="flex items-start gap-2 text-[10px] text-white/45 leading-snug">
                        <span className="flex-shrink-0 mt-0.5 w-3.5 h-3.5 rounded-full flex items-center justify-center"
                          style={{ background: `${accent}20`, color: accent, fontSize: 7, fontWeight: 700 }}>
                          {i + 1}
                        </span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {!featured && (
          <motion.p
            className="text-[9px] text-white/20 flex items-center justify-center gap-1 mt-2"
            animate={{ opacity: open ? 0 : 1 }}
          >
            <ChevronDown className={cn("w-3 h-3 transition-transform", open && "rotate-180")} />
            {open ? "Collapse" : "View sub-scores"}
          </motion.p>
        )}
      </motion.div>
    </motion.div>
  );
}

export function ExtensionsTab({ extensions }: { extensions: ExtensionResult[] }) {
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");

  const categories = useMemo(
    () => ["All", ...Array.from(new Set(extensions.map((e) => e.category))).sort()],
    [extensions]
  );

  const filtered = useMemo(() => {
    let list = extensions;
    if (category !== "All") list = list.filter((e) => e.category === category);
    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter((e) => e.name.toLowerCase().includes(q) || e.category.toLowerCase().includes(q));
    }
    return [...list].sort((a, b) => b.primary_score - a.primary_score);
  }, [extensions, category, search]);

  const featured = filtered.slice(0, 3);
  const rest = filtered.slice(3);

  const categoryChart = useMemo(() => {
    const map: Record<string, number[]> = {};
    for (const e of extensions) {
      if (!map[e.category]) map[e.category] = [];
      map[e.category].push(e.primary_score);
    }
    return Object.entries(map)
      .map(([cat, scores]) => ({
        name: cat,
        avg: Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 100),
        count: scores.length,
      }))
      .sort((a, b) => b.avg - a.avg);
  }, [extensions]);

  if (extensions.length === 0) {
    return (
      <motion.div className="py-20 text-center text-white/30 font-serif-display text-xl">
        No extension modules in this analysis.
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Summary header */}
      <motion.div
        className="rounded-2xl p-6 relative overflow-hidden"
        style={{
          background: "linear-gradient(135deg, rgba(196,165,116,0.1) 0%, rgba(8,8,20,0.8) 100%)",
          border: `1px solid ${GOLD.border}`,
        }}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <motion.div
          className="absolute inset-0 pointer-events-none"
          animate={{
            background: [
              "radial-gradient(circle at 20% 50%, rgba(196,165,116,0.08) 0%, transparent 50%)",
              "radial-gradient(circle at 80% 50%, rgba(157,139,181,0.08) 0%, transparent 50%)",
              "radial-gradient(circle at 20% 50%, rgba(196,165,116,0.08) 0%, transparent 50%)",
            ],
          }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div className="relative z-10 grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
          <motion.div className="lg:col-span-1">
            <motion.div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4" style={{ color: GOLD.primary }} />
              <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-white/35">
                Extension Intelligence Matrix
              </span>
            </motion.div>
            <h2 className="font-serif-display text-2xl text-[#e8dcc8]">
              {extensions.length} Cognitive Modules
            </h2>
            <p className="text-xs text-white/30 mt-2 leading-relaxed max-w-sm">
              Holistic extension scores aggregated across all analyzed fingerprints. Tap any card to
              reveal dimensional sub-scores.
            </p>
          </motion.div>
          <motion.div className="lg:col-span-2 h-[160px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryChart} layout="vertical" margin={{ left: 8, right: 16 }}>
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={90}
                  tick={{ fill: "rgba(255,255,255,0.45)", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  {...chartTooltipStyle}
                  contentStyle={{ ...chartTooltipStyle.contentStyle, fontSize: 11 }}
                  cursor={chartCursorStyle}
                  formatter={(v, _, item) => [
                    `${v}% avg · ${(item as { payload?: { count?: number } }).payload?.count ?? 0} modules`,
                    "",
                  ]}
                />
                <Bar dataKey="avg" radius={[0, 4, 4, 0]} maxBarSize={14}>
                  {categoryChart.map((entry, i) => (
                    <Cell
                      key={i}
                      fill={CATEGORY_COLORS[entry.name] ?? GOLD.primary}
                      fillOpacity={0.85}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Filters */}
      <motion.div className="flex flex-col sm:flex-row gap-3">
        <motion.div
          className="relative flex-1 max-w-xs"
          whileFocus={{ scale: 1.01 }}
        >
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/25 pointer-events-none" />
          <input
            // `type="search"` triggers the browser's native "searchfield"
            // appearance in Chrome/WebKit, which overrides most custom
            // width/padding/background styling and collapses the field to
            // a tiny native control with hard-to-see text. Plain `text`
            // (with `appearance-none` as a belt-and-suspenders reset, plus
            // our own clear button below) renders exactly as styled.
            type="text"
            placeholder="Search extensions..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-9 pl-9 pr-8 rounded-xl text-xs leading-none appearance-none bg-white/[0.05] border border-white/[0.1] text-white placeholder:text-white/30 focus:outline-none focus:border-[#c4a57480] focus:bg-white/[0.07]"
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch("")}
              aria-label="Clear search"
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-white/25 hover:text-white/60 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </motion.div>
        <motion.div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <motion.button
              key={cat}
              onClick={() => setCategory(cat)}
              className="text-[10px] px-3 py-1.5 rounded-full font-mono uppercase tracking-wide transition-all"
              style={
                category === cat
                  ? {
                      background: GOLD.dim,
                      color: GOLD.bright,
                      border: `1px solid ${GOLD.border}`,
                    }
                  : {
                      background: "rgba(255,255,255,0.03)",
                      color: "rgba(255,255,255,0.35)",
                      border: "1px solid rgba(255,255,255,0.06)",
                    }
              }
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.98 }}
            >
              {cat}
            </motion.button>
          ))}
        </motion.div>
      </motion.div>

      {/* Featured top 3 */}
      <motion.div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AnimatePresence mode="popLayout">
          {featured.map((ext, i) => (
            <ExtensionDetailCard key={ext.name} ext={ext} index={i} featured />
          ))}
        </AnimatePresence>
      </motion.div>

      {/* Rest grid */}
      <motion.div
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3"
        layout
      >
        <AnimatePresence mode="popLayout">
          {rest.map((ext, i) => (
            <ExtensionDetailCard key={ext.name} ext={ext} index={i + 3} />
          ))}
        </AnimatePresence>
      </motion.div>

      {filtered.length === 0 && (
        <p className="text-center text-white/25 py-12 text-sm">No extensions match your filter.</p>
      )}
    </motion.div>
  );
}
