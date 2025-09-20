import pytest
import pandas as pd
import numpy as np
from src.model_training import ModelTrainer
from sklearn.datasets import make_classification

class TestModelTrainer:
    
    @pytest.fixture
    def trainer(self):
        return ModelTrainer()
    
    @pytest.fixture
    def synthetic_data(self):
        """Create synthetic data for testing"""
        X, y = make_classification(
            n_samples=1000,
            n_features=30,
            n_informative=20,
            n_redundant=5,
            n_classes=2,
            flip_y=0.05,
            class_sep=2.0,
            random_state=42
        )
        
        # Create feature names similar to credit card dataset
        feature_names = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        X_df = pd.DataFrame(X, columns=feature_names)
        
        return X_df, y
    
    def test_model_initialization(self, trainer):
        """Test if all models are initialized correctly"""
        assert len(trainer.models) == 3
        assert 'random_forest' in trainer.models
        assert 'logistic_regression' in trainer.models
        assert 'decision_tree' in trainer.models
    
    def test_train_single_model(self, trainer, synthetic_data):
        """Test training a single model"""
        X, y = synthetic_data
        model_name = 'random_forest'
        model = trainer.models[model_name]
        
        trained_model = trainer.train_model(model, X, y, model_name)
        
        # Check if model is trained
        assert hasattr(trained_model, 'predict')
        predictions = trained_model.predict(X[:10])
        assert len(predictions) == 10
    
    def test_evaluate_model(self, trainer, synthetic_data):
        """Test model evaluation"""
        X, y = synthetic_data
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train and evaluate
        model = trainer.models['random_forest']
        trained_model = trainer.train_model(model, X_train, y_train, 'random_forest')
        metrics = trainer.evaluate_model(trained_model, X_test, y_test, 'random_forest')
        
        # Check metrics
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 'roc_auc' in metrics
        
        # Check metric ranges
        for metric in ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']:
            assert 0 <= metrics[metric] <= 1
