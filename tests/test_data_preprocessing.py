import pytest
import pandas as pd
import numpy as np
from src.data_preprocessing import DataPreprocessor
from src.config import RANDOM_STATE

class TestDataPreprocessor:
    
    @pytest.fixture
    def preprocessor(self):
        return DataPreprocessor()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        np.random.seed(RANDOM_STATE)
        n_samples = 1000
        
        # Create synthetic data similar to credit card dataset
        data = pd.DataFrame({
            'Time': np.random.uniform(0, 172800, n_samples),
            **{f'V{i}': np.random.normal(0, 1, n_samples) for i in range(1, 29)},
            'Amount': np.random.exponential(100, n_samples),
            'Class': np.random.choice([0, 1], n_samples, p=[0.98, 0.02])
        })
        
        return data
    
    def test_load_data_file_exists(self, preprocessor, tmp_path):
        """Test if data loading works when file exists"""
        # This would require mocking or using test data
        pass
    
    def test_preprocess_features(self, preprocessor, sample_data):
        """Test feature preprocessing"""
        X, y = preprocessor.preprocess_features(sample_data)
        
        # Check shapes
        assert X.shape[0] == sample_data.shape[0]
        assert X.shape[1] == sample_data.shape[1] - 1  # Minus target column
        assert len(y) == sample_data.shape[0]
        
        # Check if Time and Amount are scaled
        assert X['Time'].std() < sample_data['Time'].std()
        assert X['Amount'].std() < sample_data['Amount'].std()
    
    def test_handle_imbalance(self, preprocessor, sample_data):
        """Test class imbalance handling"""
        X, y = preprocessor.preprocess_features(sample_data)
        
        # Test undersampling
        X_balanced, y_balanced = preprocessor.handle_imbalance(X, y, method='undersample')
        
        # Check if classes are balanced
        unique, counts = np.unique(y_balanced, return_counts=True)
        assert len(unique) == 2
        assert counts[0] == counts[1]  # Should be balanced
    
    def test_split_data(self, preprocessor, sample_data):
        """Test train-test split"""
        X, y = preprocessor.preprocess_features(sample_data)
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
        
        # Check split proportions
        assert len(X_train) == int(len(X) * 0.8)
        assert len(X_test) == int(len(X) * 0.2)
        
        # Check stratification maintained
        train_ratio = sum(y_train) / len(y_train)
        test_ratio = sum(y_test) / len(y_test)
        assert abs(train_ratio - test_ratio) < 0.01
