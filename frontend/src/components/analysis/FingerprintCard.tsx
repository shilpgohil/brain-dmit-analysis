"use client";

import { cn, patternLabel, fingerLabel, fingerRouteKey, formatPercent, formatRidgeCount } from "@/lib/utils";
import { mediaUrl } from "@/lib/api";
import type { FingerBiometrics } from "@/lib/types";
import { Fingerprint } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import Link from "next/link";

interface FingerprintCardProps {
  finger: FingerBiometrics;
  sessionId: string;
  index: number;
  className?: string;
}

const PATTERN_COLORS: Record<string, string> = {
  whorl: "text-indigo-400",
  loop: "text-blue-400",
  arch: "text-amber-400",
  accidental: "text-purple-400",
  unknown: "text-slate-500",
};

const QUALITY_BADGE: Record<string, "success" | "blue" | "warning" | "neutral"> = {
  comprehensive: "success",
  advanced: "blue",
  core: "warning",
  basic: "neutral",
};

export function FingerprintCard({ finger, sessionId, index, className }: FingerprintCardProps) {
  const patternColor = PATTERN_COLORS[finger.pattern_type] ?? "text-slate-400";
  const qualityVariant = QUALITY_BADGE[finger.quality_tier ?? ""] ?? "neutral";

  return (
    <Link
      href={`/analysis/${sessionId}/finger/${encodeURIComponent(fingerRouteKey(finger))}`}
      className={cn(
        "block border border-slate-800 rounded-lg bg-slate-900 hover:border-slate-700 hover:bg-slate-900/80 transition-colors group",
        className
      )}
    >
      {/* Image / preview */}
      <div className="rounded-t-lg overflow-hidden bg-slate-950 border-b border-slate-800 h-24 flex items-center justify-center">
        {mediaUrl(finger.thumbnail_url) ? (
          <img
            src={mediaUrl(finger.thumbnail_url)}
            alt={fingerLabel(fingerRouteKey(finger))}
            className="w-full h-full object-cover filter grayscale"
          />
        ) : (
          <Fingerprint className="w-8 h-8 text-slate-700" strokeWidth={1} />
        )}
      </div>

      {/* Data */}
      <div className="p-3 space-y-2">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-300">
              {fingerLabel(finger.finger_type)}
            </p>
            <p className={cn("text-[11px] font-medium mt-0.5", patternColor)}>
              {patternLabel(finger.pattern_type)}
            </p>
          </div>
          {finger.quality_tier && (
            <Badge variant={qualityVariant} size="sm">
              {finger.quality_tier}
            </Badge>
          )}
        </div>

        <div className="grid grid-cols-2 gap-x-3 gap-y-1">
          <Stat label="Ridge Count" value={formatRidgeCount(finger.ridge_count, finger.pattern_type)} />
          <Stat
            label="Fractal Dim."
            value={finger.fractal_dimension?.toFixed(3) ?? "—"}
          />
          <Stat label="Minutiae" value={finger.minutiae_count?.toString() ?? "—"} />
          <Stat
            label="Entropy"
            value={finger.entropy?.toFixed(2) ?? "—"}
          />
        </div>
      </div>
    </Link>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[9px] text-slate-600 uppercase tracking-widest">{label}</p>
      <p className="text-[11px] text-slate-300 font-mono font-medium">{value}</p>
    </div>
  );
}
