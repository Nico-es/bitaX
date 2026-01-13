import { useState, useEffect } from 'react'
import { Search, Star, Award, Briefcase, Filter } from 'lucide-react'
import { supabase } from '../lib/supabase'

const professions = [
  'Todos',
  'Construcción',
  'Electricista',
  'Plomero',
  'Carpintero',
  'Pintor',
  'Mecánico',
  'Jardinero',
  'Limpieza',
  'Abogado',
  'Médico',
  'Ingeniero',
  'Arquitecto',
  'Otros',
]

export default function Professionals() {
  const [professionals, setProfessionals] = useState<any[]>([])
  const [filteredProfessionals, setFilteredProfessionals] = useState<any[]>([])
  const [selectedProfession, setSelectedProfession] = useState('Todos')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [verifiedOnly, setVerifiedOnly] = useState(false)

  useEffect(() => {
    loadProfessionals()
  }, [])

  useEffect(() => {
    filterProfessionals()
  }, [professionals, selectedProfession, searchQuery, verifiedOnly])

  async function loadProfessionals() {
    try {
      const { data, error } = await supabase
        .from('professionals')
        .select(`
          *,
          profiles (full_name, avatar_url, phone, bio)
        `)
        .eq('available', true)
        .order('rating', { ascending: false })

      if (error) throw error
      setProfessionals(data || [])
    } catch (error) {
      console.error('Error loading professionals:', error)
    } finally {
      setLoading(false)
    }
  }

  function filterProfessionals() {
    let filtered = professionals

    if (selectedProfession !== 'Todos') {
      filtered = filtered.filter(
        (prof) => prof.profession.toLowerCase() === selectedProfession.toLowerCase()
      )
    }

    if (verifiedOnly) {
      filtered = filtered.filter((prof) => prof.verified)
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (prof) =>
          prof.profiles?.full_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          prof.profession.toLowerCase().includes(searchQuery.toLowerCase()) ||
          prof.company_name?.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredProfessionals(filtered)
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20 md:pb-8">
      <div className="gradient-bg text-white py-8">
        <div className="page-container">
          <h1 className="text-4xl font-bold mb-4">Profesionales</h1>
          <p className="text-green-light text-lg">
            Conecta con expertos verificados en Guinea Ecuatorial
          </p>
        </div>
      </div>

      <div className="page-container py-8">
        <div className="mb-6">
          <div className="bg-white rounded-xl shadow-md p-2 flex items-center gap-2 mb-4">
            <Search className="text-gray-400 ml-2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar profesionales..."
              className="flex-1 px-4 py-3 outline-none"
            />
            <label className="flex items-center gap-2 px-4 py-2 bg-green-light rounded-lg cursor-pointer">
              <input
                type="checkbox"
                checked={verifiedOnly}
                onChange={(e) => setVerifiedOnly(e.target.checked)}
                className="w-4 h-4 text-green-ge rounded"
              />
              <Award className="w-4 h-4 text-green-ge" />
              <span className="text-sm font-medium text-green-dark">Solo Verificados</span>
            </label>
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-2">
            <Filter className="text-gray-600 flex-shrink-0" />
            {professions.map((profession) => (
              <button
                key={profession}
                onClick={() => setSelectedProfession(profession)}
                className={`px-4 py-2 rounded-full font-medium whitespace-nowrap transition-colors ${
                  selectedProfession === profession
                    ? 'bg-green-ge text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {profession}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block w-12 h-12 border-4 border-green-ge border-t-transparent rounded-full animate-spin"></div>
            <p className="text-gray-600 mt-4">Cargando profesionales...</p>
          </div>
        ) : filteredProfessionals.length === 0 ? (
          <div className="text-center py-12">
            <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 text-lg">No se encontraron profesionales</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProfessionals.map((professional) => (
              <div key={professional.id} className="card p-6 hover:shadow-xl transition-shadow">
                <div className="flex items-start gap-4 mb-4">
                  {professional.profiles?.avatar_url ? (
                    <img
                      src={professional.profiles.avatar_url}
                      alt={professional.profiles.full_name}
                      className="w-20 h-20 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-green-ge to-blue-ge flex items-center justify-center text-white text-3xl font-bold">
                      {professional.profiles?.full_name?.[0]?.toUpperCase()}
                    </div>
                  )}
                  <div className="flex-1">
                    <h3 className="font-bold text-xl text-gray-900 mb-1">
                      {professional.profiles?.full_name}
                    </h3>
                    <p className="text-gray-600 font-medium mb-2">{professional.profession}</p>
                    {professional.company_name && (
                      <p className="text-sm text-gray-500">{professional.company_name}</p>
                    )}
                  </div>
                </div>

                {professional.profiles?.bio && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {professional.profiles.bio}
                  </p>
                )}

                <div className="flex items-center gap-3 mb-4">
                  <div className="flex items-center gap-1">
                    <Star className="w-5 h-5 text-gold-ge fill-current" />
                    <span className="font-bold text-lg">{professional.rating.toFixed(1)}</span>
                  </div>
                  <span className="text-gray-600 text-sm">
                    ({professional.total_reviews} reseñas)
                  </span>
                </div>

                <div className="flex items-center gap-2 mb-4">
                  {professional.verified && (
                    <span className="badge bg-green-ge text-white flex items-center gap-1">
                      <Award className="w-3 h-3" />
                      Verificado
                    </span>
                  )}
                  {professional.years_experience > 0 && (
                    <span className="badge badge-success">
                      {professional.years_experience} años exp.
                    </span>
                  )}
                </div>

                {professional.certifications?.length > 0 && (
                  <div className="mb-4">
                    <p className="text-sm font-medium text-gray-700 mb-2">Certificaciones:</p>
                    <div className="flex flex-wrap gap-2">
                      {professional.certifications.slice(0, 3).map((cert: string, idx: number) => (
                        <span key={idx} className="badge badge-warning text-xs">
                          {cert}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <button className="btn-primary w-full">
                  Contactar
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
