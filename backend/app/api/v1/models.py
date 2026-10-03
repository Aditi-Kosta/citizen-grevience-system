from fastapi import APIRouter
from pathlib import Path
import json
from backend.app.config import MODEL_VERSION, CONFIDENCE_THRESHOLD, USE_MOCK_MODEL, DATA_DIR
router=APIRouter()
@router.get('/models')
def models(): return {'items':[{'model_version':MODEL_VERSION,'type':'mock' if USE_MOCK_MODEL else 'local','confidence_threshold':CONFIDENCE_THRESHOLD}]}
@router.get('/models/{model_version}')
def model(model_version:str): return {'model_version':model_version,'status':'available' if model_version==MODEL_VERSION else 'unknown'}
@router.get('/evaluations')
def evaluations():
    items=[]
    for p in (DATA_DIR/'evaluations').glob('*.json'):
        try: items.append({'file':p.name,'metrics':json.loads(p.read_text(encoding='utf-8'))})
        except Exception: pass
    return {'items':items}
