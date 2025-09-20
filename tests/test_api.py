import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np

class TestAPI:
    
    @pytest.fixture
    def mock_model_and_scaler(self):
        """Mock model and scaler for testing"""
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([0])
        mock_model.predict_proba.return_value = np.array([[0.98, 0.02]])
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[0, 100]])
        
        return mock_model, mock_scaler
    
    @pytest.fixture
    def client(self, mock_model_and_scaler):
        """Create test client with mocked dependencies"""
        mock_model, mock_scaler = mock_model_and_scaler
        
        with patch('src.model_serving.MODEL', mock_model), \
             patch('src.model_serving.SCALER', mock_scaler):
            from src.model_serving import app
            # Set the global variables directly
            import src.model_serving
            src.model_serving.MODEL = mock_model
            src.model_serving.SCALER = mock_scaler
            return TestClient(app)
