from fastapi import APIRouter
from backend.app.services.analytics_service import overview, departments, trends
from backend.app.services.clustering_service import cluster_summary
router = APIRouter()
@router.get("/analytics/overview")
def get_overview(): return overview()
@router.get("/analytics/departments")
def get_departments(): return departments()
@router.get("/analytics/trends")
def get_trends(): return trends()
@router.get("/analytics/clusters")
def get_clusters(): return cluster_summary()
