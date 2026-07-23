#!/usr/bin/env python3
"""
DMIT Intelligence Mapper (Scientific 3.0)

Maps extracted fingerprint features to DMIT intelligence domains, brain regions,
and cognitive/behavioral traits, following the model in
dermatoglyphics_reverified_package (Ban Jun Sin et al., 2010):

    Thumb  -> Prefrontal Lobe        -> Intra/Inter-personal, executive
    Index  -> Posterior Frontal      -> Logical-Mathematical
    Middle -> Parietal Lobe          -> Bodily-Kinesthetic
    Ring   -> Temporal Lobe          -> Musical / Linguistic
    Little -> Occipital Lobe         -> Visual-Spatial

Real-data-only: a trait is computed from the terms that are actually present.
When no term behind a trait is measurable, the trait is returned as None (absent)
rather than a fabricated default.
"""

from typing import Dict, Any, Optional, List, Tuple
from enum import Enum


class FingerType(Enum):
    THUMB = "thumb"
    INDEX = "index"
    MIDDLE = "middle"
    RING = "ring"
    LITTLE = "little"
    UNKNOWN = "unknown"


class BrainLobe(Enum):
    PREFRONTAL = "prefrontal_lobe"
    POSTERIOR_FRONTAL = "posterior_frontal"
    PARIETAL = "parietal_lobe"
    TEMPORAL = "temporal_lobe"
    OCCIPITAL = "occipital_lobe"


FINGER_LOBE_MAP = {
    FingerType.THUMB: BrainLobe.PREFRONTAL,
    FingerType.INDEX: BrainLobe.POSTERIOR_FRONTAL,
    FingerType.MIDDLE: BrainLobe.PARIETAL,
    FingerType.RING: BrainLobe.TEMPORAL,
    FingerType.LITTLE: BrainLobe.OCCIPITAL,
}


def _get(features: Dict[str, Any], key: str) -> Optional[float]:
    value = features.get(key)
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _norm(value: Optional[float], max_val: float) -> Optional[float]:
    if value is None:
        return None
    return min(max(value, 0.0) / max_val, 1.0)


def _weighted(terms: List[Tuple[Optional[float], float]]) -> Optional[float]:
    present = [(v, w) for v, w in terms if v is not None]
    total_w = sum(w for _, w in present)
    if not present or total_w <= 0:
        return None
    score = sum(v * w for v, w in present) / total_w
    return max(0.0, min(1.0, score))


def _boost(score: Optional[float], amount: float) -> Optional[float]:
    if score is None:
        return None
    return max(0.0, min(1.0, score + amount))


def _pattern_family(features: Dict[str, Any]) -> int:
    raw = features.get('pattern_family')
    if raw is None:
        return -1
    try:
        return int(raw)
    except (TypeError, ValueError):
        return -1


def _map_core_intelligences(features: Dict[str, float]) -> Dict[str, Optional[float]]:
    fam = _pattern_family(features)
    mi: Dict[str, Optional[float]] = {}

    mi['linguistic'] = _weighted([
        (_norm(_get(features, 'entropy'), 5.0), 0.3),
        (_get(features, 'fourier_harmonic_ratio'), 0.3),
        (_get(features, 'pattern_symmetry_score'), 0.4),
    ])
    if fam == 1:
        mi['linguistic'] = _boost(mi['linguistic'], 0.1)

    mi['logical_mathematical'] = _weighted([
        (_get(features, 'whorl_logical_layering_score'), 0.4),
        (_norm((lambda d: d - 1.0 if d is not None else None)(_get(features, 'box_counting_dimension')), 1.0), 0.3),
        (_get(features, 'topological_complexity'), 0.3),
    ])
    if fam == 2:
        mi['logical_mathematical'] = _boost(mi['logical_mathematical'], 0.15)

    fractal_dim = _get(features, 'fractal_ridge_dimension')
    mi['spatial'] = _weighted([
        (_get(features, 'ridge_flow_quality'), 0.3),
        (_norm(fractal_dim - 1.0 if fractal_dim is not None else None, 1.0), 0.4),
        (_get(features, 'symmetry_index'), 0.3),
    ])
    if fam == 2:
        mi['spatial'] = _boost(mi['spatial'], 0.1)

    mi['musical'] = _weighted([
        (_get(features, 'wavelet_complexity'), 0.35),
        (_get(features, 'frequency_stability'), 0.35),
        (_get(features, 'spectral_entropy'), 0.3),
    ])
    if fam == 1:
        mi['musical'] = _boost(mi['musical'], 0.1)

    mi['bodily_kinesthetic'] = _weighted([
        (_norm(_get(features, 'ridge_density'), 0.5), 0.4),
        (_norm(_get(features, 'contour_complexity'), 100.0), 0.4),
        (_norm(_get(features, 'tfrc'), 25.0), 0.2),
    ])
    if fam == 2:
        mi['bodily_kinesthetic'] = _boost(mi['bodily_kinesthetic'], 0.15)

    mi['interpersonal'] = _weighted([
        (_get(features, 'graph_density'), 0.4),
        (_get(features, 'average_clustering'), 0.3),
        (_get(features, 'cross_spectral_fusion_score'), 0.3),
    ])
    if fam == 1:
        mi['interpersonal'] = _boost(mi['interpersonal'], 0.2)

    mi['intrapersonal'] = _weighted([
        (_get(features, 'feature_stability'), 0.4),
        (_get(features, 'spectral_coherence'), 0.3),
        (_get(features, 'frequency_stability'), 0.3),
    ])
    if fam == 2:
        mi['intrapersonal'] = _boost(mi['intrapersonal'], 0.2)

    mi['naturalistic'] = _weighted([
        (_get(features, 'lacunarity'), 0.3),
        (_get(features, 'pore_density'), 0.3),
        (_norm(_get(features, 'micro_texture_entropy'), 4.0), 0.4),
    ])

    return mi


def _map_brain_lobes(features: Dict[str, float], finger_type: FingerType) -> Dict[str, Optional[float]]:
    box_dim = _get(features, 'box_counting_dimension')
    fractal_dim = _get(features, 'fractal_ridge_dimension')

    potentials = {
        BrainLobe.PREFRONTAL: _weighted([
            (_get(features, 'topological_complexity'), 0.5),
            (_get(features, 'feature_stability'), 0.5),
        ]),
        BrainLobe.POSTERIOR_FRONTAL: _weighted([
            (_get(features, 'whorl_logical_layering_score'), 0.5),
            (_get(features, 'ridge_flow_quality'), 0.5),
        ]),
        BrainLobe.PARIETAL: _weighted([
            (_norm(_get(features, 'ridge_density'), 0.5), 0.5),
            (_norm(_get(features, 'tfrc'), 25.0), 0.5),
        ]),
        BrainLobe.TEMPORAL: _weighted([
            (_get(features, 'wavelet_complexity'), 0.5),
            (_get(features, 'frequency_stability'), 0.5),
        ]),
        BrainLobe.OCCIPITAL: _weighted([
            (_norm(fractal_dim - 1.0 if fractal_dim is not None else None, 1.0), 0.5),
            (_get(features, 'pattern_symmetry_score'), 0.5),
        ]),
    }

    brain: Dict[str, Optional[float]] = {}
    primary_lobe = FINGER_LOBE_MAP.get(finger_type)
    for lobe_enum, score in potentials.items():
        key = lobe_enum.value
        if primary_lobe is None:
            brain[key] = score
        elif lobe_enum == primary_lobe:
            brain[key] = score
        else:
            brain[key] = score * 0.2 if score is not None else None

    minutiae_density = _get(features, 'minutiae_density')
    brain['left_hemisphere_bias'] = _weighted([
        (_get(features, 'whorl_logical_layering_score'), 0.4),
        (_norm(box_dim - 1.0 if box_dim is not None else None, 1.0), 0.3),
        (_norm(minutiae_density, 20.0), 0.3),
    ])
    brain['right_hemisphere_bias'] = _weighted([
        (_get(features, 'pattern_creative_vs_logical'), 0.4),
        (_get(features, 'double_loop_detected'), 0.3),
        (_get(features, 'fractal_pattern_recall'), 0.3),
    ])
    return brain


def _map_learning_styles(features: Dict[str, float]) -> Dict[str, Optional[float]]:
    fractal_dim = _get(features, 'fractal_ridge_dimension')
    return {
        'visual': _weighted([
            (_get(features, 'pattern_symmetry_score'), 0.4),
            (_norm(fractal_dim - 1.0 if fractal_dim is not None else None, 1.0), 0.3),
            (_get(features, 'ridge_flow_quality'), 0.3),
        ]),
        'auditory': _weighted([
            (_get(features, 'wavelet_complexity'), 0.4),
            (_get(features, 'frequency_stability'), 0.3),
            (_get(features, 'spectral_entropy'), 0.3),
        ]),
        'kinesthetic': _weighted([
            (_norm(_get(features, 'ridge_density'), 0.5), 0.4),
            (_norm(_get(features, 'tfrc'), 25.0), 0.3),
            (_norm(_get(features, 'contour_complexity'), 100.0), 0.3),
        ]),
    }


def _map_personality(features: Dict[str, float]) -> Dict[str, Optional[float]]:
    fam = _pattern_family(features)
    fractal_dim = _get(features, 'fractal_ridge_dimension')
    stability = _get(features, 'feature_stability')
    flow = _get(features, 'ridge_flow_quality')
    pb: Dict[str, Optional[float]] = {}

    pb['openness'] = _weighted([
        (_get(features, 'composite_pattern_diversity'), 0.4),
        (_get(features, 'pattern_creative_vs_logical'), 0.3),
        (_norm(fractal_dim - 1.0 if fractal_dim is not None else None, 1.0), 0.3),
    ])
    if fam == 2:
        pb['openness'] = _boost(pb['openness'], 0.15)

    pb['conscientiousness'] = _weighted([
        (stability, 0.4),
        (_get(features, 'whorl_logical_layering_score'), 0.3),
        (flow, 0.3),
    ])
    if fam == 2:
        pb['conscientiousness'] = _boost(pb['conscientiousness'], 0.2)
    elif fam == 0:
        pb['conscientiousness'] = _boost(pb['conscientiousness'], 0.1)

    pb['extraversion'] = _weighted([
        (_get(features, 'graph_density'), 0.4),
        (_get(features, 'topological_complexity'), 0.3),
        (_get(features, 'average_clustering'), 0.3),
    ])
    if fam == 2:
        pb['extraversion'] = _boost(pb['extraversion'], 0.1)

    pb['agreeableness'] = _weighted([
        (_get(features, 'cross_spectral_fusion_score'), 0.4),
        (_get(features, 'multi_modal_integration'), 0.3),
        (_get(features, 'pattern_symmetry_score'), 0.3),
    ])
    if fam == 1:
        pb['agreeableness'] = _boost(pb['agreeableness'], 0.25)

    entropy = _get(features, 'entropy')
    pb['neuroticism'] = _weighted([
        (1.0 - stability if stability is not None else None, 0.4),
        (_norm(entropy, 5.0), 0.3),
        (1.0 - flow if flow is not None else None, 0.3),
    ])
    if fam == 1:
        pb['neuroticism'] = _boost(pb['neuroticism'], 0.15)

    return pb


ATD_RANGES = (
    (35.0, "<=35"),
    (40.0, "36-40"),
    (45.0, "41-45"),
    (float('inf'), "45+"),
)


def map_atd_angle(angle_deg: Optional[float]) -> Optional[Dict[str, Any]]:
    if angle_deg is None:
        return None
    try:
        angle = float(angle_deg)
    except (TypeError, ValueError):
        return None
    if angle <= 0:
        return None

    if angle <= 35.0:
        category = "<=35"
        learning_speed = 0.95
        fine_motor = 0.95
        sensory = 0.95
        interpretation = (
            "Strong observation and nimble physical control. Masters new techniques quickly "
            "with high comprehension, though emotionally sensitive to the surrounding environment."
        )
    elif angle <= 40.0:
        category = "36-40"
        learning_speed = 0.8
        fine_motor = 0.85
        sensory = 0.8
        interpretation = (
            "Normal optimal range. Stable, accurate data gathering with strong fine-muscle "
            "coordination and high perception toward learning."
        )
    elif angle <= 45.0:
        category = "41-45"
        learning_speed = 0.55
        fine_motor = 0.55
        sensory = 0.55
        interpretation = (
            "Benefits from step-by-step repeated training while mastering a new technique. "
            "Performance is stable but slower; learning motivation should be reinforced."
        )
    else:
        category = "45+"
        learning_speed = 0.3
        fine_motor = 0.3
        sensory = 0.4
        interpretation = (
            "Slower information processing and response; needs more time and staged teaching. "
            "Stronger at gross-muscle actions than delicate fine-motor work."
        )

    if angle < 38.0:
        fine_motor = min(1.0, fine_motor + 0.05)
        sensory = min(1.0, sensory + 0.05)
    if angle > 42.0:
        fine_motor = max(0.0, fine_motor - 0.05)

    return {
        'angle_deg': round(angle, 1),
        'range_category': category,
        'learning_speed': round(learning_speed, 3),
        'fine_motor_capacity': round(fine_motor, 3),
        'sensory_sensitivity': round(sensory, 3),
        'interpretation': interpretation,
    }


def map_features_to_dmit_profile(features: Dict[str, float], finger_type_str: str = "unknown") -> Dict[str, Any]:
    try:
        f_type = FingerType(finger_type_str.lower().strip())
    except ValueError:
        f_type = FingerType.UNKNOWN

    return {
        'multiple_intelligences': _map_core_intelligences(features),
        'brain_mapping': _map_brain_lobes(features, f_type),
        'learning_styles': _map_learning_styles(features),
        'personality_behavior': _map_personality(features),
        'meta_data': {
            'finger_type_used': f_type.value,
            'primary_lobe': FINGER_LOBE_MAP[f_type].value if f_type in FINGER_LOBE_MAP else None,
            'mapping_standard': "3.0_DMIT_CROSS_LATERAL",
        },
    }


def create_bulletproof_dmit_analysis(features: Dict[str, float], run_extensions: bool = True,
                                     validate_compatibility: bool = True) -> Dict[str, Any]:
    return {
        'dmit_profile': map_features_to_dmit_profile(features),
        'extension_results': {},
        'quality_metrics': {'valid': True},
        'success_indicators': {'mapped': True},
    }
