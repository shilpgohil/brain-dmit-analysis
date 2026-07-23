"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { listSessions, deleteSession, reportDownloadUrl } from "@/lib/api";
import type { SessionListItem } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { relativeTime } from "@/lib/utils";
import { Fingerprint, Plus, Trash2, Download, RefreshCw, ChevronRight, AlertCircle, GitCompare } from "lucide-react";

const STATUS_COLOR: Record<string, string> = {
  completed: "#10b981",
  failed: "#f43f5e",
  pending: "#475569",
  preprocessing: "#00d4ff",
  extracting: "#00d4ff",
  mapping: "#8b5cf6",
  extending: "#8b5cf6",
  generating_report: "#f59e0b",
};

export default function SessionsPage() {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      setSessions(await listSessions(100));
      setError(null);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load sessions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this session?")) return;
    setDeletingId(id);
    try {
      await deleteSession(id);
      setSessions((p) => p.filter((s) => s.id !== id));
    } catch {
      alert("Failed to delete.");
    } finally {
      setDeletingId(null);
    }
  };

  const completed = sessions.filter((s) => s.status === "completed").length;
  const inProgress = sessions.filter((s) => !["completed", "failed", "pending"].includes(s.status)).length;

  return (
    <div className="min-h-screen pb-24">
      {/* Header */}
      <div className="relative overflow-hidden border-b border-white/[0.04] py-12 px-6">
        <div className="absolute inset-0 opacity-40">
          <FingerprintField opacity={0.05} animated={false} color="139, 92, 246" />
        </div>
        <div className="absolute inset-0"
          style={{ background: "linear-gradient(to bottom, transparent, rgba(2,2,8,0.9))" }} />
        <div className="relative z-10 max-w-5xl mx-auto">
          <motion.div
            className="flex items-end justify-between"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          >
            <div>
              <p className="text-xs text-violet-400 tracking-widest uppercase font-mono mb-2">
                Archive
              </p>
              <h1 className="text-display-section text-white">
                Analysis Sessions
              </h1>
              <p className="text-white/30 mt-1.5 text-sm">
                {sessions.length} total · {completed} completed · {inProgress} in progress
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Link href="/compare">
                <MagneticButton variant="ghost" size="sm" icon={<GitCompare className="w-3.5 h-3.5" />}>
                  Compare
                </MagneticButton>
              </Link>
              <MagneticButton variant="ghost" size="sm" onClick={load} icon={<RefreshCw className="w-3.5 h-3.5" />}>
                Refresh
              </MagneticButton>
              <Link href="/analysis/new">
                <MagneticButton size="sm" icon={<Plus className="w-3.5 h-3.5" />}>
                  New Analysis
                </MagneticButton>
              </Link>
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 pt-8">
        {/* Error */}
        {error && (
          <motion.div
            className="flex items-start gap-2 p-4 rounded-xl mb-6"
            style={{ background: "rgba(244,63,94,0.06)", border: "1px solid rgba(244,63,94,0.2)" }}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          >
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-rose-400">{error}</p>
          </motion.div>
        )}

        {/* Sessions list */}
        {loading ? (
          <div className="flex items-center justify-center py-24 text-white/20 text-sm">
            Loading sessions...
          </div>
        ) : sessions.length === 0 ? (
          <GlassCard padding="lg" gradient className="flex flex-col items-center py-20 text-center">
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4"
              style={{ background: "rgba(139,92,246,0.08)", border: "1px solid rgba(139,92,246,0.15)" }}
            >
              <Fingerprint className="w-8 h-8 opacity-30" style={{ color: "#8b5cf6" }} strokeWidth={1} />
            </div>
            <p className="text-white/40 font-medium mb-1">No sessions recorded</p>
            <p className="text-sm text-white/20 mb-6">Start your first biometric analysis.</p>
            <Link href="/analysis/new">
              <MagneticButton size="sm" icon={<Plus className="w-3.5 h-3.5" />}>
                Start Analysis
              </MagneticButton>
            </Link>
          </GlassCard>
        ) : (
          <div className="space-y-2">
            {sessions.map((session, i) => {
              const color = STATUS_COLOR[session.status] ?? "#475569";
              return (
                <motion.div
                  key={session.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: i * 0.03, ease: [0.16, 1, 0.3, 1] }}
                >
                  <div
                    className="flex items-center gap-4 px-5 py-4 rounded-2xl group transition-all duration-300 hover:bg-white/[0.03]"
                    style={{ border: "1px solid rgba(255,255,255,0.05)" }}
                  >
                    {/* Icon */}
                    <div
                      className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-300 group-hover:scale-105"
                      style={{ background: `${color}12`, border: `1px solid ${color}25` }}
                    >
                      <Fingerprint className="w-5 h-5" style={{ color }} strokeWidth={1.5} />
                    </div>

                    {/* Name + meta */}
                    <Link href={`/analysis/${session.id}`} className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white/70 group-hover:text-white transition-colors truncate">
                        {session.subject_name ?? "Anonymous Subject"}
                      </p>
                      <p className="text-[11px] text-white/20 font-mono mt-0.5">
                        {session.id.slice(0, 8)}… · {session.finger_count} prints · {relativeTime(session.created_at)}
                      </p>
                    </Link>

                    {/* Status */}
                    <span
                      className="text-[9px] font-mono uppercase tracking-wide px-2 py-1 rounded-full flex-shrink-0"
                      style={{ color, background: `${color}15` }}
                    >
                      {session.status}
                    </span>

                    {/* Actions */}
                    <div className="flex items-center gap-1 flex-shrink-0">
                      {session.has_report && (
                        <a
                          href={reportDownloadUrl(session.id)}
                          target="_blank"
                          rel="noopener noreferrer"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <button
                            className="w-8 h-8 rounded-lg flex items-center justify-center text-white/20 hover:text-[#00d4ff] hover:bg-[#00d4ff10] transition-all"
                          >
                            <Download className="w-3.5 h-3.5" />
                          </button>
                        </a>
                      )}
                      <Link href={`/analysis/${session.id}`}>
                        <button className="w-8 h-8 rounded-lg flex items-center justify-center text-white/20 hover:text-white/60 transition-all group-hover:translate-x-0.5">
                          <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                      </Link>
                      <button
                        onClick={() => handleDelete(session.id)}
                        disabled={deletingId === session.id}
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-white/10 hover:text-rose-400 hover:bg-rose-950/30 transition-all"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
