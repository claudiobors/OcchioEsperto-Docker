import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  const api = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json' },
  })

  // Attach token to every request
  api.interceptors.request.use((config) => {
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  // Handle 401 responses
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        logout()
      }
      return Promise.reject(error)
    }
  )

  useEffect(() => {
    if (token) {
      // Verify token on mount
      api.get('/me')
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('token')
          setToken(null)
          setUser(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [token])

  const login = async (email, password) => {
    const res = await api.post('/login', { email, password })
    localStorage.setItem('token', res.data.access_token)
    setToken(res.data.access_token)
    setUser(res.data.user)
    return res.data
  }

  const register = async (data) => {
    const res = await api.post('/register', data)
    localStorage.setItem('token', res.data.access_token)
    setToken(res.data.access_token)
    setUser(res.data.user)
    return res.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, api }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}