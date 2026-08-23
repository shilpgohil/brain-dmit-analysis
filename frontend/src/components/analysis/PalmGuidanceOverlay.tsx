"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, Camera, Scan, Info } from "lucide-react";
import { PalmHandSvg } from "./PalmHandSvg";
import type { PalmGuidanceInfo } from "@/lib/finger-guidance";
import { cn } from "@/lib/utils";

interface PalmGuidanceOverlayProps {
  open: boolean;
  info: PalmGuidanceInfo | null;
  onClose: () => void;
  onContinue: () => void;
}

export function PalmGuidanceOverlay({
  open,
  info,
  onClose,
  onContinue,
}: PalmGuidanceOverlayProps) {
  return (
    <AnimatePresence>
      {open && info && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Backdrop */}
          <button
            type="button"
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            aria-label="Close guidance"
            onClick={onClose}
          />

          <motion.div
            role="dialog"
            aria-labelledby="palm-guidance-title"
            className={cn(
              "relative w-full max-w-lg rounded-2xl p-6",
              "border border-[rgba(157,139,181,0.35)]",
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

            {/* Header */}
            <p className="text-[10px] font-mono uppercase tracking-widest text-[#9d8bb5]/80 mb-1">
              Palm capture guidance
            </p>
            <h2 id="palm-guidance-title" className="font-serif-display text-xl text-[#e8dcc8]">
              {info.label}
            </h2>
            <p className="text-[10px] text-white/30 font-mono mt-0.5">
              ATD Angle Analysis · Processing Speed
            </p>

            {/* Palm SVG + ATD legend */}
            <div className="flex gap-4 items-start my-5">
              <div className="flex-shrink-0 h-[160px] w-[140px]">
                <PalmHandSvg info={info} className="w-full h-full" />
              </div>
              <div className="flex-1 space-y-2.5 text-[11px] text-white/40 mt-1">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full border border-[#00d4ff] flex-shrink-0" />
                  <span><span className="text-[#00d4ff] font-mono">a-point</span> — triradius below index finger</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full border border-[#c4a574] flex-shrink-0" />
                  <span><span className="text-[#c4a574] font-mono">t-point</span> — triradius at palm center</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full border border-[#9d8bb5] flex-shrink-0" />
                  <span><span className="text-[#9d8bb5] font-mono">d-point</span> — triradius below little finger</span>
                </div>
                <p className="text-[10px] text-white/25 mt-2 leading-relaxed">
                  The angle between these three points reflects neurological processing speed and fine-motor capacity.
                </p>
              </div>
            </div>

            {/* Tips */}
            <div className="space-y-2.5 text-sm text-white/50 leading-relaxed">
              <div className="flex gap-2">
                <Camera className="w-4 h-4 text-[#00d4ff] flex-shrink-0 mt-0.5" />
                <p>{info.placementTip}</p>
              </div>
              <div className="flex gap-2">
                <Scan className="w-4 h-4 text-[#c4a574] flex-shrink-0 mt-0.5" />
                <p>{info.scannerTip}</p>
              </div>
              <div className="flex gap-2">
                <Info className="w-4 h-4 text-[#9d8bb5] flex-shrink-0 mt-0.5" />
                <p>{info.atdTip}</p>
              </div>
            </div>

            {/* Actions */}
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
                className="flex-1 py-2.5 rounded-xl text-xs font-mono text-[#e8dcc8] border border-[rgba(157,139,181,0.35)] bg-[rgba(157,139,181,0.10)] hover:bg-[rgba(157,139,181,0.20)] transition-colors"
              >
                Choose palm image
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
