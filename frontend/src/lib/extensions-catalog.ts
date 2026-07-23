/** Extension modules aligned with dmit_extensions/engine.py registry */

export type ExtensionCategory =
  | "Intelligence"
  | "Emotional & Social"
  | "Cognitive"
  | "Career & Learning"
  | "Leadership & Work"
  | "Health & Wellness"
  | "Specialized";

export interface ExtensionMeta {
  id: string;
  name: string;
  category: ExtensionCategory;
  description: string;
  inputs: string;
  accent: string;
}

export const EXTENSION_CATEGORIES: ExtensionCategory[] = [
  "Intelligence",
  "Emotional & Social",
  "Cognitive",
  "Career & Learning",
  "Leadership & Work",
  "Health & Wellness",
  "Specialized",
];

export const EXTENSIONS_CATALOG: ExtensionMeta[] = [
  { id: "linguistic_intelligence", name: "Linguistic Intelligence", category: "Intelligence", accent: "#c4a574", inputs: "Temporal + Frontal capacity", description: "Verbal fluency, language absorption, and symbolic reasoning from ring- and index-finger patterns." },
  { id: "logical_mathematical_intelligence", name: "Logical–Mathematical", category: "Intelligence", accent: "#8b9eb7", inputs: "Frontal lobe (L2/R2)", description: "Sequential analysis, abstraction, and quantitative reasoning mapped from index-finger ridge density." },
  { id: "spatial_intelligence", name: "Spatial Intelligence", category: "Intelligence", accent: "#9d8bb5", inputs: "Occipital lobe (L5/R5)", description: "Visual-spatial processing, mental rotation, and design thinking from little-finger dermatoglyphics." },
  { id: "bodily_kinesthetic_intelligence", name: "Bodily–Kinesthetic", category: "Intelligence", accent: "#6b9e8f", inputs: "Parietal lobe (L3/R3)", description: "Motor coordination, proprioception, and learning-through-movement from middle-finger capacity." },
  { id: "musical_intelligence", name: "Musical Intelligence", category: "Intelligence", accent: "#b87d8a", inputs: "Temporal lobe (L4/R4)", description: "Rhythm, pitch sensitivity, and auditory pattern recognition from ring-finger mapping." },
  { id: "interpersonal_intelligence", name: "Interpersonal Intelligence", category: "Intelligence", accent: "#d4a574", inputs: "Left Prefrontal (L1)", description: "Social awareness, empathy, and group leadership from left-thumb prefrontal emphasis." },
  { id: "intrapersonal_intelligence", name: "Intrapersonal Intelligence", category: "Intelligence", accent: "#a89b7c", inputs: "Right Prefrontal (R1)", description: "Self-reflection, emotional regulation, and independent goal-setting from right-thumb mapping." },
  { id: "naturalistic_intelligence", name: "Naturalistic Intelligence", category: "Intelligence", accent: "#7a9e6b", inputs: "Occipital + pattern memory", description: "Classification of natural systems and environmental observation from occipital capacity." },
  { id: "emotional_intelligence", name: "Emotional Intelligence", category: "Emotional & Social", accent: "#b87d8a", inputs: "Prefrontal + MI profile", description: "EQ composite: self-awareness, empathy, and emotional regulation across prefrontal-driven scores." },
  { id: "social_awareness", name: "Social Awareness", category: "Emotional & Social", accent: "#c4a574", inputs: "Interpersonal + Temporal", description: "Reading social cues and adapting communication to group dynamics." },
  { id: "relationship_dynamics", name: "Relationship Dynamics", category: "Emotional & Social", accent: "#9d8bb5", inputs: "Interpersonal + Intrapersonal balance", description: "Compatibility patterns in one-to-one and small-group relationships." },
  { id: "communication_style", name: "Communication Style", category: "Emotional & Social", accent: "#8b9eb7", inputs: "Linguistic + Interpersonal", description: "Preferred channels and tone: direct, narrative, visual, or kinesthetic expression." },
  { id: "self_regulation", name: "Self-Regulation", category: "Emotional & Social", accent: "#6b9e8f", inputs: "Intrapersonal + Executive function", description: "Impulse control, focus recovery, and stress modulation capacity." },
  { id: "stress_response", name: "Stress Response", category: "Emotional & Social", accent: "#b87d5c", inputs: "Prefrontal + pattern modifiers", description: "Fight/flight/freeze tendencies under pressure inferred from ridge-pattern expression." },
  { id: "stress_management", name: "Stress Management", category: "Health & Wellness", accent: "#6b9e8f", inputs: "Stress response + wellness", description: "Coping strategies and resilience behaviors aligned with DMIT capacity profile." },
  { id: "attention_focus", name: "Attention & Focus", category: "Cognitive", accent: "#8b9eb7", inputs: "Frontal + Executive function", description: "Sustained attention, task-switching cost, and deep-work capacity." },
  { id: "executive_function", name: "Executive Function", category: "Cognitive", accent: "#9d8bb5", inputs: "Prefrontal + Frontal", description: "Planning, inhibition, working memory, and cognitive flexibility." },
  { id: "cognitive_load", name: "Cognitive Load", category: "Cognitive", accent: "#a89b7c", inputs: "Multi-lobe capacity", description: "Tolerance for simultaneous information streams before performance drops." },
  { id: "memory_processing", name: "Memory Processing", category: "Cognitive", accent: "#c4a574", inputs: "Temporal + Frontal", description: "Encoding, retention, and retrieval styles — verbal vs visual vs procedural." },
  { id: "memory", name: "Memory", category: "Cognitive", accent: "#8b9eb7", inputs: "Temporal lobe", description: "Short- and long-term memory bandwidth from temporal-finger correlation." },
  { id: "meta_cognition", name: "Meta-Cognition", category: "Cognitive", accent: "#9d8bb5", inputs: "Intrapersonal + Logical", description: "Thinking about thinking — self-monitoring and strategy selection in learning." },
  { id: "pattern_recognition", name: "Pattern Recognition", category: "Cognitive", accent: "#7a9e6b", inputs: "Occipital + Fractal dimension", description: "Detecting regularities in complex data; ties to ridge fractal complexity." },
  { id: "decision_making", name: "Decision Making", category: "Cognitive", accent: "#d4a574", inputs: "Frontal + Risk tolerance", description: "Speed vs deliberation, intuitive vs analytical decision preferences." },
  { id: "problem_solving", name: "Problem Solving", category: "Cognitive", accent: "#6b9e8f", inputs: "Logical + Spatial", description: "Approach to novel problems: systematic, creative, or collaborative." },
  { id: "neurodivergence", name: "Neurodivergence Indicators", category: "Specialized", accent: "#9d8bb5", inputs: "Multi-lobe outliers", description: "Non-pathologizing flags for atypical cognitive profiles; requires professional interpretation." },
  { id: "left_right_brain", name: "Left / Right Brain Balance", category: "Specialized", accent: "#8b9eb7", inputs: "Hemisphere capacity split", description: "Analytic vs holistic processing emphasis across hand asymmetry." },
  { id: "learning_style", name: "Learning Style (VAK)", category: "Career & Learning", accent: "#c4a574", inputs: "Occipital, Temporal, Parietal", description: "Visual, auditory, and kinesthetic learning weights from lobe capacities." },
  { id: "learning_agility", name: "Learning Agility", category: "Career & Learning", accent: "#6b9e8f", inputs: "Multi-MI + adaptability", description: "Speed of acquiring new skills in unfamiliar domains." },
  { id: "career_guidance", name: "Career Guidance", category: "Career & Learning", accent: "#d4a574", inputs: "Top MI + extensions", description: "Career clusters and stream recommendations from dominant intelligences." },
  { id: "creativity", name: "Creativity", category: "Career & Learning", accent: "#b87d8a", inputs: "Spatial + Musical + Frontal", description: "Divergent thinking and creative output potential." },
  { id: "creativity_index", name: "Creativity Index", category: "Career & Learning", accent: "#9d8bb5", inputs: "Creativity + pattern type", description: "Quantified creative drive with whorl/loop expression modifiers." },
  { id: "innovation_intelligence", name: "Innovation Intelligence", category: "Career & Learning", accent: "#7a9e6b", inputs: "Creativity + Systems thinking", description: "Ability to introduce novel solutions in structured environments." },
  { id: "innovation_creativity", name: "Innovation & Creativity", category: "Career & Learning", accent: "#c4a574", inputs: "Combined creative metrics", description: "Blend of ideation and implementation capacity for R&D roles." },
  { id: "leadership", name: "Leadership", category: "Leadership & Work", accent: "#d4a574", inputs: "Interpersonal + Executive", description: "General leadership presence and influence style." },
  { id: "leadership_potential", name: "Leadership Potential", category: "Leadership & Work", accent: "#c4a574", inputs: "Prefrontal + Interpersonal", description: "Inborn leadership bandwidth vs learned leadership skills." },
  { id: "leadership_skills", name: "Leadership Skills", category: "Leadership & Work", accent: "#8b9eb7", inputs: "Leadership + Communication", description: "Actionable leadership competencies for management roles." },
  { id: "entrepreneurial_aptitude", name: "Entrepreneurial Aptitude", category: "Leadership & Work", accent: "#b87d5c", inputs: "Intrapersonal + Risk tolerance", description: "Self-starter drive, risk appetite, and venture-fit indicators." },
  { id: "team_collaboration", name: "Team Collaboration", category: "Leadership & Work", accent: "#6b9e8f", inputs: "Interpersonal + Communication", description: "Fit for cross-functional teams and collaborative workflows." },
  { id: "work_style", name: "Work Style", category: "Leadership & Work", accent: "#a89b7c", inputs: "MI + personality proxies", description: "Independent vs collaborative, structured vs flexible work preferences." },
  { id: "time_management", name: "Time Management", category: "Leadership & Work", accent: "#8b9eb7", inputs: "Executive function + Conscientiousness proxy", description: "Planning, prioritization, and deadline orientation." },
  { id: "motivation_drive", name: "Motivation & Drive", category: "Leadership & Work", accent: "#b87d8a", inputs: "Prefrontal + Intrapersonal", description: "Intrinsic vs extrinsic motivation patterns." },
  { id: "persistence_grit", name: "Persistence & Grit", category: "Leadership & Work", accent: "#7a9e6b", inputs: "Pattern type + Frontal", description: "Long-term goal pursuit despite obstacles." },
  { id: "risk_tolerance", name: "Risk Tolerance", category: "Leadership & Work", accent: "#b87d5c", inputs: "Frontal + Entrepreneurial", description: "Comfort with uncertainty and bold decision-making." },
  { id: "systems_thinking", name: "Systems Thinking", category: "Specialized", accent: "#9d8bb5", inputs: "Logical + Spatial", description: "Seeing interconnections across complex systems." },
  { id: "adaptability_resilience", name: "Adaptability & Resilience", category: "Health & Wellness", accent: "#6b9e8f", inputs: "Multi-lobe flexibility", description: "Recovery from change and setbacks." },
  { id: "health_wellness", name: "Health & Wellness", category: "Health & Wellness", accent: "#7a9e6b", inputs: "Parietal + stress modules", description: "Mind-body awareness and wellness-oriented behaviors." },
  { id: "wellness_intelligence", name: "Wellness Intelligence", category: "Health & Wellness", accent: "#6b9e8f", inputs: "Health + self-regulation", description: "Holistic wellbeing and lifestyle alignment score." },
  { id: "curiosity_exploratory", name: "Curiosity & Exploration", category: "Specialized", accent: "#c4a574", inputs: "Naturalistic + Openness proxy", description: "Drive to explore new domains and ask questions." },
  { id: "cultural_intelligence", name: "Cultural Intelligence", category: "Specialized", accent: "#d4a574", inputs: "Interpersonal + Linguistic", description: "Cross-cultural communication and adaptation." },
  { id: "digital_intelligence", name: "Digital Intelligence", category: "Specialized", accent: "#8b9eb7", inputs: "Logical + Spatial + Learning agility", description: "Affinity for digital tools, systems, and rapid tech adoption." },
  { id: "financial_intelligence", name: "Financial Intelligence", category: "Specialized", accent: "#a89b7c", inputs: "Logical + Risk tolerance", description: "Numeracy, planning, and resource management aptitudes." },
  { id: "sustainability_intelligence", name: "Sustainability Intelligence", category: "Specialized", accent: "#7a9e6b", inputs: "Naturalistic + Systems", description: "Environmental ethics and long-horizon ecological thinking." },
];
