import React, { useState } from 'react'
import { useReactTable, getCoreRowModel } from '@tanstack/react-table'
import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query'

import { typeMap } from './utils'
import Table from './components/Table'
import Pagination from './components/Pagination'
import TableInformation from './components/TableInformation'
import { fetchSheet, fetchSupportedTypes, updateColumnType } from './api'

function DataViewer ({ sheetId }) {
  const client = useQueryClient()

  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10
  })

  const { data: supportTypesData } = useQuery({ queryKey: ['supportedTypes'], queryFn: fetchSupportedTypes })

  const { data: sheetData } = useQuery({
    queryKey: ['sheets', sheetId, pagination],
    queryFn: () => {
      const pageIndex = pagination.pageIndex * pagination.pageSize
      const pageSize = pagination.pageSize
      return fetchSheet({
        sheetId,
        pageIndex,
        pageSize
      })
    }
  })

  const mutation = useMutation({
    mutationFn: updateColumnType,
    onSuccess: () => {
      client.invalidateQueries({ queryKey: ['sheets', sheetId] })
    }
  })

  function onUpdateType (columnId, columnType) {
    mutation.mutate({
      sheetId,
      columnId,
      columnType
    })
  }

  const rows = sheetData?.rows || []
  const fileName = sheetData?.file_name
  const columnData = sheetData?.columns || []
  const numberOfRecords = sheetData?.number_of_records || 0
  const supportedTypes = supportTypesData?.supported_types || []

  const columns = columnData.map(column => ({
    accessorKey: column.name,
    header: (
        <div className="flex flex-col items-center w-full space-y-1 py-1">
            <div className="text-center w-full">{column.name}</div>
            <div>
                <select value={column.data_type} onChange={(e) => onUpdateType(column.id, e.target.value)}>
                    {supportedTypes.map((type, index) => (
                        <option className="text-center" key={index} value={type}>{typeMap[type]}</option>
                    ))}
                </select>
            </div>
        </div>
    ),
    cell: (props) => {
      const value = props.getValue()
      return typeof value === 'boolean' ? <p>{value.toString()}</p> : <p>{value}</p>
    }
  }))

  const table = useReactTable({
    data: rows,
    columns: columns,
    manualPagination: true,
    rowCount: numberOfRecords,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    state: {
      pagination
    }
  })

  return (
      <div>
          <TableInformation fileName={fileName} numberOfRecords={numberOfRecords} />
          <Table table={table} />
          <Pagination table={table} pagination={pagination} />
      </div>
  )
}

export default DataViewer
