# AI-Powered Citizen Grievance Categorisation & Dynamic Issue Clustering

A portable academic prototype for analysing citizen grievances locally.

## What is included

- React + Vite + Tailwind-style utility UI (implemented with plain CSS utilities for zero extra UI dependency)
- FastAPI versioned API at `/api/v1`
- Local file data layer — **no database, SQLite, Docker or cloud infrastructure**
- Mock mode that works immediately after setup
- TF-IDF + Logistic Regression baseline training/evaluation
- Optional DistilBERT transformer training scaffold
- Optional Sentence Transformer embeddings + HDBSCAN clustering scripts
- Similarity/duplicate detection, transparent urgency assistance & emerging-cluster signals
- Demo data, API tests, ML utilities & reproducible dataset preparation

## Architecture

```text
React Dashboard
      |
      v
FastAPI /api/v1
      |
      v
Service Layer
  |       |       |
ML   Embeddings Analytics
  |       |       |
  +-------+-------+
          |
      Local files
CSV / JSON / NPY / Parquet
```

The frontend communicates only with FastAPI. API routes remain thin and business logic is kept in services.

## Prototype boundaries

This project intentionally does **not** use PostgreSQL, SQLite, MongoDB, MySQL, Docker, Kubernetes, Redis, cloud databases/storage, government-system integrations, authentication, Aadhaar/biometric processing, voice, image/video processing or paid APIs.

## Quick start

### 1. Backend

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

uvicorn backend.app.main:app --reload
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

### 2. Frontend

Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally http://localhost:5173.

### 3. Mock mode

The default configuration uses:

```env
USE_MOCK_MODEL=true
```

This means the complete analyzer works without downloading a large ML model. Submit a complaint such as:

> There is a large pothole near the school and vehicles are struggling to pass.

The dashboard returns a mock-but-structured category, department, confidence, urgency, similarity, cluster and review decision.

## API examples

Health:

```http
GET /api/v1/health
```

Prediction:

```http
POST /api/v1/predictions
Content-Type: application/json

{"text":"There is a large pothole near the school."}
```

List complaints:

```http
GET /api/v1/complaints?page=1&page_size=20
```

## Dataset workflow

The specification identifies the Civic Complaint Prioritization NLP dataset as the primary training source and the Mumbai Nagar Seva BMC dataset as a secondary analytics/testing source. The repository does not redistribute restricted data.

See `data/README.md` for exact source URLs, expected files, canonical columns and preparation instructions.

Then run:

```bash
python scripts/prepare_dataset.py --input data/raw/your_dataset.csv
```

## ML workflow

### Baseline

```bash
python ml/scripts/train_baseline.py --input data/processed/complaints.csv
```

This produces a TF-IDF + Logistic Regression model and actual metrics under `data/evaluations/` and `models/baseline/`.

### Transformer

A DistilBERT fine-tuning scaffold is provided in `ml/scripts/train_transformer.py`. It is intentionally optional because training requires substantially more memory/time than the local mock prototype.

### Embeddings & clustering

```bash
python scripts/generate_embeddings.py --input data/processed/complaints.csv
python scripts/run_clustering.py
```

These scripts use Sentence Transformers and HDBSCAN when their optional dependencies are installed.

## Tests

From the project root:

```bash
pytest
```

## Portability / clone-to-run

- All paths are project-relative.
- `.env` is ignored; `.env.example` is committed.
- Demo data is committed.
- No machine-specific paths are required.
- Required local directories are created automatically.
- No hidden database or Docker setup is required.
- Large/restricted datasets & model checkpoints are documented rather than committed.

## Safety note

This is an academic decision-support prototype. Predictions are AI assistance and must not be treated as authoritative government decisions or autonomous legal, entitlement or grievance-disposal decisions.
