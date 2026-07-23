"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { BrainLobeCapacity } from "@/lib/types";
import { lobeLabel } from "@/lib/utils";

interface BrainLobeChartProps {
  data: BrainLobeCapacity;
  height?: number;
}

const LOBE_KEYS: (keyof BrainLobeCapacity)[] = [
  "prefrontal_lobe",
  "posterior_frontal",
  "parietal_lobe",
  "temporal_lobe",
  "occipital_lobe",
];

const FINGER_MAP: Record<string, string> = {
  prefrontal_lobe: "Thumb",
  posterior_frontal: "Index",
  parietal_lobe: "Middle",
  temporal_lobe: "Ring",
  occipital_lobe: "Little",
};

function getBarColor(value: number): string {
  if (value >= 0.75) return "#10b981";
  if (value >= 0.5) return "#3b82f6";
  if (value >= 0.25) return "#f59e0b";
  return "#ef4444";
}

export function BrainLobeChart({ data, height = 220 }: BrainLobeChartProps) {
  const chartData = LOBE_KEYS.map((key) => {
    const raw = data[key];
    const measured = typeof raw === "number" && Number.isFinite(raw);
    return {
      name: lobeLabel(key),
      value: measured ? Math.round(raw * 100) : 0,
      finger: FINGER_MAP[key],
      raw: measured ? raw : 0,
    };
  });

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={chartData} margin={{ top: 5, right: 5, bottom: 5, left: -10 }}>
        <XAxis
          dataKey="name"
          tick={{ fill: "#475569", fontSize: 10, fontFamily: "inherit" }}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          domain={[0, 100]}
          tick={{ fill: "#334155", fontSize: 10, fontFamily: "inherit" }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(v) => `${v}%`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "#0f172a",
            border: "1px solid #1e293b",
            borderRadius: "6px",
            fontSize: "12px",
            color: "#cbd5e1",
          }}
          formatter={(val) => [`${val}%`, "Score"]}
          cursor={{ fill: "rgba(255,255,255,0.03)" }}
        />
        <Bar dataKey="value" radius={[3, 3, 0, 0]} maxBarSize={36}>
          {chartData.map((entry, idx) => (
            <Cell key={idx} fill={getBarColor(entry.raw)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
