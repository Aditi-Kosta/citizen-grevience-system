from pydantic import BaseModel, Field
from typing import Optional, List, Any

class PredictionRequest(BaseModel):
    text: str = Field(min_length=3, max_length=5000)

class SimilarComplaint(BaseModel):
    complaint_id: str
    text: str
    similarity: float
    status: str

class PredictionResponse(BaseModel):
    category: str
    department: str
    confidence: float
    urgency: str
    urgency_score: float
    review_required: bool
    possible_duplicate: bool
    cluster_id: Optional[int] = None
    similar_complaints: List[SimilarComplaint] = []
    model_version: str

class ComplaintCreate(PredictionRequest):
    source_name: str = "manual"
    location_text: Optional[str] = None

class Complaint(ComplaintCreate):
    complaint_id: str
    category: Optional[str] = None
    department: Optional[str] = None
    confidence: Optional[float] = None
    urgency: Optional[str] = None
    status: str = "new"
    cluster_id: Optional[int] = None
    created_at: str

class PaginatedComplaints(BaseModel):
    items: List[Complaint]
    page: int
    page_size: int
    total: int

class ErrorResponse(BaseModel):
    detail: str
