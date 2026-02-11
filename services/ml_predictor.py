import json
import os
from models import HealthInput

_model_data = None
_LEAF = -1  # sklearn uses -1 for leaf nodes


def _load_model():
    global _model_data
    if _model_data is not None:
        return _model_data
    model_path = os.path.join(os.path.dirname(__file__), "heart_disease_rf.json")
    with open(model_path) as f:
        _model_data = json.load(f)
    return _model_data


def _predict_tree(tree, features):
    """Walk a single decision tree, return class vote counts at leaf."""
    node = 0
    while tree["children_left"][node] != _LEAF:
        if features[tree["feature"][node]] <= tree["threshold"][node]:
            node = tree["children_left"][node]
        else:
            node = tree["children_right"][node]
    # value shape per node: [[count_class0, count_class1]]
    return tree["value"][node][0]


def predict_heart_disease(data: HealthInput) -> float | None:
    if data.age is None:
        return None

    model = _load_model()

    avg_sys = (sum(r.systolic for r in data.bp) / len(data.bp)) if data.bp else 120
    avg_pulse = (sum(r.pulse for r in data.pulse) / len(data.pulse)) if data.pulse else 72
    avg_glucose = (sum(r.glucose for r in data.glucose) / len(data.glucose)) if data.glucose else 90
    fbs = 1 if avg_glucose > 120 else 0

    features = [
        data.age,        # age
        data.sex or 0,   # sex
        0,               # cp: asymptomatic
        avg_sys,         # trestbps
        200,             # chol: population median
        fbs,             # fbs
        0,               # restecg: normal
        avg_pulse,       # thalach (proxy)
        0,               # exang
        0.0,             # oldpeak
        1,               # slope: flat
        0,               # ca
        2,               # thal: normal
    ]

    # Aggregate votes from all trees
    total_class0 = 0.0
    total_class1 = 0.0
    for tree in model["trees"]:
        counts = _predict_tree(tree, features)
        s = counts[0] + counts[1]
        if s > 0:
            total_class0 += counts[0] / s
            total_class1 += counts[1] / s

    n = len(model["trees"])
    risk = total_class1 / n
    return round(risk, 4)
