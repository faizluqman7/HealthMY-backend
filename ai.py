import os
import requests
from models import HealthInput

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY=os.getenv("GOOGLE_API_KEY")

def generate_ai_summary(data: HealthInput) -> str:
    def format_entries(label, entries):
        return "\n".join([f"{label} - {e.date.date()}: {e.dict(exclude={'date'})}" for e in entries])

    prompt = f"""
You are a virtual health assistant. Given the following historical health readings, provide:
- A brief summary of the user's condition.
- Any trends or concerns.
- Lifestyle recommendations.

Blood Pressure Readings:
{format_entries("BP", data.bp)}

Weight Readings:
{format_entries("Weight", data.weight)}

Height Readings:
{format_entries("Height", data.height)}

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
    print(response.status_code)
    print(f"Response Body: {response.text}")  # Print the response for debugging
    if response.status_code != 200:
        return f"ERROR: API returned status {response.status_code}"

    response_json = response.json()

    # Parse the generated text from response_json safely
    try:
        # Parse nested structure: candidates[0] -> content -> parts[0] -> text
        response_json = response.json()
        parts = response_json["candidates"][0]["content"]["parts"]
        generated_text = parts[0]["text"] if parts else "No AI content found."
        return generated_text.strip()
    except (KeyError, IndexError, TypeError) as e:
        print(f"Parsing error: {e}")
        return "No AI summary generated."
