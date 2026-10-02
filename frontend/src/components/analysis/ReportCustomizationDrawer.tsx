"use client";

import { useState, useEffect, useCallback } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Sliders,
  Sparkles,
  Save,
  Download,
  Loader2,
  CheckCircle2,
  Building2,
  UserCheck,
  FileText,
  MessageSquareQuote,
  RotateCcw,
  Cloud,
  Database,
  ShieldCheck,
  PenTool,
} from "lucide-react";
import { GOLD } from "@/lib/analysis-theme";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { SignaturePad } from "@/components/ui/SignaturePad";
import {
  getReportCustomization,
  generateReport,
  downloadReport,
  getReportStorageStatus,
  type ReportCustomization,
  type ReportStorageStatus,
} from "@/lib/api";

interface ReportCustomizationDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: string;
  subjectName?: string | null;
  onSuccess?: () => void;
}

const DEFAULT_NOTES =
  "Candidate demonstrates exceptional intellectual maturity and focused self-direction. Recommended for advanced STEM curriculum with supplementary leadership and debate opportunities. Scheduled 6-month progress review confirmed.";

const DEFAULT_COMMENTS =
  "The assessment provided remarkably accurate insights into my innate learning and working style. The career alignment roadmap validated my inclination toward strategic systems engineering.";

export function ReportCustomizationDrawer({
  isOpen,
  onClose,
  sessionId,
  subjectName,
  onSuccess,
}: ReportCustomizationDrawerProps) {
  const [mounted, setMounted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [storageInfo, setStorageInfo] = useState<ReportStorageStatus | null>(null);

  const [form, setForm] = useState<ReportCustomization>({
    analyst_name: "Prof. Shilp Gohil, Ph.D.",
    analyst_title: "Senior Biometric Profiler & Cognitive Development Consultant",
    analyst_id: "IADP-89241-SR",
    school_name: "Apex Global Academy",
    counselor_notes: DEFAULT_NOTES,
    participant_comments: DEFAULT_COMMENTS,
    candidate_signature: undefined,
    counselor_signature: undefined,
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const loadCurrentSettings = useCallback(async () => {
    if (!sessionId) return;
    setLoading(true);
    setError(null);
    try {
      const [customData, storageData] = await Promise.allSettled([
        getReportCustomization(sessionId),
        getReportStorageStatus(sessionId),
      ]);

      if (customData.status === "fulfilled") {
        const data = customData.value;
        setForm({
          analyst_name: data.analyst_name || "Prof. Shilp Gohil, Ph.D.",
          analyst_title:
            data.analyst_title ||
            "Senior Biometric Profiler & Cognitive Development Consultant",
          analyst_id: data.analyst_id || "IADP-89241-SR",
          school_name: data.school_name || "Apex Global Academy",
          counselor_notes: data.counselor_notes || DEFAULT_NOTES,
          participant_comments: data.participant_comments || DEFAULT_COMMENTS,
          candidate_signature: data.candidate_signature,
          counselor_signature: data.counselor_signature,
        });
      }

      if (storageData.status === "fulfilled") {
        setStorageInfo(storageData.value);
      }
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      window.dispatchEvent(new CustomEvent("lenis:stop"));
      loadCurrentSettings();
      setSavedSuccess(false);
    } else {
      document.body.style.overflow = "";
      window.dispatchEvent(new CustomEvent("lenis:start"));
    }
    return () => {
      document.body.style.overflow = "";
      window.dispatchEvent(new CustomEvent("lenis:start"));
    };
  }, [isOpen, loadCurrentSettings]);

  const handleSaveAndRecompile = async (autoDownload = false) => {
    setSaving(true);
    setError(null);
    setSavedSuccess(false);
    try {
      await generateReport(sessionId, form);
      setSavedSuccess(true);
      if (onSuccess) onSuccess();
      if (autoDownload) {
        await downloadReport(sessionId, subjectName);
      }
      try {
        const freshStorage = await getReportStorageStatus(sessionId);
        setStorageInfo(freshStorage);
      } catch {
        // Non-blocking
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Recompilation failed");
    } finally {
      setSaving(false);
    }
  };

  const handleResetDefaults = () => {
    setForm({
      analyst_name: "Prof. Shilp Gohil, Ph.D.",
      analyst_title: "Senior Biometric Profiler & Cognitive Development Consultant",
      analyst_id: "IADP-89241-SR",
      school_name: "Apex Global Academy",
      counselor_notes: DEFAULT_NOTES,
      participant_comments: DEFAULT_COMMENTS,
      candidate_signature: undefined,
      counselor_signature: undefined,
    });
  };

  if (!mounted) return null;

  const drawerContent = (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop — High z-index above CinematicNav and DossierViewerModal */}
          <motion.div
            className="fixed inset-0 z-[105] bg-black/80 backdrop-blur-md"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Slide-out Panel */}
          <motion.div
            className="fixed right-0 top-0 bottom-0 z-[110] flex flex-col w-full sm:max-w-[580px] shadow-2xl bg-[#030712] border-l border-[#D4AF37]/25 text-white overscroll-contain"
            data-lenis-prevent="true"
            initial={{ x: "100%", opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: "100%", opacity: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          >
            {/* Header — Strict Height and Contrast */}
            <div className="h-16 px-4 sm:px-6 bg-[#0B0F19] border-b border-white/[0.08] flex items-center justify-between flex-shrink-0 z-10">
              <div className="flex items-center gap-3 min-w-0">
                <div
                  className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{
                    background: "rgba(212, 175, 55, 0.15)",
                    border: "1px solid rgba(212, 175, 55, 0.35)",
                  }}
                >
                  <Sliders className="w-4 h-4 text-[#D4AF37]" />
                </div>
                <div className="truncate">
                  <h2 className="text-sm font-semibold text-white tracking-wide truncate">
                    Dossier Customization &amp; Sign-Off
                  </h2>
                  <p className="text-[11px] text-white/40 font-mono truncate">
                    Candidate: <span className="text-white/70">{subjectName || "Subject Record"}</span> &bull; 64-Page Assembly
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-1.5 flex-shrink-0">
                <button
                  type="button"
                  onClick={handleResetDefaults}
                  className="p-2 rounded-xl text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors"
                  title="Reset Default Values"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={onClose}
                  className="p-2 rounded-xl text-white/50 hover:text-white hover:bg-white/[0.08] transition-colors"
                  title="Close"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Storage Info Banner */}
            {storageInfo && (
              <div className="px-6 py-2 bg-white/[0.02] border-b border-white/[0.06] flex items-center justify-between text-[10px] font-mono text-white/40 flex-shrink-0">
                <span className="flex items-center gap-1.5">
                  {storageInfo.storage.enabled ? (
                    <Cloud className="w-3.5 h-3.5 text-cyan-400" />
                  ) : (
                    <Database className="w-3.5 h-3.5 text-[#D4AF37]" />
                  )}
                  Storage: {storageInfo.storage.provider?.toUpperCase()}
                </span>
                <span className="flex items-center gap-1 text-emerald-400">
                  <ShieldCheck className="w-3 h-3" />
                  Verified 64 Pages
                </span>
              </div>
            )}

            {/* Scrollable Form Body — Plenty of bottom padding for sticky bar */}
            <div
              className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 pb-44 space-y-6 scrollbar-thin scrollbar-thumb-white/10 overscroll-contain"
              data-lenis-prevent="true"
            >
              {loading ? (
                <div className="py-24 flex flex-col items-center justify-center gap-2 text-white/40 text-xs">
                  <Loader2 className="w-6 h-6 animate-spin text-[#D4AF37]" />
                  <span>Loading customization parameters...</span>
                </div>
              ) : (
                <>
                  {error && (
                    <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/25 text-rose-300 text-xs">
                      {error}
                    </div>
                  )}

                  {savedSuccess && (
                    <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-300 text-xs flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      <span>64-page dossier recompiled and saved successfully.</span>
                    </div>
                  )}

                  {/* Section 1: Profiler Credentials */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 pb-1.5 border-b border-white/[0.06]">
                      <UserCheck className="w-4 h-4 text-[#D4AF37]" />
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
                        1. Profiler Credentials (Page 2 &amp; Cover)
                      </h3>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <label className="block text-[11px] font-medium text-white/50 mb-1">
                          Lead Profiler Name &amp; Title
                        </label>
                        <input
                          type="text"
                          value={form.analyst_name || ""}
                          onChange={(e) =>
                            setForm((prev) => ({
                              ...prev,
                              analyst_name: e.target.value,
                            }))
                          }
                          placeholder="Prof. Shilp Gohil, Ph.D."
                          className="w-full h-10 px-3 text-xs text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors"
                        />
                      </div>

                      <div>
                        <label className="block text-[11px] font-medium text-white/50 mb-1">
                          Professional Designation / Role
                        </label>
                        <input
                          type="text"
                          value={form.analyst_title || ""}
                          onChange={(e) =>
                            setForm((prev) => ({
                              ...prev,
                              analyst_title: e.target.value,
                            }))
                          }
                          placeholder="Senior Biometric Profiler & Cognitive Development Consultant"
                          className="w-full h-10 px-3 text-xs text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors"
                        />
                      </div>

                      <div>
                        <label className="block text-[11px] font-medium text-white/50 mb-1">
                          Accreditation / Board Certification ID
                        </label>
                        <input
                          type="text"
                          value={form.analyst_id || ""}
                          onChange={(e) =>
                            setForm((prev) => ({
                              ...prev,
                              analyst_id: e.target.value,
                            }))
                          }
                          placeholder="IADP-89241-SR"
                          className="w-full h-10 px-3 text-xs font-mono text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Section 2: Institution */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 pb-1.5 border-b border-white/[0.06]">
                      <Building2 className="w-4 h-4 text-[#D4AF37]" />
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
                        2. Multi-Tenant Institution (Cover &amp; Page 3)
                      </h3>
                    </div>

                    <div>
                      <label className="block text-[11px] font-medium text-white/50 mb-1">
                        School / Partner Organization Name
                      </label>
                      <input
                        type="text"
                        value={form.school_name || ""}
                        onChange={(e) =>
                          setForm((prev) => ({
                            ...prev,
                            school_name: e.target.value,
                          }))
                        }
                        placeholder="Apex Global Academy"
                        className="w-full h-10 px-3 text-xs text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors"
                      />
                    </div>
                  </div>

                  {/* Section 3: Clinical Observations */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 pb-1.5 border-b border-white/[0.06]">
                      <FileText className="w-4 h-4 text-[#D4AF37]" />
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
                        3. Profiler Clinical Observations (Page 59)
                      </h3>
                    </div>

                    <div>
                      <label className="block text-[11px] font-medium text-white/50 mb-1">
                        Post-Assessment Consultation &amp; Strategic Roadmap Notes
                      </label>
                      <textarea
                        rows={4}
                        value={form.counselor_notes || ""}
                        onChange={(e) =>
                          setForm((prev) => ({
                            ...prev,
                            counselor_notes: e.target.value,
                          }))
                        }
                        placeholder="Enter personalized roadmap notes, developmental recommendations, and review schedules..."
                        className="w-full p-3 text-xs text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors leading-relaxed"
                      />
                    </div>
                  </div>

                  {/* Section 4: Participant Reflections */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 pb-1.5 border-b border-white/[0.06]">
                      <MessageSquareQuote className="w-4 h-4 text-[#D4AF37]" />
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
                        4. Participant Reflections &amp; Feedback (Page 60)
                      </h3>
                    </div>

                    <div>
                      <label className="block text-[11px] font-medium text-white/50 mb-1">
                        Participant / Guardian Written Feedback
                      </label>
                      <textarea
                        rows={3}
                        value={form.participant_comments || ""}
                        onChange={(e) =>
                          setForm((prev) => ({
                            ...prev,
                            participant_comments: e.target.value,
                          }))
                        }
                        placeholder="Enter participant feedback and reflection remarks..."
                        className="w-full p-3 text-xs text-white bg-white/[0.03] border border-white/[0.08] rounded-xl focus:outline-none focus:border-[#D4AF37]/60 transition-colors leading-relaxed"
                      />
                    </div>
                  </div>

                  {/* Section 5: Digital Signatures */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 pb-1.5 border-b border-white/[0.06]">
                      <PenTool className="w-4 h-4 text-[#D4AF37]" />
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-white/80">
                        5. Digital Signatures (Page 60 Execution)
                      </h3>
                    </div>

                    <div className="space-y-4">
                      <SignaturePad
                        label="Lead Profiler Digital Signature"
                        subtitle="Applied directly above certified consultant title on Page 60"
                        value={form.counselor_signature}
                        onChange={(val) =>
                          setForm((prev) => ({
                            ...prev,
                            counselor_signature: val,
                          }))
                        }
                      />

                      <SignaturePad
                        label="Candidate / Legal Guardian Digital Signature"
                        subtitle="Applied directly above candidate verification line on Page 60"
                        value={form.candidate_signature}
                        onChange={(val) =>
                          setForm((prev) => ({
                            ...prev,
                            candidate_signature: val,
                          }))
                        }
                      />
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Sticky Action Footer */}
            <div className="min-h-16 py-3 px-4 sm:px-6 flex-shrink-0 flex items-center justify-between gap-2 bg-[#0B0F19]/95 border-t border-white/[0.08] backdrop-blur-xl z-20 shadow-2xl">
              <MagneticButton
                variant="ghost"
                size="sm"
                onClick={onClose}
                disabled={saving}
              >
                Cancel
              </MagneticButton>

              <div className="flex items-center gap-2">
                <MagneticButton
                  variant="secondary"
                  size="sm"
                  disabled={saving || loading}
                  onClick={() => handleSaveAndRecompile(false)}
                  icon={
                    saving ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Save className="w-3.5 h-3.5" />
                    )
                  }
                >
                  <span className="hidden sm:inline">{saving ? "Recompiling..." : "Save & Recompile"}</span>
                  <span className="sm:hidden">{saving ? "Saving..." : "Save"}</span>
                </MagneticButton>

                <MagneticButton
                  size="sm"
                  disabled={saving || loading}
                  onClick={() => handleSaveAndRecompile(true)}
                  icon={
                    saving ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Download className="w-3.5 h-3.5" />
                    )
                  }
                >
                  <span className="hidden sm:inline">{saving ? "Compiling PDF..." : "Recompile & Download"}</span>
                  <span className="sm:hidden">{saving ? "Compiling..." : "Download"}</span>
                </MagneticButton>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );

  return createPortal(drawerContent, document.body);
}
