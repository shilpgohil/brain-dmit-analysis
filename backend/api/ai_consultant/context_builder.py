"""
DMIT AI Consultant — context builder.
Serialises a completed session result into a structured text block
that fits comfortably in one LLM context window (~6-10 KB).

KEY NOTE: AnalysisResult Pydantic model field names:
  .multiple_intelligences  (NOT 'mi' or 'intelligences')
  .brain_lobes             (NOT 'brain_analysis')
  .learning_styles         (NOT 'learning_style')
  .career_matches          (NOT 'careers' or 'career')
  .personality             ✓
  .quotients               ✓  (dict of iq/eq/cq...)
  .atd_analysis            (NOT 'atd')
  .extensions              (list of ExtensionResult objects)
  .fingers                 (list of FingerBiometrics)
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _pct(v: Any, decimals: int = 0) -> str:
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
    Handles both Pydantic-serialised AnalysisResult dicts and raw pipeline dicts.
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
    add("")

    # ── Fingerprint patterns ──────────────────────────────────────────────────
    # AnalysisResult uses 'fingers'; some older formats use 'finger_prints'
    fingers = (
        session_data.get("fingers")
        or session_data.get("finger_prints")
        or []
    )
    if fingers:
        add("[FINGERPRINT PATTERNS]")
        for f in fingers:
            if isinstance(f, dict):
                name    = _val(f, "finger_id", "finger_position", "finger_name", default="finger")
                pattern = _val(f, "pattern_type", "pattern", default="unknown")
                subtype = f.get("pattern_subtype") or ""
                trc     = f.get("ridge_count") or f.get("total_ridge_count")
                quality = f.get("quality_score")
                parts   = [f"{name}: {pattern}{('-' + subtype) if subtype else ''}"]
                if trc is not None:
                    parts.append(f"TRC={trc}")
                if quality is not None:
                    parts.append(f"Quality={_pct(quality)}")
                add(" | ".join(parts))
        add("")

    # ── Brain architecture ────────────────────────────────────────────────────
    # AnalysisResult uses 'brain_lobes' (BrainLobeCapacity model)
    brain = (
        session_data.get("brain_lobes")
        or session_data.get("brain_analysis")
        or {}
    )
    if brain and isinstance(brain, dict):
        add("[BRAIN ARCHITECTURE]")
        lh = brain.get("left_hemisphere")
        rh = brain.get("right_hemisphere")
        if lh is not None and rh is not None:
            add(f"Left Hemisphere: {_pct(lh)} | Right Hemisphere: {_pct(rh)}")
        dominant = brain.get("dominant_hemisphere") or brain.get("dominant")
        if dominant:
            add(f"Dominant: {dominant}")
        # Lobe scores
        lobe_keys = ["prefrontal_lobe", "posterior_frontal", "parietal_lobe",
                     "temporal_lobe", "occipital_lobe"]
        lobes_found = [(k.replace("_lobe","").replace("_"," ").title(), brain.get(k))
                       for k in lobe_keys if brain.get(k) is not None]
        if lobes_found:
            add("Lobes: " + " | ".join(f"{n}: {_pct(v)}" for n, v in lobes_found))
        add("")

    # ── Multiple intelligences ────────────────────────────────────────────────
    # AnalysisResult uses 'multiple_intelligences' (MultipleIntelligences model)
    mi = (
        session_data.get("multiple_intelligences")
        or session_data.get("intelligences")
        or {}
    )
    if mi and isinstance(mi, dict):
        add("[MULTIPLE INTELLIGENCES]")
        items = sorted(
            [(k.replace("_", "-").title(), v) for k, v in mi.items() if v is not None],
            key=lambda x: float(x[1]) if isinstance(x[1], (int, float)) else 0,
            reverse=True,
        )
        for label, val in items:
            add(f"{label}: {_pct(val)}")
        add("")

    # ── 10 quotients ──────────────────────────────────────────────────────────
    # AnalysisResult uses 'quotients' (dict of iq/eq/cq...)
    quotients = session_data.get("quotients") or {}
    if quotients and isinstance(quotients, dict):
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
        found_any = False
        for key, label in labels.items():
            v = quotients.get(key)
            if v is None and isinstance(quotients.get(key.upper()), (int, float)):
                v = quotients.get(key.upper())
            if v is not None:
                add(f"{key.upper()} ({label}): {_pct(v)}")
                found_any = True
        if not found_any:
            add("(Quotient scores not available for this session)")
        add("")

    # ── Learning style ────────────────────────────────────────────────────────
    # AnalysisResult uses 'learning_styles' (LearningStyles model)
    ls = (
        session_data.get("learning_styles")
        or session_data.get("learning_style")
        or {}
    )
    if ls and isinstance(ls, dict):
        add("[LEARNING STYLE]")
        v_pct = _pct(ls.get("visual"))
        a_pct = _pct(ls.get("auditory"))
        k_pct = _pct(ls.get("kinesthetic"))
        add(f"Visual: {v_pct} | Auditory: {a_pct} | Kinesthetic: {k_pct}")
        primary = ls.get("primary_style") or ls.get("dominant")
        if primary:
            add(f"Primary: {primary}")
        add("")

    # ── Personality (Big-Five) ────────────────────────────────────────────────
    personality = session_data.get("personality") or {}
    if personality and isinstance(personality, dict):
        add("[PERSONALITY PROFILE — Big-Five]")
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            v = personality.get(trait)
            if v is not None:
                add(f"{trait.title()}: {_pct(v)}")
        add("")

    # ── Career matches ────────────────────────────────────────────────────────
    # AnalysisResult uses 'career_matches' (list of CareerMatch)
    careers = (
        session_data.get("career_matches")
        or session_data.get("careers")
        or []
    )
    if careers:
        add("[CAREER MATCHES — Top 12]")
        for i, c in enumerate(careers[:12], 1):
            if isinstance(c, dict):
                title_  = _val(c, "title", "career", "name", default="Unknown")
                pct     = _pct(c.get("match_score") or c.get("suitability") or c.get("match_percentage"))
                family  = c.get("family") or c.get("category") or ""
                ks      = c.get("key_strengths") or []
                parts   = [f"{i}. {title_} ({pct})"]
                if family:
                    parts.append(f"[{family}]")
                if ks:
                    parts.append(f"Strengths: {', '.join(str(x) for x in ks[:3])}")
                add(" ".join(parts))
        add("")

    # ── ATD angle ────────────────────────────────────────────────────────────
    # AnalysisResult uses 'atd_analysis' (AtdAnalysis model)
    atd = (
        session_data.get("atd_analysis")
        or session_data.get("atd")
        or {}
    )
    if atd and isinstance(atd, dict):
        add("[ATD ANGLE ANALYSIS]")
        for hand in ["left_hand", "right_hand"]:
            h = atd.get(hand)
            if h and isinstance(h, dict):
                angle = h.get("angle_deg")
                cat   = h.get("range_category", "")
                interp = h.get("interpretation", "")
                label = "Left" if hand == "left_hand" else "Right"
                if angle is not None:
                    add(f"{label} Hand: {angle:.1f}° ({cat})")
                    if interp:
                        add(f"  → {interp[:120]}")
        summary = atd.get("summary")
        if summary:
            add(f"Summary: {summary[:200]}")
        add("")

    # ── Top extension scores ──────────────────────────────────────────────────
    # AnalysisResult uses 'extensions' (list of ExtensionResult with .name and .primary_score)
    ext_list = session_data.get("extensions") or []
    ext_dict = session_data.get("extension_results") or {}

    ext_scores = []
    if isinstance(ext_list, list) and ext_list:
        for e in ext_list:
            if isinstance(e, dict):
                name  = e.get("name") or e.get("extension_name") or ""
                score = e.get("primary_score")
                if name and score is not None:
                    ext_scores.append((name.replace("_", " ").title(), float(score)))
    elif isinstance(ext_dict, dict) and ext_dict:
        for k, v in ext_dict.items():
            score = v.get("primary_score") if isinstance(v, dict) else v
            if score is not None:
                ext_scores.append((k.replace("_", " ").title(), float(score)))

    if ext_scores:
        ext_scores.sort(key=lambda x: x[1], reverse=True)
        add("[KEY BIOMETRIC INDICATORS — Top Extension Scores]")
        for name, score in ext_scores[:15]:
            add(f"{name}: {_pct(score)}")
        add("")

    return "\n".join(lines)


def extract_candidate_meta(session_data: Dict[str, Any]) -> tuple[str, str, str]:
    """Extract (candidate_name, counsellor_name, test_date) for prompt headers."""
    name       = session_data.get("subject_name") or "the candidate"
    counsellor = session_data.get("counsellor") or "N/A"
    raw_date   = session_data.get("created_at")
    test_date  = str(raw_date)[:10] if raw_date else str(datetime.now().date())
    return name, counsellor, test_date
