import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(page_title="Inventory Avaibility", layout="wide")

# Debug: Print current working directory and sys.path
st.write("Debug: Setting up the dashboard...")
st.write(f"Debug: Current working directory: {os.getcwd()}")
st.write(f"Debug: sys.path: {sys.path}")

# Set working directory and add project path to sys.path
project_dir = 'C:/Users/pc/Desktop/Warehouse Project/7th sem project 2.0/'
os.chdir(project_dir)
sys.path.append(project_dir)
st.write(f"Debug: Updated working directory to {os.getcwd()}")
st.write(f"Debug: Updated sys.path: {sys.path}")

# Try to import modules from the same directory
try:
    from data_cleaning import process_input_data
    from data_integration import integrate_data
    from feature_engineering import feature_engineering
    from model_training import train_model, predict_order_count
    st.write("Debug: Successfully imported all modules.")
except ModuleNotFoundError as e:
    st.error(f"Module import error: {e}")
    st.stop()

if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'engineered_data' not in st.session_state:
    st.session_state.engineered_data = None
if 'model' not in st.session_state:
    st.session_state.model = None

base_path = project_dir

# Auto-process data if pre-processed files exist
if not st.session_state.processed:
    st.write("Debug: Checking for pre-processed files...")
    cleaned_files_exist = all(
        os.path.exists(os.path.join(base_path, f))
        for f in ['cleaned_inventory_data.csv', 'cleaned_order_data.csv', 'cleaned_layout_data.csv']
    )
    st.write(f"Debug: Cleaned files exist: {cleaned_files_exist}")
    if cleaned_files_exist:
        try:
            st.write("Debug: Loading cleaned data...")
            inventory_data = pd.read_csv(os.path.join(base_path, 'cleaned_inventory_data.csv'))
            order_data = pd.read_csv(os.path.join(base_path, 'cleaned_order_data.csv'))
            layout_data = pd.read_csv(os.path.join(base_path, 'cleaned_layout_data.csv'))
            st.write("Debug: Running data integration...")
            integrated_data = integrate_data(inventory_data, order_data, layout_data)
            st.write("Debug: Running feature engineering...")
            engineered_data = feature_engineering(integrated_data)
            st.write("Debug: Training model...")
            model = train_model(engineered_data)
            st.session_state.processed = True
            st.session_state.engineered_data = engineered_data
            st.session_state.model = model
            st.success("Data processing completed automatically.")
        except Exception as e:
            st.error(f"Error processing pre-existing data: {e}")
            st.session_state.processed = False
    else:
        st.warning("Debug: Pre-processed files not found. Please run the pipeline first.")

st.title("InventorySync: Real-Time Inventory Analysis Dashboard")

if st.session_state.processed:
    st.write("Debug: Rendering main content...")
    engineered_data = st.session_state.engineered_data
    model = st.session_state.model

    st.header("Data Analysis")
    st.subheader("Processed Data Summary")
    exclude_unknown = st.checkbox("Exclude rows with 'Unknown' in Aisle or Shelf")
    display_data = engineered_data[(engineered_data['Aisle'] != 'Unknown') & (engineered_data['Shelf'] != 'Unknown')] if exclude_unknown else engineered_data
    st.write(f"Displaying {len(display_data)} rows:")
    st.write(display_data)

    st.subheader("Predict Products Ordered")
    stock_level_input = st.number_input("Stock Level", min_value=0, max_value=1000, value=50, step=1)
    order_freq_input = st.number_input("Order Frequency", min_value=0, max_value=50, value=2, step=1)
    if st.button("Predict"):
        input_data = pd.DataFrame({
            'StockLevel': [stock_level_input],
            'OrderFrequency': [order_freq_input],
            'InventoryHealthScore': [stock_level_input / (1 + order_freq_input)]
        })
        prediction = predict_order_count(model, input_data)
        st.write(f"Predicted Products Ordered: {prediction[0]:.2f}")
else:
    st.info("Data processed via pipeline. If not visible, run manually.")
    st.write("Debug: Processed state is False. Check if pipeline ran successfully.")
