import { useEffect, useState } from 'react'
import { useAuth } from '../../providers/AuthProvider'
import { api } from '../../services/api'
import {
  Users, Wrench, ShoppingBag, AlertTriangle, ShieldCheck,
  Trash2, Search, RefreshCw
} from 'lucide-react'

type UserRow = {
  id: number
  full_name: string
  email: string | null
  phone: string
  role: string
  is_active: boolean
  is_verified_phone: boolean
  is_verified_email: boolean
  is_verified_identity: boolean
  created_at: string
}

export default function AdminDashboard() {
  const { user } = useAuth()
  const [users, setUsers] = useState<UserRow[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState<number | null>(null)

  const loadUsers = async () => {
    setLoading(true)
    setError('')
    try {
      const params: Record<string, string | number> = { limit: 100 }
      if (search.trim()) params.search = search.trim()
      if (roleFilter) params.role = roleFilter
      const res = await api.get('/users', { params })
      const data = res.data
      setUsers(data || [])
      setTotal((data || []).length)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.message || 'Failed to load users')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadUsers()
  }, [])

  const handleDelete = async (u: UserRow) => {
    if (u.id === user?.id) {
      alert('Huwezi kufuta akaunti yako mwenyewe / You cannot delete your own account')
      return
    }
    const ok = window.confirm(
      `Una uhakika unataka kufuta ${u.full_name} (${u.role})?\n\nThis action cannot be undone.`
    )
    if (!ok) return

    setDeletingId(u.id)
    setError('')
    try {
      await api.delete(`/users/${u.id}`)
      setUsers((prev) => prev.filter((x) => x.id !== u.id))
      setTotal((t) => Math.max(0, t - 1))
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.message || 'Delete failed')
    } finally {
      setDeletingId(null)
    }
  }

  const canDelete = (u: UserRow) => {
    if (u.id === user?.id) return false
    if (u.role === 'SUPER_ADMIN') return false
    if (u.role === 'ADMIN' && user?.role !== 'SUPER_ADMIN') return false
    return true
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-1">Admin Dashboard</h1>
      <p className="text-muted mb-6">
        Welcome, {user?.full_name} ({user?.role})
      </p>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Users', value: String(total || users.length || '—'), icon: Users },
          { label: 'Technicians', value: String(users.filter((u) => u.role === 'TECHNICIAN').length), icon: Wrench },
          { label: 'Orders', value: '0', icon: ShoppingBag },
          { label: 'Disputes', value: '0', icon: AlertTriangle },
        ].map((s) => (
          <div key={s.label} className="card flex items-center gap-3">
            <s.icon size={22} style={{ color: 'var(--color-brand-600)' }} />
            <div>
              <div className="text-xl font-bold text-primary">{s.value}</div>
              <div className="text-xs text-muted">{s.label}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-4 mb-8">
        <div className="card">
          <h2 className="font-semibold mb-2 flex items-center gap-2">
            <ShieldCheck size={18} /> Certificate Reviews
          </h2>
          <p className="text-sm text-muted">
            Optional certificates pending admin review will appear here. Only VERIFIED status shows public badge.
          </p>
        </div>
        <div className="card">
          <h2 className="font-semibold mb-2">Infrastructure Milestone</h2>
          <p className="text-sm text-muted">
            When registered users reach 1,000+, an admin-only notification will appear. No automatic upgrade or charges.
          </p>
        </div>
      </div>

      {/* Users management */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <h2 className="font-semibold text-lg flex items-center gap-2">
            <Users size={20} /> Manage Users
          </h2>
          <div className="flex flex-wrap gap-2">
            <div className="relative">
              <Search size={16} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted" />
              <input
                className="input-field !pl-8 !py-1.5 text-sm w-40 sm:w-52"
                placeholder="Search name, email, phone..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && loadUsers()}
              />
            </div>
            <select
              className="input-field !py-1.5 text-sm w-auto"
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
            >
              <option value="">All roles</option>
              <option value="CUSTOMER">Customer</option>
              <option value="TECHNICIAN">Technician</option>
              <option value="MERCHANT">Merchant</option>
              <option value="AGENCY">Agency</option>
              <option value="ADMIN">Admin</option>
              <option value="SUPER_ADMIN">Super Admin</option>
            </select>
            <button
              type="button"
              className="btn-secondary !px-3 !py-1.5 text-sm"
              onClick={loadUsers}
              disabled={loading}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-3 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}

        {loading ? (
          <p className="text-sm text-muted py-6 text-center">Loading users...</p>
        ) : users.length === 0 ? (
          <p className="text-sm text-muted py-6 text-center">No users found.</p>
        ) : (
          <div className="overflow-x-auto -mx-1">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-theme text-left text-muted">
                  <th className="py-2 px-2 font-medium">Name</th>
                  <th className="py-2 px-2 font-medium">Contact</th>
                  <th className="py-2 px-2 font-medium">Role</th>
                  <th className="py-2 px-2 font-medium">Status</th>
                  <th className="py-2 px-2 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id} className="border-b border-theme/60 hover:bg-surface-elevated/50">
                    <td className="py-2.5 px-2">
                      <div className="font-medium text-primary">{u.full_name}</div>
                      <div className="text-xs text-muted">#{u.id}</div>
                    </td>
                    <td className="py-2.5 px-2">
                      <div>{u.phone}</div>
                      {u.email && <div className="text-xs text-muted truncate max-w-[160px]">{u.email}</div>}
                    </td>
                    <td className="py-2.5 px-2">
                      <span className="inline-block rounded-full px-2 py-0.5 text-xs font-medium bg-surface-elevated border border-theme">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-2.5 px-2">
                      {u.is_verified_phone || u.is_verified_email || u.is_verified_identity ? (
                        <span className="text-xs text-green-600 font-medium">Verified</span>
                      ) : (
                        <span className="text-xs text-amber-600 font-medium">Unverified</span>
                      )}
                      {!u.is_active && (
                        <span className="ml-1 text-xs text-red-600">Inactive</span>
                      )}
                    </td>
                    <td className="py-2.5 px-2 text-right">
                      {canDelete(u) ? (
                        <button
                          type="button"
                          className="inline-flex items-center gap-1 rounded-lg px-2.5 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 border border-red-200 disabled:opacity-50"
                          onClick={() => handleDelete(u)}
                          disabled={deletingId === u.id}
                          title="Delete user"
                        >
                          <Trash2 size={14} />
                          {deletingId === u.id ? '...' : 'Delete'}
                        </button>
                      ) : (
                        <span className="text-xs text-muted">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}