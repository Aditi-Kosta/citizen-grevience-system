from fastapi import APIRouter, Query, HTTPException
from backend.app.schemas.common import ComplaintCreate, Complaint, PaginatedComplaints
from backend.app.services.complaint_service import create
from backend.app.repositories.complaint_repository import ComplaintRepository
router = APIRouter()
repo = ComplaintRepository()

@router.post("/complaints", response_model=Complaint)
def add_complaint(request: ComplaintCreate):
    return create(request.text, request.source_name, request.location_text)

@router.get("/complaints", response_model=PaginatedComplaints)
def list_complaints(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), department: str | None = None, category: str | None = None, urgency: str | None = None, status: str | None = None, cluster_id: int | None = None, q: str | None = None):
    rows = repo.filter(department, category, urgency, status, cluster_id, q)
    total = len(rows)
    start = (page - 1) * page_size
    return {"items": rows[start:start+page_size], "page": page, "page_size": page_size, "total": total}

@router.get("/complaints/{complaint_id}", response_model=Complaint)
def get_complaint(complaint_id: str):
    item = repo.get(complaint_id)
    if not item: raise HTTPException(404, "Complaint not found")
    return item
