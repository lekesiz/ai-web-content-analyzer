/**
 * LoadingSpinner Component - Reusable loading indicator.
 *
 * React concepts: Functional component, props, default props
 * ES6: Arrow function, destructuring, default parameters
 */

const LoadingSpinner = ({ message = 'Loading...', size = 'lg' }) => {
  // Destructuring and template literal for dynamic size
  const sizeClass = size === 'lg' ? 'w-12 h-12' : 'w-5 h-5'

  return (
    <div className="text-center py-20">
      <svg
        className={`animate-spin ${sizeClass} text-blue-600 mx-auto mb-4`}
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      <p className="text-gray-500 text-lg">{message}</p>
    </div>
  )
}

export default LoadingSpinner
