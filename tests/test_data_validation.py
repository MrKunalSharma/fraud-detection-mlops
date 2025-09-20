import pytest
from src.utils import validate_transaction_data

class TestDataValidation:
    
    def test_valid_transaction(self):
        """Test valid transaction passes validation"""
        valid_data = {
            'Time': 0,
            **{f'V{i}': 0.0 for i in range(1, 29)},
            'Amount': 100.0
        }
        assert validate_transaction_data(valid_data) == True
    
    def test_negative_amount_rejected(self):
        """Test negative amounts are rejected"""
        invalid_data = {
            'Time': 0,
            **{f'V{i}': 0.0 for i in range(1, 29)},
            'Amount': -100.0
        }
        assert validate_transaction_data(invalid_data) == False
