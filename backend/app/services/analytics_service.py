from collections import Counter
from datetime import datetime
from backend.app.repositories.complaint_repository import ComplaintRepository
from backend.app.services.clustering_service import cluster_summary


def overview():
    rows = ComplaintRepository().all()
    return {
        "total_complaints": len(rows),
        "high_critical": sum(x.get("urgency") in ("High", "Critical") for x in rows),
        "low_confidence": sum((x.get("confidence") or 0) < 0.75 for x in rows),
        "active_clusters": len({x.get("cluster_id") for x in rows if x.get("cluster_id") is not None}),
        "potential_emerging_clusters": sum(x["potential_emerging"] for x in cluster_summary()),
        "department_distribution": dict(Counter(x.get("department", "Unknown") for x in rows)),
        "urgency_distribution": dict(Counter(x.get("urgency", "Unknown") for x in rows)),
    }


def departments():
    rows = ComplaintRepository().all()
    return dict(Counter(x.get("department", "Unknown") for x in rows))


def trends():
    rows = ComplaintRepository().all()
    counts = Counter((x.get("created_at", "")[:10] or "unknown") for x in rows)
    return [{"date": k, "count": v} for k, v in sorted(counts.items())]
