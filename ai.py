import os
import requests
from models import HealthInput

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_ai_summary(data: HealthInput) -> str:
    def format_entries(label, entries):
        return "\n".join([f"{label} - {e.date.date()}: {e.model_dump(exclude={'date'})}" for e in entries]) or "No data"

    ml_section = ""
    if data.ml_analysis:
        ml = data.ml_analysis
        ml_section = f"""
On-Device ML Analysis (from user's phone):
- Overall Score: {ml.score}/100 ({ml.status})
- Metric Risks: {', '.join(f'{k}: {v}' for k, v in ml.metric_risks.items()) if ml.metric_risks else 'N/A'}
- Trends: {', '.join(f'{k}: {v}' for k, v in ml.trends.items()) if ml.trends else 'N/A'}
- Correlation Alerts: {'; '.join(ml.correlation_alerts) if ml.correlation_alerts else 'None detected'}

Use the ML analysis above to provide more targeted recommendations.
Focus on areas flagged as elevated/high risk and worsening trends.
"""

    prompt = f"""
You are a virtual health assistant. Given the following historical health readings and ML analysis, provide:
- A brief summary of the user's condition.
- Commentary on detected trends and correlations.
- Specific lifestyle recommendations targeting identified risk areas.

Blood Pressure Readings:
{format_entries("BP", data.bp)}

Weight Readings:
{format_entries("Weight", data.weight)}

Height Readings:
{format_entries("Height", data.height)}

Pulse Readings:
{format_entries("Pulse", data.pulse)}

Sleep Readings:
{format_entries("Sleep", data.sleep)}

Glucose Readings:
{format_entries("Glucose", data.glucose)}
{ml_section}
Be concise and medically responsible.
"""

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt.strip()
            }]
        }]
    }

    params = {"key": API_KEY}

    response = requests.post(API_URL, headers=headers, json=payload, params=params)
    if response.status_code != 200:
        return f"ERROR: API returned status {response.status_code}"

    try:
        response_json = response.json()
        parts = response_json["candidates"][0]["content"]["parts"]
        generated_text = parts[0]["text"] if parts else "No AI content found."
        return generated_text.strip()
    except (KeyError, IndexError, TypeError) as e:
        print(f"Parsing error: {e}")
        return "No AI summary generated."
