/**
 * Notification Component - Toast-style notification.
 *
 * React concepts: Functional component, props, useState, useEffect, conditional rendering
 * ES6: Arrow function, destructuring, template literals, ternary, setTimeout
 */
import { useState, useEffect } from 'react'

const Notification = ({ message, type = 'info', onClose }) => {
  const [visible, setVisible] = useState(true)

  // useEffect to auto-dismiss after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      if (onClose) onClose()
    }, 5000)

    // Cleanup function (component unmount)
    return () => clearTimeout(timer)
  }, [onClose])

  if (!visible) return null

  // Template literal for dynamic styling based on notification type
  const bgColor = type === 'error' ? 'bg-red-50 border-red-400 text-red-700'
    : type === 'success' ? 'bg-green-50 border-green-400 text-green-700'
    : 'bg-blue-50 border-blue-400 text-blue-700'

  return (
    <div className={`fixed top-20 right-4 z-50 border-l-4 p-4 rounded-lg shadow-lg max-w-md ${bgColor}`}>
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium">{message}</p>
        <button
          onClick={() => { setVisible(false); if (onClose) onClose() }}
          className="ml-4 text-gray-400 hover:text-gray-600"
        >
          &times;
        </button>
      </div>
    </div>
  )
}

export default Notification
