"""
Quotient Dashboard section — ten-quotient composite profile.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W, CONTENT_H, score_color,
)
from .helpers import section_header_plain, sub_heading, shrink_block

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

QUOTIENT_DESCRIPTIONS = {
    "IQ": "Logical reasoning, pattern recognition, memory, analytical thinking",
    "EQ": "Self-awareness, empathy, emotional stability, social sensitivity",
    "CQ": "Imagination, innovation, original thinking, creative expression",
    "AQ": "Learning agility, resilience, flexibility, recovery from change",
    "SQ": "Communication, interpersonal skills, teamwork, social influence",
    "PQ": "Body coordination, motor skills, kinaesthetic intelligence",
    "LQ": "Vision, strategic thinking, team management, decision authority",
    "MQ": "Goal orientation, persistence, self-discipline, achievement drive",
    "FQ": "Concentration, attention span, mental discipline, task completion",
    "DQ": "Judgment, risk assessment, ethical reasoning, outcome evaluation",
}

_ORDER = ("IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ")


def build_quotient_dashboard(quotients: Dict[str, float]) -> list:
    if not quotients:
        return []

    present = {k: v for k, v in quotients.items() if k in _ORDER and v is not None}
    if not present:
        return []

    block: list = []
    block += section_header_plain("Q", "Brain Potential Dashboard")
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        "The ten-quotient profile is computed as a documented weighted composite of "
        "real biometric and extension scores derived from your fingerprint analysis. "
        "Each quotient reflects a different dimension of innate cognitive potential. "
        "A missing quotient (N/A) means the required fingerprint data was not available "
        "for that dimension — it is never fabricated.",
        STYLES["body"],
    ))
    block.append(Spacer(1, 10))

    # Table
    sub = sub_heading("Ten-Quotient Profile Summary")
    block += sub

    header = [Paragraph(h, STYLES["table_header"])
              for h in ["Quotient", "Full Name", "Score", "Level", "Key Dimension"]]
    rows = [header]
    for key in _ORDER:
        val = present.get(key)
        val_str = f"{round(val * 100)}%" if val is not None else "N/A"
        _, level = score_color(val) if val is not None else (None, "N/A")
        label = QUOTIENT_LABELS.get(key, key)
        desc = QUOTIENT_DESCRIPTIONS.get(key, "")
        rows.append([
            Paragraph(f"<b>{key}</b>", STYLES["table_cell_bold"]),
            Paragraph(label, STYLES["table_cell"]),
            Paragraph(val_str, STYLES["table_cell_bold"]),
            Paragraph(level, STYLES["table_cell"]),
            Paragraph(desc, STYLES["table_cell"]),
        ])

    cw = [
        CONTENT_W * 0.07,
        CONTENT_W * 0.24,
        CONTENT_W * 0.09,
        CONTENT_W * 0.13,
        CONTENT_W * 0.43,
    ]
    t = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (3, -1), "CENTER"),
    ]))
    block.append(t)
    block.append(Spacer(1, 10))

    # Top 3 and lowest 2 highlight pills
    sorted_q = sorted(
        [(k, v) for k, v in present.items()],
        key=lambda kv: kv[1], reverse=True,
    )
    if sorted_q:
        block += sub_heading("Strongest Quotients")
        rows2 = []
        for key, val in sorted_q[:3]:
            rows2.append([
                Paragraph(f"<b>{key}</b>", STYLES["table_cell_bold"]),
                Paragraph(QUOTIENT_LABELS.get(key, key), STYLES["table_cell"]),
                Paragraph(f"{round(val * 100)}%", STYLES["table_cell_bold"]),
                Paragraph(QUOTIENT_DESCRIPTIONS.get(key, ""), STYLES["table_cell"]),
            ])
        pt = Table(rows2, colWidths=[CONTENT_W * 0.08, CONTENT_W * 0.24, CONTENT_W * 0.10, CONTENT_W * 0.53])
        pt.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GOLD_PALE, IVORY]),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
            ("BOX", (0, 0), (-1, -1), 1.0, GOLD),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        block.append(pt)

    story = [shrink_block(block, max_height=CONTENT_H - 0.4 * inch, _label="quotient_dashboard")]
    return story
