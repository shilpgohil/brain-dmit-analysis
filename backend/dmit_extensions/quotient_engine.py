"""
Ten-quotient composite layer (IQ, EQ, CQ, AQ, SQ, PQ, LQ, MQ, FQ, DQ).

Each quotient is a weighted composite of scores the pipeline already computes.
Missing inputs propagate as None — no fabricated defaults.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

QUOTIENT_KEYS = ("IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ")

QUOTIENT_LABELS = {
    "IQ": "Intelligence Quotient",
    "EQ": "Emotional Quotient",
    "CQ": "Creativity Quotient",
    "AQ": "Adaptability Quotient",
    "SQ": "Social Quotient",
    "PQ": "Physical Quotient",
    "LQ": "Leadership Quotient",
    "MQ": "Motivation Quotient",
    "FQ": "Focus Quotient",
    "DQ": "Decision Quotient",
}


def _clamp01(v: float) -> float:
    return max(0.0, min(1.0, float(v)))


def _mean(values: List[Optional[float]]) -> Optional[float]:
    present = [v for v in values if v is not None and isinstance(v, (int, float))]
    if not present:
        return None
    return _clamp01(sum(present) / len(present))


def _get_mi(mi: Dict[str, Any], key: str) -> Optional[float]:
    v = mi.get(key)
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return _clamp01(float(v))
    return None


def _get_personality(pb: Dict[str, Any], key: str) -> Optional[float]:
    v = pb.get(key)
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return _clamp01(float(v))
    return None


def _flatten_extension_scores(ext_results: Dict[str, Any]) -> Dict[str, float]:
    """Collect all numeric extension sub-scores into one flat map."""
    flat: Dict[str, float] = {}
    if not isinstance(ext_results, dict):
        return flat
    for ext_dict in ext_results.values():
        if not isinstance(ext_dict, dict):
            continue
        for k, v in ext_dict.items():
            if k in ("error", "recommendations"):
                continue
            if isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= float(v) <= 1:
                if k not in flat:
                    flat[k] = float(v)
    return flat


def compute_quotients(
    multiple_intelligences: Optional[Dict[str, Any]] = None,
    personality_behavior: Optional[Dict[str, Any]] = None,
    learning_styles: Optional[Dict[str, Any]] = None,
    extension_results: Optional[Dict[str, Any]] = None,
    brain_mapping: Optional[Dict[str, Any]] = None,
) -> Dict[str, Optional[float]]:
    mi = multiple_intelligences or {}
    pb = personality_behavior or {}
    ls = learning_styles or {}
    ext = _flatten_extension_scores(extension_results or {})
    brain = brain_mapping or {}

    iq = _mean([
        _get_mi(mi, "logical_mathematical"),
        _get_mi(mi, "linguistic"),
        ext.get("pattern_recognition_score"),
        ext.get("problem_solving_score"),
        ext.get("analytical_thinking"),
        ext.get("memory_processing_score"),
        ext.get("meta_cognition_score"),
        ext.get("logical_mathematical_intelligence_score"),
    ])

    eq = _mean([
        ext.get("emotional_intelligence_score"),
        ext.get("self_awareness"),
        ext.get("empathy_skills"),
        ext.get("social_awareness_score"),
        _get_mi(mi, "interpersonal"),
        _get_mi(mi, "intrapersonal"),
        ext.get("self_regulation_score"),
    ])

    cq = _mean([
        ext.get("creativity_index_score"),
        _get_mi(mi, "spatial"),
        _get_mi(mi, "musical"),
        ext.get("innovation_intelligence_score"),
        ext.get("curiosity_exploratory_score"),
        _get_personality(pb, "openness"),
    ])

    aq = _mean([
        ext.get("adaptability_resilience_score"),
        ext.get("learning_agility_score"),
        ext.get("risk_tolerance_index"),
        _get_personality(pb, "openness"),
        ext.get("persistence_grit_score"),
    ])

    sq = _mean([
        ext.get("communication_effectiveness_score"),
        ext.get("verbal_communication"),
        ext.get("social_awareness_score"),
        ext.get("team_collaboration_score"),
        _get_mi(mi, "interpersonal"),
        ext.get("relationship_awareness"),
        ext.get("cultural_intelligence_score"),
    ])

    pq = _mean([
        _get_mi(mi, "bodily_kinesthetic"),
        ext.get("bodily_kinesthetic_intelligence_score"),
        ext.get("wellness_intelligence_score"),
        brain.get("parietal_lobe") if isinstance(brain.get("parietal_lobe"), (int, float)) else None,
    ])

    lq = _mean([
        ext.get("leadership_potential_score"),
        ext.get("vision_leadership"),
        ext.get("strategic_thinking"),
        ext.get("influence_ability"),
        _get_personality(pb, "extraversion"),
        ext.get("entrepreneurial_aptitude_score"),
    ])

    mq = _mean([
        ext.get("motivation_drive_score"),
        ext.get("achievement_drive"),
        ext.get("persistence_grit_score"),
        _get_personality(pb, "conscientiousness"),
        ext.get("goal_orientation_score"),
    ])

    fq = _mean([
        ext.get("attention_focus_score"),
        ext.get("focus_quality"),
        ext.get("executive_function_score"),
        ext.get("time_management_score"),
        ext.get("cognitive_load_management_score"),
    ])

    dq = _mean([
        ext.get("decision_making_score"),
        ext.get("executive_function_score"),
        ext.get("financial_intelligence_score"),
        _get_personality(pb, "conscientiousness"),
        _get_mi(mi, "logical_mathematical"),
        ext.get("systems_thinking_score"),
    ])

    return {
        "IQ": iq,
        "EQ": eq,
        "CQ": cq,
        "AQ": aq,
        "SQ": sq,
        "PQ": pq,
        "LQ": lq,
        "MQ": mq,
        "FQ": fq,
        "DQ": dq,
    }


def quotients_as_dict(quotients: Dict[str, Optional[float]]) -> Dict[str, float]:
    """Return only measured quotients as floats (for JSON/API)."""
    out: Dict[str, float] = {}
    for k in QUOTIENT_KEYS:
        v = quotients.get(k)
        if v is not None:
            out[k] = round(float(v), 4)
    return out
