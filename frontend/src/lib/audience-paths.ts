export type AudienceId = "individual" | "clinic" | "institution" | "showcase";

export interface AudiencePath {
  id: AudienceId;
  title: string;
  subtitle: string;
  description: string;
  cta: string;
  href: string;
  features: string[];
  accent: string;
}

export const AUDIENCE_PATHS: AudiencePath[] = [
  {
    id: "individual",
    title: "At Home",
    subtitle: "Audience A",
    description:
      "Take the test yourself or for your child. Upload ten fingerprint images from your phone or scanner and receive a full intelligence profile with PDF — no counselor required.",
    cta: "Start My Analysis",
    href: "/analysis/new",
    features: [
      "Guided 10-finger upload",
      "Plain-English intelligence tooltips",
      "Instant PDF download",
      "Learn DMIT in /learn",
    ],
    accent: "#c4a574",
  },
  {
    id: "clinic",
    title: "Counselor & Clinic",
    subtitle: "Audience B",
    description:
      "Run many client sessions, compare profiles, explore 46 extension modules, and archive every analysis. Built for professional DMIT practitioners.",
    cta: "Open Sessions",
    href: "/sessions",
    features: [
      "Client archive & compare",
      "Extension explorer",
      "Session notes (notes field)",
      "Branded PDF (roadmap)",
    ],
    accent: "#9d8bb5",
  },
  {
    id: "institution",
    title: "School & Corporate",
    subtitle: "Audience C",
    description:
      "Batch assessments for classrooms, teams, and HR. Aggregate talent maps and career guidance at scale — cohort features on the roadmap.",
    cta: "View Solutions",
    href: "/solutions#institution",
    features: [
      "Batch cohorts (planned)",
      "Team comparison",
      "Aggregate MI charts (planned)",
      "Consent & privacy flows (planned)",
    ],
    accent: "#6b9e8f",
  },
  {
    id: "showcase",
    title: "Investors & Partners",
    subtitle: "Audience D",
    description:
      "See the full pipeline: 85 biometric features, 9 intelligences, 46 extensions, cinematic UX, and a deterministic Python engine with FastAPI + Next.js.",
    cta: "System Overview",
    href: "/system",
    features: [
      "Live health & stack",
      "Architecture transparency",
      "Extension breadth proof",
      "Premium demo UX",
    ],
    accent: "#e8dcc8",
  },
];
