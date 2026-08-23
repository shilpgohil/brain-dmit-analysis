"""
DMIT AI Consultant — status messages.
NLP rule-based (no LLM tokens spent here).
Multiple variants per stage → randomised → never feels robotic.
Each status type maps to a shimmer animation level on the frontend.
Mirrors Zenith's status_messages.py architecture exactly.
"""
from __future__ import annotations
import random
from typing import Optional


def _pick(options: list[str]) -> str:
    return random.choice(options)  # NOSONAR


# ── Lifecycle stages ──────────────────────────────────────────────────────────

_ROUTING_ANALYSIS = [
    "Looking into the biometric data",
    "Checking the analysis results",
    "Pulling up what we know about this",
    "Reading the profile data",
]
_ROUTING_CONCEPT = [
    "Scanning DMIT knowledge base",
    "Looking up the science behind this",
    "Checking dermatoglyphics research",
]
_ROUTING_DEFAULT = [
    "Reading your question",
    "Getting started on this",
    "Looking into this for you",
]

_THINKING = [
    "Mapping the right data sections",
    "Figuring out the best way to explain this",
    "Lining up the biometric evidence",
    "Planning the most useful answer for this",
    "Working out which data points matter most",
]

_GENERATING = [
    "Putting the consultation together",
    "Writing up the analysis",
    "Pulling this into a clear answer",
    "Composing the counsellor response",
]

_SEARCHING = [
    "Searching DMIT knowledge base",
    "Looking up the science behind this",
    "Checking dermatoglyphics research",
    "Scanning the knowledge base",
]

_RETRYING = [
    "Taking another pass at this",
    "Trying a different approach",
]

_DEGRADED = [
    "Running a little slower than usual, still working on it",
    "This is taking slightly longer than normal",
]

_ERROR_GENERIC = "Something went wrong on our end. Please try again."
_ERROR_UNAVAILABLE = "The AI service is temporarily unavailable. Please try again in a moment."
_ERROR_STREAM_INTERRUPTED = "That response was interrupted. Please try again."


# ── Virtual tool start messages ────────────────────────────────────────────────

_TOOL_START: dict[str, list[str]] = {
    "load_mi_profile":       [
        "Loading the Multiple Intelligence profile",
        "Pulling up the 8 intelligence scores",
        "Reading Gardner's intelligence mapping",
    ],
    "load_brain_data":       [
        "Mapping brain hemisphere activity",
        "Loading brain architecture data",
        "Reading the lobe dominance scores",
        "Tracing the neural-fingerprint connections",
    ],
    "load_quotients":        [
        "Checking all 10 quotient scores",
        "Loading the cognitive-emotional profile",
        "Pulling up the IQ–DQ quotient stack",
    ],
    "load_fingerprints":     [
        "Examining the fingerprint patterns",
        "Reading the biometric pattern data",
        "Tracing ridge formations across all 10 fingers",
        "Loading dermatoglyphic pattern types",
    ],
    "load_career_matches":   [
        "Reviewing career suitability matches",
        "Checking career fit against quotient profile",
        "Loading top career recommendations",
        "Scanning the career-quotient alignment",
    ],
    "load_personality":      [
        "Analysing the Big-Five personality profile",
        "Loading personality trait scores",
        "Reading the personality dimension data",
    ],
    "load_learning_style":   [
        "Checking how this person learns best",
        "Loading VAK learning style data",
        "Reading the visual-auditory-kinesthetic split",
    ],
    "load_development_plan": [
        "Loading the 30-day development roadmap",
        "Pulling up action steps and goals",
        "Reading the development priority sequence",
    ],
    "load_atd_analysis":     [
        "Checking the palm ATD angle measurements",
        "Loading the triradius angle data",
        "Reading fine-motor and sensory indicators",
    ],
    "load_swot":             [
        "Reviewing strengths and development areas",
        "Loading the SWOT quadrant data",
        "Reading the opportunity and threat assessment",
    ],
    "load_extensions":       [
        "Checking the extended metric scores",
        "Loading the 46-module analysis results",
        "Reading deeper biometric indicators",
    ],
    "load_all_sections":     [
        "Loading the complete analysis profile",
        "Reading all data sections",
        "Pulling the full biometric report",
        "Loading every section of the analysis",
    ],
    "search_dmit_knowledge": [
        "Checking DMIT knowledge base",
        "Looking up the science behind this",
        "Scanning dermatoglyphics research",
        "Reading domain knowledge on this topic",
    ],
    "web_search":            [
        "Searching for up-to-date information",
        "Looking this up in real time",
        "Fetching current data on this",
    ],
    "build_chart":           [
        "Preparing the visualisation",
        "Building the chart from your data",
        "Assembling the data graphic",
    ],
    "build_widget":          [
        "Preparing the visual summary",
        "Building the overview panel",
        "Assembling the data display",
    ],
}

# ── Virtual tool done messages ─────────────────────────────────────────────────

_TOOL_DONE: dict[str, list[str]] = {
    "load_mi_profile":       ["Intelligence profile loaded", "MI data is ready"],
    "load_brain_data":       ["Brain architecture data ready", "Hemisphere mapping complete"],
    "load_quotients":        ["Quotient scores loaded", "Cognitive profile ready"],
    "load_fingerprints":     ["Fingerprint data ready", "Pattern analysis loaded"],
    "load_career_matches":   ["Career matches loaded", "Suitability data ready"],
    "load_personality":      ["Personality profile ready", "Trait data loaded"],
    "load_learning_style":   ["Learning style data ready"],
    "load_development_plan": ["Roadmap data loaded", "Action steps ready"],
    "load_atd_analysis":     ["ATD angle data ready"],
    "load_swot":             ["SWOT profile ready", "Strength-weakness data loaded"],
    "load_extensions":       ["Extended metrics loaded"],
    "load_all_sections":     ["Full analysis loaded", "All profile sections ready"],
    "search_dmit_knowledge": ["Knowledge base searched", "DMIT research retrieved"],
    "web_search":            ["Search results ready", "Current information retrieved"],
    "build_chart":           ["Chart ready", "Visualisation built"],
    "build_widget":          ["Summary panel ready", "Visual overview built"],
}

_GENERIC_START = ["Gathering the data needed", "Loading the relevant information"]
_GENERIC_DONE  = ["Data is ready", "Information loaded"]


# ── Public API ─────────────────────────────────────────────────────────────────

def routing_message(is_analysis_query: bool = False, is_concept: bool = False) -> str:
    if is_concept:
        return _pick(_ROUTING_CONCEPT)
    if is_analysis_query:
        return _pick(_ROUTING_ANALYSIS)
    return _pick(_ROUTING_DEFAULT)


def thinking_message() -> str:
    return _pick(_THINKING)


def generating_message() -> str:
    return _pick(_GENERATING)


def searching_message() -> str:
    return _pick(_SEARCHING)


def retrying_message() -> str:
    return _pick(_RETRYING)


def degraded_message() -> str:
    return _pick(_DEGRADED)


def generic_error_message() -> str:
    return _ERROR_GENERIC


def unavailable_message() -> str:
    return _ERROR_UNAVAILABLE


def stream_interrupted_message() -> str:
    return _ERROR_STREAM_INTERRUPTED


def tool_call_message(tool_name: str) -> str:
    templates = _TOOL_START.get(tool_name)
    return _pick(templates) if templates else _pick(_GENERIC_START)


def tool_done_message(tool_name: str, is_error: bool = False) -> str:
    if is_error:
        return "Ran into an issue — continuing with what's available"
    templates = _TOOL_DONE.get(tool_name)
    return _pick(templates) if templates else _pick(_GENERIC_DONE)
