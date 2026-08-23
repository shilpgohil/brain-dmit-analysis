"""
DMIT AI Consultant — widget spec builders.
Produces rich structured UI component specs for the frontend.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def _pct_val(v: Any) -> float:
    if v is None:
        return 0.0
    try:
        f = float(v)
        return round(f * 100, 1) if f <= 1.0 else round(f, 1)
    except (TypeError, ValueError):
        return 0.0


def build_widget_spec(widget_key: str, session_data: Dict[str, Any]) -> Optional[Dict]:
    builders = {
        "score_grid_quotients": _score_grid_quotients,
        "score_grid_mi":        _score_grid_mi,
        "career_cards":         _career_cards,
        "swot_matrix":          _swot_matrix,
        "finger_map":           _finger_map,
        "timeline":             _timeline,
        "stat_bar_lobes":       _stat_bar_lobes,
        "trait_pills":          _trait_pills,
        "mi_strength_ladder":   _mi_strength_ladder,
        "learning_guide":       _learning_guide,
        "brain_summary":        _brain_summary,
        "atd_visual":           _atd_visual,
    }
    fn = builders.get(widget_key)
    if not fn:
        return None
    try:
        return fn(session_data)
    except Exception:
        return None


_QUOTIENT_META = {
    "iq": {"label": "Intelligence",  "color": "#c4a574", "icon": "brain"},
    "eq": {"label": "Emotional",     "color": "#9d8bb5", "icon": "heart"},
    "cq": {"label": "Creativity",    "color": "#6b9e8f", "icon": "palette"},
    "aq": {"label": "Adversity",     "color": "#b87d5c", "icon": "shield"},
    "sq": {"label": "Spiritual",     "color": "#8b9eb7", "icon": "star"},
    "pq": {"label": "Physical",      "color": "#4ade80", "icon": "activity"},
    "lq": {"label": "Leadership",    "color": "#e8dcc8", "icon": "crown"},
    "mq": {"label": "Moral",         "color": "#f59e0b", "icon": "compass"},
    "fq": {"label": "Financial",     "color": "#34d399", "icon": "trending-up"},
    "dq": {"label": "Digital",       "color": "#60a5fa", "icon": "cpu"},
}

_TIER_MAP = [
    (80, "Exceptional"),
    (65, "Strong"),
    (45, "Moderate"),
    (0,  "Developing"),
]


def _tier(pct: float) -> str:
    for threshold, label in _TIER_MAP:
        if pct >= threshold:
            return label
    return "Developing"


def _score_grid_quotients(s: Dict) -> Optional[Dict]:
    q = s.get("quotients") or {}
    if not q:
        return None
    items = []
    for key, meta in _QUOTIENT_META.items():
        v = q.get(key)
        if v is not None:
            pct = _pct_val(v)
            items.append({
                "key": key.upper(),
                "label": meta["label"],
                "value": pct,
                "unit": "%",
                "color": meta["color"],
                "icon": meta["icon"],
                "tier": _tier(pct),
            })
    return {
        "widget_type": "score_grid",
        "title": "10-Quotient Summary",
        "columns": 5,
        "items": items,
    }


def _score_grid_mi(s: Dict) -> Optional[Dict]:
    mi = s.get("multiple_intelligences") or {}
    if not mi:
        return None
    colors = ["#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7",
              "#e8dcc8", "#f59e0b", "#4ade80"]
    icons  = ["book", "calculator", "eye", "hand", "music",
              "users", "user", "leaf"]
    labels = {
        "linguistic": "Linguistic",
        "logical_mathematical": "Logical",
        "spatial": "Spatial",
        "bodily_kinesthetic": "Kinesthetic",
        "musical": "Musical",
        "interpersonal": "Interpersonal",
        "intrapersonal": "Intrapersonal",
        "naturalistic": "Naturalistic",
    }
    items = []
    for i, (key, label) in enumerate(labels.items()):
        v = mi.get(key)
        if v is not None:
            pct = _pct_val(v)
            items.append({
                "key": label,
                "label": label,
                "value": pct,
                "unit": "%",
                "color": colors[i % len(colors)],
                "icon": icons[i % len(icons)],
                "tier": _tier(pct),
            })
    return {
        "widget_type": "score_grid",
        "title": "Multiple Intelligence Scores",
        "columns": 4,
        "items": sorted(items, key=lambda x: x["value"], reverse=True),
    }


def _career_cards(s: Dict) -> Optional[Dict]:
    careers = s.get("careers") or []
    if not careers:
        return None
    colors = ["#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7", "#e8dcc8"]
    items = []
    for i, c in enumerate(careers[:6]):
        title = c.get("career") or c.get("title") or c.get("name") or "Unknown"
        pct   = _pct_val(c.get("suitability") or c.get("match_percentage") or c.get("suitability_pct"))
        items.append({
            "rank": i + 1,
            "title": title,
            "family": c.get("family") or "General",
            "suitability_pct": pct,
            "key_strengths": c.get("key_strengths") or [],
            "color": colors[i % len(colors)],
        })
    return {"widget_type": "career_cards", "title": "Your Top Career Matches", "items": items}


def _swot_matrix(s: Dict) -> Optional[Dict]:
    swot = s.get("swot") or {}
    if not swot:
        return None
    return {
        "widget_type": "swot_matrix",
        "title": "Personal SWOT Analysis",
        "strengths":     list(swot.get("strengths") or []),
        "weaknesses":    list(swot.get("weaknesses") or []),
        "opportunities": list(swot.get("opportunities") or []),
        "threats":       list(swot.get("threats") or []),
    }


def _finger_map(s: Dict) -> Optional[Dict]:
    fingers = s.get("finger_prints") or s.get("fingers") or []
    if not fingers:
        return None
    pattern_colors = {
        "whorl": "#c4a574", "loop": "#9d8bb5",
        "arch": "#6b9e8f", "accidental": "#b87d5c", "unknown": "#475569",
    }
    items = []
    for f in fingers:
        pt = (f.get("pattern_type") or "unknown").lower()
        items.append({
            "finger":       f.get("finger_name") or f.get("finger") or "Unknown",
            "hand":         f.get("hand") or ("Left" if "l" in (f.get("finger_name") or "").lower() else "Right"),
            "pattern":      (f.get("pattern_type") or "Unknown").title(),
            "subtype":      f.get("pattern_subtype") or "",
            "ridge_count":  f.get("ridge_count") or f.get("total_ridge_count"),
            "quality":      _pct_val(f.get("quality_score")),
            "lobe":         f.get("brain_lobe") or "",
            "color":        pattern_colors.get(pt, "#475569"),
        })
    return {"widget_type": "finger_map", "title": "Fingerprint Pattern Map", "fingers": items}


def _timeline(s: Dict) -> Optional[Dict]:
    roadmap = s.get("development_roadmap") or []
    if not roadmap:
        return None
    weeks = []
    week_num = 1
    week_tasks: List[str] = []
    for item in roadmap[:20]:
        if isinstance(item, str):
            week_tasks.append(item)
        elif isinstance(item, dict):
            title_ = item.get("title") or item.get("goal") or ""
            desc   = item.get("description") or item.get("action") or ""
            week_tasks.append(f"{title_}: {desc}" if title_ else desc)
        if len(week_tasks) >= 3:
            weeks.append({
                "week": week_num,
                "title": f"Week {week_num}",
                "tasks": week_tasks[:3],
                "focus_area": "",
            })
            week_num += 1
            week_tasks = []
    if week_tasks:
        weeks.append({"week": week_num, "title": f"Week {week_num}", "tasks": week_tasks, "focus_area": ""})
    return {"widget_type": "timeline", "title": "30-Day Development Roadmap", "weeks": weeks[:4]}


def _stat_bar_lobes(s: Dict) -> Optional[Dict]:
    brain = s.get("brain_analysis") or {}
    lobes = brain.get("lobe_scores") or brain.get("lobes") or {}
    if not lobes:
        return None
    lobe_descriptions = {
        "frontal": "Decision making, planning, personality",
        "temporal": "Memory, language, auditory processing",
        "parietal": "Spatial awareness, sensory integration",
        "occipital": "Visual processing, pattern recognition",
        "limbic": "Emotional regulation, motivation",
    }
    colors = ["#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7"]
    items = []
    for i, (k, v) in enumerate(lobes.items()):
        items.append({
            "label": k.replace("_", " ").title() + " Lobe",
            "value": _pct_val(v),
            "max": 100,
            "color": colors[i % len(colors)],
            "description": lobe_descriptions.get(k.lower().replace("_lobe", "").strip(), ""),
        })
    return {"widget_type": "stat_bar_group", "title": "Brain Lobe Activity", "items": items}


def _trait_pills(s: Dict) -> Optional[Dict]:
    swot = s.get("swot") or {}
    personality = s.get("personality") or {}
    groups = []
    if swot.get("strengths"):
        groups.append({"category": "Core Strengths", "color": "gold",
                       "items": list(swot["strengths"])[:6]})
    if swot.get("weaknesses"):
        groups.append({"category": "Development Areas", "color": "rose",
                       "items": list(swot["weaknesses"])[:4]})
    comm = personality.get("communication_style")
    lead = personality.get("leadership_style")
    style_traits = [x for x in [comm, lead] if x]
    if style_traits:
        groups.append({"category": "Style Traits", "color": "plum", "items": style_traits})
    if not groups:
        return None
    return {"widget_type": "trait_pills", "title": "Personality Traits", "groups": groups}


def _mi_strength_ladder(s: Dict) -> Optional[Dict]:
    mi = s.get("multiple_intelligences") or {}
    if not mi:
        return None
    labels = {
        "linguistic": "Linguistic", "logical_mathematical": "Logical",
        "spatial": "Spatial", "bodily_kinesthetic": "Kinesthetic",
        "musical": "Musical", "interpersonal": "Interpersonal",
        "intrapersonal": "Intrapersonal", "naturalistic": "Naturalistic",
    }
    ranked = sorted(
        [(labels.get(k, k.title()), _pct_val(v)) for k, v in mi.items() if v is not None],
        key=lambda x: x[1], reverse=True,
    )
    colors = ["#c4a574", "#e8dcc8", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7", "#f59e0b", "#4ade80"]
    items = [
        {"rank": i+1, "intelligence": name, "value": val,
         "tier": _tier(val), "color": colors[i % len(colors)]}
        for i, (name, val) in enumerate(ranked)
    ]
    return {"widget_type": "mi_strength_ladder", "title": "Intelligence Ranking", "items": items}


def _learning_guide(s: Dict) -> Optional[Dict]:
    ls = s.get("learning_style") or {}
    v  = _pct_val(ls.get("visual"))
    a  = _pct_val(ls.get("auditory"))
    k  = _pct_val(ls.get("kinesthetic"))
    primary = ls.get("primary_style") or ls.get("dominant") or (
        "Visual" if v >= a and v >= k else "Auditory" if a >= k else "Kinesthetic"
    )
    return {
        "widget_type": "learning_guide",
        "title": "Your Personalised Learning Guide",
        "primary_style": primary,
        "vak_scores": {"visual": v, "auditory": a, "kinesthetic": k},
        "techniques": [
            {"style": "Visual", "icon": "eye",  "methods": ["Mind maps", "Diagrams", "Colour-coded notes", "Videos", "Charts"]},
            {"style": "Auditory", "icon": "ear", "methods": ["Discussion groups", "Recorded lectures", "Verbal repetition", "Podcasts"]},
            {"style": "Kinesthetic", "icon": "hand", "methods": ["Hands-on practice", "Role-play", "Field trips", "Experiments"]},
        ],
    }


def _brain_summary(s: Dict) -> Optional[Dict]:
    brain = s.get("brain_analysis") or {}
    lh = _pct_val(brain.get("left_hemisphere_pct") or brain.get("left_pct"))
    rh = _pct_val(brain.get("right_hemisphere_pct") or brain.get("right_pct"))
    if lh == 0 and rh == 0:
        return None
    dominant = "Left" if lh >= rh else "Right"
    diff = abs(lh - rh)
    balance = "Balanced" if diff < 5 else f"{'Left' if lh > rh else 'Right'}-dominant"
    return {
        "widget_type": "brain_summary",
        "title": "Brain Architecture Overview",
        "left_pct": lh, "right_pct": rh, "dominant": dominant,
        "left_traits":  ["Logical thinking", "Language processing", "Sequential analysis", "Detail-oriented"],
        "right_traits": ["Creative expression", "Spatial awareness", "Intuitive reasoning", "Holistic thinking"],
        "balance_label": f"{balance} — {diff:.0f}% difference between hemispheres",
    }


def _atd_visual(s: Dict) -> Optional[Dict]:
    atd = s.get("atd_analysis") or {}
    if not atd:
        return None
    def _angle(key):
        v = atd.get(f"{key}_angle") or atd.get(key)
        try:
            return round(float(v), 1)
        except (TypeError, ValueError):
            return None
    la, ra = _angle("left"), _angle("right")
    if la is None and ra is None:
        return None
    def _status(angle):
        if angle is None: return "N/A"
        if 38 <= angle <= 50: return "Normal"
        if angle < 38: return "Below Normal"
        return "Above Normal"
    return {
        "widget_type": "atd_visual",
        "title": "ATD Angle Analysis",
        "left_angle": la, "right_angle": ra,
        "normal_range_min": 38, "normal_range_max": 50,
        "left_status": _status(la), "right_status": _status(ra),
        "interpretation": atd.get("interpretation") or atd.get("summary") or
            "ATD angle reflects tactile sensitivity and fine-motor coordination.",
        "fine_motor_pct":       _pct_val(atd.get("fine_motor_score")),
        "sensory_sensitivity_pct": _pct_val(atd.get("sensory_sensitivity")),
    }
