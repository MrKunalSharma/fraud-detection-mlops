from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd
import joblib
from typing import List, Dict
import logging
from pathlib import Path
import time

from prometheus_client import Counter, Histogram, Gauge, generate_latest

from .config import MODEL_PATH, PROCESSED_DATA_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
prediction_counter = Counter(
    'fraud_predictions_total', 
    'Total number of predictions made',
    ['prediction_type', 'risk_level']
)

prediction_latency = Histogram(
    'fraud_prediction_latency_seconds',
    'Latency of fraud predictions'
)

api_requests = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

# Initialize FastAPI app
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time credit card fraud detection",
    version="1.0.0"
)

# Load model and scaler at startup
MODEL = None
SCALER = None

class TransactionData(BaseModel):
    """Input data schema for prediction"""
    Time: float = Field(..., description="Time elapsed since first transaction")
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float = Field(..., description="Transaction amount")

class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    prediction: int
    probability: float
    risk_level: str
    message: str

@app.on_event("startup")
async def load_models():
    """Load model and scaler on startup"""
    global MODEL, SCALER
    
    try:
        MODEL = joblib.load(MODEL_PATH)
        SCALER = joblib.load(PROCESSED_DATA_PATH / "scaler.pkl")
        logger.info("Model and scaler loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fraud Detection API",
        "endpoints": {
            "prediction": "/predict",
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "scaler_loaded": SCALER is not None
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type="text/plain")

@app.post("/predict", response_model=PredictionResponse)
async def predict(transaction: TransactionData):
    """Make fraud prediction for a transaction"""
    
    start_time = time.time()
    
    if MODEL is None or SCALER is None:
        api_requests.labels(method="POST", endpoint="/predict", status="error").inc()
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Create DataFrame with all features
        features = {
            'Time': transaction.Time,
            'V1': transaction.V1,
            'V2': transaction.V2,
            'V3': transaction.V3,
            'V4': transaction.V4,
            'V5': transaction.V5,
            'V6': transaction.V6,
            'V7': transaction.V7,
            'V8': transaction.V8,
            'V9': transaction.V9,
            'V10': transaction.V10,
            'V11': transaction.V11,
            'V12': transaction.V12,
            'V13': transaction.V13,
            'V14': transaction.V14,
            'V15': transaction.V15,
            'V16': transaction.V16,
            'V17': transaction.V17,
            'V18': transaction.V18,
            'V19': transaction.V19,
            'V20': transaction.V20,
            'V21': transaction.V21,
            'V22': transaction.V22,
            'V23': transaction.V23,
            'V24': transaction.V24,
            'V25': transaction.V25,
            'V26': transaction.V26,
            'V27': transaction.V27,
            'V28': transaction.V28,
            'Amount': transaction.Amount
        }
        
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Scale Time and Amount
        df_scaled = df.copy()
        time_amount = df[['Time', 'Amount']].values
        time_amount_scaled = SCALER.transform(time_amount)
        df_scaled['Time'] = time_amount_scaled[0, 0]
        df_scaled['Amount'] = time_amount_scaled[0, 1]
        
        # Ensure correct column order
        column_order = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
                       'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18',
                       'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27',
                       'V28', 'Amount']
        
        df_scaled = df_scaled[column_order]
        
        # Make prediction using values
        prediction = MODEL.predict(df_scaled.values)[0]
        probability = MODEL.predict_proba(df_scaled.values)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Update metrics
        prediction_type = "fraud" if prediction == 1 else "legitimate"
        prediction_counter.labels(prediction_type=prediction_type, risk_level=risk_level).inc()
        
        # Track latency
        latency = time.time() - start_time
        prediction_latency.observe(latency)
        
        # Track successful request
        api_requests.labels(method="POST", endpoint="/predict", status="success").inc()
        
        # Create response
        response = PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            message="Fraud detected!" if prediction == 1 else "Transaction seems legitimate"
        )
        
        return response
        
    except Exception as e:
        api_requests.labels(method="POST", endpoint="/predict", status="error").inc()
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
