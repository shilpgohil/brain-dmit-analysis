"""
DMIT AI Consultant — chart spec builders.
Produces Recharts-compatible specs for the frontend.
Uses the same color palette as the platform.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

# Platform color palette
_PALETTE = [
    "#c4a574",  # gold
    "#9d8bb5",  # plum
    "#6b9e8f",  # sage
    "#b87d5c",  # copper
    "#8b9eb7",  # steel blue
    "#c4a574",
    "#9d8bb5",
    "#6b9e8f",
    "#e8dcc8",  # champagne
    "#b87d5c",
]


def _pct_val(v: Any) -> float:
    if v is None:
        return 0.0
    try:
        f = float(v)
        return round(f * 100, 1) if f <= 1.0 else round(f, 1)
    except (TypeError, ValueError):
        return 0.0


def _mi_labels():
    return ["Linguistic", "Logical", "Spatial", "Kinesthetic", "Musical",
            "Interpersonal", "Intrapersonal", "Naturalistic"]


def _mi_keys():
    return ["linguistic", "logical_mathematical", "spatial", "bodily_kinesthetic",
            "musical", "interpersonal", "intrapersonal", "naturalistic"]


def build_chart_spec(chart_key: str, session_data: Dict[str, Any]) -> Optional[Dict]:
    builders = {
        "mi_radar":              _mi_radar,
        "personality_radar":     _personality_radar,
        "quotients_radar":       _quotients_radar,
        "brain_lobe_radar":      _brain_lobe_radar,
        "quotients_bar":         _quotients_bar,
        "brain_hemisphere_bar":  _brain_hemisphere_bar,
        "brain_lobes_bar":       _brain_lobes_bar,
        "career_hbar":           _career_hbar,
        "mi_ranked_hbar":        _mi_ranked_hbar,
        "learning_doughnut":     _learning_doughnut,
        "pattern_distribution_pie": _pattern_pie,
        "mi_quotient_grouped":   _mi_quotient_grouped,
        # New types
        "extension_bar":         _extension_bar,
        "brain_split_bar":       _brain_split_bar,
        "ridge_count_bar":       _ridge_count_bar,
    }
    fn = builders.get(chart_key)
    if not fn:
        return None
    try:
        return fn(session_data)
    except Exception:
        return None


# ── Radar charts ──────────────────────────────────────────────────────────────

def _mi_radar(s: Dict) -> Optional[Dict]:
    mi = s.get("multiple_intelligences") or {}
    keys = _mi_keys()
    labels = _mi_labels()
    data = [_pct_val(mi.get(k)) for k in keys]
    if not any(data):
        return None
    return {
        "chart_type": "radar",
        "title": "Multiple Intelligence Profile",
        "labels": labels,
        "datasets": [{"label": "Your Profile", "data": data, "color": "#c4a574"}],
    }


def _personality_radar(s: Dict) -> Optional[Dict]:
    p = s.get("personality") or {}
    keys = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
    labels = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    data = [_pct_val(p.get(k)) for k in keys]
    if not any(data):
        return None
    return {
        "chart_type": "radar",
        "title": "Big-Five Personality Profile",
        "labels": labels,
        "datasets": [{"label": "Your Profile", "data": data, "color": "#9d8bb5"}],
    }


def _quotients_radar(s: Dict) -> Optional[Dict]:
    q = s.get("quotients") or {}
    keys   = ["iq", "eq", "cq", "aq", "sq", "pq", "lq", "mq", "fq", "dq"]
    labels = ["IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ"]
    data = [_pct_val(q.get(k)) for k in keys]
    if not any(data):
        return None
    return {
        "chart_type": "radar",
        "title": "10-Quotient Cognitive Profile",
        "labels": labels,
        "datasets": [{"label": "Your Quotients", "data": data, "color": "#6b9e8f"}],
    }


def _brain_lobe_radar(s: Dict) -> Optional[Dict]:
    brain = s.get("brain_analysis") or {}
    lobes = brain.get("lobe_scores") or brain.get("lobes") or {}
    if not lobes:
        return None
    keys   = list(lobes.keys())
    labels = [k.replace("_", " ").title() for k in keys]
    data   = [_pct_val(lobes[k]) for k in keys]
    return {
        "chart_type": "radar",
        "title": "Brain Lobe Dominance",
        "labels": labels,
        "datasets": [{"label": "Activity", "data": data, "color": "#b87d5c"}],
    }


# ── Bar charts ────────────────────────────────────────────────────────────────

def _quotients_bar(s: Dict) -> Optional[Dict]:
    q = s.get("quotients") or {}
    keys   = ["iq", "eq", "cq", "aq", "sq", "pq", "lq", "mq", "fq", "dq"]
    labels = ["IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ"]
    data = [_pct_val(q.get(k)) for k in keys if q.get(k) is not None]
    labels_f = [l for k, l in zip(keys, labels) if q.get(k) is not None]
    if not data:
        return None
    colored = [{"label": l, "data": [d], "color": _PALETTE[i % len(_PALETTE)]}
               for i, (l, d) in enumerate(zip(labels_f, data))]
    return {
        "chart_type": "bar",
        "title": "10-Quotient Profile",
        "x_label": "Quotient",
        "y_label": "Score (%)",
        "labels": labels_f,
        "datasets": [{"label": "Score", "data": data, "color": "#c4a574"}],
    }


def _brain_hemisphere_bar(s: Dict) -> Optional[Dict]:
    brain = s.get("brain_analysis") or {}
    lh = _pct_val(brain.get("left_hemisphere_pct") or brain.get("left_pct"))
    rh = _pct_val(brain.get("right_hemisphere_pct") or brain.get("right_pct"))
    if lh == 0 and rh == 0:
        return None
    return {
        "chart_type": "bar",
        "title": "Hemisphere Activity",
        "labels": ["Left Hemisphere", "Right Hemisphere"],
        "datasets": [{"label": "Activity %", "data": [lh, rh], "color": "#c4a574"}],
    }


def _brain_lobes_bar(s: Dict) -> Optional[Dict]:
    # AnalysisResult uses 'brain_lobes' (BrainLobeCapacity); older code used 'brain_analysis'
    brain = s.get("brain_lobes") or s.get("brain_analysis") or {}
    if not brain:
        return None
    lobe_keys = ["prefrontal_lobe", "posterior_frontal", "parietal_lobe",
                 "temporal_lobe", "occipital_lobe"]
    lobes = {k.replace("_lobe","").replace("_"," ").title(): brain.get(k)
             for k in lobe_keys if brain.get(k) is not None}
    if not lobes:
        # fallback for older format
        lobes = brain.get("lobe_scores") or brain.get("lobes") or {}
    if not lobes:
        return None
    labels = [k.replace("_", " ").title() if "_" in k else k for k in lobes]
    data   = [_pct_val(v) for v in lobes.values()]
    return {
        "chart_type": "bar",
        "title": "Brain Lobe Dominance",
        "x_label": "Lobe",
        "y_label": "Activity (%)",
        "labels": labels,
        "datasets": [{"label": "Activity", "data": data, "color": "#c4a574"}],
    }


def _career_hbar(s: Dict) -> Optional[Dict]:
    # AnalysisResult uses 'career_matches'; older formats use 'careers'
    careers = s.get("career_matches") or s.get("careers") or []
    if not careers:
        return None
    top = careers[:8]
    labels = []
    data   = []
    for c in top:
        title = c.get("title") or c.get("career") or c.get("name") or "Unknown"
        pct = _pct_val(c.get("match_score") or c.get("suitability") or c.get("match_percentage"))
        labels.append(title)
        data.append(pct)
    return {
        "chart_type": "bar",
        "title": "Career Suitability Ranking",
        "x_label": "Suitability (%)",
        "y_label": "Career",
        "horizontal": True,
        "labels": labels,
        "datasets": [{"label": "Suitability", "data": data, "color": "#c4a574"}],
    }


def _mi_ranked_hbar(s: Dict) -> Optional[Dict]:
    mi = s.get("multiple_intelligences") or {}
    if not mi:
        return None
    sorted_mi = sorted(
        [(k.replace("_", " ").title(), _pct_val(v)) for k, v in mi.items() if v is not None],
        key=lambda x: x[1], reverse=True,
    )
    labels = [x[0] for x in sorted_mi]
    data   = [x[1] for x in sorted_mi]
    return {
        "chart_type": "bar",
        "title": "Intelligence Ranking",
        "horizontal": True,
        "labels": labels,
        "datasets": [{"label": "Score", "data": data, "color": "#9d8bb5"}],
    }


# ── Doughnut / pie ────────────────────────────────────────────────────────────

def _learning_doughnut(s: Dict) -> Optional[Dict]:
    ls = s.get("learning_styles") or s.get("learning_style") or {}
    v = _pct_val(ls.get("visual"))
    a = _pct_val(ls.get("auditory"))
    k = _pct_val(ls.get("kinesthetic"))
    if v == 0 and a == 0 and k == 0:
        return None
    return {
        "chart_type": "doughnut",
        "title": "Learning Style Distribution",
        "labels": ["Visual", "Auditory", "Kinesthetic"],
        "datasets": [{"label": "Learning Style", "data": [v, a, k],
                      "colors": ["#c4a574", "#9d8bb5", "#6b9e8f"]}],
    }


def _pattern_pie(s: Dict) -> Optional[Dict]:
    fingers = s.get("finger_prints") or s.get("fingers") or []
    counts: Dict[str, int] = {}
    for f in fingers:
        pt = (f.get("pattern_type") or "unknown").lower()
        counts[pt] = counts.get(pt, 0) + 1
    if not counts:
        return None
    color_map = {"whorl": "#c4a574", "loop": "#9d8bb5", "arch": "#6b9e8f",
                 "accidental": "#b87d5c", "unknown": "#475569"}
    labels = [k.title() for k in counts]
    data   = list(counts.values())
    colors = [color_map.get(k, "#c4a574") for k in counts]
    return {
        "chart_type": "pie",
        "title": "Fingerprint Pattern Distribution",
        "labels": labels,
        "datasets": [{"label": "Pattern Count", "data": data, "colors": colors}],
    }


# ── Grouped bar ───────────────────────────────────────────────────────────────

def _mi_quotient_grouped(s: Dict) -> Optional[Dict]:
    mi = s.get("multiple_intelligences") or {}
    q  = s.get("quotients") or {}
    mi_keys = _mi_keys()
    mi_labels = _mi_labels()
    mi_data = [_pct_val(mi.get(k)) for k in mi_keys]

    q_map = {"iq": "IQ", "eq": "EQ", "cq": "CQ", "lq": "LQ", "mq": "MQ"}
    q_labels = list(q_map.values())
    q_data   = [_pct_val(q.get(k)) for k in q_map]

    if not any(mi_data) and not any(q_data):
        return None

    return {
        "chart_type": "bar",
        "title": "Intelligence & Quotient Overview",
        "labels": mi_labels + q_labels,
        "datasets": [
            {"label": "MI Score", "data": mi_data + [None]*len(q_labels), "color": "#c4a574"},
            {"label": "Quotient", "data": [None]*len(mi_labels) + q_data, "color": "#9d8bb5"},
        ],
    }


# ── Extension bar ─────────────────────────────────────────────────────────────

def _extension_bar(s: Dict) -> Optional[Dict]:
    ext = s.get("extension_results") or {}
    if not ext:
        return None
    scored = sorted(
        [(k.replace("_", " ").title(), _pct_val(v.get("primary_score") if isinstance(v, dict) else v))
         for k, v in ext.items() if v is not None],
        key=lambda x: x[1], reverse=True,
    )[:10]
    if not scored:
        return None
    labels = [x[0] for x in scored]
    data   = [x[1] for x in scored]
    return {
        "chart_type": "bar",
        "title": "Top Extension Module Scores",
        "horizontal": True,
        "labels": labels,
        "datasets": [{"label": "Score", "data": data, "color": "#6b9e8f"}],
    }


# ── Brain split bar (L + R hemispheres side by side per lobe) ─────────────────

def _brain_split_bar(s: Dict) -> Optional[Dict]:
    brain = s.get("brain_analysis") or {}
    lobes = brain.get("lobe_hemispheres") or {}
    if not lobes:
        # Fall back to simple hemisphere bar
        return _brain_hemisphere_bar(s)
    labels, left_data, right_data = [], [], []
    for lobe, sides in lobes.items():
        if isinstance(sides, dict):
            labels.append(lobe.replace("_", " ").title())
            left_data.append(_pct_val(sides.get("left")))
            right_data.append(_pct_val(sides.get("right")))
    if not labels:
        return None
    return {
        "chart_type": "bar",
        "title": "Left vs Right Brain Activity by Lobe",
        "labels": labels,
        "datasets": [
            {"label": "Left", "data": left_data, "color": "#9d8bb5"},
            {"label": "Right", "data": right_data, "color": "#c4a574"},
        ],
    }


# ── Ridge count bar ──────────────────────────────────────────────────────────

def _ridge_count_bar(s: Dict) -> Optional[Dict]:
    fingers = s.get("finger_prints") or s.get("fingers") or []
    if not fingers:
        return None
    labels, data = [], []
    for f in fingers:
        trc = f.get("ridge_count") or f.get("total_ridge_count")
        if trc is not None:
            name = f.get("finger_name") or f.get("finger") or "?"
            labels.append(name[:8])
            data.append(float(trc))
    if not data:
        return None
    return {
        "chart_type": "bar",
        "title": "Ridge Count (TRC) per Finger",
        "x_label": "Finger",
        "y_label": "Ridge Count",
        "labels": labels,
        "datasets": [{"label": "TRC", "data": data, "color": "#c4a574"}],
    }
