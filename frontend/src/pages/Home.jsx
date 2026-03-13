/**
 * Home Page - URL input form with analysis submission.
 *
 * React concepts: useState hook, event handling, conditional rendering, JSX
 * ES6: Arrow functions, destructuring, template literals, async/await, const/let
 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeUrl, getHistory } from '../services/api.js'
import FeatureCard from '../components/FeatureCard.jsx'
import Notification from '../components/Notification.jsx'

const Home = () => {
  // useState hook for managing form state
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [recentAnalyses, setRecentAnalyses] = useState([])

  const navigate = useNavigate()

  // useEffect to load recent analyses on mount
  useEffect(() => {
    const loadRecent = async () => {
      try {
        const { analyses } = await getHistory({ limit: 5 })
        setRecentAnalyses(analyses)
      } catch {
        // Silently ignore - recent analyses are optional
      }
    }
    loadRecent()
  }, [])

  // Arrow function for form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const result = await analyzeUrl(url)
      if (result.success) {
        // Navigate to results page using template literal
        navigate(`/results/${result.analysis_id}`)
      } else {
        setError(result.error || 'Analysis failed')
      }
    } catch (err) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Arrow function to get score badge color
  const getScoreBadgeClass = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-700'
    if (score >= 60) return 'bg-yellow-100 text-yellow-700'
    if (score >= 40) return 'bg-orange-100 text-orange-700'
    return 'bg-red-100 text-red-700'
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
      {/* Error notification */}
      {error && <Notification message={error} type="error" onClose={() => setError(null)} />}

      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl mb-4">
          Analyze Your Website
        </h1>
        <p className="text-xl text-gray-500 max-w-2xl mx-auto">
          Get AI-powered insights on SEO quality, content readability, and structural improvements for any web page.
        </p>
      </div>

      {/* URL Input Form */}
      <div className="bg-white rounded-2xl shadow-lg p-8 mb-12">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              required
              disabled={loading}
              className="flex-1 px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-xl hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Analyze'
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Feature Cards - using FeatureCard component with props */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard
          title="SEO Analysis"
          description="Title tags, meta descriptions, heading structure, image alt texts, keyword density, and more."
          colorClass="bg-green-100 text-green-600"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          }
        />
        <FeatureCard
          title="Content Quality"
          description="Readability scores, word count, language detection, and content structure evaluation."
          colorClass="bg-blue-100 text-blue-600"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          }
        />
        <FeatureCard
          title="AI Recommendations"
          description="GPT-powered suggestions for content improvement, SEO optimization, and best practices."
          colorClass="bg-purple-100 text-purple-600"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
        />
      </div>

      {/* Recent Analyses - conditional rendering */}
      {recentAnalyses.length > 0 && (
        <div className="mt-12">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Analyses</h2>
          <div className="space-y-3">
            {recentAnalyses.map((analysis) => (
              <div
                key={analysis.id}
                onClick={() => navigate(`/results/${analysis.id}`)}
                className="bg-white rounded-lg shadow-sm p-4 flex justify-between items-center cursor-pointer hover:shadow-md transition"
              >
                <div>
                  <p className="text-gray-900 font-medium truncate max-w-md">{analysis.url}</p>
                  <p className="text-gray-400 text-xs">
                    {analysis.timestamp ? new Date(analysis.timestamp).toLocaleDateString() : ''}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreBadgeClass(analysis.overall_score)}`}>
                  {analysis.overall_score?.toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Home
