"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  EXTENSIONS_CATALOG,
  EXTENSION_CATEGORIES,
  type ExtensionCategory,
} from "@/lib/extensions-catalog";
import { ExtensionCard } from "@/components/extensions/ExtensionCard";
import { cn } from "@/lib/utils";

export default function ExtensionsPage() {
  const [filter, setFilter] = useState<ExtensionCategory | "All">("All");
  const filtered =
    filter === "All"
      ? EXTENSIONS_CATALOG
      : EXTENSIONS_CATALOG.filter((e) => e.category === filter);

  return (
    <motion.div className="min-h-screen pb-24 px-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="max-w-5xl mx-auto pt-12">
        <p className="text-[10px] tracking-[0.3em] uppercase font-mono text-accent-gold mb-3">Extension Engine</p>
        <h1 className="text-display-section text-white mb-2">
          {EXTENSIONS_CATALOG.length} profile dimensions.
        </h1>
        <p className="text-white/40 font-light mb-8 max-w-xl">
          Every module derives from biometric capacity vectors — hover for DMIT meaning and inputs.
        </p>

        <div className="flex flex-wrap gap-2 mb-8">
          {(["All", ...EXTENSION_CATEGORIES] as const).map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setFilter(cat)}
              className={cn(
                "px-3 py-1.5 rounded-lg text-[11px] font-mono transition-colors",
                filter === cat
                  ? "bg-accent-gold-dim text-accent-champagne border border-[rgba(196,165,116,0.3)]"
                  : "text-white/40 hover:text-white/70 border border-white/[0.06]"
              )}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map((ext, i) => (
            <ExtensionCard key={ext.id} ext={ext} index={i} />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
