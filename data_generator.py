"""
Data generation module for inventory and transactions.
Handles: Creating sample stock data, transaction history
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataGenerator:
    """Generates sample inventory and transaction data"""
    
    def __init__(self, seed=42):
        """Initialize data generator with random seed"""
        np.random.seed(seed)
        self.products = [
            'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable', 'HDMI Cable',
            'Webcam', 'Headphones', 'Printer', 'Scanner', 'Router', 'Switch',
            'Hard Drive', 'SSD', 'RAM Module', 'Graphics Card', 'Motherboard',
            'Power Supply', 'CPU', 'Cooling Fan'
        ]
        self.categories = ['Electronics', 'Peripherals', 'Cables', 'Storage', 'Components', 'Networking']
        self.suppliers = ['TechSupply Co.', 'Global Electronics', 'Hardware Plus', 'Component World', 'Digital Distributors']
        self.warehouses = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Warehouse D']
    
    def generate_stock_data(self):
        """Generate comprehensive stock inventory DataFrame"""
        stock_data = []
        for i, product in enumerate(self.products):
            stock_data.append({
                'SKU': f'SKU-{1000 + i}',
                'Product': product,
                'Category': np.random.choice(self.categories),
                'Quantity': np.random.randint(10, 500),
                'Reorder_Level': np.random.randint(20, 100),
                'Unit_Price': round(np.random.uniform(10, 1000), 2),
                'Supplier': np.random.choice(self.suppliers),
                'Warehouse': np.random.choice(self.warehouses),
                'Last_Restocked': (datetime.now() - timedelta(days=np.random.randint(1, 90))).strftime('%Y-%m-%d'),
                'Expiry_Date': (datetime.now() + timedelta(days=np.random.randint(180, 720))).strftime('%Y-%m-%d') if np.random.random() > 0.5 else 'N/A'
            })
        
        df = pd.DataFrame(stock_data)
        df['Total_Value'] = df['Quantity'] * df['Unit_Price']
        df['Stock_Status'] = df.apply(self._calculate_stock_status, axis=1)
        
        return df
    
    def generate_transactions(self, num_transactions=200):
        """Generate transaction history DataFrame"""
        transactions = []
        for _ in range(num_transactions):
            product = np.random.choice(self.products)
            transaction_type = np.random.choice(['In', 'Out'], p=[0.4, 0.6])
            transactions.append({
                'Date': (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d %H:%M'),
                'Product': product,
                'Type': transaction_type,
                'Quantity': np.random.randint(1, 50),
                'Reference': f'REF-{np.random.randint(10000, 99999)}'
            })
        
        df_transactions = pd.DataFrame(transactions)
        df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])
        df_transactions = df_transactions.sort_values('Date', ascending=False)
        
        return df_transactions
    
    @staticmethod
    def _calculate_stock_status(row):
        """Calculate stock status based on quantity and reorder level"""
        if row['Quantity'] < row['Reorder_Level'] * 0.5:
            return 'Critical'
        elif row['Quantity'] < row['Reorder_Level']:
            return 'Low'
        elif row['Quantity'] < row['Reorder_Level'] * 2:
            return 'Adequate'
        else:
            return 'Overstocked'
