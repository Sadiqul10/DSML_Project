from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.config import MODEL_PATH
from src.predict import prepare_for_prediction


app = FastAPI(
    title="DSML 311 Fast Close Prediction API",
    description="DSML project API that predicts whether a 311 service request will close within 48 hours.",
    version="1.0.0",
)

MODEL_BUNDLE = None

FIELD_ALIASES = {
    "created_date": "Created Date",
    "agency": "Agency",
    "complaint_type": "Complaint Type",
    "descriptor": "Descriptor",
    "location_type": "Location Type",
    "incident_zip": "Incident Zip",
    "borough": "Borough",
    "open_data_channel_type": "Open Data Channel Type",
    "latitude": "Latitude",
    "longitude": "Longitude",
}


def load_model():
    global MODEL_BUNDLE
    if MODEL_BUNDLE is None:
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Model file not found: {model_path}",
            )
        MODEL_BUNDLE = joblib.load(model_path)
    return MODEL_BUNDLE


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = {}
    for key, value in payload.items():
        normalized_key = FIELD_ALIASES.get(key, key)
        normalized[normalized_key] = value
    return normalized


@app.get("/")
def root():
    return {
        "message": "DSML 311 Fast Close Prediction API",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict",
    }


@app.get("/health")
def health():
    model_exists = Path(MODEL_PATH).exists()
    return {"status": "ok", "model_loaded": model_exists}


@app.post("/predict")
def predict(payload: dict[str, Any]):
    bundle = load_model()
    pipeline = bundle["pipeline"]
    features = bundle["features"]
    fast_close_hours = bundle.get("fast_close_hours", 48)

    row = normalize_payload(payload)
    df = pd.DataFrame([row])
    prepared = prepare_for_prediction(df)

    try:
        probability = float(pipeline.predict_proba(prepared[features])[:, 1][0])
        prediction = int(pipeline.predict(prepared[features])[0])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "fast_close_prediction": prediction,
        "fast_close_label": "fast_close" if prediction == 1 else "slow_close",
        "fast_close_probability": round(probability, 4),
        "fast_close_hours": fast_close_hours,
    }
