import os
import numpy as np
from huggingface_hub import hf_hub_download
import joblib
from models import HealthInput

_model = None

def _load_model():
    global _model
    if _model is not None:
        return _model
    cache_dir = os.environ.get("HF_CACHE_DIR", "/tmp/hf_cache")
    path = hf_hub_download(
        repo_id="BrejBala/Heart-Disease-Prediction",
        filename="heart_disease_model.joblib",
        cache_dir=cache_dir,
    )
    _model = joblib.load(path)
    return _model


def predict_heart_disease(data: HealthInput) -> float | None:
    if data.age is None:
        return None

    model = _load_model()

    # Map app data to 13 UCI Cleveland features
    avg_sys = (sum(r.systolic for r in data.bp) / len(data.bp)) if data.bp else 120
    avg_pulse = (sum(r.pulse for r in data.pulse) / len(data.pulse)) if data.pulse else 72
    avg_glucose = (sum(r.glucose for r in data.glucose) / len(data.glucose)) if data.glucose else 90
    fbs = 1 if avg_glucose > 120 else 0

    features = np.array([[
        data.age,             # age
        data.sex or 0,        # sex (default female if not set)
        0,                    # cp: asymptomatic
        avg_sys,              # trestbps
        200,                  # chol: population median
        fbs,                  # fbs
        0,                    # restecg: normal
        avg_pulse,            # thalach (proxy: avg pulse)
        0,                    # exang: no
        0.0,                  # oldpeak
        1,                    # slope: flat
        0,                    # ca
        2,                    # thal: normal
    ]])

    proba = model.predict_proba(features)
    # Class 1 = heart disease present
    risk = float(proba[0][1])
    return round(risk, 4)
