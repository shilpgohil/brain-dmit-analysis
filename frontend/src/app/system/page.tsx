"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getHealth } from "@/lib/api";
import type { SystemStatus } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { RefreshCw, CheckCircle2, XCircle, AlertTriangle, Activity } from "lucide-react";

const COMPONENT_META: Record<string, { label: string; desc: string; color: string }> = {
  feature_extractor: {
    label: "Feature Extractor",
    desc: "Extracts 85 biometric measurements per fingerprint via OpenCV, fractal analysis, topological computation, and ridge characterization.",
    color: "#00d4ff",
  },
  intelligence_mapper: {
    label: "Intelligence Mapper",
    desc: "Maps biometric vectors to Howard Gardner's Multiple Intelligence framework using CADA Table 1.1 finger-lobe correlations.",
    color: "#8b5cf6",
  },
  extensions_engine: {
    label: "Extensions Engine",
    desc: "Orchestrates 46 behavioral analysis modules across career, emotional intelligence, cognitive load, and personality domains.",
    color: "#3b82f6",
  },
  pdf_generator: {
    label: "PDF Generator",
    desc: "Generates professional multi-page reports using ReportLab with embedded Plotly visualizations and biometric summaries.",
    color: "#10b981",
  },
};

export default function SystemPage() {
  const [health, setHealth] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [lastChecked, setLastChecked] = useState<Date>(new Date());

  const load = async () => {
    setLoading(true);
    try {
      setHealth(await getHealth());
      setError(false);
      setLastChecked(new Date());
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const allOk = health ? Object.values(health.components).every(Boolean) : false;

  return (
    <div className="min-h-screen pb-24 px-6 pt-12">
      <div className="max-w-3xl mx-auto space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="text-xs text-[#00d4ff] tracking-widest uppercase font-mono mb-2">
            Infrastructure
          </p>
          <h1 className="text-display-section text-white">
            System Status
          </h1>
        </motion.div>

        {/* Status banner */}
        {health && (
          <motion.div
            className="flex items-center gap-4 p-4 rounded-2xl"
            style={{
              background: allOk ? "rgba(16,185,129,0.06)" : "rgba(245,158,11,0.06)",
              border: `1px solid ${allOk ? "rgba(16,185,129,0.2)" : "rgba(245,158,11,0.2)"}`,
            }}
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            {allOk
              ? <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              : <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0" />
            }
            <div>
              <p className={`text-sm font-medium ${allOk ? "text-emerald-400" : "text-amber-400"}`}>
                {allOk ? "All systems operational" : "Some components offline"}
              </p>
              <p className="text-xs text-white/25 mt-0.5 font-mono">
                v{health.pipeline_version} · checked {lastChecked.toLocaleTimeString()}
              </p>
            </div>
            <MagneticButton
              variant="ghost"
              size="sm"
              onClick={load}
              loading={loading}
              icon={<RefreshCw className="w-3.5 h-3.5" />}
              className="ml-auto"
            >
              Refresh
            </MagneticButton>
          </motion.div>
        )}

        {error && (
          <motion.div
            className="p-5 rounded-2xl"
            style={{ background: "rgba(244,63,94,0.06)", border: "1px solid rgba(244,63,94,0.2)" }}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          >
            <div className="flex items-start gap-3">
              <XCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-rose-400 mb-1">API Unreachable</p>
                <p className="text-xs text-white/30 mb-3">
                  The FastAPI backend is not responding on port 8000.
                </p>
                <div className="font-mono text-xs text-white/30 p-3 rounded-lg"
                  style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                  python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Components */}
        {health && (
          <div className="space-y-3">
            <p className="text-[10px] text-white/25 uppercase tracking-widest font-mono">Pipeline Components</p>
            {Object.entries(health.components).map(([key, ok], i) => {
              const meta = COMPONENT_META[key];
              return (
                <motion.div
                  key={key}
                  initial={{ opacity: 0, x: -16 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] }}
                >
                  <GlassCard padding="md" glow="none" hover={false}>
                    <div className="flex items-start gap-4">
                      <div
                        className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                        style={{
                          background: ok ? `${meta?.color ?? "#00d4ff"}15` : "rgba(244,63,94,0.1)",
                          border: `1px solid ${ok ? `${meta?.color ?? "#00d4ff"}25` : "rgba(244,63,94,0.2)"}`,
                        }}
                      >
                        {ok
                          ? <CheckCircle2 className="w-4 h-4" style={{ color: meta?.color ?? "#00d4ff" }} />
                          : <XCircle className="w-4 h-4 text-rose-400" />
                        }
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-white/80">
                            {meta?.label ?? key}
                          </p>
                          <span className={`text-xs font-mono ${ok ? "text-emerald-400" : "text-rose-400"}`}>
                            {ok ? "Online" : "Offline"}
                          </span>
                        </div>
                        <p className="text-xs text-white/25 mt-1 leading-relaxed">{meta?.desc}</p>
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Stats */}
        {health && (
          <GlassCard gradient>
            <div className="flex items-center gap-2 mb-5">
              <Activity className="w-4 h-4 text-white/30" />
              <span className="text-xs text-white/30 uppercase tracking-widest font-mono">Runtime Statistics</span>
            </div>
            <div className="grid grid-cols-2 gap-5">
              <StatItem label="Total Sessions" value={String(health.total_sessions)} />
              <StatItem label="Processing Queue" value={String(health.processing_queue)} />
              <StatItem label="API Status" value={health.status} highlight={health.status === "operational"} />
              <StatItem label="Pipeline Version" value={health.pipeline_version} mono />
            </div>
          </GlassCard>
        )}
      </div>
    </div>
  );
}

function StatItem({ label, value, highlight, mono }: { label: string; value: string; highlight?: boolean; mono?: boolean }) {
  return (
    <div>
      <p className="text-[10px] text-white/20 uppercase tracking-widest font-mono mb-1">{label}</p>
      <p className={`text-sm font-medium ${highlight ? "text-emerald-400" : "text-white/70"} ${mono ? "font-mono" : ""}`}>
        {value}
      </p>
    </div>
  );
}
