import React from 'react'

export default function TableInformation ({ fileName, numberOfRecords }) {
  return (
      <div className="pb-4">
          <h1 className="font-medium text-lg">{fileName}</h1>
          <p className="text-sm">Contains <span className="font-bold">{numberOfRecords}</span> rows</p>
      </div>
  )
};
