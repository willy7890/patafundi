import { Link } from 'react-router-dom'
import { useAuth } from '../providers/AuthProvider'
import { useLanguage } from '../providers/LanguageProvider'
import { LayoutDashboard, User, Briefcase, Settings, Search } from 'lucide-react'

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth()
  const { t } = useLanguage()

  if (isLoading) {
    return <div className="text-center py-20 text-text-muted">{t('common.loading')}</div>
  }

  if (!isAuthenticated || !user) {
    return (
      <div className="text-center py-20">
        <p className="text-text-muted mb-4">Please login to access your dashboard.</p>
        <Link to="/login" className="btn-primary">{t('nav.login')}</Link>
      </div>
    )
  }

  const isTechnician = user.role === 'TECHNICIAN'
  const isAdmin = user.role === 'ADMIN' || user.role === 'SUPER_ADMIN'

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex items-center gap-3 mb-8">
        <LayoutDashboard className="h-7 w-7 text-brand-600" />
        <div>
          <h1 className="text-2xl font-bold">{t('nav.dashboard')}</h1>
          <p className="text-text-muted">Karibu, {user.full_name}</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        <div className="card">
          <p className="text-sm text-text-muted">Role</p>
          <p className="text-xl font-bold mt-1">{user.role}</p>
        </div>
        <div className="card">
          <p className="text-sm text-text-muted">Phone</p>
          <p className="text-xl font-bold mt-1 flex items-center gap-2">
            {user.phone}
            {user.is_verified_phone && (
              <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Verified</span>
            )}
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-text-muted">Language</p>
          <p className="text-xl font-bold mt-1">{user.language === 'sw' ? 'Kiswahili' : 'English'}</p>
        </div>
        <div className="card">
          <p className="text-sm text-text-muted">Theme</p>
          <p className="text-xl font-bold mt-1 capitalize">{user.theme || 'classic'}</p>
        </div>
      </div>

      {/* Quick actions */}
      <h2 className="font-semibold text-lg mb-4">Quick Actions</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Link to="/find-fundi" className="card hover:border-brand-400 transition flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
            <Search className="h-6 w-6" />
          </div>
          <div>
            <p className="font-semibold">{t('nav.find_fundi')}</p>
            <p className="text-sm text-text-muted">Search technicians near you</p>
          </div>
        </Link>

        <Link to="/settings" className="card hover:border-brand-400 transition flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
            <Settings className="h-6 w-6" />
          </div>
          <div>
            <p className="font-semibold">{t('nav.settings')}</p>
            <p className="text-sm text-text-muted">Theme, language, account</p>
          </div>
        </Link>

        {isTechnician && (
          <div className="card flex items-center gap-4 opacity-75">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
              <Briefcase className="h-6 w-6" />
            </div>
            <div>
              <p className="font-semibold">My Jobs</p>
              <p className="text-sm text-text-muted">Coming in Version 2</p>
            </div>
          </div>
        )}

        {isAdmin && (
          <div className="card flex items-center gap-4 border-amber-200 bg-amber-50">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-amber-100 text-amber-700">
              <User className="h-6 w-6" />
            </div>
            <div>
              <p className="font-semibold">Admin Panel</p>
              <p className="text-sm text-text-muted">API: /api/v1/admin/stats</p>
            </div>
          </div>
        )}
      </div>

      <div className="mt-10 rounded-xl border border-dashed border-border p-6 text-center text-text-muted text-sm">
        <p className="font-medium mb-1">Version 1 — Website Foundation</p>
        <p>Bookings, Chat, Payments, and full dashboards arrive in Version 2 & 3.</p>
      </div>
    </div>
  )
}
