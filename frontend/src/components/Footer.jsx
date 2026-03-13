/**
 * Footer Component - Displays project information.
 *
 * React concepts: Functional component, JSX
 * ES6: Arrow function, const
 */

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
          <p>AI Web Content Analyzer &mdash; UE 6.5 Projet Tutor&eacute;</p>
          <p>Licence Professionnelle LPDWCA &mdash; Universit&eacute; de Strasbourg</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
