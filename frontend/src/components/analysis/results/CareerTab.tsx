"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
} from "recharts";
import type { AnalysisResult } from "@/lib/types";
import { deriveCareerMatches, getCareerGuidanceExtension } from "@/lib/derive-careers";
import { measuredEntries } from "@/lib/utils";
import { GOLD, PLUM, scoreToGoldTier } from "@/lib/analysis-theme";
import { Briefcase, Target, TrendingUp, Compass } from "lucide-react";

const CLUSTER_ICONS: Record<string, typeof Briefcase> = {
  Career: Briefcase,
  Cluster: TrendingUp,
};

export function CareerTab({ result }: { result: AnalysisResult }) {
  const careers = useMemo(() => deriveCareerMatches(result), [result]);
  const guidance = getCareerGuidanceExtension(result.extensions);
  const primary = careers[0];
  const profile =
    typeof guidance?.scores?.career_guidance_profile === "string"
      ? guidance.scores.career_guidance_profile
      : typeof guidance?.scores?.primary_career_aptitude === "string"
        ? `Primary aptitude: ${guidance.scores.primary_career_aptitude}`
        : null;

  const chartData = careers.map((c) => ({
    name: c.title.length > 22 ? c.title.slice(0, 20) + "…" : c.title,
    fullName: c.title,
    value: Math.round(c.match_score * 100),
    category: c.category,
  }));

  const radarFromMi = measuredEntries(result.multiple_intelligences)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 6)
    .map(([k, v]) => ({
      subject: k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()).slice(0, 12),
      value: Math.round(v * 100),
    }));

  if (careers.length === 0) {
    return (
      <motion.div
        className="rounded-2xl p-12 text-center"
        style={{ border: `1px solid ${GOLD.border}`, background: GOLD.dim }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <Compass className="w-10 h-10 mx-auto mb-4 opacity-40" style={{ color: GOLD.primary }} />
        <p className="font-serif-display text-xl text-[#e8dcc8] mb-2">Career data synthesizing</p>
        <p className="text-sm text-white/30 max-w-md mx-auto">
          Re-run analysis to populate career aptitude from the guidance module, or ensure at least
          one fingerprint completed extraction.
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Hero primary match */}
      <motion.div
        className="relative rounded-2xl overflow-hidden p-8 sm:p-10"
        style={{
          background: "linear-gradient(145deg, rgba(196,165,116,0.14) 0%, rgba(8,8,20,0.9) 55%)",
          border: `1px solid ${GOLD.border}`,
        }}
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <motion.div
          className="absolute inset-0 pointer-events-none"
          animate={{
            background: [
              `radial-gradient(ellipse at 0% 50%, ${GOLD.glow} 0%, transparent 55%)`,
              `radial-gradient(ellipse at 100% 50%, rgba(157,139,181,0.2) 0%, transparent 55%)`,
              `radial-gradient(ellipse at 0% 50%, ${GOLD.glow} 0%, transparent 55%)`,
            ],
          }}
          transition={{ duration: 10, repeat: Infinity }}
        />
        <motion.div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <motion.div>
            <motion.span
              className="text-[10px] font-mono uppercase tracking-[0.25em] flex items-center gap-2 mb-3"
              style={{ color: GOLD.primary }}
            >
              <Target className="w-3.5 h-3.5" />
              Primary Career Aptitude
            </motion.span>
            <h2 className="font-serif-display text-3xl sm:text-4xl text-[#e8dcc8] leading-tight">
              {primary.title}
            </h2>
            <motion.p
              className="text-5xl sm:text-6xl font-mono mt-4 tabular-nums"
              style={{ color: GOLD.bright }}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
            >
              {Math.round(primary.match_score * 100)}%
              <span className="text-lg text-white/30 ml-2">match</span>
            </motion.p>
            {profile && (
              <p className="text-sm text-white/40 mt-4 leading-relaxed max-w-md">{profile}</p>
            )}
            <motion.p className="text-xs text-white/25 mt-4 leading-relaxed">
              Derived from dermatoglyphic ridge complexity, fractal dimension, and aggregated
              multiple-intelligence mapping across all submitted fingerprints.
            </motion.p>
          </motion.div>

          {radarFromMi.length > 0 && (
            <motion.div
              className="h-[260px]"
              initial={{ opacity: 0, rotate: -5 }}
              animate={{ opacity: 1, rotate: 0 }}
              transition={{ delay: 0.15 }}
            >
              <p className="text-[9px] font-mono uppercase tracking-widest text-white/30 mb-2 text-center">
                Intelligence drivers for career fit
              </p>
              <ResponsiveContainer width="100%" height="90%">
                <RadarChart data={radarFromMi}>
                  <PolarGrid stroke="rgba(196,165,116,0.15)" />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: "rgba(232,220,200,0.5)", fontSize: 9 }}
                  />
                  <Radar
                    dataKey="value"
                    stroke={PLUM}
                    fill={PLUM}
                    fillOpacity={0.2}
                    strokeWidth={2}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "rgba(8,8,20,0.95)",
                      border: `1px solid ${GOLD.border}`,
                      borderRadius: 8,
                    }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </motion.div>
          )}
        </motion.div>
      </motion.div>

      <motion.div className="grid grid-cols-1 xl:grid-cols-5 gap-5">
        {/* Bar chart all paths */}
        <motion.div
          className="xl:col-span-3 rounded-2xl p-6"
          style={{ background: "rgba(255,255,255,0.02)", border: `1px solid ${GOLD.border}` }}
          initial={{ opacity: 0, x: -12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h3 className="font-serif-display text-lg text-[#e8dcc8] mb-1">Career Path Rankings</h3>
          <p className="text-[10px] text-white/25 font-mono uppercase tracking-widest mb-5">
            {careers.length} aptitude vectors
          </p>
          <div className="h-[min(420px,50vh)]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ left: 4, right: 24 }}>
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={130}
                  tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    background: "rgba(8,8,20,0.95)",
                    border: `1px solid ${GOLD.border}`,
                    borderRadius: 10,
                  }}
                  formatter={(v, _, item) => {
                    const p = item as { payload?: { fullName?: string } };
                    return [`${v}%`, p.payload?.fullName ?? ""];
                  }}
                />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} maxBarSize={18}>
                  {chartData.map((entry, i) => {
                    const tier = scoreToGoldTier(entry.value / 100);
                    return (
                      <Cell
                        key={i}
                        fill={tier.color}
                        fillOpacity={0.9 - i * 0.03}
                      />
                    );
                  })}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Ranked list with detail */}
        <motion.div
          className="xl:col-span-2 space-y-3"
          initial={{ opacity: 0, x: 12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.15 }}
        >
          <h3 className="font-serif-display text-lg text-[#e8dcc8] mb-4">Detailed Matches</h3>
          {careers.map((career, i) => {
            const pct = Math.round(career.match_score * 100);
            const tier = scoreToGoldTier(career.match_score);
            const Icon = CLUSTER_ICONS[career.category] ?? Briefcase;
            return (
              <motion.div
                key={career.title}
                className="flex gap-4 p-4 rounded-xl"
                style={{
                  background: i === 0 ? GOLD.dim : "rgba(255,255,255,0.02)",
                  border: `1px solid ${i === 0 ? GOLD.border : "rgba(255,255,255,0.06)"}`,
                }}
                initial={{ opacity: 0, x: 16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.05 * i }}
                whileHover={{ x: 4, borderColor: GOLD.border }}
              >
                <motion.div
                  className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 font-mono text-sm font-bold"
                  style={{
                    background: `${tier.color}15`,
                    color: tier.color,
                    border: `1px solid ${tier.color}40`,
                  }}
                >
                  {i < 3 ? (
                    <Icon className="w-4 h-4" />
                  ) : (
                    <span className="text-white/40">{i + 1}</span>
                  )}
                </motion.div>
                <motion.div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <div>
                      <p className="text-sm font-medium text-white/85 leading-snug">
                        {career.title}
                      </p>
                      <p className="text-[9px] text-white/25 uppercase tracking-widest font-mono mt-0.5">
                        {career.category} · {tier.label}
                      </p>
                    </div>
                    <span className="text-lg font-mono tabular-nums flex-shrink-0" style={{ color: tier.color }}>
                      {pct}%
                    </span>
                  </div>
                  <motion.div
                    className="h-1 rounded-full overflow-hidden"
                    style={{ background: "rgba(255,255,255,0.05)" }}
                  >
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: GOLD.bar }}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 0.8, delay: 0.1 + i * 0.05 }}
                    />
                  </motion.div>
                </motion.div>
              </motion.div>
            );
          })}
        </motion.div>
      </motion.div>

      {/* Guidance sub-metrics */}
      {guidance && Object.keys(guidance.scores).length > 4 && (
        <motion.div
          className="rounded-2xl p-6"
          style={{ border: `1px solid rgba(157,139,181,0.25)`, background: "rgba(157,139,181,0.05)" }}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
        >
          <h3 className="font-serif-display text-lg text-[#e8dcc8] mb-4">
            Career Guidance — Full Metric Breakdown
          </h3>
          <motion.div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
            {Object.entries(guidance.scores)
              .filter(([k, v]) => typeof v === "number" && !["overall", "score"].includes(k))
              .sort(([, a], [, b]) => (b as number) - (a as number))
              .map(([k, v], i) => (
                <motion.div
                  key={k}
                  className="p-3 rounded-xl"
                  style={{ background: "rgba(0,0,0,0.25)", border: "1px solid rgba(255,255,255,0.06)" }}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.02 }}
                  whileHover={{ borderColor: PLUM }}
                >
                  <p className="text-[9px] text-white/30 capitalize truncate">
                    {k.replace(/_/g, " ")}
                  </p>
                  <p className="text-xl font-mono mt-1" style={{ color: GOLD.primary }}>
                    {Math.round(Math.min(1, Math.max(0, v as number)) * 100)}%
                  </p>
                </motion.div>
              ))}
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  );
}
