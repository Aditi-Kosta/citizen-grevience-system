from fastapi import APIRouter, UploadFile, File, HTTPException
import csv, io, uuid
from backend.app.services.complaint_service import create
router = APIRouter()
_jobs = {}

@router.post('/complaints/batch')
async def batch(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.csv'): raise HTTPException(400, 'Only CSV files are supported')
    raw = await file.read()
    if len(raw) > 10_000_000: raise HTTPException(413, 'CSV file is too large')
    try: rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    except UnicodeDecodeError: raise HTTPException(400, 'CSV must be UTF-8 encoded')
    created=[]
    for row in rows:
        text=row.get('complaint_text') or row.get('text') or row.get('complaint')
        if text and text.strip(): created.append(create(text.strip(), row.get('source_name',file.filename), row.get('location_text')))
    job_id=f'local-{uuid.uuid4().hex[:8]}'
    _jobs[job_id]={'job_id':job_id,'processed':len(created),'status':'completed'}
    return _jobs[job_id]

@router.get('/jobs/{job_id}')
def job(job_id: str):
    if job_id not in _jobs: raise HTTPException(404,'Job not found')
    return _jobs[job_id]
