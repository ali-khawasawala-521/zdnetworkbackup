import { format } from 'date-fns'

export const formatLocaleDate = (date: string | Date) => {
  const formatString = 'dd-MMM-yyyy HH:mm:ss'
  if (typeof date === 'string') {
    return format(new Date(`${date}Z`), formatString)
  }
  return format(date, formatString)
}
