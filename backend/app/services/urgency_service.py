import re

CRITICAL = ["fire", "gas leak", "electrocution", "collapse", "life threatening", "dangerous", "emergency"]
HIGH = ["pothole", "overflow", "sewage", "broken streetlight", "accident", "flood", "leak"]


def score_urgency(text: str, base_score: float | None = None):
    t = text.lower()
    score = float(base_score) if base_score is not None else 0.35
    if any(k in t for k in CRITICAL): score = max(score, 0.9)
    elif any(k in t for k in HIGH): score = max(score, 0.72)
    if re.search(r"\b(today|now|immediately|urgent|danger)\b", t): score = min(1.0, score + 0.12)
    if score >= 0.85: label = "Critical"
    elif score >= 0.65: label = "High"
    elif score >= 0.45: label = "Medium"
    else: label = "Routine"
    return round(min(score, 1.0), 3), label
