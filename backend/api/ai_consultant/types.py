"""
DMIT AI Consultant — shared type definitions.
Mirrors Zenith's orchestrator/types.py structure.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
import uuid


# ── Intent types ──────────────────────────────────────────────────────────────

class DMITIntentType(str, Enum):
    SESSION_QUERY    = "session_query"    # about specific scores in this session
    CONCEPT_QUERY    = "concept_query"    # "what does whorl mean", DMIT science
    VISUALIZATION    = "visualization"    # "show my MI chart", "visualize quotients"
    COMPARISON       = "comparison"       # "compare left vs right brain"
    DEVELOPMENT_PLAN = "development_plan" # "how can I improve", action steps
    DEEP_DIVE        = "deep_dive"        # comprehensive multi-section analysis
    REPORT_SUMMARY   = "report_summary"   # "give me an overview of results"
    FREE_CHAT        = "free_chat"        # greeting, off-topic, something-else


class DMITIntentResult(BaseModel):
    intent: DMITIntentType
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_agents: List[str]
    needs_chart: bool = False
    section_focus: Optional[str] = None  # "mi_profile" | "career" | "brain" etc.
    reasoning: str = ""


# ── Request context ───────────────────────────────────────────────────────────

class DMITRequestContext(BaseModel):
    partner_id: str
    session_id: str
    thread_id: str
    input_text: str
    session_data: Dict[str, Any] = Field(default_factory=dict)
    session_context_text: str = ""
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    candidate_name: str = "Candidate"
    counsellor_name: str = ""
    test_date: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ── Execution plan ────────────────────────────────────────────────────────────

class ExecutionStrategy(str, Enum):
    SEQUENTIAL  = "sequential"
    PARALLEL    = "parallel"
    CONDITIONAL = "conditional"


class TaskStep(BaseModel):
    step_id: int
    agent: str
    action: str
    input: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[int] = Field(default_factory=list)
    timeout: int = 45
    can_run_parallel: bool = False


class ExecutionPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL
    steps: List[TaskStep]
    estimated_time: int = 5
    reasoning: str = ""


class AgentOutput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    agent_name: str
    step_id: int
    success: bool
    content: Any = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class GatewayResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content: Any
    sources: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    plan_id: Optional[str] = None


# ── Stream chunk ──────────────────────────────────────────────────────────────

class DMITStreamChunk(BaseModel):
    """NDJSON line schema — exact parallel of Zenith's StreamResponse."""
    chunk_type: str                                  # status|text|chart|widget|table|suggestions|done
    response: str = ""
    stream_completed: bool = False
    chart: Optional[Dict[str, Any]] = None
    widget: Optional[Dict[str, Any]] = None
    table: Optional[Dict[str, Any]] = None
    status: Optional[str] = None                     # routing|thinking|tool_call|tool_done|generating|error
    status_message: Optional[str] = None
    suggested_questions: Optional[List[str]] = None
    section_ref: Optional[str] = None               # "MI Profile" | "Career Matches"
