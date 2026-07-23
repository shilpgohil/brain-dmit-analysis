"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { AUDIENCE_PATHS } from "@/lib/audience-paths";
import { AudiencePathCard } from "@/components/solutions/AudiencePathCard";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { FileText } from "lucide-react";

export default function SolutionsPage() {
  return (
    <motion.div className="min-h-screen pb-24" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <section className="relative py-20 px-6 overflow-hidden">
        <div className="absolute inset-0 opacity-30">
          <FingerprintField opacity={0.08} animated color="196, 165, 116" />
        </div>
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <p className="text-[10px] tracking-[0.3em] uppercase font-mono text-accent-gold mb-4">Solutions</p>
          <h1 className="text-display-section text-white mb-4">
            Built for <span className="text-emphasis-italic gradient-text-premium">every audience.</span>
          </h1>
          <p className="text-white/45 font-light leading-relaxed">
            Individuals at home, DMIT clinics, schools, corporates, and strategic partners — one platform, four paths.
          </p>
          <Link
            href="/about"
            className="inline-flex items-center gap-2 mt-6 text-xs font-mono text-white/30 hover:text-accent-gold transition-colors"
          >
            <FileText className="w-3.5 h-3.5" />
            DMIT science guide · see docs/PRODUCT_ROADMAP.md in repo
          </Link>
        </div>
      </section>

      <section className="px-6 max-w-5xl mx-auto">
        <motion.div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {AUDIENCE_PATHS.map((path, i) => (
            <AudiencePathCard key={path.id} path={path} index={i} />
          ))}
        </motion.div>
      </section>
    </motion.div>
  );
}
