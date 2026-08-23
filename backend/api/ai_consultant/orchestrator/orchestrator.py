"""
DMIT AI Consultant — main orchestrator.
Implements the fast-path: simple queries start streaming immediately.
Mirrors Zenith's orchestrator.process_request pattern.
"""
from __future__ import annotations

import asyncio
import logging
import re
from typing import Any, AsyncGenerator, Dict, Optional

from api.ai_consultant.types import DMITIntentType, DMITRequestContext
from api.ai_consultant.context_builder import format_session_as_context, extract_candidate_meta
from api.ai_consultant.db import get_or_create_thread, get_recent_history
from api.ai_consultant import status_messages as sm
from api.ai_consultant.agents.dmit_consultant import DMITConsultantAgent

logger = logging.getLogger(__name__)

# ── Fast-path keyword detection (no LLM needed) ───────────────────────────────

_SESSION_NOUNS = re.compile(
    r'\b(my|career|intelligence|brain|scores?|quotient|fingerprint|learning|personality|'
    r'swot|strengths?|development|plan|roadmap|mi|iq|eq|profile|result|analysis)\b',
    re.I
)
_VISUAL_KEYWORDS = re.compile(
    r'\b(show|chart|plot|visuali[sz]e|graph|display|draw|diagram|see)\b', re.I
)
_CONCEPT_KEYWORDS = re.compile(
    r'\b(what\s+is|what\s+does|explain|mean|define|how\s+does|why\s+does|what\s+are)\b', re.I
)
_SUMMARY_KEYWORDS = re.compile(
    r'\b(overview|summary|summarize|summarise|full\s+report|brief|all\s+sections)\b', re.I
)

# Section focus from keywords
_SECTION_KEYWORDS: Dict[str, str] = {
    "intelligence|mi|musical|linguistic|logical|spatial|kinesthetic|interpersonal|intrapersonal|naturalistic": "mi_profile",
    r"brain|hemisphere|left\s+brain|right\s+brain|frontal|temporal|parietal|occipital|limbic": "brain",
    r"quotient|iq|eq|cq|aq|sq|pq|lq|mq|fq|dq": "quotients",
    r"career|job|profession|work|occupation": "career",
    r"personality|big.five|openness|conscientiousness|extraversion|agreeableness|neuroticism": "personality",
    r"learning\s+style|study|vak|visual\s+learner|auditory": "learning_style",
    r"swot|strength|weakness|opportunity|threat": "swot",
    r"fingerprint|pattern|whorl|loop|arch|ridge\s+count|trc": "fingerprints",
    r"quotient|iq|eq|cq": "quotients",
    r"development|roadmap|improve|plan|action": "development",
    r"atd|palm|angle|triradius": "atd",
}


def _detect_intent(query: str) -> tuple[DMITIntentType, Optional[str], bool]:
    """
    Rule-based intent detection. Returns (intent, section_focus, needs_chart).
    No LLM call needed for >90% of queries.
    """
    q = query.lower()
    needs_chart = bool(_VISUAL_KEYWORDS.search(q))

    if _SUMMARY_KEYWORDS.search(q):
        return DMITIntentType.REPORT_SUMMARY, None, needs_chart

    if _CONCEPT_KEYWORDS.search(q):
        return DMITIntentType.CONCEPT_QUERY, _detect_section(q), needs_chart

    if _VISUAL_KEYWORDS.search(q):
        return DMITIntentType.VISUALIZATION, _detect_section(q), True

    if re.search(r'\b(improve|develop|practice|better|grow|work\s+on)\b', q, re.I):
        return DMITIntentType.DEVELOPMENT_PLAN, _detect_section(q), needs_chart

    if re.search(r'\b(compare|vs|versus|difference\s+between)\b', q, re.I):
        return DMITIntentType.COMPARISON, _detect_section(q), needs_chart

    # Default: session query if query touches analysis data
    if _SESSION_NOUNS.search(q) or len(query.split()) >= 3:
        return DMITIntentType.SESSION_QUERY, _detect_section(q), needs_chart

    return DMITIntentType.FREE_CHAT, None, False


def _detect_section(query: str) -> Optional[str]:
    for pattern, section in _SECTION_KEYWORDS.items():
        if re.search(pattern, query, re.I):
            return section
    return None


def _is_simple_query(intent: DMITIntentType) -> bool:
    return intent in {
        DMITIntentType.SESSION_QUERY,
        DMITIntentType.FREE_CHAT,
        DMITIntentType.VISUALIZATION,
        DMITIntentType.COMPARISON,
        DMITIntentType.DEVELOPMENT_PLAN,
        DMITIntentType.CONCEPT_QUERY,
    }


# ── Main orchestrator ──────────────────────────────────────────────────────────

class DMITOrchestrator:
    """
    Orchestrates the DMIT AI consultant flow.
    Phase 1: single-agent fast-path (dmit_consultant).
    """

    def __init__(self):
        self._consultant = DMITConsultantAgent()

    async def process_request(
        self,
        session_id: str,
        partner_id: str,
        query: str,
        session_data: Dict[str, Any],
        thread_id: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Main entry. Returns an async generator of NDJSON lines.
        """
        return self._stream(session_id, partner_id, query, session_data, thread_id)

    async def _stream(
        self,
        session_id: str,
        partner_id: str,
        query: str,
        session_data: Dict[str, Any],
        thread_id: Optional[str],
    ) -> AsyncGenerator[str, None]:
        # ── Resolve thread ────────────────────────────────────────────────────
        if not thread_id:
            thread_id = get_or_create_thread(session_id, partner_id)

        # ── Detect intent (fast, rule-based) ──────────────────────────────────
        intent, section_focus, needs_chart = _detect_intent(query)
        logger.info(f"Orchestrator: intent={intent} section={section_focus} needs_chart={needs_chart}")

        # ── Build context ─────────────────────────────────────────────────────
        context_text = format_session_as_context(session_data)
        candidate_name, counsellor_name, test_date = extract_candidate_meta(session_data)
        history = get_recent_history(thread_id, limit=8)

        context = DMITRequestContext(
            partner_id=partner_id,
            session_id=session_id,
            thread_id=thread_id,
            input_text=query,
            session_data=session_data,
            session_context_text=context_text,
            conversation_history=history,
            candidate_name=candidate_name,
            counsellor_name=counsellor_name,
            test_date=test_date,
        )

        # ── Stream from consultant agent ──────────────────────────────────────
        async for chunk in self._consultant.stream(
            context,
            section_focus=section_focus,
            needs_chart=needs_chart,
        ):
            yield chunk


# ── Module-level singleton ────────────────────────────────────────────────────
_orchestrator: Optional[DMITOrchestrator] = None


def get_orchestrator() -> DMITOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = DMITOrchestrator()
    return _orchestrator
