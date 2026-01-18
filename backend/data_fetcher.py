import yfinance as yf
import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta


class DataFetcher:
    """Handles fetching market data from Yahoo Finance"""
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch comprehensive market data for a symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary containing market data including current price, 
            historical data, volume, etc.
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get historical data (last 30 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=60)
            hist = ticker.history(start=start_date, end=end_date)
            
            # Get current price from latest close or current price
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or float(hist['Close'].iloc[-1])
            previous_close = info.get('previousClose') or float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
            
            # Format historical data
            historical_data = []
            for date, row in hist.iterrows():
                historical_data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                })
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'previous_close': previous_close,
                'volume': info.get('volume', hist['Volume'].iloc[-1] if len(hist) > 0 else 0),
                'market_cap': info.get('marketCap'),
                'year_high': info.get('fiftyTwoWeekHigh'),
                'year_low': info.get('fiftyTwoWeekLow'),
                'historical_data': historical_data,
            }
            
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Get historical price data as DataFrame for analysis
        
        Args:
            symbol: Stock ticker symbol
            period: Period to fetch ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            raise Exception(f"Error fetching historical data for {symbol}: {str(e)}")
