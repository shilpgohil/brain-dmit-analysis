"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { AnalysisResult, QuotientKey } from "@/lib/types";
import { QUOTIENT_LABELS } from "@/lib/types";
import { GOLD, PLUM, SAGE, scoreToGoldTier, chartTooltipStyle } from "@/lib/analysis-theme";
import { cn, measuredEntries } from "@/lib/utils";

const QUOTIENT_DESCRIPTIONS: Record<QuotientKey, string> = {
  IQ: "Logical reasoning, pattern recognition, memory, and analytical thinking",
  EQ: "Self-awareness, empathy, emotional stability, and social sensitivity",
  CQ: "Imagination, innovation, original thinking, and creative expression",
  AQ: "Learning agility, resilience, flexibility, and recovery from change",
  SQ: "Communication, interpersonal skills, teamwork, and social influence",
  PQ: "Body coordination, motor skills, and kinaesthetic intelligence",
  LQ: "Vision, strategic thinking, team management, and authority",
  MQ: "Goal orientation, persistence, self-discipline, and achievement drive",
  FQ: "Concentration, attention span, mental discipline, and task completion",
  DQ: "Judgment, risk assessment, ethical reasoning, and outcome evaluation",
};

const ORDER: QuotientKey[] = ["IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ"];

const Q_COLORS: Record<QuotientKey, string> = {
  IQ: "#00d4ff",
  EQ: "#b87d8a",
  CQ: "#9d8bb5",
  AQ: "#6b9e8f",
  SQ: "#c4a574",
  PQ: "#7a9e6b",
  LQ: "#d4a574",
  MQ: "#8b9eb7",
  FQ: "#a89b7c",
  DQ: "#e8dcc8",
};

function QuotientCircle({
  k,
  value,
  index,
}: {
  k: QuotientKey;
  value: number | null | undefined;
  index: number;
}) {
  const pct = value != null ? Math.round(Math.min(1, Math.max(0, value)) * 100) : null;
  const color = Q_COLORS[k];
  const radius = 26;
  const circ = 2 * Math.PI * radius;
  const tier = pct != null ? scoreToGoldTier(value!) : null;

  return (
    <motion.div
      className="flex flex-col items-center gap-2"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="relative w-16 h-16">
        <svg width={64} height={64} className="-rotate-90">
          <circle cx={32} cy={32} r={radius} fill="none"
            stroke="rgba(255,255,255,0.06)" strokeWidth={4} />
          <motion.circle
            cx={32} cy={32} r={radius} fill="none"
            stroke={color} strokeWidth={4} strokeLinecap="round"
            strokeDasharray={circ}
            initial={{ strokeDashoffset: circ }}
            animate={{ strokeDashoffset: pct != null ? circ * (1 - pct / 100) : circ }}
            transition={{ duration: 1.1, delay: 0.2 + index * 0.05, ease: [0.16, 1, 0.3, 1] }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[10px] font-bold font-mono" style={{ color }}>
            {k}
          </span>
          <span className="text-[9px] font-mono text-white/60 tabular-nums">
            {pct != null ? `${pct}%` : "N/A"}
          </span>
        </div>
      </div>
      <div className="text-center">
        <p className="text-[9px] text-white/50 font-medium leading-tight">
          {QUOTIENT_LABELS[k].replace(" Quotient", "")}
        </p>
        {tier && (
          <p className="text-[8px] font-mono uppercase tracking-wide mt-0.5" style={{ color: tier.color }}>
            {tier.label}
          </p>
        )}
      </div>
    </motion.div>
  );
}

export function QuotientsTab({ result }: { result: AnalysisResult }) {
  const quotients = result.quotients;

  const present = useMemo(
    () => ORDER.filter((k) => quotients?.[k] != null),
    [quotients]
  );

  const radarData = useMemo(
    () =>
      ORDER.filter((k) => quotients?.[k] != null).map((k) => ({
        subject: k,
        value: Math.round((quotients![k]!) * 100),
        fullMark: 100,
      })),
    [quotients]
  );

  const sorted = useMemo(
    () =>
      present
        .map((k) => ({ k, v: quotients![k]! }))
        .sort((a, b) => b.v - a.v),
    [present, quotients]
  );

  const topStrengths = sorted.slice(0, 3);
  const developing = sorted.slice(-3).reverse();

  if (!quotients || present.length === 0) {
    return (
      <motion.div
        className="rounded-2xl p-12 text-center"
        style={{ border: `1px solid ${GOLD.border}`, background: GOLD.dim }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <p className="font-serif-display text-xl text-[#e8dcc8] mb-2">Quotient data not available</p>
        <p className="text-sm text-white/30 max-w-md mx-auto">
          Re-run the analysis to compute the full 10-quotient profile from this session&apos;s biometric data.
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8"
    >
      {/* Intro banner */}
      <motion.div
        className="rounded-2xl p-6"
        style={{ background: "linear-gradient(135deg, rgba(196,165,116,0.10) 0%, rgba(8,8,20,0.8) 60%)", border: `1px solid ${GOLD.border}` }}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <p className="text-[10px] font-mono uppercase tracking-widest mb-1" style={{ color: GOLD.primary }}>
          Brain Potential Dashboard
        </p>
        <h2 className="font-serif-display text-2xl text-[#e8dcc8] mb-2">
          10-Quotient Intelligence Profile
        </h2>
        <p className="text-sm text-white/40 max-w-2xl leading-relaxed">
          Each quotient is a real composite derived from biometric fingerprint data — ridge patterns,
          extension scores, MI measurements, and personality traits. Missing quotients (N/A) mean the
          required biometric data was unavailable for that dimension.
        </p>
      </motion.div>

      {/* Circle gauges 2×5 grid */}
      <div className="rounded-2xl p-6" style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}>
        <h3 className="text-sm font-medium text-white/50 uppercase tracking-widest font-mono mb-6">All Quotients</h3>
        <div className="grid grid-cols-5 gap-6">
          {ORDER.map((k, i) => (
            <QuotientCircle key={k} k={k} value={quotients[k]} index={i} />
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Radar chart */}
        {radarData.length >= 3 && (
          <motion.div
            className="rounded-2xl p-6"
            style={{ background: "rgba(255,255,255,0.02)", border: `1px solid ${GOLD.border}` }}
            initial={{ opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.15 }}
          >
            <h3 className="font-serif-display text-lg text-[#e8dcc8] mb-1">Quotient Radar</h3>
            <p className="text-[10px] text-white/25 font-mono uppercase tracking-widest mb-4">
              Full spectrum view
            </p>
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData} margin={{ top: 16, right: 28, bottom: 16, left: 28 }}>
                  <PolarGrid stroke="rgba(196,165,116,0.12)" />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: "rgba(232,220,200,0.6)", fontSize: 11, fontFamily: "inherit", fontWeight: 600 }}
                    tickLine={false}
                  />
                  <Radar
                    name="Score"
                    dataKey="value"
                    stroke={GOLD.primary}
                    fill={GOLD.primary}
                    fillOpacity={0.18}
                    strokeWidth={2}
                  />
                  <Tooltip
                    {...chartTooltipStyle}
                    formatter={(v, name) => [`${v}%`, QUOTIENT_LABELS[name as QuotientKey] ?? name]}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}

        {/* Strengths + developing */}
        <motion.div
          className="space-y-4"
          initial={{ opacity: 0, x: 12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          {/* Top 3 */}
          <div className="rounded-2xl p-5" style={{ background: "rgba(255,255,255,0.02)", border: `1px solid ${GOLD.border}` }}>
            <p className="text-[10px] font-mono uppercase tracking-widest mb-4" style={{ color: GOLD.primary }}>
              Strongest Quotients
            </p>
            {topStrengths.map(({ k, v }, i) => {
              const pct = Math.round(v * 100);
              const color = Q_COLORS[k];
              return (
                <motion.div
                  key={k}
                  className={cn("flex items-start gap-3 mb-4", i < topStrengths.length - 1 ? "pb-4 border-b border-white/[0.05]" : "")}
                  initial={{ opacity: 0, x: 12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * i }}
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center font-mono text-xs font-bold"
                    style={{ background: `${color}18`, color, border: `1px solid ${color}40` }}>
                    {k}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-medium text-white/80">{QUOTIENT_LABELS[k]}</p>
                      <span className="text-sm font-mono" style={{ color }}>{pct}%</span>
                    </div>
                    <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.05)" }}>
                      <motion.div className="h-full rounded-full" style={{ background: color }}
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 0.8, delay: 0.2 + i * 0.05 }}
                      />
                    </div>
                    <p className="text-[10px] text-white/30 mt-1 leading-snug">{QUOTIENT_DESCRIPTIONS[k]}</p>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Developing */}
          <div className="rounded-2xl p-5" style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)" }}>
            <p className="text-[10px] font-mono uppercase tracking-widest mb-4 text-white/35">
              Development Areas
            </p>
            {developing.map(({ k, v }, i) => {
              const pct = Math.round(v * 100);
              return (
                <motion.div
                  key={k}
                  className={cn("flex items-start gap-3 mb-3", i < developing.length - 1 ? "pb-3 border-b border-white/[0.05]" : "")}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.15 + i * 0.08 }}
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center font-mono text-xs font-bold"
                    style={{ background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.35)", border: "1px solid rgba(255,255,255,0.08)" }}>
                    {k}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-xs text-white/55">{QUOTIENT_LABELS[k]}</p>
                      <span className="text-xs font-mono text-white/40">{pct}%</span>
                    </div>
                    <p className="text-[10px] text-white/25 leading-snug">{QUOTIENT_DESCRIPTIONS[k]}</p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* Full description table */}
      <motion.div
        className="rounded-2xl p-6"
        style={{ background: "rgba(255,255,255,0.015)", border: "1px solid rgba(255,255,255,0.05)" }}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <h3 className="font-serif-display text-lg text-[#e8dcc8] mb-5">Complete Quotient Breakdown</h3>
        <div className="space-y-3">
          {ORDER.map((k, i) => {
            const v = quotients[k];
            const pct = v != null ? Math.round(v * 100) : null;
            const color = Q_COLORS[k];
            const tier = pct != null ? scoreToGoldTier(v!) : null;
            return (
              <motion.div
                key={k}
                className="grid grid-cols-[3rem_1fr_auto] items-center gap-4 py-3 border-b border-white/[0.05] last:border-0"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.03 * i }}
              >
                <div className="font-mono text-sm font-bold text-center py-1 rounded-lg"
                  style={{ background: `${color}15`, color }}>
                  {k}
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm text-white/70">{QUOTIENT_LABELS[k]}</span>
                    {tier && (
                      <span className="text-[8px] font-mono uppercase tracking-widest px-2 py-0.5 rounded-full"
                        style={{ color: tier.color, background: `${tier.color}15` }}>
                        {tier.label}
                      </span>
                    )}
                  </div>
                  <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.04)" }}>
                    {pct != null && (
                      <motion.div className="h-full rounded-full" style={{ background: color }}
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 0.9, delay: 0.4 + i * 0.04 }}
                      />
                    )}
                  </div>
                  <p className="text-[10px] text-white/25 mt-1">{QUOTIENT_DESCRIPTIONS[k]}</p>
                </div>
                <div className="text-right">
                  <span className="text-xl font-mono tabular-nums" style={{ color: pct != null ? color : "rgba(255,255,255,0.2)" }}>
                    {pct != null ? `${pct}%` : "N/A"}
                  </span>
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </motion.div>
  );
}
