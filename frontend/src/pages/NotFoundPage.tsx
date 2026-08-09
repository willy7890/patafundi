import { Link } from 'react-router-dom'
import { useLanguage } from '../providers/LanguageProvider'

export default function NotFoundPage() {
  const { t } = useLanguage()
  return (
    <div className="mx-auto max-w-lg px-4 py-24 text-center">
      <h1 className="text-6xl font-bold text-brand-600 mb-4">404</h1>
      <p className="text-xl text-text-secondary mb-8">Page not found</p>
      <Link to="/" className="btn-primary">
        {t('nav.home')}
      </Link>
    </div>
  )
}
