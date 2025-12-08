"""
Flask API Server - Provides data endpoints for the dashboard
Pure backend - no UI rendering
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from .data_api import DashboardDataAPI
from datetime import datetime
import traceback
import os

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, 
            static_folder=os.path.join(BASE_DIR, 'static'),
            static_url_path='/static',
            template_folder=os.path.join(BASE_DIR, 'templates'))
CORS(app)

# Initialize data API
data_api = DashboardDataAPI()

# Register forecasting blueprint
try:
    from ..forecasting.api import forecast_bp
    app.register_blueprint(forecast_bp)
    print("✅ Forecasting API registered")
except ImportError as e:
    print(f"⚠️ Forecasting API not available: {e}")

@app.route('/')
def index():
    """Serve the main dashboard HTML (single-page app)"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Check API health status"""
    return jsonify(data_api.health_check())

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get all dashboard data"""
    try:
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        data = data_api.get_dashboard_data(refresh=refresh)
        
        # Convert to JSON-serializable format
        response_data = {
            'stock': data['stock'],
            'transactions': data['transactions'],
            'kpis': data['kpis'],
            'summary': data['summary']
        }
        
        return jsonify({
            'success': True,
            'data': response_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error in /api/dashboard: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/api/stock')
def get_stock():
    """Get stock summary"""
    try:
        df = data_api.get_stock_summary()
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'count': len(df)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/transactions')
def get_transactions():
    """Get transaction history"""
    try:
        days = request.args.get('days', None)
        if days:
            days = int(days)
        df = data_api.get_transactions(days=days)
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'count': len(df)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kpis')
def get_kpis():
    """Get all KPIs"""
    try:
        stock_df = data_api.get_stock_summary()
        trans_df = data_api.get_transactions()
        kpis = data_api.calculate_kpis(stock_df, trans_df)
        return jsonify({
            'success': True,
            'data': kpis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kpi/<kpi_id>')
def get_kpi_detail(kpi_id):
    """Get specific KPI details"""
    try:
        data = data_api.get_kpi_details(kpi_id)
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        return jsonify({
            'success': False,
            'error': 'KPI not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stock/low')
def get_low_stock():
    """Get low stock items"""
    try:
        df = data_api.get_low_stock_items()
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'count': len(df)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stock/by-warehouse')
def get_stock_by_warehouse():
    """Get stock grouped by warehouse"""
    try:
        df = data_api.get_stock_by_warehouse()
        return jsonify({
            'success': True,
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stock/by-category')
def get_stock_by_category():
    """Get stock grouped by category"""
    try:
        df = data_api.get_stock_by_category()
        return jsonify({
            'success': True,
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export/json')
def export_json():
    """Export dashboard data to JSON"""
    try:
        filename = data_api.export_to_json()
        return jsonify({
            'success': True,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export/csv')
def export_csv():
    """Export data to CSV files"""
    try:
        files = data_api.export_to_csv()
        return jsonify({
            'success': True,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Flask API Server for Stock Dashboard")
    print("=" * 70)
    print("📊 Dashboard URL: http://127.0.0.1:5000")
    print("🔌 API Endpoints:")
    print("   GET  /api/health              - Health check")
    print("   GET  /api/dashboard           - All dashboard data")
    print("   GET  /api/stock               - Stock summary")
    print("   GET  /api/transactions        - Transaction history")
    print("   GET  /api/kpis                - All KPIs")
    print("   GET  /api/kpi/<id>            - Specific KPI details")
    print("   GET  /api/stock/low           - Low stock items")
    print("   GET  /api/stock/by-warehouse  - Stock by warehouse")
    print("   GET  /api/stock/by-category   - Stock by category")
    print("   GET  /api/export/json         - Export to JSON")
    print("   GET  /api/export/csv          - Export to CSV")
    print("=" * 70)
    print("\n✨ Features:")
    print("  • Pure REST API - No server-side rendering")
    print("  • HTML/CSS/JS frontend - Client-side rendering")
    print("  • Auto-refresh every 60 seconds")
    print("  • Responsive design")
    print("=" * 70)
    
    app.run(host='127.0.0.1', port=5000, debug=True)
