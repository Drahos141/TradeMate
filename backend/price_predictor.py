import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any
import warnings

from data_fetcher import DataFetcher

warnings.filterwarnings('ignore')


class PricePredictor:
    """Predicts future stock prices using machine learning"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _calculate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators as features"""
        features_df = df.copy()
        
        # Moving averages
        features_df['MA5'] = features_df['Close'].rolling(window=5).mean()
        features_df['MA10'] = features_df['Close'].rolling(window=10).mean()
        features_df['MA20'] = features_df['Close'].rolling(window=20).mean()
        features_df['MA50'] = features_df['Close'].rolling(window=50).mean()
        
        # Price changes
        features_df['PriceChange'] = features_df['Close'].pct_change()
        features_df['HighLowRatio'] = features_df['High'] / features_df['Low']
        features_df['CloseOpenRatio'] = features_df['Close'] / features_df['Open']
        
        # Volume indicators
        features_df['VolumeMA'] = features_df['Volume'].rolling(window=10).mean()
        features_df['VolumeRatio'] = features_df['Volume'] / features_df['VolumeMA']
        
        # Volatility
        features_df['Volatility'] = features_df['Close'].rolling(window=10).std()
        
        # RSI calculation
        delta = features_df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        features_df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = features_df['Close'].ewm(span=12).mean()
        ema26 = features_df['Close'].ewm(span=26).mean()
        features_df['MACD'] = ema12 - ema26
        features_df['MACD_Signal'] = features_df['MACD'].ewm(span=9).mean()
        
        return features_df
    
    def _prepare_data(self, df: pd.DataFrame, lookback: int = 5) -> tuple:
        """Prepare features and target for model training"""
        df_features = self._calculate_features(df)
        
        # Select feature columns
        feature_columns = [
            'MA5', 'MA10', 'MA20', 'MA50',
            'PriceChange', 'HighLowRatio', 'CloseOpenRatio',
            'VolumeRatio', 'Volatility', 'RSI', 'MACD', 'MACD_Signal'
        ]
        
        X = []
        y = []
        
        # Create sequences
        for i in range(lookback, len(df_features) - 1):
            # Get lookback window of features
            window = df_features.iloc[i-lookback:i][feature_columns].values
            if not np.isnan(window).any():
                X.append(window.flatten())
                # Target: next day's close price
                y.append(df_features.iloc[i+1]['Close'])
        
        return np.array(X), np.array(y)
    
    def predict(self, symbol: str, days_ahead: int = 1) -> Dict[str, Any]:
        """
        Predict future price for a given symbol
        
        Args:
            symbol: Stock ticker symbol
            days_ahead: Number of days ahead to predict (default: 1)
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Fetch historical data
            df = self.data_fetcher.get_historical_data(symbol, period="1y")
            
            if len(df) < 60:
                raise Exception(f"Insufficient data for {symbol}. Need at least 60 days of history.")
            
            # Prepare data
            X, y = self._prepare_data(df)
            
            if len(X) == 0:
                raise Exception("Could not prepare features. Check data quality.")
            
            # Train model
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            # Make prediction using most recent data
            recent_features = self._calculate_features(df)
            feature_columns = [
                'MA5', 'MA10', 'MA20', 'MA50',
                'PriceChange', 'HighLowRatio', 'CloseOpenRatio',
                'VolumeRatio', 'Volatility', 'RSI', 'MACD', 'MACD_Signal'
            ]
            
            lookback = 5
            if len(recent_features) < lookback + 1:
                raise Exception("Insufficient recent data for prediction")
            
            # Get the last lookback window
            last_window = recent_features.iloc[-lookback:][feature_columns].values
            if np.isnan(last_window).any():
                # Fill NaN with forward fill
                last_window = pd.DataFrame(last_window, columns=feature_columns).ffill().fillna(0).values
            
            X_pred = last_window.flatten().reshape(1, -1)
            X_pred_scaled = self.scaler.transform(X_pred)
            
            predicted_price = self.model.predict(X_pred_scaled)[0]
            current_price = float(df['Close'].iloc[-1])
            
            # Calculate confidence based on model uncertainty (using std of tree predictions)
            tree_predictions = [tree.predict(X_pred_scaled)[0] for tree in self.model.estimators_]
            confidence_std = np.std(tree_predictions)
            confidence = max(0, min(1, 1 - (confidence_std / current_price)))
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'predicted_price': float(predicted_price),
                'confidence': float(confidence),
                'model_info': 'Random Forest (100 trees)'
            }
            
        except Exception as e:
            raise Exception(f"Error predicting price for {symbol}: {str(e)}")
