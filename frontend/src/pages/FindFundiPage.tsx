import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Star, MapPin, CheckCircle, Search, LocateFixed, Filter } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { techniciansApi, categoriesApi } from '../services/api'
import { useLanguage } from '../providers/LanguageProvider'

// Dar es Salaam fallback
const DEFAULT_LAT = -6.7924
const DEFAULT_LNG = 39.2083

export default function FindFundiPage() {
  const { t, language } = useLanguage()

  // Search state
  const [q, setQ] = useState('')
  const [selectedCategories, setSelectedCategories] = useState<number[]>([])
  const [radiusKm, setRadiusKm] = useState(25)
  const [availableOnly, setAvailableOnly] = useState(true)
  const [lat, setLat] = useState<number | null>(null)
  const [lng, setLng] = useState<number | null>(null)
  const [locationStatus, setLocationStatus] = useState<'idle' | 'loading' | 'ok' | 'denied'>('idle')
  const [showFilters, setShowFilters] = useState(false)

  // Get browser location once
  useEffect(() => {
    if (!navigator.geolocation) {
      setLat(DEFAULT_LAT)
      setLng(DEFAULT_LNG)
      setLocationStatus('denied')
      return
    }
    setLocationStatus('loading')
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLat(pos.coords.latitude)
        setLng(pos.coords.longitude)
        setLocationStatus('ok')
      },
      () => {
        setLat(DEFAULT_LAT)
        setLng(DEFAULT_LNG)
        setLocationStatus('denied')
      },
      { enableHighAccuracy: false, timeout: 8000 }
    )
  }, [])

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.list,
  })

  const searchParams = {
    lat: lat ?? DEFAULT_LAT,
    lng: lng ?? DEFAULT_LNG,
    radius_km: radiusKm,
    available_only: availableOnly,
    q: q.trim() || undefined,
    // Backend currently accepts single category_id; we send first selected
    category_id: selectedCategories.length === 1 ? selectedCategories[0] : undefined,
  }

  const { data: technicians, isLoading, isFetching, refetch } = useQuery({
    queryKey: ['technicians-search', searchParams],
    queryFn: () => techniciansApi.search(searchParams),
    enabled: lat !== null && lng !== null,
  })

  const toggleCategory = (id: number) => {
    setSelectedCategories((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    )
  }

  const useMyLocation = () => {
    if (!navigator.geolocation) return
    setLocationStatus('loading')
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLat(pos.coords.latitude)
        setLng(pos.coords.longitude)
        setLocationStatus('ok')
      },
      () => setLocationStatus('denied'),
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="section-title mb-2">{t('nav.find_fundi')}</h1>
        <p className="text-text-muted">
          {language === 'sw'
            ? 'Tafuta fundi karibu nawe kwa umbali, rating na uzoefu.'
            : 'Find technicians near you by distance, rating and experience.'}
        </p>
      </div>

      {/* Search bar + location */}
      <div className="card mb-6 space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
            <input
              type="text"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder={
                language === 'sw'
                  ? 'Tafuta jina, kichwa cha kazi...'
                  : 'Search name, title...'
              }
              className="input-field pl-10"
            />
          </div>
          <button
            type="button"
            onClick={() => refetch()}
            className="btn-primary shrink-0"
          >
            {language === 'sw' ? 'Tafuta' : 'Search'}
          </button>
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="btn-secondary sm:hidden shrink-0"
          >
            <Filter className="h-4 w-4" />
            {language === 'sw' ? 'Filters' : 'Filters'}
          </button>
        </div>

        {/* Location row */}
        <div className="flex flex-wrap items-center gap-3 text-sm">
          <button
            type="button"
            onClick={useMyLocation}
            className="btn-ghost text-sm px-3 py-1.5"
          >
            <LocateFixed className="h-4 w-4" />
            {language === 'sw' ? 'Tumia eneo langu' : 'Use my location'}
          </button>
          <span className="text-text-muted">
            {locationStatus === 'loading' &&
              (language === 'sw' ? 'Inatafuta eneo...' : 'Getting location...')}
            {locationStatus === 'ok' &&
              (language === 'sw' ? 'Eneo limetambuliwa' : 'Location detected')}
            {locationStatus === 'denied' &&
              (language === 'sw'
                ? 'Inatumia Dar es Salaam (default)'
                : 'Using Dar es Salaam (default)')}
          </span>
          <span className="text-text-muted">
            • {language === 'sw' ? 'Radius' : 'Radius'}: {radiusKm} km
          </span>
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Filters sidebar */}
        <aside className={`lg:col-span-1 ${showFilters ? 'block' : 'hidden lg:block'}`}>
          <div className="card sticky top-24 space-y-6">
            <h3 className="font-semibold">
              {language === 'sw' ? 'Chuja' : 'Filters'}
            </h3>

            {/* Radius */}
            <div>
              <label className="text-sm font-medium text-text-secondary mb-2 block">
                {language === 'sw' ? 'Umbali (km)' : 'Distance (km)'}: {radiusKm}
              </label>
              <input
                type="range"
                min={5}
                max={100}
                step={5}
                value={radiusKm}
                onChange={(e) => setRadiusKm(Number(e.target.value))}
                className="w-full accent-brand-600"
              />
              <div className="flex justify-between text-xs text-text-muted mt-1">
                <span>5 km</span>
                <span>100 km</span>
              </div>
            </div>

            {/* Available only */}
            <label className="flex items-center gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={availableOnly}
                onChange={(e) => setAvailableOnly(e.target.checked)}
                className="rounded border-border text-brand-600"
              />
              {language === 'sw' ? 'Wanaopatikana tu' : 'Available only'}
            </label>

            {/* Categories */}
            <div>
              <p className="text-sm font-medium text-text-secondary mb-2">
                {language === 'sw' ? 'Kategoria' : 'Categories'}
              </p>
              <div className="space-y-1.5 max-h-64 overflow-y-auto">
                {(categories || []).map((cat) => (
                  <label
                    key={cat.id}
                    className="flex items-center gap-2 text-sm cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedCategories.includes(cat.id)}
                      onChange={() => toggleCategory(cat.id)}
                      className="rounded border-border text-brand-600"
                    />
                    {language === 'sw' ? cat.name_sw : cat.name_en}
                  </label>
                ))}
              </div>
              {selectedCategories.length > 1 && (
                <p className="text-xs text-amber-600 mt-2">
                  {language === 'sw'
                    ? 'Kwa sasa search inachukua kategoria moja tu (ya kwanza).'
                    : 'Search currently uses only the first selected category.'}
                </p>
              )}
            </div>

            <button
              type="button"
              onClick={() => {
                setQ('')
                setSelectedCategories([])
                setRadiusKm(25)
                setAvailableOnly(true)
              }}
              className="btn-ghost text-sm w-full"
            >
              {language === 'sw' ? 'Futa filters' : 'Clear filters'}
            </button>
          </div>
        </aside>

        {/* Results */}
        <div className="lg:col-span-3 space-y-4">
          {(isLoading || isFetching) && (
            <p className="text-center py-12 text-text-muted">
              {t('common.loading') || (language === 'sw' ? 'Inapakia...' : 'Loading...')}
            </p>
          )}

          {!isLoading && !isFetching && (technicians || []).map((tech) => (
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
                    {tech.average_rating?.toFixed(1) ?? '0.0'} ({tech.total_reviews ?? 0})
                  </span>
                  <span className="text-text-muted">
                    {tech.completed_jobs ?? 0} {t('technician.completed_jobs')}
                  </span>
                  <span className="text-text-muted">
                    {tech.years_experience ?? 0} {t('technician.years_experience')}
                  </span>
                </div>

                <p className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-text-muted">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5" />
                    {tech.region}
                    {tech.district ? `, ${tech.district}` : ''}
                  </span>
                  {typeof tech.distance_km === 'number' && (
                    <span className="font-medium text-brand-600">
                      {tech.distance_km < 1
                        ? `${Math.round(tech.distance_km * 1000)} m`
                        : `${tech.distance_km.toFixed(1)} km`}
                    </span>
                  )}
                  {tech.is_available ? (
                    <span className="text-green-600 font-medium">
                      • {t('technician.available')}
                    </span>
                  ) : (
                    <span className="text-red-500">
                      • {t('technician.not_available')}
                    </span>
                  )}
                </p>
              </div>

              <div className="flex sm:flex-col items-center justify-center gap-2">
                <span className="btn-primary text-sm pointer-events-none">
                  {t('technician.book_now')}
                </span>
              </div>
            </Link>
          ))}

          {!isLoading && !isFetching && (!technicians || technicians.length === 0) && (
            <div className="text-center py-16 card">
              <p className="text-text-muted mb-2">
                {language === 'sw'
                  ? 'Hakuna fundi aliyepatikana kwa filters hizi.'
                  : 'No technicians found with these filters.'}
              </p>
              <p className="text-sm text-text-muted">
                {language === 'sw'
                  ? 'Jaribu kuongeza radius au kuondoa filters.'
                  : 'Try increasing the radius or clearing filters.'}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}