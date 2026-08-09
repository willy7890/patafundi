import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'

export type ThemeName = 'classic' | 'ocean' | 'forest' | 'sunset' | 'midnight'
export type Appearance = 'light' | 'dark' | 'system'

interface ThemeContextType {
  theme: ThemeName
  appearance: Appearance
  setTheme: (theme: ThemeName) => void
  setAppearance: (appearance: Appearance) => void
  isDark: boolean
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<ThemeName>(() => {
    return (localStorage.getItem('patafundi_theme') as ThemeName) || 'classic'
  })
  const [appearance, setAppearanceState] = useState<Appearance>(() => {
    return (localStorage.getItem('patafundi_appearance') as Appearance) || 'system'
  })
  const [isDark, setIsDark] = useState(false)

  const applyTheme = useCallback((t: ThemeName, a: Appearance) => {
    document.documentElement.setAttribute('data-theme', t)

    let dark = false
    if (a === 'dark') dark = true
    else if (a === 'light') dark = false
    else dark = window.matchMedia('(prefers-color-scheme: dark)').matches

    // Midnight is always dark-oriented
    if (t === 'midnight') dark = true

    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    setIsDark(dark)
  }, [])

  useEffect(() => {
    applyTheme(theme, appearance)
  }, [theme, appearance, applyTheme])

  useEffect(() => {
    if (appearance !== 'system') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => applyTheme(theme, appearance)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [appearance, theme, applyTheme])

  const setTheme = (t: ThemeName) => {
    setThemeState(t)
    localStorage.setItem('patafundi_theme', t)
  }

  const setAppearance = (a: Appearance) => {
    setAppearanceState(a)
    localStorage.setItem('patafundi_appearance', a)
  }

  return (
    <ThemeContext.Provider value={{ theme, appearance, setTheme, setAppearance, isDark }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}
