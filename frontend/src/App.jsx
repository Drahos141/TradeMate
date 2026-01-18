import React, { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>TradeMate</h1>
        <p>Trading Analytics & Strategy Testing</p>
      </header>
      <Dashboard />
    </div>
  )
}

export default App
