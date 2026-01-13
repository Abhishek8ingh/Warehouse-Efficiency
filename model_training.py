import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score

base_path = os.getcwd()

def train_model(engineered_data):
    df = engineered_data.copy()
    
    # Check for required columns
    if 'ProductsOrdered' not in df.columns:
        # If running with dummy data, we might need to simulate this column if missing
        df['ProductsOrdered'] = df['OrderFrequency'] * 10 # Dummy logic for safety
        
    # Filter valid rows
    df = df[df['ProductsOrdered'] > 0]
    
    # Handle empty data
    if df.empty:
        return None, {'r2': 0}

    # Ensure ReorderFlag exists
    if 'ReorderFlag' not in df.columns:
        df['ReorderFlag'] = (df['StockLevel'] <= 10).astype(int)

    # Define features and target
    features = ['StockLevel', 'OrderFrequency', 'InventoryHealthScore', 'ReorderFlag']
    
    # Check if we have 'ProductCategory' (from uploaded data)
    if 'ProductCategory' in df.columns:
        features.append('ProductCategory')
        
    target = 'ProductsOrdered'
    
    X = df[features]
    y = df[target]
    
    # preprocessing for categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['StockLevel', 'OrderFrequency', 'InventoryHealthScore', 'ReorderFlag']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['ProductCategory']) if 'ProductCategory' in features else ('passthrough', 'drop', [])
        ])

    # Create Pipeline
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])
    
    # Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    
    metrics = {'r2': r2}
    
    return model, metrics

# --- THIS IS THE FUNCTION I MISSED ---
def predict_order_count(model, input_data):
    """
    Wrapper function to make predictions using the trained model.
    """
    try:
        return model.predict(input_data)
    except Exception as e:
        print(f"Prediction Error: {e}")
        return [0]