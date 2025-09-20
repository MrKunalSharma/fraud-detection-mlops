import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data paths
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "creditcard.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed"

# Model paths
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "fraud_detection_model.pkl"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "raw").mkdir(exist_ok=True)
(DATA_DIR / "processed").mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
