"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { SignaturePad } from "@/components/ui/SignaturePad";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import {
  getBrandingSettings,
  updateBrandingSettings,
  getStorageTelemetry,
  type ReportCustomization,
  type GlobalStorageTelemetry,
} from "@/lib/api";
import { DEFAULT_API_ORIGIN, loadPreferences, savePreferences } from "@/lib/preferences";
import {
  Building2,
  UserCheck,
  PenTool,
  Cloud,
  Database,
  Sparkles,
  Save,
  Check,
  RefreshCw,
  Sliders,
  ShieldCheck,
  Globe,
  Phone,
  Mail,
  FileText,
  Loader2,
  HardDrive,
  Cpu,
} from "lucide-react";

const BRAND_THEMES = [
  { label: "Imperial Gold", hex: "#D4AF37", bg: "rgba(212,175,55,0.15)", border: "rgba(212,175,55,0.4)" },
  { label: "Obsidian Cyan", hex: "#00D4FF", bg: "rgba(0,212,255,0.15)", border: "rgba(0,212,255,0.4)" },
  { label: "Royal Indigo", hex: "#6366F1", bg: "rgba(99,102,241,0.15)", border: "rgba(99,102,241,0.4)" },
  { label: "Emerald Apex", hex: "#10B981", bg: "rgba(16,185,129,0.15)", border: "rgba(16,185,129,0.4)" },
];

function SettingToggle({
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
      type="button"
      onClick={() => onChange(!active)}
      className="w-full flex items-start justify-between gap-4 text-left p-3.5 rounded-xl transition-all"
      style={{
        background: active ? "rgba(0,212,255,0.06)" : "rgba(255,255,255,0.02)",
        border: `1px solid ${active ? "rgba(0,212,255,0.25)" : "rgba(255,255,255,0.07)"}`,
      }}
    >
      <span className="min-w-0">
        <span className="block text-sm font-medium text-white/80">{label}</span>
        <span className="block text-[11px] text-white/35 mt-0.5 leading-snug">{desc}</span>
      </span>
      <span
        className="mt-1 w-9 h-5 rounded-full flex-shrink-0 relative transition-colors"
        style={{ background: active ? "#00d4ff" : "rgba(255,255,255,0.12)" }}
      >
        <span
          className="absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all shadow-sm"
          style={{ left: active ? "1.125rem" : "0.125rem" }}
        />
      </span>
    </button>
  );
}

export default function SettingsPage() {
  const { user, isLoading } = useAuthGuard("partner");

  const [activeTab, setActiveTab] = useState<"branding" | "storage" | "pipeline">("branding");
  const [loadingData, setLoadingData] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [storageChecking, setStorageChecking] = useState(false);

  const [branding, setBranding] = useState<ReportCustomization>({
    school_name: "Apex Global Academy",
    franchise_code: "FR-IN-8892-APEX",
    analyst_name: "Prof. Shilp Gohil, Ph.D.",
    analyst_title: "Senior Biometric Profiler & Cognitive Development Consultant",
    analyst_id: "IADP-89241-SR",
    brand_color: "#D4AF37",
    contact_phone: "+1 (800) 555-DMIT",
    contact_email: "profiling@apexdmit.org",
    website: "https://apexdmit.org",
    counselor_notes:
      "Candidate demonstrates exceptional intellectual maturity and focused self-direction. Recommended for advanced STEM curriculum with supplementary leadership and debate opportunities. Scheduled 6-month progress review confirmed.",
    participant_comments:
      "The assessment provided remarkably accurate insights into my innate learning and working style. The career alignment roadmap validated my inclination toward strategic systems engineering.",
    counselor_signature: "",
  });

  const [storageTelemetry, setStorageTelemetry] = useState<GlobalStorageTelemetry | null>(null);

  const [apiUrl, setApiUrl] = useState(DEFAULT_API_ORIGIN);
  const [generatePdf, setGeneratePdf] = useState(true);
  const [usePreprocessing, setUsePreprocessing] = useState(true);

  useEffect(() => {
    const prefs = loadPreferences();
    setApiUrl(prefs.apiUrl);
    setGeneratePdf(prefs.generatePdf);
    setUsePreprocessing(prefs.usePreprocessing);

    async function loadAll() {
      try {
        const [brandData, storageData] = await Promise.allSettled([
          getBrandingSettings(),
          getStorageTelemetry(),
        ]);
        if (brandData.status === "fulfilled" && brandData.value) {
          setBranding((prev) => ({ ...prev, ...brandData.value }));
        }
        if (storageData.status === "fulfilled" && storageData.value) {
          setStorageTelemetry(storageData.value);
        }
      } finally {
        setLoadingData(false);
      }
    }

    if (user) {
      loadAll();
    }
  }, [user]);

  const handleRefreshStorage = async () => {
    setStorageChecking(true);
    try {
      const data = await getStorageTelemetry();
      setStorageTelemetry(data);
    } catch {
      // Standby fallback
    } finally {
      setStorageChecking(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      savePreferences({ apiUrl, generatePdf, usePreprocessing });
      await updateBrandingSettings(branding);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Failed to persist franchise settings.");
    } finally {
      setSaving(false);
    }
  };

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-7 h-7 animate-spin text-[#c4a574]" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-28 pt-8 px-6">
      {/* Background Ambience */}
      <div className="fixed inset-0 pointer-events-none opacity-25">
        <FingerprintField opacity={0.04} animated={false} color="212, 175, 55" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-white/[0.06] pb-6"
        >
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-1.5 h-1.5 rounded-full bg-[#D4AF37] animate-pulse" />
              <p className="text-[10px] text-[#D4AF37] tracking-[0.25em] uppercase font-mono">
                Franchise Command Deck · Master Settings
              </p>
            </div>
            <h1 className="text-display-section text-white">Global Franchise & Dossier Config</h1>
            <p className="text-sm text-white/40 mt-1 max-w-xl">
              Enterprise white-label branding, default profiler signatures, object storage telemetry, and runtime pipeline controls.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <MagneticButton
              onClick={handleSave}
              disabled={saving}
              icon={saving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
            >
              {saving ? "Persisting..." : "Save Settings"}
            </MagneticButton>
          </div>
        </motion.div>

        {/* Status notification */}
        {saved && (
          <motion.div
            className="flex items-center gap-3 p-4 rounded-xl text-sm"
            style={{
              background: "rgba(16,185,129,0.08)",
              border: "1px solid rgba(16,185,129,0.25)",
              color: "#10b981",
            }}
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <ShieldCheck className="w-4 h-4 flex-shrink-0" />
            <span>
              Franchise profile & digital signatures successfully persisted into SQLite database (<code>partner_settings</code>).
            </span>
          </motion.div>
        )}

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-white/[0.06] pb-3">
          <button
            type="button"
            onClick={() => setActiveTab("branding")}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === "branding"
                ? "bg-[#D4AF37]/15 text-[#D4AF37] border border-[#D4AF37]/30"
                : "text-white/40 hover:text-white/70 hover:bg-white/[0.03]"
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            Franchise & Profiler Identity
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("storage")}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === "storage"
                ? "bg-[#00D4FF]/15 text-[#00D4FF] border border-[#00D4FF]/30"
                : "text-white/40 hover:text-white/70 hover:bg-white/[0.03]"
            }`}
          >
            <Cloud className="w-3.5 h-3.5" />
            Cloud Object Storage
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("pipeline")}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono uppercase tracking-wider transition-all ${
              activeTab === "pipeline"
                ? "bg-[#8B5CF6]/15 text-[#8B5CF6] border border-[#8B5CF6]/30"
                : "text-white/40 hover:text-white/70 hover:bg-white/[0.03]"
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            Pipeline & Engine
          </button>
        </div>

        {/* Tab Content */}
        {loadingData ? (
          <div className="py-20 flex flex-col items-center justify-center text-white/30 text-sm gap-2">
            <Loader2 className="w-6 h-6 animate-spin text-[#D4AF37]" />
            <span>Loading enterprise configurations...</span>
          </div>
        ) : (
          <div className="space-y-6">
            {activeTab === "branding" && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Organization & White-Label */}
                <GlassCard gradient>
                  <div className="flex items-center gap-2 mb-4">
                    <Building2 className="w-4 h-4 text-[#D4AF37]" />
                    <h2 className="text-xs uppercase tracking-widest text-[#D4AF37] font-mono">
                      Institution & White-Label Details
                    </h2>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        School / Institution Name
                      </label>
                      <input
                        type="text"
                        value={branding.school_name ?? ""}
                        onChange={(e) => setBranding({ ...branding, school_name: e.target.value })}
                        placeholder="Apex Global Academy"
                        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Franchise License Code
                      </label>
                      <input
                        type="text"
                        value={branding.franchise_code ?? ""}
                        onChange={(e) => setBranding({ ...branding, franchise_code: e.target.value })}
                        placeholder="FR-IN-8892-APEX"
                        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 font-mono bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                      />
                    </div>

                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Official Contact Phone
                      </label>
                      <div className="relative">
                        <Phone className="w-3.5 h-3.5 text-white/20 absolute left-3 top-3.5" />
                        <input
                          type="text"
                          value={branding.contact_phone ?? ""}
                          onChange={(e) => setBranding({ ...branding, contact_phone: e.target.value })}
                          placeholder="+1 (800) 555-DMIT"
                          className="w-full h-10 rounded-lg pl-9 pr-3 text-sm text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Official Contact Email
                      </label>
                      <div className="relative">
                        <Mail className="w-3.5 h-3.5 text-white/20 absolute left-3 top-3.5" />
                        <input
                          type="text"
                          value={branding.contact_email ?? ""}
                          onChange={(e) => setBranding({ ...branding, contact_email: e.target.value })}
                          placeholder="profiling@apexdmit.org"
                          className="w-full h-10 rounded-lg pl-9 pr-3 text-sm text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Brand Color Theme */}
                  <div className="mt-5 pt-4 border-t border-white/[0.04]">
                    <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-2">
                      Primary Report Accent Theme
                    </label>
                    <div className="flex flex-wrap gap-2.5">
                      {BRAND_THEMES.map((theme) => {
                        const isSelected = branding.brand_color === theme.hex;
                        return (
                          <button
                            key={theme.hex}
                            type="button"
                            onClick={() => setBranding({ ...branding, brand_color: theme.hex })}
                            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono transition-all"
                            style={{
                              background: isSelected ? theme.bg : "rgba(255,255,255,0.03)",
                              border: `1px solid ${isSelected ? theme.border : "rgba(255,255,255,0.06)"}`,
                              color: isSelected ? theme.hex : "rgba(255,255,255,0.5)",
                            }}
                          >
                            <span
                              className="w-3 h-3 rounded-full flex-shrink-0"
                              style={{ background: theme.hex }}
                            />
                            {theme.label}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </GlassCard>

                {/* Profiler Credentials & Signature */}
                <GlassCard gradient>
                  <div className="flex items-center gap-2 mb-4">
                    <UserCheck className="w-4 h-4 text-[#D4AF37]" />
                    <h2 className="text-xs uppercase tracking-widest text-[#D4AF37] font-mono">
                      Lead DMIT Profiler & Certified Signature
                    </h2>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-5">
                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Profiler Full Name & Degree
                      </label>
                      <input
                        type="text"
                        value={branding.analyst_name ?? ""}
                        onChange={(e) => setBranding({ ...branding, analyst_name: e.target.value })}
                        placeholder="Prof. Shilp Gohil, Ph.D."
                        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Professional Title
                      </label>
                      <input
                        type="text"
                        value={branding.analyst_title ?? ""}
                        onChange={(e) => setBranding({ ...branding, analyst_title: e.target.value })}
                        placeholder="Senior Biometric Profiler"
                        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-1.5">
                        Analyst Registry / ID
                      </label>
                      <input
                        type="text"
                        value={branding.analyst_id ?? ""}
                        onChange={(e) => setBranding({ ...branding, analyst_id: e.target.value })}
                        placeholder="IADP-89241-SR"
                        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 font-mono bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                      />
                    </div>
                  </div>

                  {/* Digital Signature Pad */}
                  <div className="pt-2 border-t border-white/[0.04]">
                    <SignaturePad
                      label="Permanent Profiler Certified Signature"
                      subtitle="Draw with stylus, mouse, or touch. This signature will automatically populate Page 60 of all generated dossiers."
                      value={branding.counselor_signature}
                      onChange={(dataUrl) => setBranding({ ...branding, counselor_signature: dataUrl })}
                      strokeColor={branding.brand_color || "#D4AF37"}
                    />
                  </div>
                </GlassCard>

                {/* Default Counseling Observation Template */}
                <GlassCard gradient>
                  <div className="flex items-center gap-2 mb-3">
                    <FileText className="w-4 h-4 text-[#D4AF37]" />
                    <h2 className="text-xs uppercase tracking-widest text-[#D4AF37] font-mono">
                      Default Counseling Recommendation Preamble
                    </h2>
                  </div>
                  <p className="text-[11px] text-white/30 mb-2">
                    Pre-fills the Counselor Observations section on Page 60 of newly initialized analysis sessions.
                  </p>
                  <textarea
                    rows={3}
                    value={branding.counselor_notes ?? ""}
                    onChange={(e) => setBranding({ ...branding, counselor_notes: e.target.value })}
                    className="w-full rounded-xl p-3 text-xs leading-relaxed text-white/80 bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#D4AF37]/50"
                  />
                </GlassCard>
              </motion.div>
            )}

            {activeTab === "storage" && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <GlassCard gradient>
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-2">
                      <Cloud className="w-4 h-4 text-[#00D4FF]" />
                      <h2 className="text-xs uppercase tracking-widest text-[#00D4FF] font-mono">
                        Object Storage Engine Telemetry
                      </h2>
                    </div>
                    <button
                      type="button"
                      onClick={handleRefreshStorage}
                      disabled={storageChecking}
                      className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-mono uppercase bg-white/[0.04] hover:bg-white/[0.08] text-white/50 hover:text-white transition-all"
                    >
                      <RefreshCw className={`w-3 h-3 ${storageChecking ? "animate-spin" : ""}`} />
                      Test Link
                    </button>
                  </div>

                  {/* Status Banner */}
                  <div
                    className="p-4 rounded-xl flex items-center justify-between gap-4 mb-6"
                    style={{
                      background: storageTelemetry?.storage?.enabled
                        ? "rgba(16,185,129,0.08)"
                        : "rgba(0,212,255,0.05)",
                      border: `1px solid ${
                        storageTelemetry?.storage?.enabled
                          ? "rgba(16,185,129,0.25)"
                          : "rgba(0,212,255,0.2)"
                      }`,
                    }}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center"
                        style={{
                          background: storageTelemetry?.storage?.enabled
                            ? "rgba(16,185,129,0.15)"
                            : "rgba(0,212,255,0.15)",
                        }}
                      >
                        <HardDrive
                          className="w-4 h-4"
                          style={{
                            color: storageTelemetry?.storage?.enabled ? "#10B981" : "#00D4FF",
                          }}
                        />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono font-medium text-white/90 uppercase tracking-wide">
                            {storageTelemetry?.storage?.enabled
                              ? `Cloud Object Storage: ${storageTelemetry.provider?.toUpperCase()}`
                              : "Local Filesystem Storage (Dev Standby)"}
                          </span>
                          <span
                            className="text-[9px] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider"
                            style={{
                              background: storageTelemetry?.storage?.enabled
                                ? "rgba(16,185,129,0.2)"
                                : "rgba(0,212,255,0.15)",
                              color: storageTelemetry?.storage?.enabled ? "#10B981" : "#00D4FF",
                            }}
                          >
                            {storageTelemetry?.storage?.enabled ? "ONLINE" : "STANDBY"}
                          </span>
                        </div>
                        <p className="text-[11px] text-white/40 mt-0.5">
                          {storageTelemetry?.storage?.enabled
                            ? `Automated sync active: 64-page dossiers and fingerprint scans are uploaded to remote bucket.`
                            : `Operating in direct server-disk mode. Presigned URLs will fallback to direct streaming.`}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Telemetry specs grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 font-mono">
                    <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                      <span className="text-[10px] text-white/30 uppercase tracking-widest block mb-1">
                        Active Provider
                      </span>
                      <span className="text-xs text-white/80 font-medium">
                        {storageTelemetry?.storage?.provider ?? "local"}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                      <span className="text-[10px] text-white/30 uppercase tracking-widest block mb-1">
                        Bucket Destination
                      </span>
                      <span className="text-xs text-[#00D4FF] font-medium truncate block">
                        {storageTelemetry?.bucket || storageTelemetry?.storage?.bucket || "dmit-production-reports"}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                      <span className="text-[10px] text-white/30 uppercase tracking-widest block mb-1">
                        Remote Endpoint
                      </span>
                      <span className="text-xs text-white/60 truncate block">
                        {storageTelemetry?.endpoint || storageTelemetry?.storage?.endpoint || "https://s3.us-west-004.backblazeb2.com"}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                      <span className="text-[10px] text-white/30 uppercase tracking-widest block mb-1">
                        Presigned Token TTL
                      </span>
                      <span className="text-xs text-[#10B981] font-medium">
                        3,600 seconds (1 hour strict expiration)
                      </span>
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            )}

            {activeTab === "pipeline" && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <GlassCard gradient>
                  <div className="flex items-center gap-2 mb-4">
                    <Sliders className="w-4 h-4 text-[#8B5CF6]" />
                    <h2 className="text-xs uppercase tracking-widest text-[#8B5CF6] font-mono">
                      Biometric Processing Defaults
                    </h2>
                  </div>
                  <div className="space-y-3">
                    <SettingToggle
                      active={usePreprocessing}
                      onChange={setUsePreprocessing}
                      label="Automated Ridge Preprocessing"
                      desc="Applies 5-stage skin segmentation, blur validation, ROI extraction, nail contour removal, and CLAHE/Gabor enhancement."
                    />
                    <SettingToggle
                      active={generatePdf}
                      onChange={setGeneratePdf}
                      label="Automatic 64-Page Master Dossier Compilation"
                      desc="Immediately compiles the full 64-page luxury PDF report upon completion of Table 1.1 feature extraction."
                    />
                  </div>
                </GlassCard>

                <GlassCard gradient>
                  <div className="flex items-center gap-2 mb-4">
                    <Database className="w-4 h-4 text-[#8B5CF6]" />
                    <h2 className="text-xs uppercase tracking-widest text-[#8B5CF6] font-mono">
                      FastAPI Backend Gateway
                    </h2>
                  </div>
                  <div>
                    <label className="block text-[10px] text-white/35 uppercase tracking-widest font-mono mb-2">
                      API Server Origin
                    </label>
                    <input
                      type="text"
                      value={apiUrl}
                      onChange={(e) => setApiUrl(e.target.value)}
                      placeholder={DEFAULT_API_ORIGIN}
                      className="w-full h-10 rounded-lg px-3 text-sm text-white/70 font-mono bg-white/[0.04] border border-white/[0.08] focus:outline-none focus:border-[#8B5CF6]/50"
                    />
                    <div className="flex items-center justify-between mt-1.5">
                      <p className="text-[10px] text-white/30">
                        Default: <code>http://localhost:8001</code>.
                      </p>
                      <button
                        type="button"
                        onClick={() => setApiUrl(DEFAULT_API_ORIGIN)}
                        className="text-[10px] text-white/40 hover:text-white/80"
                      >
                        Reset to default
                      </button>
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
