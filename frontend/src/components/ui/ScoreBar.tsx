"use client";
import { cn, formatPercent, scoreBg } from "@/lib/utils";

interface ScoreBarProps {
  label: string;
  value: number;
  sublabel?: string;
  showValue?: boolean;
  size?: "sm" | "md";
  className?: string;
}

export function ScoreBar({
  label,
  value,
  sublabel,
  showValue = true,
  size = "md",
  className,
}: ScoreBarProps) {
  const clamped = Math.min(Math.max(value, 0), 1);

  return (
    <div className={cn("space-y-1", className)}>
      <div className="flex items-baseline justify-between">
        <div>
          <span className={cn("font-medium text-slate-300", size === "sm" ? "text-xs" : "text-sm")}>
            {label}
          </span>
          {sublabel && (
            <span className="ml-1.5 text-[10px] text-slate-600 uppercase tracking-wide">{sublabel}</span>
          )}
        </div>
        {showValue && (
          <span className={cn("tabular-nums font-mono text-slate-400", size === "sm" ? "text-xs" : "text-sm")}>
            {formatPercent(clamped, 0)}
          </span>
        )}
      </div>
      <div className={cn("w-full bg-slate-800 rounded-full overflow-hidden", size === "sm" ? "h-1" : "h-1.5")}>
        <div
          className={cn("h-full rounded-full transition-all duration-700", scoreBg(clamped))}
          style={{ width: `${clamped * 100}%` }}
        />
      </div>
    </div>
  );
}

interface ScoreGridProps {
  items: { label: string; value: number; sublabel?: string }[];
  columns?: 1 | 2;
}

export function ScoreGrid({ items, columns = 1 }: ScoreGridProps) {
  return (
    <div className={cn("gap-3", columns === 2 ? "grid grid-cols-2" : "flex flex-col")}>
      {items.map((item) => (
        <ScoreBar key={item.label} {...item} size="sm" />
      ))}
    </div>
  );
}
