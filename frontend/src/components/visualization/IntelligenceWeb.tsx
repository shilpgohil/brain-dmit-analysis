"use client";

import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import type { MultipleIntelligences } from "@/lib/types";

interface IntelligenceWebProps {
  data: MultipleIntelligences;
  size?: number;
}

const AXES = [
  { key: "linguistic" as const, label: "Linguistic" },
  { key: "logical_mathematical" as const, label: "Logical" },
  { key: "spatial" as const, label: "Spatial" },
  { key: "musical" as const, label: "Musical" },
  { key: "bodily_kinesthetic" as const, label: "Kinesthetic" },
  { key: "interpersonal" as const, label: "Interpersonal" },
  { key: "intrapersonal" as const, label: "Intrapersonal" },
  { key: "naturalistic" as const, label: "Naturalistic" },
  { key: "existential" as const, label: "Existential" },
];

function polar(angle: number, radius: number, cx: number, cy: number) {
  return {
    x: cx + radius * Math.cos(angle - Math.PI / 2),
    y: cy + radius * Math.sin(angle - Math.PI / 2),
  };
}

export function IntelligenceWeb({ data, size = 320 }: IntelligenceWebProps) {
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.38;
  const n = AXES.length;

  // Grid rings
  const rings = [0.25, 0.5, 0.75, 1.0];

  // Data polygon
  const dataPoints = AXES.map((axis, i) => {
    const angle = (i * 2 * Math.PI) / n;
    const r = (data[axis.key] ?? 0) * maxR;
    return polar(angle, r, cx, cy);
  });

  const polygonPath = dataPoints.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ") + " Z";

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background rings */}
        {rings.map((r) =>
          AXES.map((_, i) => {
            const a1 = (i * 2 * Math.PI) / n;
            const a2 = ((i + 1) * 2 * Math.PI) / n;
            const p1 = polar(a1, r * maxR, cx, cy);
            const p2 = polar(a2, r * maxR, cx, cy);
            return (
              <line
                key={`${r}-${i}`}
                x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y}
                stroke="rgba(255,255,255,0.05)"
                strokeWidth={0.5}
              />
            );
          })
        )}

        {/* Spoke lines */}
        {AXES.map((_, i) => {
          const angle = (i * 2 * Math.PI) / n;
          const outer = polar(angle, maxR, cx, cy);
          return (
            <line
              key={i}
              x1={cx} y1={cy} x2={outer.x} y2={outer.y}
              stroke="rgba(255,255,255,0.06)"
              strokeWidth={0.5}
            />
          );
        })}

        {/* Glow fill */}
        <defs>
          <radialGradient id="webGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.1" />
          </radialGradient>
          <filter id="webBlur">
            <feGaussianBlur stdDeviation="3" />
          </filter>
        </defs>

        {/* Blurred glow layer */}
        <motion.path
          d={polygonPath}
          fill="url(#webGlow)"
          filter="url(#webBlur)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.6 }}
          transition={{ duration: 1, delay: 0.3 }}
        />

        {/* Main polygon */}
        <motion.path
          d={polygonPath}
          fill="rgba(0,212,255,0.06)"
          stroke="rgba(0,212,255,0.6)"
          strokeWidth={1.5}
          strokeLinejoin="round"
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          style={{ transformOrigin: `${cx}px ${cy}px` }}
        />

        {/* Data points */}
        {dataPoints.map((p, i) => (
          <motion.circle
            key={i}
            cx={p.x} cy={p.y} r={3}
            fill="#00d4ff"
            initial={{ opacity: 0, r: 0 }}
            animate={{ opacity: 1, r: 3 }}
            transition={{ duration: 0.4, delay: 0.6 + i * 0.04 }}
          />
        ))}

        {/* Labels */}
        {AXES.map((axis, i) => {
          const angle = (i * 2 * Math.PI) / n;
          const p = polar(angle, maxR + 18, cx, cy);
          const textAnchor = p.x < cx - 5 ? "end" : p.x > cx + 5 ? "start" : "middle";
          const value = Math.round((data[axis.key] ?? 0) * 100);

          return (
            <g key={axis.key}>
              <text
                x={p.x} y={p.y}
                textAnchor={textAnchor}
                dominantBaseline="middle"
                fontSize={9}
                fill="rgba(255,255,255,0.4)"
                fontFamily="Inter, sans-serif"
              >
                {axis.label}
              </text>
              <text
                x={p.x} y={p.y + 10}
                textAnchor={textAnchor}
                dominantBaseline="middle"
                fontSize={8}
                fill="rgba(0,212,255,0.7)"
                fontFamily="JetBrains Mono, monospace"
              >
                {value}%
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
