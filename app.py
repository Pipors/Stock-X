"""
Main Dashboard Application - Entry Point
Handles: Dash app initialization, layout assembly, and server startup

This is the main orchestrator that brings together all modules:
- config.py: Configuration and colors
- database.py: PostgreSQL database connection
- charts.py: Chart visualizations
- ui_components.py: Reusable UI elements
- kpi_modals.py: KPI detail modals
- tab_renderers.py: Tab content rendering
- callbacks.py: Interactive callbacks
- kpi_calculator.py: KPI calculations (existing file)
"""

import dash
from dash import dcc, html
from datetime import datetime
import os
import pandas as pd

# Import configuration
from config import COLORS, APP_CONFIG

# Import database connection
from database import DatabaseConnection, StockDataAccess

# Import KPI calculator
from kpi_calculator import InventoryKPICalculator

# Import chart builder
from charts import ChartBuilder

# Import UI components
from ui_components import UIComponents

# Import KPI modal generator
from kpi_modals import KPIDetailsModal

# Import tab renderers
from tab_renderers import TabRenderer

# Import callbacks
from callbacks import DashboardCallbacks


class StockDashboardApp:
    """Main Stock Management Dashboard Application"""
    
    def __init__(self):
        """Initialize the dashboard application"""
        # Database configuration for Docker container
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),  # Docker container host
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'stock_management'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
        
        print("=" * 70)
        print("🔌 Connecting to PostgreSQL database...")
        print(f"   Host: {db_config['host']}")
        print(f"   Port: {db_config['port']}")
        print(f"   Database: {db_config['database']}")
        print(f"   Container: postgres-stock")
        
        try:
            # Initialize database connection
            self.db_connection = DatabaseConnection(db_config)
            self.stock_data_access = StockDataAccess(self.db_connection)
            
            # Fetch data from database
            print("📊 Fetching inventory data from database...")
            self.df = self.stock_data_access.get_current_stock_summary()
            self.df_transactions = self.stock_data_access.get_transaction_history(days=30)
            
            # Convert numeric columns to proper types
            numeric_cols = ['Quantity', 'Reserved', 'Available', 'Reorder_Level', 
                          'Unit_Price', 'Selling_Price', 'Total_Value']
            for col in numeric_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
            
            # Convert transaction numeric columns
            trans_numeric_cols = ['Quantity', 'Unit_Cost', 'Total_Value']
            for col in trans_numeric_cols:
                if col in self.df_transactions.columns:
                    self.df_transactions[col] = pd.to_numeric(self.df_transactions[col], errors='coerce').fillna(0)
            
            print(f"✅ Successfully loaded {len(self.df)} products")
            print(f"✅ Successfully loaded {len(self.df_transactions)} transactions")
            print("=" * 70)
            
        except Exception as e:
            print("❌ Database connection failed!")
            print(f"   Error: {str(e)}")
            print("\n💡 Troubleshooting:")
            print("   1. Ensure Docker container 'postgres-stock' is running:")
            print("      docker ps | grep postgres-stock")
            print("   2. Check container port mapping:")
            print("      docker port postgres-stock")
            print("   3. Verify database exists:")
            print("      docker exec -it postgres-stock psql -U postgres -l")
            print("   4. Check credentials match your container setup")
            print("=" * 70)
            raise
        
        # Calculate KPIs
        kpi_calc = InventoryKPICalculator(self.df, self.df_transactions)
        self.all_kpis = kpi_calc.get_all_kpis()
        
        # Initialize components
        self.ui_components = UIComponents(COLORS)
        self.chart_builder = ChartBuilder(self.df, COLORS)
        self.kpi_modal_gen = KPIDetailsModal(self.df, self.all_kpis, COLORS)
        self.tab_renderer = TabRenderer(
            self.df, 
            self.df_transactions, 
            self.all_kpis, 
            self.ui_components, 
            self.chart_builder
        )
        
        # Initialize Dash app
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.title = APP_CONFIG['title']
        
        # Build layout
        self._build_layout()
        
        # Register callbacks
        self.callbacks = DashboardCallbacks(self.app, self.tab_renderer, self.kpi_modal_gen)
    
    def _build_layout(self):
        """Build the main dashboard layout"""
        self.app.layout = html.Div(
            style={
                'backgroundColor': COLORS['background'], 
                'fontFamily': 'Arial, sans-serif', 
                'minHeight': '100vh', 
                'color': COLORS['text']
            }, 
            children=[
                # Header
                self.ui_components.create_header(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                
                # Main Navigation Tabs
                html.Div([
                    dcc.Tabs(id='main-tabs', value='stock-overview', children=[
                        dcc.Tab(
                            label='📊 Stock Dashboard', 
                            value='stock-overview', 
                            style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['card_bg'], 
                                'color': COLORS['text'], 
                                'border': f'1px solid {COLORS["border"]}'
                            },
                            selected_style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['primary'], 
                                'color': '#ffffff', 
                                'border': f'1px solid {COLORS["primary"]}'
                            }
                        ),
                        dcc.Tab(
                            label='🎯 KPI Metrics', 
                            value='kpis', 
                            style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['card_bg'], 
                                'color': COLORS['text'], 
                                'border': f'1px solid {COLORS["border"]}'
                            },
                            selected_style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['primary'], 
                                'color': '#ffffff', 
                                'border': f'1px solid {COLORS["primary"]}'
                            }
                        ),
                        dcc.Tab(
                            label='📊 Advanced Analytics', 
                            value='analytics', 
                            style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['card_bg'], 
                                'color': COLORS['text'], 
                                'border': f'1px solid {COLORS["border"]}'
                            },
                            selected_style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['primary'], 
                                'color': '#ffffff', 
                                'border': f'1px solid {COLORS["primary"]}'
                            }
                        ),
                        dcc.Tab(
                            label='📋 Inventory Details', 
                            value='details', 
                            style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['card_bg'], 
                                'color': COLORS['text'], 
                                'border': f'1px solid {COLORS["border"]}'
                            },
                            selected_style={
                                'fontWeight': 'bold', 
                                'backgroundColor': COLORS['primary'], 
                                'color': '#ffffff', 
                                'border': f'1px solid {COLORS["primary"]}'
                            }
                        ),
                    ], style={'fontFamily': 'Arial'})
                ], style={
                    'margin': '20px', 
                    'backgroundColor': COLORS['card_bg'], 
                    'borderRadius': '8px', 
                    'border': f'1px solid {COLORS["border"]}'
                }),
                
                # Content Container
                html.Div(id='tab-content'),
                
                # Modal for KPI details
                html.Div(id='kpi-modal', style={'display': 'none'}, children=[
                    html.Button('', id='close-modal', style={'display': 'none'})
                ]),
                
                # Store to track which KPI was clicked
                dcc.Store(id='clicked-kpi-store', data=None)
            ]
        )
    
    def run(self):
        """Run the dashboard server"""
        print("=" * 70)
        print("🚀 Starting Unified Stock Management Dashboard...")
        print("=" * 70)
        print(f"📊 Dashboard URL: http://127.0.0.1:{APP_CONFIG['port']}")
        print(f"🗄️  Database: PostgreSQL (Container: postgres-stock)")
        print(f"📦 Products loaded: {len(self.df)}")
        print(f"📝 Transactions loaded: {len(self.df_transactions)}")
        print("=" * 70)
        print("\n✨ Features Available:")
        print("  • Stock Dashboard - Real-time inventory from database")
        print("  • KPI Metrics - 11 clickable KPI cards with detailed calculations")
        print("  • Advanced Analytics - ABC analysis, supplier performance, aging")
        print("  • Inventory Details - Filterable, sortable data table")
        print("\n💡 Click any KPI card to see detailed calculation breakdown!")
        print("💾 All data is fetched from PostgreSQL database in real-time!")
        print("=" * 70)
        
        self.app.run(
            debug=APP_CONFIG['debug'], 
            port=APP_CONFIG['port']
        )


if __name__ == '__main__':
    dashboard = StockDashboardApp()
    dashboard.run()
