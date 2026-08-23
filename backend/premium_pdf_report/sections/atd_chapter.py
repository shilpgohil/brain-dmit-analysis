"""
ATD Angle Analysis chapter — dedicated PDF section.
Uses the existing real geometric palm-estimate data (angle, confidence,
derived traits). Clearly labeled as an estimate throughout.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

from ..theme import (
    STYLES, NAVY, GOLD, GOLD_DARK, GOLD_LIGHT, GOLD_PALE,
    IVORY, WHITE, CONTENT_W, score_color,
)
from .helpers import section_header_plain, sub_heading, shrink_block

_RANGE_MEANING = {
    "normal": "Normal ATD range — balanced neurological processing speed.",
    "low": "Below-average ATD angle — typically indicates faster neural conduction and fine motor dexterity.",
    "high": "Above-average ATD angle — associated with broader pattern-recognition tendencies.",
}


def _hand_block(label: str, hand: Dict[str, Any]) -> list:
    rows = [
        [Paragraph("Parameter", STYLES["table_header"]),
         Paragraph("Value", STYLES["table_header"]),
         Paragraph("Interpretation", STYLES["table_header"])],
    ]
    angle = hand.get("angle_deg")
    conf = hand.get("confidence")
    method = hand.get("method", "geometric_landmark_estimate")
    rc = hand.get("range_category", "")
    ls = hand.get("learning_speed")
    fm = hand.get("fine_motor_capacity")
    ss = hand.get("sensory_sensitivity")
    interp = hand.get("interpretation", "")

    def row(p, v, i=""):
        return [Paragraph(p, STYLES["table_cell_bold"]),
                Paragraph(str(v), STYLES["table_cell"]),
                Paragraph(i, STYLES["table_cell"])]

    angle_str = f"{angle:.1f}°" if angle is not None else "N/A"
    conf_str = f"{round(conf * 100)}% confidence" if conf is not None else "N/A"
    ls_str = f"{round(ls * 100)}%" if ls is not None else "N/A"
    fm_str = f"{round(fm * 100)}%" if fm is not None else "N/A"
    ss_str = f"{round(ss * 100)}%" if ss is not None else "N/A"

    rows += [
        row("ATD Angle", angle_str, _RANGE_MEANING.get(rc, rc)),
        row("Range Category", rc.title() if rc else "N/A", ""),
        row("Confidence", conf_str, "Geometric landmark estimate from palm photo"),
        row("Measurement Method", "Palm-photo geometric estimate",
            "Not ridge-triradius — a landmark approximation (A, T, D positions)"),
        row("Learning Speed Index", ls_str, "Higher = faster neural processing tendency"),
        row("Fine Motor Capacity", fm_str, "Precision and dexterity potential"),
        row("Sensory Sensitivity", ss_str, "Tactile/sensory processing tendency"),
        row("Interpretation", interp, ""),
    ]

    cw = [CONTENT_W * 0.26, CONTENT_W * 0.22, CONTENT_W * 0.48]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GOLD_PALE, IVORY]),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.4, GOLD_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    items: list = []
    items += sub_heading(label)
    items.append(t)
    return items


def build_atd_chapter(atd_analysis: Dict[str, Any]) -> list:
    if not atd_analysis:
        return []
    left_hand = atd_analysis.get("left_hand")
    right_hand = atd_analysis.get("right_hand")
    if not left_hand and not right_hand:
        return []

    block: list = []
    block += section_header_plain("ATD", "ATD Angle Analysis")
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        "The ATD angle is formed at the base of the palm between three reference points: "
        "the <b>a-triradius</b> (above the index finger), the <b>t-triradius</b> (center of the palm), "
        "and the <b>d-triradius</b> (above the little finger). Its size reflects neurological "
        "organisation during fetal development and correlates with processing speed, fine-motor "
        "capacity, and sensory sensitivity.",
        STYLES["body"],
    ))
    block.append(Spacer(1, 6))
    block.append(Paragraph(
        "<i>Note: Values below are geometric estimates derived from palm-photo landmarks, "
        "not from ridge-triradius measurements. True ridge-triradius detection requires a "
        "ridge-grade palm scan. Confidence levels reflect estimation reliability.</i>",
        STYLES["caption"],
    ))
    block.append(Spacer(1, 8))

    if right_hand and isinstance(right_hand, dict):
        block += _hand_block("Right Hand (Left Brain)", right_hand)
        block.append(Spacer(1, 8))

    if left_hand and isinstance(left_hand, dict):
        block += _hand_block("Left Hand (Right Brain)", left_hand)
        block.append(Spacer(1, 8))

    summary = atd_analysis.get("summary")
    if summary:
        block += sub_heading("Summary")
        block.append(Paragraph(summary, STYLES["body"]))

    story = [shrink_block(block, _label="atd_chapter")]
    return story
