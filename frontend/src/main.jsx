/**
 * Entry point for the React application.
 * Uses ReactDOM.createRoot (React 18+) to render the App component.
 *
 * ES6 features used: import/export modules
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom'
import App from './App.jsx'

// React 18+ createRoot API - renders the root component
const root = createRoot(document.getElementById('root'))
root.render(
  <StrictMode>
    <App />
  </StrictMode>
)
