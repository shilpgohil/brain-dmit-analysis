"""
DMIT AI Consultant — context builder.
Serialises a completed session result into a structured text block
that fits comfortably in one LLM context window (~6-10 KB).
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _pct(v: Any, decimals: int = 0) -> str:
    """Format a 0-1 float or 0-100 number as a clean percentage string."""
    if v is None:
        return "N/A"
    try:
        f = float(v)
        if f <= 1.0:
            f *= 100
        if decimals:
            return f"{f:.{decimals}f}%"
        return f"{f:.0f}%"
    except (TypeError, ValueError):
        return "N/A"


def _val(d: Dict, *keys, default="N/A") -> str:
    for k in keys:
        v = d.get(k)
        if v is not None:
            return str(v)
    return default


def format_session_as_context(session_data: Dict[str, Any]) -> str:
    """
    Converts a full session result dict into a structured plain-text block
    suitable for injection into the LLM system prompt.
    """
    lines = []
    add = lines.append

    # ── Candidate profile ────────────────────────────────────────────────────
    add("[CANDIDATE PROFILE]")
    add(f"Name:        {_val(session_data, 'subject_name', default='Unknown')}")
    add(f"Age:         {_val(session_data, 'subject_age', default='N/A')}")
    add(f"Gender:      {_val(session_data, 'subject_gender', default='N/A')}")
    add(f"DOB:         {_val(session_data, 'subject_dob', default='N/A')}")
    add(f"School:      {_val(session_data, 'school', default='N/A')}")
    add(f"Counsellor:  {_val(session_data, 'counsellor', default='N/A')}")
    add(f"Test Date:   {_val(session_data, 'created_at', default=str(datetime.now().date()))[:10]}")
    add(f"Session ID:  {_val(session_data, 'session_id', default='N/A')}")
    add("")

    # ── Fingerprint patterns ──────────────────────────────────────────────────
    fingers = session_data.get("finger_prints") or session_data.get("fingers") or []
    if fingers:
        add("[FINGERPRINT PATTERNS]")
        for f in fingers:
            name    = _val(f, "finger_name", "finger")
            pattern = _val(f, "pattern_type", "unknown")
            subtype = f.get("pattern_subtype") or ""
            trc     = f.get("ridge_count") or f.get("total_ridge_count")
            quality = f.get("quality_score")
            lobe    = f.get("brain_lobe") or ""
            parts   = [f"{name}: {pattern}{('-' + subtype) if subtype else ''}"]
            if trc is not None:
                parts.append(f"TRC={trc}")
            if quality is not None:
                parts.append(f"Quality={_pct(quality)}")
            if lobe:
                parts.append(f"→ {lobe}")
            add(" | ".join(parts))
        add("")

    # ── Brain architecture ────────────────────────────────────────────────────
    brain = session_data.get("brain_analysis") or {}
    if brain:
        add("[BRAIN ARCHITECTURE]")
        lh = brain.get("left_hemisphere_pct") or brain.get("left_pct")
        rh = brain.get("right_hemisphere_pct") or brain.get("right_pct")
        if lh is not None and rh is not None:
            add(f"Left Hemisphere: {_pct(lh)} | Right Hemisphere: {_pct(rh)}")
        dominant = brain.get("dominant_hemisphere") or brain.get("dominant")
        if dominant:
            add(f"Dominant: {dominant}")
        lobes = brain.get("lobe_scores") or brain.get("lobes") or {}
        if lobes:
            lobe_str = " | ".join(f"{k.replace('_',' ').title()}: {_pct(v)}" for k, v in lobes.items())
            add(f"Lobes: {lobe_str}")
        add("")

    # ── Multiple intelligences ────────────────────────────────────────────────
    mi = session_data.get("multiple_intelligences") or {}
    if mi:
        add("[MULTIPLE INTELLIGENCES]")
        items = sorted(
            [(k.replace("_", "-").title(), v) for k, v in mi.items() if v is not None],
            key=lambda x: (x[1] if isinstance(x[1], (int, float)) else 0),
            reverse=True,
        )
        for label, val in items:
            add(f"{label}: {_pct(val)}")
        add("")

    # ── 10 quotients ──────────────────────────────────────────────────────────
    quotients = session_data.get("quotients") or {}
    if quotients:
        add("[TEN QUOTIENTS]")
        labels = {
            "iq": "Intelligence Quotient",
            "eq": "Emotional Quotient",
            "cq": "Creativity Quotient",
            "aq": "Adversity Quotient",
            "sq": "Spiritual Quotient",
            "pq": "Physical Quotient",
            "lq": "Leadership Quotient",
            "mq": "Moral Quotient",
            "fq": "Financial Quotient",
            "dq": "Digital Quotient",
        }
        for key, label in labels.items():
            v = quotients.get(key)
            if v is not None:
                add(f"{key.upper()} ({label}): {_pct(v)}")
        add("")

    # ── Learning style ────────────────────────────────────────────────────────
    ls = session_data.get("learning_style") or {}
    if ls:
        add("[LEARNING STYLE]")
        v_pct = _pct(ls.get("visual"))
        a_pct = _pct(ls.get("auditory"))
        k_pct = _pct(ls.get("kinesthetic"))
        primary = ls.get("primary_style") or ls.get("dominant") or ""
        add(f"Visual: {v_pct} | Auditory: {a_pct} | Kinesthetic: {k_pct}")
        if primary:
            add(f"Primary Learning Style: {primary}")
        add("")

    # ── Personality (Big-Five) ────────────────────────────────────────────────
    personality = session_data.get("personality") or {}
    if personality:
        add("[PERSONALITY PROFILE — Big-Five]")
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            v = personality.get(trait)
            if v is not None:
                add(f"{trait.title()}: {_pct(v)}")
        # Derived styles
        for style_key in ["communication_style", "decision_style", "leadership_style", "stress_response"]:
            s = personality.get(style_key)
            if s:
                add(f"{style_key.replace('_', ' ').title()}: {s}")
        add("")

    # ── SWOT ──────────────────────────────────────────────────────────────────
    swot = session_data.get("swot") or {}
    if swot:
        add("[SWOT ANALYSIS]")
        for quad in ["strengths", "weaknesses", "opportunities", "threats"]:
            items = swot.get(quad) or []
            if items:
                add(f"{quad.title()}: {' | '.join(str(x) for x in items)}")
        add("")

    # ── Career matches ────────────────────────────────────────────────────────
    careers = session_data.get("careers") or []
    if careers:
        add("[CAREER MATCHES]")
        for i, c in enumerate(careers[:12], 1):
            title  = _val(c, "career", "title", "name", default="Unknown")
            pct    = _pct(c.get("suitability") or c.get("match_percentage") or c.get("suitability_pct"))
            family = c.get("family") or ""
            ks     = c.get("key_strengths") or []
            parts  = [f"{i}. {title} ({pct})"]
            if family:
                parts.append(f"[{family}]")
            if ks:
                parts.append(f"Strengths: {', '.join(str(x) for x in ks[:3])}")
            add(" ".join(parts))
        add("")

    # ── ATD angle ────────────────────────────────────────────────────────────
    atd = session_data.get("atd_analysis") or {}
    if atd:
        add("[ATD ANGLE ANALYSIS]")
        for hand in ["left", "right"]:
            angle = atd.get(f"{hand}_angle") or atd.get(f"{hand}")
            conf  = atd.get(f"{hand}_confidence")
            if angle is not None:
                parts = [f"{hand.title()} Hand: {angle:.1f}°"]
                if conf is not None:
                    parts.append(f"(conf: {_pct(conf)})")
                add(" | ".join(parts))
        interp = atd.get("interpretation") or atd.get("summary")
        if interp:
            add(f"Interpretation: {interp}")
        add("")

    # ── Development roadmap ───────────────────────────────────────────────────
    roadmap = session_data.get("development_roadmap") or []
    if roadmap:
        add("[DEVELOPMENT ROADMAP]")
        for item in roadmap[:10]:
            if isinstance(item, str):
                add(f"• {item}")
            elif isinstance(item, dict):
                title_ = item.get("title") or item.get("goal") or ""
                desc   = item.get("description") or item.get("action") or ""
                add(f"• {title_}: {desc}" if title_ else f"• {desc}")
        add("")

    # ── Top extension scores ──────────────────────────────────────────────────
    ext_results = session_data.get("extension_results") or {}
    if ext_results:
        add("[KEY BIOMETRIC INDICATORS — Top Scores]")
        sorted_ext = sorted(
            [(k, v.get("primary_score") if isinstance(v, dict) else v)
             for k, v in ext_results.items()
             if v is not None],
            key=lambda x: (x[1] if isinstance(x[1], (int, float)) else 0),
            reverse=True,
        )
        for k, v in sorted_ext[:12]:
            if isinstance(v, (int, float)):
                add(f"{k.replace('_', ' ').title()}: {_pct(v)}")
        add("")

    return "\n".join(lines)


def extract_candidate_meta(session_data: Dict[str, Any]) -> tuple[str, str, str]:
    """Extract (candidate_name, counsellor_name, test_date) for prompt headers."""
    name = session_data.get("subject_name") or "the candidate"
    counsellor = session_data.get("counsellor") or "N/A"
    # created_at may be a datetime object or an ISO string — stringify first
    raw_date = session_data.get("created_at")
    test_date = str(raw_date)[:10] if raw_date else str(datetime.now().date())
    return name, counsellor, test_date
