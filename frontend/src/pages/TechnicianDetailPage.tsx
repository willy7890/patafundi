import { useParams, Link } from 'react-router-dom'
import { Star, MapPin, CheckCircle, ArrowLeft } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { techniciansApi } from '../services/api'
import { useLanguage } from '../providers/LanguageProvider'

export default function TechnicianDetailPage() {
  const { id } = useParams()
  const { t } = useLanguage()

  const { data: tech, isLoading } = useQuery({
    queryKey: ['technician', id],
    queryFn: () => techniciansApi.get(Number(id)),
    enabled: !!id,
  })

  if (isLoading) {
    return <div className="text-center py-20 text-text-muted">{t('common.loading')}</div>
  }

  if (!tech) {
    return (
      <div className="text-center py-20">
        <p className="text-text-muted mb-4">Technician not found</p>
        <Link to="/find-fundi" className="btn-primary">{t('common.back')}</Link>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Link to="/find-fundi" className="inline-flex items-center gap-1 text-sm text-text-muted hover:text-brand-600 mb-6">
        <ArrowLeft className="h-4 w-4" /> {t('common.back')}
      </Link>

      <div className="card">
        <div className="flex flex-col sm:flex-row gap-6">
          <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-2xl bg-brand-100 text-brand-700 text-4xl font-bold">
            {tech.user?.full_name?.charAt(0) || 'F'}
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-bold">{tech.user?.full_name}</h1>
            <p className="text-lg text-text-secondary">{tech.professional_title}</p>

            <div className="mt-3 flex flex-wrap gap-2">
              {tech.user?.is_verified_phone && (
                <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
                  <CheckCircle className="h-3.5 w-3.5" /> Phone Verified
                </span>
              )}
              {/* Certificate badge only if verified — never shown as verified if pending */}
              <span className="inline-flex items-center gap-1 rounded-full bg-surface-muted px-2.5 py-1 text-xs font-medium text-text-muted">
                {t('technician.no_certificate')}
              </span>
            </div>

            <div className="mt-4 flex flex-wrap gap-6 text-sm">
              <div>
                <span className="flex items-center gap-1 text-amber-500 font-semibold">
                  <Star className="h-5 w-5 fill-current" />
                  {tech.average_rating.toFixed(1)}
                </span>
                <span className="text-text-muted">{tech.total_reviews} reviews</span>
              </div>
              <div>
                <p className="font-semibold">{tech.completed_jobs}</p>
                <p className="text-text-muted">{t('technician.completed_jobs')}</p>
              </div>
              <div>
                <p className="font-semibold">{tech.years_experience}</p>
                <p className="text-text-muted">{t('technician.years_experience')}</p>
              </div>
            </div>
          </div>
        </div>

        {tech.bio && (
          <div className="mt-6 pt-6 border-t border-border">
            <h3 className="font-semibold mb-2">About</h3>
            <p className="text-text-secondary leading-relaxed">{tech.bio}</p>
          </div>
        )}

        <div className="mt-6 pt-6 border-t border-border grid sm:grid-cols-2 gap-4 text-sm">
          <div className="flex items-center gap-2 text-text-muted">
            <MapPin className="h-4 w-4" />
            {tech.region}{tech.district ? `, ${tech.district}` : ''}{tech.ward ? `, ${tech.ward}` : ''}
          </div>
          <div className="text-text-muted">
            {t('technician.service_radius')}: {tech.service_radius_km} km
          </div>
          <div>
            {tech.is_available ? (
              <span className="text-green-600 font-medium">{t('technician.available')}</span>
            ) : (
              <span className="text-red-500">{t('technician.not_available')}</span>
            )}
          </div>
        </div>

        <div className="mt-8 flex gap-3">
          <button className="btn-primary flex-1">{t('technician.book_now')}</button>
          <button className="btn-secondary">Message</button>
        </div>
      </div>
    </div>
  )
}
