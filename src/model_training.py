import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)
import joblib
import json
from datetime import datetime
import logging
from pathlib import Path

from .config import (
    PROCESSED_DATA_PATH, 
    MODEL_DIR,
    MODEL_PATH,
    RANDOM_STATE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Train and evaluate fraud detection models"""
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                random_state=RANDOM_STATE,
                n_jobs=-1
            ),
            'logistic_regression': LogisticRegression(
                random_state=RANDOM_STATE,
                max_iter=1000
            ),
            'decision_tree': DecisionTreeClassifier(
                random_state=RANDOM_STATE,
                max_depth=5
            )
        }
        self.best_model = None
        self.best_model_name = None
        self.metrics = {}
        
    def load_processed_data(self):
        """Load the preprocessed data"""
        logger.info("Loading processed data...")
        
        X_train = pd.read_csv(PROCESSED_DATA_PATH / "X_train.csv")
        X_test = pd.read_csv(PROCESSED_DATA_PATH / "X_test.csv")
        y_train = pd.read_csv(PROCESSED_DATA_PATH / "y_train.csv").values.ravel()
        y_test = pd.read_csv(PROCESSED_DATA_PATH / "y_test.csv").values.ravel()
        
        logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def train_model(self, model, X_train, y_train, model_name):
        """Train a single model"""
        logger.info(f"Training {model_name}...")
        model.fit(X_train, y_train)
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate a single model"""
        logger.info(f"Evaluating {model_name}...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        # Log metrics
        logger.info(f"{model_name} - Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"{model_name} - Precision: {metrics['precision']:.4f}")
        logger.info(f"{model_name} - Recall: {metrics['recall']:.4f}")
        logger.info(f"{model_name} - F1-Score: {metrics['f1_score']:.4f}")
        logger.info(f"{model_name} - ROC-AUC: {metrics['roc_auc']:.4f}")
        
        return metrics
    
    def train_all_models(self):
        """Train and evaluate all models"""
        # Load data
        X_train, X_test, y_train, y_test = self.load_processed_data()
        
        best_f1 = 0
        
        for model_name, model in self.models.items():
            # Train
            trained_model = self.train_model(model, X_train, y_train, model_name)
            
            # Evaluate
            metrics = self.evaluate_model(trained_model, X_test, y_test, model_name)
            self.metrics[model_name] = metrics
            
            # Track best model (using F1-score)
            if metrics['f1_score'] > best_f1:
                best_f1 = metrics['f1_score']
                self.best_model = trained_model
                self.best_model_name = model_name
        
        logger.info(f"\nBest model: {self.best_model_name} with F1-score: {best_f1:.4f}")
        
    def save_model(self):
        """Save the best model and metrics"""
        if self.best_model is None:
            logger.error("No model to save!")
            return
            
        # Save model
        joblib.dump(self.best_model, MODEL_PATH)
        logger.info(f"Model saved to {MODEL_PATH}")
        
        # Save metrics
        metrics_data = {
            'model_name': self.best_model_name,
            'metrics': self.metrics,
            'training_date': datetime.now().isoformat(),
            'model_path': str(MODEL_PATH)
        }
        
        metrics_path = MODEL_DIR / "model_metrics.json"
        with open(metrics_path, 'w') as f:
            json.dump(metrics_data, f, indent=4)
        
        logger.info(f"Metrics saved to {metrics_path}")
        
    def run_training_pipeline(self):
        """Run the complete training pipeline"""
        logger.info("Starting model training pipeline...")
        
        # Train all models
        self.train_all_models()
        
        # Save the best model
        self.save_model()
        
        logger.info("Training pipeline completed!")
        
        return self.best_model, self.metrics

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run_training_pipeline()
