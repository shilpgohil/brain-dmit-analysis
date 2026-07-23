"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { getAnalysis, reportDownloadUrl, mediaUrl } from "@/lib/api";
import type { AnalysisResult } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { PipelineTracker } from "@/components/analysis/PipelineTracker";
import { OverviewTab } from "@/components/analysis/results/OverviewTab";
import { ExtensionsTab } from "@/components/analysis/results/ExtensionsTab";
import { CareerTab } from "@/components/analysis/results/CareerTab";
import { GOLD } from "@/lib/analysis-theme";
import { cn, fingerLabel, fingerRouteKey, formatRidgeCount } from "@/lib/utils";
import {
  Download, RefreshCw, AlertCircle, Fingerprint,
  Loader2, Clock, User, Layers,
} from "lucide-react";

const IN_PROGRESS = new Set(["preprocessing", "extracting", "mapping", "extending", "generating_report"]);
const TABS = ["overview", "fingerprints", "extensions", "career"] as const;

const PATTERN_COLORS: Record<string, string> = {
  whorl: "#c4a574",
  loop: "#9d8bb5",
  arch: "#b87d5c",
  accidental: "#6b9e8f",
  unknown: "#475569",
};

export default function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<typeof TABS[number]>("overview");

  const load = useCallback(async () => {
    try {
      setResult(await getAnalysis(id));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load.");
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    if (!result || !IN_PROGRESS.has(result.status)) return;
    const t = setInterval(load, 1800);
    return () => clearInterval(t);
  }, [result, load]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[70vh] text-center p-6">
        <AlertCircle className="w-10 h-10 text-rose-400 mb-4" />
        <p className="text-white/40">{error}</p>
        <MagneticButton variant="ghost" size="sm" onClick={load} icon={<RefreshCw className="w-3.5 h-3.5" />} className="mt-4">
          Retry
        </MagneticButton>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin" style={{ color: GOLD.primary }} />
          <p className="text-sm text-white/30">Loading analysis...</p>
        </div>
      </div>
    );
  }

  const isProcessing = IN_PROGRESS.has(result.status);
  const isComplete = result.status === "completed";
  const isFailed = result.status === "failed";

  return (
    <div className="min-h-screen pb-24">
      {/* Hero header */}
      <div className="relative overflow-hidden border-b border-white/[0.05] py-10 px-6">
        <div className="absolute inset-0 opacity-60">
          <FingerprintField opacity={0.06} animated={isProcessing} color="196, 165, 116" />
        </div>
        <div
          className="absolute inset-0"
          style={{ background: "linear-gradient(to bottom, rgba(2,2,8,0) 0%, rgba(2,2,8,0.8) 100%)" }}
        />

        <div className="relative z-10 max-w-6xl mx-auto">
          <motion.div
            className="flex flex-col sm:flex-row sm:items-end justify-between gap-4"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          >
            <div>
              <div className="flex items-center gap-2 mb-2">
                <StatusPill status={result.status} />
                {result.processing_time_ms && (
                  <span className="text-[10px] text-white/20 font-mono flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {(result.processing_time_ms / 1000).toFixed(1)}s
                  </span>
                )}
              </div>
              <h1 className="text-display-section text-white text-3xl sm:text-4xl">
                {result.subject_name ?? "Anonymous Subject"}
              </h1>
              <div className="flex items-center gap-4 mt-1.5 text-xs text-white/25">
                <span className="font-mono flex items-center gap-1">
                  <User className="w-3 h-3" />
                  {result.session_id.slice(0, 12)}
                </span>
                {result.total_features_extracted > 0 && (
                  <span className="flex items-center gap-1">
                    <Layers className="w-3 h-3" />
                    {result.total_features_extracted} features
                  </span>
                )}
                <span className="flex items-center gap-1">
                  <Fingerprint className="w-3 h-3" />
                  {result.fingers.length} fingers
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <MagneticButton variant="ghost" size="sm" onClick={load} icon={<RefreshCw className="w-3.5 h-3.5" />}>
                Refresh
              </MagneticButton>
              {result.report_url && (
                <a href={reportDownloadUrl(id, result.report_url)} target="_blank" rel="noopener noreferrer">
                  <MagneticButton size="sm" icon={<Download className="w-3.5 h-3.5" />}>
                    Download Report
                  </MagneticButton>
                </a>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 pt-8 space-y-8">
        {/* PROCESSING STATE */}
        {isProcessing && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="md:col-span-2">
              <GlassCard gradient glow="cyan">
                <div className="flex items-center gap-2 mb-5">
                  <Loader2 className="w-4 h-4 text-[#00d4ff] animate-spin" />
                  <span className="text-xs text-[#00d4ff] uppercase tracking-widest font-mono">
                    Pipeline Running
                  </span>
                </div>
                <PipelineTracker stages={result.pipeline_stages} />
              </GlassCard>
            </div>
            <GlassCard gradient>
              <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-3">Status</p>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 rounded-full bg-[#00d4ff] animate-pulse" />
                <span className="text-sm text-[#00d4ff] font-medium capitalize">
                  {result.status.replace(/_/g, " ")}
                </span>
              </div>
              <p className="text-xs text-white/25 leading-relaxed">
                The DMIT pipeline is processing your fingerprints. This typically
                takes 2–10 seconds.
              </p>
            </GlassCard>
          </div>
        )}

        {/* FAILED STATE */}
        {isFailed && (
          <GlassCard glow="none" className="border-rose-900/30" style={{ background: "rgba(244,63,94,0.05)" } as React.CSSProperties}>
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-rose-400 mb-1">Analysis failed</p>
                <p className="text-xs text-white/30 leading-relaxed">
                  {result.error_message ??
                    "The pipeline encountered an error. Ensure the FastAPI server is running and that the uploaded images are valid fingerprint files."}
                </p>
              </div>
            </div>
          </GlassCard>
        )}

        {/* COMPLETED */}
        {isComplete && (
          <>
            {result.warnings && result.warnings.length > 0 && (
              <GlassCard glow="none" className="border-amber-900/30" style={{ background: "rgba(245,158,11,0.06)" } as React.CSSProperties}>
                <p className="text-xs font-medium text-amber-400 mb-2">Notices</p>
                <ul className="text-xs text-white/35 space-y-1 list-disc list-inside">
                  {result.warnings.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </GlassCard>
            )}

            {/* Tab bar */}
            <motion.div
              className="flex gap-1 p-1 rounded-2xl w-fit max-w-full overflow-x-auto"
              style={{ background: "rgba(196,165,116,0.06)", border: `1px solid ${GOLD.border}` }}
            >
              {TABS.map((t) => (
                <button
                  key={t}
                  onClick={() => setTab(t)}
                  className={cn(
                    "relative px-5 py-2.5 text-xs font-medium capitalize transition-all duration-300 rounded-xl whitespace-nowrap",
                    tab === t ? "text-[#1a1510]" : "text-white/35 hover:text-white/60"
                  )}
                  style={
                    tab === t
                      ? { background: GOLD.gradient, boxShadow: `0 4px 20px ${GOLD.glow}` }
                      : undefined
                  }
                >
                  {t === "extensions" ? "Extensions" : t === "fingerprints" ? "Fingerprints" : t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </motion.div>

            <AnimatePresence mode="wait">
              {/* OVERVIEW TAB */}
              {tab === "overview" && (
                <motion.div
                  key="overview"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                >
                  <OverviewTab result={result} />
                </motion.div>
              )}

              {/* FINGERPRINTS TAB */}
              {tab === "fingerprints" && (
                <motion.div
                  key="fingerprints"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                >
                  {result.fingers.length === 0 ? (
                    <div className="py-16 text-center text-white/25">No finger data available.</div>
                  ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                      {result.fingers.map((f, i) => {
                        const patColor = PATTERN_COLORS[f.pattern_type] ?? "#475569";
                        return (
                          <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 16 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: i * 0.05, ease: [0.16, 1, 0.3, 1] }}
                          >
                            <Link href={`/analysis/${id}/finger/${encodeURIComponent(fingerRouteKey(f))}`}>
                              <div
                                className="group rounded-2xl overflow-hidden transition-all duration-400 hover:scale-[1.02] cursor-pointer"
                                style={{
                                  background: "rgba(255,255,255,0.03)",
                                  border: `1px solid ${patColor}25`,
                                  boxShadow: `0 0 30px ${patColor}08`,
                                }}
                              >
                                {/* Preview */}
                                <div
                                  className="relative h-28 flex items-center justify-center overflow-hidden"
                                  style={{ background: `${patColor}08` }}
                                >
                                  {mediaUrl(f.thumbnail_url) ? (
                                    // eslint-disable-next-line @next/next/no-img-element
                                    <img
                                      src={mediaUrl(f.thumbnail_url)}
                                      alt={fingerLabel(fingerRouteKey(f))}
                                      className="absolute inset-0 w-full h-full object-cover opacity-70 group-hover:opacity-90 transition-opacity"
                                    />
                                  ) : (
                                    <Fingerprint className="w-10 h-10 opacity-20 transition-opacity group-hover:opacity-30" style={{ color: patColor }} strokeWidth={0.8} />
                                  )}
                                  <div className="absolute inset-0"
                                    style={{ background: `radial-gradient(circle at center, ${patColor}10 0%, transparent 70%)` }} />
                                </div>

                                {/* Data */}
                                <div className="p-3 space-y-2">
                                  <div className="flex items-start justify-between">
                                    <p className="text-xs font-semibold text-white/80">
                                      {fingerLabel(fingerRouteKey(f))}
                                    </p>
                                    <span
                                      className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded"
                                      style={{ color: patColor, background: `${patColor}18` }}
                                    >
                                      {f.pattern_type}
                                    </span>
                                  </div>
                                  <div className="grid grid-cols-2 gap-x-2 gap-y-1.5">
                                    <DataPoint label="Ridges" value={formatRidgeCount(f.ridge_count, f.pattern_type)} />
                                    <DataPoint label="Fractal" value={f.fractal_dimension?.toFixed(3) ?? "—"} />
                                    <DataPoint label="Minutiae" value={f.minutiae_count?.toString() ?? "—"} />
                                    <DataPoint label="Entropy" value={f.entropy?.toFixed(2) ?? "—"} />
                                  </div>
                                </div>
                              </div>
                            </Link>
                          </motion.div>
                        );
                      })}
                    </div>
                  )}
                </motion.div>
              )}

              {/* EXTENSIONS TAB */}
              {tab === "extensions" && (
                <motion.div
                  key="extensions"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                >
                  <ExtensionsTab extensions={result.extensions} />
                </motion.div>
              )}

              {/* CAREER TAB */}
              {tab === "career" && (
                <motion.div
                  key="career"
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                >
                  <CareerTab result={result} />
                </motion.div>
              )}
            </AnimatePresence>
          </>
        )}
      </div>
    </div>
  );
}

function StatusPill({ status }: { status: string }) {
  const map: Record<string, { label: string; color: string }> = {
    completed:         { label: "Completed",  color: "#10b981" },
    failed:            { label: "Failed",     color: "#f43f5e" },
    pending:           { label: "Pending",    color: "#475569" },
    preprocessing:     { label: "Preprocessing", color: "#00d4ff" },
    extracting:        { label: "Extracting",    color: "#00d4ff" },
    mapping:           { label: "Mapping",       color: "#8b5cf6" },
    extending:         { label: "Analyzing",     color: "#8b5cf6" },
    generating_report: { label: "Generating",    color: "#f59e0b" },
  };
  const cfg = map[status] ?? { label: status, color: "#475569" };

  return (
    <span
      className="inline-flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-wide px-2 py-1 rounded-full"
      style={{ color: cfg.color, background: `${cfg.color}15`, border: `1px solid ${cfg.color}30` }}
    >
      <span
        className={cn("w-1.5 h-1.5 rounded-full", (!["completed","failed","pending"].includes(status)) && "animate-pulse")}
        style={{ background: cfg.color }}
      />
      {cfg.label}
    </span>
  );
}

function DataPoint({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[8px] text-white/20 uppercase tracking-widest">{label}</p>
      <p className="text-[11px] text-white/60 font-mono">{value}</p>
    </div>
  );
}
