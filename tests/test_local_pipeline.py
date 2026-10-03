from fastapi.testclient import TestClient
from backend.app.main import app

client=TestClient(app)

def test_health():
 r=client.get('/api/v1/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_prediction():
 r=client.post('/api/v1/predictions',json={'text':'There is a large pothole near the school.'}); assert r.status_code==200; body=r.json(); assert body['category']=='Road Damage'; assert 0<=body['confidence']<=1; assert 'review_required' in body

def test_complaints():
 r=client.get('/api/v1/complaints?page=1&page_size=5'); assert r.status_code==200; assert len(r.json()['items'])<=5

def test_analytics():
 r=client.get('/api/v1/analytics/overview'); assert r.status_code==200; assert r.json()['total_complaints']>=1
