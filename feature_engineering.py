import pandas as pd
import os

base_path = os.getcwd()

def feature_engineering(integrated_data):
    df = integrated_data.copy()
    
    # Create Inventory Health Score
    # (Avoid division by zero by adding 1)
    df['InventoryHealthScore'] = df['StockLevel'] / (1 + df['OrderFrequency'])
    
    # Create Reorder Flag (1 if stock is low, 0 otherwise)
    df['ReorderFlag'] = (df['StockLevel'] <= 10).astype(int)
    
    return df