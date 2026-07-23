"use client";

import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import type { AnalysisResult } from "@/lib/types";
import { GoldRadarChart } from "@/components/charts/GoldRadarChart";
import { BrainLobeDiagram } from "@/components/visualization/BrainLobeDiagram";
import { PipelineTracker } from "@/components/analysis/PipelineTracker";
import { MetricStrip } from "./MetricStrip";
import { AtdPanel } from "./AtdPanel";
import { GOLD, PLUM, SAGE, scoreToGoldTier } from "@/lib/analysis-theme";
import { lobeLabel, measuredEntries, isMeasured, pct } from "@/lib/utils";

const MI_LABELS: Record<string, string> = {
  linguistic: "Linguistic",
  logical_mathematical: "Logical",
  spatial: "Spatial",
  musical: "Musical",
  bodily_kinesthetic: "Kinesthetic",
  interpersonal: "Interpersonal",
  intrapersonal: "Intrapersonal",
  naturalistic: "Naturalistic",
  existential: "Existential",
};

const PERSONALITY_LABELS: Record<string, string> = {
  openness: "Openness",
  conscientiousness: "Conscientiousness",
  extraversion: "Extraversion",
  agreeableness: "Agreeableness",
  neuroticism: "Neuroticism",
};

const PERSONALITY_DESC: Record<string, string> = {
  openness: "Creative curiosity & novel experience",
  conscientiousness: "Discipline, planning & reliability",
  extraversion: "Social energy & outward engagement",
  agreeableness: "Cooperation, trust & empathy",
  neuroticism: "Emotional sensitivity under stress",
};

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] as const } },
};

function Panel({
  title,
  subtitle,
  children,
  className = "",
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      variants={item}
      className={`rounded-2xl p-5 sm:p-6 relative overflow-hidden ${className}`}
      style={{
        background: "linear-gradient(145deg, rgba(196,165,116,0.06) 0%, rgba(8,8,20,0.6) 50%)",
        border: `1px solid ${GOLD.border}`,
        boxShadow: `0 0 60px ${GOLD.dim}`,
      }}
    >
      <motion.div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: `linear-gradient(90deg, transparent, ${GOLD.primary}, transparent)` }}
        animate={{ opacity: [0.3, 0.8, 0.3] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
      <motion.div
        className="absolute -top-20 -right-20 w-40 h-40 rounded-full pointer-events-none"
        style={{ background: `radial-gradient(circle, ${GOLD.glow} 0%, transparent 70%)` }}
        animate={{ scale: [1, 1.2, 1], opacity: [0.15, 0.25, 0.15] }}
        transition={{ duration: 5, repeat: Infinity }}
      />
      <div className="relative z-10">
        <div className="flex items-baseline justify-between gap-2 mb-5">
          <h3 className="font-serif-display text-xl text-[#e8dcc8] tracking-tight">{title}</h3>
          {subtitle && (
            <span className="text-[9px] font-mono uppercase tracking-[0.18em] text-white/25">{subtitle}</span>
          )}
        </div>
        {children}
      </div>
    </motion.div>
  );
}

function GoldBar({ label, value, delay = 0 }: { label: string; value: number; delay?: number }) {
  const pct = Math.round(value * 100);
  const tier = scoreToGoldTier(value);
  return (
    <motion.div
      className="space-y-1.5"
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.4 }}
    >
      <motion.div className="flex items-center justify-between gap-2">
        <span className="text-[11px] text-white/55 truncate">{label}</span>
        <span className="text-[11px] font-mono tabular-nums flex-shrink-0" style={{ color: tier.color }}>
          {pct}%
        </span>
      </motion.div>
      <motion.div className="h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.04)" }}>
        <motion.div
          className="h-full rounded-full"
          style={{ background: GOLD.bar }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.9, delay: delay + 0.1, ease: [0.16, 1, 0.3, 1] }}
        />
      </motion.div>
    </motion.div>
  );
}

export function OverviewTab({ result }: { result: AnalysisResult }) {
  const miEntries = measuredEntries(result.multiple_intelligences).sort(
    ([, a], [, b]) => b - a,
  );
  const hasMi = miEntries.length > 0;

  const radarData = miEntries.map(([k, v]) => ({
    label: MI_LABELS[k] ?? k,
    value: v,
  }));

  const learningEntries = measuredEntries(result.learning_styles);
  const learningData = learningEntries.map(([k, v]) => ({
    name: k.charAt(0).toUpperCase() + k.slice(1),
    value: Math.round(v * 100),
    fill: k === "visual" ? GOLD.primary : k === "auditory" ? PLUM : SAGE,
  }));

  const personalityEntries = measuredEntries(result.personality);

  const lobeBarData = result.brain_lobes
    ? (
        [
          "prefrontal_lobe",
          "posterior_frontal",
          "parietal_lobe",
          "temporal_lobe",
          "occipital_lobe",
        ] as const
      )
        .filter((k) => isMeasured(result.brain_lobes![k]))
        .map((k) => ({
          name: lobeLabel(k).split(" ")[0],
          value: Math.round((result.brain_lobes![k] as number) * 100),
        }))
    : [];

  const dominant = result.brain_lobes?.dominant_hemisphere;

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      <MetricStrip result={result} />

      {/* Intelligence — hero bento */}
      {hasMi && (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-5">
          <Panel title="Multiple Intelligences" subtitle="Gardner · DMIT" className="xl:col-span-7">
            <motion.div
              className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center"
              layout
            >
              <GoldRadarChart data={radarData} height={300} />
              <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1 custom-scrollbar">
                {miEntries.map(([k, v], i) => (
                  <GoldBar key={k} label={MI_LABELS[k] ?? k} value={v} delay={i * 0.04} />
                ))}
              </div>
            </motion.div>
            {/* Top 3 highlight */}
            <motion.div className="grid grid-cols-3 gap-2 mt-6 pt-5 border-t border-white/[0.06]">
              {miEntries.slice(0, 3).map(([k, v], i) => (
                <motion.div
                  key={k}
                  className="text-center p-3 rounded-xl"
                  style={{ background: GOLD.dim, border: `1px solid ${GOLD.border}` }}
                  whileHover={{ y: -2 }}
                >
                  <p className="text-[8px] uppercase tracking-widest text-white/30 font-mono">#{i + 1}</p>
                  <p className="text-lg font-serif-display text-[#e8dcc8] mt-1">{Math.round(v * 100)}%</p>
                  <p className="text-[10px] text-white/40 mt-0.5">{MI_LABELS[k]}</p>
                </motion.div>
              ))}
            </motion.div>
          </Panel>

          <div className="xl:col-span-5 space-y-5">
            {result.brain_lobes && (
              <Panel title="Brain Lobe Capacity" subtitle="Cross-lateral Map">
                <BrainLobeDiagram data={result.brain_lobes} />
                {lobeBarData.length > 0 && (
                  <div className="mt-4 h-[140px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={lobeBarData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                        <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 9 }} axisLine={false} tickLine={false} />
                        <YAxis domain={[0, 100]} hide />
                        <Tooltip
                          contentStyle={{
                            background: "rgba(8,8,20,0.95)",
                            border: `1px solid ${GOLD.border}`,
                            borderRadius: 8,
                            fontSize: 11,
                          }}
                          formatter={(v) => [`${v}%`, "Capacity"]}
                        />
                        <Bar dataKey="value" radius={[4, 4, 0, 0]} maxBarSize={28}>
                          {lobeBarData.map((_, idx) => (
                            <Cell key={idx} fill={idx % 2 === 0 ? GOLD.primary : PLUM} fillOpacity={0.85} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
                <motion.div
                  className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-white/[0.06]"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  {(["left_hemisphere", "right_hemisphere"] as const).map((k) => {
                    const side = k === "left_hemisphere" ? "left" : "right";
                    const isDominant = dominant === side;
                    return (
                      <motion.div
                        key={k}
                        className="p-3 rounded-xl text-center"
                        style={{
                          background: isDominant ? "rgba(157,139,181,0.16)" : "rgba(157,139,181,0.08)",
                          border: `1px solid ${isDominant ? PLUM : "rgba(157,139,181,0.2)"}`,
                        }}
                        whileHover={{ scale: 1.02 }}
                      >
                        <p className="text-[9px] text-white/30 uppercase tracking-widest font-mono">
                          {side === "left" ? "Left" : "Right"} Hemisphere
                        </p>
                        <p className="text-xl font-mono mt-1" style={{ color: PLUM }}>
                          {pct(result.brain_lobes![k])}
                        </p>
                        {isDominant && (
                          <p className="text-[8px] uppercase tracking-widest font-mono mt-0.5" style={{ color: PLUM }}>
                            Dominant
                          </p>
                        )}
                      </motion.div>
                    );
                  })}
                </motion.div>
                {dominant && (
                  <p className="text-[10px] text-white/30 mt-3 text-center">
                    {dominant === "balanced"
                      ? "Balanced hemispheric profile — analytical and holistic processing are evenly expressed."
                      : `${dominant === "left" ? "Left" : "Right"}-hemisphere dominant — ${
                          dominant === "left"
                            ? "analytical, sequential, language-led processing."
                            : "holistic, intuitive, spatial-led processing."
                        }`}
                  </p>
                )}
              </Panel>
            )}

            <AtdPanel atd={result.atd_analysis} palms={result.palms ?? []} />
          </div>
        </div>
      )}

      {/* Personality + Learning */}
      <motion.div variants={container} className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {personalityEntries.length > 0 && (
          <Panel title="Personality Profile" subtitle="Big Five Model">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {personalityEntries.map(([k, v], i) => (
                <motion.div
                  key={k}
                  className="p-4 rounded-xl"
                  style={{ background: "rgba(157,139,181,0.06)", border: "1px solid rgba(157,139,181,0.15)" }}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.05 }}
                  whileHover={{ borderColor: PLUM }}
                >
                  <div className="flex justify-between items-baseline mb-2">
                    <span className="text-xs font-medium text-white/70">
                      {PERSONALITY_LABELS[k] ?? k}
                    </span>
                    <span className="text-sm font-mono" style={{ color: PLUM }}>
                      {Math.round(v * 100)}%
                    </span>
                  </div>
                  <motion.div
                    className="h-1 rounded-full mb-2"
                    style={{ background: "rgba(255,255,255,0.05)" }}
                  >
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: `linear-gradient(90deg, ${PLUM}, #c4a574)` }}
                      initial={{ width: 0 }}
                      animate={{ width: `${v * 100}%` }}
                      transition={{ duration: 0.8, delay: 0.1 + i * 0.05 }}
                    />
                  </motion.div>
                  <p className="text-[10px] text-white/25 leading-snug">{PERSONALITY_DESC[k]}</p>
                </motion.div>
              ))}
            </div>
          </Panel>
        )}

        {learningEntries.length > 0 && (
          <Panel title="Learning Style Distribution" subtitle="VAK Model">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <motion.div
                className="w-[200px] h-[200px] flex-shrink-0"
                initial={{ rotate: -8, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                transition={{ duration: 0.7 }}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={learningData}
                      cx="50%"
                      cy="50%"
                      innerRadius={55}
                      outerRadius={85}
                      paddingAngle={4}
                      dataKey="value"
                      stroke="none"
                    >
                      {learningData.map((entry, i) => (
                        <Cell key={i} fill={entry.fill} fillOpacity={0.9} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: "rgba(8,8,20,0.95)",
                        border: `1px solid ${GOLD.border}`,
                        borderRadius: 8,
                      }}
                      formatter={(v) => [`${v}%`, ""]}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </motion.div>
              <motion.div
                className="flex-1 w-full space-y-4"
                variants={container}
                initial="hidden"
                animate="show"
              >
                {learningEntries.map(([k, v], i) => (
                  <GoldBar
                    key={k}
                    label={k.charAt(0).toUpperCase() + k.slice(1) + " Learning"}
                    value={v}
                    delay={i * 0.08}
                  />
                ))}
                <p className="text-[10px] text-white/20 leading-relaxed pt-2 border-t border-white/[0.05]">
                  Dominant modality guides study design, classroom engagement, and memory encoding strategies.
                </p>
              </motion.div>
            </div>
          </Panel>
        )}
      </motion.div>

      {/* Pipeline */}
      <Panel title="Analysis Pipeline" subtitle="Processing Audit">
        <PipelineTracker stages={result.pipeline_stages} />
      </Panel>
    </motion.div>
  );
}
