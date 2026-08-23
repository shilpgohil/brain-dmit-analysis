"""
DMIT AI Consultant — dmit_consultant agent.
Architecture: charts/widgets are PRE-BUILT from session data before the LLM call.
The LLM never sees or emits [CHART:] / [WIDGET:] markers — it writes clean prose.
Status messages are NLP-rule-based (no LLM tokens spent on them).
"""
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

from api.ai_consultant.types import DMITStreamChunk, DMITRequestContext
from api.ai_consultant import llm_provider as llm
from api.ai_consultant import status_messages as sm

logger = logging.getLogger(__name__)


# ── Section → virtual tool map ─────────────────────────────────────────────────

_SECTION_TOOLS: Dict[str, str] = {
    "mi_profile":       "load_mi_profile",
    "brain":            "load_brain_data",
    "brain_data":       "load_brain_data",
    "quotients":        "load_quotients",
    "fingerprints":     "load_fingerprints",
    "career":           "load_career_matches",
    "career_matches":   "load_career_matches",
    "personality":      "load_personality",
    "learning_style":   "load_learning_style",
    "development":      "load_development_plan",
    "development_plan": "load_development_plan",
    "atd":              "load_atd_analysis",
    "swot":             "load_swot",
    "extensions":       "load_extensions",
}

# ── Section → best-fit chart keys ─────────────────────────────────────────────

_SECTION_CHARTS: Dict[str, List[str]] = {
    "mi_profile":    ["mi_radar", "mi_ranked_hbar"],
    "brain":         ["brain_hemisphere_bar", "brain_lobes_bar"],
    "brain_data":    ["brain_hemisphere_bar", "brain_lobes_bar"],
    "quotients":     ["quotients_bar", "quotients_radar"],
    "fingerprints":  ["pattern_distribution_pie"],
    "career":        ["career_hbar"],
    "career_matches":["career_hbar"],
    "personality":   ["personality_radar"],
    "learning_style":["learning_doughnut"],
    "development":   [],
    "atd":           [],
    "swot":          [],
    "extensions":    ["extension_bar"],
}

# ── Section → best-fit widget key ────────────────────────────────────────────

_SECTION_WIDGETS: Dict[str, Optional[str]] = {
    "mi_profile":    "mi_strength_ladder",
    "brain":         "brain_summary",
    "brain_data":    "brain_summary",
    "quotients":     "score_grid_quotients",
    "fingerprints":  "finger_map",
    "career":        "career_cards",
    "career_matches":"career_cards",
    "personality":   "trait_pills",
    "learning_style":"learning_guide",
    "development":   "timeline",
    "atd":           "atd_visual",
    "swot":          "swot_matrix",
    "extensions":    None,
}

# ── Stage tool sequences per intent ───────────────────────────────────────────

_INTENT_TOOL_SEQUENCE: Dict[str, List[str]] = {
    "session_query":    ["load_all_sections"],
    "concept_query":    ["search_dmit_knowledge"],
    "visualization":    [],   # filled dynamically
    "comparison":       ["load_brain_data", "load_mi_profile"],
    "development_plan": ["load_development_plan", "load_personality"],
    "deep_dive":        ["load_all_sections"],
    "report_summary":   ["load_all_sections"],
    "free_chat":        [],
}


# ── System prompt ──────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are DMIT Insight, a world-class DMIT (Dermatoglyphics Multiple Intelligence Test) counsellor.

You are consulting for **{candidate_name}**, whose biometric analysis was conducted on {test_date}.
Counsellor: {counsellor_name}

CRITICAL RULES:
1. Use ONLY the data in the SESSION DATA block. Never fabricate scores or facts.
2. If a data point is missing, say: "This wasn't measured in this session."
3. This data belongs to ONE specific person — never reference any other session.
4. Reference specific values when making claims (e.g. "your Intrapersonal at 84%").
5. Write in warm, expert, counsellor-quality prose. Use Markdown: **bold**, *italic*, bullet lists.
6. Be insightful and practical — explain what scores mean in real life.
7. Do NOT output any [CHART:...] or [WIDGET:...] markers. Visual charts are handled separately.
8. Today's date is {current_date}.

--- SESSION DATA ---
{session_context}
--- END SESSION DATA ---
"""


# ── Suggestions generator ──────────────────────────────────────────────────────

def _generate_suggestions(session_data: Dict, used_section: str) -> List[str]:
    candidate = session_data.get("subject_name") or "the candidate"
    pools = {
        "mi_profile":    ["Which careers fit this MI profile?", "Show the 10-quotient scores", "How should this person learn best?", "Explain the brain architecture"],
        "brain":         ["Show the Multiple Intelligence chart", "Explain the lobe-to-finger connection", "Which careers suit this brain type?"],
        "quotients":     ["Show the MI profile radar", "Compare intelligences and quotients", "Create a development plan"],
        "career":        ["Explain the top career in depth", "Show the MI profile behind these careers", "What skills to develop for the #1 career?"],
        "personality":   ["Show the SWOT analysis", "How does personality affect learning?", "What careers suit this personality?"],
        "learning_style":["Show the MI profile chart", "Create a 30-day study plan", "How does the brain architecture affect learning?"],
        "development":   ["Show strengths as a chart", "What careers align with the development goals?", "Show the personality profile"],
        "swot":          ["Show the career cards", "How to build on the strengths?", "Create a development plan"],
        "fingerprints":  ["What do these patterns mean for intelligence?", "Show the brain lobe mapping", "Explain the TRC significance"],
        "atd":           ["Show the overall profile", "How does ATD affect career choices?"],
    }
    base = [
        "Show my intelligence chart",
        "Which career is the best fit?",
        "Explain the brain hemisphere results",
        "Create a personalised development plan",
        "Show the personality SWOT analysis",
        "How should I study best?",
    ]
    specific = pools.get(used_section, [])
    combined = specific + [s for s in base if s.lower() not in [x.lower() for x in specific]]
    return combined[:4]


# ── Main agent ─────────────────────────────────────────────────────────────────

class DMITConsultantAgent:

    async def stream(
        self,
        context: DMITRequestContext,
        section_focus: Optional[str] = None,
        needs_chart: bool = False,
        intent: str = "session_query",
    ) -> AsyncGenerator[str, None]:
        """
        Full streaming flow:
        1. Status: routing
        2. Status: thinking
        3. Pre-build chart/widget specs (instant — no LLM)
        4. Status: tool_call per section
        5. Status: tool_done
        6. Status: generating
        7. Stream LLM text (clean prose, NO markers)
        8. Emit pre-built chart specs
        9. Emit pre-built widget specs
        10. Emit suggestion chips
        11. Done
        """
        # ── Stage 1: Routing ──────────────────────────────────────────────────
        is_analysis = intent not in ("free_chat", "concept_query")
        yield _status("routing", sm.routing_message(is_analysis_query=is_analysis))

        # ── Stage 2: Thinking ─────────────────────────────────────────────────
        yield _status("thinking", sm.thinking_message())

        # ── Stage 3: Pre-build charts/widgets from session data ───────────────
        pre_charts: List[Dict] = []
        pre_widgets: List[Dict] = []

        if section_focus or needs_chart:
            charts_to_build, widget_to_build = _decide_visuals(
                section_focus, needs_chart, intent, context.session_data
            )

            # Emit tool calls for the sections we'll load
            tool_names = _decide_tools(section_focus, intent)
            for tool_name in tool_names:
                yield _status("tool_call", sm.tool_call_message(tool_name))
                # (data is already loaded in context — this is just status feedback)

            # Build chart specs
            for chart_key in charts_to_build[:2]:
                yield _status("tool_call", sm.tool_call_message("build_chart"))
                try:
                    from api.ai_consultant.chart_builder import build_chart_spec
                    spec = build_chart_spec(chart_key, context.session_data)
                    if spec:
                        pre_charts.append(spec)
                        yield _status("tool_done", sm.tool_done_message("build_chart"))
                    else:
                        yield _status("tool_done", sm.tool_done_message("build_chart", is_error=True))
                except Exception as e:
                    logger.warning(f"Chart build failed {chart_key}: {e}")

            # Build widget spec
            if widget_to_build:
                yield _status("tool_call", sm.tool_call_message("build_widget"))
                try:
                    from api.ai_consultant.widget_builder import build_widget_spec
                    spec = build_widget_spec(widget_to_build, context.session_data)
                    if spec:
                        pre_widgets.append(spec)
                        yield _status("tool_done", sm.tool_done_message("build_widget"))
                    else:
                        yield _status("tool_done", sm.tool_done_message("build_widget", is_error=True))
                except Exception as e:
                    logger.warning(f"Widget build failed {widget_to_build}: {e}")

            # Tool done for section loads
            for tool_name in tool_names:
                yield _status("tool_done", sm.tool_done_message(tool_name))

        elif intent == "concept_query":
            yield _status("tool_call", sm.tool_call_message("search_dmit_knowledge"))
            yield _status("tool_done", sm.tool_done_message("search_dmit_knowledge"))

        # ── Stage 4: Build system prompt ──────────────────────────────────────
        system_msg = _SYSTEM_PROMPT.format(
            candidate_name=context.candidate_name,
            test_date=context.test_date or str(datetime.now().date()),
            counsellor_name=context.counsellor_name or "N/A",
            current_date=str(datetime.now().date()),
            session_context=context.session_context_text,
        )

        messages: List[Dict[str, Any]] = [{"role": "system", "content": system_msg}]
        for h in context.conversation_history[-8:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": context.input_text})

        # ── Stage 5: Stream LLM ───────────────────────────────────────────────
        yield _status("generating", sm.generating_message())

        full_response: List[str] = []
        try:
            async for delta in llm.stream_chat(messages, temperature=0.45, use_reasoning=False):
                full_response.append(delta)
                yield _text(delta)
        except Exception as e:
            logger.error(f"DMITConsultant: LLM stream error: {e}")
            yield _status("error", sm.generic_error_message())
            yield _done()
            return

        # ── Stage 6: Emit pre-built charts ────────────────────────────────────
        for chart_spec in pre_charts:
            yield _chart(chart_spec)

        # ── Stage 7: Emit pre-built widgets ──────────────────────────────────
        for widget_spec in pre_widgets:
            yield _widget(widget_spec)

        # ── Stage 8: Suggestion chips ─────────────────────────────────────────
        suggestions = _generate_suggestions(context.session_data, section_focus or "")
        yield _suggestions(suggestions)

        yield _done()


# ── Visual decision logic ──────────────────────────────────────────────────────

def _decide_visuals(
    section_focus: Optional[str],
    needs_chart: bool,
    intent: str,
    session_data: Dict,
) -> Tuple[List[str], Optional[str]]:
    """
    Decide which chart keys and widget key to pre-build.
    Pure logic — no LLM, no network calls.
    """
    charts: List[str] = []
    widget: Optional[str] = None

    # Visualization intent: always show chart
    if intent == "visualization" or needs_chart:
        if section_focus in _SECTION_CHARTS:
            charts = _SECTION_CHARTS[section_focus][:2]
        elif not section_focus:
            charts = ["mi_radar"]  # default

    # Widget: show only when specific section is focused
    if section_focus in _SECTION_WIDGETS:
        widget = _SECTION_WIDGETS[section_focus]

    # Special case: report_summary → show the key quotient grid
    if intent == "report_summary":
        charts = ["quotients_bar"]
        widget = "score_grid_quotients"

    # Special case: comparison → show two charts
    if intent == "comparison":
        charts = ["brain_hemisphere_bar", "mi_radar"]
        widget = "brain_summary"

    # Special case: development_plan → show roadmap widget
    if intent == "development_plan":
        charts = ["mi_ranked_hbar"]
        widget = "timeline"

    return charts, widget


def _decide_tools(section_focus: Optional[str], intent: str) -> List[str]:
    """Which virtual tools to call (for status messages only)."""
    if section_focus:
        tool = _SECTION_TOOLS.get(section_focus)
        return [tool] if tool else ["load_all_sections"]
    return _INTENT_TOOL_SEQUENCE.get(intent, ["load_all_sections"])


# ── Chunk helpers ──────────────────────────────────────────────────────────────

def _status(status: str, msg: str) -> str:
    return DMITStreamChunk(chunk_type="status", status=status, status_message=msg).model_dump_json()

def _text(delta: str) -> str:
    return DMITStreamChunk(chunk_type="text", response=delta).model_dump_json()

def _chart(spec: Dict) -> str:
    return DMITStreamChunk(chunk_type="chart", chart=spec).model_dump_json()

def _widget(spec: Dict) -> str:
    return DMITStreamChunk(chunk_type="widget", widget=spec).model_dump_json()

def _suggestions(qs: List[str]) -> str:
    return DMITStreamChunk(chunk_type="suggestions", suggested_questions=qs).model_dump_json()

def _done() -> str:
    return DMITStreamChunk(chunk_type="done", stream_completed=True).model_dump_json()
