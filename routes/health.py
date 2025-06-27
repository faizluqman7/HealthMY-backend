from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BPReading(BaseModel):
    systolic: int
    diastolic: int
    date: datetime

class WeightReading(BaseModel):
    weight: float
    date: datetime

class HeightReading(BaseModel):
    height: float
    date: datetime

@router.post("/bp")
async def save_bp(reading: BPReading):
    print("Received BP reading:", reading)
    return {"status": "success"}

@router.post("/weight")
async def save_weight(reading: WeightReading):
    print("Received weight:", reading)
    return {"status": "success"}

@router.post("/height")
async def save_height(reading: HeightReading):
    print("Received height:", reading)
    return {"status": "success"}

@router.get("/status")
async def health_check():
    return {"status": "healthy", "message": "HealthMY FastAPI backend is running"}

@router.get("/bp")
async def get_bp_readings():
    # Placeholder for actual BP readings retrieval logic
    return {"status": "success", "readings": []}