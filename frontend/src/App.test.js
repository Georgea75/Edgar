import React from 'react'
import { render, fireEvent } from '@testing-library/react'

import '@testing-library/jest-dom/extend-expect'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'

const queryClient = new QueryClient()

describe('App component', () => {
  it('renders without crashing', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>)
  })

  it('displays Instructions and FileUploader initially', () => {
    const { getByText } = render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    )
    expect(getByText('Instructions:')).toBeInTheDocument()
    expect(getByText('Upload a file:')).toBeInTheDocument()
  })

  it('renders DataViewer after successful file upload', () => {
    const { getByText, getByRole } = render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    )
    const fileUploader = getByRole('button', { name: 'Upload' })
    fireEvent.change(fileUploader, { target: { files: [{ name: 'example.csv', type: 'text/csv' }] } })

    expect(getByText('Instructions:')).toBeInTheDocument()
    expect(getByText('Upload a file:')).toBeInTheDocument()
  })
})
