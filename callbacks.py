"""
Callbacks module for dashboard interactivity.
Handles: All Dash callbacks for user interactions
"""

import dash
from dash.dependencies import Input, Output


class DashboardCallbacks:
    """Manages all dashboard callbacks"""
    
    def __init__(self, app, tab_renderer, kpi_modal_generator):
        """Initialize callbacks with app and components"""
        self.app = app
        self.tab_renderer = tab_renderer
        self.kpi_modal = kpi_modal_generator
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register all callbacks"""
        self._register_tab_navigation_callback()
        self._register_kpi_click_callback()
        self._register_modal_toggle_callback()
    
    def _register_tab_navigation_callback(self):
        """Register callback for tab navigation"""
        @self.app.callback(
            Output('tab-content', 'children'),
            Input('main-tabs', 'value')
        )
        def render_tab_content(tab):
            if tab == 'stock-overview':
                return self.tab_renderer.render_stock_overview_tab()
            elif tab == 'kpis':
                return self.tab_renderer.render_kpi_tab()
            elif tab == 'analytics':
                return self.tab_renderer.render_analytics_tab()
            elif tab == 'details':
                return self.tab_renderer.render_details_tab()
    
    def _register_kpi_click_callback(self):
        """Register callback to store clicked KPI"""
        @self.app.callback(
            Output('clicked-kpi-store', 'data'),
            Input({'type': 'kpi-card', 'index': dash.dependencies.ALL}, 'n_clicks'),
            prevent_initial_call=True
        )
        def store_clicked_kpi(n_clicks):
            ctx = dash.callback_context
            
            if not ctx.triggered:
                return dash.no_update
            
            # Get which card was clicked
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == '.' or not button_id:
                return dash.no_update
            
            try:
                kpi_id = eval(button_id)['index']
                return kpi_id
            except:
                return dash.no_update
    
    def _register_modal_toggle_callback(self):
        """Register callback to show/hide KPI modal"""
        @self.app.callback(
            Output('kpi-modal', 'style'),
            Output('kpi-modal', 'children'),
            Input('clicked-kpi-store', 'data'),
            Input('close-modal', 'n_clicks'),
            prevent_initial_call=True
        )
        def toggle_kpi_modal(kpi_id, close_clicks):
            ctx = dash.callback_context
            
            if not ctx.triggered:
                return dash.no_update, dash.no_update
            
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            # If close button was clicked
            if trigger_id == 'close-modal':
                return {'display': 'none'}, []
            
            # If a KPI was clicked
            if trigger_id == 'clicked-kpi-store' and kpi_id:
                modal_content = self.kpi_modal.generate_kpi_details(kpi_id)
                
                modal_style = {
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'backgroundColor': 'rgba(0,0,0,0.8)',
                    'zIndex': '1000',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'overflow': 'auto',
                    'padding': '20px'
                }
                
                return modal_style, modal_content
            
            return dash.no_update, dash.no_update
