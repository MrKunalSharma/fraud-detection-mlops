import os
import urllib.request
from src.config import RAW_DATA_PATH

def download_credit_card_data():
    """Download the credit card fraud dataset from Kaggle"""
    
    # We'll use a direct link to the dataset
    url = "https://raw.githubusercontent.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection/master/creditcard.csv"
    
    print("Downloading credit card fraud dataset...")
    print("This may take a few minutes...")
    
    try:
        urllib.request.urlretrieve(url, RAW_DATA_PATH)
        print(f"Dataset downloaded successfully to {RAW_DATA_PATH}")
        
        # Check file size
        file_size = os.path.getsize(RAW_DATA_PATH) / (1024 * 1024)  # Convert to MB
        print(f"File size: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("\nAlternative: Download manually from:")
        print("https://www.kaggle.com/mlg-ulb/creditcardfraud")
        print(f"And place it in: {RAW_DATA_PATH}")

if __name__ == "__main__":
    download_credit_card_data()
