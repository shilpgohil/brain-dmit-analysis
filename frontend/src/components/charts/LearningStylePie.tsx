"use client";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import type { LearningStyles } from "@/lib/types";

interface LearningStylePieProps {
  data: LearningStyles;
  height?: number;
}

const COLORS = ["#3b82f6", "#10b981", "#f59e0b"];
const LABELS = ["Visual", "Auditory", "Kinesthetic"];

export function LearningStylePie({ data, height = 200 }: LearningStylePieProps) {
  const visual = data.visual ?? 0;
  const auditory = data.auditory ?? 0;
  const kinesthetic = data.kinesthetic ?? 0;
  const total = visual + auditory + kinesthetic || 1;
  const chartData = [
    { name: "Visual", value: Math.round((visual / total) * 100) },
    { name: "Auditory", value: Math.round((auditory / total) * 100) },
    { name: "Kinesthetic", value: Math.round((kinesthetic / total) * 100) },
  ];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          innerRadius={50}
          outerRadius={75}
          paddingAngle={3}
          dataKey="value"
          strokeWidth={0}
        >
          {chartData.map((_, idx) => (
            <Cell key={idx} fill={COLORS[idx]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "#0f172a",
            border: "1px solid #1e293b",
            borderRadius: "6px",
            fontSize: "12px",
            color: "#cbd5e1",
          }}
          formatter={(val) => [`${val}%`]}
        />
        <Legend
          iconType="circle"
          iconSize={7}
          wrapperStyle={{ fontSize: "11px", color: "#64748b" }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
