# InventorySync 📦
### Smart Warehouse Efficiency Dashboard

## 📌 Project Overview
**InventorySync** is an interactive data analytics dashboard designed to optimize warehouse operations. It automates the process of cleaning, integrating, and analyzing inventory data to help businesses track stock levels, monitor order frequency, and predict future product demand.

The system uses **Machine Learning (Random Forest)** to forecast orders and provides a **Streamlit** interface for real-time decision-making.

## 🚀 Key Features
- **Data Integration:** Merges Inventory, Order, and Layout data into a single master dataset.
- **Automated Cleaning:** Handles missing values and standardizes data formats automatically.
- **Smart Analytics:** Calculates unique metrics like **Inventory Health Score** to identify efficient vs. stagnant stock.
- **Demand Forecasting:** Uses Machine Learning to predict the number of products likely to be ordered next month.
- **Reorder Alerts:** Automatically flags items with low stock and high demand.
- **Interactive Dashboard:** Visualizes stock trends, order frequency, and warehouse layout performance.

## 🛠️ Tech Stack
- **Language:** Python 🐍
- **Frontend:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (Random Forest Regressor)
- **Visualization:** Matplotlib

## 📂 Project Structure
```text
📦 InventorySync
 ┣ 📜 run_project.py          # Main application runner
 ┣ 📜 dashboard.py            # Streamlit dashboard interface
 ┣ 📜 data_cleaning.py        # Data cleaning module
 ┣ 📜 data_integration.py     # Merges different CSVs
 ┣ 📜 feature_engineering.py  # Creates Health Score & Reorder flags
 ┣ 📜 model_training.py       # Trains the ML model
 ┣ 📜 utils.py                # Helper functions for plotting
 ┣ 📜 requirements.txt        # List of dependencies
 ┗ 📜 README.md               # Project documentation

## Screenshot
![](https://github.com/Abhishek8ingh/Warehouse-Efficiency/blob/main/InventorySync%20%F0%9F%93%A6.png)
