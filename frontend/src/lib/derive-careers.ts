import type { AnalysisResult, CareerMatch, ExtensionResult } from "./types";

const CAREER_KEYS: Record<string, string> = {
  technical_career: "Technology & Engineering",
  creative_career: "Arts, Media & Design",
  analytical_career: "Research & Analysis",
  leadership_career: "Management & Leadership",
  social_career: "People & Service",
  administrative_career: "Operations & Administration",
  research_career: "Science & Investigation",
  entrepreneurial_career: "Entrepreneurship & Ventures",
  stem_careers: "STEM Cluster",
  arts_media_careers: "Arts & Media Cluster",
  business_careers: "Business Cluster",
  service_careers: "Service Cluster",
  innovation_careers: "Innovation Cluster",
};

export function deriveCareerMatches(result: AnalysisResult): CareerMatch[] {
  if (result.career_matches.length > 0) {
    return [...result.career_matches].sort((a, b) => b.match_score - a.match_score);
  }

  const guidance = result.extensions.find(
    (e) => e.name.toLowerCase().includes("career guidance")
  );
  if (!guidance) return [];

  const matches: CareerMatch[] = [];
  for (const [key, title] of Object.entries(CAREER_KEYS)) {
    const score = guidance.scores[key];
    if (typeof score === "number" && score > 0) {
      matches.push({
        title,
        category: key.includes("cluster") ? "Cluster" : "Career",
        match_score: score,
        key_strengths: [],
      });
    }
  }
  return matches.sort((a, b) => b.match_score - a.match_score);
}

export function getCareerGuidanceExtension(extensions: ExtensionResult[]) {
  return extensions.find((e) => e.name.toLowerCase().includes("career guidance"));
}
