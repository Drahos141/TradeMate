import React from 'react'
import './MarketData.css'

const MarketData = ({ data }) => {
  if (!data) {
    return <div className="no-data">No market data available</div>
  }

  const currentPrice = parseFloat(data.current_price || 0)
  const previousClose = parseFloat(data.previous_close || 0)
  const change = currentPrice - previousClose
  const changePercent = previousClose !== 0 ? ((change / previousClose) * 100).toFixed(2) : 0

  return (
    <div className="market-data">
      <div className="price-display">
        <div className="current-price">${currentPrice.toFixed(2)}</div>
        <div className={`price-change ${change >= 0 ? 'positive' : 'negative'}`}>
          {change >= 0 ? '+' : ''}
          {change.toFixed(2)} ({changePercent}%)
        </div>
      </div>
      <div className="data-grid">
        <div className="data-item">
          <span className="label">Previous Close:</span>
          <span className="value">${previousClose.toFixed(2)}</span>
        </div>
        <div className="data-item">
          <span className="label">Volume:</span>
          <span className="value">{data.volume?.toLocaleString() || 'N/A'}</span>
        </div>
        <div className="data-item">
          <span className="label">Market Cap:</span>
          <span className="value">{data.market_cap ? `$${(data.market_cap / 1e9).toFixed(2)}B` : 'N/A'}</span>
        </div>
        <div className="data-item">
          <span className="label">52 Week High:</span>
          <span className="value">${data.year_high?.toFixed(2) || 'N/A'}</span>
        </div>
        <div className="data-item">
          <span className="label">52 Week Low:</span>
          <span className="value">${data.year_low?.toFixed(2) || 'N/A'}</span>
        </div>
      </div>
    </div>
  )
}

export default MarketData
