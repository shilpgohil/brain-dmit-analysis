"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import type { PipelineStage } from "@/lib/types";
import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";

interface PipelineTrackerProps {
  stages: PipelineStage[];
}

export function PipelineTracker({ stages }: PipelineTrackerProps) {
  return (
    <div className="space-y-0">
      {stages.map((stage, idx) => {
        const isLast = idx === stages.length - 1;
        const color = stage.status === "completed" ? "#10b981"
          : stage.status === "running" ? "#00d4ff"
          : stage.status === "failed" ? "#f43f5e"
          : "rgba(255,255,255,0.12)";

        return (
          <div key={stage.id} className="flex gap-3">
            <div className="flex flex-col items-center">
              <StageIcon status={stage.status} color={color} />
              {!isLast && (
                <motion.div
                  className="w-px flex-1 min-h-4 mt-1"
                  style={{ background: stage.status === "completed" ? "#10b98140" : "rgba(255,255,255,0.05)" }}
                />
              )}
            </div>

            <div className={cn("pb-4 flex-1 min-w-0", isLast && "pb-0")}>
              <div className="flex items-baseline justify-between">
                <span
                  className="text-xs font-medium"
                  style={{ color: stage.status === "pending" ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.7)" }}
                >
                  {stage.label}
                </span>
                {stage.duration_ms != null && (
                  <span className="text-[9px] text-white/20 font-mono ml-2">
                    {stage.duration_ms < 1000
                      ? `${stage.duration_ms.toFixed(0)}ms`
                      : `${(stage.duration_ms / 1000).toFixed(1)}s`}
                  </span>
                )}
              </div>
              {stage.detail && (
                <p className="text-[10px] text-white/20 mt-0.5">{stage.detail}</p>
              )}
              {stage.status === "running" && (
                <div className="mt-1.5 h-0.5 w-full rounded-full overflow-hidden"
                  style={{ background: "rgba(255,255,255,0.05)" }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: "linear-gradient(90deg, #00d4ff, #8b5cf6)" }}
                    animate={{ x: ["-100%", "200%"] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  />
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function StageIcon({ status, color }: { status: PipelineStage["status"]; color: string }) {
  if (status === "completed")
    return (
      <CheckCircle2
        className="w-3.5 h-3.5 flex-shrink-0 mt-0.5"
        style={{ color }}
      />
    );
  if (status === "running")
    return (
      <Loader2
        className="w-3.5 h-3.5 animate-spin flex-shrink-0 mt-0.5"
        style={{ color }}
      />
    );
  if (status === "failed")
    return (
      <XCircle
        className="w-3.5 h-3.5 flex-shrink-0 mt-0.5"
        style={{ color }}
      />
    );
  return (
    <Circle
      className="w-3.5 h-3.5 flex-shrink-0 mt-0.5"
      style={{ color: "rgba(255,255,255,0.1)" }}
    />
  );
}
