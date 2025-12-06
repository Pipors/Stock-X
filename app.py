"""
Main Dashboard Application - Entry Point
Handles: Dash app initialization, layout assembly, and server startup

This is the main orchestrator that brings together all modules:
- config.py: Configuration and colors
- data_generator.py: Sample data creation
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

# Import configuration
from config import COLORS, APP_CONFIG

# Import data generation
from data_generator import DataGenerator

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
        # Generate data
        self.data_gen = DataGenerator()
        self.df = self.data_gen.generate_stock_data()
        self.df_transactions = self.data_gen.generate_transactions()
        
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
        print("=" * 70)
        print("\n✨ Features Available:")
        print("  • Stock Dashboard - Comprehensive inventory overview")
        print("  • KPI Metrics - 11 clickable KPI cards with detailed calculations")
        print("  • Advanced Analytics - ABC analysis, supplier performance, aging")
        print("  • Inventory Details - Filterable, sortable data table")
        print("\n💡 Click any KPI card to see detailed calculation breakdown!")
        print("=" * 70)
        
        self.app.run(
            debug=APP_CONFIG['debug'], 
            port=APP_CONFIG['port']
        )


if __name__ == '__main__':
    dashboard = StockDashboardApp()
    dashboard.run()
