"""
DMIT AI Consultant — widget spec builders.
Produces rich structured UI component specs for the frontend.

DATA SHAPE NOTES (AnalysisResult, serialised via model_dump):
  quotients        → Dict with UPPERCASE keys: {"IQ": 0.78, "EQ": 0.65, ...}
  career_matches   → List[{title, category, family, match_score, key_strengths}]
  fingers          → List[{finger_id, finger_position, pattern_type, pattern_subtype,
                           ridge_count, quality_score, ...}]
  brain_lobes      → {prefrontal_lobe, posterior_frontal, parietal_lobe, temporal_lobe,
                      occipital_lobe, left_hemisphere, right_hemisphere, dominant_hemisphere}
  learning_styles  → {visual, auditory, kinesthetic}
  personality      → {openness, conscientiousness, extraversion, agreeableness, neuroticism}
  atd_analysis     → {left_hand: {angle_deg, range_category, interpretation, ...},
                      right_hand: {...}, summary}
  (AnalysisResult has NO swot / development_roadmap fields — those widgets
   return None unless an older data shape provides them.)
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


def _quotient_value(q: Dict, key: str) -> Optional[float]:
    """Case-insensitive quotient lookup — engine emits UPPERCASE keys."""
    for k in (key.upper(), key.lower()):
        v = q.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return float(v)
    return None


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
        v = _quotient_value(q, key)
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
    if not items:
        return None
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
    if not items:
        return None
    return {
        "widget_type": "score_grid",
        "title": "Multiple Intelligence Scores",
        "columns": 4,
        "items": sorted(items, key=lambda x: x["value"], reverse=True),
    }


def _career_cards(s: Dict) -> Optional[Dict]:
    careers = s.get("career_matches") or s.get("careers") or []
    if not careers:
        return None
    colors = ["#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7", "#e8dcc8"]
    items = []
    for i, c in enumerate(careers[:6]):
        if not isinstance(c, dict):
            continue
        title = c.get("title") or c.get("career") or c.get("name") or "Unknown"
        pct   = _pct_val(c.get("match_score") or c.get("suitability") or c.get("match_percentage"))
        items.append({
            "rank": i + 1,
            "title": title,
            "family": c.get("family") or c.get("category") or "General",
            "suitability_pct": pct,
            "key_strengths": c.get("key_strengths") or [],
            "color": colors[i % len(colors)],
        })
    if not items:
        return None
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
    fingers = s.get("fingers") or s.get("finger_prints") or []
    if not fingers:
        return None
    pattern_colors = {
        "whorl": "#c4a574", "loop": "#9d8bb5",
        "arch": "#6b9e8f", "accidental": "#b87d5c", "unknown": "#475569",
    }
    items = []
    for f in fingers:
        if not isinstance(f, dict):
            continue
        fid = f.get("finger_id") or f.get("finger_position") or f.get("finger_name") or "?"
        pt = (f.get("pattern_type") or "unknown").lower()
        hand = "Left" if str(fid).upper().startswith("L") else "Right"
        items.append({
            "finger":       str(fid),
            "hand":         hand,
            "pattern":      (f.get("pattern_type") or "Unknown").title(),
            "subtype":      f.get("pattern_subtype") or "",
            "ridge_count":  f.get("ridge_count"),
            "quality":      _pct_val(f.get("quality_score")),
            "lobe":         f.get("brain_lobe") or "",
            "color":        pattern_colors.get(pt, "#475569"),
        })
    if not items:
        return None
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
    brain = s.get("brain_lobes") or s.get("brain_analysis") or {}
    if not brain:
        return None
    lobe_keys = {
        "prefrontal_lobe":   "Executive function, planning, personality",
        "posterior_frontal": "Logic, language production, reasoning",
        "parietal_lobe":     "Spatial awareness, sensory integration",
        "temporal_lobe":     "Memory, language, auditory processing",
        "occipital_lobe":    "Visual processing, pattern recognition",
    }
    colors = ["#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7"]
    items = []
    i = 0
    for k, desc in lobe_keys.items():
        v = brain.get(k)
        if v is not None:
            items.append({
                "label": k.replace("_lobe", "").replace("_", " ").title(),
                "value": _pct_val(v),
                "max": 100,
                "color": colors[i % len(colors)],
                "description": desc,
            })
            i += 1
    if not items:
        return None
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
    # Derive trait pills from Big-Five when SWOT is absent (AnalysisResult has no swot)
    if not groups and personality:
        high = [(k.title(), _pct_val(v)) for k, v in personality.items()
                if isinstance(v, (int, float)) and _pct_val(v) >= 65 and k != "neuroticism"]
        if high:
            groups.append({
                "category": "Dominant Traits", "color": "gold",
                "items": [f"{name} ({val:.0f}%)" for name, val in
                          sorted(high, key=lambda x: x[1], reverse=True)[:5]],
            })
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
    if not ranked:
        return None
    colors = ["#c4a574", "#e8dcc8", "#9d8bb5", "#6b9e8f", "#b87d5c", "#8b9eb7", "#f59e0b", "#4ade80"]
    items = [
        {"rank": i+1, "intelligence": name, "value": val,
         "tier": _tier(val), "color": colors[i % len(colors)]}
        for i, (name, val) in enumerate(ranked)
    ]
    return {"widget_type": "mi_strength_ladder", "title": "Intelligence Ranking", "items": items}


def _learning_guide(s: Dict) -> Optional[Dict]:
    ls = s.get("learning_styles") or s.get("learning_style") or {}
    if not ls:
        return None
    v  = _pct_val(ls.get("visual"))
    a  = _pct_val(ls.get("auditory"))
    k  = _pct_val(ls.get("kinesthetic"))
    if v == 0 and a == 0 and k == 0:
        return None
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
    brain = s.get("brain_lobes") or s.get("brain_analysis") or {}
    lh = _pct_val(brain.get("left_hemisphere") or brain.get("left_hemisphere_pct") or brain.get("left_pct"))
    rh = _pct_val(brain.get("right_hemisphere") or brain.get("right_hemisphere_pct") or brain.get("right_pct"))
    if lh == 0 and rh == 0:
        return None
    dominant = brain.get("dominant_hemisphere") or ("Left" if lh >= rh else "Right")
    diff = abs(lh - rh)
    balance = "Balanced" if diff < 5 else f"{'Left' if lh > rh else 'Right'}-dominant"
    return {
        "widget_type": "brain_summary",
        "title": "Brain Architecture Overview",
        "left_pct": lh, "right_pct": rh, "dominant": str(dominant).title(),
        "left_traits":  ["Logical thinking", "Language processing", "Sequential analysis", "Detail-oriented"],
        "right_traits": ["Creative expression", "Spatial awareness", "Intuitive reasoning", "Holistic thinking"],
        "balance_label": f"{balance} — {diff:.0f}% difference between hemispheres",
    }


def _atd_visual(s: Dict) -> Optional[Dict]:
    atd = s.get("atd_analysis") or s.get("atd") or {}
    if not atd:
        return None

    def _hand(key):
        """AnalysisResult shape: atd_analysis.left_hand = {angle_deg, range_category, ...}"""
        h = atd.get(key)
        if isinstance(h, dict):
            try:
                return round(float(h.get("angle_deg")), 1), h
            except (TypeError, ValueError):
                return None, h
        return None, None

    la, lh_data = _hand("left_hand")
    ra, rh_data = _hand("right_hand")
    if la is None and ra is None:
        return None

    def _status(angle):
        if angle is None:
            return "N/A"
        if 35 <= angle <= 46:
            return "Normal"
        if angle < 35:
            return "Below Normal"
        return "Above Normal"

    interp = atd.get("summary") or ""
    if not interp and isinstance(rh_data, dict):
        interp = rh_data.get("interpretation") or ""
    if not interp:
        interp = "ATD angle reflects tactile sensitivity and fine-motor coordination."

    fm = None
    ss = None
    for h in (rh_data, lh_data):
        if isinstance(h, dict):
            fm = fm if fm is not None else h.get("fine_motor_capacity")
            ss = ss if ss is not None else h.get("sensory_sensitivity")

    return {
        "widget_type": "atd_visual",
        "title": "ATD Angle Analysis",
        "left_angle": la, "right_angle": ra,
        "normal_range_min": 35, "normal_range_max": 46,
        "left_status": _status(la), "right_status": _status(ra),
        "interpretation": interp,
        "fine_motor_pct": _pct_val(fm),
        "sensory_sensitivity_pct": _pct_val(ss),
    }
