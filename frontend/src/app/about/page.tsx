"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { IntelligenceCard } from "@/components/analysis/IntelligenceCard";
import {
  DMIT_FIELD_SECTIONS,
  PLATFORM_SECTIONS,
  INTELLIGENCE_PROFILES,
} from "@/lib/dmit-knowledge";
import { ArrowRight, BookOpen, Cpu, Fingerprint, Brain } from "lucide-react";

const FINGER_LOBE_TABLE = [
  { finger: "Thumb (L1 / R1)", lobe: "Prefrontal", role: "Executive function, self & social awareness" },
  { finger: "Index (L2 / R2)", lobe: "Frontal", role: "Logic, language reasoning, existential thought" },
  { finger: "Middle (L3 / R3)", lobe: "Parietal", role: "Kinesthetic coordination, spatial body sense" },
  { finger: "Ring (L4 / R4)", lobe: "Temporal", role: "Auditory processing, music, verbal memory" },
  { finger: "Little (L5 / R5)", lobe: "Occipital", role: "Visual-spatial observation, natural patterns" },
];

export default function AboutPage() {
  return (
    <motion.div
      className="min-h-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Hero */}
      <section className="relative py-24 px-6 overflow-hidden">
        <div className="absolute inset-0 opacity-40">
          <FingerprintField opacity={0.1} animated color="196, 165, 116" />
        </div>
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <p className="text-[10px] tracking-[0.3em] uppercase font-mono text-accent-gold mb-4">
            Knowledge Base
          </p>
          <h1 className="text-display-section text-white mb-4">
            The science & story of{" "}
            <span className="text-emphasis-italic gradient-text-premium">DMIT.</span>
          </h1>
          <p className="text-white/45 text-lg font-light leading-relaxed max-w-2xl mx-auto">
            Everything this platform measures, how dermatoglyphics connects to the brain,
            and how our biometric pipeline turns ten fingerprints into a full intelligence profile.
          </p>
        </div>
      </section>

      {/* DMIT Field */}
      <section className="py-16 px-6 border-t border-white/[0.05]">
        <motion.div className="max-w-4xl mx-auto">
          <SectionHeader icon={<BookOpen className="w-4 h-4" />} label="The Field" title="Understanding DMIT" />
          <div className="space-y-6 mt-10">
            {DMIT_FIELD_SECTIONS.map((s, i) => (
              <motion.div
                key={s.id}
                id={s.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ delay: i * 0.08, duration: 0.6 }}
              >
                <GlassCard padding="lg">
                  <h3 className="font-editorial text-2xl text-white mb-3">{s.title}</h3>
                  <p className="text-sm text-white/55 leading-relaxed font-light">{s.body}</p>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Finger–Lobe Table */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <SectionHeader icon={<Brain className="w-4 h-4" />} label="CADA Standard" title="Finger–brain mapping" />
          <GlassCard padding="lg" className="mt-8 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-white/[0.08]">
                  <th className="py-3 pr-4 font-mono text-[10px] uppercase tracking-widest text-accent-gold">Finger</th>
                  <th className="py-3 pr-4 font-mono text-[10px] uppercase tracking-widest text-accent-gold">Lobe</th>
                  <th className="py-3 font-mono text-[10px] uppercase tracking-widest text-accent-gold">Function</th>
                </tr>
              </thead>
              <tbody>
                {FINGER_LOBE_TABLE.map((row) => (
                  <tr key={row.finger} className="border-b border-white/[0.04] last:border-0">
                    <td className="py-3 pr-4 text-white/80 font-medium">{row.finger}</td>
                    <td className="py-3 pr-4 text-white/50">{row.lobe}</td>
                    <td className="py-3 text-white/40 font-light">{row.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </GlassCard>
        </div>
      </section>

      {/* Nine Intelligences — interactive */}
      <section className="py-16 px-6 border-t border-white/[0.05]">
        <div className="max-w-5xl mx-auto">
          <SectionHeader
            icon={<Fingerprint className="w-4 h-4" />}
            label="Gardner MI"
            title="Nine intelligences explained"
          />
          <p className="text-white/40 text-sm mt-4 mb-8 max-w-xl font-light">
            Hover or tap each card for a full DMIT interpretation — finger correlation, brain lobe, and practical meaning.
          </p>
          <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2">
            {INTELLIGENCE_PROFILES.map((p, i) => (
              <IntelligenceCard key={p.key} profile={p} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* Platform */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <SectionHeader icon={<Cpu className="w-4 h-4" />} label="This Platform" title="Our system" />
          <motion.div className="space-y-6 mt-10">
            {PLATFORM_SECTIONS.map((s, i) => (
              <motion.div
                key={s.id}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
              >
                <GlassCard padding="lg">
                  <h3 className="font-editorial text-xl text-white mb-3">{s.title}</h3>
                  {"body" in s && s.body && (
                    <p className="text-sm text-white/55 leading-relaxed font-light">{s.body}</p>
                  )}
                  {"bullets" in s && s.bullets && (
                    <ul className="mt-2 space-y-2">
                      {s.bullets.map((b) => (
                        <li key={b} className="flex gap-2 text-sm text-white/50 font-light">
                          <span className="text-accent-gold mt-1">·</span>
                          {b}
                        </li>
                      ))}
                    </ul>
                  )}
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 text-center">
        <p className="text-white/40 mb-6 font-light">Ready to map your own dermatoglyphic profile?</p>
        <Link href="/analysis/new">
          <MagneticButton size="lg" icon={<ArrowRight className="w-4 h-4" />}>
            Begin Analysis
          </MagneticButton>
        </Link>
      </section>
    </motion.div>
  );
}

function SectionHeader({
  icon,
  label,
  title,
}: {
  icon: React.ReactNode;
  label: string;
  title: string;
}) {
  return (
    <div>
      <div className="flex items-center gap-2 text-accent-gold mb-2">
        {icon}
        <p className="text-[10px] tracking-[0.25em] uppercase font-mono">{label}</p>
      </div>
      <h2 className="text-display-section text-white">{title}</h2>
    </div>
  );
}
