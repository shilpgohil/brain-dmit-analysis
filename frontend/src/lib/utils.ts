import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercent(value: number, decimals = 1): string {
  return `${(value * 100).toFixed(decimals)}%`;
}

export function isMeasured(value: number | null | undefined): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

export function pct(value: number | null | undefined): string {
  return isMeasured(value) ? `${Math.round(value * 100)}%` : "N/A";
}

export function measuredEntries(
  scores: object | null | undefined,
): [string, number][] {
  if (!scores) return [];
  return Object.entries(scores).filter(
    (entry): entry is [string, number] => isMeasured(entry[1]),
  );
}

export function formatRidgeCount(
  ridge: number | null | undefined,
  pattern?: string,
): string {
  if (!isMeasured(ridge)) return "—";
  if (ridge === 0 && pattern === "arch") return "0 (arch)";
  return String(Math.round(ridge));
}

export function formatScore(value: number): string {
  return (value * 100).toFixed(0);
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function scoreColor(value: number): string {
  if (value >= 0.75) return "text-emerald-400";
  if (value >= 0.5) return "text-blue-400";
  if (value >= 0.25) return "text-amber-400";
  return "text-red-400";
}

export function scoreBg(value: number): string {
  if (value >= 0.75) return "bg-emerald-500";
  if (value >= 0.5) return "bg-blue-500";
  if (value >= 0.25) return "bg-amber-500";
  return "bg-red-500";
}

export function patternLabel(type: string): string {
  const map: Record<string, string> = {
    whorl: "Whorl",
    loop: "Loop",
    arch: "Arch",
    accidental: "Accidental",
    unknown: "Unknown",
  };
  return map[type?.toLowerCase()] ?? type ?? "—";
}

/** Stable key for finger detail routes (L1–R5 preferred). */
export function fingerRouteKey(finger: { finger_position?: string; finger_type: string }): string {
  return finger.finger_position ?? finger.finger_type;
}

export function fingerLabel(id: string): string {
  const map: Record<string, string> = {
    R1: "Right Thumb",
    R2: "Right Index",
    R3: "Right Middle",
    R4: "Right Ring",
    R5: "Right Little",
    L1: "Left Thumb",
    L2: "Left Index",
    L3: "Left Middle",
    L4: "Left Ring",
    L5: "Left Little",
    thumb: "Thumb",
    index: "Index",
    middle: "Middle",
    ring: "Ring",
    little: "Little",
    unknown: "Unknown",
  };
  return map[id] ?? id ?? "—";
}

export function lobeLabel(key: string): string {
  const map: Record<string, string> = {
    prefrontal_lobe: "Prefrontal",
    posterior_frontal: "Frontal",
    parietal_lobe: "Parietal",
    temporal_lobe: "Temporal",
    occipital_lobe: "Occipital",
    left_hemisphere: "Left Hemisphere",
    right_hemisphere: "Right Hemisphere",
  };
  return map[key] ?? key;
}

export function lobeDescription(key: string): string {
  const map: Record<string, string> = {
    prefrontal_lobe: "Executive function, personality, interpersonal skill",
    posterior_frontal: "Logic, language production, reasoning",
    parietal_lobe: "Somatosensory, bodily-kinesthetic integration",
    temporal_lobe: "Auditory processing, memory, musical ability",
    occipital_lobe: "Visual processing, spatial perception",
    left_hemisphere: "Analytical, sequential, linguistic processing",
    right_hemisphere: "Creative, holistic, intuitive processing",
  };
  return map[key] ?? "";
}

export function relativeTime(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  const mins = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (mins < 1) return "Just now";
  if (mins < 60) return `${mins}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}
