"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, Upload, Scan } from "lucide-react";
import { FingerHandSvg } from "./FingerHandSvg";
import type { FingerGuidanceInfo } from "@/lib/finger-guidance";
import { cn } from "@/lib/utils";

interface FingerGuidanceOverlayProps {
  open: boolean;
  info: FingerGuidanceInfo | null;
  onClose: () => void;
  onContinue: () => void;
  showContinueLabel?: string;
}

export function FingerGuidanceOverlay({
  open,
  info,
  onClose,
  onContinue,
  showContinueLabel = "Choose image",
}: FingerGuidanceOverlayProps) {
  return (
    <AnimatePresence>
      {open && info && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <button
            type="button"
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            aria-label="Close guidance"
            onClick={onClose}
          />
          <motion.div
            role="dialog"
            aria-labelledby="finger-guidance-title"
            className={cn(
              "relative w-full max-w-md rounded-2xl p-6",
              "border border-[rgba(196,165,116,0.28)]",
              "bg-gradient-to-b from-[#12121f] to-[#080818]"
            )}
            initial={{ scale: 0.94, y: 12 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.96, y: 8 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
          >
            <button
              type="button"
              onClick={onClose}
              className="absolute top-4 right-4 text-white/30 hover:text-white/70 transition-colors"
              aria-label="Close"
            >
              <X className="w-4 h-4" />
            </button>

            <p className="text-[10px] font-mono uppercase tracking-widest text-[#c4a574]/80 mb-1">
              Capture guidance
            </p>
            <h2 id="finger-guidance-title" className="font-serif-display text-xl text-[#e8dcc8]">
              {info.label}
            </h2>
            <p className="text-xs text-white/35 font-mono mt-1">Slot {info.slotId}</p>

            <div className="flex justify-center my-5 h-[180px]">
              <FingerHandSvg info={info} className="w-full max-w-[200px] h-full" />
            </div>

            <div className="space-y-3 text-sm text-white/55 leading-relaxed">
              <div className="flex gap-2">
                <Upload className="w-4 h-4 text-[#00d4ff] flex-shrink-0 mt-0.5" />
                <p>{info.placementTip}</p>
              </div>
              <div className="flex gap-2">
                <Scan className="w-4 h-4 text-[#c4a574] flex-shrink-0 mt-0.5" />
                <p>{info.scannerTip}</p>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 py-2.5 rounded-xl text-xs font-mono text-white/40 border border-white/[0.08] hover:bg-white/[0.04] transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={onContinue}
                className="flex-1 py-2.5 rounded-xl text-xs font-mono text-[#e8dcc8] border border-[rgba(196,165,116,0.35)] bg-[rgba(196,165,116,0.12)] hover:bg-[rgba(196,165,116,0.2)] transition-colors"
              >
                {showContinueLabel}
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
