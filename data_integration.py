import pandas as pd
import os

base_path = os.getcwd()

def integrate_data(inventory_data, order_data, layout_data):
    # Merge Inventory and Order data
    merged = pd.merge(inventory_data, order_data, on='ProductID', how='inner')
    
    # Merge with Layout data
    final_df = pd.merge(merged, layout_data, on='ProductID', how='left')
    
    # Fill missing values to prevent crashes
    final_df['StockLevel'] = final_df['StockLevel'].fillna(0)
    final_df['Aisle'] = final_df['Aisle'].fillna('Unknown')
    final_df['Shelf'] = final_df['Shelf'].fillna('Unknown')
    
    return final_df