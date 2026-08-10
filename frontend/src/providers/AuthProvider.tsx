import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authApi, User } from '../services/api'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (phoneOrEmail: string, password: string) => Promise<void>
  logout: () => void
  register: (data: {
    full_name: string
    phone: string
    email?: string
    password: string
  }) => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    if (typeof window === 'undefined') return null
    try {
      const stored = localStorage.getItem('patafundi_user')
      return stored ? (JSON.parse(stored) as User) : null
    } catch {
      return null
    }
  })
  const [isLoading, setIsLoading] = useState(true)

  const refreshUser = useCallback(async () => {
    const token = localStorage.getItem('patafundi_access_token')
    if (!token) {
      localStorage.removeItem('patafundi_user')
      setUser(null)
      setIsLoading(false)
      return
    }
    try {
      const me = await authApi.me()
      setUser(me)
      localStorage.setItem('patafundi_user', JSON.stringify(me))
    } catch {
      localStorage.removeItem('patafundi_access_token')
      localStorage.removeItem('patafundi_refresh_token')
      localStorage.removeItem('patafundi_user')
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  const login = async (phoneOrEmail: string, password: string) => {
    const tokens = await authApi.login(phoneOrEmail, password)
    localStorage.setItem('patafundi_access_token', tokens.access_token)
    localStorage.setItem('patafundi_refresh_token', tokens.refresh_token)
    await refreshUser()
  }

  const register = async (data: {
    full_name: string
    phone: string
    email?: string
    password: string
  }) => {
    await authApi.register(data)
    // Auto-login after register
    await login(data.phone, data.password)
  }

  const logout = () => {
    localStorage.removeItem('patafundi_access_token')
    localStorage.removeItem('patafundi_refresh_token')
    localStorage.removeItem('patafundi_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        register,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
