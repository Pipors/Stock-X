"""
KPI Details Modal Generator.
Handles: Creating detailed KPI information modals with formulas, calculations, and product tables
"""

from dash import html, dash_table
from config import COLORS


class KPIDetailsModal:
    """Generates detailed KPI information modals"""
    
    def __init__(self, df, all_kpis, colors=None):
        """Initialize modal generator with data"""
        self.df = df
        self.all_kpis = all_kpis
        self.colors = colors or COLORS
    
    def generate_kpi_details(self, kpi_id):
        """Generate detailed KPI calculation information modal"""
        kpi_data = self.all_kpis.get(kpi_id, {})
        
        # Get KPI information
        kpi_info = self._get_kpi_info(kpi_id, kpi_data)
        
        if not kpi_info:
            return html.Div([
                html.H3('KPI details not available', style={'color': self.colors['text']})
            ])
        
        # Create modal content
        return html.Div([
            html.Div([
                html.Div([
                    # Header with close button
                    html.Div([
                        html.H2(kpi_info['title'], style={'color': self.colors['text'], 'margin': '0'}),
                        html.Button('✕', id='close-modal', 
                                   style={'backgroundColor': 'transparent', 'border': 'none', 
                                          'color': self.colors['text'], 'fontSize': '32px', 
                                          'cursor': 'pointer', 'position': 'absolute', 'right': '10px', 'top': '0px'})
                    ], style={'position': 'relative', 'borderBottom': f'2px solid {self.colors["border"]}', 'paddingBottom': '15px'}),
                    
                    # Formula
                    #self._create_formula_section(kpi_info['formula']),
                    
                    # Calculation Steps
                    self._create_calculation_steps_section(kpi_info['calculation_steps']),
                    
                    # Interpretation
                    self._create_interpretation_section(kpi_info['interpretation']),
                    
                    # Benchmark
                    self._create_benchmark_section(kpi_info['benchmark']),
                    
                    # Products Table
                    self._create_products_table_section(kpi_info['products_table'])
                    
                ], style={
                    'backgroundColor': self.colors['background'],
                    'padding': '30px',
                    'borderRadius': '12px',
                    'maxWidth': '900px',
                    'maxHeight': '90vh',
                    'overflow': 'auto',
                    'border': f'2px solid {self.colors["border"]}',
                    'boxShadow': '0 10px 40px rgba(0,0,0,0.5)',
                    'position': 'relative',
                    'margin': 'auto'
                })
            ])
        ])
    
    def _create_formula_section(self, formula):
        """Create formula display section"""
        return html.Div([
            html.H4('📐 Formula:', style={'color': self.colors['primary'], 'marginTop': '20px'}),
            html.P(formula, style={'color': self.colors['text'], 'fontSize': '16px', 
                                   'backgroundColor': self.colors['hover'], 'padding': '15px', 
                                   'borderRadius': '8px', 'fontFamily': 'monospace'})
        ])
    
    def _create_calculation_steps_section(self, steps):
        """Create calculation steps section"""
        return html.Div([
            html.H4('🔢 Calculation Steps:', style={'color': self.colors['primary'], 'marginTop': '20px'}),
            html.Div([
                html.P(step, style={'color': self.colors['text'], 'margin': '8px 0', 'fontSize': '14px'})
                for step in steps
            ])
        ], style={'backgroundColor': self.colors['card_bg'], 'padding': '15px', 'borderRadius': '8px', 'marginTop': '10px'})
    
    def _create_interpretation_section(self, interpretation):
        """Create interpretation section"""
        return html.Div([
            html.H4('💡 Interpretation:', style={'color': self.colors['success'], 'marginTop': '20px'}),
            html.P(interpretation, style={'color': self.colors['text'], 'fontSize': '14px'})
        ])
    
    def _create_benchmark_section(self, benchmark):
        """Create benchmark section"""
        return html.Div([
            html.H4('🎯 Benchmark:', style={'color': self.colors['warning'], 'marginTop': '20px'}),
            html.P(benchmark, style={'color': self.colors['text'], 'fontSize': '14px', 
                                     'backgroundColor': self.colors['hover'], 'padding': '10px', 
                                     'borderRadius': '8px'})
        ])
    
    def _create_products_table_section(self, products_table):
        """Create products table section"""
        return html.Div([
            html.H4('📦 Related Products:', style={'color': self.colors['info'], 'marginTop': '20px'}),
            dash_table.DataTable(
                data=products_table.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in products_table.columns],
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'backgroundColor': self.colors['card_bg'],
                    'color': self.colors['text'],
                    'fontSize': '12px'
                },
                style_header={
                    'backgroundColor': self.colors['primary'],
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': self.colors['hover']
                    }
                ],
                page_size=10
            )
        ], style={'marginTop': '20px'})
    
    def _get_kpi_info(self, kpi_id, kpi_data):
        """Get KPI information dictionary based on KPI ID"""
        kpi_definitions = {
            'inventory_turnover': self._get_inventory_turnover_info(kpi_data),
            'dsi': self._get_dsi_info(kpi_data),
            'stock_accuracy': self._get_stock_accuracy_info(kpi_data),
            'stockout': self._get_stockout_info(kpi_data),
            'fulfillment': self._get_fulfillment_info(kpi_data),
            'carrying_cost': self._get_carrying_cost_info(kpi_data),
            'dead_stock': self._get_dead_stock_info(kpi_data),
            'backorder': self._get_backorder_info(kpi_data),
            'fill_rate': self._get_fill_rate_info(kpi_data),
            'shrinkage': self._get_shrinkage_info(kpi_data),
            'lead_time': self._get_lead_time_info(kpi_data)
        }
        
        return kpi_definitions.get(kpi_id, {})
    
    def _get_inventory_turnover_info(self, kpi_data):
        """Get inventory turnover KPI info"""
        return {
            'title': '🔄 Inventory Turnover Ratio',
            'formula': 'Inventory Turnover = Cost of Goods Sold (COGS) / Average Inventory Value',
            'calculation_steps': [
                f"1. Total Inventory Value: ${self.df['Total_Value'].sum():,.2f}",
                f"2. Number of Products: {len(self.df)}",
                f"3. Average Product Value: ${self.df['Total_Value'].mean():,.2f}",
                f"4. Estimated COGS (60% of inventory): ${self.df['Total_Value'].sum() * 0.6:,.2f}",
                f"5. Annual Turnover Ratio: {kpi_data.get('annual_turnover', 0)}x"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Industry Standard: 5-10x per year (varies by industry)',
            'products_table': self.df[['Product', 'Quantity', 'Total_Value', 'Stock_Status']].sort_values('Total_Value', ascending=False).head(10)
        }
    
    def _get_dsi_info(self, kpi_data):
        """Get DSI KPI info"""
        return {
            'title': '📅 Days Sales Inventory (DSI)',
            'formula': 'DSI = (Average Inventory / COGS) × 365 days',
            'calculation_steps': [
                f"1. Average Inventory Value: ${self.df['Total_Value'].sum():,.2f}",
                f"2. Daily COGS: ${(self.df['Total_Value'].sum() * 0.6) / 365:,.2f}",
                f"3. Days Sales Inventory: {kpi_data.get('days_sales_inventory', 0)} days",
                f"4. This means inventory sits for ~{kpi_data.get('days_sales_inventory', 0)} days before being sold"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Lower DSI is better (30-60 days is ideal for most industries)',
            'products_table': self.df[['Product', 'Quantity', 'Last_Restocked', 'Stock_Status']].sort_values('Last_Restocked')
        }
    
    def _get_stock_accuracy_info(self, kpi_data):
        """Get stock accuracy KPI info"""
        return {
            'title': '🎯 Stock Accuracy Rate',
            'formula': 'Stock Accuracy = (Accurate Stock Records / Total Stock Items) × 100',
            'calculation_steps': [
                f"1. Total Items in System: {kpi_data.get('total_items', 0)}",
                f"2. Items with Accurate Records: {kpi_data.get('accurate_items', 0)}",
                f"3. Accuracy Rate: {kpi_data.get('accuracy_rate', 0)}%",
                f"4. Discrepancies Found: {kpi_data.get('total_items', 0) - kpi_data.get('accurate_items', 0)}"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: >95% accuracy',
            'products_table': self.df[['Product', 'Quantity', 'Stock_Status', 'Warehouse']].head(15)
        }
    
    def _get_stockout_info(self, kpi_data):
        """Get stockout KPI info"""
        return {
            'title': '⚠️ Stockout Rate',
            'formula': 'Stockout Rate = (Items Below Reorder Level / Total Items) × 100',
            'calculation_steps': [
                f"1. Total Items: {len(self.df)}",
                f"2. Items Below Reorder Level: {kpi_data.get('stockout_items', 0)}",
                f"3. Critical Items: {len(self.df[self.df['Stock_Status'] == 'Critical'])}",
                f"4. Low Stock Items: {len(self.df[self.df['Stock_Status'] == 'Low'])}",
                f"5. Stockout Rate: {kpi_data.get('stockout_rate', 0)}%"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: <5% stockout rate',
            'products_table': self.df[self.df['Stock_Status'].isin(['Critical', 'Low'])][['Product', 'Quantity', 'Reorder_Level', 'Stock_Status']].sort_values('Quantity')
        }
    
    def _get_fulfillment_info(self, kpi_data):
        """Get fulfillment KPI info"""
        return {
            'title': '✅ Order Fulfillment Rate',
            'formula': 'Fulfillment Rate = (Fulfilled Orders / Total Orders) × 100',
            'calculation_steps': [
                f"1. Total Orders (30 days): {kpi_data.get('total_orders', 0)}",
                f"2. Successfully Fulfilled: {kpi_data.get('fulfilled_orders', 0)}",
                f"3. Pending/Failed: {kpi_data.get('total_orders', 0) - kpi_data.get('fulfilled_orders', 0)}",
                f"4. Fulfillment Rate: {kpi_data.get('fulfillment_rate', 0)}%"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: >95% same-day fulfillment',
            'products_table': self.df.nlargest(10, 'Quantity')[['Product', 'Quantity', 'Stock_Status', 'Warehouse']]
        }
    
    def _get_carrying_cost_info(self, kpi_data):
        """Get carrying cost KPI info"""
        return {
            'title': '💸 Inventory Carrying Cost',
            'formula': 'Carrying Cost = Inventory Value × Carrying Cost Rate (typically 20-30%)',
            'calculation_steps': [
                f"1. Total Inventory Value: ${kpi_data.get('inventory_value', 0):,.2f}",
                f"2. Carrying Cost Rate: {kpi_data.get('carrying_cost_rate', 0)}%",
                f"3. Annual Carrying Cost: ${kpi_data.get('annual_carrying_cost', 0):,.2f}",
                f"4. Storage Cost: ${kpi_data.get('breakdown', {}).get('Storage', 0):,.2f}",
                f"5. Insurance Cost: ${kpi_data.get('breakdown', {}).get('Insurance', 0):,.2f}",
                f"6. Obsolescence: ${kpi_data.get('breakdown', {}).get('Obsolescence', 0):,.2f}",
                f"7. Opportunity Cost: ${kpi_data.get('breakdown', {}).get('Opportunity Cost', 0):,.2f}"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Industry Average: 20-30% of inventory value',
            'products_table': self.df.nlargest(10, 'Total_Value')[['Product', 'Quantity', 'Unit_Price', 'Total_Value']]
        }
    
    def _get_dead_stock_info(self, kpi_data):
        """Get dead stock KPI info"""
        return {
            'title': '☠️ Dead Stock Percentage',
            'formula': 'Dead Stock % = (Value of Dead Stock / Total Inventory Value) × 100',
            'calculation_steps': [
                f"1. Total Inventory Value: ${self.df['Total_Value'].sum():,.2f}",
                f"2. Dead Stock Value: ${kpi_data.get('dead_stock_value', 0):,.2f}",
                f"3. Dead Stock Items: {kpi_data.get('dead_stock_count', 0)}",
                f"4. Dead Stock Percentage: {kpi_data.get('dead_stock_percentage', 0)}%",
                f"5. Items with no movement >90 days"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: <5% of total inventory',
            'products_table': self.df[self.df['Stock_Status'] == 'Overstocked'].nlargest(10, 'Quantity')[['Product', 'Quantity', 'Total_Value', 'Last_Restocked']]
        }
    
    def _get_backorder_info(self, kpi_data):
        """Get backorder KPI info"""
        return {
            'title': '📦 Backorder Rate',
            'formula': 'Backorder Rate = (Backorders / Total Orders) × 100',
            'calculation_steps': [
                f"1. Total Orders: {kpi_data.get('total_orders', 0)}",
                f"2. Backorders: {kpi_data.get('backorders', 0)}",
                f"3. Backorder Rate: {kpi_data.get('backorder_rate', 0)}%",
                f"4. Estimated backorder from Critical/Low stock items"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: <2% backorder rate',
            'products_table': self.df[self.df['Stock_Status'].isin(['Critical', 'Low'])][['Product', 'Quantity', 'Reorder_Level', 'Supplier']]
        }
    
    def _get_fill_rate_info(self, kpi_data):
        """Get fill rate KPI info"""
        return {
            'title': '📊 Fill Rate',
            'formula': 'Fill Rate = (Items in Stock / Total Items) × 100',
            'calculation_steps': [
                f"1. Total Items: {kpi_data.get('total_items', 0)}",
                f"2. Items in Stock: {kpi_data.get('items_in_stock', 0)}",
                f"3. Out of Stock: {kpi_data.get('total_items', 0) - kpi_data.get('items_in_stock', 0)}",
                f"4. Fill Rate: {kpi_data.get('fill_rate', 0)}%"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: >98% fill rate',
            'products_table': self.df[['Product', 'Quantity', 'Stock_Status', 'Category']].sort_values('Quantity')
        }
    
    def _get_shrinkage_info(self, kpi_data):
        """Get shrinkage KPI info"""
        return {
            'title': '📉 Inventory Shrinkage',
            'formula': 'Shrinkage Rate = ((Expected - Actual Inventory) / Expected) × 100',
            'calculation_steps': [
                f"1. Expected Inventory Value: ${kpi_data.get('expected_inventory', 0):,.2f}",
                f"2. Actual Inventory Value: ${self.df['Total_Value'].sum():,.2f}",
                f"3. Shrinkage Value: ${kpi_data.get('shrinkage_value', 0):,.2f}",
                f"4. Shrinkage Rate: {kpi_data.get('shrinkage_rate', 0)}%",
                f"5. Due to theft, damage, errors, etc."
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Industry Average: 1-2%',
            'products_table': self.df.sample(min(10, len(self.df)))[['Product', 'Quantity', 'Total_Value', 'Warehouse']]
        }
    
    def _get_lead_time_info(self, kpi_data):
        """Get lead time KPI info"""
        return {
            'title': '⏱️ Lead Time Analysis',
            'formula': 'Average Lead Time = Sum of all lead times / Number of suppliers',
            'calculation_steps': [
                f"1. Number of Suppliers: {self.df['Supplier'].nunique()}",
                f"2. Average Lead Time: {kpi_data.get('average_lead_time_days', 0)} days",
                f"3. Minimum Lead Time: {kpi_data.get('min_lead_time', 0)} days",
                f"4. Maximum Lead Time: {kpi_data.get('max_lead_time', 0)} days",
                f"5. Lead time varies by supplier and product type"
            ],
            'interpretation': kpi_data.get('interpretation', ''),
            'benchmark': 'Target: <7 days average',
            'products_table': self.df.groupby('Supplier').agg({
                'Product': 'count',
                'Total_Value': 'sum',
                'Quantity': 'sum'
            }).reset_index().rename(columns={'Product': 'Items'}).sort_values('Total_Value', ascending=False)
        }
