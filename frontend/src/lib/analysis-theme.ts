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

/**
 * Shared Recharts `<Tooltip>` props for every chart on the dark theme.
 *
 * Recharts' `DefaultTooltipContent` hardcodes `itemStyle.color: '#000'` and
 * only reads `contentStyle.color` for the wrapper div — never for the
 * item/label text itself — so every chart that set only `contentStyle`
 * rendered near-invisible black text on this dark background. Spreading
 * `chartTooltipStyle` fixes that everywhere at once.
 */
export const chartTooltipStyle = {
  contentStyle: {
    background: "rgba(8,8,20,0.95)",
    border: `1px solid ${GOLD.border}`,
    borderRadius: 8,
  },
  itemStyle: {
    color: GOLD.bright,
  },
  labelStyle: {
    color: "rgba(255,255,255,0.55)",
  },
} as const;

/**
 * Shared Recharts `<Tooltip cursor={...}>` prop. Recharts defaults the bar
 * hover/active "cursor" band to a flat `fill: '#ccc'` (light gray), which
 * on this dark UI reads as a jarring bright/white rectangle around the bar
 * being pointed at. A faint, colour-matched highlight looks intentional
 * instead.
 */
export const chartCursorStyle = {
  fill: "rgba(196, 165, 116, 0.08)",
  stroke: "none",
} as const;
