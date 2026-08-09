import { Outlet, Link, useNavigate } from 'react-router-dom'
import { Menu, X, LogOut, Settings, LayoutDashboard } from 'lucide-react'
import { useState } from 'react'
import { useLanguage } from '../providers/LanguageProvider'
import { useAuth } from '../providers/AuthProvider'

export default function MainLayout() {
  const { t, language, setLanguage } = useLanguage()
  const { isAuthenticated, logout } = useAuth()
  const [mobileOpen, setMobileOpen] = useState(false)
  const navigate = useNavigate()
  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen flex flex-col bg-surface text-text-primary">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-border bg-surface/95 backdrop-blur supports-[backdrop-filter]:bg-surface/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600 text-white font-bold text-lg">
                P
              </div>
              <span className="text-xl font-bold tracking-tight text-text-primary">
                Pata<span className="text-brand-600">Fundi</span>
              </span>
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-1">
              <Link to="/" className="btn-ghost">{t('nav.home')}</Link>
              <Link to="/find-fundi" className="btn-ghost">{t('nav.find_fundi')}</Link>
              <Link to="/#services" className="btn-ghost">{t('nav.services')}</Link>
              <Link to="/#how" className="btn-ghost">{t('nav.how_it_works')}</Link>
            </nav>

            {/* Right side */}
            <div className="flex items-center gap-2">
              {/* Language toggle */}
              <button
                onClick={() => setLanguage(language === 'sw' ? 'en' : 'sw')}
                className="btn-ghost text-xs font-semibold uppercase"
                title="Change language"
              >
                {language === 'sw' ? 'EN' : 'SW'}
              </button>

              {isAuthenticated ? (
                <div className="hidden sm:flex items-center gap-2">
                  <Link to="/dashboard" className="btn-ghost">
                    <LayoutDashboard className="h-4 w-4" />
                    {t('nav.dashboard')}
                  </Link>
                  <Link to="/settings" className="btn-ghost">
                    <Settings className="h-4 w-4" />
                  </Link>
                  <button onClick={handleLogout} className="btn-ghost text-red-600">
                    <LogOut className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <div className="hidden sm:flex items-center gap-2">
                  <Link to="/login" className="btn-ghost">{t('nav.login')}</Link>
                  <Link to="/register" className="btn-primary">{t('nav.get_started')}</Link>
                </div>
              )}

              {/* Mobile menu button */}
              <button
                className="md:hidden btn-ghost"
                onClick={() => setMobileOpen(!mobileOpen)}
              >
                {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden border-t border-border bg-surface px-4 py-4 space-y-2">
            <Link to="/" className="block btn-ghost w-full justify-start" onClick={() => setMobileOpen(false)}>
              {t('nav.home')}
            </Link>
            <Link to="/find-fundi" className="block btn-ghost w-full justify-start" onClick={() => setMobileOpen(false)}>
              {t('nav.find_fundi')}
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="block btn-ghost w-full justify-start" onClick={() => setMobileOpen(false)}>
                  {t('nav.dashboard')}
                </Link>
                <Link to="/settings" className="block btn-ghost w-full justify-start" onClick={() => setMobileOpen(false)}>
                  {t('nav.settings')}
                </Link>
                <button onClick={() => { handleLogout(); setMobileOpen(false) }} className="block btn-ghost w-full justify-start text-red-600">
                  {t('nav.logout')}
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="block btn-ghost w-full justify-start" onClick={() => setMobileOpen(false)}>
                  {t('nav.login')}
                </Link>
                <Link to="/register" className="block btn-primary w-full justify-center" onClick={() => setMobileOpen(false)}>
                  {t('nav.get_started')}
                </Link>
              </>
            )}
          </div>
        )}
      </header>

      {/* Main content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-surface-muted">
        <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between gap-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-white font-bold">
                  P
                </div>
                <span className="text-lg font-bold">PataFundi</span>
              </div>
              <p className="text-sm text-text-muted max-w-xs">
                {t('app.tagline')}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-8 sm:grid-cols-3">
              <div>
                <h4 className="text-sm font-semibold mb-3">{t('nav.services')}</h4>
                <ul className="space-y-2 text-sm text-text-muted">
                  <li><Link to="/find-fundi" className="hover:text-brand-600">Electrician</Link></li>
                  <li><Link to="/find-fundi" className="hover:text-brand-600">Plumber</Link></li>
                  <li><Link to="/find-fundi" className="hover:text-brand-600">AC Technician</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold mb-3">{t('nav.help')}</h4>
                <ul className="space-y-2 text-sm text-text-muted">
                  <li><a href="#" className="hover:text-brand-600">{t('nav.how_it_works')}</a></li>
                  <li><a href="#" className="hover:text-brand-600">{t('nav.about')}</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-8 border-t border-border pt-6 flex flex-col sm:flex-row justify-between text-sm text-text-muted">
            <p>© {new Date().getFullYear()} PataFundi. {t('footer.rights')}</p>
            <p>{t('footer.made_for')}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
