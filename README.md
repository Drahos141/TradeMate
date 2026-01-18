# TradeMate
Trading App in React and Python

A comprehensive trading application with a React dashboard frontend and Python backend for market data analysis, price prediction, and strategy backtesting.

## Features

- **Real-time Market Data**: Fetch current prices, historical data, and market statistics
- **Price Prediction**: ML-based price forecasting using Random Forest models
- **Strategy Backtesting**: Test trading strategies (Moving Average, Momentum, RSI) with historical data
- **Modern Dashboard UI**: Clean, responsive React interface with real-time charts

## Project Structure

```
TradeMate/
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── components/ # Dashboard components
│   │   └── ...
│   └── package.json
├── backend/            # Python FastAPI backend
│   ├── main.py        # API server
│   ├── data_fetcher.py      # Market data fetching
│   ├── price_predictor.py   # ML price prediction
│   ├── strategy_tester.py   # Strategy backtesting
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /api/market-data/{symbol}` - Get market data for a symbol
- `GET /api/predict/{symbol}` - Get price prediction for a symbol
- `POST /api/test-strategy` - Backtest a trading strategy

## Usage

1. Start both the backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)
4. View market data, predictions, and test strategies

## Technologies Used

### Frontend
- React 18
- Vite
- Recharts (for charts)
- Axios (for API calls)

### Backend
- FastAPI
- scikit-learn (ML models)
- yfinance (market data)
- pandas, numpy (data processing)

## License

MIT License