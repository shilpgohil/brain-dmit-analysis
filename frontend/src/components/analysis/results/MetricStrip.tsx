"use client";

import { motion } from "framer-motion";
import { GOLD } from "@/lib/analysis-theme";
import { measuredEntries } from "@/lib/utils";
import type { AnalysisResult } from "@/lib/types";

interface MetricStripProps {
  result: AnalysisResult;
}

export function MetricStrip({ result }: MetricStripProps) {
  const topMi = measuredEntries(result.multiple_intelligences).sort(
    ([, a], [, b]) => b - a,
  )[0];

  const metrics = [
    { label: "Biometric Features", value: result.total_features_extracted.toLocaleString(), sub: "extracted" },
    { label: "Fingerprints", value: String(result.fingers.length), sub: "analyzed" },
    { label: "Extensions", value: String(result.extensions.length), sub: "modules" },
    {
      label: "Dominant Intelligence",
      value: topMi ? Math.round(topMi[1] * 100) + "%" : "—",
      sub: topMi ? topMi[0].replace(/_/g, " ") : "pending",
    },
  ];

  return (
    <motion.div
      className="grid grid-cols-2 lg:grid-cols-4 gap-3"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      {metrics.map((m, i) => (
        <motion.div
          key={m.label}
          className="relative rounded-2xl p-4 overflow-hidden"
          style={{
            background: "rgba(196,165,116,0.04)",
            border: `1px solid ${GOLD.border}`,
          }}
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: i * 0.06, duration: 0.4 }}
          whileHover={{ scale: 1.02, borderColor: GOLD.glow }}
        >
          <motion.div
            className="absolute -top-8 -right-8 w-24 h-24 rounded-full opacity-30"
            style={{ background: `radial-gradient(circle, ${GOLD.glow} 0%, transparent 70%)` }}
            animate={{ scale: [1, 1.15, 1], opacity: [0.2, 0.35, 0.2] }}
            transition={{ duration: 4 + i, repeat: Infinity, ease: "easeInOut" }}
          />
          <p className="text-[9px] uppercase tracking-[0.2em] text-white/30 font-mono mb-1">{m.label}</p>
          <p className="text-2xl font-serif-display text-[#e8dcc8] tabular-nums">{m.value}</p>
          <p className="text-[10px] text-white/25 capitalize mt-0.5 truncate">{m.sub}</p>
        </motion.div>
      ))}
    </motion.div>
  );
}
