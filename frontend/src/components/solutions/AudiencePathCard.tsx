"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { AudiencePath } from "@/lib/audience-paths";
import { ArrowRight } from "lucide-react";

export function AudiencePathCard({ path, index }: { path: AudiencePath; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.5, delay: index * 0.08 }}
    >
      <Link href={path.href} id={path.id === "institution" ? "institution" : undefined}>
        <div
          className="group h-full rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
          style={{
            background: "rgba(255,255,255,0.03)",
            border: `1px solid ${path.accent}30`,
            boxShadow: `0 0 0 0 ${path.accent}00`,
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = `0 12px 40px ${path.accent}18`;
            e.currentTarget.style.borderColor = `${path.accent}50`;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = "none";
            e.currentTarget.style.borderColor = `${path.accent}30`;
          }}
        >
          <p className="text-[10px] font-mono uppercase tracking-widest mb-2" style={{ color: path.accent }}>
            {path.subtitle}
          </p>
          <h3 className="font-editorial text-2xl text-white mb-2">{path.title}</h3>
          <p className="text-sm text-white/45 font-light leading-relaxed mb-4">{path.description}</p>
          <ul className="space-y-1.5 mb-5">
            {path.features.map((f) => (
              <li key={f} className="text-[11px] text-white/35 flex gap-2">
                <span style={{ color: path.accent }}>·</span>
                {f}
              </li>
            ))}
          </ul>
          <span
            className="inline-flex items-center gap-1.5 text-xs font-medium transition-colors"
            style={{ color: path.accent }}
          >
            {path.cta}
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </span>
        </div>
      </Link>
    </motion.div>
  );
}
