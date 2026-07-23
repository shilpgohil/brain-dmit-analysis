"use client";

import { motion } from "framer-motion";
import { Hand } from "lucide-react";
import type { AtdAnalysis, AtdHand, PalmCapture } from "@/lib/types";
import { GOLD, PLUM, scoreToGoldTier } from "@/lib/analysis-theme";
import { mediaUrl } from "@/lib/api";

const RANGE_LABEL: Record<string, string> = {
  "<=35": "≤ 35° — fast, sensitive, nimble",
  "36-40": "36–40° — optimal fine-motor control",
  "41-45": "41–45° — needs staged repetition",
  "45+": "45°+ — slower, gross-motor oriented",
};

function HandCard({ side, hand, hemisphere }: { side: string; hand: AtdHand; hemisphere: string }) {
  const tier = scoreToGoldTier(hand.learning_speed);
  return (
    <div
      className="p-4 rounded-xl"
      style={{ background: "rgba(157,139,181,0.07)", border: "1px solid rgba(157,139,181,0.2)" }}
    >
      <div className="flex items-baseline justify-between gap-2">
        <p className="text-[10px] uppercase tracking-widest font-mono text-white/35">
          {side} Palm
        </p>
        <p className="text-2xl font-mono" style={{ color: PLUM }}>
          {hand.angle_deg}°
        </p>
      </div>
      <p className="text-[10px] text-white/40 mt-1">{RANGE_LABEL[hand.range_category] ?? hand.range_category}</p>
      <p className="text-[9px] text-white/25 font-mono mt-1">{hemisphere} hemisphere processing speed</p>
      {hand.method === "geometric_landmark_estimate" && (
        <p className="text-[9px] mt-1" style={{ color: PLUM }}>
          Geometric estimate
          {typeof hand.confidence === "number" ? ` · ${Math.round(hand.confidence * 100)}% confidence` : ""}
        </p>
      )}
      <div className="grid grid-cols-3 gap-2 mt-3">
        {[
          ["Learning", hand.learning_speed],
          ["Fine motor", hand.fine_motor_capacity],
          ["Sensory", hand.sensory_sensitivity],
        ].map(([label, v]) => (
          <div key={label as string} className="text-center">
            <p className="text-[8px] uppercase tracking-widest text-white/25 font-mono">{label}</p>
            <p className="text-sm font-mono mt-0.5" style={{ color: tier.color }}>
              {Math.round((v as number) * 100)}%
            </p>
          </div>
        ))}
      </div>
      <p className="text-[10px] text-white/30 mt-3 leading-snug">{hand.interpretation}</p>
    </div>
  );
}

export function AtdPanel({
  atd,
  palms = [],
}: {
  atd?: AtdAnalysis | null;
  palms?: PalmCapture[];
}) {
  const hasData = atd && (atd.left_hand || atd.right_hand);

  return (
    <motion.div
      className="rounded-2xl p-5 sm:p-6 relative overflow-hidden"
      style={{
        background: "linear-gradient(145deg, rgba(157,139,181,0.06) 0%, rgba(8,8,20,0.6) 50%)",
        border: `1px solid ${GOLD.border}`,
      }}
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-baseline justify-between gap-2 mb-4">
        <h3 className="font-serif-display text-xl text-[#e8dcc8] tracking-tight flex items-center gap-2">
          <Hand className="w-4 h-4" style={{ color: PLUM }} />
          atd Angle
        </h3>
        <span className="text-[9px] font-mono uppercase tracking-[0.18em] text-white/25">
          Palm · Processing Speed
        </span>
      </div>

      {hasData ? (
        <div className="space-y-3">
          {/* Right palm -> left hemisphere; left palm -> right hemisphere (cross-lateral) */}
          {atd!.right_hand && <HandCard side="Right" hand={atd!.right_hand} hemisphere="Left" />}
          {atd!.left_hand && <HandCard side="Left" hand={atd!.left_hand} hemisphere="Right" />}
          {atd!.summary && <p className="text-[10px] text-white/30 leading-relaxed">{atd!.summary}</p>}
          <p className="text-[9px] text-white/20 leading-relaxed">
            Geometric estimates approximate atd from hand landmarks, not ridge triradii. A ridge-grade
            palm scan is required for a clinical-standard measurement.
          </p>
        </div>
      ) : (
        <div className="py-5 text-center">
          <p className="text-3xl font-serif-display text-white/40">N/A</p>
          {palms.length > 0 ? (
            <>
              <div className="flex items-center justify-center gap-3 mt-4">
                {palms.map((palm) => (
                  <div key={palm.slot} className="text-center">
                    <div
                      className="w-20 h-16 rounded-lg overflow-hidden mx-auto"
                      style={{ border: "1px solid rgba(157,139,181,0.3)" }}
                    >
                      {mediaUrl(palm.thumbnail_url) ? (
                        <img
                          src={mediaUrl(palm.thumbnail_url)}
                          alt={`${palm.hand} palm`}
                          className="w-full h-full object-cover opacity-80"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <Hand className="w-5 h-5 text-white/25" />
                        </div>
                      )}
                    </div>
                    <p className="text-[9px] text-white/40 font-mono mt-1">{palm.hand} palm</p>
                  </div>
                ))}
              </div>
              <p className="text-[11px] mt-3" style={{ color: PLUM }}>
                Palm captured — pending palm analysis
              </p>
              <p className="text-[10px] text-white/25 mt-1 leading-relaxed max-w-xs mx-auto">
                atd needs the palm&apos;s a/t/d ridge triradii. These captures are stored; a
                ridge-grade palm scan is required to compute the angle.
              </p>
            </>
          ) : (
            <p className="text-xs text-white/30 mt-2 leading-relaxed max-w-xs mx-auto">
              The atd angle is measured from a palm print (the a–t–d triradii). It is not derived from
              fingerprints. Provide an inked or high-resolution contact palm scan to compute brain–muscle
              processing speed.
            </p>
          )}
        </div>
      )}
    </motion.div>
  );
}
