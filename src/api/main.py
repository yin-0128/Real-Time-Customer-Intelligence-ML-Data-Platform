from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="Customer Churn Prediction API")

# Load model
MODEL_PATH = "artifacts/churn_model.pkl"
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = None
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

class PredictionRequest(BaseModel):
    days_active: int
    total_events: int
    avg_event_value: float

class PredictionResponse(BaseModel):
    churn_prediction: int
    probability: float

@app.get("/")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    features = [[request.days_active, request.total_events, request.avg_event_value]]
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    
    return PredictionResponse(
        churn_prediction=int(prediction),
        probability=float(probability)
    )
