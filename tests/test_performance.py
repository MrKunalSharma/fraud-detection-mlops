import time
import pytest
from src.model_serving import app
from fastapi.testclient import TestClient

class TestPerformance:
    
    def test_prediction_latency(self, client, sample_transaction):
        """Ensure predictions complete within SLA"""
        start = time.time()
        response = client.post("/predict", json=sample_transaction)
        latency = time.time() - start
        
        assert latency < 0.1  # 100ms SLA
        assert response.status_code in [200, 503]
