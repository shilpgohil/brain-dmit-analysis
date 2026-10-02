"use client";

import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Download,
  Printer,
  Sliders,
  Maximize2,
  Minimize2,
  ChevronLeft,
  ChevronRight,
  BookOpen,
  Cloud,
  Database,
  ShieldCheck,
  Loader2,
  AlertCircle,
  RefreshCw,
  Menu,
} from "lucide-react";
import { MagneticButton } from "@/components/ui/MagneticButton";
import {
  fetchReportPdfBlobUrl,
  downloadReport,
  getReportStorageStatus,
  type ReportStorageStatus,
} from "@/lib/api";
import { cn } from "@/lib/utils";

interface DossierViewerModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: string;
  subjectName?: string | null;
  onOpenCustomizer?: () => void;
  refreshKey?: number | string;
}

const DOSSIER_SECTIONS = [
  { id: 1, title: "1. Cover & Profiler Credentials", page: 1, range: "P 1–6" },
  { id: 2, title: "2. Candidate Bio & Legal Plaque", page: 7, range: "P 7" },
  { id: 3, title: "3. Scientific Dermatoglyphics", page: 8, range: "P 8–10" },
  { id: 4, title: "4. SWOT Personality Quadrants", page: 11, range: "P 11–15" },
  { id: 5, title: "5. Brain Lobe Capacity (Table 1.1)", page: 16, range: "P 16" },
  { id: 6, title: "6. Subject Aptitude & 10 Quotients", page: 17, range: "P 17–19" },
  { id: 7, title: "7. Academic & Co-Curricular Guidance", page: 20, range: "P 20–22" },
  { id: 8, title: "8. Learning Modality (VAK) & Habits", page: 23, range: "P 23–34" },
  { id: 9, title: "9. 8 Corporate Competencies", page: 35, range: "P 35–42" },
  { id: 10, title: "10. 14 Sector Career Compatibility", page: 43, range: "P 43–58" },
  { id: 11, title: "11. Action Plan & Verification Sign-Off", page: 59, range: "P 59–60" },
  { id: 12, title: "12. Institutional Biometric Appendix", page: 61, range: "P 61–64" },
];

export function DossierViewerModal({
  isOpen,
  onClose,
  sessionId,
  subjectName,
  onOpenCustomizer,
  refreshKey,
}: DossierViewerModalProps) {
  const [mounted, setMounted] = useState(false);
  const [activePage, setActivePage] = useState<number>(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [mobileTocOpen, setMobileTocOpen] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [loadingPdf, setLoadingPdf] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [pdfBlobUrl, setPdfBlobUrl] = useState<string | null>(null);
  const [storageStatus, setStorageStatus] = useState<ReportStorageStatus | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const loadDossierBlob = async () => {
    if (!sessionId) return;
    setLoadingPdf(true);
    setLoadError(null);
    try {
      const url = await fetchReportPdfBlobUrl(sessionId);
      setPdfBlobUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return url;
      });
    } catch (err: unknown) {
      setLoadError(err instanceof Error ? err.message : "Failed to load master dossier");
    } finally {
      setLoadingPdf(false);
    }
  };

  useEffect(() => {
    if (isOpen && sessionId) {
      document.body.style.overflow = "hidden";
      window.dispatchEvent(new CustomEvent("lenis:stop"));
      loadDossierBlob();
      getReportStorageStatus(sessionId)
        .then(setStorageStatus)
        .catch(() => {});
    } else {
      document.body.style.overflow = "";
      window.dispatchEvent(new CustomEvent("lenis:start"));
    }
    return () => {
      document.body.style.overflow = "";
      window.dispatchEvent(new CustomEvent("lenis:start"));
    };
  }, [isOpen, sessionId, refreshKey]);

  useEffect(() => {
    return () => {
      if (pdfBlobUrl) {
        URL.revokeObjectURL(pdfBlobUrl);
      }
    };
  }, [pdfBlobUrl]);

  const handlePrint = () => {
    if (iframeRef.current && iframeRef.current.contentWindow) {
      iframeRef.current.contentWindow.print();
    } else if (pdfBlobUrl) {
      const w = window.open(pdfBlobUrl, "_blank");
      if (w) w.print();
    }
  };

  const handleDownload = async () => {
    setDownloading(true);
    try {
      await downloadReport(sessionId, subjectName);
    } catch {
      // Handled in api helper
    } finally {
      setDownloading(false);
    }
  };

  const handleJump = (page: number) => {
    setActivePage(page);
    setMobileTocOpen(false);
  };

  if (!mounted) return null;

  const modalContent = (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-[100] flex flex-col bg-[#020617] text-white select-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {/* Top Bar Navigation — Strict Height & No Collisions */}
          <header className="h-16 px-3 sm:px-6 bg-[#0B0F19] border-b border-white/[0.08] flex items-center justify-between flex-shrink-0 z-20 shadow-lg">
            <div className="flex items-center gap-2 sm:gap-3 min-w-0">
              <button
                type="button"
                onClick={() => setMobileTocOpen(!mobileTocOpen)}
                className="md:hidden p-2 rounded-xl text-[#D4AF37] hover:bg-white/[0.06] transition-colors flex-shrink-0"
                title="Toggle Table of Contents"
              >
                <BookOpen className="w-4 h-4" />
              </button>

              <div
                className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl items-center justify-center flex-shrink-0 hidden sm:flex"
                style={{
                  background: "rgba(212, 175, 55, 0.15)",
                  border: "1px solid rgba(212, 175, 55, 0.35)",
                }}
              >
                <BookOpen className="w-4 h-4 text-[#D4AF37]" />
              </div>

              <div className="truncate">
                <div className="flex items-center gap-2">
                  <h2 className="text-xs sm:text-sm font-semibold text-white tracking-wide truncate">
                    Master Dossier
                  </h2>
                  <span className="text-[9px] sm:text-[10px] font-mono px-1.5 sm:px-2 py-0.5 rounded-full bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30 flex-shrink-0">
                    64 Pages
                  </span>
                </div>
                <p className="text-[10px] sm:text-[11px] text-white/40 font-mono truncate">
                  <span className="text-white/70">{subjectName || "Candidate"}</span> &bull; {sessionId.slice(0, 8)}
                </p>
              </div>
            </div>

            {/* Page Stepper */}
            <div className="hidden sm:flex items-center gap-1 px-2 py-1 rounded-xl bg-white/[0.04] border border-white/[0.08] flex-shrink-0">
              <button
                type="button"
                onClick={() => handleJump(Math.max(1, activePage - 1))}
                disabled={activePage <= 1}
                className="p-1 rounded-lg text-white/50 hover:text-white disabled:opacity-30 transition-colors"
                title="Previous Page"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <span className="text-[11px] font-mono text-white/70 px-1.5 select-none">
                Page {activePage} / 64
              </span>
              <button
                type="button"
                onClick={() => handleJump(Math.min(64, activePage + 1))}
                disabled={activePage >= 64}
                className="p-1 rounded-lg text-white/50 hover:text-white disabled:opacity-30 transition-colors"
                title="Next Page"
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Storage status pill (desktop) */}
            {storageStatus && (
              <div className="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.07] text-[10px] font-mono text-white/60">
                {storageStatus.storage.enabled ? (
                  <Cloud className="w-3.5 h-3.5 text-cyan-400" />
                ) : (
                  <Database className="w-3.5 h-3.5 text-[#D4AF37]" />
                )}
                <span>{storageStatus.storage.provider?.toUpperCase()}</span>
                <span className="text-white/20">&bull;</span>
                <span className="text-emerald-400 flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" />
                  Verified 64p
                </span>
              </div>
            )}

            {/* Action buttons */}
            <div className="flex items-center gap-1.5 sm:gap-2 flex-shrink-0">
              {onOpenCustomizer && (
                <MagneticButton
                  variant="secondary"
                  size="sm"
                  onClick={onOpenCustomizer}
                  icon={<Sliders className="w-3.5 h-3.5 text-[#D4AF37]" />}
                >
                  <span className="hidden sm:inline">Customize &amp; Sign</span>
                  <span className="sm:hidden">Sign</span>
                </MagneticButton>
              )}

              <div className="hidden md:inline-flex">
                <MagneticButton
                  variant="ghost"
                  size="sm"
                  onClick={handlePrint}
                  icon={<Printer className="w-3.5 h-3.5" />}
                >
                  Print
                </MagneticButton>
              </div>

              <MagneticButton
                size="sm"
                onClick={handleDownload}
                disabled={downloading}
                icon={
                  downloading ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Download className="w-3.5 h-3.5" />
                  )
                }
              >
                <span className="hidden sm:inline">Download PDF</span>
                <span className="sm:hidden">PDF</span>
              </MagneticButton>

              <button
                type="button"
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="hidden sm:inline-flex p-2 rounded-xl text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors"
                title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
              >
                {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
              </button>

              <div className="h-6 w-[1px] bg-white/[0.1] mx-0.5 sm:mx-1" />

              <button
                type="button"
                onClick={onClose}
                className="p-2 rounded-xl text-white/50 hover:text-white hover:bg-white/[0.08] transition-colors"
                title="Close Viewer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </header>

          {/* Main Body */}
          <div className="flex-1 flex overflow-hidden relative" data-lenis-prevent="true">
            {/* Desktop Sidebar Bookmark Navigator */}
            <div
              className={cn(
                "w-72 border-r border-white/[0.08] flex-col overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 flex-shrink-0 overscroll-contain hidden md:flex",
                isFullscreen && "hidden"
              )}
              style={{ background: "#070B14" }}
              data-lenis-prevent="true"
            >
              <div className="px-4 py-3.5 border-b border-white/[0.06] text-[10px] font-mono uppercase tracking-[0.2em] text-[#D4AF37]/80">
                Master Table of Contents
              </div>

              <div className="p-2 space-y-1">
                {DOSSIER_SECTIONS.map((sec) => {
                  const isCurrent = activePage === sec.page;
                  return (
                    <button
                      key={sec.id}
                      type="button"
                      onClick={() => handleJump(sec.page)}
                      className={cn(
                        "w-full text-left px-3 py-2.5 rounded-xl text-xs transition-all flex items-center justify-between group",
                        isCurrent
                          ? "bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30 font-medium"
                          : "text-white/60 hover:text-white hover:bg-white/[0.04]"
                      )}
                    >
                      <span className="truncate pr-2">{sec.title}</span>
                      <span className="text-[10px] font-mono text-white/30 group-hover:text-white/60 flex-shrink-0">
                        {sec.range}
                      </span>
                    </button>
                  );
                })}
              </div>

              <div className="mt-auto p-4 border-t border-white/[0.06] text-[10px] text-white/30 font-mono space-y-1">
                <p>Engine: DMIT Core 3.2 Full</p>
                <p>Standard: 60 Client + 4 Technical</p>
              </div>
            </div>

            {/* Mobile Slide-Over Table of Contents */}
            {mobileTocOpen && (
              <>
                <div
                  className="md:hidden fixed inset-0 z-30 bg-black/70 backdrop-blur-sm"
                  onClick={() => setMobileTocOpen(false)}
                />
                <div
                  className="md:hidden absolute top-0 left-0 bottom-0 z-40 w-72 bg-[#070B14] border-r border-white/[0.08] flex flex-col overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 shadow-2xl overscroll-contain"
                  data-lenis-prevent="true"
                >
                  <div className="p-4 border-b border-white/[0.06] flex items-center justify-between text-[11px] font-mono uppercase tracking-[0.18em] text-[#D4AF37]">
                    <span>Table of Contents</span>
                    <button
                      type="button"
                      onClick={() => setMobileTocOpen(false)}
                      className="p-1 rounded-lg text-white/50 hover:text-white"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="p-2 space-y-1 flex-1">
                    {DOSSIER_SECTIONS.map((sec) => (
                      <button
                        key={sec.id}
                        type="button"
                        onClick={() => handleJump(sec.page)}
                        className={cn(
                          "w-full text-left px-3 py-2.5 rounded-xl text-xs transition-all flex items-center justify-between",
                          activePage === sec.page
                            ? "bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30 font-medium"
                            : "text-white/60 hover:text-white hover:bg-white/[0.04]"
                        )}
                      >
                        <span className="truncate pr-2">{sec.title}</span>
                        <span className="text-[10px] font-mono text-white/30">{sec.range}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* Center PDF Viewer */}
            <div
              className="flex-1 relative bg-[#0B0F19] flex flex-col items-center justify-center overflow-hidden overscroll-contain"
              data-lenis-prevent="true"
            >
              {loadingPdf ? (
                <div className="flex flex-col items-center justify-center gap-3 p-8">
                  <div className="w-12 h-12 rounded-2xl bg-[#D4AF37]/10 border border-[#D4AF37]/25 flex items-center justify-center">
                    <Loader2 className="w-6 h-6 animate-spin text-[#D4AF37]" />
                  </div>
                  <p className="text-xs text-white/60 font-mono tracking-wide">
                    Streaming 64-page authenticated master dossier...
                  </p>
                </div>
              ) : loadError ? (
                <div className="flex flex-col items-center justify-center gap-4 p-8 text-center max-w-md">
                  <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/25 flex items-center justify-center">
                    <AlertCircle className="w-6 h-6 text-rose-400" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white mb-1">Failed to Stream Dossier</h3>
                    <p className="text-xs text-white/40">{loadError}</p>
                  </div>
                  <button
                    type="button"
                    onClick={loadDossierBlob}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono bg-white/[0.06] hover:bg-white/[0.12] text-white transition-all"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    Retry Load
                  </button>
                </div>
              ) : pdfBlobUrl ? (
                <iframe
                  key={`pdf-frame-${sessionId}-page-${activePage}`}
                  ref={iframeRef}
                  src={`${pdfBlobUrl}#page=${activePage}&view=FitH`}
                  className="w-full h-full border-none"
                  title="DMIT Assessment Master Dossier"
                />
              ) : null}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );

  return createPortal(modalContent, document.body);
}
