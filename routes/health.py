from fastapi import APIRouter
from models import HealthInput, HealthAdvice
from ai import generate_ai_summary

router = APIRouter()

# --- Route ---

@router.post("/summary", response_model=HealthAdvice)
async def calculate_health_summary(data: HealthInput):
    print("Received data:")
    print(data)

    # Simple rule-based analysis
    avg_systolic = sum(r.systolic for r in data.bp) / len(data.bp) if data.bp else 0
    avg_diastolic = sum(r.diastolic for r in data.bp) / len(data.bp) if data.bp else 0
    avg_weight = sum(r.weight for r in data.weight) / len(data.weight) if data.weight else 0
    avg_height = sum(r.height for r in data.height) / len(data.height) if data.height else 0

    score = 100
    recommendations = []

    if avg_systolic > 130 or avg_diastolic > 85:
        score -= 20
        recommendations.append("Monitor your blood pressure regularly.")
    if avg_weight / ((avg_height / 100) ** 2) > 25:
        score -= 20
        recommendations.append("Consider a balanced diet and more exercise.")

    status = "Healthy" if score >= 80 else "Needs Attention"

    # Generate AI summary
    ai_summary = generate_ai_summary(data)

    return HealthAdvice(
        score=score,
        status=status,
        recommendations=recommendations,
        ai_summary=ai_summary
    )

@router.get("/status")
async def health_check():
    return {"status": "healthy", "message": "HealthMY FastAPI backend is running"}