"""
Forecasting API Endpoints
Provides REST API for inventory forecasting
"""

from flask import Blueprint, jsonify, request
import pandas as pd
from ..forecasting import InventoryForecaster
from ..api.data_api import DashboardDataAPI

# Create blueprint
forecast_bp = Blueprint('forecast', __name__, url_prefix='/api/forecast')

# Initialize data API
data_api = DashboardDataAPI()


@forecast_bp.route('/demand', methods=['POST'])
def forecast_demand():
    """
    Generate demand forecast for a product
    
    Request body:
        product_id: Product ID to forecast (optional, forecasts all if not provided)
        periods: Number of days to forecast (default: 30)
        model: Model type - 'auto', 'prophet', 'xgboost', 'simple' (default: 'auto')
    """
    try:
        params = request.get_json() or {}
        product_id = params.get('product_id')
        periods = params.get('periods', 30)
        model_type = params.get('model', 'auto')
        
        # Get transaction data
        dashboard_data = data_api.get_dashboard_data()
        transactions = pd.DataFrame(dashboard_data['transactions'])
        
        if transactions.empty:
            return jsonify({
                'success': False,
                'error': 'No transaction data available'
            }), 400
        
        # Initialize forecaster
        forecaster = InventoryForecaster(model_type=model_type)
        
        # Prepare and fit
        forecaster.prepare_data(
            transactions,
            product_id=product_id,
            date_col='Date',
            quantity_col='Quantity',
            product_col='Product_ID'
        )
        forecaster.fit()
        
        # Generate forecast
        forecast = forecaster.predict(periods)
        
        return jsonify({
            'success': True,
            'data': {
                'product_id': product_id,
                'periods': periods,
                'model': forecaster.model.name,
                'metrics': forecaster.get_metrics(),
                'forecast': forecaster.to_dict(forecast)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@forecast_bp.route('/reorder/<product_id>', methods=['GET'])
def get_reorder_recommendation(product_id: str):
    """
    Get reorder recommendation for a product
    
    Query params:
        current_stock: Current inventory level
        lead_time: Supplier lead time in days (default: 7)
    """
    try:
        current_stock = request.args.get('current_stock', type=int)
        lead_time = request.args.get('lead_time', 7, type=int)
        
        if current_stock is None:
            return jsonify({
                'success': False,
                'error': 'current_stock parameter required'
            }), 400
        
        # Get transaction data
        dashboard_data = data_api.get_dashboard_data()
        transactions = pd.DataFrame(dashboard_data['transactions'])
        
        # Generate forecast
        forecaster = InventoryForecaster(model_type='auto')
        forecaster.prepare_data(
            transactions,
            product_id=product_id,
            date_col='Date',
            quantity_col='Quantity',
            product_col='Product_ID'
        )
        forecaster.fit()
        forecast = forecaster.predict(lead_time + 14)  # Lead time + buffer
        
        # Get recommendation
        recommendation = forecaster.get_reorder_recommendations(
            forecast,
            current_stock=current_stock,
            lead_time_days=lead_time
        )
        
        return jsonify({
            'success': True,
            'data': recommendation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@forecast_bp.route('/batch', methods=['POST'])
def batch_forecast():
    """
    Generate forecasts for multiple products
    
    Request body:
        periods: Days to forecast (default: 30)
        top_n: Limit to top N products (optional)
    """
    try:
        params = request.get_json() or {}
        periods = params.get('periods', 30)
        top_n = params.get('top_n')
        
        # Get transaction data
        dashboard_data = data_api.get_dashboard_data()
        transactions = pd.DataFrame(dashboard_data['transactions'])
        
        # Initialize forecaster
        forecaster = InventoryForecaster(model_type='simple')  # Use simple for batch
        
        # Generate forecasts
        forecasts = forecaster.forecast_all_products(
            transactions,
            periods=periods,
            top_n=top_n,
            product_col='Product_ID'
        )
        
        # Convert to serializable format
        result = {}
        for product_id, forecast in forecasts.items():
            result[product_id] = forecaster.to_dict(forecast)
        
        return jsonify({
            'success': True,
            'data': {
                'products_forecasted': len(result),
                'periods': periods,
                'forecasts': result
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
