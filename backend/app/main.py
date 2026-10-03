from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1 import health, predictions, complaints, clusters, analytics, models, batch

app = FastAPI(title="Citizen Grievance AI Prototype", version="1.0.0", description="Local academic prototype for AI-assisted citizen grievance analysis.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

for router in [health.router, predictions.router, complaints.router, clusters.router, analytics.router, models.router, batch.router]:
    app.include_router(router, prefix="/api/v1")

@app.get("/")
def root(): return {"name": "Citizen Grievance AI", "docs": "/docs", "api": "/api/v1"}
