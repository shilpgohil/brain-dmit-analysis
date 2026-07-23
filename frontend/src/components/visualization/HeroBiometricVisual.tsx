"use client";

import { motion } from "framer-motion";
/**
 * Cinematic hero visual using real dermatoglyphic scan imagery
 * with laboratory-grade overlays — not generic procedural circles.
 */
export function HeroBiometricVisual() {
  return (
    <motion.div
      className="absolute inset-0 overflow-hidden pointer-events-none"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.4, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Real fingerprint scan — center, masked */}
      <motion.div
        className="absolute left-1/2 top-[42%] -translate-x-1/2 -translate-y-1/2 w-[min(92vw,720px)] aspect-square"
        animate={{ scale: [1, 1.02, 1] }}
        transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
      >
        <motion.div
          className="relative w-full h-full"
          animate={{ rotate: [0, 1.5, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/images/hero-fingerprint.bmp"
            alt=""
            className="w-full h-full object-cover opacity-[0.22] mix-blend-screen"
            style={{
              filter: "contrast(1.35) brightness(0.85) grayscale(100%)",
              maskImage: "radial-gradient(ellipse 70% 70% at 50% 50%, black 20%, transparent 72%)",
              WebkitMaskImage: "radial-gradient(ellipse 70% 70% at 50% 50%, black 20%, transparent 72%)",
            }}
          />
        </motion.div>
      </motion.div>

      {/* Chromatic aberration fringe */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          background:
            "radial-gradient(ellipse 55% 45% at 50% 42%, rgba(0,212,255,0.12) 0%, transparent 55%), radial-gradient(ellipse 40% 35% at 48% 44%, rgba(139,92,246,0.08) 0%, transparent 50%)",
        }}
      />

      {/* Scan beam */}
      <motion.div
        className="absolute left-0 right-0 h-[2px] pointer-events-none"
        style={{
          background: "linear-gradient(90deg, transparent, rgba(0,212,255,0.7), rgba(255,255,255,0.9), rgba(0,212,255,0.7), transparent)",
          boxShadow: "0 0 24px rgba(0,212,255,0.5), 0 0 60px rgba(0,212,255,0.2)",
        }}
        animate={{ top: ["18%", "78%", "18%"] }}
        transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Crosshair / measurement reticle */}
      <svg
        className="absolute left-1/2 top-[42%] -translate-x-1/2 -translate-y-1/2 w-[min(85vw,640px)] h-[min(85vw,640px)] opacity-[0.15]"
        viewBox="0 0 400 400"
        fill="none"
      >
        <circle cx="200" cy="200" r="160" stroke="rgba(0,212,255,0.5)" strokeWidth="0.5" strokeDasharray="4 8" />
        <circle cx="200" cy="200" r="120" stroke="rgba(255,255,255,0.2)" strokeWidth="0.5" />
        <line x1="200" y1="20" x2="200" y2="80" stroke="rgba(0,212,255,0.4)" strokeWidth="0.5" />
        <line x1="200" y1="320" x2="200" y2="380" stroke="rgba(0,212,255,0.4)" strokeWidth="0.5" />
        <line x1="20" y1="200" x2="80" y2="200" stroke="rgba(0,212,255,0.4)" strokeWidth="0.5" />
        <line x1="320" y1="200" x2="380" y2="200" stroke="rgba(0,212,255,0.4)" strokeWidth="0.5" />
        {/* Core marker */}
        <circle cx="200" cy="185" r="4" fill="rgba(0,212,255,0.6)" />
        <circle cx="200" cy="185" r="8" stroke="rgba(0,212,255,0.3)" strokeWidth="0.5" />
      </svg>

      {/* Bottom vignette for text legibility */}
      <motion.div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 50%, transparent 0%, rgba(2,2,8,0.4) 55%, rgba(2,2,8,0.92) 100%)",
        }}
      />
    </motion.div>
  );
}
