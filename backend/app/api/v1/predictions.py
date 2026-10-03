from fastapi import APIRouter
from backend.app.schemas.common import PredictionRequest, PredictionResponse
from backend.app.services.complaint_service import process
router = APIRouter()
@router.post("/predictions", response_model=PredictionResponse)
def prediction(request: PredictionRequest):
    return process(request.text)
