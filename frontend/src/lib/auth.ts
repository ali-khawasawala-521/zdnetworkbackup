import { apiBaseUrl } from '@/lib/constants'

const baseUrl = `${apiBaseUrl}/auth`

export const isAuthenticated = async () => {
  try {
    const response = await fetch(`${baseUrl}/verify-user`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) return false

    const data = await response.json()
    return !!data
  } catch (error) {
    console.error('Auth check failed:', error)
    return false
  }
}

export const login = async (payload: { email: string; password: string }) => {
  try {
    const response = await fetch(`${baseUrl}/login`, {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()
    localStorage.setItem('user', JSON.stringify(data?.user))
    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

export const logout = async () => {
  try {
    const response = await fetch(`${baseUrl}/logout`, {
      method: 'POST',
      credentials: 'include',
    })

    if (!response.ok) throw new Error('Logout failed')
    localStorage.removeItem('user')
    return true
  } catch (error) {
    console.error('Logout error:', error)
    throw error
  }
}

export const register = async (payload: { email: string; password: string }) => {
  try {
    const response = await fetch(`${baseUrl}/register`, {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('Registration failed')

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Registration error:', error)
    throw error
  }
}
