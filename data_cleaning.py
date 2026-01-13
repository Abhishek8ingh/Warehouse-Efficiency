import pandas as pd
import numpy as np
import os

# Set base path to current folder
base_path = os.getcwd()

def process_input_data(inventory_file=None, order_file=None, layout_file=None):
    """
    Loads data. If no file is provided, generates synthetic (fake) data for testing.
    """
    # 1. Inventory Data
    if inventory_file:
        inventory_data = pd.read_csv(inventory_file)
    else:
        # Generate Synthetic Data
        inventory_data = pd.DataFrame({
            'ProductID': [f'P{i}' for i in range(1001, 1051)],
            'StockLevel': np.random.randint(5, 1000, 50),
            'OrderFrequency': np.random.randint(1, 50, 50)
        })

    # 2. Order Data
    if order_file:
        order_data = pd.read_csv(order_file)
    else:
        order_data = pd.DataFrame({
            'OrderID': [f'O{i}' for i in range(5000, 5050)],
            'ProductID': [f'P{i}' for i in range(1001, 1051)],
            'ProductsOrdered': np.random.randint(10, 100, 50)
        })

    # 3. Layout Data
    if layout_file:
        layout_data = pd.read_csv(layout_file)
    else:
        layout_data = pd.DataFrame({
            'ProductID': [f'P{i}' for i in range(1001, 1051)],
            'Aisle': [f'A{np.random.randint(1, 10)}' for _ in range(50)],
            'Shelf': [f'S{np.random.randint(1, 5)}' for _ in range(50)]
        })

    return inventory_data, order_data, layout_data