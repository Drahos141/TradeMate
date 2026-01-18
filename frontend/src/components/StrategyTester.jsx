import React, { useState } from 'react'
import './StrategyTester.css'

const StrategyTester = ({ symbol }) => {
  const [strategy, setStrategy] = useState('moving_average')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [params, setParams] = useState({
    short_period: 10,
    long_period: 30,
    initial_capital: 10000,
  })

  const handleTest = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/test-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol,
          strategy,
          parameters: params,
        }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error testing strategy:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="strategy-tester">
      <div className="strategy-controls">
        <div className="control-group">
          <label htmlFor="strategy">Strategy:</label>
          <select
            id="strategy"
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
          >
            <option value="moving_average">Moving Average Crossover</option>
            <option value="momentum">Momentum</option>
            <option value="rsi">RSI</option>
          </select>
        </div>

        {strategy === 'moving_average' && (
          <>
            <div className="control-group">
              <label htmlFor="short">Short Period:</label>
              <input
                id="short"
                type="number"
                value={params.short_period}
                onChange={(e) => setParams({ ...params, short_period: parseInt(e.target.value) })}
                min="1"
                max="100"
              />
            </div>
            <div className="control-group">
              <label htmlFor="long">Long Period:</label>
              <input
                id="long"
                type="number"
                value={params.long_period}
                onChange={(e) => setParams({ ...params, long_period: parseInt(e.target.value) })}
                min="1"
                max="200"
              />
            </div>
          </>
        )}

        <div className="control-group">
          <label htmlFor="capital">Initial Capital ($):</label>
          <input
            id="capital"
            type="number"
            value={params.initial_capital}
            onChange={(e) => setParams({ ...params, initial_capital: parseFloat(e.target.value) })}
            min="1000"
            step="1000"
          />
        </div>

        <button onClick={handleTest} disabled={loading} className="test-button">
          {loading ? 'Testing...' : 'Test Strategy'}
        </button>
      </div>

      {results && (
        <div className="strategy-results">
          <h3>Backtest Results</h3>
          <div className="results-grid">
            <div className="result-item">
              <span className="result-label">Final Value:</span>
              <span className={`result-value ${results.total_return >= 0 ? 'positive' : 'negative'}`}>
                ${results.final_value?.toFixed(2) || 'N/A'}
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Total Return:</span>
              <span className={`result-value ${results.total_return >= 0 ? 'positive' : 'negative'}`}>
                {results.total_return?.toFixed(2) || 'N/A'}%
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Max Drawdown:</span>
              <span className="result-value negative">
                {results.max_drawdown?.toFixed(2) || 'N/A'}%
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Sharpe Ratio:</span>
              <span className="result-value">
                {results.sharpe_ratio?.toFixed(2) || 'N/A'}
              </span>
            </div>
            <div className="result-item">
              <span className="result-label">Total Trades:</span>
              <span className="result-value">{results.total_trades || 0}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Win Rate:</span>
              <span className="result-value">
                {results.win_rate ? (results.win_rate * 100).toFixed(2) : '0.00'}%
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default StrategyTester
