"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { listSessions, getAnalysis } from "@/lib/api";
import type { SessionListItem, AnalysisResult } from "@/lib/types";
import { CompareView } from "@/components/compare/CompareView";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { GlassCard } from "@/components/ui/GlassCard";
import { GitCompare, Loader2 } from "lucide-react";
import { useAuthGuard } from "@/hooks/useAuthGuard";

export default function ComparePage() {
  const { user, isLoading } = useAuthGuard("partner");
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [idA, setIdA] = useState("");
  const [idB, setIdB] = useState("");
  const [resultA, setResultA] = useState<AnalysisResult | null>(null);
  const [resultB, setResultB] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    listSessions(100)
      .then((s) => setSessions(s.filter((x) => x.status === "completed")))
      .catch(() => setSessions([]));
  }, [user]);

  const runCompare = async () => {
    if (!idA || !idB || idA === idB) {
      setError("Select two different completed sessions.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const [a, b] = await Promise.all([getAnalysis(idA), getAnalysis(idB)]);
      setResultA(a);
      setResultB(b);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load sessions.");
      setResultA(null);
      setResultB(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div className="min-h-screen pb-24 px-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="max-w-3xl mx-auto pt-12">
        <motion.div className="flex items-center gap-2 text-accent-gold mb-3">
          <GitCompare className="w-4 h-4" />
          <p className="text-[10px] tracking-[0.25em] uppercase font-mono">Counselor Tool</p>
        </motion.div>
        <h1 className="text-display-section text-white mb-2">Compare profiles.</h1>
        <p className="text-white/40 font-light mb-8">
          Side-by-side multiple intelligence comparison for couples, siblings, or team members.
        </p>

        <GlassCard padding="lg" className="mb-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="text-[10px] font-mono uppercase text-white/35 mb-1 block">Session A</label>
              <select
                value={idA}
                onChange={(e) => setIdA(e.target.value)}
                className="w-full h-10 rounded-lg border border-white/[0.08] text-sm px-3"
                style={{ background: "rgba(8,8,24,0.9)", color: "rgba(255,255,255,0.7)" }}
              >
                <option value="" style={{ background: "#0d0d1a" }}>Select…</option>
                {sessions.map((s) => (
                  <option key={s.id} value={s.id} style={{ background: "#0d0d1a" }}>
                    {s.subject_name ?? s.id.slice(0, 8)} — {new Date(s.created_at).toLocaleDateString()}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-[10px] font-mono uppercase text-white/35 mb-1 block">Session B</label>
              <select
                value={idB}
                onChange={(e) => setIdB(e.target.value)}
                className="w-full h-10 rounded-lg border border-white/[0.08] text-sm px-3"
                style={{ background: "rgba(8,8,24,0.9)", color: "rgba(255,255,255,0.7)" }}
              >
                <option value="" style={{ background: "#0d0d1a" }}>Select…</option>
                {sessions.map((s) => (
                  <option key={s.id} value={s.id} style={{ background: "#0d0d1a" }}>
                    {s.subject_name ?? s.id.slice(0, 8)} — {new Date(s.created_at).toLocaleDateString()}
                  </option>
                ))}
              </select>
            </div>
          </div>
          {error && <p className="text-rose-400 text-sm mb-3">{error}</p>}
          <MagneticButton
            onClick={runCompare}
            disabled={loading}
            icon={loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <GitCompare className="w-4 h-4" />}
          >
            {loading ? "Loading…" : "Compare"}
          </MagneticButton>
          {sessions.length === 0 && (
            <p className="text-white/30 text-xs mt-4">
              No completed sessions yet.{" "}
              <Link href="/analysis/new" className="text-accent-gold hover:underline">
                Run an analysis first.
              </Link>
            </p>
          )}
        </GlassCard>

        {resultA && resultB && <CompareView a={resultA} b={resultB} />}
      </div>
    </motion.div>
  );
}
