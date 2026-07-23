"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { DMIT_GLOSSARY, FINGER_ENCYCLOPEDIA } from "@/lib/dmit-glossary";
import { GlassCard } from "@/components/ui/GlassCard";
import { FingerprintField } from "@/components/effects/FingerprintField";

export default function LearnPage() {
  const [activeFinger, setActiveFinger] = useState<string | null>(null);
  const finger = FINGER_ENCYCLOPEDIA.find((f) => f.id === activeFinger);

  return (
    <motion.div className="min-h-screen pb-24" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <section className="relative py-16 px-6">
        <div className="absolute inset-0 opacity-25">
          <FingerprintField opacity={0.06} animated={false} color="196, 165, 116" />
        </div>
        <motion.div className="relative z-10 max-w-3xl mx-auto text-center mb-12">
          <p className="text-[10px] tracking-[0.3em] uppercase font-mono text-accent-gold mb-3">DMIT Academy</p>
          <h1 className="text-display-section text-white">Learn the language of ridges.</h1>
          <p className="text-white/40 mt-3 font-light">Glossary terms and finger encyclopedia — tap any finger for detail.</p>
        </motion.div>

        <div className="relative z-10 max-w-4xl mx-auto space-y-12">
          <div>
            <h2 className="font-editorial text-2xl text-white mb-4">Glossary</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {DMIT_GLOSSARY.map((term, i) => (
                <motion.div
                  key={term.term}
                  initial={{ opacity: 0, y: 8 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.03 }}
                >
                  <GlassCard padding="md" className="h-full">
                    <p className="font-editorial text-lg text-accent-gold">{term.term}</p>
                    <p className="text-[10px] font-mono text-white/35 mb-2">{term.short}</p>
                    <p className="text-[11px] text-white/55 font-light leading-relaxed">{term.detail}</p>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="font-editorial text-2xl text-white mb-4">Finger encyclopedia</h2>
            <div className="grid grid-cols-5 sm:grid-cols-10 gap-2 mb-4">
              {FINGER_ENCYCLOPEDIA.map((f) => (
                <button
                  key={f.id}
                  type="button"
                  onClick={() => setActiveFinger(f.id === activeFinger ? null : f.id)}
                  className="aspect-square rounded-lg text-[10px] font-mono transition-all"
                  style={{
                    background: activeFinger === f.id ? "rgba(196,165,116,0.15)" : "rgba(255,255,255,0.03)",
                    border: `1px solid ${activeFinger === f.id ? "rgba(196,165,116,0.4)" : "rgba(255,255,255,0.08)"}`,
                    color: activeFinger === f.id ? "#e8dcc8" : "rgba(255,255,255,0.5)",
                  }}
                >
                  {f.id}
                </button>
              ))}
            </div>
            {finger && (
              <GlassCard padding="lg">
                <p className="text-[10px] font-mono text-accent-gold uppercase tracking-widest mb-1">
                  {finger.hand} hand · {finger.lobe}
                </p>
                <h3 className="font-editorial text-2xl text-white mb-2">{finger.name}</h3>
                <p className="text-xs text-white/40 mb-3">Intelligences: {finger.intelligences.join(", ")}</p>
                <p className="text-sm text-white/55 font-light leading-relaxed">{finger.narrative}</p>
              </GlassCard>
            )}
          </div>
        </div>
      </section>
    </motion.div>
  );
}
