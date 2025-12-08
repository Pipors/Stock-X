"""
Inventory Forecaster - Main interface for demand prediction
Handles data preparation, model selection, and forecast generation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from .models import ProphetModel, XGBoostModel, EnsembleModel, SimpleMovingAverage


class InventoryForecaster:
    """
    Main forecasting interface for inventory demand prediction
    Optimized for medium-sized datasets (1000-100000 records)
    """
    
    def __init__(self, model_type: str = 'auto'):
        """
        Initialize forecaster
        
        Args:
            model_type: 'prophet', 'xgboost', 'ensemble', 'simple', or 'auto'
        """
        self.model_type = model_type
        self.model = None
        self.data = None
        self.product_id = None
        self.metrics = {}
    
    def _select_model(self, data_size: int) -> object:
        """Auto-select best model based on data characteristics"""
        if self.model_type == 'auto':
            if data_size < 30:
                print("📊 Auto-selected: Simple Moving Average (small dataset)")
                return SimpleMovingAverage(window=min(7, data_size))
            elif data_size < 365:
                print("📊 Auto-selected: XGBoost (medium dataset)")
                return XGBoostModel()
            else:
                print("📊 Auto-selected: Ensemble (large dataset)")
                return EnsembleModel()
        
        models = {
            'prophet': ProphetModel,
            'xgboost': XGBoostModel,
            'ensemble': EnsembleModel,
            'simple': SimpleMovingAverage
        }
        
        return models.get(self.model_type, XGBoostModel)()
    
    def prepare_data(self, 
                     transactions: pd.DataFrame,
                     product_id: Optional[str] = None,
                     date_col: str = 'Date',
                     quantity_col: str = 'Quantity',
                     product_col: str = 'Product_ID') -> pd.DataFrame:
        """
        Prepare transaction data for forecasting
        
        Args:
            transactions: DataFrame with transaction history
            product_id: Filter to specific product (optional)
            date_col: Name of date column
            quantity_col: Name of quantity column
            product_col: Name of product ID column
        
        Returns:
            Prepared DataFrame with 'ds' and 'y' columns
        """
        df = transactions.copy()
        
        # Filter by product if specified
        if product_id and product_col in df.columns:
            df = df[df[product_col] == product_id]
            self.product_id = product_id
        
        # Ensure date column exists
        if date_col not in df.columns:
            raise ValueError(f"Date column '{date_col}' not found")
        
        # Convert and aggregate by date
        df[date_col] = pd.to_datetime(df[date_col])
        
        if quantity_col in df.columns:
            daily = df.groupby(date_col)[quantity_col].sum().reset_index()
        else:
            # Count transactions as fallback
            daily = df.groupby(date_col).size().reset_index(name='count')
            quantity_col = 'count'
        
        # Rename to standard format
        daily.columns = ['ds', 'y']
        
        # Fill missing dates
        date_range = pd.date_range(start=daily['ds'].min(), end=daily['ds'].max())
        daily = daily.set_index('ds').reindex(date_range, fill_value=0).reset_index()
        daily.columns = ['ds', 'y']
        
        self.data = daily
        return daily
    
    def fit(self, df: Optional[pd.DataFrame] = None) -> 'InventoryForecaster':
        """
        Train the forecasting model
        
        Args:
            df: Prepared DataFrame (optional if prepare_data was called)
        
        Returns:
            self for method chaining
        """
        if df is not None:
            self.data = df
        
        if self.data is None:
            raise ValueError("No data provided. Call prepare_data() first or pass df")
        
        print(f"\n🔮 Training Forecasting Model")
        print(f"   Data points: {len(self.data)}")
        print(f"   Date range: {self.data['ds'].min()} to {self.data['ds'].max()}")
        
        self.model = self._select_model(len(self.data))
        self.model.fit(self.data)
        
        # Calculate training metrics
        self._calculate_metrics()
        
        print(f"   ✅ Model trained successfully")
        
        return self
    
    def predict(self, periods: int = 30) -> pd.DataFrame:
        """
        Generate demand forecast
        
        Args:
            periods: Number of days to forecast
        
        Returns:
            DataFrame with forecast, lower/upper bounds
        """
        if self.model is None or not self.model.is_fitted:
            raise ValueError("Model not trained. Call fit() first")
        
        print(f"\n📈 Generating {periods}-day forecast...")
        
        forecast = self.model.predict(periods)
        
        # Add additional info
        forecast['product_id'] = self.product_id
        forecast['model'] = self.model.name
        forecast['generated_at'] = datetime.now().isoformat()
        
        print(f"   ✅ Forecast generated")
        
        return forecast
    
    def _calculate_metrics(self) -> Dict:
        """Calculate model accuracy metrics using cross-validation"""
        if len(self.data) < 30:
            self.metrics = {'note': 'Insufficient data for CV'}
            return self.metrics
        
        # Simple holdout validation
        train_size = int(len(self.data) * 0.8)
        train = self.data.iloc[:train_size]
        test = self.data.iloc[train_size:]
        
        try:
            temp_model = self.model.__class__()
            temp_model.fit(train)
            predictions = temp_model.predict(len(test))
            
            actual = test['y'].values
            predicted = predictions['forecast'].values[:len(actual)]
            
            # Calculate metrics
            mae = np.mean(np.abs(actual - predicted))
            rmse = np.sqrt(np.mean((actual - predicted) ** 2))
            mape = np.mean(np.abs((actual - predicted) / (actual + 1))) * 100
            
            self.metrics = {
                'mae': round(mae, 2),
                'rmse': round(rmse, 2),
                'mape': round(mape, 2),
                'train_size': train_size,
                'test_size': len(test)
            }
        except Exception as e:
            self.metrics = {'error': str(e)}
        
        return self.metrics
    
    def get_metrics(self) -> Dict:
        """Get model performance metrics"""
        return self.metrics
    
    def forecast_all_products(self, 
                              transactions: pd.DataFrame,
                              periods: int = 30,
                              top_n: Optional[int] = None,
                              product_col: str = 'Product_ID') -> Dict[str, pd.DataFrame]:
        """
        Generate forecasts for multiple products
        
        Args:
            transactions: Full transaction history
            periods: Days to forecast
            top_n: Limit to top N products by transaction volume
            product_col: Product identifier column
        
        Returns:
            Dictionary of product_id -> forecast DataFrame
        """
        products = transactions[product_col].value_counts()
        
        if top_n:
            products = products.head(top_n)
        
        print(f"\n🔮 Forecasting {len(products)} products...")
        
        forecasts = {}
        
        for product_id in products.index:
            try:
                self.prepare_data(transactions, product_id=product_id, product_col=product_col)
                self.fit()
                forecast = self.predict(periods)
                forecasts[product_id] = forecast
                print(f"   ✓ {product_id}")
            except Exception as e:
                print(f"   ✗ {product_id}: {e}")
        
        return forecasts
    
    def get_reorder_recommendations(self, 
                                    forecast: pd.DataFrame,
                                    current_stock: int,
                                    lead_time_days: int = 7,
                                    safety_stock_multiplier: float = 1.5) -> Dict:
        """
        Get reorder recommendations based on forecast
        
        Args:
            forecast: Forecast DataFrame from predict()
            current_stock: Current inventory level
            lead_time_days: Supplier lead time in days
            safety_stock_multiplier: Safety stock factor
        
        Returns:
            Reorder recommendation dictionary
        """
        if len(forecast) < lead_time_days:
            return {'error': 'Forecast period shorter than lead time'}
        
        # Calculate expected demand during lead time
        demand_during_lead = forecast['forecast'].iloc[:lead_time_days].sum()
        
        # Safety stock based on forecast uncertainty
        avg_daily = forecast['forecast'].mean()
        safety_stock = avg_daily * safety_stock_multiplier * np.sqrt(lead_time_days)
        
        # Reorder point
        reorder_point = demand_during_lead + safety_stock
        
        # Days until stockout
        cumulative_demand = forecast['forecast'].cumsum()
        days_until_stockout = len(cumulative_demand[cumulative_demand <= current_stock])
        
        # Recommendation
        should_reorder = current_stock <= reorder_point
        order_quantity = max(0, reorder_point - current_stock + (avg_daily * 14))  # 2 weeks buffer
        
        return {
            'current_stock': current_stock,
            'reorder_point': round(reorder_point),
            'safety_stock': round(safety_stock),
            'should_reorder': should_reorder,
            'recommended_order_qty': round(order_quantity),
            'days_until_stockout': days_until_stockout,
            'avg_daily_demand': round(avg_daily, 1),
            'demand_during_lead_time': round(demand_during_lead)
        }
    
    def to_dict(self, forecast: pd.DataFrame) -> List[Dict]:
        """Convert forecast DataFrame to JSON-serializable format"""
        result = []
        for _, row in forecast.iterrows():
            result.append({
                'date': row['date'].isoformat() if hasattr(row['date'], 'isoformat') else str(row['date']),
                'forecast': round(row['forecast'], 2),
                'lower_bound': round(row['lower_bound'], 2),
                'upper_bound': round(row['upper_bound'], 2)
            })
        return result
