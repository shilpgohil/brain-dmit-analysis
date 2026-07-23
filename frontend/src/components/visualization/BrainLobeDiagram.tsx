"use client";

import { motion } from "framer-motion";
import type { BrainLobeCapacity } from "@/lib/types";
import { lobeLabel, lobeDescription, isMeasured, pct } from "@/lib/utils";

interface BrainLobeDiagramProps {
  data: BrainLobeCapacity;
}

const LOBES = [
  {
    key: "prefrontal_lobe" as const,
    x: 145, y: 40, w: 90, h: 50,
    finger: "Thumb",
    color: "#8b5cf6",
  },
  {
    key: "posterior_frontal" as const,
    x: 80, y: 50, w: 75, h: 45,
    finger: "Index",
    color: "#3b82f6",
  },
  {
    key: "parietal_lobe" as const,
    x: 145, y: 95, w: 90, h: 50,
    finger: "Middle",
    color: "#00d4ff",
  },
  {
    key: "temporal_lobe" as const,
    x: 55, y: 115, w: 70, h: 45,
    finger: "Ring",
    color: "#f59e0b",
  },
  {
    key: "occipital_lobe" as const,
    x: 145, y: 150, w: 90, h: 50,
    finger: "Little",
    color: "#10b981",
  },
];

export function BrainLobeDiagram({ data }: BrainLobeDiagramProps) {
  return (
    <div className="space-y-3">
      {LOBES.map((lobe, i) => {
        const value = data[lobe.key];
        const measured = isMeasured(value);
        const width = measured ? Math.round(value * 100) : 0;
        const hemis = data.lobe_hemispheres?.[lobe.key];

        return (
          <motion.div
            key={lobe.key}
            className="group"
            initial={{ opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="flex items-center gap-3 mb-1.5">
              <div
                className="w-2 h-2 rounded-full flex-shrink-0"
                style={{ background: lobe.color, boxShadow: `0 0 8px ${lobe.color}80` }}
              />
              <span className="text-xs font-medium text-white/70">{lobeLabel(lobe.key)}</span>
              <span className="text-[10px] text-white/25 font-mono ml-auto">
                {lobe.finger} finger
              </span>
              <span
                className="text-xs font-bold font-mono"
                style={{ color: measured ? lobe.color : "rgba(255,255,255,0.3)" }}
              >
                {pct(value)}
              </span>
            </div>
            <div
              className="h-1.5 rounded-full overflow-hidden"
              style={{ background: "rgba(255,255,255,0.05)" }}
            >
              <motion.div
                className="h-full rounded-full"
                style={{ background: `linear-gradient(90deg, ${lobe.color}80, ${lobe.color})` }}
                initial={{ width: 0 }}
                animate={{ width: `${width}%` }}
                transition={{ duration: 0.9, delay: 0.3 + i * 0.08, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
            {hemis && (isMeasured(hemis.left) || isMeasured(hemis.right)) && (
              <div className="flex items-center gap-3 mt-1 text-[9px] font-mono text-white/30">
                <span>L (right hand): {pct(hemis.left)}</span>
                <span>R (left hand): {pct(hemis.right)}</span>
              </div>
            )}
            <p className="text-[10px] text-white/20 mt-1 leading-snug">
              {lobeDescription(lobe.key)}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}
