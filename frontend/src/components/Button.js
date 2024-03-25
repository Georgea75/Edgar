import React from 'react'

export default function Button ({ children, ...props }) {
  return (
    <button {...props} className="h-8 px-4 m-2 text-sm text-gray-100 transition-colors duration-150 bg-gray-700 rounded-lg focus:shadow-outline hover:bg-gray-800 cursor-pointer">{children}</button>
  )
}
