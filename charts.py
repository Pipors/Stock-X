"""
Chart generation module for all visualizations.
Handles: Creating Plotly charts with consistent theming
"""

import plotly.graph_objs as go
from config import COLORS


class ChartBuilder:
    """Builds Plotly charts with consistent styling"""
    
    def __init__(self, df, colors=None):
        """Initialize chart builder with data and colors"""
        self.df = df
        self.colors = colors or COLORS
    
    def create_stock_by_category_chart(self):
        """Create bar chart of stock quantity by category"""
        cat_data = self.df.groupby('Category')['Quantity'].sum().reset_index()
        fig = go.Figure(data=[
            go.Bar(x=cat_data['Category'], y=cat_data['Quantity'], marker_color=self.colors['primary'])
        ])
        fig.update_layout(
            title='Stock Quantity by Category',
            xaxis_title='Category',
            yaxis_title='Quantity',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
    
    def create_stock_status_pie(self):
        """Create pie chart of stock status distribution"""
        status_data = self.df['Stock_Status'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=status_data.index,
            values=status_data.values,
            hole=0.4,
            marker=dict(colors=[self.colors['danger'], self.colors['warning'], 
                               self.colors['success'], self.colors['primary']])
        )])
        fig.update_layout(
            title='Stock Status Distribution',
            paper_bgcolor=self.colors['card_bg'],
            plot_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
    
    def create_value_by_warehouse_chart(self):
        """Create bar chart of total stock value by warehouse"""
        wh_data = self.df.groupby('Warehouse')['Total_Value'].sum().reset_index()
        fig = go.Figure(data=[
            go.Bar(x=wh_data['Warehouse'], y=wh_data['Total_Value'], marker_color=self.colors['success'])
        ])
        fig.update_layout(
            title='Total Stock Value by Warehouse',
            xaxis_title='Warehouse',
            yaxis_title='Value ($)',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
    
    def create_top_products_chart(self):
        """Create bar chart of top 10 products by value"""
        top_products = self.df.nlargest(10, 'Total_Value')
        fig = go.Figure(data=[
            go.Bar(x=top_products['Product'], y=top_products['Total_Value'], 
                   marker_color=self.colors['warning'])
        ])
        fig.update_layout(
            title='Top 10 Products by Value',
            xaxis_title='Product',
            yaxis_title='Value ($)',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400,
            xaxis={'tickangle': -45}
        )
        return fig
    
    def create_carrying_cost_chart(self, carrying):
        """Create bar chart of carrying cost breakdown"""
        breakdown = carrying['breakdown']
        fig = go.Figure(data=[
            go.Bar(
                x=list(breakdown.keys()),
                y=list(breakdown.values()),
                marker_color=[self.colors['primary'], self.colors['info'], 
                             self.colors['warning'], self.colors['danger']],
                text=[f'${v:,.0f}' for v in breakdown.values()],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title='Carrying Cost Components',
            xaxis_title='Cost Type',
            yaxis_title='Amount ($)',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
    
    def create_supplier_performance_chart(self, supplier_perf):
        """Create dual-axis chart for supplier performance"""
        suppliers = list(supplier_perf['suppliers'].keys())
        scores = [supplier_perf['suppliers'][s]['quality_score'] for s in suppliers]
        values = [supplier_perf['suppliers'][s]['total_value'] for s in suppliers]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Quality Score', x=suppliers, y=scores, marker_color=self.colors['success']))
        fig.add_trace(go.Scatter(name='Total Value', x=suppliers, y=values, yaxis='y2', 
                                mode='lines+markers', marker=dict(size=10, color=self.colors['primary'])))
        
        fig.update_layout(
            title='Supplier Performance Analysis',
            xaxis_title='Supplier',
            yaxis_title='Quality Score',
            yaxis2=dict(title='Total Value ($)', overlaying='y', side='right'),
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400,
            legend=dict(x=0.01, y=0.99)
        )
        return fig
    
    def create_aging_chart(self, aging):
        """Create bar chart of item count by age"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(aging['age_distribution'].keys()),
                y=list(aging['age_distribution'].values()),
                marker_color=[self.colors['success'], self.colors['info'], 
                             self.colors['warning'], self.colors['danger']],
                text=list(aging['age_distribution'].values()),
                textposition='auto'
            )
        ])
        fig.update_layout(
            title='Item Count by Age',
            xaxis_title='Age Range',
            yaxis_title='Number of Items',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
    
    def create_aging_value_chart(self, aging):
        """Create bar chart of inventory value by age"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(aging['value_by_age'].keys()),
                y=list(aging['value_by_age'].values()),
                marker_color=[self.colors['success'], self.colors['info'], 
                             self.colors['warning'], self.colors['danger']],
                text=[f'${v:,.0f}' for v in aging['value_by_age'].values()],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title='Inventory Value by Age',
            xaxis_title='Age Range',
            yaxis_title='Value ($)',
            plot_bgcolor=self.colors['card_bg'],
            paper_bgcolor=self.colors['card_bg'],
            font={'color': self.colors['text']},
            height=400
        )
        return fig
