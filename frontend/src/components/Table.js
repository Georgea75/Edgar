import React from 'react'
import { flexRender } from '@tanstack/react-table'

function Table ({ table }) {
  return (
      <table className="w-full border table-auto">
          <thead>
              {table.getHeaderGroups().map(headerGroup => (
                  <tr className="border-b bg-gray-200" key={headerGroup.id}>
                      {headerGroup.headers.map(header => (
                          <th key={header.id} className="font-medium p-1">
                              {header.column.columnDef.header}
                          </th>
                      ))}
                  </tr>
              ))}
          </thead>
          <tbody>
              {table.getRowModel().rows.map((row) => {
                return (
                    <tr className="even:bg-gray-50 odd:bg-white" key={row.id}>
                        {row.getVisibleCells().map((cell) => {
                          return (
                            <td className="text-center p-2" key={cell.id}>
                                {flexRender(
                                  cell.column.columnDef.cell,
                                  cell.getContext()
                                )}
                            </td>
                          )
                        })}
                    </tr>
                )
              })}
          </tbody>
      </table>
  )
}

export default Table
