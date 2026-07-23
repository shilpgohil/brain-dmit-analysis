import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "error" | "neutral" | "blue";
  size?: "sm" | "md";
  className?: string;
}

export function Badge({ children, variant = "default", size = "sm", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center font-medium tracking-wide uppercase",
        size === "sm" ? "text-[10px] px-2 py-0.5 rounded" : "text-xs px-2.5 py-1 rounded-md",
        variant === "default" && "bg-slate-800 text-slate-300 border border-slate-700",
        variant === "success" && "bg-emerald-950 text-emerald-400 border border-emerald-800",
        variant === "warning" && "bg-amber-950 text-amber-400 border border-amber-800",
        variant === "error" && "bg-red-950 text-red-400 border border-red-800",
        variant === "neutral" && "bg-slate-900 text-slate-400 border border-slate-800",
        variant === "blue" && "bg-blue-950 text-blue-400 border border-blue-800",
        className
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({ status }: { status: string }) {
  const map: Record<string, { label: string; variant: BadgeProps["variant"] }> = {
    pending: { label: "Pending", variant: "neutral" },
    preprocessing: { label: "Preprocessing", variant: "blue" },
    extracting: { label: "Extracting", variant: "blue" },
    mapping: { label: "Mapping", variant: "blue" },
    extending: { label: "Analyzing", variant: "blue" },
    generating_report: { label: "Generating Report", variant: "blue" },
    completed: { label: "Completed", variant: "success" },
    failed: { label: "Failed", variant: "error" },
  };
  const cfg = map[status] ?? { label: status, variant: "neutral" as const };
  return <Badge variant={cfg.variant}>{cfg.label}</Badge>;
}
