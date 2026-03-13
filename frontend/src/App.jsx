/**
 * Main App component with React Router for client-side navigation.
 *
 * ES6 features: import/export modules, arrow functions
 * React concepts: JSX, components composition, React Router
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Footer from './components/Footer.jsx'
import Home from './pages/Home.jsx'
import Results from './pages/Results.jsx'
import History from './pages/History.jsx'
import About from './pages/About.jsx'

const App = () => {
  return (
    <BrowserRouter>
      <div className="bg-gray-50 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results/:id" element={<Results />} />
            <Route path="/history" element={<History />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
