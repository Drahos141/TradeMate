from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

from data_fetcher import DataFetcher
from price_predictor import PricePredictor
from strategy_tester import StrategyTester

app = FastAPI(title="TradeMate API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_fetcher = DataFetcher()
price_predictor = PricePredictor()
strategy_tester = StrategyTester()


class StrategyTestRequest(BaseModel):
    symbol: str
    strategy: str
    parameters: Dict


@app.get("/")
def read_root():
    return {"message": "TradeMate API is running"}


@app.get("/api/market-data/{symbol}")
async def get_market_data(symbol: str):
    """Fetch market data for a given symbol"""
    try:
        data = data_fetcher.get_market_data(symbol)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predict/{symbol}")
async def predict_price(symbol: str):
    """Predict future price for a given symbol"""
    try:
        prediction = price_predictor.predict(symbol)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/test-strategy")
async def test_strategy(request: StrategyTestRequest):
    """Test a trading strategy with backtesting"""
    try:
        results = strategy_tester.test_strategy(
            symbol=request.symbol,
            strategy_type=request.strategy,
            parameters=request.parameters
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
