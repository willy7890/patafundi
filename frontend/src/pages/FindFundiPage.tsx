import { Link } from 'react-router-dom'
import { Star, MapPin, CheckCircle } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { techniciansApi, categoriesApi } from '../services/api'
import { useLanguage } from '../providers/LanguageProvider'

export default function FindFundiPage() {
  const { t, language } = useLanguage()

  const { data: technicians, isLoading } = useQuery({
    queryKey: ['technicians'],
    queryFn: () => techniciansApi.list(),
  })

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.list,
  })

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <h1 className="section-title mb-2">{t('nav.find_fundi')}</h1>
      <p className="text-text-muted mb-8">
        {t('home.hero_subtitle')}
      </p>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Filters sidebar */}
        <aside className="lg:col-span-1">
          <div className="card sticky top-24">
            <h3 className="font-semibold mb-4">{t('common.filter')}</h3>
            <div className="space-y-3">
              <p className="text-sm font-medium text-text-secondary">Categories</p>
              <div className="space-y-1 max-h-64 overflow-y-auto">
                {(categories || []).map((cat) => (
                  <label key={cat.id} className="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="checkbox" className="rounded border-border text-brand-600" />
                    {language === 'sw' ? cat.name_sw : cat.name_en}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Results */}
        <div className="lg:col-span-3 space-y-4">
          {isLoading && (
            <p className="text-center py-12 text-text-muted">{t('common.loading')}</p>
          )}
          {(technicians || []).map((tech) => (
            <Link
              key={tech.id}
              to={`/technicians/${tech.id}`}
              className="card flex flex-col sm:flex-row gap-4 hover:border-brand-400 hover:shadow-md transition"
            >
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-700 text-2xl font-bold">
                {tech.user?.full_name?.charAt(0) || 'F'}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-semibold text-lg">{tech.user?.full_name}</h3>
                  {tech.user?.is_verified_phone && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
                      <CheckCircle className="h-3 w-3" /> Phone
                    </span>
                  )}
                </div>
                <p className="text-text-secondary">{tech.professional_title}</p>
                <div className="mt-2 flex flex-wrap items-center gap-4 text-sm">
                  <span className="flex items-center gap-1 text-amber-500">
                    <Star className="h-4 w-4 fill-current" />
                    {tech.average_rating.toFixed(1)} ({tech.total_reviews})
                  </span>
                  <span className="text-text-muted">
                    {tech.completed_jobs} {t('technician.completed_jobs')}
                  </span>
                  <span className="text-text-muted">
                    {tech.years_experience} {t('technician.years_experience')}
                  </span>
                </div>
                <p className="mt-1 flex items-center gap-1 text-sm text-text-muted">
                  <MapPin className="h-3.5 w-3.5" />
                  {tech.region}{tech.district ? `, ${tech.district}` : ''}
                  {tech.is_available ? (
                    <span className="ml-2 text-green-600 font-medium">• {t('technician.available')}</span>
                  ) : (
                    <span className="ml-2 text-red-500">• {t('technician.not_available')}</span>
                  )}
                </p>
              </div>
              <div className="flex sm:flex-col items-center justify-center gap-2">
                <span className="btn-primary text-sm">{t('technician.book_now')}</span>
              </div>
            </Link>
          ))}
          {!isLoading && (!technicians || technicians.length === 0) && (
            <p className="text-center py-12 text-text-muted">No technicians found yet.</p>
          )}
        </div>
      </div>
    </div>
  )
}
