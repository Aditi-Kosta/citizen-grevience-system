from collections import Counter
from backend.app.services.embedding_service import embed, cosine
from backend.app.repositories.complaint_repository import ComplaintRepository


def similar_complaints(text, limit=3):
    repo = ComplaintRepository()
    source = embed(text)
    results = []
    for row in repo.all():
        sim = cosine(source, embed(row.get("text", "")))
        if sim > 0:
            results.append({"complaint_id": row["complaint_id"], "text": row["text"], "similarity": round(sim, 3), "status": "similar"})
    return sorted(results, key=lambda x: x["similarity"], reverse=True)[:limit]


def cluster_summary():
    rows = ComplaintRepository().all()
    groups = {}
    for r in rows:
        cid = r.get("cluster_id")
        if cid is not None:
            groups.setdefault(str(cid), []).append(r)
    result = []
    for cid, items in groups.items():
        cats = Counter(x.get("category") for x in items)
        result.append({"cluster_id": int(cid), "label": cats.most_common(1)[0][0] if cats else "Unlabelled", "complaint_count": len(items), "growth": min(100, len(items) * 7), "main_category": cats.most_common(1)[0][0] if cats else "Unlabelled", "potential_emerging": len(items) >= 3, "representative_complaints": [x["text"] for x in items[:3]]})
    return result
