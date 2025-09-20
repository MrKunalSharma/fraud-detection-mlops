"""
Utility functions for the fraud detection pipeline
"""

import json
import pickle
import logging
from pathlib import Path
from typing import Dict, Any, Union, List
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

def load_model(model_path: Union[str, Path]):
    """
    Safely load a pickled model
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

def save_model(model, model_path: Union[str, Path]):
    """
    Save model to disk
    """
    try:
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise

def validate_transaction_data(data: Dict[str, float]) -> bool:
    """
    Validate incoming transaction data
    """
    required_features = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
    
    # Check if all required features are present
    missing_features = set(required_features) - set(data.keys())
    if missing_features:
        logger.error(f"Missing features: {missing_features}")
        return False
    
    # Validate data types
    for feature, value in data.items():
        if not isinstance(value, (int, float)):
            logger.error(f"Invalid data type for {feature}: {type(value)}")
            return False
    
    # Validate ranges
    if data['Amount'] < 0:
        logger.error("Amount cannot be negative")
        return False
    
    return True

def preprocess_transaction(transaction: Dict[str, float]) -> pd.DataFrame:
    """
    Preprocess a single transaction for prediction
    """
    # Ensure correct column order
    column_order = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    
    # Create DataFrame
    df = pd.DataFrame([transaction])
    df = df[column_order]
    
    return df

def calculate_risk_score(probability: float) -> Dict[str, Any]:
    """
    Calculate detailed risk score and recommendations
    """
    if probability < 0.3:
        risk_level = "Low"
        action = "Approve"
        color = "green"
    elif probability < 0.7:
        risk_level = "Medium"
        action = "Review"
        color = "yellow"
    else:
        risk_level = "High"
        action = "Block"
        color = "red"
    
    return {
        "risk_level": risk_level,
        "risk_score": round(probability * 100, 2),
        "recommended_action": action,
        "color_code": color
    }

def generate_transaction_id() -> str:
    """
    Generate a unique transaction ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = np.random.randint(1000, 9999)
    return f"TXN-{timestamp}-{random_suffix}"

def log_transaction(transaction_id: str, prediction: int, probability: float, 
                   risk_info: Dict[str, Any], latency: float):
    """
    Log transaction details for audit trail
    """
    log_entry = {
        "transaction_id": transaction_id,
        "timestamp": datetime.now().isoformat(),
        "prediction": prediction,
        "probability": probability,
        "risk_info": risk_info,
        "processing_time_ms": round(latency * 1000, 2)
    }
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs/transactions")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log to daily file
    log_file = log_dir / f"transactions_{datetime.now().strftime('%Y%m%d')}.jsonl"
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    return transaction_id

def create_model_card(model_name: str, metrics: Dict[str, float], 
                     training_date: str) -> Dict[str, Any]:
    """
    Create a model card with metadata and performance metrics
    """
    model_card = {
        "model_details": {
            "name": model_name,
            "version": "1.0.0",
            "type": "Binary Classification",
            "framework": "scikit-learn",
            "training_date": training_date
        },
        "intended_use": {
            "primary_use": "Real-time credit card fraud detection",
            "users": "Financial institutions, payment processors",
            "out_of_scope": "Other types of financial fraud"
        },
        "performance_metrics": metrics,
        "training_data": {
            "dataset": "Credit Card Fraud Detection Dataset",
            "source": "Kaggle",
            "size": "284,807 transactions",
            "features": "30 (Time, V1-V28, Amount)",
            "class_distribution": "Highly imbalanced (0.172% fraud)"
        },
        "ethical_considerations": {
            "bias": "Model may have bias towards certain transaction patterns",
            "fairness": "Regular monitoring required to ensure fair treatment",
            "privacy": "No personal information used, only transaction features"
        }
    }
    
    return model_card

def format_metrics_for_display(metrics: Dict[str, float]) -> str:
    """
    Format metrics dictionary for nice display
    """
    display = "\n=== Model Performance Metrics ===\n"
    for metric, value in metrics.items():
        if metric != "confusion_matrix":
            display += f"{metric.replace('_', ' ').title()}: {value:.4f}\n"
    
    return display
