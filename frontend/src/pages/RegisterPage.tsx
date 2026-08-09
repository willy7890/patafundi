import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../providers/AuthProvider'
import { useLanguage } from '../providers/LanguageProvider'
import { authApi } from '../services/api'

export default function RegisterPage() {
  const { t } = useLanguage()
  const { register, login } = useAuth()
  const navigate = useNavigate()
  const [isTechnician, setIsTechnician] = useState(false)
  const [form, setForm] = useState({
    full_name: '',
    phone: '',
    email: '',
    password: '',
    professional_title: '',
    years_experience: 0,
    region: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: name === 'years_experience' ? Number(value) : value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (isTechnician) {
        await authApi.registerTechnician({
          full_name: form.full_name,
          phone: form.phone,
          email: form.email || undefined,
          password: form.password,
          professional_title: form.professional_title || undefined,
          years_experience: form.years_experience,
          region: form.region || undefined,
        })
        await login(form.phone, form.password)
      } else {
        await register({
          full_name: form.full_name,
          phone: form.phone,
          email: form.email || undefined,
          password: form.password,
        })
      }
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-12">
      <div className="card">
        <h1 className="text-2xl font-bold text-center mb-2">
          {isTechnician ? t('auth.register_technician') : t('auth.register_title')}
        </h1>
        <p className="text-center text-sm text-text-muted mb-6">
          {isTechnician && t('auth.technician_note')}
        </p>

        {/* Toggle */}
        <div className="flex rounded-lg border border-border p-1 mb-6">
          <button
            type="button"
            onClick={() => setIsTechnician(false)}
            className={`flex-1 rounded-md py-2 text-sm font-medium transition ${
              !isTechnician ? 'bg-brand-600 text-white' : 'text-text-secondary'
            }`}
          >
            Customer
          </button>
          <button
            type="button"
            onClick={() => setIsTechnician(true)}
            className={`flex-1 rounded-md py-2 text-sm font-medium transition ${
              isTechnician ? 'bg-brand-600 text-white' : 'text-text-secondary'
            }`}
          >
            Technician / Fundi
          </button>
        </div>

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.full_name')}</label>
            <input
              name="full_name"
              className="input-field"
              value={form.full_name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.phone')}</label>
            <input
              name="phone"
              className="input-field"
              value={form.phone}
              onChange={handleChange}
              placeholder="+2557..."
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.email')}</label>
            <input
              name="email"
              type="email"
              className="input-field"
              value={form.email}
              onChange={handleChange}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1.5">{t('auth.password')}</label>
            <input
              name="password"
              type="password"
              className="input-field"
              value={form.password}
              onChange={handleChange}
              minLength={8}
              required
            />
          </div>

          {isTechnician && (
            <>
              <div>
                <label className="block text-sm font-medium mb-1.5">Professional Title</label>
                <input
                  name="professional_title"
                  className="input-field"
                  value={form.professional_title}
                  onChange={handleChange}
                  placeholder="e.g. Electrician, Plumber"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">{t('technician.years_experience')}</label>
                <input
                  name="years_experience"
                  type="number"
                  min={0}
                  className="input-field"
                  value={form.years_experience}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">Region</label>
                <input
                  name="region"
                  className="input-field"
                  value={form.region}
                  onChange={handleChange}
                  placeholder="e.g. Dar es Salaam"
                />
              </div>
              <p className="text-xs text-text-muted bg-brand-50 border border-brand-100 rounded-lg p-3">
                ✓ Certificates are <strong>optional</strong>. You can start receiving jobs immediately without any formal certificate.
              </p>
            </>
          )}

          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? t('common.loading') : t('auth.register_button')}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-text-muted">
          {t('auth.have_account')}{' '}
          <Link to="/login" className="font-semibold text-brand-600 hover:underline">
            {t('auth.login_button')}
          </Link>
        </p>
      </div>
    </div>
  )
}
