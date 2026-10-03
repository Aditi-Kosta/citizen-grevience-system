from fastapi import APIRouter
from backend.app.services.clustering_service import cluster_summary
router = APIRouter()
@router.get("/clusters")
def clusters(): return {"items": cluster_summary()}
@router.get("/clusters/{cluster_id}")
def cluster(cluster_id: int):
    return next((x for x in cluster_summary() if x["cluster_id"] == cluster_id), {"cluster_id": cluster_id, "complaint_count": 0, "potential_emerging": False, "representative_complaints": []})
