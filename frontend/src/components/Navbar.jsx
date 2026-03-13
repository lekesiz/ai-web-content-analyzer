/**
 * Navbar Component - Navigation bar with links.
 *
 * React concepts: Functional component, JSX, props (via NavLink)
 * ES6: Arrow function, template literals
 */
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  // useLocation hook to highlight active nav link
  const location = useLocation()
  const { pathname } = location

  // Arrow function to determine link styling based on current path
  const linkClass = (path) =>
    `px-3 py-2 rounded-md text-sm font-medium transition ${
      pathname === path
        ? 'text-blue-600 bg-blue-50'
        : 'text-gray-600 hover:text-blue-600'
    }`

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span className="text-xl font-bold text-gray-900">AI Web Analyzer</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/" className={linkClass('/')}>Home</Link>
            <Link to="/history" className={linkClass('/history')}>History</Link>
            <Link to="/about" className={linkClass('/about')}>About</Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
