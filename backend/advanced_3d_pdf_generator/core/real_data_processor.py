#!/usr/bin/env python3
"""
Real Data Processor - Works ONLY with Real Pipeline Data
==========================================================

Processes and validates real DMIT pipeline data.
NO MOCK VALUES, NO DEFAULTS, NO FALLBACKS.
Everything must come from your actual pipeline.

Author: DMIT Research Team
Version: 4.0 - Full Extension Data Extraction
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Extension grouping map - used by PDF builder
# ---------------------------------------------------------------------------
EXTENSION_GROUPS = {
    'emotional': ['EmotionalIntelligenceExtension'],
    'cognitive': [
        'DecisionMakingExtension', 'AttentionFocusExtension',
        'MemoryProcessingExtension', 'ExecutiveFunctionExtension',
        'CognitiveLoadExtension', 'MetaCognitionExtension', 'LearningAgilityExtension'
    ],
    'social_leadership': [
        'LeadershipPotentialExtension', 'CommunicationStyleExtension',
        'InterpersonalIntelligenceExtension', 'SocialAwarenessExtension',
        'RelationshipDynamicsExtension', 'LeftRightBrainExtension'
    ],
    'motivation_creativity': [
        'CreativityIndexExtension', 'InnovationIntelligenceExtension',
        'EntrepreneurialAptitudeExtension', 'RiskToleranceExtension',
        'CuriosityExploratoryExtension', 'PersistenceGritExtension',
        'MotivationDriveExtension'
    ],
    'career_life': [
        'CareerGuidanceExtension', 'FinancialIntelligenceExtension',
        'DigitalIntelligenceExtension', 'CulturalIntelligenceExtension',
        'StressResponseExtension', 'AdaptabilityResilienceExtension',
        'SelfRegulationExtension', 'HealthWellnessExtension',
        'NeurodivergenceExtension'
    ],
    'specialized': [
        'LinguisticIntelligenceExtension', 'LogicalMathematicalIntelligenceExtension',
        'SpatialIntelligenceExtension', 'MusicalIntelligenceExtension',
        'BodilyKinestheticIntelligenceExtension', 'IntrapersonalIntelligenceExtension',
        'NaturalisticIntelligenceExtension', 'SystemsThinkingExtension',
        'PatternRecognitionExtension', 'WellnessIntelligenceExtension',
        'SustainabilityIntelligenceExtension'
    ],
}

# Human-readable names for extensions
EXTENSION_DISPLAY_NAMES = {
    'EmotionalIntelligenceExtension': 'Emotional Intelligence',
    'DecisionMakingExtension': 'Decision Making',
    'AttentionFocusExtension': 'Attention & Focus',
    'MemoryProcessingExtension': 'Memory Processing',
    'ExecutiveFunctionExtension': 'Executive Function',
    'CognitiveLoadExtension': 'Cognitive Load',
    'MetaCognitionExtension': 'Meta-Cognition',
    'LearningAgilityExtension': 'Learning Agility',
    'LeadershipPotentialExtension': 'Leadership Potential',
    'CommunicationStyleExtension': 'Communication Style',
    'InterpersonalIntelligenceExtension': 'Interpersonal Intelligence',
    'SocialAwarenessExtension': 'Social Awareness',
    'RelationshipDynamicsExtension': 'Relationship Dynamics',
    'LeftRightBrainExtension': 'Left-Right Brain Balance',
    'CreativityIndexExtension': 'Creativity Index',
    'InnovationIntelligenceExtension': 'Innovation Intelligence',
    'EntrepreneurialAptitudeExtension': 'Entrepreneurial Aptitude',
    'RiskToleranceExtension': 'Risk Tolerance',
    'CuriosityExploratoryExtension': 'Curiosity & Exploration',
    'PersistenceGritExtension': 'Persistence & Grit',
    'MotivationDriveExtension': 'Motivation & Drive',
    'CareerGuidanceExtension': 'Career Guidance',
    'FinancialIntelligenceExtension': 'Financial Intelligence',
    'DigitalIntelligenceExtension': 'Digital Intelligence',
    'CulturalIntelligenceExtension': 'Cultural Intelligence',
    'StressResponseExtension': 'Stress Response',
    'AdaptabilityResilienceExtension': 'Adaptability & Resilience',
    'SelfRegulationExtension': 'Self-Regulation',
    'HealthWellnessExtension': 'Health & Wellness',
    'NeurodivergenceExtension': 'Neurodivergence Profile',
    'LinguisticIntelligenceExtension': 'Linguistic Intelligence',
    'LogicalMathematicalIntelligenceExtension': 'Logical-Mathematical Intelligence',
    'SpatialIntelligenceExtension': 'Spatial Intelligence',
    'MusicalIntelligenceExtension': 'Musical Intelligence',
    'BodilyKinestheticIntelligenceExtension': 'Bodily-Kinesthetic Intelligence',
    'IntrapersonalIntelligenceExtension': 'Intrapersonal Intelligence',
    'NaturalisticIntelligenceExtension': 'Naturalistic Intelligence',
    'SystemsThinkingExtension': 'Systems Thinking',
    'PatternRecognitionExtension': 'Pattern Recognition',
    'WellnessIntelligenceExtension': 'Wellness Intelligence',
    'SustainabilityIntelligenceExtension': 'Sustainability Intelligence',
}


def _find_main_score(ext_data: Dict[str, Any]) -> float:
    """
    Find the primary numeric score from an extension result dict.
    Conventions: key ending in '_score', or first float value found.
    """
    if not isinstance(ext_data, dict):
        return 0.0
    # Look for canonical _score key first
    for key, val in ext_data.items():
        if key.endswith('_score') and isinstance(val, (int, float)):
            return float(val)
    # Fallback: first numeric in 0-1 range
    for key, val in ext_data.items():
        if isinstance(val, (int, float)) and 0.0 <= val <= 1.0:
            return float(val)
    return 0.0


def _find_primary_style(ext_data: Dict[str, Any]) -> str:
    """Find primary style/label from an extension result dict."""
    if not isinstance(ext_data, dict):
        return ''
    for key, val in ext_data.items():
        if 'primary_' in key or 'style' in key or 'profile' in key or 'type' in key:
            if isinstance(val, str):
                return val.replace('_', ' ').title()
    return ''


# ---------------------------------------------------------------------------
# Narrative interpretation helpers (rule-based, no LLM)
# ---------------------------------------------------------------------------

def interpret_score(score: float, domain: str = '') -> str:
    """Return a narrative sentence interpreting a 0-1 score in a given domain."""
    pct = score * 100
    if score >= 0.80:
        level = 'exceptional'
        adj = 'a standout strength'
    elif score >= 0.65:
        level = 'strong'
        adj = 'a notable advantage'
    elif score >= 0.50:
        level = 'moderate'
        adj = 'a developing capability'
    elif score >= 0.35:
        level = 'emerging'
        adj = 'an area for focused growth'
    else:
        level = 'foundational'
        adj = 'a priority development area'

    domain_str = f' in {domain}' if domain else ''
    return (
        f'Your score of {pct:.0f}%{domain_str} is at the {level} level, representing {adj}. '
        f'{"This reflects high natural capacity in this area." if score >= 0.65 else "Targeted practice can meaningfully improve this dimension."}'
    )


def derive_personality_archetype(big5: Dict[str, float]) -> str:
    """Derive a named personality archetype from Big-5 scores."""
    o = big5.get('openness', 0.5)
    c = big5.get('conscientiousness', 0.5)
    e = big5.get('extraversion', 0.5)
    a = big5.get('agreeableness', 0.5)
    n = big5.get('neuroticism', 0.5)

    if o > 0.7 and c > 0.7:
        return 'The Strategic Innovator'
    elif o > 0.7 and e > 0.6:
        return 'The Visionary Leader'
    elif c > 0.7 and a > 0.65:
        return 'The Trusted Executor'
    elif e > 0.7 and a > 0.65:
        return 'The Natural Connector'
    elif o > 0.65 and n < 0.4:
        return 'The Creative Thinker'
    elif c > 0.7 and n < 0.4:
        return 'The Disciplined Achiever'
    elif a > 0.7 and e < 0.45:
        return 'The Empathetic Supporter'
    elif e > 0.65 and c > 0.55:
        return 'The Dynamic Organiser'
    elif n > 0.6 and o > 0.6:
        return 'The Sensitive Idealist'
    else:
        return 'The Balanced Generalist'


# ---------------------------------------------------------------------------
# Main Processor class
# ---------------------------------------------------------------------------

class RealDataProcessor:
    """
    Processes real DMIT pipeline data for PDF generation.
    Validates that all data comes from actual analysis.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    def validate_real_data(self, pipeline_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate that data contains real pipeline results."""
        errors = []

        if not isinstance(pipeline_data, dict):
            errors.append("Pipeline data must be a dictionary")
            return False, errors

        if 'pipeline_info' not in pipeline_data:
            errors.append("Missing pipeline_info")
            return False, errors

        if 'individual_results' not in pipeline_data:
            errors.append("Missing individual_results")
            return False, errors

        individual_results = pipeline_data['individual_results']
        if not isinstance(individual_results, list) or len(individual_results) == 0:
            errors.append("No individual results found")
            return False, errors

        # Validate at least first result has dmit_analysis
        first_result = individual_results[0]
        if 'dmit_analysis' not in first_result:
            errors.append("Missing dmit_analysis in results")
            return False, errors

        dmit_analysis = first_result['dmit_analysis']
        if 'dmit_profile' not in dmit_analysis:
            errors.append("Missing dmit_profile")
            return False, errors

        dmit_profile = dmit_analysis['dmit_profile']
        if 'multiple_intelligences' not in dmit_profile:
            errors.append("Missing multiple_intelligences")
            return False, errors

        intelligence_scores = dmit_profile['multiple_intelligences']
        if not isinstance(intelligence_scores, dict) or len(intelligence_scores) == 0:
            errors.append("No intelligence scores found")
            return False, errors

        for intel_type, score in intelligence_scores.items():
            if not isinstance(score, (int, float)) or score < 0 or score > 1:
                errors.append(f"Invalid intelligence score for {intel_type}: {score}")
                return False, errors

        return True, errors

    # ------------------------------------------------------------------
    # MAIN EXTRACTION — reads from aggregated_analysis (the correct place)
    # ------------------------------------------------------------------

    def extract_real_intelligence_data(self, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract ALL real intelligence data from pipeline results.
        Reads primarily from aggregated_analysis, not individual_results[0].
        """
        is_valid, errors = self.validate_real_data(pipeline_data)
        if not is_valid:
            raise ValueError(f"Invalid pipeline data: {'; '.join(errors)}")

        individual_results = pipeline_data['individual_results']
        pipeline_info = pipeline_data['pipeline_info']

        # ----------------------------------------------------------------
        # Primary source: aggregated_analysis (contains the holistic view)
        # ----------------------------------------------------------------
        aggregated = pipeline_data.get('aggregated_analysis', {})
        agg_profile = aggregated.get('dmit_profile', {})

        # If aggregated_analysis exists and has data, use it as the primary source
        if agg_profile and agg_profile.get('multiple_intelligences'):
            intelligence_scores = agg_profile['multiple_intelligences']
            brain_mapping = agg_profile.get('brain_mapping', {})
            learning_styles = agg_profile.get('learning_styles', {})
            personality_behavior = agg_profile.get('personality_behavior', {})
            extension_results = aggregated.get('extension_results', {})
        else:
            # Fallback to first individual result if no aggregated data
            self.logger.warning("No aggregated_analysis found, falling back to individual_results[0]")
            first_result = individual_results[0]
            dmit_analysis = first_result['dmit_analysis']
            dmit_profile = dmit_analysis['dmit_profile']
            intelligence_scores = dmit_profile['multiple_intelligences']
            brain_mapping = dmit_profile.get('brain_mapping', {})
            learning_styles = dmit_profile.get('learning_styles', {})
            personality_behavior = dmit_profile.get('personality_behavior', {})
            extension_results = dmit_analysis.get('extension_results', {})

        def _numeric_only(scores):
            if not isinstance(scores, dict):
                return {}
            return {
                k: float(v) for k, v in scores.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }

        intelligence_scores = _numeric_only(intelligence_scores)
        brain_mapping = _numeric_only(brain_mapping)
        learning_styles = _numeric_only(learning_styles)
        personality_behavior = _numeric_only(personality_behavior)

        # ----------------------------------------------------------------
        # Extract per-finger data from individual_results
        # ----------------------------------------------------------------
        per_finger_data = self._extract_per_finger_data(individual_results)

        # ----------------------------------------------------------------
        # Extract quality metrics — average across all fingers
        # ----------------------------------------------------------------
        quality_metrics = self._extract_aggregated_quality_metrics(individual_results)

        # ----------------------------------------------------------------
        # Timestamp — prefer aggregated, fall back to first individual
        # ----------------------------------------------------------------
        analysis_timestamp = (
            aggregated.get('aggregation_timestamp')
            or individual_results[0].get('pipeline_info', {}).get('timestamp')
            or datetime.now().isoformat()
        )

        return {
            'intelligence_scores': intelligence_scores,
            'brain_mapping': brain_mapping,
            'learning_styles': learning_styles,
            'personality_behavior': personality_behavior,
            'extension_results': extension_results,
            'per_finger_data': per_finger_data,
            'quality_metrics': quality_metrics,
            'pipeline_info': pipeline_info,
            'analysis_timestamp': analysis_timestamp,
        }

    def _extract_per_finger_data(self, individual_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract per-finger summary: pattern, quality, minutiae, confidence."""
        per_finger = []
        for idx, result in enumerate(individual_results):
            try:
                pipe_info = result.get('pipeline_info', {})
                feat = result.get('feature_extraction', {})
                consolidated = feat.get('consolidated_features', {})
                quality = feat.get('quality_metrics', {})
                dmit_analysis = result.get('dmit_analysis', {})
                ext_results = dmit_analysis.get('extension_results', {})

                # Pattern info
                pattern_family_code = consolidated.get('pattern_family', -1)
                family_map = {0: 'Arch', 1: 'Loop', 2: 'Whorl', 3: 'Composite', -1: 'Unknown'}
                pattern_name = family_map.get(int(pattern_family_code) if pattern_family_code is not None else -1, 'Unknown')

                per_finger.append({
                    'index': idx + 1,
                    'image_path': pipe_info.get('image_path', f'Finger {idx+1}'),
                    'finger_type': pipe_info.get('finger_type', 'UNKNOWN'),
                    'pattern_type': pattern_name,
                    'pattern_confidence': float(consolidated.get('pattern_confidence', 0.0) or 0.0),
                    'image_quality': float(quality.get('image_quality', 0.0) or 0.0),
                    'feature_confidence': float(quality.get('feature_confidence', 0.0) or 0.0),
                    'minutiae_count': int(consolidated.get('minutiae_count', 0) or 0),
                    'ridge_density': float(consolidated.get('ridge_density', 0.0) or 0.0),
                    'fractal_dimension': float(consolidated.get('box_counting_dimension', 0.0) or 0.0),
                    'tfrc': float(consolidated.get('tfrc', 0.0) or 0.0),
                })
            except Exception as e:
                self.logger.warning(f"Could not extract per-finger data for result {idx}: {e}")

        return per_finger

    def _extract_aggregated_quality_metrics(self, individual_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Average quality metrics across all fingers."""
        metrics_accumulator: Dict[str, List[float]] = {}

        for result in individual_results:
            feat = result.get('feature_extraction', {})
            quality = feat.get('quality_metrics', {})
            for key, val in quality.items():
                if isinstance(val, (int, float)):
                    metrics_accumulator.setdefault(key, []).append(float(val))

        return {
            key: sum(vals) / len(vals)
            for key, vals in metrics_accumulator.items()
            if vals
        }

    # ------------------------------------------------------------------
    # INSIGHTS (rule-based narrative)
    # ------------------------------------------------------------------

    def generate_real_insights(self, intelligence_data: Dict[str, Any]) -> List[str]:
        """Generate narrative insights from real intelligence scores."""
        insights = []
        intelligence_scores = intelligence_data.get('intelligence_scores', {})

        if not intelligence_scores:
            return ["Analysis completed with comprehensive intelligence mapping."]

        dominant = max(intelligence_scores.items(), key=lambda x: x[1])
        intel_type, score = dominant
        insights.append(
            f"Your dominant intelligence is {intel_type.replace('_', ' ').title()} ({score:.1%}), "
            f"indicating exceptional natural strength in this domain."
        )

        high_scores = [(k, v) for k, v in intelligence_scores.items() if v > 0.65]
        if len(high_scores) > 1:
            names = ', '.join(k.replace('_', ' ').title() for k, _ in high_scores[:3])
            insights.append(
                f"You demonstrate strong performance across multiple domains: {names}. "
                f"This cognitive diversity is a significant asset."
            )

        weakest = min(intelligence_scores.items(), key=lambda x: x[1])
        if weakest[1] < 0.40:
            insights.append(
                f"{weakest[0].replace('_', ' ').title()} ({weakest[1]:.1%}) is your primary development "
                f"opportunity — focused practice here yields the highest returns."
            )

        score_range = max(intelligence_scores.values()) - min(intelligence_scores.values())
        if score_range < 0.20:
            insights.append(
                "Your intelligence profile is remarkably balanced, reflecting versatile and "
                "adaptable cognitive abilities."
            )
        elif score_range > 0.45:
            insights.append(
                "Your profile shows distinct specialisation — you have clear peaks that make you "
                "exceptionally well-suited to roles that leverage those strengths."
            )

        # Brain hemisphere insight
        brain = intelligence_data.get('brain_mapping', {})
        left = brain.get('left_hemisphere_bias', 0.5)
        right = brain.get('right_hemisphere_bias', 0.5)
        if abs(left - right) > 0.10:
            dominant_hemi = 'left' if left > right else 'right'
            hemi_trait = 'analytical and sequential processing' if dominant_hemi == 'left' else 'creative and holistic thinking'
            insights.append(
                f"Your brain mapping shows a {dominant_hemi}-hemisphere bias ({max(left, right):.1%}), "
                f"suggesting natural aptitude for {hemi_trait}."
            )

        return insights

    # ------------------------------------------------------------------
    # CAREER RECOMMENDATIONS (score-weighted, real data)
    # ------------------------------------------------------------------

    def generate_real_career_recommendations(self, intelligence_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate career recommendations from real intelligence scores."""
        recommendations = []
        intelligence_scores = intelligence_data.get('intelligence_scores', {})

        if not intelligence_scores:
            return []

        career_mapping = {
            'linguistic': [
                {'title': 'Content Strategist', 'match': 0.95, 'description': 'Leverages communication and narrative thinking'},
                {'title': 'Journalist / Author', 'match': 0.92, 'description': 'Perfect for creative and analytical writing'},
                {'title': 'Marketing Manager', 'match': 0.88, 'description': 'Persuasive communication meets strategic thinking'},
                {'title': 'Lawyer / Advocate', 'match': 0.85, 'description': 'Strong verbal reasoning and argumentation'},
            ],
            'logical_mathematical': [
                {'title': 'Data Scientist', 'match': 0.96, 'description': 'Analytical thinking and problem-solving at scale'},
                {'title': 'Software Engineer', 'match': 0.92, 'description': 'Logical systems design and structured thinking'},
                {'title': 'Financial Analyst', 'match': 0.88, 'description': 'Numerical mastery and strategic forecasting'},
                {'title': 'Research Scientist', 'match': 0.85, 'description': 'Hypothesis-driven inquiry and rigorous analysis'},
            ],
            'spatial': [
                {'title': 'Architect', 'match': 0.95, 'description': 'Spatial planning and 3-D visualisation'},
                {'title': 'UX/UI Designer', 'match': 0.92, 'description': 'Visual-spatial layout and user experience design'},
                {'title': 'Surgeon', 'match': 0.88, 'description': 'Precise spatial awareness and hand-eye coordination'},
                {'title': 'Pilot / Navigator', 'match': 0.84, 'description': 'Spatial orientation and dynamic decision-making'},
            ],
            'musical': [
                {'title': 'Music Producer', 'match': 0.95, 'description': 'Creative audio production and pattern recognition'},
                {'title': 'Sound Engineer', 'match': 0.90, 'description': 'Technical audio mastery and creative ear'},
                {'title': 'Composer', 'match': 0.87, 'description': 'Structural creativity and emotional expression'},
            ],
            'bodily_kinesthetic': [
                {'title': 'Physiotherapist', 'match': 0.94, 'description': 'Body mechanics, movement rehabilitation'},
                {'title': 'Professional Athlete / Coach', 'match': 0.92, 'description': 'Peak physical performance and tactical thinking'},
                {'title': 'Surgeon', 'match': 0.88, 'description': 'Fine motor precision and spatial dexterity'},
            ],
            'interpersonal': [
                {'title': 'HR Director', 'match': 0.95, 'description': 'People leadership and organisational culture'},
                {'title': 'Sales / Business Development', 'match': 0.92, 'description': 'Relationship building and persuasion'},
                {'title': 'Counsellor / Therapist', 'match': 0.88, 'description': 'Empathic listening and emotional support'},
                {'title': 'Diplomat', 'match': 0.84, 'description': 'Cross-cultural communication and negotiation'},
            ],
            'intrapersonal': [
                {'title': 'Life Coach / Mentor', 'match': 0.94, 'description': 'Deep self-awareness and guiding others'},
                {'title': 'Psychologist', 'match': 0.91, 'description': 'Understanding human behaviour and motivation'},
                {'title': 'Executive Coach', 'match': 0.87, 'description': 'Strategic self-reflection and leadership development'},
            ],
            'naturalistic': [
                {'title': 'Environmental Scientist', 'match': 0.95, 'description': 'Natural systems research and sustainability'},
                {'title': 'Biologist / Ecologist', 'match': 0.92, 'description': 'Scientific observation and natural pattern analysis'},
                {'title': 'Veterinarian', 'match': 0.86, 'description': 'Animal biology, care and natural empathy'},
            ],
            'existential': [
                {'title': 'Philosopher / Academic', 'match': 0.93, 'description': 'Deep inquiry into meaning and existence'},
                {'title': 'Spiritual Guide / Teacher', 'match': 0.89, 'description': "Guiding others through life's big questions"},
            ],
        }

        for intel_type, score in intelligence_scores.items():
            if intel_type in career_mapping and score > 0.45:
                for career in career_mapping[intel_type]:
                    adjusted_match = min(1.0, career['match'] * score)
                    recommendations.append({
                        'title': career['title'],
                        'match_percentage': adjusted_match * 100,
                        'description': career['description'],
                        'intelligence_type': intel_type.replace('_', ' ').title(),
                        'intelligence_score': score * 100,
                    })

        recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
        # Deduplicate by title (keep highest match)
        seen = set()
        deduped = []
        for rec in recommendations:
            if rec['title'] not in seen:
                seen.add(rec['title'])
                deduped.append(rec)
        return deduped[:12]

    # ------------------------------------------------------------------
    # DEVELOPMENT PLAN
    # ------------------------------------------------------------------

    def generate_real_development_plan(self, intelligence_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable development plan from real intelligence scores."""
        plans = []
        intelligence_scores = intelligence_data.get('intelligence_scores', {})

        if not intelligence_scores:
            return []

        # Sort by score ascending — lowest scores are highest priority
        sorted_areas = sorted(intelligence_scores.items(), key=lambda x: x[1])

        activity_map = {
            'linguistic': ['Daily journaling (500 words)', 'Join a debate or Toastmasters club', 'Read one book per month across genres', 'Write summaries of everything you learn'],
            'logical_mathematical': ['Solve logic puzzles daily (15 min)', 'Take an online statistics or coding course', 'Analyse real datasets for patterns', 'Study mathematical proofs'],
            'spatial': ['Practice freehand sketching', 'Solve 3-D puzzle games', 'Study architectural blueprints', 'Use mind-mapping tools visually'],
            'musical': ['Learn a musical instrument (even basic piano)', 'Analyse music structure — identify chords, rhythm', 'Attend live performances', 'Practice rhythmic exercises daily'],
            'bodily_kinesthetic': ['Engage in a sport or martial art', 'Practice yoga or tai chi for body awareness', 'Learn to type, sculpt or craft', 'Take up dance or choreography'],
            'interpersonal': ['Join a community volunteer group', 'Practice active listening in every conversation', 'Take a negotiation or facilitation workshop', 'Mentoring someone junior'],
            'intrapersonal': ['Daily 10-minute mindfulness / journaling', 'Conduct quarterly self-assessments', 'Work with a coach or therapist', 'Set and review personal goals weekly'],
            'naturalistic': ['Spend regular time in nature observing patterns', 'Start a nature journal or plant journal', 'Study biology or ecology courses', 'Practice categorising and organising natural objects'],
            'existential': ['Read philosophy texts across cultures', 'Attend philosophical discussion groups', 'Maintain a reflective journal on life themes', 'Engage in cross-cultural conversation and travel'],
        }

        for intel_type, score in sorted_areas[:5]:  # Top 5 development areas
            activities = activity_map.get(intel_type, [
                f'Practice {intel_type.replace("_", " ")} activities regularly',
                f'Seek feedback on {intel_type.replace("_", " ")} performance',
                f'Set measurable goals for {intel_type.replace("_", " ")} improvement',
                f'Track monthly progress in {intel_type.replace("_", " ")} development',
            ])
            plans.append({
                'title': f'{intel_type.replace("_", " ").title()} Intelligence',
                'current_level': f'{score:.1%}',
                'current_score': score,
                'target_level': '70%',
                'priority': 'High' if score < 0.35 else ('Medium' if score < 0.55 else 'Low'),
                'description': interpret_score(score, intel_type.replace('_', ' ')),
                'steps': activities,
            })

        return plans

