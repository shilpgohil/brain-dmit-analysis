"""
Curated career reference database (~48 careers across 15 families).
Maps each career to required-quotient emphasis weights for suitability matching.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


CAREER_ENTRIES: List[Dict[str, Any]] = [
    # Medical & Healthcare
    {"title": "Physician / Doctor",         "family": "Medical & Healthcare",      "weights": {"IQ": 0.9, "EQ": 0.7, "DQ": 0.8, "FQ": 0.75}},
    {"title": "Surgeon",                    "family": "Medical & Healthcare",      "weights": {"IQ": 0.85, "DQ": 0.85, "PQ": 0.7, "FQ": 0.8}},
    {"title": "Nurse / Paramedic",          "family": "Medical & Healthcare",      "weights": {"EQ": 0.85, "SQ": 0.75, "PQ": 0.6, "MQ": 0.65}},
    {"title": "Psychologist / Counsellor",  "family": "Psychology & Counselling",  "weights": {"EQ": 0.9, "SQ": 0.85, "IQ": 0.65, "MQ": 0.6}},
    # Engineering & Technology
    {"title": "Software Developer",         "family": "Engineering & Technology",  "weights": {"IQ": 0.9, "CQ": 0.65, "FQ": 0.75, "AQ": 0.55}},
    {"title": "AI / ML Engineer",           "family": "Engineering & Technology",  "weights": {"IQ": 0.95, "CQ": 0.7, "FQ": 0.8, "AQ": 0.6}},
    {"title": "Data Scientist",             "family": "Engineering & Technology",  "weights": {"IQ": 0.95, "FQ": 0.75, "CQ": 0.6, "DQ": 0.65}},
    {"title": "Mechanical Engineer",        "family": "Engineering & Technology",  "weights": {"IQ": 0.85, "DQ": 0.7, "FQ": 0.65, "PQ": 0.55}},
    {"title": "Civil Engineer",             "family": "Engineering & Technology",  "weights": {"IQ": 0.8, "DQ": 0.75, "FQ": 0.65, "LQ": 0.55}},
    {"title": "Cybersecurity Analyst",      "family": "Engineering & Technology",  "weights": {"IQ": 0.85, "FQ": 0.8, "DQ": 0.75, "AQ": 0.6}},
    # Business & Management
    {"title": "Business Manager",           "family": "Business Management",       "weights": {"LQ": 0.85, "DQ": 0.75, "SQ": 0.7, "IQ": 0.6}},
    {"title": "HR Manager",                 "family": "Business Management",       "weights": {"EQ": 0.85, "SQ": 0.8, "LQ": 0.65, "MQ": 0.6}},
    {"title": "Marketing Manager",          "family": "Business Management",       "weights": {"CQ": 0.75, "SQ": 0.8, "LQ": 0.6, "MQ": 0.65}},
    {"title": "Operations Manager",         "family": "Business Management",       "weights": {"DQ": 0.8, "FQ": 0.7, "LQ": 0.65, "IQ": 0.6}},
    # Banking & Finance
    {"title": "Financial Analyst",          "family": "Banking & Finance",         "weights": {"IQ": 0.9, "DQ": 0.8, "FQ": 0.75, "MQ": 0.6}},
    {"title": "Chartered Accountant",       "family": "Banking & Finance",         "weights": {"IQ": 0.85, "FQ": 0.8, "DQ": 0.7, "MQ": 0.7}},
    # Entrepreneurship & Sales
    {"title": "Entrepreneur / Founder",     "family": "Entrepreneurship",          "weights": {"LQ": 0.85, "CQ": 0.8, "AQ": 0.85, "MQ": 0.9, "DQ": 0.7}},
    {"title": "Sales Executive",            "family": "Sales & Marketing",         "weights": {"SQ": 0.9, "EQ": 0.7, "MQ": 0.8, "LQ": 0.55}},
    {"title": "Digital Marketing Specialist","family": "Sales & Marketing",        "weights": {"CQ": 0.8, "SQ": 0.75, "IQ": 0.6, "MQ": 0.65}},
    # Education & Research
    {"title": "School Teacher",             "family": "Education & Research",      "weights": {"EQ": 0.8, "SQ": 0.85, "MQ": 0.7, "FQ": 0.6}},
    {"title": "University Professor",       "family": "Education & Research",      "weights": {"IQ": 0.9, "SQ": 0.75, "CQ": 0.65, "MQ": 0.65}},
    {"title": "Research Scientist",         "family": "Education & Research",      "weights": {"IQ": 0.95, "FQ": 0.8, "CQ": 0.65, "MQ": 0.7}},
    # Legal & Government
    {"title": "Lawyer / Advocate",          "family": "Legal & Judiciary",         "weights": {"IQ": 0.85, "SQ": 0.8, "DQ": 0.8, "FQ": 0.65}},
    {"title": "Judicial Services",          "family": "Legal & Judiciary",         "weights": {"IQ": 0.9, "DQ": 0.85, "EQ": 0.65, "FQ": 0.7}},
    {"title": "Civil Services (UPSC/PCS)",  "family": "Government & Administration","weights": {"IQ": 0.85, "LQ": 0.75, "DQ": 0.8, "SQ": 0.7}},
    {"title": "Police / Defence Officer",   "family": "Defence & Security",        "weights": {"PQ": 0.8, "DQ": 0.8, "LQ": 0.7, "MQ": 0.75}},
    # Creative & Media
    {"title": "Graphic / UI Designer",      "family": "Arts & Design",             "weights": {"CQ": 0.9, "IQ": 0.6, "FQ": 0.65, "AQ": 0.55}},
    {"title": "Architect",                  "family": "Arts & Design",             "weights": {"IQ": 0.85, "CQ": 0.8, "DQ": 0.7, "FQ": 0.6}},
    {"title": "Animator / VFX Artist",      "family": "Arts & Design",             "weights": {"CQ": 0.85, "IQ": 0.65, "FQ": 0.7, "PQ": 0.55}},
    {"title": "Journalist / Media",         "family": "Media & Communication",     "weights": {"SQ": 0.85, "CQ": 0.7, "IQ": 0.65, "MQ": 0.6}},
    {"title": "Film / Content Creator",     "family": "Media & Communication",     "weights": {"CQ": 0.85, "SQ": 0.75, "EQ": 0.65, "MQ": 0.65}},
    {"title": "Musician / Performer",       "family": "Performing Arts",           "weights": {"CQ": 0.9, "PQ": 0.65, "EQ": 0.7, "MQ": 0.75}},
    {"title": "Writer / Author",            "family": "Writing & Publishing",      "weights": {"CQ": 0.85, "IQ": 0.7, "FQ": 0.75, "MQ": 0.65}},
    # Sports & Wellness
    {"title": "Professional Athlete",       "family": "Sports & Athletics",        "weights": {"PQ": 0.95, "MQ": 0.85, "FQ": 0.75, "DQ": 0.6}},
    {"title": "Sports Coach",               "family": "Sports & Athletics",        "weights": {"PQ": 0.75, "LQ": 0.7, "SQ": 0.75, "EQ": 0.65}},
    {"title": "Yoga / Wellness Coach",      "family": "Wellness",                  "weights": {"EQ": 0.8, "PQ": 0.7, "SQ": 0.75, "MQ": 0.6}},
    # Social & Public Service
    {"title": "Social Worker / NGO Lead",   "family": "Social Service",            "weights": {"EQ": 0.9, "SQ": 0.8, "LQ": 0.65, "MQ": 0.65}},
    {"title": "Politics / Public Leadership","family": "Public Leadership",        "weights": {"LQ": 0.9, "SQ": 0.85, "EQ": 0.75, "DQ": 0.7}},
    {"title": "Hospitality Manager",        "family": "Hospitality & Tourism",     "weights": {"SQ": 0.85, "EQ": 0.7, "LQ": 0.6, "MQ": 0.6}},
    # Agriculture & Environment
    {"title": "Agriculture Scientist",      "family": "Agriculture & Environment", "weights": {"IQ": 0.8, "AQ": 0.65, "MQ": 0.6, "FQ": 0.6}},
    {"title": "Environmental Specialist",   "family": "Agriculture & Environment", "weights": {"IQ": 0.8, "CQ": 0.6, "AQ": 0.65, "MQ": 0.6}},
    # Logistics & Transportation
    {"title": "Pilot / Aviation",           "family": "Transportation",            "weights": {"IQ": 0.85, "PQ": 0.75, "FQ": 0.85, "DQ": 0.8}},
    {"title": "Supply Chain Manager",       "family": "Logistics",                 "weights": {"IQ": 0.75, "DQ": 0.8, "FQ": 0.7, "LQ": 0.55}},
    # Skilled trades
    {"title": "Skilled Technician",         "family": "Skilled Trades",            "weights": {"PQ": 0.8, "IQ": 0.65, "FQ": 0.65, "MQ": 0.55}},
    {"title": "Fashion Designer",           "family": "Fashion & Lifestyle",       "weights": {"CQ": 0.85, "SQ": 0.65, "FQ": 0.6, "MQ": 0.6}},
    # Finance edge cases
    {"title": "Investment Banker",          "family": "Banking & Finance",         "weights": {"IQ": 0.9, "DQ": 0.85, "MQ": 0.7, "LQ": 0.65}},
    {"title": "Insurance Analyst",          "family": "Banking & Finance",         "weights": {"IQ": 0.8, "DQ": 0.75, "FQ": 0.7, "MQ": 0.6}},
]

CAREER_FAMILIES = sorted({e["family"] for e in CAREER_ENTRIES})


def _match_score(quotients: Dict[str, Optional[float]], weights: Dict[str, float]) -> Optional[float]:
    total = 0.0
    weight_sum = 0.0
    for q, emphasis in weights.items():
        val = quotients.get(q)
        if val is None:
            continue
        total += float(val) * float(emphasis)
        weight_sum += float(emphasis)
    if weight_sum <= 0:
        return None
    return min(1.0, total / weight_sum)


def match_careers_from_quotients(
    quotients: Dict[str, Optional[float]],
    top_n: int = 25,
) -> List[Dict[str, Any]]:
    """Return careers ranked by suitability against the subject's quotients."""
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for entry in CAREER_ENTRIES:
        score = _match_score(quotients, entry["weights"])
        if score is None:
            continue
        scored.append((score, {
            "title": entry["title"],
            "family": entry["family"],
            "match_score": round(score, 4),
            "required_quotients": list(entry["weights"].keys()),
        }))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_n]]


def top_quotient_strengths(
    quotients: Dict[str, Optional[float]],
    weights: Dict[str, float],
    threshold: float = 0.55,
) -> List[str]:
    from .quotient_engine import QUOTIENT_LABELS
    out = []
    for q, emphasis in sorted(weights.items(), key=lambda kv: kv[1], reverse=True):
        if emphasis < 0.65:
            continue
        val = quotients.get(q)
        if val is not None and val >= threshold:
            out.append(f"{QUOTIENT_LABELS.get(q, q)} ({round(val * 100)}%)")
    return out[:3]
