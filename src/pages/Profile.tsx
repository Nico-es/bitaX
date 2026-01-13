import { useState, useEffect } from 'react'
import { Mail, Phone, Briefcase, Award, Edit2, Save, X } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../lib/supabase'

export default function Profile() {
  const { profile, user, updateProfile } = useAuth()
  const [editing, setEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [isProfessional, setIsProfessional] = useState(false)
  const [professionalData, setProfessionalData] = useState<any>(null)

  const [formData, setFormData] = useState({
    full_name: profile?.full_name || '',
    phone: profile?.phone || '',
    bio: profile?.bio || '',
  })

  useEffect(() => {
    if (profile?.user_type === 'professional') {
      setIsProfessional(true)
      loadProfessionalData()
    }
  }, [profile])

  async function loadProfessionalData() {
    if (!user) return

    try {
      const { data, error } = await supabase
        .from('professionals')
        .select('*')
        .eq('user_id', user.id)
        .maybeSingle()

      if (error) throw error
      if (data) setProfessionalData(data)
    } catch (error) {
      console.error('Error loading professional data:', error)
    }
  }

  async function handleSave() {
    setLoading(true)
    const { error } = await updateProfile(formData)

    if (error) {
      alert('Error al actualizar el perfil')
    } else {
      setEditing(false)
    }
    setLoading(false)
  }

  function handleCancel() {
    setFormData({
      full_name: profile?.full_name || '',
      phone: profile?.phone || '',
      bio: profile?.bio || '',
    })
    setEditing(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20 md:pb-8">
      <div className="gradient-bg text-white py-12">
        <div className="page-container">
          <div className="flex items-center justify-between">
            <h1 className="text-4xl font-bold">Mi Perfil</h1>
            {!editing && (
              <button
                onClick={() => setEditing(true)}
                className="bg-white text-green-ge px-6 py-2 rounded-lg font-semibold hover:bg-green-light transition-colors flex items-center gap-2"
              >
                <Edit2 className="w-4 h-4" />
                Editar
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="page-container py-8">
        <div className="max-w-4xl mx-auto">
          <div className="card p-8 mb-6">
            <div className="flex items-start gap-6 mb-8">
              {profile?.avatar_url ? (
                <img
                  src={profile.avatar_url}
                  alt={profile.full_name}
                  className="w-32 h-32 rounded-full object-cover"
                />
              ) : (
                <div className="w-32 h-32 rounded-full bg-gradient-to-br from-green-ge to-blue-ge flex items-center justify-center text-white text-5xl font-bold">
                  {profile?.full_name?.[0]?.toUpperCase()}
                </div>
              )}

              <div className="flex-1">
                {editing ? (
                  <>
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nombre Completo
                      </label>
                      <input
                        type="text"
                        value={formData.full_name}
                        onChange={(e) =>
                          setFormData({ ...formData, full_name: e.target.value })
                        }
                        className="input-field"
                      />
                    </div>

                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Teléfono
                      </label>
                      <input
                        type="tel"
                        value={formData.phone}
                        onChange={(e) =>
                          setFormData({ ...formData, phone: e.target.value })
                        }
                        className="input-field"
                      />
                    </div>

                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Biografía
                      </label>
                      <textarea
                        value={formData.bio}
                        onChange={(e) =>
                          setFormData({ ...formData, bio: e.target.value })
                        }
                        className="input-field"
                        rows={4}
                        placeholder="Cuéntanos sobre ti..."
                      />
                    </div>

                    <div className="flex gap-3">
                      <button
                        onClick={handleSave}
                        disabled={loading}
                        className="btn-primary flex items-center gap-2 disabled:opacity-50"
                      >
                        <Save className="w-4 h-4" />
                        {loading ? 'Guardando...' : 'Guardar Cambios'}
                      </button>
                      <button
                        onClick={handleCancel}
                        disabled={loading}
                        className="px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition-colors flex items-center gap-2"
                      >
                        <X className="w-4 h-4" />
                        Cancelar
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">
                      {profile?.full_name}
                    </h2>
                    {isProfessional && (
                      <span className="badge bg-green-ge text-white mb-3">
                        Profesional
                      </span>
                    )}

                    <div className="space-y-2 mt-4">
                      <div className="flex items-center gap-2 text-gray-600">
                        <Mail className="w-5 h-5" />
                        <span>{user?.email}</span>
                      </div>

                      {profile?.phone && (
                        <div className="flex items-center gap-2 text-gray-600">
                          <Phone className="w-5 h-5" />
                          <span>{profile.phone}</span>
                        </div>
                      )}
                    </div>

                    {profile?.bio && (
                      <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                        <p className="text-gray-700">{profile.bio}</p>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>

          {isProfessional && professionalData && (
            <div className="card p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Briefcase className="text-green-ge" />
                Información Profesional
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Profesión
                  </label>
                  <p className="text-lg font-semibold text-gray-900">
                    {professionalData.profession}
                  </p>
                </div>

                {professionalData.company_name && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Empresa
                    </label>
                    <p className="text-lg font-semibold text-gray-900">
                      {professionalData.company_name}
                    </p>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Años de Experiencia
                  </label>
                  <p className="text-lg font-semibold text-gray-900">
                    {professionalData.years_experience} años
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Calificación
                  </label>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-green-ge">
                      {professionalData.rating.toFixed(1)}
                    </span>
                    <span className="text-gray-600">
                      ({professionalData.total_reviews} reseñas)
                    </span>
                  </div>
                </div>
              </div>

              {professionalData.certifications?.length > 0 && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
                    <Award className="w-5 h-5 text-green-ge" />
                    Certificaciones
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {professionalData.certifications.map((cert: string, idx: number) => (
                      <span key={idx} className="badge badge-warning">
                        {cert}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-6 flex items-center gap-3">
                {professionalData.verified && (
                  <span className="badge bg-green-ge text-white flex items-center gap-2">
                    <Award className="w-4 h-4" />
                    Verificado
                  </span>
                )}
                <span
                  className={`badge ${
                    professionalData.available ? 'badge-success' : 'bg-gray-400 text-white'
                  }`}
                >
                  {professionalData.available ? 'Disponible' : 'No Disponible'}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
