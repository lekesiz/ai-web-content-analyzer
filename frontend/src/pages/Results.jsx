/**
 * Results Page - Displays full analysis results with scores and details.
 *
 * React concepts: useState, useEffect, useParams, conditional rendering, lists with map/key
 * ES6: Arrow functions, destructuring, template literals, spread operator, optional chaining
 */
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getAnalysis, getExportJsonUrl, getExportPdfUrl } from '../services/api.js'
import ScoreCard from '../components/ScoreCard.jsx'
import ScoreChart from '../components/ScoreChart.jsx'
import LoadingSpinner from '../components/LoadingSpinner.jsx'
import Notification from '../components/Notification.jsx'

const Results = () => {
  // useParams hook - gets :id from URL
  const { id } = useParams()
  const navigate = useNavigate()

  // useState hooks for component state management
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // useEffect hook - fetch data when component mounts or id changes
  useEffect(() => {
    const fetchResults = async () => {
      try {
        setLoading(true)
        const data = await getAnalysis(id)
        if (data.success) {
          setAnalysis(data.analysis)
        } else {
          setError(data.error || 'Failed to load results')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [id])

  // Arrow function for issue severity badge color
  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'bg-red-100 text-red-700',
      high: 'bg-orange-100 text-orange-700',
      medium: 'bg-yellow-100 text-yellow-700',
      low: 'bg-blue-100 text-blue-700',
    }
    return colors[severity] || 'bg-gray-100 text-gray-700'
  }

  // Arrow function for priority badge color
  const getPriorityColor = (priority) => {
    const colors = {
      high: 'bg-red-100 text-red-700',
      medium: 'bg-yellow-100 text-yellow-700',
      low: 'bg-green-100 text-green-700',
    }
    return colors[priority] || 'bg-gray-100 text-gray-700'
  }

  // Loading state
  if (loading) return <LoadingSpinner message="Loading analysis results..." />

  // Error state
  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <Notification message={error} type="error" />
        <button
          onClick={() => navigate('/')}
          className="mt-8 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Go Home
        </button>
      </div>
    )
  }

  if (!analysis) return null

  // Destructuring the analysis object (ES6 destructuring)
  const {
    url,
    overall_score,
    seo_score,
    content_score,
    technical_score,
    page_title,
    word_count,
    language,
    response_time,
    timestamp,
    seo_details,
    ai_recommendations,
  } = analysis

  // Parse issues from seo_details (using optional chaining)
  let issues = []
  try {
    issues = seo_details?.issues_json ? JSON.parse(seo_details.issues_json) : []
  } catch {
    issues = []
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-1">Analysis Results</h1>
          <p className="text-gray-500 text-sm break-all">{url}</p>
          <p className="text-gray-400 text-xs mt-1">
            {timestamp ? new Date(timestamp).toLocaleString() : ''}
          </p>
        </div>
        <div className="flex gap-2 mt-4 sm:mt-0">
          <a
            href={getExportJsonUrl(id)}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium transition"
          >
            Export JSON
          </a>
          <a
            href={getExportPdfUrl(id)}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium transition"
          >
            Export PDF
          </a>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition"
          >
            New Analysis
          </button>
        </div>
      </div>

      {/* Score Overview - 4 column grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm p-6 flex flex-col items-center">
          <h3 className="text-sm font-medium text-gray-500 mb-3">Overall Score</h3>
          <ScoreChart score={overall_score || 0} />
        </div>
        <ScoreCard title="SEO Score" score={seo_score} />
        <ScoreCard title="Content Score" score={content_score} />
        <ScoreCard title="Technical Score" score={technical_score} />
      </div>

      {/* Page Info */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Page Information</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Title', value: page_title || 'N/A' },
            { label: 'Words', value: word_count || 0 },
            { label: 'Language', value: language || 'Unknown' },
            { label: 'Response Time', value: `${(response_time || 0).toFixed(2)}s` },
          ].map(({ label, value }) => (
            <div key={label} className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">{label}</p>
              <p className="text-sm font-medium text-gray-900 truncate">{value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* SEO Details */}
      {seo_details && (
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">SEO Analysis Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Spread operator to create detail items array */}
            {[
              { label: 'Title Tag', score: seo_details.title_score, detail: `${seo_details.title_length} characters` },
              { label: 'Meta Description', score: seo_details.meta_desc_score, detail: `${seo_details.meta_desc_length} characters` },
              { label: 'Headings', score: seo_details.headings_score, detail: `H1: ${seo_details.h1_count}, H2: ${seo_details.h2_count}` },
              { label: 'Images', score: seo_details.images_score, detail: `${seo_details.img_total} total, ${seo_details.img_without_alt} without alt` },
              { label: 'Links', score: seo_details.links_score, detail: `Internal: ${seo_details.internal_links}, External: ${seo_details.external_links}` },
              { label: 'URL Structure', score: seo_details.url_score, detail: 'URL quality analysis' },
              { label: 'Canonical', score: seo_details.has_canonical ? 100 : 0, detail: seo_details.has_canonical ? 'Present' : 'Missing' },
              { label: 'Open Graph', score: seo_details.has_og_tags ? 100 : 0, detail: seo_details.has_og_tags ? 'Present' : 'Missing' },
            ].map(({ label, score, detail }) => (
              <div key={label} className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
                <div>
                  <p className="font-medium text-gray-900">{label}</p>
                  <p className="text-xs text-gray-500">{detail}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  score >= 80 ? 'bg-green-100 text-green-700'
                  : score >= 50 ? 'bg-yellow-100 text-yellow-700'
                  : 'bg-red-100 text-red-700'
                }`}>
                  {score}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Issues */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Issues Found</h2>
        {issues.length > 0 ? (
          <div className="space-y-3">
            {issues.map((issue, index) => (
              <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-gray-50">
                <span className={`px-2 py-0.5 rounded text-xs font-medium mt-0.5 ${getSeverityColor(issue.severity)}`}>
                  {issue.severity}
                </span>
                <p className="text-sm text-gray-700">{issue.message}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No issues found. Great job!</p>
        )}
      </div>

      {/* AI Recommendations */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Recommendations</h2>
        {ai_recommendations && ai_recommendations.length > 0 ? (
          <div className="space-y-4">
            {ai_recommendations.map((rec, index) => (
              <div key={index} className="border border-gray-100 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(rec.priority)}`}>
                    {rec.priority}
                  </span>
                  <span className="px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600">
                    {rec.category}
                  </span>
                </div>
                <h3 className="font-medium text-gray-900 mb-1">{rec.title}</h3>
                <p className="text-sm text-gray-600">{rec.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">
            AI analysis not available. Set OPENAI_API_KEY to enable.
          </p>
        )}
      </div>
    </div>
  )
}

export default Results
