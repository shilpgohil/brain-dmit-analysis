"use client";

import { motion } from "framer-motion";
import type { PalmGuidanceInfo } from "@/lib/finger-guidance";

/**
 * Open-palm line-art SVG.
 * Shows the three ATD triradius landmark positions (a, t, d) with
 * pulsing halos so the user understands what to keep visible.
 */
export function PalmHandSvg({
  info,
  className = "",
}: {
  info: PalmGuidanceInfo;
  className?: string;
}) {
  const isLeft = info.hand === "left";

  return (
    <svg
      viewBox="0 0 200 230"
      className={className}
      aria-hidden
      style={{ transform: isLeft ? "scaleX(-1)" : undefined }}
    >
      {/* Palm body */}
      <path
        d="M45 105 Q40 65 55 40 Q70 18 95 18 Q120 18 135 40 Q150 65 145 105
           Q148 155 130 185 Q115 205 95 208 Q75 205 60 185 Z"
        fill="rgba(196,165,116,0.08)"
        stroke="rgba(196,165,116,0.35)"
        strokeWidth="1.5"
      />

      {/* Wrist / base lines */}
      <path
        d="M60 190 Q70 215 95 218 Q120 215 130 190"
        fill="none"
        stroke="rgba(196,165,116,0.2)"
        strokeWidth="1"
      />

      {/* Finger outlines — all five */}
      {/* Thumb */}
      <path
        d="M38 100 Q22 88 26 65 Q30 48 45 54 Q56 66 50 90"
        fill="rgba(196,165,116,0.10)"
        stroke="rgba(196,165,116,0.30)"
        strokeWidth="1.2"
      />
      {/* Index */}
      <rect x="60" y="14" width="20" height="64" rx="10"
        fill="rgba(196,165,116,0.10)" stroke="rgba(196,165,116,0.28)" strokeWidth="1.2" />
      {/* Middle */}
      <rect x="82" y="8" width="21" height="70" rx="10.5"
        fill="rgba(196,165,116,0.10)" stroke="rgba(196,165,116,0.28)" strokeWidth="1.2" />
      {/* Ring */}
      <rect x="105" y="14" width="20" height="65" rx="10"
        fill="rgba(196,165,116,0.10)" stroke="rgba(196,165,116,0.28)" strokeWidth="1.2" />
      {/* Little */}
      <rect x="127" y="28" width="16" height="52" rx="8"
        fill="rgba(196,165,116,0.10)" stroke="rgba(196,165,116,0.28)" strokeWidth="1.2" />

      {/* Major palm creases */}
      <path d="M50 95 Q80 80 140 100" fill="none" stroke="rgba(196,165,116,0.18)" strokeWidth="0.8" />
      <path d="M48 120 Q85 108 142 118" fill="none" stroke="rgba(196,165,116,0.18)" strokeWidth="0.8" />

      {/* ── ATD triradius points ─────────────────────────── */}
      {/* a-point — below index finger (left side when right hand) */}
      <motion.circle cx="72" cy="100" r="5"
        fill="none" stroke="#00d4ff" strokeWidth="1.5"
        animate={{ scale: [1, 1.4, 1], opacity: [0.7, 1, 0.7] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0 }}
      />
      <text x="58" y="96" fontSize="8" fill="#00d4ff" fontFamily="monospace">a</text>

      {/* t-point — center palm */}
      <motion.circle cx="96" cy="140" r="5"
        fill="none" stroke="#c4a574" strokeWidth="1.5"
        animate={{ scale: [1, 1.4, 1], opacity: [0.7, 1, 0.7] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
      />
      <text x="101" y="136" fontSize="8" fill="#c4a574" fontFamily="monospace">t</text>

      {/* d-point — below little finger (right side when right hand) */}
      <motion.circle cx="128" cy="100" r="5"
        fill="none" stroke="#9d8bb5" strokeWidth="1.5"
        animate={{ scale: [1, 1.4, 1], opacity: [0.7, 1, 0.7] }}
        transition={{ duration: 2, repeat: Infinity, delay: 1 }}
      />
      <text x="134" y="96" fontSize="8" fill="#9d8bb5" fontFamily="monospace">d</text>

      {/* Angle lines connecting a–t–d */}
      <line x1="72" y1="100" x2="96" y2="140"
        stroke="rgba(196,165,116,0.30)" strokeWidth="0.8" strokeDasharray="3 2" />
      <line x1="128" y1="100" x2="96" y2="140"
        stroke="rgba(196,165,116,0.30)" strokeWidth="0.8" strokeDasharray="3 2" />
    </svg>
  );
}
