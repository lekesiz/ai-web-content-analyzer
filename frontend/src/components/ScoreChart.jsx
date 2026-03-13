/**
 * ScoreChart Component - Doughnut chart for overall score using Chart.js.
 *
 * THIS IS A CLASS COMPONENT to demonstrate both functional and class patterns.
 * (Course objective: "composing components using functions and classes")
 *
 * React concepts: Class component, constructor, state, setState, render(),
 *                 componentDidMount lifecycle, props via this.props
 * ES6: Class syntax, inheritance (extends), super(), arrow functions,
 *       destructuring, template literals, spread operator
 */
import { Component } from 'react'
import { Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip)

class ScoreChart extends Component {
  // Constructor - initialize state
  constructor(props) {
    super(props)

    // this.state - class component state management
    this.state = {
      animated: false,
      displayScore: 0,
    }
  }

  // Lifecycle method - runs after component mounts to DOM
  componentDidMount() {
    // Animate score from 0 to actual value
    const { score } = this.props
    const duration = 800
    const startTime = Date.now()

    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)

      // Easing function for smooth animation
      const eased = 1 - Math.pow(1 - progress, 3)

      // setState - class component way to update state
      this.setState({
        displayScore: score * eased,
        animated: progress >= 1,
      })

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }

  // Arrow function as class method (auto-binds 'this')
  getColor = (value) => {
    if (value >= 80) return '#22c55e'
    if (value >= 60) return '#eab308'
    if (value >= 40) return '#f97316'
    return '#ef4444'
  }

  // render() method - required in class components
  render() {
    // Destructuring props and state (ES6)
    const { size = 128 } = this.props
    const { displayScore } = this.state

    const color = this.getColor(displayScore)

    // Chart.js data object using spread and computed values
    const data = {
      datasets: [
        {
          data: [displayScore, 100 - displayScore],
          backgroundColor: [color, '#e5e7eb'],
          borderWidth: 0,
          cutout: '75%',
        },
      ],
    }

    const options = {
      responsive: false,
      animation: false,
      plugins: {
        tooltip: { enabled: false },
      },
    }

    return (
      <div className="relative flex flex-col items-center">
        <Doughnut data={data} options={options} width={size} height={size} />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-3xl font-bold" style={{ color }}>
            {displayScore.toFixed(1)}
          </span>
        </div>
      </div>
    )
  }
}

export default ScoreChart
