import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime

from data_fetcher import DataFetcher


class StrategyTester:
    """Backtests trading strategies on historical data"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def _calculate_moving_averages(self, df: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:
        """Calculate moving averages"""
        df = df.copy()
        df['MA_Short'] = df['Close'].rolling(window=short_period).mean()
        df['MA_Long'] = df['Close'].rolling(window=long_period).mean()
        return df
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate RSI indicator"""
        df = df.copy()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    def _moving_average_strategy(self, df: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:
        """Moving Average Crossover Strategy"""
        df = self._calculate_moving_averages(df, short_period, long_period)
        df['Signal'] = 0
        
        # Generate buy signals when short MA crosses above long MA
        df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1
        df.loc[df['MA_Short'] < df['MA_Long'], 'Signal'] = -1
        
        # Generate actual trade signals (when signal changes)
        df['Position'] = df['Signal'].diff()
        
        return df
    
    def _momentum_strategy(self, df: pd.DataFrame, period: int = 10) -> pd.DataFrame:
        """Momentum Strategy based on price changes"""
        df = df.copy()
        df['Momentum'] = df['Close'].pct_change(periods=period)
        df['Signal'] = 0
        
        # Buy when momentum is positive and strong
        df.loc[df['Momentum'] > 0.02, 'Signal'] = 1
        # Sell when momentum is negative
        df.loc[df['Momentum'] < -0.02, 'Signal'] = -1
        
        df['Position'] = df['Signal'].diff()
        return df
    
    def _rsi_strategy(self, df: pd.DataFrame, oversold: int = 30, overbought: int = 70) -> pd.DataFrame:
        """RSI-based Strategy"""
        df = self._calculate_rsi(df)
        df['Signal'] = 0
        
        # Buy when RSI < oversold (oversold condition)
        df.loc[df['RSI'] < oversold, 'Signal'] = 1
        # Sell when RSI > overbought (overbought condition)
        df.loc[df['RSI'] > overbought, 'Signal'] = -1
        
        df['Position'] = df['Signal'].diff()
        return df
    
    def _backtest_strategy(self, df: pd.DataFrame, initial_capital: float = 10000) -> Dict[str, Any]:
        """Run backtest on strategy signals"""
        capital = initial_capital
        shares = 0
        trades = []
        equity_curve = []
        in_position = False
        entry_price = 0
        
        for i, row in df.iterrows():
            position = row.get('Position', 0)
            price = row['Close']
            
            # Buy signal
            if position > 0 and not in_position and capital > 0:
                shares = capital / price
                capital = 0
                in_position = True
                entry_price = price
                trades.append({
                    'type': 'BUY',
                    'date': i,
                    'price': price,
                    'shares': shares
                })
            
            # Sell signal
            elif position < 0 and in_position and shares > 0:
                capital = shares * price
                in_position = False
                exit_price = price
                pnl = (exit_price - entry_price) / entry_price * 100
                trades.append({
                    'type': 'SELL',
                    'date': i,
                    'price': price,
                    'shares': shares,
                    'pnl': pnl
                })
                shares = 0
            
            # Calculate current equity
            current_equity = capital + (shares * price) if in_position else capital
            equity_curve.append(current_equity)
        
        # Final value (sell if still holding)
        if in_position:
            final_price = df['Close'].iloc[-1]
            capital = shares * final_price
            trades.append({
                'type': 'SELL',
                'date': df.index[-1],
                'price': final_price,
                'shares': shares
            })
        
        final_value = capital
        total_return = ((final_value - initial_capital) / initial_capital) * 100
        
        # Calculate metrics
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in trades if t.get('pnl', 0) < 0]
        total_trades = len(winning_trades) + len(losing_trades)
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        # Calculate max drawdown
        equity_array = np.array(equity_curve)
        running_max = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - running_max) / running_max * 100
        max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        returns = pd.Series(equity_curve).pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        return {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'trades': trades[-10:] if trades else []  # Last 10 trades
        }
    
    def test_strategy(self, symbol: str, strategy_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test a trading strategy with backtesting
        
        Args:
            symbol: Stock ticker symbol
            strategy_type: Type of strategy ('moving_average', 'momentum', 'rsi')
            parameters: Strategy parameters
            
        Returns:
            Dictionary with backtest results
        """
        try:
            # Fetch historical data
            df = self.data_fetcher.get_historical_data(symbol, period="1y")
            
            if len(df) < 60:
                raise Exception(f"Insufficient data for {symbol}. Need at least 60 days.")
            
            # Apply strategy
            if strategy_type == 'moving_average':
                short_period = parameters.get('short_period', 10)
                long_period = parameters.get('long_period', 30)
                df = self._moving_average_strategy(df, short_period, long_period)
            
            elif strategy_type == 'momentum':
                period = parameters.get('period', 10)
                df = self._momentum_strategy(df, period)
            
            elif strategy_type == 'rsi':
                oversold = parameters.get('oversold', 30)
                overbought = parameters.get('overbought', 70)
                df = self._rsi_strategy(df, oversold, overbought)
            
            else:
                raise Exception(f"Unknown strategy type: {strategy_type}")
            
            # Run backtest
            initial_capital = parameters.get('initial_capital', 10000)
            results = self._backtest_strategy(df, initial_capital)
            
            # Add strategy info
            results['strategy'] = strategy_type
            results['symbol'] = symbol
            results['parameters'] = parameters
            
            return results
            
        except Exception as e:
            raise Exception(f"Error testing strategy: {str(e)}")
