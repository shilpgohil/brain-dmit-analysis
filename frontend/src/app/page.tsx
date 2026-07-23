"use client";

import { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { motion, useScroll, useTransform, useSpring } from "framer-motion";
import { listSessions, getHealth } from "@/lib/api";
import type { SessionListItem, SystemStatus } from "@/lib/types";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { ParticleField } from "@/components/effects/ParticleField";
import { PipelineStageVisual, type PipelineStageId } from "@/components/visualization/PipelineStageVisual";
import { IntelligenceCard } from "@/components/analysis/IntelligenceCard";
import { INTELLIGENCE_PROFILES } from "@/lib/dmit-knowledge";
import { AUDIENCE_PATHS } from "@/lib/audience-paths";
import { AudiencePathCard } from "@/components/solutions/AudiencePathCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { GlassCard } from "@/components/ui/GlassCard";
import { CinematicText, RevealBlock } from "@/components/ui/CinematicText";
import { relativeTime } from "@/lib/utils";
import {
  ArrowRight,
  Fingerprint,
  Activity,
  ChevronRight,
} from "lucide-react";

const PIPELINE_STAGES: {
  id: PipelineStageId;
  label: string;
  desc: string;
  color: string;
}[] = [
  { id: "capture", label: "Biometric Capture", desc: "10-finger dermatoglyphic imaging", color: "#00d4ff" },
  { id: "extraction", label: "Feature Extraction", desc: "85 biometric metrics per print", color: "#8b5cf6" },
  { id: "mapping", label: "Neural Mapping", desc: "Finger-to-brain-lobe correlation", color: "#3b82f6" },
  { id: "profile", label: "Intelligence Profile", desc: "Gardner MI + behavioral modeling", color: "#f59e0b" },
  { id: "report", label: "Report Generation", desc: "Professional PDF output", color: "#10b981" },
];

export default function LandingPage() {
  const { scrollY } = useScroll();
  const heroY = useTransform(scrollY, [0, 600], [0, -120]);
  const heroOpacity = useTransform(scrollY, [0, 400], [1, 0.3]);
  const fpScale = useTransform(scrollY, [0, 500], [1, 1.15]);

  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [health, setHealth] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      listSessions(6).catch(() => []),
      getHealth().catch(() => null),
    ]).then(([s, h]) => {
      setSessions(s);
      setHealth(h);
      setLoading(false);
    });
  }, []);

  const completed = sessions.filter((s) => s.status === "completed").length;

  return (
    <div className="min-h-screen">
      {/* â”€â”€ HERO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden px-6">
        {/* Orbital ridge lines â€” animated fingerprint field */}
        <motion.div className="absolute inset-0" style={{ scale: fpScale }}>
          <FingerprintField opacity={0.12} animated color="196, 165, 116" />
        </motion.div>

        {/* Particle field */}
        <div className="absolute inset-0 pointer-events-none">
          <ParticleField count={50} />
        </div>

        {/* Central radial glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: "radial-gradient(ellipse 60% 50% at 50% 45%, rgba(196,165,116,0.08) 0%, transparent 70%)",
          }}
        />

        {/* Hero content */}
        <motion.div
          className="relative z-10 text-center max-w-4xl mx-auto"
          style={{ y: heroY, opacity: heroOpacity }}
        >
          {/* Pre-title chip */}
          <RevealBlock delay={0.1}>
            <div className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 rounded-full border border-white/[0.10] bg-white/[0.03] text-xs text-white/50">
              <span className="w-1.5 h-1.5 rounded-full bg-[var(--accent-gold)] animate-pulse" />
              <span className="tracking-widest uppercase font-mono">Biometric Intelligence Platform</span>
            </div>
          </RevealBlock>

          {/* Main headline */}
          <h1 className="text-display-hero mb-6">
            <div className="overflow-hidden">
              <motion.div
                initial={{ y: "110%" }}
                animate={{ y: 0 }}
                transition={{ duration: 0.9, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                className="text-white/95"
              >
                Your Fingerprints
              </motion.div>
            </div>
            <div className="overflow-hidden">
              <motion.div
                initial={{ y: "110%" }}
                animate={{ y: 0 }}
                transition={{ duration: 0.9, delay: 0.35, ease: [0.16, 1, 0.3, 1] }}
                className="text-emphasis-italic gradient-text-cyan-violet"
              >
                Hold Your Mind.
              </motion.div>
            </div>
          </h1>

          {/* Subline */}
          <RevealBlock delay={0.55} className="mb-8">
            <p className="text-lg text-white/40 max-w-2xl mx-auto leading-relaxed font-light">
              Advanced dermatoglyphics intelligence analysis â€” mapping biometric ridge patterns
              to brain lobes, cognitive capacities, and behavioral profiles.
            </p>
          </RevealBlock>

          {/* CTAs */}
          <RevealBlock delay={0.7} className="flex items-center justify-center gap-4">
            <Link href="/analysis/new">
              <MagneticButton size="lg" icon={<Fingerprint className="w-4 h-4" />}>
                Begin Analysis
              </MagneticButton>
            </Link>
            <Link href="/sessions">
              <MagneticButton variant="secondary" size="lg" icon={<Activity className="w-4 h-4" />}>
                View Sessions
              </MagneticButton>
            </Link>
          </RevealBlock>

          {/* Stats */}
          <RevealBlock delay={0.9} className="mt-14 flex items-center justify-center gap-8">
            <Stat value="85" label="Features Extracted" />
            <div className="w-px h-8 bg-white/[0.08]" />
            <Stat value="9" label="Intelligence Types" />
            <div className="w-px h-8 bg-white/[0.08]" />
            <Stat value="46" label="Extension Modules" />
            <div className="w-px h-8 bg-white/[0.08]" />
            <Stat value={String(sessions.length)} label="Sessions" dynamic />
          </RevealBlock>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4, duration: 0.8 }}
        >
          <span className="text-[10px] text-white/20 tracking-widest uppercase font-mono">Scroll</span>
          <div className="w-px h-10 bg-gradient-to-b from-white/20 to-transparent" />
        </motion.div>
      </section>

      {/* â”€â”€ SOLUTIONS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="py-24 px-6 border-t border-white/[0.05]">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-xs text-accent-gold tracking-widest uppercase font-mono mb-3">Who it&apos;s for</p>
            <h2 className="text-display-section text-white">
              One platform. <span className="text-emphasis-italic gradient-text-premium">Four paths.</span>
            </h2>
            <Link href="/solutions" className="inline-block mt-3 text-xs font-mono text-accent-gold/80 hover:text-accent-gold">
              Explore all solutions â†’
            </Link>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {AUDIENCE_PATHS.map((path, i) => (
              <AudiencePathCard key={path.id} path={path} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* â”€â”€ PIPELINE SECTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="relative py-32 px-6 overflow-hidden">
        <div className="absolute inset-0"
          style={{ background: "linear-gradient(180deg, transparent, rgba(4,4,15,0.95) 20%, rgba(4,4,15,0.95) 80%, transparent)" }} />

        <div className="relative z-10 max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 32 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <p className="text-xs text-accent-gold tracking-widest uppercase font-mono mb-3">
              Analysis Pipeline
            </p>
            <h2 className="text-display-section text-white">
              Five stages from print to profile.
            </h2>
          </motion.div>

          <div className="relative">
            {/* Connecting line */}
            <div className="absolute top-8 left-8 right-8 h-px bg-gradient-to-r from-transparent via-white/[0.08] to-transparent hidden lg:block" />

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              {PIPELINE_STAGES.map((stage, i) => (
                <motion.div
                  key={stage.label}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-40px" }}
                  transition={{ duration: 0.6, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
                >
                  <GlassCard padding="md" gradient className="h-full group cursor-default overflow-hidden">
                    <PipelineStageVisual stage={stage.id} index={i} accent={stage.color} />
                    <p className="font-editorial text-lg text-white/90 mb-1 leading-tight">{stage.label}</p>
                    <p className="text-[11px] text-white/35 leading-relaxed font-light">{stage.desc}</p>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* â”€â”€ INTELLIGENCE GRID â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="py-24 px-6 relative">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="mb-12"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <p className="text-xs text-accent-gold tracking-widest uppercase font-mono mb-3">
              Intelligence Mapping
            </p>
            <h2 className="text-display-section text-white">
              Nine intelligences.{" "}
              <span className="text-emphasis-italic gradient-text-premium">Ten fingers.</span>
            </h2>
            <p className="text-white/40 mt-3 max-w-lg font-light">
              Howard Gardner&apos;s framework mapped to brain lobes via the CADA dermatoglyphics standard.
              Hover or tap any card for a full DMIT explanation.
            </p>
            <Link href="/about" className="inline-block mt-3 text-xs text-accent-gold/80 hover:text-accent-gold transition-colors font-mono tracking-wide">
              Read full DMIT guide â†’
            </Link>
          </motion.div>

          <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2 overflow-visible pt-4">
            {INTELLIGENCE_PROFILES.map((profile, i) => (
              <IntelligenceCard key={profile.key} profile={profile} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* â”€â”€ RECENT SESSIONS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="py-24 px-6 relative">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-end justify-between mb-10">
            <motion.div
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              <p className="text-xs text-accent-gold tracking-widest uppercase font-mono mb-2">
                Recent Activity
              </p>
              <h2 className="text-display-section text-white text-3xl">
                {sessions.length > 0 ? `${sessions.length} analyses on record.` : "No analyses yet."}
              </h2>
            </motion.div>
            <Link href="/sessions">
              <MagneticButton variant="ghost" size="sm" icon={<ChevronRight className="w-3.5 h-3.5" />}>
                All sessions
              </MagneticButton>
            </Link>
          </div>

          {sessions.length === 0 ? (
            <GlassCard padding="lg" className="flex flex-col items-center py-16 text-center">
              <div
                className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4"
                style={{ background: "rgba(196,165,116,0.08)", border: "1px solid rgba(196,165,116,0.2)" }}
              >
                <Fingerprint className="w-8 h-8 text-accent-gold/50" strokeWidth={1} />
              </div>
              <p className="text-white/40 mb-1">No sessions recorded</p>
              <p className="text-sm text-white/20">Start your first analysis to see results here.</p>
              <div className="mt-6">
                <Link href="/analysis/new">
                  <MagneticButton size="sm">Start Analysis</MagneticButton>
                </Link>
              </div>
            </GlassCard>
          ) : (
            <div className="space-y-2">
              {sessions.map((session, i) => (
                <SessionRow key={session.id} session={session} index={i} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* â”€â”€ CTA SECTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <section className="py-32 px-6 relative overflow-hidden">
        <div
          className="absolute inset-0 pointer-events-none"
          style={{ background: "radial-gradient(ellipse 60% 60% at 50% 50%, rgba(139,92,246,0.08) 0%, transparent 70%)" }}
        />

        <motion.div
          className="relative z-10 max-w-2xl mx-auto text-center"
          initial={{ opacity: 0, y: 32 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <h2 className="text-display-section text-white mb-4">
            Begin a{" "}
            <span className="text-emphasis-italic gradient-text-cyan-violet">new analysis.</span>
          </h2>
          <p className="text-white/40 text-lg mb-8 leading-relaxed">
            Upload ten fingerprint images and receive a complete cognitive intelligence profile
            in under ten seconds.
          </p>
          <Link href="/analysis/new">
            <MagneticButton size="lg" icon={<ArrowRight className="w-4 h-4" />} strength={0.5}>
              Start Analysis
            </MagneticButton>
          </Link>
        </motion.div>
      </section>

      {/* â”€â”€ Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <footer className="border-t border-white/[0.05] py-8 px-6">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Fingerprint className="w-4 h-4 text-accent-gold/50" />
            <span className="text-[11px] text-white/20 font-mono tracking-widest uppercase">
              DMIT Platform v3.2
            </span>
          </div>
          <Link href="/about" className="text-[11px] text-white/25 hover:text-accent-gold transition-colors">
            About DMIT & Platform
          </Link>
        </div>
      </footer>
    </div>
  );
}

function Stat({ value, label, dynamic }: { value: string; label: string; dynamic?: boolean }) {
  return (
    <div className="text-center">
      <p className={`text-2xl font-bold tabular font-mono ${dynamic ? "text-accent-gold" : "text-white"}`}>
        {value}
      </p>
      <p className="text-[10px] text-white/30 mt-0.5 uppercase tracking-widest">{label}</p>
    </div>
  );
}

function SessionRow({ session, index }: { session: SessionListItem; index: number }) {
  const STATUS_COLOR: Record<string, string> = {
    completed: "#10b981",
    failed: "#f43f5e",
    pending: "#475569",
  };
  const color = STATUS_COLOR[session.status] ?? "#3b82f6";

  return (
    <motion.div
      initial={{ opacity: 0, x: -16 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4, delay: index * 0.06, ease: [0.16, 1, 0.3, 1] }}
    >
      <Link href={`/analysis/${session.id}`}>
        <div
          className="flex items-center gap-4 px-5 py-3.5 rounded-xl group transition-all duration-300 hover:bg-white/[0.04]"
          style={{ border: "1px solid rgba(255,255,255,0.05)" }}
        >
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-all duration-300 group-hover:scale-110"
            style={{ background: `${color}15`, border: `1px solid ${color}25` }}
          >
            <Fingerprint className="w-4 h-4" style={{ color }} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white/70 group-hover:text-white transition-colors truncate">
              {session.subject_name ?? "Anonymous Subject"}
            </p>
            <p className="text-[11px] text-white/20 font-mono">
              {session.finger_count} fingerprints Â· {relativeTime(session.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span
              className="text-[10px] font-medium uppercase tracking-wide px-2 py-0.5 rounded font-mono"
              style={{ color, background: `${color}15` }}
            >
              {session.status}
            </span>
            <ChevronRight className="w-4 h-4 text-white/15 group-hover:text-white/40 group-hover:translate-x-1 transition-all" />
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
