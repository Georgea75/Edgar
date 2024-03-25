const ENDPOINT = 'http://localhost:8000/api'

async function makeRequest (...args) {
  const response = await fetch(...args)
  const data = await response.json()
  if (!response.ok) throw new Error(data.error)
  return data
}

export async function createFile ({ file }) {
  const body = new FormData()
  body.append('file', file)

  try {
    return await makeRequest(`${ENDPOINT}/sheets/`, {
      body,
      method: 'POST'
    })
  } catch (error) {
    alert(`An error occurred: ${error.message}`)
    return undefined
  }
}

export async function updateColumnType ({ sheetId, columnId, columnType }) {
  const body = new FormData()
  body.append('data_type', columnType)

  const data = await makeRequest(`${ENDPOINT}/columns/${columnId}`, {
    body,
    method: 'PUT'
  })

  if (data.data_type !== columnType) {
    alert(`The column could not be converted to type: ${columnType}`)
  }
}

export async function fetchSupportedTypes () {
  return makeRequest(`${ENDPOINT}/supported-types/`)
}

export async function fetchSheet ({ sheetId, pageIndex, pageSize }) {
  return makeRequest(`${ENDPOINT}/sheets/${sheetId}/?start_index=${pageIndex}&num_records=${pageSize}`)
}
