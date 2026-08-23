/** Per-slot capture guidance for the biometric intake flow. */

export interface FingerGuidanceInfo {
  slotId: string;
  label: string;
  hand: "right" | "left";
  fingerKey: "thumb" | "index" | "middle" | "ring" | "little";
  short: string;
  placementTip: string;
  scannerTip: string;
}

export const FINGER_GUIDANCE: Record<string, FingerGuidanceInfo> = {
  R1: {
    slotId: "R1",
    label: "Right Thumb",
    hand: "right",
    fingerKey: "thumb",
    short: "RT",
    placementTip: "Place the pad of your right thumb flat on the scanner or hold it steady for a clear photo.",
    scannerTip: "On a USB scanner: center the thumb, press lightly, capture one flat image.",
  },
  R2: {
    slotId: "R2",
    label: "Right Index",
    hand: "right",
    fingerKey: "index",
    short: "RI",
    placementTip: "Extend your right index finger and align the full ridge area within the frame.",
    scannerTip: "Roll slightly left and right only if your scanner workflow requires side ridges.",
  },
  R3: {
    slotId: "R3",
    label: "Right Middle",
    hand: "right",
    fingerKey: "middle",
    short: "RM",
    placementTip: "Keep the right middle finger straight; avoid overlapping adjacent fingers.",
    scannerTip: "Dry the finger before scanning to prevent smudged ridge detail.",
  },
  R4: {
    slotId: "R4",
    label: "Right Ring",
    hand: "right",
    fingerKey: "ring",
    short: "RR",
    placementTip: "Capture the full print area of the right ring finger with even lighting.",
    scannerTip: "Scanner BMP exports are ideal — they are auto-detected and skip phone preprocessing.",
  },
  R5: {
    slotId: "R5",
    label: "Right Little",
    hand: "right",
    fingerKey: "little",
    short: "RL",
    placementTip: "Place the right little finger carefully; small prints need sharp focus.",
    scannerTip: "If the image looks blurry, recapture before continuing.",
  },
  L1: {
    slotId: "L1",
    label: "Left Thumb",
    hand: "left",
    fingerKey: "thumb",
    short: "LT",
    placementTip: "Place the pad of your left thumb flat, covering the capture area.",
    scannerTip: "Label files L1.bmp (or similar) so bulk upload assigns the correct slot.",
  },
  L2: {
    slotId: "L2",
    label: "Left Index",
    hand: "left",
    fingerKey: "index",
    short: "LI",
    placementTip: "Extend the left index finger with the nail pointing upward in the frame.",
    scannerTip: "Use consistent naming (L2.jpg) when uploading a full scanner batch.",
  },
  L3: {
    slotId: "L3",
    label: "Left Middle",
    hand: "left",
    fingerKey: "middle",
    short: "LM",
    placementTip: "Isolate the left middle finger from the ring and index fingers.",
    scannerTip: "Avoid shadows across the ridge pattern.",
  },
  L4: {
    slotId: "L4",
    label: "Left Ring",
    hand: "left",
    fingerKey: "ring",
    short: "LR",
    placementTip: "Center the left ring finger print with clear ridge contrast.",
    scannerTip: "Phone photos work, but scanner images give the most reliable ridge counts.",
  },
  L5: {
    slotId: "L5",
    label: "Left Little",
    hand: "left",
    fingerKey: "little",
    short: "LL",
    placementTip: "Capture the entire left little finger — edges are easy to crop out.",
    scannerTip: "After all ten fingers, add optional palm images in the Palm Prints section below.",
  },
};

// ── Palm guidance ────────────────────────────────────────────────────────────

export interface PalmGuidanceInfo {
  slotId: "LPALM" | "RPALM";
  label: string;
  hand: "left" | "right";
  placementTip: string;
  scannerTip: string;
  atdTip: string;
}

export const PALM_GUIDANCE: Record<string, PalmGuidanceInfo> = {
  LPALM: {
    slotId: "LPALM",
    label: "Left Palm",
    hand: "left",
    placementTip:
      "Hold your left palm flat, fingers together, facing the camera directly. " +
      "Ensure the full palm — from wrist crease to fingertip bases — is inside the frame.",
    scannerTip:
      "For the best ATD angle result, use a ridge-grade palm scanner at 500 DPI. " +
      "A phone photo is accepted and stored, but will yield a geometric estimate only.",
    atdTip:
      "The ATD angle is formed by three triradius landmarks: " +
      "a-point (below the index finger), t-point (center of the palm), " +
      "and d-point (below the little finger). Keep the palm well-lit with no shadows across the center.",
  },
  RPALM: {
    slotId: "RPALM",
    label: "Right Palm",
    hand: "right",
    placementTip:
      "Hold your right palm flat, fingers together, facing the camera directly. " +
      "The wrist crease and all four finger-base creases should be visible.",
    scannerTip:
      "For the best ATD angle result, use a ridge-grade palm scanner at 500 DPI. " +
      "A phone photo is accepted and stored, but will yield a geometric estimate only.",
    atdTip:
      "The ATD angle is formed by three triradius landmarks: " +
      "a-point (below the index finger), t-point (center of the palm), " +
      "and d-point (below the little finger). Keep the palm well-lit with no shadows across the center.",
  },
};

export const GUIDANCE_ONBOARDING_KEY = "dmit_upload_guidance_seen";
export const PALM_GUIDANCE_KEY = "dmit_palm_guidance_seen";

export function hasSeenUploadGuidance(): boolean {
  if (typeof window === "undefined") return true;
  return window.localStorage.getItem(GUIDANCE_ONBOARDING_KEY) === "true";
}

export function markUploadGuidanceSeen(): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(GUIDANCE_ONBOARDING_KEY, "true");
}

export function hasSeenPalmGuidance(): boolean {
  if (typeof window === "undefined") return true;
  return window.localStorage.getItem(PALM_GUIDANCE_KEY) === "true";
}

export function markPalmGuidanceSeen(): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(PALM_GUIDANCE_KEY, "true");
}
