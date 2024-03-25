import React from 'react'

import Button from './Button'

export default function Pagination ({ table, pagination }) {
  return (
      <div className="w-full text-center p-4">
          <Button onClick={() => table.firstPage()} disabled={!table.getCanPreviousPage()}>
              {'<<'}
          </Button>
          <Button onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
              {'<'}
          </Button>
          <span className="text-sm">
              Page {pagination.pageIndex + 1} of {table.getPageCount()}
          </span>
          <Button onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
              {'>'}
          </Button>
          <Button onClick={() => table.lastPage()} disabled={!table.getCanNextPage()}>
              {'>>'}
          </Button>
      </div>
  )
}
