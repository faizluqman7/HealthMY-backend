from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class BPEntry(BaseModel):
    systolic: int
    diastolic: int
    date: datetime

class WeightEntry(BaseModel):
    weight: float
    date: datetime

class HeightEntry(BaseModel):
    height: float
    date: datetime

class PulseEntry(BaseModel):
    pulse: int
    date: datetime

class SleepEntry(BaseModel):
    hours: float
    date: datetime

class GlucoseEntry(BaseModel):
    glucose: float
    date: datetime

class MLAnalysis(BaseModel):
    score: int
    status: str
    metric_risks: dict[str, str] = Field(default_factory=dict)
    trends: dict[str, str] = Field(default_factory=dict)
    correlation_alerts: list[str] = Field(default_factory=list)

class HealthInput(BaseModel):
    bp: List[BPEntry] = Field(default_factory=list)
    weight: List[WeightEntry] = Field(default_factory=list)
    height: List[HeightEntry] = Field(default_factory=list)
    pulse: List[PulseEntry] = Field(default_factory=list)
    sleep: List[SleepEntry] = Field(default_factory=list)
    glucose: List[GlucoseEntry] = Field(default_factory=list)
    ml_analysis: Optional[MLAnalysis] = None

class HealthAdvice(BaseModel):
    score: int
    status: str
    recommendations: List[str]
    ai_summary: str
