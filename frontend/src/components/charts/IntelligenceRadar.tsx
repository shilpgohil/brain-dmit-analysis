"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { MultipleIntelligences } from "@/lib/types";
import { formatPercent } from "@/lib/utils";

interface IntelligenceRadarProps {
  data: MultipleIntelligences;
  height?: number;
}

const LABELS: Record<keyof MultipleIntelligences, string> = {
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

export function IntelligenceRadar({ data, height = 300 }: IntelligenceRadarProps) {
  const chartData = (Object.keys(LABELS) as (keyof MultipleIntelligences)[]).map((key) => ({
    subject: LABELS[key],
    value: Math.round((data[key] ?? 0) * 100),
    fullMark: 100,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={chartData} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="#1e293b" strokeDasharray="0" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "#64748b", fontSize: 10, fontFamily: "inherit" }}
          tickLine={false}
        />
        <Radar
          name="Intelligence"
          dataKey="value"
          stroke="#3b82f6"
          fill="#3b82f6"
          fillOpacity={0.15}
          strokeWidth={1.5}
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
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
