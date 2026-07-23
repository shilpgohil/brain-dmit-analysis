"""
Pydantic schemas for the DMIT API.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PREPROCESSING = "preprocessing"
    EXTRACTING = "extracting"
    MAPPING = "mapping"
    EXTENDING = "extending"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"


class PatternType(str, Enum):
    WHORL = "whorl"
    LOOP = "loop"
    ARCH = "arch"
    ACCIDENTAL = "accidental"
    UNKNOWN = "unknown"


class FingerPosition(str, Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"


class SingularPoint(BaseModel):
    x: float
    y: float
    type: str  # "core" or "delta"


class FingerBiometrics(BaseModel):
    finger_id: str
    finger_type: str
    finger_position: Optional[str] = None  # L1–R5 slot from upload grid
    pattern_type: PatternType
    pattern_subtype: Optional[str] = None
    ridge_count: Optional[int] = None
    fractal_dimension: Optional[float] = None
    quality_score: Optional[float] = None
    quality_tier: Optional[str] = None
    singular_points: Optional[List[SingularPoint]] = None
    minutiae_count: Optional[int] = None
    entropy: Optional[float] = None
    image_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    raw_features: Optional[Dict[str, Any]] = None


class LobeHemispheres(BaseModel):
    left: Optional[float] = None
    right: Optional[float] = None


class BrainLobeCapacity(BaseModel):
    prefrontal_lobe: Optional[float] = None
    posterior_frontal: Optional[float] = None
    parietal_lobe: Optional[float] = None
    temporal_lobe: Optional[float] = None
    occipital_lobe: Optional[float] = None
    left_hemisphere: Optional[float] = None
    right_hemisphere: Optional[float] = None
    dominant_hemisphere: Optional[str] = None
    lobe_hemispheres: Optional[Dict[str, LobeHemispheres]] = None


class AtdHand(BaseModel):
    angle_deg: float
    range_category: str
    learning_speed: float
    fine_motor_capacity: float
    sensory_sensitivity: float
    interpretation: str
    method: Optional[str] = None
    confidence: Optional[float] = None
    source_note: Optional[str] = None


class AtdAnalysis(BaseModel):
    left_hand: Optional[AtdHand] = None
    right_hand: Optional[AtdHand] = None
    summary: Optional[str] = None


class PalmCapture(BaseModel):
    hand: str
    slot: str
    thumbnail_url: Optional[str] = None
    status: str = "pending_analysis"


class MultipleIntelligences(BaseModel):
    linguistic: Optional[float] = None
    logical_mathematical: Optional[float] = None
    spatial: Optional[float] = None
    musical: Optional[float] = None
    bodily_kinesthetic: Optional[float] = None
    interpersonal: Optional[float] = None
    intrapersonal: Optional[float] = None
    naturalistic: Optional[float] = None
    existential: Optional[float] = None


class LearningStyles(BaseModel):
    visual: Optional[float] = None
    auditory: Optional[float] = None
    kinesthetic: Optional[float] = None


class PersonalityProfile(BaseModel):
    openness: Optional[float] = None
    conscientiousness: Optional[float] = None
    extraversion: Optional[float] = None
    agreeableness: Optional[float] = None
    neuroticism: Optional[float] = None


class ExtensionResult(BaseModel):
    name: str
    category: str
    scores: Dict[str, float]
    primary_score: float
    description: Optional[str] = None
    recommendations: Optional[List[str]] = None


class CareerMatch(BaseModel):
    title: str
    category: str
    match_score: float
    key_strengths: List[str]


class PipelineStage(BaseModel):
    id: str
    label: str
    status: str  # "pending" | "running" | "completed" | "failed"
    duration_ms: Optional[float] = None
    detail: Optional[str] = None


class AnalysisSession(BaseModel):
    id: str
    subject_name: Optional[str] = None
    subject_age: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    status: AnalysisStatus
    finger_count: int = 0
    completed_fingers: int = 0
    pipeline_stages: List[PipelineStage] = []


class AnalysisResult(BaseModel):
    session_id: str
    status: AnalysisStatus
    subject_name: Optional[str] = None
    created_at: datetime
    error_message: Optional[str] = None
    fingers: List[FingerBiometrics] = []
    brain_lobes: Optional[BrainLobeCapacity] = None
    multiple_intelligences: Optional[MultipleIntelligences] = None
    learning_styles: Optional[LearningStyles] = None
    personality: Optional[PersonalityProfile] = None
    atd_analysis: Optional[AtdAnalysis] = None
    palms: List[PalmCapture] = []
    extensions: List[ExtensionResult] = []
    career_matches: List[CareerMatch] = []
    pipeline_stages: List[PipelineStage] = []
    report_url: Optional[str] = None
    processing_time_ms: Optional[float] = None
    total_features_extracted: int = 0
    warnings: List[str] = []


class CreateSessionRequest(BaseModel):
    subject_name: Optional[str] = None
    subject_age: Optional[int] = None
    subject_gender: Optional[str] = None
    notes: Optional[str] = None


class AnalyzeRequest(BaseModel):
    session_id: str
    use_preprocessing: bool = False
    generate_pdf: bool = True


class SessionListItem(BaseModel):
    id: str
    subject_name: Optional[str] = None
    created_at: datetime
    status: AnalysisStatus
    finger_count: int
    has_report: bool


class SystemStatus(BaseModel):
    status: str
    pipeline_version: str
    components: Dict[str, bool]
    total_sessions: int
    processing_queue: int
