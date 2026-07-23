"use client";

import { useEffect, useRef } from "react";
import { motion, useInView } from "framer-motion";

interface ScoreOrbProps {
  value: number; // 0–1
  label: string;
  sublabel?: string;
  size?: "sm" | "md" | "lg";
  color?: "cyan" | "violet" | "amber" | "emerald" | "blue";
}

const SIZE_MAP = {
  sm: { outer: 56, stroke: 3, r: 22, fontSize: "text-xs", labelSize: "text-[9px]" },
  md: { outer: 80, stroke: 4, r: 32, fontSize: "text-sm", labelSize: "text-[10px]" },
  lg: { outer: 110, stroke: 5, r: 44, fontSize: "text-base", labelSize: "text-xs" },
};

const COLOR_MAP = {
  cyan:    { stroke: "#00d4ff", glow: "rgba(0,212,255,0.5)",   text: "text-[#00d4ff]" },
  violet:  { stroke: "#8b5cf6", glow: "rgba(139,92,246,0.5)",  text: "text-violet-400" },
  amber:   { stroke: "#f59e0b", glow: "rgba(245,158,11,0.5)",  text: "text-amber-400" },
  emerald: { stroke: "#10b981", glow: "rgba(16,185,129,0.5)",  text: "text-emerald-400" },
  blue:    { stroke: "#3b82f6", glow: "rgba(59,130,246,0.5)",  text: "text-blue-400" },
};

export function ScoreOrb({ value, label, sublabel, size = "md", color = "cyan" }: ScoreOrbProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(containerRef, { once: true });
  const config = SIZE_MAP[size];
  const colorConfig = COLOR_MAP[color];
  const clamped = Math.min(Math.max(value, 0), 1);
  const circumference = 2 * Math.PI * config.r;
  const offset = circumference * (1 - clamped);
  const pct = Math.round(clamped * 100);

  return (
    <div className="flex flex-col items-center gap-2" ref={containerRef}>
      <div className="relative" style={{ width: config.outer, height: config.outer }}>
        <svg
          width={config.outer}
          height={config.outer}
          viewBox={`0 0 ${config.outer} ${config.outer}`}
          className="-rotate-90"
          style={{ filter: `drop-shadow(0 0 8px ${colorConfig.glow})` }}
        >
          {/* Track */}
          <circle
            cx={config.outer / 2}
            cy={config.outer / 2}
            r={config.r}
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth={config.stroke}
          />
          {/* Fill */}
          <motion.circle
            cx={config.outer / 2}
            cy={config.outer / 2}
            r={config.r}
            fill="none"
            stroke={colorConfig.stroke}
            strokeWidth={config.stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1], delay: 0.2 }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.span
            className={`font-mono font-bold ${config.fontSize} ${colorConfig.text}`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            {pct}
          </motion.span>
        </div>
      </div>
      <div className="text-center">
        <p className={`${config.fontSize} font-medium text-white/70 leading-tight`}>{label}</p>
        {sublabel && <p className={`${config.labelSize} text-white/30 mt-0.5`}>{sublabel}</p>}
      </div>
    </div>
  );
}
