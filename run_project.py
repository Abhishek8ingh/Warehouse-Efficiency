import streamlit as st
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# --- FIX: Set up Relative Paths (Works on any computer) ---
# Get the folder where this script is running
project_dir = os.getcwd()
os.chdir(project_dir)  # Set it as the current working directory
sys.path.append(project_dir)  # Allow importing other files from here

# Import your modules
try:
    from data_cleaning import process_input_data
    from data_integration import integrate_data
    from feature_engineering import feature_engineering
    from model_training import train_model,predict_order_count
except ModuleNotFoundError as e:
    st.error(f"Error: Could not load modules. Make sure all .py files are in the same folder.\nDetails: {e}")
    st.stop()

# Streamlit Page Config
st.set_page_config(page_title="Inventory Availability", layout="wide")
st.title("📦 Inventory Availability & Demand Prediction")

# Session State (Keeps data alive while you click buttons)
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'engineered_data' not in st.session_state:
    st.session_state.engineered_data = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'metrics' not in st.session_state:
    st.session_state.metrics = None

# --- SIDEBAR: Upload Files ---
with st.sidebar:
    st.header("📂 Upload Data")
    inv_file = st.file_uploader("Inventory Data (CSV)", type=['csv'])
    ord_file = st.file_uploader("Order Data (CSV)", type=['csv'])
    lay_file = st.file_uploader("Layout Data (CSV)", type=['csv'])
    
    run_btn = st.button("🚀 Run Analysis Pipeline")

# --- MAIN LOGIC ---
if run_btn:
    with st.spinner("Running Data Pipeline..."):
        try:
            # 1. Cleaning (Pass None if no file uploaded -> generates synthetic data)
            inv_path = inv_file if inv_file else None
            ord_path = ord_file if ord_file else None
            lay_path = lay_file if lay_file else None
            
            inventory_df, order_df, layout_df = process_input_data(inv_path, ord_path, lay_path)
            
            # 2. Integration
            integrated_df = integrate_data(inventory_df, order_df, layout_df)
            
            # 3. Feature Engineering
            engineered_df = feature_engineering(integrated_df)
            
            # 4. Model Training
            model, metrics = train_model(engineered_df)
            
            # Save to Session State
            st.session_state.engineered_data = engineered_df
            st.session_state.model = model
            st.session_state.metrics = metrics
            st.session_state.processed = True
            
            st.success("Pipeline executed successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- DASHBOARD VIEW ---
if st.session_state.processed:
    df = st.session_state.engineered_data
    
    # Metrics Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Products", len(df))
    c2.metric("Avg Inventory Health", f"{df['InventoryHealthScore'].mean():.2f}")
    c3.metric("Model Accuracy (R²)", f"{st.session_state.metrics.get('r2', 0):.2f}")
    
    st.divider()
    
    # Charts
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("📉 Stock Levels by Product")
        st.bar_chart(df.set_index('ProductID')['StockLevel'].head(20))
        
    with c_right:
        st.subheader("📦 Order Frequency")
        st.line_chart(df.set_index('ProductID')['OrderFrequency'].head(20))
        
    st.divider()
    st.subheader("🔮 Demand Prediction Tool")
    
    # Prediction Form
    with st.form("pred_form"):
        col_a, col_b = st.columns(2)
        stock_in = col_a.number_input("Current Stock Level", 50)
        freq_in = col_b.number_input("Order Frequency (Past Month)", 5)
        
        predict_btn = st.form_submit_button("Predict Future Orders")
        
        if predict_btn:
            # Create a dataframe for the model input
            input_row = pd.DataFrame([{
                'StockLevel': stock_in,
                'OrderFrequency': freq_in,
                'InventoryHealthScore': stock_in / (1 + freq_in),
                'ReorderFlag': 1 if stock_in <= 10 else 0
            }])
            
            # Predict
            pred_val = st.session_state.model.predict(input_row)[0]
            st.success(f"Predicted Order Quantity: {int(pred_val)} units")