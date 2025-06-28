from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

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

class HealthInput(BaseModel):
    bp: List[BPEntry] = Field(default_factory=list)
    weight: List[WeightEntry] = Field(default_factory=list)
    height: List[HeightEntry] = Field(default_factory=list)

class HealthAdvice(BaseModel):
    score: int
    status: str
    recommendations: List[str]
    ai_summary: str