"""FastAPI service for HR attrition prediction (Random Forest) + SHAP explainability."""
import json
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
import io
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api.database import PredictionRecord, get_db, init_db
from api.schemas import EmployeeFeatures, PredictionLog, PredictionResponse

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "attrition_model_rf.joblib"
METRICS_PATH = ROOT / "models" / "metrics_rf.json"
DEFAULT_THRESHOLD = 0.30

# Friendly Indonesian labels per original feature
LABELS = {
    "Age": "Usia", "BusinessTravel": "Perjalanan Dinas", "DailyRate": "Daily Rate",
    "Department": "Departemen", "DistanceFromHome": "Jarak dari Rumah", "Education": "Pendidikan",
    "EducationField": "Bidang Studi", "EnvironmentSatisfaction": "Kepuasan Lingkungan",
    "Gender": "Jenis Kelamin", "HourlyRate": "Hourly Rate", "JobInvolvement": "Keterlibatan Kerja",
    "JobLevel": "Level Jabatan", "JobRole": "Posisi", "JobSatisfaction": "Kepuasan Kerja",
    "MaritalStatus": "Status Pernikahan", "MonthlyIncome": "Gaji Bulanan", "MonthlyRate": "Monthly Rate",
    "NumCompaniesWorked": "Jumlah Perusahaan", "OverTime": "Lembur", "PercentSalaryHike": "Kenaikan Gaji",
    "PerformanceRating": "Rating Performa", "RelationshipSatisfaction": "Kepuasan Hubungan",
    "StockOptionLevel": "Opsi Saham", "TotalWorkingYears": "Total Pengalaman",
    "TrainingTimesLastYear": "Pelatihan", "WorkLifeBalance": "Work-Life Balance",
    "YearsAtCompany": "Lama di Perusahaan", "YearsInCurrentRole": "Lama di Posisi",
    "YearsSinceLastPromotion": "Sejak Promosi", "YearsWithCurrManager": "Lama dgn Manajer",
}

_artifacts: dict = {}


def _load_threshold() -> float:
    try:
        with open(METRICS_PATH) as f:
            return float(json.load(f).get("best_threshold", DEFAULT_THRESHOLD))
    except (FileNotFoundError, ValueError, KeyError):
        return DEFAULT_THRESHOLD


def _orig_of(name, num_cols, cat_cols):
    """Map nama fitur ter-encode (44) → fitur asli (30)."""
    if name in num_cols:
        return name
    for c in cat_cols:
        if name.startswith(c + "_"):
            return c
    return name


def reload_model():
    _artifacts["threshold"] = _load_threshold()
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        _artifacts["model"] = model
        prep = model.named_steps["preprocessor"]
        rf = model.named_steps["rf"]
        num_cols = list(prep.transformers_[0][2])
        cat_cols = list(prep.transformers_[1][2])
        ohe = prep.named_transformers_["cat"]
        feat_names = num_cols + list(ohe.get_feature_names_out(cat_cols))
        _artifacts.update(prep=prep, rf=rf, num_cols=num_cols,
                          cat_cols=cat_cols, feat_names=feat_names)
        # SHAP explainer
        _artifacts["explainer"] = shap.TreeExplainer(rf)
        # Global importance aggregated to original features
        agg = {}
        for n, imp in zip(feat_names, rf.feature_importances_):
            o = _orig_of(n, num_cols, cat_cols)
            agg[o] = agg.get(o, 0.0) + float(imp)
        _artifacts["global_importance"] = dict(
            sorted(agg.items(), key=lambda kv: kv[1], reverse=True))
        print(f"Model + SHAP loaded (threshold={_artifacts['threshold']})")
    else:
        print("Model not found. Train first: python -m src.train_rf")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    reload_model()
    yield
    _artifacts.clear()


app = FastAPI(
    title="HR Attrition Predictor API",
    description="Predict employee attrition risk + SHAP explanations.",
    version="3.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


def _risk_level(p):
    return "Low" if p < 0.30 else ("Medium" if p < 0.60 else "High")


def _recommendation(p):
    if p < 0.30:
        return "Low risk. Continue regular engagement check-ins."
    if p < 0.60:
        return ("Medium risk. Schedule a 1-on-1 to discuss career growth, "
                "workload, and satisfaction.")
    return ("High risk. Immediate retention conversation recommended. "
            "Review compensation, role fit, and work-life balance.")


def _infer(features, db):
    if "model" not in _artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded. Train first.")
    df = pd.DataFrame([features.model_dump()])
    prob = float(_artifacts["model"].predict_proba(df)[0][1])
    thr = _artifacts["threshold"]
    pred = "Will Leave" if prob >= thr else "Will Stay"
    risk = _risk_level(prob)
    rec = _recommendation(prob)
    record = PredictionRecord(probability=prob, prediction=pred, risk_level=risk,
                              input_payload=json.dumps(features.model_dump()))
    db.add(record)
    db.commit()
    return df, prob, pred, risk, rec


@app.get("/")
def root():
    return {"service": "HR Attrition Predictor", "status": "ok",
            "model_loaded": "model" in _artifacts}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": "model" in _artifacts}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: EmployeeFeatures, db: Session = Depends(get_db)):
    _, prob, pred, risk, rec = _infer(features, db)
    return PredictionResponse(probability=round(prob, 4), prediction=pred,
                              risk_level=risk, recommendation=rec)


@app.post("/explain")
def explain(features: EmployeeFeatures, db: Session = Depends(get_db)):
    """Prediksi + faktor pendorong (SHAP). Positif = dorong keluar, negatif = bikin bertahan."""
    df, prob, pred, risk, rec = _infer(features, db)
    prep, num_cols, cat_cols = _artifacts["prep"], _artifacts["num_cols"], _artifacts["cat_cols"]
    feat_names = _artifacts["feat_names"]
    X = prep.transform(df)

    sv = _artifacts["explainer"].shap_values(X)
    if isinstance(sv, list):
        contrib = np.array(sv[1])[0]
    else:
        arr = np.asarray(sv)
        contrib = arr[0, :, 1] if arr.ndim == 3 else arr[0]

    ev = _artifacts["explainer"].expected_value
    base = float(ev[1]) if np.ndim(ev) else float(ev)

    agg = {}
    for n, v in zip(feat_names, contrib):
        o = _orig_of(n, num_cols, cat_cols)
        agg[o] = agg.get(o, 0.0) + float(v)

    raw = features.model_dump()
    items = sorted(agg.items(), key=lambda kv: abs(kv[1]), reverse=True)[:8]
    contributions = [{
        "feature": o, "label": LABELS.get(o, o), "value": round(v, 4),
        "input": raw.get(o), "direction": "naik" if v > 0 else "turun",
    } for o, v in items]

    return {"probability": round(prob, 4), "prediction": pred, "risk_level": risk,
            "recommendation": rec, "base_value": round(base, 4), "contributions": contributions}


@app.get("/feature-importance")
def feature_importance(top: int = 12):
    if "global_importance" not in _artifacts:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    items = list(_artifacts["global_importance"].items())[:top]
    return [{"feature": o, "label": LABELS.get(o, o), "importance": round(v, 4)} for o, v in items]


@app.get("/predictions", response_model=list[PredictionLog])
def list_predictions(limit: int = 20, db: Session = Depends(get_db)):
    return (db.query(PredictionRecord).order_by(PredictionRecord.timestamp.desc())
            .limit(limit).all())


@app.delete("/predictions")
def clear_predictions(db: Session = Depends(get_db)):
    deleted = db.query(PredictionRecord).delete()
    db.commit()
    return {"deleted": deleted}

