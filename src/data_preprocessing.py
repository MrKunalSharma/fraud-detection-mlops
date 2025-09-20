import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
import joblib
from pathlib import Path
import logging

from .config import (
    RAW_DATA_PATH, 
    PROCESSED_DATA_PATH, 
    RANDOM_STATE, 
    TEST_SIZE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handle all data preprocessing steps"""
    
    def __init__(self):
        self.scaler = RobustScaler()  # More robust to outliers
        
    def load_data(self):
        """Load the credit card dataset"""
        logger.info(f"Loading data from {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH)
        logger.info(f"Loaded {len(df)} rows")
        return df
    
    def preprocess_features(self, df):
        """Preprocess features"""
        # Separate features and target
        X = df.drop('Class', axis=1)
        y = df['Class']
        
        # Scale only 'Amount' and 'Time' columns (others are already scaled)
        logger.info("Scaling features...")
        X_scaled = X.copy()
        X_scaled[['Amount', 'Time']] = self.scaler.fit_transform(X[['Amount', 'Time']])
        
        return X_scaled, y
    
    def handle_imbalance(self, X, y, method='undersample'):
        """Handle class imbalance"""
        logger.info(f"Handling imbalance using {method}")
        
        if method == 'undersample':
            sampler = RandomUnderSampler(random_state=RANDOM_STATE)
        elif method == 'smote':
            sampler = SMOTE(random_state=RANDOM_STATE)
        else:
            return X, y
            
        X_resampled, y_resampled = sampler.fit_resample(X, y)
        logger.info(f"Resampled dataset shape: {X_resampled.shape}")
        
        return X_resampled, y_resampled
    
    def split_data(self, X, y):
        """Split data into train and test sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=TEST_SIZE, 
            random_state=RANDOM_STATE,
            stratify=y
        )
        
        logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, X_train, X_test, y_train, y_test):
        """Save processed data"""
        PROCESSED_DATA_PATH.mkdir(exist_ok=True)
        
        # Save datasets
        pd.DataFrame(X_train).to_csv(PROCESSED_DATA_PATH / "X_train.csv", index=False)
        pd.DataFrame(X_test).to_csv(PROCESSED_DATA_PATH / "X_test.csv", index=False)
        pd.DataFrame(y_train).to_csv(PROCESSED_DATA_PATH / "y_train.csv", index=False)
        pd.DataFrame(y_test).to_csv(PROCESSED_DATA_PATH / "y_test.csv", index=False)
        
        # Save scaler
        joblib.dump(self.scaler, PROCESSED_DATA_PATH / "scaler.pkl")
        
        logger.info("Processed data saved successfully")
    
    def run_preprocessing_pipeline(self):
        """Run the complete preprocessing pipeline"""
        # Load data
        df = self.load_data()
        
        # Preprocess features
        X, y = self.preprocess_features(df)
        
        # Split data first (before handling imbalance)
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Handle imbalance only on training data
        X_train_balanced, y_train_balanced = self.handle_imbalance(
            X_train, y_train, method='undersample'
        )
        
        # Save processed data
        self.save_processed_data(
            X_train_balanced, X_test, y_train_balanced, y_test
        )
        
        return X_train_balanced, X_test, y_train_balanced, y_test

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.run_preprocessing_pipeline()
