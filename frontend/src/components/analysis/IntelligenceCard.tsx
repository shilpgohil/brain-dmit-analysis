"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { IntelligenceProfile } from "@/lib/dmit-knowledge";

interface IntelligenceCardProps {
  profile: IntelligenceProfile;
  index: number;
}

export function IntelligenceCard({ profile, index }: IntelligenceCardProps) {
  const [open, setOpen] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);
  const isTouchRef = useRef(false);

  useEffect(() => {
    const onPointerDown = () => {
      isTouchRef.current = true;
    };
    window.addEventListener("pointerdown", onPointerDown, { once: true });
    return () => window.removeEventListener("pointerdown", onPointerDown);
  }, []);

  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent) => {
      if (cardRef.current && !cardRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [open]);

  return (
    <motion.div
      ref={cardRef}
      initial={{ opacity: 0, scale: 0.92 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.05, ease: [0.16, 1, 0.3, 1] }}
      className="relative"
      onMouseEnter={() => !isTouchRef.current && setOpen(true)}
      onMouseLeave={() => !isTouchRef.current && setOpen(false)}
      onClick={() => isTouchRef.current && setOpen((v) => !v)}
    >
      <motion.div
        className="aspect-square rounded-xl flex flex-col items-center justify-center gap-1.5 p-2 text-center cursor-pointer transition-all duration-300"
        style={{
          background: open
            ? `linear-gradient(145deg, ${profile.accent}18, rgba(255,255,255,0.04))`
            : "rgba(255,255,255,0.03)",
          border: `1px solid ${open ? `${profile.accent}55` : "rgba(255,255,255,0.08)"}`,
          boxShadow: open ? `0 8px 32px ${profile.accent}22` : "none",
        }}
        whileHover={{ scale: 1.05, y: -2 }}
        whileTap={{ scale: 0.98 }}
      >
        {/* Mini ridge glyph */}
        <svg className="w-6 h-6 opacity-60 mb-0.5" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 4 C8 8 6 12 8 16 C10 18 14 18 16 16 C18 12 16 8 12 4"
            stroke={profile.accent}
            strokeWidth="0.8"
            opacity="0.7"
          />
          <ellipse cx="12" cy="11" rx="5" ry="4" stroke={profile.accent} strokeWidth="0.5" opacity="0.4" />
        </svg>
        <p className="font-editorial text-[11px] text-white/90 leading-tight">{profile.key}</p>
        <p className="text-[7px] text-white/35 font-mono uppercase tracking-wider">{profile.finger}</p>
      </motion.div>

      <AnimatePresence>
        {open && (
          <motion.div
            role="tooltip"
            initial={{ opacity: 0, y: 6, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 4, scale: 0.98 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="absolute z-[100] left-1/2 -translate-x-1/2 w-[min(92vw,280px)] sm:w-[300px] pointer-events-none"
            style={{
              bottom: "calc(100% + 10px)",
            }}
          >
            <motion.div
              className="rounded-xl p-4 text-left"
              style={{
                background: "rgba(8, 8, 20, 0.88)",
                backdropFilter: "blur(24px)",
                WebkitBackdropFilter: "blur(24px)",
                border: `1px solid ${profile.accent}40`,
                boxShadow: `0 16px 48px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04) inset`,
              }}
            >
              <motion.div className="flex items-start justify-between gap-2 mb-2" layout={false}>
                <div>
                  <p className="font-editorial text-lg text-white leading-tight">{profile.key}</p>
                  <p className="text-[9px] font-mono uppercase tracking-widest mt-0.5" style={{ color: profile.accent }}>
                    {profile.shortLabel}
                  </p>
                </div>
                <span
                  className="text-[8px] font-mono px-1.5 py-0.5 rounded shrink-0"
                  style={{ background: `${profile.accent}20`, color: profile.accent }}
                >
                  {profile.lobe}
                </span>
              </motion.div>
              <p className="text-[10px] font-mono text-white/40 mb-2">{profile.fingers}</p>
              <p className="text-[11px] text-white/65 leading-relaxed font-light">{profile.description}</p>
            </motion.div>
            <div
              className="absolute left-1/2 -translate-x-1/2 -bottom-1.5 w-3 h-3 rotate-45"
              style={{
                background: "rgba(8, 8, 20, 0.88)",
                borderRight: `1px solid ${profile.accent}40`,
                borderBottom: `1px solid ${profile.accent}40`,
              }}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
