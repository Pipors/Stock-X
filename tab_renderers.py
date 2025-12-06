"""
Tab Renderers module for dashboard content.
Handles: Rendering different dashboard tabs (Stock Overview, KPIs, Analytics, Details)
"""

from dash import html, dcc, dash_table
from datetime import datetime, timedelta


class TabRenderer:
    """Renders content for different dashboard tabs"""
    
    def __init__(self, df, df_transactions, all_kpis, ui_components, chart_builder):
        """Initialize tab renderer with data and components"""
        self.df = df
        self.df_transactions = df_transactions
        self.all_kpis = all_kpis
        self.ui = ui_components
        self.charts = chart_builder

    def render_stock_overview_tab(self):
        """Render Stock Overview Tab - Original stock dashboard view"""
        return html.Div([
            # Quick Stats Cards
            self.ui.create_section_container([
                self.ui.create_section_header('📦', 'Quick Stats'),
                html.Div([
                    self.ui.create_kpi_card('Total Products', f'{len(self.df)}', f'{self.df["Quantity"].sum():,} Units', '📦', self.ui.colors['primary']),
                    self.ui.create_kpi_card('Total Value', f'${self.df["Total_Value"].sum():,.0f}', f'Avg: ${self.df["Total_Value"].mean():,.0f}', '💰', self.ui.colors['success']),
                    self.ui.create_kpi_card('Low Stock Items', f'{len(self.df[self.df["Stock_Status"].isin(["Low", "Critical"])])}', 
                                          f'{len(self.df[self.df["Stock_Status"] == "Critical"])} Critical', '⚠️', self.ui.colors['warning']),
                    self.ui.create_kpi_card('Transactions (30d)', 
                                          f'{len(self.df_transactions[self.df_transactions["Date"] >= datetime.now() - timedelta(days=30)])}', 
                                          f'In: {len(self.df_transactions[(self.df_transactions["Date"] >= datetime.now() - timedelta(days=30)) & (self.df_transactions["Type"] == "In")])}', 
                                          '📈', self.ui.colors['info']),
                    self.ui.create_kpi_card('Warehouses', f'{self.df["Warehouse"].nunique()}', f'{self.df["Supplier"].nunique()} Suppliers', '🏢', self.ui.colors['primary']),
                ], style={'padding': '10px 20px'}),
            ]),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    dcc.Graph(figure=self.charts.create_stock_by_category_chart(), config={'displayModeBar': False})
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                
                html.Div([
                    dcc.Graph(figure=self.charts.create_stock_status_pie(), config={'displayModeBar': False})
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
            ]),
            
            # Charts Row 2
            html.Div([
                html.Div([
                    dcc.Graph(figure=self.charts.create_value_by_warehouse_chart(), config={'displayModeBar': False})
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                
                html.Div([
                    dcc.Graph(figure=self.charts.create_top_products_chart(), config={'displayModeBar': False})
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
            ]),
        ])
    
    def render_kpi_tab(self):
        """Render KPI Metrics Tab"""
        inventory_turnover = self.all_kpis['inventory_turnover']
        dsi = self.all_kpis['days_sales_inventory']  #Day Sales Inventory = dsi
        stock_accuracy = self.all_kpis['stock_accuracy']
        stockout = self.all_kpis['stockout_rate']
        fulfillment = self.all_kpis['order_fulfillment']
        carrying = self.all_kpis['carrying_cost']
        dead_stock = self.all_kpis['dead_stock_percentage']
        backorder = self.all_kpis['backorder_rate']
        fill_rate = self.all_kpis['fill_rate']
        shrinkage = self.all_kpis['inventory_shrinkage']
        lead_time = self.all_kpis['lead_time']
        
        return html.Div([
            # Financial KPIs
            self.ui.create_section_container([
                self.ui.create_section_header('💰', 'Financial KPIs'),
                html.Div([
                    self.ui.create_kpi_card('Inventory Turnover', f'{inventory_turnover["annual_turnover"]}x', 
                                          inventory_turnover['interpretation'], '🔄', self.ui.colors['primary'], 
                                          'Good' if inventory_turnover["annual_turnover"] > 6 else 'Average', "inventory_turnover"),
                    self.ui.create_kpi_card('Days Sales Inventory', f'{dsi["days_sales_inventory"]} days', 
                                          dsi['interpretation'], '📅', self.ui.colors['info'], dsi['status'], "dsi"),
                    self.ui.create_kpi_card('Carrying Cost', f'${carrying["annual_carrying_cost"]:,.0f}', 
                                          f'{carrying["carrying_cost_rate"]}% of inventory', '💸', self.ui.colors['warning'], carrying['status'], "carrying"),
                    self.ui.create_kpi_card('Dead Stock', f'{dead_stock["dead_stock_percentage"]}%', 
                                          f'${dead_stock["dead_stock_value"]:,.0f} value', '☠️', self.ui.colors['danger'], dead_stock['status'], "dead_stock"),
                    self.ui.create_kpi_card('Shrinkage', f'{shrinkage["shrinkage_rate"]}%', 
                                          f'${shrinkage["shrinkage_value"]:,.0f} loss', '📉', self.ui.colors['danger'], shrinkage['status'], "shrinkage"),
                ], style={'padding': '10px 20px'}),
            ]),
            
            # Operational KPIs
            self.ui.create_section_container([
                self.ui.create_section_header('⚙️', 'Operational KPIs'),
                html.Div([
                    self.ui.create_kpi_card('Stock Accuracy', f'{stock_accuracy["accuracy_rate"]}%', 
                                          f'{stock_accuracy["accurate_items"]}/{stock_accuracy["total_items"]} items', '🎯', self.ui.colors['success'], stock_accuracy['status'], 'stock_accuracy'),
                    self.ui.create_kpi_card('Stockout Rate', f'{stockout["stockout_rate"]}%', 
                                          f'{stockout["stockout_items"]} items affected', '⚠️', self.ui.colors['warning'], stockout['status'], 'stockout'),
                    self.ui.create_kpi_card('Order Fulfillment', f'{fulfillment["fulfillment_rate"]}%', 
                                          f'{fulfillment["fulfilled_orders"]}/{fulfillment["total_orders"]} orders', '✅', self.ui.colors['success'], fulfillment['status'], 'fulfillment'),
                    self.ui.create_kpi_card('Backorder Rate', f'{backorder["backorder_rate"]}%', 
                                          f'{backorder["backorders"]} backorders', '📦', self.ui.colors['warning'], backorder['status'], 'backorder'),
                    self.ui.create_kpi_card('Fill Rate', f'{fill_rate["fill_rate"]}%', 
                                          f'{fill_rate["items_in_stock"]}/{fill_rate["total_items"]} in stock', '📊', self.ui.colors['success'], fill_rate['status'], 'fill_rate'),
                ], style={'padding': '10px 20px'}),
            ]),
            
            # Supply Chain KPIs
            self.ui.create_section_container([
                self.ui.create_section_header('🚚', 'Supply Chain KPIs'),
                html.Div([
                    self.ui.create_kpi_card('Avg Lead Time', f'{lead_time["average_lead_time_days"]} days', 
                                          f'Min: {lead_time["min_lead_time"]} | Max: {lead_time["max_lead_time"]}', '⏱️', self.ui.colors['info'], lead_time['status'], 'lead_time'),
                    html.Div([
                        html.Div([
                            html.H4('Lead Time by Supplier', style={'color': self.ui.colors['text'], 'marginBottom': '15px'}),
                            html.Div([
                                html.Div([
                                    html.Span(f'{supplier}: ', style={'fontWeight': 'bold', 'color': self.ui.colors['text']}),
                                    html.Span(f'{days} days', style={'color': self.ui.colors['primary'], 'fontSize': '18px', 'marginLeft': '10px'})
                                ], style={'padding': '8px', 'borderBottom': '1px solid #ecf0f1'})
                                for supplier, days in lead_time['by_supplier'].items()
                            ])
                        ], style={'backgroundColor': self.ui.colors['card_bg'], 'padding': '20px', 'borderRadius': '8px', 
                                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)', 'height': '100%'})
                    ], style={'width': '78%', 'display': 'inline-block', 'margin': '0.5%', 'verticalAlign': 'top'}),
                ], style={'padding': '10px 20px'}),
            ]),
            
            # Carrying Cost Breakdown
            self.ui.create_section_container([
                self.ui.create_section_header('💸', 'Carrying Cost Breakdown'),
                dcc.Graph(figure=self.charts.create_carrying_cost_chart(carrying), config={'displayModeBar': False})
            ]),
        ])
    
    def render_analytics_tab(self):
        """Render Advanced Analytics Tab"""
        abc = self.all_kpis['abc_analysis']
        valuation = self.all_kpis['inventory_valuation']
        supplier_perf = self.all_kpis['supplier_performance']
        aging = self.all_kpis['item_aging']
        
        return html.Div([
            # ABC Analysis
            self.ui.create_section_container([
                self.ui.create_section_header('📊', 'ABC Analysis'),
                html.Div([
                    self.ui.create_abc_category_card('A', abc['category_A']),
                    self.ui.create_abc_category_card('B', abc['category_B']),
                    self.ui.create_abc_category_card('C', abc['category_C']),
                ])
            ]),
            
            # Inventory Valuation
            self.ui.create_section_container([
                self.ui.create_section_header('💎', 'Inventory Valuation Methods'),
                html.Div([
                    self.ui.create_kpi_card('FIFO Method', f'${valuation["fifo_valuation"]:,.0f}', 
                                          'First In First Out', '1️⃣', self.ui.colors['primary']),
                    self.ui.create_kpi_card('Average Cost', f'${valuation["average_cost_valuation"]:,.0f}', 
                                          'Simple Average', '2️⃣', self.ui.colors['info']),
                    self.ui.create_kpi_card('Weighted Avg', f'${valuation["weighted_average_valuation"]:,.0f}', 
                                          'Quantity Weighted', '3️⃣', self.ui.colors['success']),
                    self.ui.create_kpi_card('Total Units', f'{valuation["total_units"]:,}', 
                                          'All Warehouses', '📦', self.ui.colors['warning']),
                ], style={'padding': '10px 20px'}),
            ]),
            
            # Supplier Performance
            self.ui.create_section_container([
                self.ui.create_section_header('🏆', 'Supplier Performance'),
                html.Div([
                    dcc.Graph(figure=self.charts.create_supplier_performance_chart(supplier_perf), config={'displayModeBar': False})
                ], style={'padding': '0 20px 20px 20px'})
            ]),
            
            # Item Aging
            self.ui.create_section_container([
                self.ui.create_section_header('⏳', 'Item Aging Analysis'),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=self.charts.create_aging_chart(aging), config={'displayModeBar': False})
                    ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                    
                    html.Div([
                        dcc.Graph(figure=self.charts.create_aging_value_chart(aging), config={'displayModeBar': False})
                    ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
                ])
            ]),
        ])
    
    def render_details_tab(self):
        """Render Inventory Details Tab"""
        return html.Div([
            # Detailed Stock Table
            self.ui.create_section_container([
                self.ui.create_section_header('📋', 'Detailed Stock Inventory'),
                dash_table.DataTable(
                    id='stock-table',
                    data=self.df.to_dict('records'),
                    columns=[
                        {'name': 'SKU', 'id': 'SKU'},
                        {'name': 'Product', 'id': 'Product'},
                        {'name': 'Category', 'id': 'Category'},
                        {'name': 'Quantity', 'id': 'Quantity'},
                        {'name': 'Reorder Level', 'id': 'Reorder_Level'},
                        {'name': 'Unit Price ($)', 'id': 'Unit_Price'},
                        {'name': 'Total Value ($)', 'id': 'Total_Value'},
                        {'name': 'Status', 'id': 'Stock_Status'},
                        {'name': 'Warehouse', 'id': 'Warehouse'},
                        {'name': 'Supplier', 'id': 'Supplier'},
                        {'name': 'Last Restocked', 'id': 'Last_Restocked'},
                    ],
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'fontFamily': 'Arial',
                        'backgroundColor': self.ui.colors['card_bg'],
                        'color': self.ui.colors['text']
                    },
                    style_header={
                        'backgroundColor': self.ui.colors['primary'],
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Stock_Status} = "Critical"'},
                            'backgroundColor': '#3d1f1f',
                            'color': self.ui.colors['danger']
                        },
                        {
                            'if': {'filter_query': '{Stock_Status} = "Low"'},
                            'backgroundColor': '#3d2f1a',
                            'color': self.ui.colors['warning']
                        },
                        {
                            'if': {'filter_query': '{Stock_Status} = "Overstocked"'},
                            'backgroundColor': '#1f3d23',
                            'color': self.ui.colors['success']
                        }
                    ],
                    page_size=20,
                    sort_action='native',
                    filter_action='native',
                    export_format='xlsx',
                    export_headers='display'
                )
            ]),
        ])
