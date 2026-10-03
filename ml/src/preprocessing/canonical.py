CANONICAL_COLUMNS = [
    "complaint_id","source_id","source_name","complaint_text","language","category","department","severity","urgency_score","location_text","latitude","longitude","submitted_at","status","is_duplicate","duplicate_of","cluster_id","classifier_confidence","classifier_model_version","embedding_model_version","created_at","updated_at"
]

def clean_text(text):
    return " ".join(str(text or "").strip().split())
