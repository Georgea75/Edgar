import React, { useState } from 'react'
import { useMutation } from '@tanstack/react-query'

import { createFile } from './api'
import { isFileValid } from './utils'
import Button from './components/Button'
import UploadInput from './components/UploadInput'

function FileUploader ({ onSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const { mutate } = useMutation({
    mutationFn: createFile,
    onSuccess: (data) => {
      onSuccess(data)
    }
  })

  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file && isFileValid(file)) {
      setSelectedFile(file)
    } else {
      setSelectedFile(null)
      alert('Please select a valid CSV or Excel file.')
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      mutate({
        file: selectedFile
      })
    }
  }

  return (
      <div>
          <label className="pb-0">Upload a file:</label>
          <UploadInput type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} />
          <Button onClick={handleUpload} disabled={!selectedFile}>Upload</Button>
      </div>
  )
}

export default FileUploader
