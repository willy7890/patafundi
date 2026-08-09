import axios from 'axios'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('patafundi_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('patafundi_access_token')
      localStorage.removeItem('patafundi_refresh_token')
      localStorage.removeItem('patafundi_user')
      // Optionally redirect
    }
    return Promise.reject(error)
  }
)

export interface User {
  id: number
  full_name: string
  phone: string
  email?: string
  role: string
  is_active: boolean
  is_verified_phone: boolean
  is_verified_email: boolean
  is_verified_identity: boolean
  profile_photo?: string
  language: string
  theme: string
  appearance: string
  created_at: string
}

export interface TechnicianProfile {
  id: number
  user_id: number
  professional_title?: string
  bio?: string
  years_experience: number
  service_radius_km: number
  region?: string
  district?: string
  ward?: string
  street?: string
  latitude?: number
  longitude?: number
  is_available: boolean
  average_rating: number
  total_reviews: number
  completed_jobs: number
  response_rate: number
  profile_completion: number
  user?: User
}

export interface ServiceCategory {
  id: number
  name_en: string
  name_sw: string
  slug: string
  icon?: string
  is_active: boolean
}

export const authApi = {
  login: async (phoneOrEmail: string, password: string) => {
    const form = new URLSearchParams()
    form.append('username', phoneOrEmail)
    form.append('password', password)
    const { data } = await api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return data
  },
  register: async (payload: {
    full_name: string
    phone: string
    email?: string
    password: string
    role?: string
  }) => {
    const { data } = await api.post('/auth/register', payload)
    return data
  },
  registerTechnician: async (payload: any) => {
    const { data } = await api.post('/auth/register/technician', payload)
    return data
  },
  me: async () => {
    const { data } = await api.get('/auth/me')
    return data as User
  },
}

export const categoriesApi = {
  list: async () => {
    const { data } = await api.get('/categories/')
    return data as ServiceCategory[]
  },
}

export const techniciansApi = {
  list: async (params?: { region?: string; available_only?: boolean }) => {
    const { data } = await api.get('/technicians/', { params })
    return data as TechnicianProfile[]
  },
  get: async (id: number) => {
    const { data } = await api.get(`/technicians/${id}`)
    return data as TechnicianProfile
  },
}
