"""
Forecasting Models for Inventory Prediction
Optimized for medium-sized datasets (1000-100000 records)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class BaseModel(ABC):
    """Abstract base class for forecasting models"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_fitted = False
        self.model = None
    
    @abstractmethod
    def fit(self, df: pd.DataFrame) -> None:
        """Train the model on historical data"""
        pass
    
    @abstractmethod
    def predict(self, periods: int) -> pd.DataFrame:
        """Generate predictions for future periods"""
        pass
    
    def validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and prepare input data"""
        required_cols = ['ds', 'y']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        df = df.copy()
        df['ds'] = pd.to_datetime(df['ds'])
        df['y'] = pd.to_numeric(df['y'], errors='coerce')
        df = df.dropna()
        df = df.sort_values('ds').reset_index(drop=True)
        
        return df


class ProphetModel(BaseModel):
    """
    Facebook Prophet Model
    Best for: Daily data with strong seasonality, holidays, trend changes
    Handles missing data and outliers well
    """
    
    def __init__(self, seasonality_mode: str = 'multiplicative', 
                 yearly_seasonality: bool = True,
                 weekly_seasonality: bool = True,
                 daily_seasonality: bool = False):
        super().__init__('Prophet')
        self.seasonality_mode = seasonality_mode
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.training_data = None
    
    def fit(self, df: pd.DataFrame) -> None:
        """Train Prophet model"""
        try:
            from prophet import Prophet
        except ImportError:
            raise ImportError("Prophet not installed. Run: pip install prophet")
        
        df = self.validate_data(df)
        self.training_data = df
        
        self.model = Prophet(
            seasonality_mode=self.seasonality_mode,
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
            interval_width=0.95
        )
        
        # Suppress Prophet's verbose output
        self.model.fit(df)
        self.is_fitted = True
    
    def predict(self, periods: int) -> pd.DataFrame:
        """Generate forecast for future periods"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        # Return only future predictions
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        result.columns = ['date', 'forecast', 'lower_bound', 'upper_bound']
        result['forecast'] = result['forecast'].clip(lower=0)  # No negative forecasts
        result['lower_bound'] = result['lower_bound'].clip(lower=0)
        
        return result.reset_index(drop=True)
    
    def get_components(self) -> Dict:
        """Get trend and seasonality components"""
        if not self.is_fitted:
            return {}
        
        future = self.model.make_future_dataframe(periods=0)
        forecast = self.model.predict(future)
        
        return {
            'trend': forecast['trend'].values,
            'weekly': forecast.get('weekly', pd.Series([0])).values,
            'yearly': forecast.get('yearly', pd.Series([0])).values
        }


class XGBoostModel(BaseModel):
    """
    XGBoost Gradient Boosting Model
    Best for: Feature-rich data, fast training, high accuracy
    Requires feature engineering for time series
    """
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 6, 
                 learning_rate: float = 0.1, lookback_days: int = 30):
        super().__init__('XGBoost')
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.lookback_days = lookback_days
        self.feature_cols = []
        self.training_data = None
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features for XGBoost"""
        df = df.copy()
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Time features
        df['dayofweek'] = df['ds'].dt.dayofweek
        df['dayofmonth'] = df['ds'].dt.day
        df['month'] = df['ds'].dt.month
        df['quarter'] = df['ds'].dt.quarter
        df['year'] = df['ds'].dt.year
        df['weekofyear'] = df['ds'].dt.isocalendar().week.astype(int)
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
        df['is_month_start'] = df['ds'].dt.is_month_start.astype(int)
        df['is_month_end'] = df['ds'].dt.is_month_end.astype(int)
        
        # Lag features
        for lag in [1, 7, 14, 30]:
            if lag <= len(df):
                df[f'lag_{lag}'] = df['y'].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 30]:
            if window <= len(df):
                df[f'rolling_mean_{window}'] = df['y'].rolling(window=window).mean()
                df[f'rolling_std_{window}'] = df['y'].rolling(window=window).std()
        
        # Fill NaN values from lagging
        df = df.fillna(method='bfill').fillna(0)
        
        self.feature_cols = [col for col in df.columns if col not in ['ds', 'y']]
        
        return df
    
    def fit(self, df: pd.DataFrame) -> None:
        """Train XGBoost model"""
        try:
            import xgboost as xgb
        except ImportError:
            raise ImportError("XGBoost not installed. Run: pip install xgboost")
        
        df = self.validate_data(df)
        df = self._create_features(df)
        self.training_data = df
        
        X = df[self.feature_cols]
        y = df['y']
        
        self.model = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            objective='reg:squarederror',
            random_state=42
        )
        
        self.model.fit(X, y)
        self.is_fitted = True
    
    def predict(self, periods: int) -> pd.DataFrame:
        """Generate forecast for future periods"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        last_date = self.training_data['ds'].max()
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods)
        
        predictions = []
        current_data = self.training_data.copy()
        
        for date in future_dates:
            # Create row for prediction
            new_row = pd.DataFrame({'ds': [date], 'y': [0]})
            temp_df = pd.concat([current_data[['ds', 'y']], new_row], ignore_index=True)
            temp_df = self._create_features(temp_df)
            
            # Predict
            X_pred = temp_df[self.feature_cols].iloc[-1:].fillna(0)
            pred = max(0, self.model.predict(X_pred)[0])
            predictions.append(pred)
            
            # Update for next iteration
            current_data = pd.concat([current_data, pd.DataFrame({'ds': [date], 'y': [pred]})], ignore_index=True)
        
        result = pd.DataFrame({
            'date': future_dates,
            'forecast': predictions,
            'lower_bound': [max(0, p * 0.85) for p in predictions],
            'upper_bound': [p * 1.15 for p in predictions]
        })
        
        return result
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.is_fitted:
            return {}
        
        importance = dict(zip(self.feature_cols, self.model.feature_importances_))
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))


class EnsembleModel(BaseModel):
    """
    Ensemble of multiple models for robust predictions
    Combines Prophet and XGBoost for best results
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        super().__init__('Ensemble')
        self.models = {
            'prophet': ProphetModel(),
            'xgboost': XGBoostModel()
        }
        self.weights = weights or {'prophet': 0.5, 'xgboost': 0.5}
        self.available_models = []
    
    def fit(self, df: pd.DataFrame) -> None:
        """Train all models in ensemble"""
        df = self.validate_data(df)
        self.available_models = []
        
        for name, model in self.models.items():
            try:
                model.fit(df)
                self.available_models.append(name)
                print(f"  ✓ {name} trained successfully")
            except ImportError as e:
                print(f"  ⚠ {name} skipped: {e}")
            except Exception as e:
                print(f"  ✗ {name} failed: {e}")
        
        if not self.available_models:
            raise ValueError("No models could be trained")
        
        self.is_fitted = True
    
    def predict(self, periods: int) -> pd.DataFrame:
        """Generate ensemble prediction"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        predictions = {}
        
        for name in self.available_models:
            try:
                pred = self.models[name].predict(periods)
                predictions[name] = pred['forecast'].values
            except Exception as e:
                print(f"Warning: {name} prediction failed: {e}")
        
        if not predictions:
            raise ValueError("No predictions could be generated")
        
        # Weighted average
        total_weight = sum(self.weights.get(m, 1.0) for m in predictions.keys())
        ensemble_forecast = np.zeros(periods)
        
        for name, pred in predictions.items():
            weight = self.weights.get(name, 1.0) / total_weight
            ensemble_forecast += weight * pred
        
        # Get date range from first successful model
        first_model = self.available_models[0]
        dates = self.models[first_model].predict(periods)['date'].values
        
        result = pd.DataFrame({
            'date': dates,
            'forecast': ensemble_forecast,
            'lower_bound': ensemble_forecast * 0.9,
            'upper_bound': ensemble_forecast * 1.1
        })
        
        return result


class SimpleMovingAverage(BaseModel):
    """
    Simple Moving Average - Fallback model
    Works without any external dependencies
    """
    
    def __init__(self, window: int = 7):
        super().__init__('SimpleMA')
        self.window = window
        self.last_values = None
        self.last_date = None
    
    def fit(self, df: pd.DataFrame) -> None:
        """Fit by storing recent values"""
        df = self.validate_data(df)
        self.last_values = df['y'].tail(self.window).values
        self.last_date = df['ds'].max()
        self.is_fitted = True
    
    def predict(self, periods: int) -> pd.DataFrame:
        """Predict using moving average"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        predictions = []
        values = list(self.last_values)
        
        for _ in range(periods):
            pred = np.mean(values[-self.window:])
            predictions.append(max(0, pred))
            values.append(pred)
        
        dates = pd.date_range(start=self.last_date + timedelta(days=1), periods=periods)
        
        return pd.DataFrame({
            'date': dates,
            'forecast': predictions,
            'lower_bound': [p * 0.8 for p in predictions],
            'upper_bound': [p * 1.2 for p in predictions]
        })
