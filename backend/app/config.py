from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / os.getenv("DATA_DIR", "data")
MODEL_DIR = ROOT / os.getenv("MODEL_DIR", "models")
CONFIDENCE_THRESHOLD = float(os.getenv("CLASSIFICATION_CONFIDENCE_THRESHOLD", "0.75"))
DUPLICATE_THRESHOLD = float(os.getenv("DUPLICATE_SIMILARITY_THRESHOLD", "0.90"))
USE_MOCK_MODEL = os.getenv("USE_MOCK_MODEL", "true").lower() == "true"
MODEL_VERSION = os.getenv("CLASSIFIER_MODEL_VERSION", "classifier-v1")

for folder in [DATA_DIR, MODEL_DIR, DATA_DIR / "demo", DATA_DIR / "predictions", DATA_DIR / "clusters", DATA_DIR / "evaluations", DATA_DIR / "exports"]:
    folder.mkdir(parents=True, exist_ok=True)
