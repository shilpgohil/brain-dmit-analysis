"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { Save, Check } from "lucide-react";
import { DEFAULT_API_ORIGIN, loadPreferences, savePreferences } from "@/lib/preferences";

function Toggle({
  active,
  onChange,
  label,
  desc,
}: {
  active: boolean;
  onChange: (v: boolean) => void;
  label: string;
  desc: string;
}) {
  return (
    <button
      onClick={() => onChange(!active)}
      className="w-full flex items-start justify-between gap-4 text-left p-3 rounded-lg transition-all"
      style={{
        background: active ? "rgba(0,212,255,0.06)" : "rgba(255,255,255,0.02)",
        border: `1px solid ${active ? "rgba(0,212,255,0.25)" : "rgba(255,255,255,0.07)"}`,
      }}
    >
      <span className="min-w-0">
        <span className="block text-sm text-white/75">{label}</span>
        <span className="block text-[11px] text-white/30 mt-0.5 leading-snug">{desc}</span>
      </span>
      <span
        className="mt-1 w-9 h-5 rounded-full flex-shrink-0 relative transition-colors"
        style={{ background: active ? "#00d4ff" : "rgba(255,255,255,0.12)" }}
      >
        <span
          className="absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all"
          style={{ left: active ? "1.125rem" : "0.125rem" }}
        />
      </span>
    </button>
  );
}

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState(DEFAULT_API_ORIGIN);
  const [generatePdf, setGeneratePdf] = useState(true);
  const [usePreprocessing, setUsePreprocessing] = useState(true);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const prefs = loadPreferences();
    setApiUrl(prefs.apiUrl);
    setGeneratePdf(prefs.generatePdf);
    setUsePreprocessing(prefs.usePreprocessing);
  }, []);

  const handleSave = () => {
    savePreferences({ apiUrl, generatePdf, usePreprocessing });
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const resetApiUrl = () => setApiUrl(DEFAULT_API_ORIGIN);

  return (
    <div className="min-h-screen pb-24 px-6 pt-12">
      <div className="max-w-2xl mx-auto space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <p className="text-xs text-white/25 tracking-widest uppercase font-mono mb-2">Configuration</p>
          <h1 className="text-display-section text-white">Settings</h1>
          <p className="text-sm text-white/35 mt-2">
            Stored in this browser and applied immediately across the app.
          </p>
        </motion.div>

        <GlassCard gradient>
          <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-5">API Configuration</p>
          <div>
            <label className="block text-[10px] text-white/25 uppercase tracking-widest font-mono mb-2">
              Backend URL
            </label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              placeholder={DEFAULT_API_ORIGIN}
              className="w-full h-10 rounded-lg px-3 text-sm text-white/70 font-mono focus:outline-none transition-all"
              style={{
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
              onFocus={(e) => (e.target.style.borderColor = "rgba(0,212,255,0.4)")}
              onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
            />
            <div className="flex items-center justify-between mt-1.5">
              <p className="text-[10px] text-white/20">
                FastAPI origin (the <code className="text-white/40">/api</code> suffix is added
                automatically). Start with <code className="text-white/40">.\start_api.ps1</code>.
              </p>
              <button onClick={resetApiUrl} className="text-[10px] text-white/30 hover:text-white/60 flex-shrink-0 ml-3">
                Reset
              </button>
            </div>
          </div>
        </GlassCard>

        <GlassCard gradient>
          <p className="text-xs text-white/30 uppercase tracking-widest font-mono mb-5">Analysis Defaults</p>
          <div className="space-y-3">
            <Toggle
              active={usePreprocessing}
              onChange={setUsePreprocessing}
              label="Image preprocessing"
              desc="Run finger-photo to fingerprint enhancement (segmentation, ROI, ridge enhancement) before extraction. Disable for already-scanned prints."
            />
            <Toggle
              active={generatePdf}
              onChange={setGeneratePdf}
              label="Generate PDF report"
              desc="Produce the premium PDF report after analysis completes."
            />
            <p className="text-[10px] text-white/20 leading-snug pt-1">
              These pre-fill the toggles on the New Analysis screen for each new session.
            </p>
          </div>
        </GlassCard>

        <div className="flex items-center justify-end gap-3">
          {saved && (
            <motion.span
              className="text-xs text-emerald-400 flex items-center gap-1"
              initial={{ opacity: 0, x: 8 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <Check className="w-3.5 h-3.5" />
              Saved
            </motion.span>
          )}
          <MagneticButton onClick={handleSave} icon={<Save className="w-3.5 h-3.5" />}>
            Save Settings
          </MagneticButton>
        </div>
      </div>
    </div>
  );
}
