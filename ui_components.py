"""
UI Components module for reusable dashboard elements.
Handles: KPI cards, modals, headers, and common UI elements
"""

from dash import html
from config import COLORS


class UIComponents:
    """Reusable UI components for dashboard"""
    
    def __init__(self, colors=None):
        """Initialize UI components with color scheme"""
        self.colors = colors or COLORS
    
    def create_kpi_card(self, title, value, subtitle, icon, color, status=None, kpi_id=None):
        """Create a KPI display card (clickable if kpi_id provided)"""
        status_color = self.colors['success'] if status in ['Excellent', 'Good'] else \
                      self.colors['warning'] if status == 'Average' else \
                      self.colors['danger']
        
        card_style = {
            'backgroundColor': self.colors['card_bg'], 
            'padding': '20px', 
            'borderRadius': '8px', 
            'boxShadow': '0 4px 12px rgba(0,0,0,0.3)', 
            'height': '100%',
            'border': f'2px solid {self.colors["border"]}', 
            'borderLeft': f'4px solid {color}',
            'cursor': 'pointer' if kpi_id else 'default',
            'transition': 'transform 0.2s, box-shadow 0.2s'
        }
        
        return html.Div([
            html.Div([
                html.Div([
                    html.Span(icon, style={'fontSize': '40px', 'marginBottom': '10px'}),
                    html.H4(title, style={'color': self.colors['text'], 'margin': '10px 0', 'fontSize': '14px'}),
                    html.H2(value, style={'color': color, 'margin': '10px 0', 'fontSize': '28px', 'fontWeight': 'bold'}),
                    html.P(subtitle, style={'color': '#8b949e', 'margin': '5px 0', 'fontSize': '12px'}),
                    html.Span(status if status else '', 
                             style={'backgroundColor': status_color if status else 'transparent', 
                                    'color': 'white', 'padding': '4px 12px', 'borderRadius': '12px',
                                    'fontSize': '11px', 'fontWeight': 'bold', 'marginTop': '8px', 'display': 'inline-block'}),
                    html.P('🔍 Click for details' if kpi_id else '', 
                          style={'color': self.colors['primary'], 'fontSize': '10px', 'marginTop': '8px', 'fontStyle': 'italic'})
                ], style={'textAlign': 'center'})
            ], style=card_style, id={'type': 'kpi-card', 'index': kpi_id} if kpi_id else {})
        ], style={'width': '19%', 'display': 'inline-block', 'margin': '0.5%', 'verticalAlign': 'top'})
    
    def create_header(self, last_updated):
        """Create dashboard header"""
        return html.Div([
            html.H1('📊 Stock Management System', 
                    style={'textAlign': 'center', 'color': self.colors['text'], 'padding': '20px', 'margin': '0'}),
            html.P(f'Last Updated: {last_updated} | Comprehensive Analytics',
                   style={'textAlign': 'center', 'color': '#8b949e', 'marginTop': '-10px'})
        ], style={'backgroundColor': self.colors['card_bg'], 'boxShadow': '0 4px 12px rgba(0,0,0,0.3)', 
                  'marginBottom': '20px', 'border': f'1px solid {self.colors["border"]}'})
    
    def create_section_header(self, icon, title):
        """Create section header with icon"""
        return html.H3(f'{icon} {title}', 
                      style={'color': self.colors['text'], 'padding': '20px 20px 10px 20px'})
    
    def create_abc_category_card(self, category_letter, data):
        """Create ABC analysis category card"""
        color_map = {
            'A': self.colors['danger'],
            'B': self.colors['warning'],
            'C': self.colors['success']
        }
        bg_map = {
            'A': '#3d1f1f',
            'B': '#3d2f1a',
            'C': '#1f3d23'
        }
        
        color = color_map[category_letter]
        bg_color = bg_map[category_letter]
        
        return html.Div([
            html.Div([
                html.H2(category_letter, style={'color': color, 'fontSize': '48px', 'margin': '0'}),
                html.H4(f'{data["count"]} items', style={'color': self.colors['text'], 'margin': '10px 0'}),
                html.P(f'{data["percentage"]}% of items', style={'color': '#8b949e'}),
                html.H3(f'${data["value"]:,.0f}', style={'color': color, 'margin': '10px 0'}),
                html.P(f'{data["value_percentage"]}% of value', style={'color': '#8b949e'})
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': bg_color, 
                     'borderRadius': '8px', 'border': f'2px solid {color}'})
        ], style={'width': '31%', 'display': 'inline-block', 'margin': '1%'})
    
    def create_section_container(self, children):
        """Create styled container for section content"""
        return html.Div(children, 
                       style={'backgroundColor': self.colors['card_bg'], 'margin': '20px', 
                              'borderRadius': '8px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.3)',
                              'border': f'1px solid {self.colors["border"]}'})
