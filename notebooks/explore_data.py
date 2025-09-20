import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from src.config import RAW_DATA_PATH

# Load the data
print("Loading credit card dataset...")
df = pd.read_csv(RAW_DATA_PATH)

print(f"\nDataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df.head())

# Check for missing values
print(f"\nMissing values: {df.isnull().sum().sum()}")

# Check class distribution
fraud_count = df['Class'].value_counts()
print(f"\nClass distribution:")
print(f"Normal transactions: {fraud_count[0]} ({fraud_count[0]/len(df)*100:.2f}%)")
print(f"Fraudulent transactions: {fraud_count[1]} ({fraud_count[1]/len(df)*100:.2f}%)")

# Basic statistics
print(f"\nBasic statistics for Amount:")
print(df['Amount'].describe())
