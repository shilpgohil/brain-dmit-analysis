/** DMIT field knowledge — intelligence types, finger–lobe mapping, platform context */

export interface IntelligenceProfile {
  key: string;
  finger: string;
  fingers: string;
  lobe: string;
  accent: string;
  shortLabel: string;
  description: string;
}

export const INTELLIGENCE_PROFILES: IntelligenceProfile[] = [
  {
    key: "Linguistic",
    finger: "Ring",
    fingers: "L4 / R4 (Ring) + Frontal contribution",
    lobe: "Temporal & Frontal",
    accent: "#c4a574",
    shortLabel: "Word intelligence",
    description:
      "Linguistic intelligence reflects how naturally you absorb, organize, and express language — spoken, written, and symbolic. In DMIT, ring-finger dermatoglyphics (Temporal lobe) correlate with auditory processing, rhythm of speech, and verbal memory, while Frontal contribution supports reasoning with words. A strong profile suggests aptitude for teaching, writing, negotiation, translation, and structured communication. Ridge density and pattern type (loop vs whorl) indicate whether expression is environment-responsive or self-directed.",
  },
  {
    key: "Logical",
    finger: "Index",
    fingers: "L2 / R2 (Index)",
    lobe: "Frontal",
    accent: "#8b9eb7",
    shortLabel: "Reasoning intelligence",
    description:
      "Logical–mathematical intelligence maps to the Frontal lobe via index-finger ridge patterns. It governs sequential thinking, cause-and-effect analysis, abstraction, and quantitative reasoning. In dermatoglyphics, higher ridge counts on L2/R2 suggest stronger cortical allocation for problem decomposition and strategic planning. This dimension is central to engineering, finance, research, coding, and any role requiring structured hypotheses rather than intuition alone.",
  },
  {
    key: "Spatial",
    finger: "Little",
    fingers: "L5 / R5 (Little)",
    lobe: "Occipital",
    accent: "#9d8bb5",
    shortLabel: "Visual intelligence",
    description:
      "Spatial intelligence is tied to the Occipital lobe through the little finger (L5/R5). It covers mental rotation, navigation, design sense, depth perception, and the ability to hold complex visual maps in mind. DMIT reads ridge complexity and fractal dimension here as proxies for visual-processing bandwidth. Strong spatial profiles often excel in architecture, surgery, arts, UX design, and fields where seeing relationships in space matters more than verbal explanation.",
  },
  {
    key: "Musical",
    finger: "Ring",
    fingers: "L4 / R4 (Ring)",
    lobe: "Temporal",
    accent: "#b87d8a",
    shortLabel: "Rhythmic intelligence",
    description:
      "Musical intelligence shares Temporal-lobe pathways with linguistic processing but emphasizes pitch, rhythm, timbre, and emotional tone. Ring-finger patterns in DMIT indicate sensitivity to auditory patterns and harmonic structure. This is not only “playing instruments” — it includes pattern recognition in soundscapes, memorization through melody, and emotional attunement through listening. Whorl patterns may indicate independent creative voice; loops often suggest learning strongly from environment and mentors.",
  },
  {
    key: "Kinesthetic",
    finger: "Middle",
    fingers: "L3 / R3 (Middle)",
    lobe: "Parietal",
    accent: "#6b9e8f",
    shortLabel: "Body intelligence",
    description:
      "Bodily–kinesthetic intelligence connects to the Parietal lobe via middle-finger dermatoglyphics. It reflects proprioception, fine-motor control, coordination, and learning through movement. In DMIT, parietal capacity scores derived from L3/R3 indicate how comfortably you integrate physical action with cognition — sports, dance, surgery, craftsmanship, or hands-on experimentation. High ridge count with whorl patterns often correlates with self-paced physical mastery.",
  },
  {
    key: "Interpersonal",
    finger: "Thumb",
    fingers: "L1 (Left Thumb)",
    lobe: "Prefrontal (left emphasis)",
    accent: "#d4a574",
    shortLabel: "Social intelligence",
    description:
      "Interpersonal intelligence is anchored in the left Prefrontal lobe (L1 — left thumb in CADA mapping). It governs empathy, reading social cues, collaboration, leadership of groups, and adaptive communication across personalities. DMIT interprets thumb-pattern symmetry and ridge volume as indicators of social–emotional bandwidth. Strong interpersonal profiles suit counseling, sales, HR, teaching, politics, and any role requiring trust-building at scale.",
  },
  {
    key: "Intrapersonal",
    finger: "Thumb",
    fingers: "R1 (Right Thumb)",
    lobe: "Prefrontal (right emphasis)",
    accent: "#a89b7c",
    shortLabel: "Self intelligence",
    description:
      "Intrapersonal intelligence maps to the right Prefrontal lobe (R1 — right thumb). It reflects self-awareness, emotional regulation, independent goal-setting, and an internal narrative of identity. In DMIT, contrasting L1 vs R1 patterns reveals balance between outward social drive and inward reflective depth. High intrapersonal capacity supports entrepreneurship, philosophy, deep creative work, and roles requiring sustained focus without external validation.",
  },
  {
    key: "Naturalistic",
    finger: "Little",
    fingers: "L5 / R5 (Little)",
    lobe: "Occipital (pattern recognition)",
    accent: "#7a9e6b",
    shortLabel: "Nature intelligence",
    description:
      "Naturalistic intelligence involves classification of living systems, ecological awareness, and sensitivity to natural patterns — weather, terrain, species, cycles. While linked to Occipital visual processing (little finger), it also draws on Temporal memory for seasonal and environmental rhythms. DMIT treats strong L5/R5 profiles as indicators for biology, agriculture, veterinary science, environmental policy, and observational research disciplines.",
  },
  {
    key: "Existential",
    finger: "Index",
    fingers: "L2 / R2 (Index) + Frontal",
    lobe: "Frontal",
    accent: "#9a8fb5",
    shortLabel: "Meaning intelligence",
    description:
      "Existential intelligence (Gardner’s extended dimension) concerns big-picture questions — purpose, mortality, ethics, and humanity’s place in the cosmos. Frontal-lobe index-finger mapping supports abstract reasoning beyond concrete logic. In DMIT, this emerges when logical capacity combines with high introspective (thumb) balance. It suits theology, philosophy, strategic leadership, and roles requiring long-horizon moral reasoning rather than short-term metrics alone.",
  },
];

export const DMIT_FIELD_SECTIONS = [
  {
    id: "what-is-dmit",
    title: "What is DMIT?",
    body: `Dermatoglyphics Multiple Intelligence Test (DMIT) is a scientific assessment framework that studies fingerprint ridge patterns to infer inborn cognitive tendencies, learning style, and multiple-intelligence distribution. Unlike questionnaires, DMIT relies on biometric data formed during fetal development — fingerprints and the neocortex develop between the 13th and 21st weeks of gestation from the same embryonic layer (ectoderm), which is why dermatoglyphics practitioners correlate ridge features with brain-region activity.`,
  },
  {
    id: "science",
    title: "The Science",
    body: `DMIT integrates dermatoglyphics (ridge flow, cores, deltas, ridge counts), neuroscience (lobe functions), and Howard Gardner's theory of Multiple Intelligences. Ridge count (TFRC), pattern classification (Arch / Loop / Whorl per CADA rules), singular-point detection (Poincaré index), and fractal dimension quantify the physical print. These metrics are normalized into capacity scores before any psychological interpretation — preserving a strict separation between measurable biometrics and DMIT meaning.`,
  },
  {
    id: "finger-lobe",
    title: "Finger–Brain Mapping (CADA)",
    body: `Standard DMIT maps each finger to a cortical region: Thumb (L1/R1) → Prefrontal; Index (L2/R2) → Frontal; Middle (L3/R3) → Parietal; Ring (L4/R4) → Temporal; Little (L5/R5) → Occipital. Left-hand fingers often emphasize receptive/interpersonal functions; right-hand fingers emphasize expressive/intrapersonal functions. Pattern type modulates expression: loops tend toward environment-driven learning; whorls toward self-directed independence.`,
  },
  {
    id: "applications",
    title: "Applications",
    body: `DMIT is used for early talent identification in children, career and stream guidance for students, team composition in HR, couple compatibility counseling, and personal development planning. It is non-invasive — only fingerprint images are required — and results can be generated within minutes when paired with automated analysis pipelines.`,
  },
];

export const PLATFORM_SECTIONS = [
  {
    id: "pipeline",
    title: "Our Analysis Pipeline",
    body: `This platform implements a four-stage deterministic pipeline: (1) Biometric extraction — 85+ features per finger including pattern type, ridge count, singular points, and fractal dimension; (2) Cross-lateral brain-lobe mapping via dmit_intelligence_mapper (finger to lobe, hand to hemisphere); (3) 46 extension modules (leadership, EQ, learning style, career guidance, stress response, and more); (4) Professional PDF report generation with 3D visualizations. Data flows one way: biometrics first, interpretation second — never the reverse.`,
  },
  {
    id: "features",
    title: "Platform Capabilities",
    bullets: [
      "10-finger upload workspace with live scan preview",
      "85 biometric features per dermatoglyphic print",
      "9 Gardner intelligence types + 46 extension modules",
      "Finger-level drill-down with per-print metrics",
      "Session archive with status tracking",
      "PDF export via advanced 3D report generator",
      "FastAPI backend with real-time analysis polling",
    ],
  },
  {
    id: "tech",
    title: "Technology Stack",
    body: `Backend: Python, FastAPI, OpenCV-based preprocessing, optimized feature extractor, DMIT extension engine. Frontend: Next.js 16, TypeScript, Framer Motion, canvas-based fingerprint field visualization, and a cinematic editorial design system. Reports: ReportLab / Plotly with honest handling of missing data (e.g., ATD angles require palm prints and are never fabricated).`,
  },
  {
    id: "integrity",
    title: "Scientific Integrity",
    body: `We distinguish verifiable biometrics from interpretive DMIT theory. Metrics tied to palm-only data (such as ATD angle) are omitted rather than defaulted. Extension scores are derived from measured capacity vectors, not random placeholders. This platform is built for transparency — every chart should trace back to a fingerprint measurement or a documented mapping rule.`,
  },
];
