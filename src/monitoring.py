"""
Monitoring utilities for tracking model performance and system health
"""

import time
import logging
import json
from datetime import datetime
from pathlib import Path
from prometheus_client import Counter, Histogram, Gauge, Summary
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ModelMonitor:
    """Monitor model performance and drift"""
    
    def __init__(self):
        # Performance metrics
        self.prediction_accuracy = Gauge(
            'model_accuracy_current',
            'Current model accuracy score'
        )
        
        self.data_drift_score = Gauge(
            'data_drift_score',
            'Data drift detection score'
        )
        
        self.model_staleness = Gauge(
            'model_staleness_days',
            'Days since model was last trained'
        )
        
        # Feature statistics tracking
        self.feature_stats = {}
        
    def update_accuracy(self, accuracy):
        """Update current model accuracy"""
        self.prediction_accuracy.set(accuracy)
        logger.info(f"Model accuracy updated: {accuracy:.4f}")
        
    def check_data_drift(self, current_data, reference_data):
        """
        Simple drift detection using statistical tests
        """
        drift_scores = []
        
        for column in current_data.columns:
            if column in reference_data.columns:
                # Calculate mean shift
                current_mean = current_data[column].mean()
                reference_mean = reference_data[column].mean()
                
                if reference_mean != 0:
                    drift = abs(current_mean - reference_mean) / abs(reference_mean)
                    drift_scores.append(drift)
        
        avg_drift = np.mean(drift_scores) if drift_scores else 0
        self.data_drift_score.set(avg_drift)
        
        return avg_drift
    
    def calculate_model_staleness(self, model_path):
        """Calculate how old the model is"""
        if Path(model_path).exists():
            model_time = Path(model_path).stat().st_mtime
            current_time = time.time()
            days_old = (current_time - model_time) / (24 * 3600)
            self.model_staleness.set(days_old)
            return days_old
        return -1
    
    def log_prediction_details(self, prediction, probability, features, latency):
        """Log detailed prediction information for analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prediction": int(prediction),
            "probability": float(probability),
            "latency_ms": float(latency * 1000),
            "features_summary": {
                "amount": float(features.get("Amount", 0)),
                "time": float(features.get("Time", 0))
            }
        }
        
        # Log to file for later analysis
        log_path = Path("logs/predictions.jsonl")
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    def generate_monitoring_report(self):
        """Generate a monitoring report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "accuracy": self.prediction_accuracy._value.get(),
                "drift_score": self.data_drift_score._value.get(),
                "model_age_days": self.model_staleness._value.get()
            },
            "status": "healthy" if self.data_drift_score._value.get() < 0.1 else "warning"
        }
        
        return report


class PerformanceTracker:
    """Track API and system performance"""
    
    def __init__(self):
        self.response_time = Summary(
            'api_response_time_seconds',
            'API response time in seconds'
        )
        
        self.memory_usage = Gauge(
            'memory_usage_mb',
            'Memory usage in MB'
        )
        
        self.cpu_usage = Gauge(
            'cpu_usage_percent',
            'CPU usage percentage'
        )
    
    def track_response_time(self, func):
        """Decorator to track function execution time"""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            self.response_time.observe(time.time() - start)
            return result
        return wrapper
    
    def update_system_metrics(self):
        """Update system resource metrics"""
        try:
            import psutil
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.set(memory.used / 1024 / 1024)
            
            # CPU usage
            cpu = psutil.cpu_percent(interval=1)
            self.cpu_usage.set(cpu)
            
        except ImportError:
            logger.warning("psutil not installed, system metrics unavailable")


# Initialize global monitoring instances
model_monitor = ModelMonitor()
performance_tracker = PerformanceTracker()
