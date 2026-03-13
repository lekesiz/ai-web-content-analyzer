/**
 * ScoreChart Component - Doughnut chart for overall score using Chart.js.
 *
 * React concepts: Functional component, props, JSX
 * ES6: Arrow function, destructuring, spread operator, const/let
 */
import { Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip)

const ScoreChart = ({ score, size = 128 }) => {
  // Determine color based on score range
  const getColor = (value) => {
    if (value >= 80) return '#22c55e'
    if (value >= 60) return '#eab308'
    if (value >= 40) return '#f97316'
    return '#ef4444'
  }

  const color = getColor(score)

  // Chart.js data object using spread and computed values
  const data = {
    datasets: [
      {
        data: [score, 100 - score],
        backgroundColor: [color, '#e5e7eb'],
        borderWidth: 0,
        cutout: '75%',
      },
    ],
  }

  const options = {
    responsive: false,
    plugins: {
      tooltip: { enabled: false },
    },
  }

  return (
    <div className="relative flex flex-col items-center">
      <Doughnut data={data} options={options} width={size} height={size} />
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-3xl font-bold" style={{ color }}>
          {score.toFixed(1)}
        </span>
      </div>
    </div>
  )
}

export default ScoreChart
