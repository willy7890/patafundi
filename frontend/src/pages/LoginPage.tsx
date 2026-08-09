import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../providers/AuthProvider'
import { useLanguage } from '../providers/LanguageProvider'

export default function LoginPage() {
  const { t } = useLanguage()
  const { login } = useAuth()
  const navigate = useNavigate()
  const [phoneOrEmail, setPhoneOrEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(phoneOrEmail, password)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-16">
      <div className="card">
        <h1 className="text-2xl font-bold text-center mb-6">{t('auth.login_title')}</h1>

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.phone')} / Email</label>
            <input
              type="text"
              className="input-field"
              value={phoneOrEmail}
              onChange={(e) => setPhoneOrEmail(e.target.value)}
              placeholder="+2557... or email"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.password')}</label>
            <input
              type="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? t('common.loading') : t('auth.login_button')}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-text-muted">
          {t('auth.no_account')}{' '}
          <Link to="/register" className="font-semibold text-brand-600 hover:underline">
            {t('auth.register_button')}
          </Link>
        </p>

        <div className="mt-6 rounded-lg bg-surface-muted p-3 text-xs text-text-muted">
          <p className="font-medium mb-1">Demo accounts:</p>
          <p>Admin: admin@patafundi.co.tz / Admin@123</p>
          <p>Customer: customer@example.com / Customer1!</p>
          <p>Technician: fundi@example.com / Fundi123!</p>
        </div>
      </div>
    </div>
  )
}
