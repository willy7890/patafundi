import { useLanguage } from '../providers/LanguageProvider'
import { useTheme, ThemeName, Appearance } from '../providers/ThemeProvider'
import { useAuth } from '../providers/AuthProvider'
import { Check } from 'lucide-react'

const THEMES: { id: ThemeName; labelKey: string; colors: string[] }[] = [
  { id: 'classic', labelKey: 'settings.theme_classic', colors: ['#0ea5e9', '#0284c7', '#0369a1'] },
  { id: 'ocean', labelKey: 'settings.theme_ocean', colors: ['#3b82f6', '#2563eb', '#1d4ed8'] },
  { id: 'forest', labelKey: 'settings.theme_forest', colors: ['#22c55e', '#16a34a', '#15803d'] },
  { id: 'sunset', labelKey: 'settings.theme_sunset', colors: ['#f97316', '#ea580c', '#c2410c'] },
  { id: 'midnight', labelKey: 'settings.theme_midnight', colors: ['#6366f1', '#4f46e5', '#0f172a'] },
]

export default function SettingsPage() {
  const { t, language, setLanguage } = useLanguage()
  const { theme, appearance, setTheme, setAppearance } = useTheme()
  const { user, isAuthenticated } = useAuth()

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
      <h1 className="section-title mb-8">{t('settings.title')}</h1>

      {/* Language */}
      <section className="card mb-6">
        <h2 className="font-semibold text-lg mb-4">{t('settings.language')}</h2>
        <div className="flex gap-3">
          <button
            onClick={() => setLanguage('sw')}
            className={`flex-1 rounded-lg border-2 px-4 py-3 text-sm font-medium transition ${
              language === 'sw'
                ? 'border-brand-600 bg-brand-50 text-brand-700'
                : 'border-border hover:border-brand-300'
            }`}
          >
            Kiswahili
          </button>
          <button
            onClick={() => setLanguage('en')}
            className={`flex-1 rounded-lg border-2 px-4 py-3 text-sm font-medium transition ${
              language === 'en'
                ? 'border-brand-600 bg-brand-50 text-brand-700'
                : 'border-border hover:border-brand-300'
            }`}
          >
            English
          </button>
        </div>
      </section>

      {/* Theme */}
      <section className="card mb-6">
        <h2 className="font-semibold text-lg mb-4">{t('settings.theme')}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {THEMES.map((th) => (
            <button
              key={th.id}
              onClick={() => setTheme(th.id)}
              className={`relative flex items-center gap-3 rounded-xl border-2 p-4 text-left transition ${
                theme === th.id
                  ? 'border-brand-600 bg-brand-50/50'
                  : 'border-border hover:border-brand-300'
              }`}
            >
              <div className="flex gap-1">
                {th.colors.map((c, i) => (
                  <div
                    key={i}
                    className="h-8 w-8 rounded-full border border-black/10"
                    style={{ backgroundColor: c }}
                  />
                ))}
              </div>
              <span className="font-medium text-sm">{t(th.labelKey)}</span>
              {theme === th.id && (
                <Check className="absolute right-3 top-3 h-5 w-5 text-brand-600" />
              )}
            </button>
          ))}
        </div>
      </section>

      {/* Appearance */}
      <section className="card mb-6">
        <h2 className="font-semibold text-lg mb-4">{t('settings.appearance')}</h2>
        <div className="flex gap-3">
          {(['light', 'dark', 'system'] as Appearance[]).map((a) => (
            <button
              key={a}
              onClick={() => setAppearance(a)}
              className={`flex-1 rounded-lg border-2 px-4 py-3 text-sm font-medium transition ${
                appearance === a
                  ? 'border-brand-600 bg-brand-50 text-brand-700'
                  : 'border-border hover:border-brand-300'
              }`}
            >
              {t(`settings.appearance_${a}`)}
            </button>
          ))}
        </div>
      </section>

      {/* Account info */}
      {isAuthenticated && user && (
        <section className="card">
          <h2 className="font-semibold text-lg mb-4">{t('settings.account')}</h2>
          <dl className="space-y-3 text-sm">
            <div className="flex justify-between">
              <dt className="text-text-muted">Name</dt>
              <dd className="font-medium">{user.full_name}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-text-muted">Phone</dt>
              <dd className="font-medium">{user.phone}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-text-muted">Role</dt>
              <dd className="font-medium">{user.role}</dd>
            </div>
          </dl>
        </section>
      )}
    </div>
  )
}
