from fastapi import APIRouter
from models import HealthInput, HealthAdvice
from ai import generate_ai_summary

router = APIRouter()

def safe_avg(values):
    return sum(values) / len(values) if values else None

@router.post("/summary", response_model=HealthAdvice)
async def calculate_health_summary(data: HealthInput):
    score = 100
    recommendations = []

    # BP scoring (relaxed wellness thresholds)
    avg_sys = safe_avg([r.systolic for r in data.bp])
    avg_dia = safe_avg([r.diastolic for r in data.bp])
    if avg_sys is not None and avg_dia is not None:
        if avg_sys >= 135 or avg_dia >= 88:
            score -= 20
            recommendations.append("Your blood pressure is elevated. Consider stress management and reducing sodium.")
        elif avg_sys >= 125 or avg_dia >= 82:
            score -= 10
            recommendations.append("Your blood pressure is slightly above optimal. Monitor it regularly.")

    # BMI scoring (relaxed)
    avg_weight = safe_avg([r.weight for r in data.weight])
    avg_height = safe_avg([r.height for r in data.height])
    if avg_weight is not None and avg_height is not None and avg_height > 0:
        bmi = avg_weight / ((avg_height / 100) ** 2)
        if bmi > 30 or bmi < 17:
            score -= 20
            recommendations.append("Your BMI is outside the healthy range. Consider consulting a nutritionist.")
        elif bmi > 27 or bmi < 18.5:
            score -= 10
            recommendations.append("Your BMI is slightly outside optimal. A balanced diet can help.")

    # Pulse scoring
    avg_pulse = safe_avg([r.pulse for r in data.pulse])
    if avg_pulse is not None:
        if avg_pulse > 100 or avg_pulse < 50:
            score -= 15
            recommendations.append("Your resting pulse is outside the normal range. Consider consulting a doctor.")
        elif avg_pulse > 90 or avg_pulse < 55:
            score -= 8
            recommendations.append("Your pulse is slightly outside the optimal range.")

    # Sleep scoring
    avg_sleep = safe_avg([r.hours for r in data.sleep])
    if avg_sleep is not None:
        if avg_sleep < 5.5 or avg_sleep > 10.5:
            score -= 15
            recommendations.append("Your sleep duration needs attention. Aim for 7-9 hours.")
        elif avg_sleep < 6.5 or avg_sleep > 9.5:
            score -= 8
            recommendations.append("Your sleep is slightly outside the optimal range.")

    # Glucose scoring
    avg_glucose = safe_avg([r.glucose for r in data.glucose])
    if avg_glucose is not None:
        if avg_glucose > 130 or avg_glucose < 65:
            score -= 15
            recommendations.append("Your glucose levels need attention. Consider dietary adjustments.")
        elif avg_glucose > 110:
            score -= 8
            recommendations.append("Your glucose is slightly elevated. Monitor your carbohydrate intake.")

    score = max(0, min(100, score))

    # Blend with ML analysis if provided
    if data.ml_analysis:
        ml = data.ml_analysis
        score = int(0.4 * score + 0.6 * ml.score)
        score = max(0, min(100, score))

    if score >= 80:
        status = "Healthy"
    elif score >= 60:
        status = "Needs Attention"
    else:
        status = "At Risk"

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
