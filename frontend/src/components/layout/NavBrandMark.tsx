"use client";

import { motion } from "framer-motion";

/** Premium nav mark — ridge orbital glyph, not a flat Lucide icon */
export function NavBrandMark() {
  return (
    <motion.div
      className="relative w-9 h-9 rounded-lg overflow-hidden flex-shrink-0"
      style={{
        background: "linear-gradient(145deg, rgba(196,165,116,0.2), rgba(157,139,181,0.15))",
        border: "1px solid rgba(196,165,116,0.35)",
        boxShadow: "0 0 20px rgba(196,165,116,0.15), inset 0 1px 0 rgba(255,255,255,0.08)",
      }}
      whileHover={{ scale: 1.06 }}
      transition={{ type: "spring", stiffness: 400, damping: 22 }}
    >
      <svg className="absolute inset-0 w-full h-full p-1.5" viewBox="0 0 36 36" fill="none">
        <defs>
          <radialGradient id="navCore" cx="50%" cy="45%" r="50%">
            <stop offset="0%" stopColor="#e8dcc8" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#c4a574" stopOpacity="0.3" />
          </radialGradient>
        </defs>
        {[6, 10, 14, 18].map((r, i) => (
          <ellipse
            key={r}
            cx="18"
            cy="17"
            rx={r * 0.95}
            ry={r * 0.82}
            stroke="rgba(196,165,116,0.35)"
            strokeWidth="0.5"
            opacity={0.3 + i * 0.15}
          />
        ))}
        <circle cx="18" cy="15" r="2" fill="url(#navCore)" />
        <path
          d="M18 8 L20 12 L18 16 L16 12 Z"
          stroke="#c4a574"
          strokeWidth="0.6"
          fill="none"
          opacity="0.6"
        />
      </svg>
    </motion.div>
  );
}
