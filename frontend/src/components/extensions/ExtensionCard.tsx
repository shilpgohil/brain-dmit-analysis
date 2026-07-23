"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { ExtensionMeta } from "@/lib/extensions-catalog";

export function ExtensionCard({ ext, index }: { ext: ExtensionMeta; index: number }) {
  const [open, setOpen] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: (index % 12) * 0.03 }}
      className="relative"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onClick={() => setOpen((v) => !v)}
    >
      <div
        className="rounded-xl p-4 cursor-pointer h-full min-h-[100px] transition-all duration-200"
        style={{
          background: open ? `${ext.accent}12` : "rgba(255,255,255,0.03)",
          border: `1px solid ${open ? `${ext.accent}45` : "rgba(255,255,255,0.07)"}`,
        }}
      >
        <p className="text-[9px] font-mono uppercase tracking-wider mb-1" style={{ color: ext.accent }}>
          {ext.category}
        </p>
        <p className="font-editorial text-base text-white/90 leading-tight">{ext.name}</p>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="absolute z-50 left-0 right-0 mt-2 rounded-xl p-4 pointer-events-none"
            style={{
              background: "rgba(8,8,20,0.92)",
              backdropFilter: "blur(20px)",
              border: `1px solid ${ext.accent}40`,
            }}
          >
            <p className="text-[11px] text-white/65 leading-relaxed font-light mb-2">{ext.description}</p>
            <p className="text-[9px] font-mono text-white/35">
              <span className="text-white/50">Inputs: </span>
              {ext.inputs}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
