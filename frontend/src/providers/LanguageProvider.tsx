import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import sw from '../translations/sw.json'
import en from '../translations/en.json'

type Language = 'sw' | 'en'
type Translations = typeof sw

interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
  translations: Translations
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

const dictionaries: Record<Language, Translations> = { sw, en }

function getNested(obj: any, path: string): string {
  return path.split('.').reduce((acc, part) => acc?.[part], obj) ?? path
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('patafundi_language') as Language
    return saved === 'en' || saved === 'sw' ? saved : 'sw'
  })

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang)
    localStorage.setItem('patafundi_language', lang)
    document.documentElement.lang = lang
  }, [])

  useEffect(() => {
    document.documentElement.lang = language
  }, [language])

  const t = useCallback(
    (key: string) => getNested(dictionaries[language], key),
    [language]
  )

  return (
    <LanguageContext.Provider
      value={{ language, setLanguage, t, translations: dictionaries[language] }}
    >
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider')
  return ctx
}
