import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import './PriceChart.css'

const PriceChart = ({ data }) => {
  if (!data || !data.historical_data) {
    return <div className="no-data">No chart data available</div>
  }

  // Format data for the chart
  const chartData = data.historical_data
    .slice()
    .reverse()
    .map((item) => ({
      date: new Date(item.Date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      price: parseFloat(item.Close),
    }))

  return (
    <div className="price-chart">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e2746" />
          <XAxis dataKey="date" stroke="#9ca3af" style={{ fontSize: '12px' }} />
          <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1f3a',
              border: '1px solid #1e2746',
              borderRadius: '6px',
              color: '#e0e0e0',
            }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#4facfe"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PriceChart
