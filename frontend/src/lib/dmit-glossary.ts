export interface GlossaryTerm {
  term: string;
  short: string;
  detail: string;
}

export const DMIT_GLOSSARY: GlossaryTerm[] = [
  { term: "DMIT", short: "Dermatoglyphics Multiple Intelligence Test", detail: "A scientific assessment combining fingerprint ridge analysis with Howard Gardner's Multiple Intelligence theory to profile inborn cognitive tendencies." },
  { term: "Dermatoglyphics", short: "Study of skin ridge patterns", detail: "The scientific field examining fingerprints, palm prints, and sole patterns — formed permanently during fetal development." },
  { term: "CADA", short: "Classification standard", detail: "Rules for classifying fingerprint patterns as Arch (0 deltas), Loop (1 delta), or Whorl (2 deltas) based on singular points." },
  { term: "TFRC", short: "Total Finger Ridge Count", detail: "Count of ridges between core and delta along a defined line — a key quantitative biometric per finger." },
  { term: "Core", short: "Ridge center point", detail: "Singular point where ridges form a loop or whorl center; detected via Poincaré index +0.5 in the orientation field." },
  { term: "Delta", short: "Triradius", detail: "Singular point where three ridge systems meet; Poincaré index −0.5. Loops have one delta; whorls typically two." },
  { term: "ATD Angle", short: "Palm metric", detail: "Angle between a-t and d triradii on the palm — requires palm print, not fingerprint alone. Omitted when unavailable." },
  { term: "Capacity Score", short: "0–1 normalized ridge strength", detail: "Ridge count normalized against baseline (e.g. /25) to represent cortical allocation proxy per finger." },
  { term: "Multiple Intelligence", short: "Gardner's 8+1 framework", detail: "Distinct cognitive abilities (linguistic, logical, spatial, etc.) rather than a single IQ number." },
  { term: "Extension Module", short: "Derived profile dimension", detail: "Post-mapping analysis (EQ, career, leadership…) computed from capacity vectors and pattern modifiers." },
  { term: "Pattern Modifier", short: "Whorl / Loop expression", detail: "Whorls may add independence weight; loops may add environment-responsiveness — without changing raw ridge count." },
  { term: "Fractal Dimension", short: "Ridge complexity measure", detail: "Box-counting dimension of the binarized print — higher values suggest denser, more complex ridge topology." },
];

export interface FingerEncyclopediaEntry {
  id: string;
  name: string;
  hand: "Left" | "Right";
  lobe: string;
  intelligences: string[];
  narrative: string;
}

export const FINGER_ENCYCLOPEDIA: FingerEncyclopediaEntry[] = [
  { id: "L1", name: "Left Thumb", hand: "Left", lobe: "Prefrontal", intelligences: ["Interpersonal", "Social awareness"], narrative: "Left thumb (L1) maps to the prefrontal region with emphasis on outward social processing — empathy, group dynamics, and reading others." },
  { id: "R1", name: "Right Thumb", hand: "Right", lobe: "Prefrontal", intelligences: ["Intrapersonal", "Self-regulation"], narrative: "Right thumb (R1) reflects inward prefrontal capacity — self-awareness, emotional regulation, and independent executive goals." },
  { id: "L2", name: "Left Index", hand: "Left", lobe: "Frontal", intelligences: ["Logical", "Existential"], narrative: "Index fingers (L2/R2) tie to frontal-lobe reasoning — logic, planning, and abstract meaning-making." },
  { id: "R2", name: "Right Index", hand: "Right", lobe: "Frontal", intelligences: ["Logical", "Existential"], narrative: "The right index contributes to expressive and strategic application of frontal logical capacity." },
  { id: "L3", name: "Left Middle", hand: "Left", lobe: "Parietal", intelligences: ["Kinesthetic"], narrative: "Middle fingers map to parietal somatosensory integration — body coordination, athletics, craftsmanship." },
  { id: "R3", name: "Right Middle", hand: "Right", lobe: "Parietal", intelligences: ["Kinesthetic"], narrative: "Right middle finger supports fine-motor expression of parietal kinesthetic strength." },
  { id: "L4", name: "Left Ring", hand: "Left", lobe: "Temporal", intelligences: ["Musical", "Linguistic"], narrative: "Ring fingers connect to temporal processing — language rhythm, music, and auditory memory." },
  { id: "R4", name: "Right Ring", hand: "Right", lobe: "Temporal", intelligences: ["Musical", "Linguistic"], narrative: "Right ring finger emphasizes expressive and performative aspects of temporal intelligence." },
  { id: "L5", name: "Left Little", hand: "Left", lobe: "Occipital", intelligences: ["Spatial", "Naturalistic"], narrative: "Little fingers map to occipital visual processing — spatial design, observation, and pattern recognition in nature." },
  { id: "R5", name: "Right Little", hand: "Right", lobe: "Occipital", intelligences: ["Spatial", "Naturalistic"], narrative: "Right little finger supports active visual-spatial output and environmental scanning." },
];
