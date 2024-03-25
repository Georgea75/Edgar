export const typeMap = {
  bool: 'Boolean',
  category: 'Category',
  int8: 'Int8',
  int16: 'Int16',
  int32: 'Int32',
  int64: 'Int64',
  float32: 'Float32',
  float64: 'Float64',
  complex128: 'Complex',
  'timedelta64[ns]': 'Time Interval',
  'datetime64[ns]': 'Date',
  object: 'Text'
}

export function isFileValid (file) {
  return [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ].includes(file.type)
}
