import { apiBaseUrl } from '@/lib/constants'

const baseUrl = `${apiBaseUrl}/scheduler`

export const start_scheduler = async () => {
  try {
    const response = await fetch(`${baseUrl}/start`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error starting scheduler:', error)
    throw error
  }
}

export const stop_scheduler = async () => {
  try {
    const response = await fetch(`${baseUrl}/stop`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error stopping scheduler:', error)
    throw error
  }
}

export const scheduler_status = async () => {
  try {
    const response = await fetch(`${baseUrl}/status`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error checking scheduler status:', error)
    throw error
  }
}
