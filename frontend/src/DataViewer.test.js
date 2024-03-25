import React from 'react'
import { render, waitFor } from '@testing-library/react'
import DataViewer from './DataViewer'
import {
  QueryClient,
  QueryClientProvider
} from '@tanstack/react-query'

import { fetchSupportedTypes, fetchSheet } from './api'

const queryClient = new QueryClient()

jest.mock('./api', () => ({
  fetchSupportedTypes: jest.fn(),
  fetchSheet: jest.fn(),
  updateColumnType: jest.fn()
}))

describe('<DataViewer />', () => {
  beforeEach(() => {
    fetchSupportedTypes.mockResolvedValue({ supported_types: ['type1', 'type2'] })
    fetchSheet.mockResolvedValue({ rows: [], file_name: 'test.xlsx', columns: [{ id: '1', name: 'Column1', data_type: 'type1' }], number_of_records: 0 })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  it('renders without crashing', () => {
    render(
          <QueryClientProvider client={queryClient}>
              <DataViewer sheetId="testSheetId" />
          </QueryClientProvider>
    )
  })

  it('fetches supported types and sheet data on mount', async () => {
    render(
          <QueryClientProvider client={queryClient}>
              <DataViewer sheetId="testSheetId" />
          </QueryClientProvider>
    )
    expect(fetchSupportedTypes).toHaveBeenCalled()
    expect(fetchSheet).toHaveBeenCalledWith({ sheetId: 'testSheetId', pageIndex: 0, pageSize: 10 })
    await waitFor(() => expect(fetchSheet).toHaveBeenCalledTimes(1))
  })
})
