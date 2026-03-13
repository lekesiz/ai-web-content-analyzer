/**
 * API Service Module - handles all communication with the Flask backend.
 *
 * ES6 features used:
 * - Arrow functions
 * - Template literals
 * - Destructuring
 * - Async/await
 * - Default parameters
 * - Modules (import/export)
 */

// Base URL - empty string means same origin (works with Vite proxy in dev, Flask in prod)
const API_BASE = '/api'

/**
 * Generic fetch wrapper with error handling.
 * Uses arrow function and template literals.
 */
const fetchJSON = async (url, options = {}) => {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.error || `Request failed with status ${response.status}`)
  }

  return response.json()
}

/**
 * Submit a URL for analysis.
 * @param {string} url - The URL to analyze
 * @returns {Promise<object>} Analysis result with analysis_id
 */
export const analyzeUrl = async (url) => {
  const data = await fetchJSON('/analyze', {
    method: 'POST',
    body: JSON.stringify({ url }),
  })
  return data
}

/**
 * Get analysis results by ID.
 * Uses template literal for dynamic URL.
 */
export const getAnalysis = async (analysisId) => {
  const data = await fetchJSON(`/analysis/${analysisId}`)
  return data
}

/**
 * Delete an analysis by ID.
 */
export const deleteAnalysis = async (analysisId) => {
  const data = await fetchJSON(`/analysis/${analysisId}`, {
    method: 'DELETE',
  })
  return data
}

/**
 * Get paginated analysis history.
 * Destructuring used for parameters with defaults.
 */
export const getHistory = async ({ page = 1, limit = 20, sort = 'timestamp', order = 'desc', search = '' } = {}) => {
  const params = new URLSearchParams({ page, limit, sort, order, search })
  const data = await fetchJSON(`/history?${params}`)
  return data
}

/**
 * Get export URL for JSON download.
 */
export const getExportJsonUrl = (analysisId) => `${API_BASE}/analysis/${analysisId}/export/json`

/**
 * Get export URL for PDF download.
 */
export const getExportPdfUrl = (analysisId) => `${API_BASE}/analysis/${analysisId}/export/pdf`
