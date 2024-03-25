import React from 'react'

export default function UploadInput (props) {
  return (
      <div>
          <input {...props} className="text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none p-2" type="file" />
      </div>
  )
}
