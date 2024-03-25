import classNames from 'classnames'
import React, { useState } from 'react'

import DataViewer from './DataViewer'
import FileUploader from './FileUploader'
import Instructions from './components/Instructions'

function App () {
  const [data, setData] = useState(null)

  const handleFileUpload = (fileData) => {
    const parsedData = fileData
    setData(parsedData)
  }

  return (
    <div className='font-sans h-full'>
      <div className='flex h-full'>
        <div className={classNames('p-4 border h-full shadow-xl', data ? 'w-[380px]' : 'flex-1')}>
          <Instructions />
          <FileUploader className onSuccess={handleFileUpload} />
        </div>
        {data && (
          <div className='flex-1 p-4 overflow-x-scroll'>
            <DataViewer sheetId={data.id} />
          </div>
        )}
      </div>
    </div >
  )
}

export default App
