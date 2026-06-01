"""FastAPI service for HR attrition prediction."""
import json
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from tensorflow import keras

from api.database import PredictionRecord, get_db, init_db
from api.schemas import EmployeeFeatures, PredictionLog, PredictionResponse

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "attrition_model.keras"
PREPROCESSOR_PATH = ROOT / "models" / "preprocessor.joblib"

# Loaded on startup
_artifacts: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model + preprocessor once at startup."""
    init_db()
    if MODEL_PATH.exists() and PREPROCESSOR_PATH.exists():
        _artifacts["model"] = keras.models.load_model(MODEL_PATH)
        _artifacts["preprocessor"] = joblib.load(PREPROCESSOR_PATH)
        print("✅ Model & preprocessor loaded")

        # Warmup prediction biar tidak lambat di request pertama
        dummy = np.zeros((1, _artifacts["model"].input_shape[1]))
        _artifacts["model"].predict(dummy, verbose=0)
        print("✅ Warmup complete")
    else:
        print("⚠️  Model files not found. Train first: python src/train.py")
    yield
    _artifacts.clear()


app = FastAPI(
    title="HR Attrition Predictor API",
    description="Predict employee attrition risk for proactive HR intervention.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - allow Streamlit (default 8501) and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _risk_level(prob: float) -> str:
    if prob < 0.3:
        return "Low"
    if prob < 0.6:
        return "Medium"
    return "High"


def _recommendation(prob: float) -> str:
    if prob < 0.3:
        return "Low risk. Continue regular engagement check-ins."
    if prob < 0.6:
        return (
            "Medium risk. Schedule a 1-on-1 to discuss career growth, "
            "workload, and satisfaction."
        )
    return (
        "High risk. Immediate retention conversation recommended. "
        "Review compensation, role fit, and work-life balance."
    )


@app.get("/")
def root():
    return {
        "service": "HR Attrition Predictor",
        "status": "ok",
        "model_loaded": "model" in _artifacts,
    }


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": "model" in _artifacts}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: EmployeeFeatures, db: Session = Depends(get_db)):
    if "model" not in _artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded. Train first.")

    # Build single-row DataFrame in correct column order
    df = pd.DataFrame([features.model_dump()])

    # Transform + predict
    X = _artifacts["preprocessor"].transform(df)
    prob = float(_artifacts["model"].predict(X, verbose=0)[0][0])

    pred = "Will Leave" if prob >= 0.5 else "Will Stay"
    risk = _risk_level(prob)
    rec = _recommendation(prob)

    # Log to DB
    record = PredictionRecord(
        probability=prob,
        prediction=pred,
        risk_level=risk,
        input_payload=json.dumps(features.model_dump()),
    )
    db.add(record)
    db.commit()

    return PredictionResponse(
        probability=round(prob, 4),
        prediction=pred,
        risk_level=risk,
        recommendation=rec,
    )


@app.get("/predictions", response_model=list[PredictionLog])
def list_predictions(limit: int = 20, db: Session = Depends(get_db)):
    """Get most recent predictions for audit / dashboard."""
    rows = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.timestamp.desc())
        .limit(limit)
        .all()
    )
    return rows


@app.delete("/predictions")
def clear_predictions(db: Session = Depends(get_db)):
    """Clear all logged predictions."""
    deleted = db.query(PredictionRecord).delete()
    db.commit()
    return {"deleted": deleted}