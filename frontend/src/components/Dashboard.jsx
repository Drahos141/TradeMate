import React, { useState, useEffect } from 'react'
import PriceChart from './PriceChart'
import PredictionCard from './PredictionCard'
import StrategyTester from './StrategyTester'
import MarketData from './MarketData'
import './Dashboard.css'

const Dashboard = () => {
  const [symbol, setSymbol] = useState('AAPL')
  const [marketData, setMarketData] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchMarketData()
  }, [symbol])

  const fetchMarketData = async () => {
    setLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/market-data/${symbol}`)
      const data = await response.json()
      setMarketData(data)
      
      // Fetch prediction when market data is loaded
      const predResponse = await fetch(`http://localhost:8000/api/predict/${symbol}`)
      const predData = await predResponse.json()
      setPrediction(predData)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <div className="dashboard-controls">
        <div className="symbol-selector">
          <label htmlFor="symbol">Symbol:</label>
          <input
            id="symbol"
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            onKeyPress={(e) => e.key === 'Enter' && fetchMarketData()}
            placeholder="Enter stock symbol"
          />
          <button onClick={fetchMarketData} disabled={loading}>
            {loading ? 'Loading...' : 'Update'}
          </button>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card chart-card">
          <h2>Price Chart</h2>
          {marketData ? (
            <PriceChart data={marketData} />
          ) : (
            <div className="loading">Loading chart data...</div>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Market Data</h2>
          {marketData ? (
            <MarketData data={marketData} />
          ) : (
            <div className="loading">Loading market data...</div>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Price Prediction</h2>
          {prediction ? (
            <PredictionCard prediction={prediction} />
          ) : (
            <div className="loading">Loading prediction...</div>
          )}
        </div>

        <div className="dashboard-card strategy-card">
          <h2>Strategy Tester</h2>
          <StrategyTester symbol={symbol} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
