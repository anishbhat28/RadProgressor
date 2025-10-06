"""Pydantic schemas for request/response payloads."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class CVResult(BaseModel):
    """Computer vision analysis result."""
    labels: Dict[str, float] = Field(..., description="Label probabilities")
    severity_score: float = Field(..., description="Overall severity score (0-1)")


class NLPResult(BaseModel):
    """NLP analysis result."""
    sections: Dict[str, str] = Field(..., description="Extracted report sections")
    change: str = Field(..., description="Change classification: improved/stable/worsened")
    delta: int = Field(..., description="Change delta: -1/0/+1")


class ProgressionResult(BaseModel):
    """Progression analysis result."""
    progression_score: float = Field(..., description="Overall progression score (0-1)")
    trend_direction: str = Field(..., description="Trend direction: up/down/flat")
    last_delta: float = Field(..., description="Change from previous scan")


class GenAIResult(BaseModel):
    """GenAI summary result."""
    clinician_summary: str = Field(..., description="Clinical-style summary")
    patient_summary: str = Field(..., description="Patient-friendly summary")


class StudyAnalysis(BaseModel):
    """Complete study analysis result."""
    patient_id: str
    study_date: str
    cv_result: CVResult
    nlp_result: NLPResult
    progression_result: ProgressionResult
    genai_result: GenAIResult


class AnalyzeRequest(BaseModel):
    """Request payload for /api/analyze endpoint."""
    patient_id: str = Field(..., description="Patient identifier")
    study_date: str = Field(..., description="Study date (YYYY-MM-DD)")
    report_text: Optional[str] = Field(None, description="Radiology report text")


class TimelineEntry(BaseModel):
    """Timeline entry for progression tracking."""
    date: str
    progression_score: float
    key_labels: Dict[str, float]
    change: str


class PatientTimeline(BaseModel):
    """Patient timeline response."""
    patient_id: str
    timeline: List[TimelineEntry]


class PatientSnapshot(BaseModel):
    """Patient snapshot response."""
    patient_id: str
    last_study: StudyAnalysis
    timeline_summary: Dict[str, Any]
