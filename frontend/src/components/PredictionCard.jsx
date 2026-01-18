import React from 'react'
import './PredictionCard.css'

const PredictionCard = ({ prediction }) => {
  if (!prediction) {
    return <div className="no-data">No prediction available</div>
  }

  const predictedPrice = parseFloat(prediction.predicted_price || 0)
  const currentPrice = parseFloat(prediction.current_price || 0)
  const expectedChange = predictedPrice - currentPrice
  const expectedChangePercent = currentPrice !== 0 ? ((expectedChange / currentPrice) * 100).toFixed(2) : 0
  const confidence = parseFloat(prediction.confidence || 0) * 100

  return (
    <div className="prediction-card">
      <div className="prediction-price">
        <div className="predicted-value">${predictedPrice.toFixed(2)}</div>
        <div className="prediction-label">Predicted Price</div>
      </div>
      <div className="prediction-details">
        <div className="detail-item">
          <span className="detail-label">Expected Change:</span>
          <span className={`detail-value ${expectedChange >= 0 ? 'positive' : 'negative'}`}>
            {expectedChange >= 0 ? '+' : ''}
            {expectedChange.toFixed(2)} ({expectedChangePercent}%)
          </span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Confidence:</span>
          <span className="detail-value">{confidence.toFixed(1)}%</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Direction:</span>
          <span className={`detail-value direction ${expectedChange >= 0 ? 'bullish' : 'bearish'}`}>
            {expectedChange >= 0 ? '↑ BULLISH' : '↓ BEARISH'}
          </span>
        </div>
      </div>
      {prediction.model_info && (
        <div className="model-info">
          <div className="model-label">Model: {prediction.model_info}</div>
        </div>
      )}
    </div>
  )
}

export default PredictionCard
