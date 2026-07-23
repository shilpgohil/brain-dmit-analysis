"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { GOLD } from "@/lib/analysis-theme";

interface GoldRadarChartProps {
  data: { label: string; value: number }[];
  height?: number;
}

export function GoldRadarChart({ data, height = 280 }: GoldRadarChartProps) {
  const chartData = data.map((d) => ({
    subject: d.label,
    value: Math.round(d.value * 100),
    fullMark: 100,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={chartData} margin={{ top: 16, right: 28, bottom: 16, left: 28 }}>
        <PolarGrid stroke="rgba(196,165,116,0.12)" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "rgba(232,220,200,0.55)", fontSize: 10, fontFamily: "inherit" }}
          tickLine={false}
        />
        <Radar
          name="Score"
          dataKey="value"
          stroke={GOLD.primary}
          fill={GOLD.primary}
          fillOpacity={0.22}
          strokeWidth={2}
        />
        <Tooltip
          contentStyle={{
            background: "rgba(8,8,20,0.95)",
            border: `1px solid ${GOLD.border}`,
            borderRadius: 12,
            fontSize: 12,
            color: GOLD.bright,
          }}
          formatter={(val) => [`${val}%`, "Capacity"]}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
