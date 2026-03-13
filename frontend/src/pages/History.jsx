/**
 * History Page - Browse, search, and manage past analyses.
 *
 * React concepts: useState, useEffect, event handling, lists with map/key, conditional rendering
 * ES6: Arrow functions, destructuring, template literals, spread operator, async/await
 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getHistory, deleteAnalysis } from '../services/api.js'
import LoadingSpinner from '../components/LoadingSpinner.jsx'
import Notification from '../components/Notification.jsx'

const History = () => {
  // Multiple useState hooks for different state pieces
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [sortField, setSortField] = useState('timestamp')
  const [sortOrder, setSortOrder] = useState('desc')
  const [notification, setNotification] = useState(null)

  const navigate = useNavigate()
  const perPage = 20

  // useEffect - fetches data when search, page, sort changes
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true)
        // Destructuring the response
        const { analyses: data, total: count } = await getHistory({
          page,
          limit: perPage,
          sort: sortField,
          order: sortOrder,
          search,
        })
        setAnalyses(data)
        setTotal(count)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [search, page, sortField, sortOrder])

  // Arrow function for sorting
  const handleSort = (field) => {
    if (sortField === field) {
      // Toggle order if same field
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortOrder('desc')
    }
    setPage(1)
  }

  // Arrow function for search with debounce effect
  const handleSearch = (e) => {
    setSearch(e.target.value)
    setPage(1)
  }

  // Arrow function for delete
  const handleDelete = async (e, analysisId) => {
    e.stopPropagation()
    if (!confirm('Are you sure you want to delete this analysis?')) return

    try {
      await deleteAnalysis(analysisId)
      // Update state: filter out deleted item (using spread/filter)
      setAnalyses(analyses.filter((a) => a.id !== analysisId))
      setTotal(total - 1)
      setNotification({ message: 'Analysis deleted', type: 'success' })
    } catch (err) {
      setNotification({ message: err.message, type: 'error' })
    }
  }

  // Arrow function for score badge color
  const getScoreBadge = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-700'
    if (score >= 60) return 'bg-yellow-100 text-yellow-700'
    if (score >= 40) return 'bg-orange-100 text-orange-700'
    return 'bg-red-100 text-red-700'
  }

  // Calculate total pages
  const totalPages = Math.ceil(total / perPage)

  // Arrow function for sort indicator
  const sortIcon = (field) => {
    if (sortField !== field) return ''
    return sortOrder === 'asc' ? ' ↑' : ' ↓'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      {/* Notification */}
      {notification && (
        <Notification
          message={notification.message}
          type={notification.type}
          onClose={() => setNotification(null)}
        />
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Analysis History</h1>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition"
        >
          New Analysis
        </button>
      </div>

      {/* Search Input */}
      <div className="mb-6">
        <input
          type="text"
          value={search}
          onChange={handleSearch}
          placeholder="Search by URL..."
          className="w-full sm:w-96 px-4 py-2 border border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
        />
      </div>

      {/* Loading */}
      {loading ? (
        <LoadingSpinner message="Loading history..." />
      ) : analyses.length === 0 ? (
        /* Empty State */
        <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-400">
          <p>
            No analyses yet.{' '}
            <button onClick={() => navigate('/')} className="text-blue-600 hover:underline">
              Start your first analysis
            </button>
          </p>
        </div>
      ) : (
        <>
          {/* Table */}
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    onClick={() => handleSort('url')}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  >
                    URL{sortIcon('url')}
                  </th>
                  <th
                    onClick={() => handleSort('overall_score')}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  >
                    Score{sortIcon('overall_score')}
                  </th>
                  <th
                    onClick={() => handleSort('timestamp')}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700"
                  >
                    Date{sortIcon('timestamp')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analyses.map((item) => (
                  <tr
                    key={item.id}
                    onClick={() => navigate(`/results/${item.id}`)}
                    className="hover:bg-gray-50 cursor-pointer transition"
                  >
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                      {item.url}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getScoreBadge(item.overall_score)}`}>
                        {item.overall_score?.toFixed(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {item.timestamp ? new Date(item.timestamp).toLocaleDateString() : ''}
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full font-medium">
                        {item.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={(e) => handleDelete(e, item.id)}
                        className="text-red-400 hover:text-red-600 text-sm transition"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center mt-6 gap-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="px-3 py-1 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 text-sm"
              >
                Previous
              </button>
              {/* Generate page buttons using Array spread */}
              {[...Array(totalPages)].map((_, i) => (
                <button
                  key={i + 1}
                  onClick={() => setPage(i + 1)}
                  className={`px-3 py-1 rounded text-sm ${
                    page === i + 1
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
              <button
                onClick={() => setPage(Math.min(totalPages, page + 1))}
                disabled={page === totalPages}
                className="px-3 py-1 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 text-sm"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default History
