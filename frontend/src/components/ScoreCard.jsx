/**
 * ScoreCard Component - Displays a score with progress bar.
 *
 * React concepts: Functional component, props, conditional rendering
 * ES6: Arrow function, destructuring, template literals, ternary operator
 */

const ScoreCard = ({ title, score, showBar = true }) => {
  // Arrow function for score color based on value
  const getScoreColor = (value) => {
    if (value >= 80) return { text: 'text-green-600', bar: 'bg-green-500' }
    if (value >= 60) return { text: 'text-yellow-600', bar: 'bg-yellow-500' }
    if (value >= 40) return { text: 'text-orange-500', bar: 'bg-orange-500' }
    return { text: 'text-red-500', bar: 'bg-red-500' }
  }

  // Destructuring the color object
  const { text: textColor, bar: barColor } = getScoreColor(score)

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-sm font-medium text-gray-500 mb-2">{title}</h3>
      <div className={`text-3xl font-bold mb-2 ${textColor}`}>
        {score !== null && score !== undefined ? score.toFixed(1) : 'N/A'}
      </div>
      {showBar && (
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-500 ${barColor}`}
            style={{ width: `${Math.min(score || 0, 100)}%` }}
          />
        </div>
      )}
    </div>
  )
}

export default ScoreCard
