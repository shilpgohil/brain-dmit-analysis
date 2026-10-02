"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { listSessions, deleteSession, downloadReport, exportBatchZip } from "@/lib/api";
import type { SessionListItem } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { relativeTime } from "@/lib/utils";
import {
  Fingerprint,
  Plus,
  Trash2,
  Download,
  RefreshCw,
  ChevronRight,
  AlertCircle,
  GitCompare,
  BookOpen,
  Loader2,
  CheckSquare,
  Square,
  FileArchive,
  X,
  Layers,
} from "lucide-react";
import { DossierViewerModal } from "@/components/analysis/DossierViewerModal";
import { ReportCustomizationDrawer } from "@/components/analysis/ReportCustomizationDrawer";
import { useAuthGuard } from "@/hooks/useAuthGuard";

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
  const { user, isLoading } = useAuthGuard("partner");
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);
  const [selectedViewerSession, setSelectedViewerSession] = useState<{ id: string; name?: string | null } | null>(null);
  const [selectedCustomizerSession, setSelectedCustomizerSession] = useState<{ id: string; name?: string | null } | null>(null);
  const [dossierRevision, setDossierRevision] = useState(0);

  // Batch cohort selection
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [isExportingZip, setIsExportingZip] = useState(false);

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

  useEffect(() => {
    if (user) load();
  }, [user]);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this session?")) return;
    setDeletingId(id);
    try {
      await deleteSession(id);
      setSessions((p) => p.filter((s) => s.id !== id));
      setSelectedIds((p) => {
        const next = new Set(p);
        next.delete(id);
        return next;
      });
    } catch {
      alert("Failed to delete.");
    } finally {
      setDeletingId(null);
    }
  };

  const handleDownload = async (id: string, subjectName?: string | null) => {
    setDownloadingId(id);
    try {
      await downloadReport(id, subjectName);
    } catch {
      alert("Report download failed. Please try again.");
    } finally {
      setDownloadingId(null);
    }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const completedSessions = sessions.filter((s) => s.status === "completed" || s.has_report);
  const isAllCompletedSelected =
    completedSessions.length > 0 && completedSessions.every((s) => selectedIds.has(s.id));

  const toggleSelectAllCompleted = () => {
    if (isAllCompletedSelected) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(completedSessions.map((s) => s.id)));
    }
  };

  const handleBatchExport = async () => {
    if (selectedIds.size === 0) return;
    setIsExportingZip(true);
    try {
      await exportBatchZip(Array.from(selectedIds));
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Batch export failed.");
    } finally {
      setIsExportingZip(false);
    }
  };

  const completed = sessions.filter((s) => s.status === "completed").length;
  const inProgress = sessions.filter((s) => !["completed", "failed", "pending"].includes(s.status)).length;

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-7 h-7 animate-spin text-[#c4a574]" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-28">
      {/* Header */}
      <div className="relative overflow-hidden border-b border-white/[0.04] py-12 px-6">
        <div className="absolute inset-0 opacity-40">
          <FingerprintField opacity={0.05} animated={false} color="139, 92, 246" />
        </div>
        <div
          className="absolute inset-0"
          style={{ background: "linear-gradient(to bottom, transparent, rgba(2,2,8,0.9))" }}
        />
        <div className="relative z-10 max-w-5xl mx-auto">
          <motion.div
            className="flex flex-col sm:flex-row sm:items-end justify-between gap-4"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          >
            <div>
              <p className="text-xs text-violet-400 tracking-widest uppercase font-mono mb-2">
                Archive & Cohorts
              </p>
              <h1 className="text-display-section text-white">Analysis Sessions</h1>
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
              <MagneticButton
                variant="ghost"
                size="sm"
                onClick={load}
                icon={<RefreshCw className="w-3.5 h-3.5" />}
              >
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
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-rose-400">{error}</p>
          </motion.div>
        )}

        {/* Action bar for cohort batch controls */}
        {completedSessions.length > 0 && !loading && (
          <div className="flex items-center justify-between gap-4 mb-4 px-2">
            <button
              type="button"
              onClick={toggleSelectAllCompleted}
              className="flex items-center gap-2 text-xs font-mono text-white/50 hover:text-white transition-colors"
            >
              {isAllCompletedSelected ? (
                <CheckSquare className="w-4 h-4 text-[#D4AF37]" />
              ) : (
                <Square className="w-4 h-4 text-white/30" />
              )}
              <span>
                {isAllCompletedSelected ? "Deselect All Cohort" : `Select All Completed (${completedSessions.length})`}
              </span>
            </button>

            {selectedIds.size > 0 && (
              <span className="text-xs font-mono text-[#D4AF37]">
                {selectedIds.size} session{selectedIds.size > 1 ? "s" : ""} selected
              </span>
            )}
          </div>
        )}

        {/* Sessions list */}
        {loading ? (
          <div className="flex items-center justify-center py-24 text-white/20 text-sm gap-2">
            <Loader2 className="w-4 h-4 animate-spin text-white/40" />
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
              const isSelected = selectedIds.has(session.id);
              const isCompleted = session.status === "completed" || session.has_report;

              return (
                <motion.div
                  key={session.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: i * 0.03, ease: [0.16, 1, 0.3, 1] }}
                >
                  <div
                    className={`flex items-center gap-3 sm:gap-4 px-4 sm:px-5 py-4 rounded-2xl group transition-all duration-300 ${
                      isSelected
                        ? "bg-[#D4AF37]/[0.06] border-[#D4AF37]/30"
                        : "hover:bg-white/[0.03] border-white/[0.05]"
                    }`}
                    style={{ border: `1px solid ${isSelected ? "rgba(212,175,55,0.35)" : "rgba(255,255,255,0.05)"}` }}
                  >
                    {/* Multi-select Checkbox */}
                    <button
                      type="button"
                      onClick={() => toggleSelect(session.id)}
                      className="p-1 rounded-lg text-white/30 hover:text-white transition-colors"
                      title={isSelected ? "Deselect" : "Select for Cohort ZIP export"}
                    >
                      {isSelected ? (
                        <CheckSquare className="w-4 h-4 text-[#D4AF37]" />
                      ) : (
                        <Square className="w-4 h-4 text-white/25 hover:text-white/50" />
                      )}
                    </button>

                    {/* Biometric Icon */}
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
                    {isCompleted && (
                      <span
                        className="text-[8px] font-mono uppercase tracking-wide px-2 py-1 rounded-full flex-shrink-0 hidden sm:inline"
                        style={{
                          color: "#10b981",
                          background: "rgba(16,185,129,0.1)",
                          border: "1px solid rgba(16,185,129,0.2)",
                        }}
                      >
                        Dossier Ready
                      </span>
                    )}

                    {/* Actions */}
                    <div className="flex items-center gap-1 flex-shrink-0">
                      {isCompleted && (
                        <>
                          <button
                            type="button"
                            title="View 64-page master dossier"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedViewerSession({ id: session.id, name: session.subject_name });
                            }}
                            className="w-8 h-8 rounded-lg flex items-center justify-center text-white/40 hover:text-[#D4AF37] hover:bg-[#D4AF37]/10 transition-all"
                          >
                            <BookOpen className="w-3.5 h-3.5" />
                          </button>
                          <button
                            type="button"
                            title="Download 64-page dossier"
                            disabled={downloadingId === session.id}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDownload(session.id, session.subject_name);
                            }}
                            className="w-8 h-8 rounded-lg flex items-center justify-center text-white/20 hover:text-[#00d4ff] hover:bg-[#00d4ff10] transition-all disabled:opacity-40"
                          >
                            {downloadingId === session.id ? (
                              <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            ) : (
                              <Download className="w-3.5 h-3.5" />
                            )}
                          </button>
                        </>
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

      {/* Floating Cohort Batch Export Bar */}
      <AnimatePresence>
        {selectedIds.size > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 max-w-xl w-[92%] sm:w-auto"
          >
            <div
              className="flex items-center justify-between gap-4 sm:gap-6 px-5 py-3 rounded-2xl shadow-2xl backdrop-blur-2xl"
              style={{
                background: "rgba(11, 15, 25, 0.92)",
                border: "1px solid rgba(212, 175, 55, 0.35)",
                boxShadow: "0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(212,175,55,0.15)",
              }}
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-[#D4AF37]/15 border border-[#D4AF37]/30 flex items-center justify-center text-[#D4AF37]">
                  <Layers className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs font-mono font-medium text-white">
                    {selectedIds.size} Candidate Dossier{selectedIds.size > 1 ? "s" : ""} Selected
                  </p>
                  <p className="text-[10px] text-white/35">Batch export as unified cohort ZIP archive</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedIds(new Set())}
                  className="p-1.5 rounded-lg text-white/30 hover:text-white/70 hover:bg-white/[0.05] transition-all"
                  title="Clear selection"
                >
                  <X className="w-4 h-4" />
                </button>
                <MagneticButton
                  size="sm"
                  onClick={handleBatchExport}
                  disabled={isExportingZip}
                  icon={
                    isExportingZip ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <FileArchive className="w-3.5 h-3.5 text-[#030712]" />
                    )
                  }
                >
                  {isExportingZip ? "Synthesizing Archive..." : "Export Cohort ZIP"}
                </MagneticButton>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 64-Page Dossier Streaming Modal */}
      {selectedViewerSession && (
        <DossierViewerModal
          isOpen={true}
          onClose={() => setSelectedViewerSession(null)}
          sessionId={selectedViewerSession.id}
          subjectName={selectedViewerSession.name}
          refreshKey={dossierRevision}
          onOpenCustomizer={() => {
            setSelectedCustomizerSession({
              id: selectedViewerSession.id,
              name: selectedViewerSession.name,
            });
          }}
        />
      )}

      {/* Dossier Customization Drawer */}
      {selectedCustomizerSession && (
        <ReportCustomizationDrawer
          isOpen={true}
          onClose={() => setSelectedCustomizerSession(null)}
          sessionId={selectedCustomizerSession.id}
          subjectName={selectedCustomizerSession.name}
          onSuccess={() => {
            load();
            setDossierRevision((prev) => prev + 1);
          }}
        />
      )}
    </div>
  );
}
