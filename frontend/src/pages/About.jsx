/**
 * About Page - Project information and technology stack.
 *
 * React concepts: Functional component, JSX, lists with map/key, props
 * ES6: Arrow function, const, destructuring, array of objects
 */

// Technology data as array of objects (ES6 data structure)
const technologies = [
  { name: 'React + Vite', description: 'Frontend Framework' },
  { name: 'Python / Flask', description: 'Backend Framework' },
  { name: 'BeautifulSoup', description: 'Web Scraping' },
  { name: 'OpenAI GPT', description: 'AI Analysis' },
  { name: 'SQLite', description: 'Database' },
  { name: 'Tailwind CSS', description: 'UI Styling' },
  { name: 'Chart.js', description: 'Data Visualization' },
]

// Steps data using array of objects with spread-friendly structure
const steps = [
  { number: 1, title: 'Enter URL', description: 'Provide the URL of any web page you want to analyze.' },
  { number: 2, title: 'Automated Analysis', description: 'The system scrapes, parses, and runs SEO, content, and AI analyses.' },
  { number: 3, title: 'Get Results', description: 'View detailed scores, issues, and AI-powered recommendations.' },
]

const About = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">About This Project</h1>

      {/* Overview */}
      <div className="bg-white rounded-xl shadow-sm p-8 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Overview</h2>
        <p className="text-gray-600 mb-4">
          The AI Web Content Analyzer is a web-based system that automatically analyzes website content
          and provides insights related to SEO quality, readability, and content structure.
        </p>
        <p className="text-gray-600 mb-4">
          It retrieves webpage content, analyzes it using natural language processing techniques and AI,
          then generates actionable recommendations to improve the visibility and quality of the content.
        </p>
        <div className="bg-blue-50 rounded-lg p-4 mt-4">
          <p className="text-blue-800 text-sm">
            <strong>Academic Context:</strong> This project is developed as part of{' '}
            <strong>UE 6.5 &mdash; Projet Tutor&eacute;</strong> for the{' '}
            <strong>Licence Professionnelle LPDWCA</strong> at{' '}
            <strong>Universit&eacute; de Strasbourg</strong>.
          </p>
        </div>
      </div>

      {/* How It Works - using map to render steps */}
      <div className="bg-white rounded-xl shadow-sm p-8 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {steps.map(({ number, title, description }) => (
            <div key={number} className="text-center">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-3 text-xl font-bold">
                {number}
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
              <p className="text-gray-500 text-sm">{description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Technologies - using map to render tech stack */}
      <div className="bg-white rounded-xl shadow-sm p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Technologies Used</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {technologies.map(({ name, description }) => (
            <div key={name} className="bg-gray-50 rounded-lg p-3 text-center">
              <p className="font-medium text-gray-900">{name}</p>
              <p className="text-gray-500 text-xs">{description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Author */}
      <div className="mt-8 text-center text-gray-500 text-sm">
        <p>Developed by <strong>Mikail Lekesiz</strong></p>
        <p>Licence Professionnelle LPDWCA &mdash; Universit&eacute; de Strasbourg</p>
      </div>
    </div>
  )
}

export default About
