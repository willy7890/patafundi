import { Link } from 'react-router-dom'
import { Search, MapPin, Wrench, Shield, Star, CheckCircle, ArrowRight } from 'lucide-react'
import { useLanguage } from '../providers/LanguageProvider'
import { useQuery } from '@tanstack/react-query'
import { categoriesApi, techniciansApi } from '../services/api'

export default function HomePage() {
  const { t, language } = useLanguage()

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesApi.list,
  })

  const { data: technicians } = useQuery({
    queryKey: ['technicians-featured'],
    queryFn: () => techniciansApi.list({ available_only: true }),
  })

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-600 to-brand-800 text-white">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0djItaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6bTAtNHYyaDJ2LTJoLTJ6Ii8+PC9nPjwvZz48L3N2Zz4=')] opacity-30" />
        <div className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-28">
          <div className="max-w-3xl">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
              {t('home.hero_title')}
            </h1>
            <p className="mt-4 text-lg text-brand-100 sm:text-xl">
              {t('home.hero_subtitle')}
            </p>

            {/* Search box */}
            <div className="mt-8 flex flex-col sm:flex-row gap-3 rounded-2xl bg-white/10 p-3 backdrop-blur-sm border border-white/20">
              <div className="flex-1 flex items-center gap-2 rounded-xl bg-white px-4 py-3 text-text-primary">
                <Search className="h-5 w-5 text-text-muted" />
                <input
                  type="text"
                  placeholder={t('home.search_placeholder_service')}
                  className="w-full bg-transparent text-sm outline-none placeholder:text-text-muted"
                />
              </div>
              <div className="flex-1 flex items-center gap-2 rounded-xl bg-white px-4 py-3 text-text-primary">
                <MapPin className="h-5 w-5 text-text-muted" />
                <input
                  type="text"
                  placeholder={t('home.search_placeholder_location')}
                  className="w-full bg-transparent text-sm outline-none placeholder:text-text-muted"
                />
              </div>
              <Link
                to="/find-fundi"
                className="flex items-center justify-center gap-2 rounded-xl bg-brand-500 px-6 py-3 text-sm font-semibold text-white hover:bg-brand-400 transition"
              >
                {t('home.search_button')}
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Services */}
      <section id="services" className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="section-title text-center mb-10">{t('home.popular_services')}</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {(categories || []).slice(0, 10).map((cat) => (
            <Link
              key={cat.id}
              to={`/find-fundi?category=${cat.slug}`}
              className="card flex flex-col items-center gap-3 text-center hover:border-brand-400 hover:shadow-md transition group"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-100 text-brand-700 group-hover:bg-brand-600 group-hover:text-white transition">
                <Wrench className="h-6 w-6" />
              </div>
              <span className="text-sm font-medium">
                {language === 'sw' ? cat.name_sw : cat.name_en}
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="bg-surface-muted py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="section-title text-center mb-12">{t('home.how_it_works')}</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { icon: Search, title: t('home.step1'), desc: t('home.step1_desc') },
              { icon: Star, title: t('home.step2'), desc: t('home.step2_desc') },
              { icon: CheckCircle, title: t('home.step3'), desc: t('home.step3_desc') },
              { icon: Shield, title: t('home.step4'), desc: t('home.step4_desc') },
            ].map((step, i) => (
              <div key={i} className="text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-600 text-white mb-4">
                  <step.icon className="h-7 w-7" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
                <p className="text-sm text-text-muted">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Technicians */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <h2 className="section-title">{t('home.featured_technicians')}</h2>
          <Link to="/find-fundi" className="btn-ghost text-brand-600">
            {t('common.view_all')} →
          </Link>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {(technicians || []).slice(0, 3).map((tech) => (
            <Link
              key={tech.id}
              to={`/technicians/${tech.id}`}
              className="card hover:border-brand-400 hover:shadow-md transition"
            >
              <div className="flex items-start gap-4">
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-700 text-xl font-bold">
                  {tech.user?.full_name?.charAt(0) || 'F'}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold truncate">{tech.user?.full_name}</h3>
                  <p className="text-sm text-text-muted">{tech.professional_title}</p>
                  <div className="mt-2 flex items-center gap-3 text-sm">
                    <span className="flex items-center gap-1 text-amber-500">
                      <Star className="h-4 w-4 fill-current" />
                      {tech.average_rating.toFixed(1)}
                    </span>
                    <span className="text-text-muted">
                      {tech.completed_jobs} {t('technician.completed_jobs').toLowerCase()}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-text-muted">
                    {tech.region}{tech.district ? `, ${tech.district}` : ''}
                  </p>
                </div>
              </div>
            </Link>
          ))}
          {(!technicians || technicians.length === 0) && (
            <p className="text-text-muted col-span-full text-center py-8">
              {t('common.loading')}
            </p>
          )}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-brand-600 text-white py-16">
        <div className="mx-auto max-w-3xl px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">{t('home.cta_title')}</h2>
          <p className="text-brand-100 mb-8">
            {t('auth.technician_note')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="btn-primary bg-white text-brand-700 hover:bg-brand-50">
              {t('home.cta_button')}
            </Link>
            <Link to="/register" className="btn-secondary border-white/30 text-white hover:bg-white/10">
              {t('home.become_technician')}
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
