export type AnalysisStatus =
  | "pending"
  | "preprocessing"
  | "extracting"
  | "mapping"
  | "extending"
  | "generating_report"
  | "completed"
  | "failed";

export type PatternType = "whorl" | "loop" | "arch" | "accidental" | "unknown";

export interface SingularPoint {
  x: number;
  y: number;
  type: "core" | "delta";
}

export interface FingerBiometrics {
  finger_id: string;
  finger_type: string;
  finger_position?: string;
  pattern_type: PatternType;
  pattern_subtype?: string;
  ridge_count?: number;
  fractal_dimension?: number;
  quality_score?: number;
  quality_tier?: string;
  singular_points?: SingularPoint[];
  minutiae_count?: number;
  entropy?: number;
  image_path?: string;
  thumbnail_url?: string;
  raw_features?: Record<string, number>;
}

export interface LobeHemispheres {
  left: number | null;
  right: number | null;
}

export interface BrainLobeCapacity {
  prefrontal_lobe: number | null;
  posterior_frontal: number | null;
  parietal_lobe: number | null;
  temporal_lobe: number | null;
  occipital_lobe: number | null;
  left_hemisphere: number | null;
  right_hemisphere: number | null;
  dominant_hemisphere?: "left" | "right" | "balanced" | null;
  lobe_hemispheres?: Record<string, LobeHemispheres> | null;
}

export interface MultipleIntelligences {
  linguistic: number | null;
  logical_mathematical: number | null;
  spatial: number | null;
  musical: number | null;
  bodily_kinesthetic: number | null;
  interpersonal: number | null;
  intrapersonal: number | null;
  naturalistic: number | null;
  existential: number | null;
}

export interface LearningStyles {
  visual: number | null;
  auditory: number | null;
  kinesthetic: number | null;
}

export interface PersonalityProfile {
  openness: number | null;
  conscientiousness: number | null;
  extraversion: number | null;
  agreeableness: number | null;
  neuroticism: number | null;
}

export interface AtdHand {
  angle_deg: number;
  range_category: string;
  learning_speed: number;
  fine_motor_capacity: number;
  sensory_sensitivity: number;
  interpretation: string;
  method?: string | null;
  confidence?: number | null;
  source_note?: string | null;
}

export interface AtdAnalysis {
  left_hand?: AtdHand | null;
  right_hand?: AtdHand | null;
  summary?: string | null;
}

export interface PalmCapture {
  hand: string;
  slot: string;
  thumbnail_url?: string | null;
  status: string;
}

export interface ExtensionResult {
  name: string;
  category: string;
  scores: Record<string, number>;
  primary_score: number;
  description?: string;
  recommendations?: string[];
}

export interface CareerMatch {
  title: string;
  category: string;
  match_score: number;
  key_strengths: string[];
}

export interface PipelineStage {
  id: string;
  label: string;
  status: "pending" | "running" | "completed" | "failed";
  duration_ms?: number;
  detail?: string;
}

export interface AnalysisSession {
  id: string;
  subject_name?: string;
  subject_age?: number;
  created_at: string;
  updated_at: string;
  status: AnalysisStatus;
  finger_count: number;
  completed_fingers: number;
  pipeline_stages: PipelineStage[];
}

export interface AnalysisResult {
  session_id: string;
  status: AnalysisStatus;
  subject_name?: string;
  created_at: string;
  error_message?: string;
  fingers: FingerBiometrics[];
  brain_lobes?: BrainLobeCapacity;
  multiple_intelligences?: MultipleIntelligences;
  learning_styles?: LearningStyles;
  personality?: PersonalityProfile;
  atd_analysis?: AtdAnalysis | null;
  palms?: PalmCapture[];
  extensions: ExtensionResult[];
  career_matches: CareerMatch[];
  pipeline_stages: PipelineStage[];
  report_url?: string;
  processing_time_ms?: number;
  total_features_extracted: number;
  warnings: string[];
}

export interface SessionListItem {
  id: string;
  subject_name?: string;
  created_at: string;
  status: AnalysisStatus;
  finger_count: number;
  has_report: boolean;
}

export interface SystemStatus {
  status: string;
  pipeline_version: string;
  components: Record<string, boolean>;
  total_sessions: number;
  processing_queue: number;
}
