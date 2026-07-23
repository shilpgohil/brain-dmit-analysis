/** Premium champagne / gold palette for analysis results */
export const GOLD = {
  primary: "#c4a574",
  bright: "#e8dcc8",
  dim: "rgba(196, 165, 116, 0.14)",
  border: "rgba(196, 165, 116, 0.28)",
  glow: "rgba(196, 165, 116, 0.35)",
  gradient: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 45%, #9a7b4f 100%)",
  bar: "linear-gradient(90deg, #9a7b4f, #c4a574, #e8dcc8)",
} as const;

export const PLUM = "#9d8bb5";
export const SAGE = "#6b9e8f";

export function scoreToGoldTier(value: number): { color: string; label: string } {
  if (value >= 0.75) return { color: GOLD.bright, label: "Dominant" };
  if (value >= 0.55) return { color: GOLD.primary, label: "Strong" };
  if (value >= 0.35) return { color: "#b87d5c", label: "Moderate" };
  return { color: "rgba(238,242,255,0.35)", label: "Emerging" };
}
