"""
API Data Handler - Pure data operations without UI
Handles: Database queries, data processing, KPI calculations
"""

import pandas as pd
from datetime import datetime
from src.database.connection import DatabaseConnection, StockDataAccess
from src.kpi.calculator import InventoryKPICalculator
import os


class DashboardDataAPI:
    """API for dashboard data operations - no UI logic"""
    
    def __init__(self, db_config=None):
        """Initialize data API with database connection"""
        if db_config is None:
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 5432)),
                'database': os.getenv('DB_NAME', 'stock_management'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'postgres')
            }
        
        self.db_connection = DatabaseConnection(db_config)
        self.stock_data_access = StockDataAccess(self.db_connection)
        self._cache = {}
        self._last_refresh = None
    
    def get_stock_summary(self):
        """Get current stock summary data"""
        df = self.stock_data_access.get_current_stock_summary()
        
        # Convert numeric columns
        numeric_cols = ['Quantity', 'Reserved', 'Available', 'Reorder_Level', 
                       'Unit_Price', 'Selling_Price', 'Total_Value']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def get_transactions(self, days=None):
        """Get transaction history"""
        df = self.stock_data_access.get_transaction_history(days=days)
        
        # Convert numeric columns
        trans_numeric_cols = ['Quantity', 'Unit_Cost', 'Total_Value']
        for col in trans_numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Convert Date column
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    
    def get_low_stock_items(self):
        """Get items below reorder point"""
        return self.stock_data_access.get_low_stock_items()
    
    def get_stock_by_warehouse(self):
        """Get stock grouped by warehouse"""
        return self.stock_data_access.get_stock_by_warehouse()
    
    def get_stock_by_category(self):
        """Get stock grouped by category"""
        return self.stock_data_access.get_stock_by_category()
    
    def calculate_kpis(self, stock_df, transactions_df):
        """Calculate all KPIs"""
        kpi_calc = InventoryKPICalculator(stock_df, transactions_df)
        return kpi_calc.get_all_kpis()
    
    def get_dashboard_data(self, refresh=False):
        """Get all dashboard data in one call"""
        if not refresh and self._cache.get('data') and self._last_refresh:
            # Return cached data if available and not expired (< 60 seconds)
            elapsed = (datetime.now() - self._last_refresh).total_seconds()
            if elapsed < 60:
                print(f"📦 Returning cached data (age: {elapsed:.1f}s)")
                return self._cache['data']
        
        print("🔄 Fetching fresh data from database...")
        
        # Fetch fresh data
        stock_df = self.get_stock_summary()
        transactions_df = self.get_transactions()
        
        print(f"✅ Loaded {len(stock_df)} products and {len(transactions_df)} transactions")
        
        kpis = self.calculate_kpis(stock_df, transactions_df)
        
        # Convert DataFrames to dict with proper date handling
        def convert_df(df):
            # Convert dates to strings
            for col in df.columns:
                if df[col].dtype == 'datetime64[ns]':
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            return df.to_dict('records')
        
        data = {
            'stock': convert_df(stock_df.copy()),
            'transactions': convert_df(transactions_df.copy()),
            'kpis': kpis,
            'summary': {
                'total_products': len(stock_df),
                'total_transactions': len(transactions_df),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        # Cache the data
        self._cache['data'] = data
        self._last_refresh = datetime.now()
        
        print(f"💾 Data cached at {self._last_refresh.strftime('%H:%M:%S')}")
        
        return data
    
    def get_kpi_details(self, kpi_id):
        """Get detailed information for a specific KPI"""
        data = self.get_dashboard_data()
        kpis = data['kpis']
        
        if kpi_id in kpis:
            return kpis[kpi_id]
        return None
    
    def export_to_json(self, filename='dashboard_data.json'):
        """Export dashboard data to JSON file"""
        import json
        data = self.get_dashboard_data()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filename
    
    def export_to_csv(self, directory='exports'):
        """Export data to CSV files"""
        import os
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        stock_df = self.get_stock_summary()
        transactions_df = self.get_transactions()
        
        stock_file = os.path.join(directory, 'stock_summary.csv')
        trans_file = os.path.join(directory, 'transactions.csv')
        
        stock_df.to_csv(stock_file, index=False)
        transactions_df.to_csv(trans_file, index=False)
        
        return {
            'stock': stock_file,
            'transactions': trans_file
        }
    
    def health_check(self):
        """Check if database connection is healthy"""
        try:
            df = self.stock_data_access.get_current_stock_summary()
            return {
                'status': 'healthy',
                'records': len(df),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


# Standalone API functions for external use
def get_api_instance():
    """Get a singleton instance of the data API"""
    if not hasattr(get_api_instance, 'instance'):
        get_api_instance.instance = DashboardDataAPI()
    return get_api_instance.instance


# Quick access functions
def fetch_stock_data():
    """Quick function to fetch stock data"""
    api = get_api_instance()
    return api.get_stock_summary()


def fetch_transactions():
    """Quick function to fetch transactions"""
    api = get_api_instance()
    return api.get_transactions()


def fetch_kpis():
    """Quick function to fetch all KPIs"""
    api = get_api_instance()
    stock = api.get_stock_summary()
    transactions = api.get_transactions()
    return api.calculate_kpis(stock, transactions)


if __name__ == '__main__':
    # Test the API
    print("Testing Dashboard Data API...")
    api = DashboardDataAPI()
    
    print("\n1. Health Check:")
    print(api.health_check())
    
    print("\n2. Fetching Dashboard Data:")
    data = api.get_dashboard_data()
    print(f"   Products: {data['summary']['total_products']}")
    print(f"   Transactions: {data['summary']['total_transactions']}")
    print(f"   Last Updated: {data['summary']['last_updated']}")
    
    print("\n3. KPIs Available:")
    for kpi_id in data['kpis'].keys():
        kpi = data['kpis'][kpi_id]
        print(f"   - {kpi_id}: {kpi.get('value', 'N/A')}")
    
    print("\n✅ API test complete!")
