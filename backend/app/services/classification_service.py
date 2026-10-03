from pathlib import Path
import json
import re
from backend.app.config import CONFIDENCE_THRESHOLD, MODEL_VERSION, USE_MOCK_MODEL, MODEL_DIR
from backend.app.services.urgency_service import score_urgency

RULES = [
    ("Road Damage", "Roads", ["pothole", "road", "footpath", "pavement", "street"], 0.90),
    ("Water Supply", "Water", ["water", "tap", "pipeline", "supply", "tank"], 0.88),
    ("Sanitation", "Sanitation", ["garbage", "waste", "sewage", "drain", "dirty"], 0.89),
    ("Street Lighting", "Electrical", ["streetlight", "street light", "lamp", "dark road"], 0.91),
    ("Electricity", "Electrical", ["electricity", "power cut", "transformer", "wire", "voltage"], 0.87),
    ("Traffic", "Traffic", ["traffic", "signal", "congestion", "parking", "vehicle"], 0.84),
    ("Public Health", "Health", ["hospital", "clinic", "mosquito", "health", "disease"], 0.82),
]


def _mock(text):
    t = text.lower()
    best = None
    for category, dept, words, conf in RULES:
        hits = sum(1 for w in words if w in t)
        if hits and (best is None or hits > best[0]): best = (hits, category, dept, conf)
    if best:
        _, category, dept, confidence = best
    else:
        category, dept, confidence = "General Civic Issue", "General Services", 0.58
    urgency_score, urgency = score_urgency(text)
    return {"category": category, "department": dept, "confidence": confidence, "urgency": urgency, "urgency_score": urgency_score, "model_version": MODEL_VERSION}


def predict(text: str):
    # Real local model hook. A packaged sklearn model can be loaded later without changing the API.
    model_file = MODEL_DIR / "baseline" / "classifier.joblib"
    if not USE_MOCK_MODEL and model_file.exists():
        try:
            import joblib
            bundle = joblib.load(model_file)
            probabilities = bundle["model"].predict_proba([text])[0]
            idx = int(probabilities.argmax())
            label = bundle["labels"][idx]
            confidence = float(probabilities[idx])
            mapping = bundle.get("departments", {})
            dept = mapping.get(label, "General Services")
            us, urgency = score_urgency(text)
            return {"category": label, "department": dept, "confidence": confidence, "urgency": urgency, "urgency_score": us, "model_version": MODEL_VERSION}
        except Exception:
            pass
    return _mock(text)
