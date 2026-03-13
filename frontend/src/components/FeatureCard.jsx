/**
 * FeatureCard Component - Displays a feature with icon, title, description.
 *
 * React concepts: Functional component, props, children
 * ES6: Arrow function, destructuring
 */

const FeatureCard = ({ icon, title, description, colorClass }) => {
  // Destructured props used directly in JSX
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 text-center">
      <div className={`w-12 h-12 ${colorClass} rounded-full flex items-center justify-center mx-auto mb-4`}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 text-sm">{description}</p>
    </div>
  )
}

export default FeatureCard
