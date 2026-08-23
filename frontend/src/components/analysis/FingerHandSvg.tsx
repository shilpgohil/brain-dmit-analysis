"use client";

import { motion } from "framer-motion";
import type { FingerGuidanceInfo } from "@/lib/finger-guidance";

/** Simple line-art hand with one finger highlighted (gold theme). */
export function FingerHandSvg({
  info,
  className = "",
}: {
  info: FingerGuidanceInfo;
  className?: string;
}) {
  const isLeft = info.hand === "left";
  const highlight = info.fingerKey;

  const fingerOpacity = (key: string) => (key === highlight ? 1 : 0.22);

  return (
    <svg
      viewBox="0 0 200 220"
      className={className}
      aria-hidden
      style={{ transform: isLeft ? "scaleX(-1)" : undefined }}
    >
      {/* Palm */}
      <path
        d="M55 95 Q55 55 95 50 Q130 48 145 75 L155 130 Q158 175 120 190 Q85 200 60 175 Z"
        fill="rgba(196,165,116,0.08)"
        stroke="rgba(196,165,116,0.35)"
        strokeWidth="1.5"
      />
      {/* Wrist */}
      <path
        d="M70 175 Q75 205 100 210 Q125 205 130 175"
        fill="none"
        stroke="rgba(196,165,116,0.25)"
        strokeWidth="1.2"
      />
      {/* Thumb */}
      <motion.path
        d="M48 88 Q25 70 30 45 Q35 25 55 35 Q65 50 58 75"
        fill="rgba(196,165,116,0.15)"
        stroke="#c4a574"
        strokeWidth={highlight === "thumb" ? 2.5 : 1.2}
        animate={{ opacity: fingerOpacity("thumb") }}
        transition={{ duration: 0.4 }}
      />
      {/* Index */}
      <motion.rect
        x="78"
        y="18"
        width="22"
        height="72"
        rx="11"
        fill="rgba(196,165,116,0.15)"
        stroke="#c4a574"
        strokeWidth={highlight === "index" ? 2.5 : 1.2}
        animate={{ opacity: fingerOpacity("index") }}
      />
      {/* Middle */}
      <motion.rect
        x="98"
        y="12"
        width="22"
        height="78"
        rx="11"
        fill="rgba(196,165,116,0.15)"
        stroke="#c4a574"
        strokeWidth={highlight === "middle" ? 2.5 : 1.2}
        animate={{ opacity: fingerOpacity("middle") }}
      />
      {/* Ring */}
      <motion.rect
        x="122"
        y="18"
        width="20"
        height="72"
        rx="10"
        fill="rgba(196,165,116,0.15)"
        stroke="#c4a574"
        strokeWidth={highlight === "ring" ? 2.5 : 1.2}
        animate={{ opacity: fingerOpacity("ring") }}
      />
      {/* Little */}
      <motion.rect
        x="142"
        y="32"
        width="16"
        height="58"
        rx="8"
        fill="rgba(196,165,116,0.15)"
        stroke="#c4a574"
        strokeWidth={highlight === "little" ? 2.5 : 1.2}
        animate={{ opacity: fingerOpacity("little") }}
      />
      {highlight === "thumb" && (
        <motion.circle
          cx="42"
          cy="52"
          r="6"
          fill="none"
          stroke="#e8dcc8"
          strokeWidth="1"
          animate={{ scale: [1, 1.15, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.8, repeat: Infinity }}
        />
      )}
    </svg>
  );
}
