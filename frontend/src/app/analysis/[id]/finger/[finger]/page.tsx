"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { getAnalysis } from "@/lib/api";
import type { FingerBiometrics } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { patternLabel, fingerLabel, fingerRouteKey, lobeLabel, lobeDescription, formatRidgeCount } from "@/lib/utils";
import { ArrowLeft, Fingerprint, AlertCircle, Loader2 } from "lucide-react";

const FINGER_LOBE: Record<string, string> = {
  thumb: "prefrontal_lobe",
  index: "posterior_frontal",
  middle: "parietal_lobe",
  ring: "temporal_lobe",
  little: "occipital_lobe",
};

const PATTERN_COLORS: Record<string, string> = {
  whorl: "#8b5cf6",
  loop: "#00d4ff",
  arch: "#f59e0b",
  accidental: "#10b981",
  unknown: "#475569",
};

const PATTERN_DESCRIPTIONS: Record<string, string> = {
  whorl: "Whorls feature two triradii (delta points) and indicate strong self-motivation, independence, and analytical depth. Subjects with predominant whorls tend toward introversion, systematic thinking, and high focus capacity.",
  loop: "Loops feature one triradius and are the most prevalent pattern globally. They indicate sociability, adaptability, and environment-sensitivity — correlating with cooperative, flexible cognitive styles.",
  arch: "Arches feature no triradius and are the rarest pattern. They indicate practicality, reliability, and a strong preference for concrete tasks over abstract reasoning.",
  accidental: "Accidentals are hybrid formations combining multiple pattern family characteristics — indicating complex, multifaceted, and often highly adaptable cognitive profiles.",
  unknown: "Pattern classification could not be resolved for this image. Image quality may be insufficient for accurate ridge characterization.",
};

export default function FingerDetailPage() {
  const { id, finger } = useParams<{ id: string; finger: string }>();
  const [data, setData] = useState<FingerBiometrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAnalysis(id)
      .then((result) => {
        const key = decodeURIComponent(finger);
        setData(result.fingers.find((f) => fingerRouteKey(f) === key) ?? null);
      })
      .catch((e) => setError(e.message));
  }, [id, finger]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[70vh] text-center p-6">
        <AlertCircle className="w-8 h-8 text-rose-400 mb-3" />
        <p className="text-sm text-white/40">{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <Loader2 className="w-8 h-8 text-[#00d4ff] animate-spin" />
      </div>
    );
  }

  const lobe = FINGER_LOBE[data.finger_type];
  const patColor = PATTERN_COLORS[data.pattern_type] ?? "#475569";

  return (
    <div className="min-h-screen pb-24">
      {/* Hero */}
      <div className="relative overflow-hidden border-b border-white/[0.04] py-10 px-6">
        <div className="absolute inset-0 opacity-50">
          <FingerprintField opacity={0.1} animated color={patColor === "#00d4ff" ? "0, 212, 255" : "139, 92, 246"} />
        </div>
        <div
          className="absolute inset-0"
          style={{ background: "linear-gradient(to bottom, rgba(2,2,8,0), rgba(2,2,8,0.85))" }}
        />

        <div className="relative z-10 max-w-5xl mx-auto">
          <Link href={`/analysis/${id}`}>
            <MagneticButton variant="ghost" size="sm" icon={<ArrowLeft className="w-3.5 h-3.5" />} className="mb-6">
              Back to Analysis
            </MagneticButton>
          </Link>

          <motion.div
            className="flex items-start gap-5"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          >
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center flex-shrink-0"
              style={{
                background: `${patColor}12`,
                border: `1px solid ${patColor}30`,
                boxShadow: `0 0 30px ${patColor}15`,
              }}
            >
              <Fingerprint className="w-8 h-8" style={{ color: patColor }} strokeWidth={1} />
            </div>
            <div>
              <h1 className="text-display-section text-white text-3xl">
                {fingerLabel(data.finger_type)}
              </h1>
              <p className="text-white/40 mt-1">
                Pattern:{" "}
                <span className="font-medium" style={{ color: patColor }}>
                  {patternLabel(data.pattern_type)}
                </span>
                {data.pattern_subtype && (
                  <span className="text-white/20 ml-2 font-mono text-sm">{data.pattern_subtype}</span>
                )}
              </p>
              {lobe && (
                <p className="text-xs text-white/20 mt-1 font-mono">
                  Brain region: <span className="text-blue-400">{lobeLabel(lobe)}</span>
                </p>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 pt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {/* Biometric measurements */}
          <div className="lg:col-span-2 space-y-5">
            <GlassCard gradient glow="cyan">
              <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-5">
                Biometric Measurements
              </p>
              <div className="grid grid-cols-2 gap-4">
                <BiometricMetric
                  label="Ridge Count (TFRC)"
                  value={formatRidgeCount(data.ridge_count, data.pattern_type)}
                  desc="Physical count of ridges along the core–delta axis"
                  color={patColor}
                  i={0}
                />
                <BiometricMetric
                  label="Fractal Dimension"
                  value={data.fractal_dimension?.toFixed(4) ?? "—"}
                  desc="Box-counting complexity (0–2 scale)"
                  color={patColor}
                  i={1}
                />
                <BiometricMetric
                  label="Minutiae Count"
                  value={data.minutiae_count != null ? String(data.minutiae_count) : "—"}
                  desc="Detected ridge endings and bifurcations"
                  color={patColor}
                  i={2}
                />
                <BiometricMetric
                  label="Shannon Entropy"
                  value={data.entropy?.toFixed(4) ?? "—"}
                  desc="Information content of the ridge pattern"
                  color={patColor}
                  i={3}
                />
                <BiometricMetric
                  label="Quality Score"
                  value={data.quality_score != null ? `${(data.quality_score * 100).toFixed(1)}%` : "—"}
                  desc="Overall image quality assessment"
                  color={patColor}
                  i={4}
                />
                <BiometricMetric
                  label="Quality Tier"
                  value={data.quality_tier ?? "—"}
                  desc="Feature extraction depth achieved"
                  color={patColor}
                  i={5}
                />
              </div>
            </GlassCard>

            {/* Pattern interpretation */}
            <GlassCard gradient>
              <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-4">
                Pattern Interpretation
              </p>
              <p className="text-sm text-white/50 leading-relaxed">
                {PATTERN_DESCRIPTIONS[data.pattern_type] ?? PATTERN_DESCRIPTIONS.unknown}
              </p>
            </GlassCard>

            {/* Raw features */}
            {data.raw_features && Object.keys(data.raw_features).length > 0 && (
              <GlassCard gradient>
                <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-4">
                  Extracted Features
                  <span className="ml-2 text-white/15">
                    {Object.keys(data.raw_features).length} metrics
                  </span>
                </p>
                <div className="grid grid-cols-2 gap-x-5 gap-y-1.5 max-h-72 overflow-y-auto no-scrollbar">
                  {Object.entries(data.raw_features)
                    .sort((a, b) => a[0].localeCompare(b[0]))
                    .map(([k, v]) => (
                      <div
                        key={k}
                        className="flex items-center justify-between py-1 border-b border-white/[0.04]"
                      >
                        <span className="text-[10px] text-white/30 truncate pr-2">
                          {k.replace(/_/g, " ")}
                        </span>
                        <span className="text-[10px] text-white/50 font-mono flex-shrink-0">
                          {typeof v === "number" ? (Number.isInteger(v) ? v : v.toFixed(4)) : String(v)}
                        </span>
                      </div>
                    ))}
                </div>
              </GlassCard>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-5">
            {lobe && (
              <GlassCard gradient glow="blue">
                <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-4">
                  Brain Lobe Mapping
                </p>
                <div className="space-y-4">
                  <div>
                    <p className="text-[10px] text-white/20 uppercase tracking-widest font-mono mb-1">
                      Primary Region
                    </p>
                    <p className="text-sm font-semibold text-blue-400">{lobeLabel(lobe)}</p>
                  </div>
                  <div>
                    <p className="text-[10px] text-white/20 uppercase tracking-widest font-mono mb-1">
                      Function
                    </p>
                    <p className="text-xs text-white/40 leading-relaxed">
                      {lobeDescription(lobe)}
                    </p>
                  </div>
                  <div className="border-t border-white/[0.05] pt-4">
                    <p className="text-[10px] text-white/15 leading-relaxed">
                      Based on CADA (China Association of Dermatoglyphics Analyst) standards.
                      Finger-lobe correlations follow Table 1.1 of the DMIT scientific mapping standard.
                    </p>
                  </div>
                </div>
              </GlassCard>
            )}

            <GlassCard gradient>
              <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-4">
                Classification
              </p>
              <div className="space-y-2.5">
                <Row label="Pattern Family" value={data.pattern_type} color={patColor} />
                {data.pattern_subtype && <Row label="Subtype" value={data.pattern_subtype} />}
                <div className="border-t border-white/[0.05] pt-3 mt-3">
                  <p className="text-[10px] text-white/15 leading-relaxed">
                    CADA standard: Arch (0 delta), Loop (1 delta, 1 core), Whorl (2+ deltas).
                  </p>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  );
}

function BiometricMetric({
  label, value, desc, color, i,
}: { label: string; value: string; desc?: string; color: string; i: number }) {
  return (
    <motion.div
      className="py-3 border-b border-white/[0.04]"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: i * 0.06 }}
    >
      <p className="text-[9px] text-white/20 uppercase tracking-widest font-mono mb-1">{label}</p>
      <p className="text-base font-bold font-mono" style={{ color }}>{value}</p>
      {desc && <p className="text-[10px] text-white/20 mt-0.5 leading-snug">{desc}</p>}
    </motion.div>
  );
}

function Row({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-white/30">{label}</span>
      <span
        className="text-xs font-medium font-mono capitalize"
        style={{ color: color ?? "rgba(255,255,255,0.6)" }}
      >
        {value}
      </span>
    </div>
  );
}
