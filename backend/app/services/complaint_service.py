from datetime import datetime, timezone
import uuid
from backend.app.config import CONFIDENCE_THRESHOLD, DUPLICATE_THRESHOLD
from backend.app.repositories.complaint_repository import ComplaintRepository
from backend.app.services.classification_service import predict
from backend.app.services.clustering_service import similar_complaints

repo = ComplaintRepository()


def process(text: str):
    result = predict(text)
    sims = similar_complaints(text)
    possible_duplicate = bool(sims and sims[0]["similarity"] >= DUPLICATE_THRESHOLD)
    result.update({
        "review_required": result["confidence"] < CONFIDENCE_THRESHOLD,
        "possible_duplicate": possible_duplicate,
        "cluster_id": None,
        "similar_complaints": sims,
    })
    return result


def create(text, source_name="manual", location_text=None):
    prediction = process(text)
    item = {
        "complaint_id": f"CG-{uuid.uuid4().hex[:8].upper()}",
        "text": text,
        "source_name": source_name,
        "location_text": location_text,
        "category": prediction["category"],
        "department": prediction["department"],
        "confidence": prediction["confidence"],
        "urgency": prediction["urgency"],
        "urgency_score": prediction["urgency_score"],
        "status": "new",
        "cluster_id": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return repo.save(item)
