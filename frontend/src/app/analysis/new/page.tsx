"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { createSession, uploadImagesWithSlots, runAnalysis } from "@/lib/api";
import { getDefaultGeneratePdf, getDefaultUsePreprocessing } from "@/lib/preferences";
import { GlassCard } from "@/components/ui/GlassCard";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { FingerGuidanceOverlay } from "@/components/analysis/FingerGuidanceOverlay";
import { PalmGuidanceOverlay } from "@/components/analysis/PalmGuidanceOverlay";
import {
  FINGER_GUIDANCE,
  PALM_GUIDANCE,
  hasSeenUploadGuidance,
  markUploadGuidanceSeen,
  markPalmGuidanceSeen,
} from "@/lib/finger-guidance";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { cn } from "@/lib/utils";
import {
  Fingerprint,
  Upload,
  X,
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  Info,
  User,
  Hand,
  HelpCircle,
} from "lucide-react";

const FINGER_SLOTS = [
  { id: "R1", label: "Right Thumb",  short: "RT", hand: "right" },
  { id: "R2", label: "Right Index",  short: "RI", hand: "right" },
  { id: "R3", label: "Right Middle", short: "RM", hand: "right" },
  { id: "R4", label: "Right Ring",   short: "RR", hand: "right" },
  { id: "R5", label: "Right Little", short: "RL", hand: "right" },
  { id: "L1", label: "Left Thumb",   short: "LT", hand: "left" },
  { id: "L2", label: "Left Index",   short: "LI", hand: "left" },
  { id: "L3", label: "Left Middle",  short: "LM", hand: "left" },
  { id: "L4", label: "Left Ring",    short: "LR", hand: "left" },
  { id: "L5", label: "Left Little",  short: "LL", hand: "left" },
];

const PALM_SLOTS = [
  { id: "LPALM", label: "Left Palm" },
  { id: "RPALM", label: "Right Palm" },
];

interface SlotFile {
  file: File;
  preview: string;
  slotId: string;
}

// Mirrors api/helpers.py's parse_finger_position / parse_palm_position so a
// bulk-dropped batch of already-named files (R1.bmp, L3Center.jpg, Lpalm.png)
// lands on the *correct* slot instead of being assigned by arbitrary drop
// order, which silently mislabelled fingers whenever filenames were present.
const FILE_EXT_RE = /\.(bmp|jpe?g|png|tiff?|webp)$/i;
const SLOT_PREFIX_RE = /^(R[1-5]|L[1-5])/i;

function isSupportedImageFile(file: File): boolean {
  return file.type.startsWith("image/") || FILE_EXT_RE.test(file.name);
}

/**
 * Compress an image file using the browser Canvas API before uploading.
 * - Resizes to maxDim on the longest side (preserves aspect ratio)
 * - Re-encodes as JPEG at the given quality (0-1)
 * - BMP scanner images smaller than maxDim are returned unchanged as PNG
 *   (no upscaling, no quality loss for already-small scanner prints)
 *
 * Fingerprint ridges need enough resolution for feature extraction — 1200 px
 * at quality 0.92 retains full visible detail while reducing file size ~90%.
 */
async function compressImage(
  file: File,
  maxDim = 1200,
  quality = 0.92,
): Promise<File> {
  return new Promise((resolve) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      URL.revokeObjectURL(url);
      const { naturalWidth: w, naturalHeight: h } = img;
      // Don't upscale — if already smaller, just convert format if needed
      const scale = Math.min(1, maxDim / Math.max(w, h));
      const tw = Math.round(w * scale);
      const th = Math.round(h * scale);
      const canvas = document.createElement("canvas");
      canvas.width = tw;
      canvas.height = th;
      const ctx = canvas.getContext("2d");
      if (!ctx) { resolve(file); return; }
      ctx.drawImage(img, 0, 0, tw, th);
      canvas.toBlob(
        (blob) => {
          if (!blob) { resolve(file); return; }
          // Keep original filename but with .jpg extension
          const name = file.name.replace(/\.[^.]+$/, "") + ".jpg";
          resolve(new File([blob], name, { type: "image/jpeg" }));
        },
        "image/jpeg",
        quality,
      );
    };
    img.onerror = () => { URL.revokeObjectURL(url); resolve(file); };
    img.src = url;
  });
}

function detectSlotFromFilename(filename: string): string | null {
  const stem = filename.replace(/\.[^./\\]+$/, "");
  const prefixMatch = SLOT_PREFIX_RE.exec(stem);
  if (prefixMatch) return prefixMatch[1].toUpperCase();
  const upper = stem.toUpperCase();
  if (upper.includes("LPALM")) return "LPALM";
  if (upper.includes("RPALM")) return "RPALM";
  for (const pos of FINGER_SLOTS) {
    if (upper.includes(pos.id)) return pos.id;
  }
  return null;
}

export default function NewAnalysisPage() {
  const router = useRouter();
  const { user, isLoading } = useAuthGuard("partner");
  const [slots, setSlots] = useState<(SlotFile | null)[]>(Array(10).fill(null));
  const [palms, setPalms] = useState<(SlotFile | null)[]>([null, null]);
  const [draggingSlot, setDraggingSlot] = useState<number | null>(null);
  const [subjectName, setSubjectName] = useState("");
  const [subjectAge, setSubjectAge] = useState("");
  const [subjectGender, setSubjectGender] = useState<"" | "male" | "female" | "other">("");
  const [school, setSchool] = useState("");
  const [counsellor, setCounsellor] = useState("");
  const [purpose, setPurpose] = useState<"self" | "child" | "career" | "couple" | "corporate" | "other">("self");
  const [usePreprocessing, setUsePreprocessing] = useState(false);
  const [generatePdf, setGeneratePdf] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [guidanceSlotIndex, setGuidanceSlotIndex] = useState<number | null>(null);
  const [palmGuidanceIndex, setPalmGuidanceIndex] = useState<number | null>(null);
  const fileInputRefs = useRef<(HTMLInputElement | null)[]>([]);
  const palmInputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    setUsePreprocessing(getDefaultUsePreprocessing());
    setGeneratePdf(getDefaultGeneratePdf());
  }, []);

  useEffect(() => {
    if (!notice) return;
    const t = setTimeout(() => setNotice(null), 3000);
    return () => clearTimeout(t);
  }, [notice]);

  useEffect(() => {
    if (!hasSeenUploadGuidance()) {
      setGuidanceSlotIndex(0);
    }
  }, []);

  const openGuidanceForSlot = (slotIndex: number) => {
    setGuidanceSlotIndex(slotIndex);
  };

  const closeGuidance = () => {
    setGuidanceSlotIndex(null);
    markUploadGuidanceSeen();
  };

  const continueGuidanceUpload = () => {
    if (guidanceSlotIndex === null) return;
    markUploadGuidanceSeen();
    const idx = guidanceSlotIndex;
    setGuidanceSlotIndex(null);
    requestAnimationFrame(() => {
      fileInputRefs.current[idx]?.click();
    });
  };

  // Tapping an empty slot always shows the guidance overlay so the user
  // sees placement instructions before the file picker opens.
  // On filled slots the outer div click is a no-op (filled guard below).
  const handleEmptySlotClick = (slotIndex: number) => {
    openGuidanceForSlot(slotIndex);
  };

  const openPalmGuidance = (palmIndex: number) => {
    setPalmGuidanceIndex(palmIndex);
  };

  const closePalmGuidance = () => {
    markPalmGuidanceSeen();
    setPalmGuidanceIndex(null);
  };

  const continuePalmGuidance = () => {
    if (palmGuidanceIndex === null) return;
    markPalmGuidanceSeen();
    const idx = palmGuidanceIndex;
    setPalmGuidanceIndex(null);
    requestAnimationFrame(() => {
      palmInputRefs.current[idx]?.click();
    });
  };

  const filledCount = slots.filter(Boolean).length;
  const progress = (filledCount / 10) * 100;

  const assignFile = useCallback((file: File, slotIndex: number) => {
    const preview = URL.createObjectURL(file);
    setSlots((prev) => {
      const next = [...prev];
      next[slotIndex] = { file, preview, slotId: FINGER_SLOTS[slotIndex].id };
      return next;
    });
  }, []);

  const handleDropOnSlot = (e: React.DragEvent, slotIndex: number) => {
    e.preventDefault();
    setDraggingSlot(null);
    const file = e.dataTransfer.files[0];
    if (file) assignFile(file, slotIndex);
  };

  // Handles both drag-drop and click-to-browse bulk selection. Builds the
  // whole next slots/palms array locally in one pass (rather than calling
  // setSlots per-file against the render-time `slots` closure, which was
  // the root cause of files overwriting each other / landing in the wrong
  // slot whenever some slots were already filled) so every file is placed
  // exactly once, in a single, predictable state update.
  const handleBulkFiles = useCallback(
    (fileList: File[]) => {
      if (fileList.length === 0) return;

      const images = fileList.filter(isSupportedImageFile);
      const rejectedCount = fileList.length - images.length;

      const nextSlots = [...slots];
      const nextPalms = [...palms];
      const unmatched: File[] = [];

      for (const file of images) {
        const slotId = detectSlotFromFilename(file.name);
        if (slotId === "LPALM" || slotId === "RPALM") {
          const idx = PALM_SLOTS.findIndex((s) => s.id === slotId);
          if (nextPalms[idx]?.preview) URL.revokeObjectURL(nextPalms[idx]!.preview);
          nextPalms[idx] = { file, preview: URL.createObjectURL(file), slotId };
        } else if (slotId) {
          const idx = FINGER_SLOTS.findIndex((s) => s.id === slotId);
          if (nextSlots[idx]?.preview) URL.revokeObjectURL(nextSlots[idx]!.preview);
          nextSlots[idx] = { file, preview: URL.createObjectURL(file), slotId };
        } else {
          unmatched.push(file);
        }
      }

      // Files with no recognizable slot in their filename fill whatever
      // finger slots are still empty, in order.
      let cursor = 0;
      let overflow = 0;
      for (const file of unmatched) {
        while (cursor < nextSlots.length && nextSlots[cursor]) cursor++;
        if (cursor >= nextSlots.length) {
          overflow++;
          continue;
        }
        nextSlots[cursor] = { file, preview: URL.createObjectURL(file), slotId: FINGER_SLOTS[cursor].id };
        cursor++;
      }

      setSlots(nextSlots);
      setPalms(nextPalms);

      const problems: string[] = [];
      if (rejectedCount > 0) {
        problems.push(`${rejectedCount} file${rejectedCount !== 1 ? "s" : ""} skipped (unsupported format)`);
      }
      if (overflow > 0) {
        problems.push(`${overflow} file${overflow !== 1 ? "s" : ""} could not be placed (all 10 slots are full)`);
      }
      if (problems.length > 0) {
        setError(problems.join(". ") + ".");
        setNotice(null);
      } else {
        setError(null);
        const placed = images.length - overflow;
        setNotice(`${placed} image${placed !== 1 ? "s" : ""} added.`);
      }
    },
    [slots, palms]
  );

  const handleBulkDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    handleBulkFiles(Array.from(e.dataTransfer.files));
  };

  const handleBulkFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleBulkFiles(Array.from(e.target.files ?? []));
    e.target.value = "";
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>, slotIndex: number) => {
    const file = e.target.files?.[0];
    if (file) assignFile(file, slotIndex);
  };

  const removeSlot = (slotIndex: number) => {
    setSlots((prev) => {
      const next = [...prev];
      if (prev[slotIndex]?.preview) URL.revokeObjectURL(prev[slotIndex]!.preview);
      next[slotIndex] = null;
      return next;
    });
  };

  const assignPalm = (file: File, palmIndex: number) => {
    const preview = URL.createObjectURL(file);
    setPalms((prev) => {
      const next = [...prev];
      if (prev[palmIndex]?.preview) URL.revokeObjectURL(prev[palmIndex]!.preview);
      next[palmIndex] = { file, preview, slotId: PALM_SLOTS[palmIndex].id };
      return next;
    });
  };

  const removePalm = (palmIndex: number) => {
    setPalms((prev) => {
      const next = [...prev];
      if (prev[palmIndex]?.preview) URL.revokeObjectURL(prev[palmIndex]!.preview);
      next[palmIndex] = null;
      return next;
    });
  };

  const handleSubmit = async () => {
    const filled = slots.filter(Boolean) as SlotFile[];
    if (filled.length === 0) {
      setError("Upload at least one fingerprint image.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const session = await createSession({
        subject_name: subjectName || undefined,
        subject_age: subjectAge ? Number.parseInt(subjectAge) : undefined,
        subject_gender: subjectGender || undefined,
        school: school || undefined,
        counsellor: counsellor || undefined,
        notes: `Purpose: ${purpose}`,
      });

      // Compress images before upload to reduce server memory usage and upload size.
      // Fingerprints: max 1200px, quality 0.92 — retains all ridge detail.
      // Palms: max 1000px, quality 0.88 — only need geometry for ATD angle.
      const compressedFingers = await Promise.all(
        filled.map(async (s) => ({
          slotId: s.slotId,
          file: await compressImage(s.file, 1200, 0.92),
        }))
      );
      const palmFiles = palms.filter(Boolean) as SlotFile[];
      const compressedPalms = await Promise.all(
        palmFiles.map(async (p) => ({
          slotId: p.slotId,
          file: await compressImage(p.file, 1000, 0.88),
        }))
      );

      await uploadImagesWithSlots(session.id, [...compressedFingers, ...compressedPalms]);
      await runAnalysis({ session_id: session.id, use_preprocessing: usePreprocessing, generate_pdf: generatePdf });
      router.push(`/analysis/${session.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unexpected error occurred.");
      setLoading(false);
    }
  };

  if (isLoading || !user) {
    return (
      <div className="min-h-screen pb-24 px-6 pt-12 flex items-center justify-center">
        <div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-24 px-6 pt-12">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <p className="text-xs text-accent-gold tracking-widest uppercase font-mono mb-2">
            New Analysis
          </p>
          <h1 className="text-display-section text-white">
            Biometric Intake
          </h1>
          <p className="text-white/40 mt-2">
            Upload up to 10 fingerprint images. Assign each to a finger position.
          </p>
          <p className="text-[11px] text-white/25 mt-2 leading-relaxed max-w-2xl">
            Supports phone photos and USB fingerprint-scanner exports (BMP, PNG, JPEG, TIFF, WebP).
            Scanner-grade prints are detected automatically and skip phone-photo enhancement.
          </p>
        </motion.div>

        {/* Progress bar */}
        <motion.div
          className="relative h-px rounded-full overflow-hidden"
          style={{ background: "rgba(255,255,255,0.06)" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <motion.div
            className="absolute inset-y-0 left-0 rounded-full"
            style={{ background: "linear-gradient(90deg, #00d4ff, #8b5cf6)" }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          />
          <div className="absolute right-0 top-4 text-[10px] text-white/30 font-mono">
            {filledCount}/10
          </div>
        </motion.div>

        {/* Subject info */}
        <GlassCard gradient>
          <div className="flex items-center gap-2 mb-5">
            <User className="w-4 h-4 text-white/30" />
            <span className="text-xs text-white/50 uppercase tracking-widest font-mono">Subject Information</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <CinematicInput
              label="Subject Name"
              placeholder="Jane Smith"
              value={subjectName}
              onChange={setSubjectName}
            />
            <CinematicInput
              label="Age"
              placeholder="28"
              type="number"
              value={subjectAge}
              onChange={setSubjectAge}
            />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
            <div>
              <label className="text-[10px] font-mono uppercase text-white/35 mb-2 block">Gender</label>
              <select
                value={subjectGender}
                onChange={(e) => setSubjectGender(e.target.value as "" | "male" | "female" | "other")}
                className="w-full h-10 rounded-lg px-3 text-sm text-white/70 focus:outline-none transition-all"
                style={{ background: "rgba(8,8,24,0.9)", border: "1px solid rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.7)" }}
              >
                <option value="" style={{ background: "#0d0d1a" }}>—</option>
                <option value="male" style={{ background: "#0d0d1a" }}>Male</option>
                <option value="female" style={{ background: "#0d0d1a" }}>Female</option>
                <option value="other" style={{ background: "#0d0d1a" }}>Other</option>
              </select>
            </div>
            <CinematicInput label="School / Institution" placeholder="e.g. DPS" value={school} onChange={setSchool} />
            <CinematicInput label="Counsellor" placeholder="Dr. Sharma" value={counsellor} onChange={setCounsellor} />
          </div>
          <div className="mt-4">
            <label className="text-[10px] font-mono uppercase text-white/35 mb-2 block">Analysis purpose</label>
            <div className="flex flex-wrap gap-2">
              {(["self", "child", "career", "couple", "corporate", "other"] as const).map((id) => (
                <button key={id} type="button" onClick={() => setPurpose(id)} className={cn("px-3 py-1.5 rounded-lg text-[11px] font-mono capitalize", purpose === id ? "bg-accent-gold-dim text-accent-champagne border border-[rgba(196,165,116,0.35)]" : "text-white/40 border border-white/[0.08]")}>{id}</button>
              ))}
            </div>
          </div>
        </GlassCard>

        {/* Fingerprint slots */}
        <GlassCard gradient padding="lg">
          <div className="flex items-center gap-2 mb-6">
            <Fingerprint className="w-4 h-4 text-[#00d4ff]" />
            <span className="text-xs text-white/50 uppercase tracking-widest font-mono">Fingerprint Images</span>
            <span className="ml-auto text-xs text-white/25 font-mono">{filledCount} / 10 loaded</span>
          </div>

          {/* Bulk drop zone — drag-drop OR click to browse; files named
              R1/L1/LPALM etc. auto-map to the right slot, unnamed files
              fill whatever slots are still empty. */}
          <label
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleBulkDrop}
            className={cn(
              "relative mb-5 rounded-xl border border-dashed transition-all duration-300 py-5 flex flex-col items-center gap-2 cursor-pointer",
              dragOver
                ? "border-[rgba(0,212,255,0.5)] bg-[rgba(0,212,255,0.05)]"
                : "border-white/[0.08] hover:border-white/[0.14] hover:bg-white/[0.02]"
            )}
          >
            <input
              type="file"
              multiple
              accept="image/*,.bmp,.tif,.tiff,.webp"
              className="hidden"
              onChange={handleBulkFileInput}
            />
            <Upload className="w-5 h-5 text-white/20" />
            <p className="text-xs text-white/30">
              Drop or click to select multiple images at once
            </p>
            <p className="text-[10px] text-white/20">
              Files named like R1.bmp, L3.jpg, or LPalm.png auto-assign to the right slot
            </p>
          </label>

          <AnimatePresence>
            {notice && (
              <motion.div
                className="mb-4 flex items-center gap-2 p-2.5 rounded-lg"
                style={{ background: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.2)" }}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.25 }}
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-green-400 flex-shrink-0" />
                <p className="text-xs text-green-400/90">{notice}</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* 2×5 Finger grid — shows 5 columns on all sizes (represents the 5 fingers per hand) */}
          <div className="grid grid-cols-5 gap-2 sm:gap-3">
            {FINGER_SLOTS.map((slot, i) => {
              const filled = slots[i];
              return (
                <motion.div
                  key={slot.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: i * 0.04, ease: [0.16, 1, 0.3, 1] }}
                >
                  <div className="relative">
                  <div
                    className={cn(
                      "relative flex flex-col items-center justify-center rounded-xl cursor-pointer transition-all duration-300 overflow-hidden group",
                      "border aspect-[3/4]",
                      filled
                        ? "border-[rgba(0,212,255,0.3)] bg-[rgba(0,212,255,0.05)]"
                        : "border-white/[0.07] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.04]",
                    )}
                    onDragOver={(e) => { e.preventDefault(); setDraggingSlot(i); }}
                    onDragLeave={() => setDraggingSlot(null)}
                    onDrop={(e) => handleDropOnSlot(e, i)}
                    onClick={() => { if (!filled) handleEmptySlotClick(i); }}
                    onKeyDown={(e) => {
                      if (!filled && (e.key === "Enter" || e.key === " ")) {
                        e.preventDefault();
                        handleEmptySlotClick(i);
                      }
                    }}
                    role={filled ? undefined : "button"}
                    tabIndex={filled ? undefined : 0}
                  >
                    <input
                      ref={(el) => { fileInputRefs.current[i] = el; }}
                      type="file"
                      accept="image/*,.bmp,.tif,.tiff,.webp"
                      className="hidden"
                      onChange={(e) => handleFileInput(e, i)}
                    />
                    {filled ? (
                      <>
                        <img
                          src={filled.preview}
                          alt={slot.label}
                          className="absolute inset-0 w-full h-full object-cover filter grayscale opacity-80"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                        <div className="absolute top-1.5 right-1.5">
                          <button
                            type="button"
                            onClick={(e) => { e.preventDefault(); removeSlot(i); }}
                            className="w-5 h-5 rounded-full bg-black/50 flex items-center justify-center text-white/50 hover:text-white hover:bg-black/80 transition-colors"
                          >
                            <X className="w-3 h-3" />
                          </button>
                        </div>
                        <div className="absolute bottom-0 left-0 right-0 p-1.5">
                          <p className="text-[9px] text-white/90 font-medium text-center leading-tight">
                            {slot.short}
                          </p>
                        </div>
                        <div className="absolute top-1.5 left-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-[#00d4ff]" />
                        </div>
                      </>
                    ) : (
                      <>
                        <Fingerprint className="w-5 h-5 text-white/15 mb-1 group-hover:text-white/30 transition-colors" strokeWidth={1} />
                        <p className="text-[9px] text-white/20 font-mono">{slot.short}</p>
                        {draggingSlot === i && (
                          <div className="absolute inset-0 bg-[rgba(0,212,255,0.08)] rounded-xl" />
                        )}
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            openGuidanceForSlot(i);
                          }}
                          className="absolute bottom-1 right-1 w-5 h-5 rounded-full bg-black/40 flex items-center justify-center text-white/35 hover:text-white/70 transition-colors"
                          aria-label={`Help for ${slot.label}`}
                        >
                          <HelpCircle className="w-3 h-3" />
                        </button>
                      </>
                    )}
                  </div>
                  <p className="text-[8px] text-white/20 text-center mt-1 leading-tight truncate px-0.5">
                    {slot.label.replace("Right ", "R. ").replace("Left ", "L. ")}
                  </p>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {filledCount > 0 && filledCount < 10 && (
            <motion.div
              className="mt-5 flex items-start gap-2 p-3 rounded-lg"
              style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.15)" }}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              transition={{ duration: 0.3 }}
            >
              <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-amber-400/80">
                {10 - filledCount} slots empty. Analysis will be computed from available prints only.
                For complete profiling, all 10 fingerprints are recommended.
              </p>
            </motion.div>
          )}
        </GlassCard>

        {/* Palm prints (optional) */}
        <GlassCard gradient padding="lg">
          <div className="flex items-center gap-2 mb-2">
            <Hand className="w-4 h-4 text-[#9d8bb5]" />
            <span className="text-xs text-white/50 uppercase tracking-widest font-mono">Palm Prints</span>
            <span className="ml-auto text-[10px] text-white/25 font-mono">Optional</span>
          </div>
          <p className="text-[11px] text-white/30 mb-5 leading-relaxed max-w-2xl">
            Palm prints are captured for the atd angle (brain–muscle processing speed). atd requires the
            palm&apos;s a/t/d ridge triradii — a casual photo shows creases, not ridges — so captured palms
            are stored and marked <span className="text-white/50">pending palm analysis</span>. The atd
            section stays N/A until a ridge-grade palm scan is processed.
          </p>
          <div className="grid grid-cols-2 gap-3 max-w-md">
            {PALM_SLOTS.map((slot, i) => {
              const filled = palms[i];
              return (
                <div key={slot.id} className="relative">
                  <div
                    className={cn(
                      "relative flex flex-col items-center justify-center rounded-xl transition-all duration-300 overflow-hidden group border aspect-[4/3]",
                      filled
                        ? "border-[rgba(157,139,181,0.4)] bg-[rgba(157,139,181,0.06)]"
                        : "border-white/[0.07] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.04] cursor-pointer",
                    )}
                    onClick={() => { if (!filled) openPalmGuidance(i); }}
                    onKeyDown={(e) => {
                      if (!filled && (e.key === "Enter" || e.key === " ")) {
                        e.preventDefault();
                        openPalmGuidance(i);
                      }
                    }}
                    role={filled ? undefined : "button"}
                    tabIndex={filled ? undefined : 0}
                  >
                    <input
                      ref={(el) => { palmInputRefs.current[i] = el; }}
                      type="file"
                      accept="image/*,.bmp,.tif,.tiff,.webp"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) assignPalm(file, i);
                        if (e.target) e.target.value = "";
                      }}
                    />
                    {filled ? (
                      <>
                        <img
                          src={filled.preview}
                          alt={slot.label}
                          className="absolute inset-0 w-full h-full object-cover opacity-80"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                        <button
                          type="button"
                          onClick={(e) => { e.stopPropagation(); removePalm(i); }}
                          className="absolute top-1.5 right-1.5 w-5 h-5 rounded-full bg-black/50 flex items-center justify-center text-white/50 hover:text-white hover:bg-black/80 transition-colors"
                        >
                          <X className="w-3 h-3" />
                        </button>
                        <div className="absolute top-1.5 left-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-[#9d8bb5]" />
                        </div>
                        <p className="absolute bottom-1 left-0 right-0 text-[9px] text-white/90 text-center">
                          {slot.label}
                        </p>
                      </>
                    ) : (
                      <>
                        <Hand className="w-5 h-5 text-white/15 mb-1 group-hover:text-white/30 transition-colors" strokeWidth={1} />
                        <p className="text-[10px] text-white/25 font-mono">{slot.label}</p>
                        <button
                          type="button"
                          onClick={(e) => { e.stopPropagation(); openPalmGuidance(i); }}
                          className="absolute bottom-1 right-1 w-5 h-5 rounded-full bg-black/40 flex items-center justify-center text-white/35 hover:text-white/70 transition-colors"
                          aria-label={`Help for ${slot.label}`}
                        >
                          <HelpCircle className="w-3 h-3" />
                        </button>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </GlassCard>

        {/* Pipeline options */}
        <GlassCard gradient>
          <div className="flex items-center gap-2 mb-5">
            <span className="text-xs text-white/50 uppercase tracking-widest font-mono">Pipeline Configuration</span>
          </div>
          <div className="space-y-4">
            <ToggleRow
              label="Image Preprocessing"
              sub="CLAHE enhancement + Gabor ridge filtering + segmentation before feature extraction"
              checked={usePreprocessing}
              onChange={setUsePreprocessing}
              recommended
            />
            <div className="h-px bg-white/[0.05]" />
            <ToggleRow
              label="Generate PDF Report"
              sub="Produce a professional multi-page analysis report after processing completes"
              checked={generatePdf}
              onChange={setGeneratePdf}
            />
          </div>
        </GlassCard>

        {/* Info */}
        <div
          className="flex items-start gap-3 p-4 rounded-xl"
          style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}
        >
          <Info className="w-4 h-4 text-white/20 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-white/30 leading-relaxed">
            All processing occurs locally. No biometric data is transmitted externally.
            For optimal accuracy, use 500 DPI grayscale scans. Analysis completes in approximately 2â€“10 seconds.
          </p>
        </div>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              className="flex items-start gap-2 p-4 rounded-xl"
              style={{ background: "rgba(244,63,94,0.08)", border: "1px solid rgba(244,63,94,0.2)" }}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
            >
              <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-rose-400">{error}</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Submit */}
        <div className="flex justify-end">
          <MagneticButton
            size="lg"
            onClick={handleSubmit}
            loading={loading}
            disabled={filledCount === 0}
            icon={<ArrowRight className="w-4 h-4" />}
            strength={0.4}
          >
            {loading ? "Initiating analysis..." : `Analyze ${filledCount} fingerprint${filledCount !== 1 ? "s" : ""}`}
          </MagneticButton>
        </div>
      </div>

      <FingerGuidanceOverlay
        open={guidanceSlotIndex !== null}
        info={
          guidanceSlotIndex !== null
            ? FINGER_GUIDANCE[FINGER_SLOTS[guidanceSlotIndex].id]
            : null
        }
        onClose={closeGuidance}
        onContinue={continueGuidanceUpload}
      />

      <PalmGuidanceOverlay
        open={palmGuidanceIndex !== null}
        info={
          palmGuidanceIndex !== null
            ? PALM_GUIDANCE[PALM_SLOTS[palmGuidanceIndex].id]
            : null
        }
        onClose={closePalmGuidance}
        onContinue={continuePalmGuidance}
      />
    </div>
  );
}

function CinematicInput({
  label, placeholder, value, onChange, type = "text",
}: {
  label: string; placeholder: string; value: string;
  onChange: (v: string) => void; type?: string;
}) {
  return (
    <div>
      <label className="block text-[10px] text-white/25 uppercase tracking-widest font-mono mb-2">
        {label}
      </label>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-10 rounded-lg px-3 text-sm text-white/80 placeholder-white/15 focus:outline-none transition-all duration-200"
        style={{
          background: "rgba(255,255,255,0.04)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}
        onFocus={(e) => (e.target.style.borderColor = "rgba(0,212,255,0.4)")}
        onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
      />
    </div>
  );
}

function ToggleRow({
  label, sub, checked, onChange, recommended,
}: {
  label: string; sub: string; checked: boolean;
  onChange: (v: boolean) => void; recommended?: boolean;
}) {
  return (
    <div className="flex items-start justify-between gap-6">
      <div>
        <div className="flex items-center gap-2">
          <p className="text-sm font-medium text-white/70">{label}</p>
          {recommended && (
            <span className="text-[9px] px-1.5 py-0.5 rounded font-mono uppercase tracking-wide"
              style={{ background: "rgba(0,212,255,0.1)", color: "#00d4ff", border: "1px solid rgba(0,212,255,0.2)" }}>
              Recommended
            </span>
          )}
        </div>
        <p className="text-xs text-white/25 mt-0.5 leading-relaxed">{sub}</p>
      </div>
      <button
        role="switch"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        className={cn(
          "relative flex-shrink-0 w-10 h-5.5 rounded-full transition-all duration-300 focus:outline-none",
          checked
            ? "bg-gradient-to-r from-[#0ea5e9] to-[#8b5cf6] shadow-[0_0_12px_rgba(0,212,255,0.4)]"
            : "bg-white/[0.08]"
        )}
        style={{ height: "22px", width: "40px" }}
      >
        <span
          className="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-md transition-all duration-300"
          style={{ left: checked ? "calc(100% - 18px)" : "2px" }}
        />
      </button>
    </div>
  );
}
