import joblib
import pandas as pd
from src.config import MODEL_PATH, PROCESSED_DATA_PATH

# Load model and check expected features
model = joblib.load(MODEL_PATH)
scaler = joblib.load(PROCESSED_DATA_PATH / "scaler.pkl")

# Load training data to see column order
X_train = pd.read_csv(PROCESSED_DATA_PATH / "X_train.csv")
print("Expected columns from training data:")
print(X_train.columns.tolist())
print(f"\nNumber of features: {len(X_train.columns)}")

# Check if model has feature names
if hasattr(model, 'feature_names_in_'):
    print("\nModel's expected features:")
    print(model.feature_names_in_)
