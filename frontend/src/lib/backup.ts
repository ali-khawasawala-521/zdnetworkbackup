const baseUrl = 'http://localhost:6565/backup/'

import type { Backup } from '@/types/backup'

export const getBackup = async (id: string | number) => {
  try {
    const response = await fetch(`${baseUrl}${id}`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot fetch backup')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const getBackupList = async () => {
  try {
    const response = await fetch(baseUrl, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot fetch backups')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const deleteBackup = async (id: string | number) => {
  try {
    const response = await fetch(`${baseUrl}${id}`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot delete backup')

    return response.json()
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}

export const downloadBackup = async (backup: Backup) => {
  try {
    const response = await fetch(`${baseUrl}download/${backup.id}`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Cannot download backup')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${backup.id}-${backup.hostname}-${backup.ip_address}.cfg`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
