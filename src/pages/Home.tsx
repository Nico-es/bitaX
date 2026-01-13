import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, MapPin, Briefcase, Building2, Users, Star, TrendingUp } from 'lucide-react'
import { supabase } from '../lib/supabase'
import GoogleMap from '../components/Map/GoogleMap'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [featuredProperties, setFeaturedProperties] = useState<any[]>([])
  const [topProfessionals, setTopProfessionals] = useState<any[]>([])
  const setLoading = () => {}

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const [propertiesRes, professionalsRes] = await Promise.all([
        supabase.from('properties').select('*').eq('available', true).limit(3),
        supabase
          .from('professionals')
          .select('*, profiles(full_name, avatar_url)')
          .eq('available', true)
          .order('rating', { ascending: false })
          .limit(3),
      ])

      if (propertiesRes.data) setFeaturedProperties(propertiesRes.data)
      if (professionalsRes.data) setTopProfessionals(professionalsRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="gradient-bg text-white">
        <div className="page-container py-16">
          <div className="max-w-3xl mx-auto text-center animate-fade-in">
            <h1 className="text-5xl font-bold mb-4">
              Bienvenido a abitaX
            </h1>
            <p className="text-xl mb-8 text-green-light">
              La primera superapp basada en mapas de Guinea Ecuatorial
            </p>
            <p className="text-lg mb-8">
              Conectando personas, lugares y servicios en todo el país
            </p>

            <div className="bg-white rounded-xl shadow-lg p-2 flex items-center gap-2">
              <Search className="text-gray-400 ml-2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar servicios, propiedades, profesionales..."
                className="flex-1 px-4 py-3 text-gray-900 outline-none"
              />
              <button className="btn-primary py-3 px-6">
                Buscar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="page-container py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Link
            to="/services"
            className="card p-6 hover:scale-105 transform transition-all duration-200"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-green-light rounded-lg flex items-center justify-center">
                <Briefcase className="text-green-ge w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Servicios</h3>
                <p className="text-gray-600">
                  Encuentra profesionales para cualquier servicio que necesites
                </p>
              </div>
            </div>
          </Link>

          <Link
            to="/properties"
            className="card p-6 hover:scale-105 transform transition-all duration-200"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Building2 className="text-blue-ge w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Propiedades</h3>
                <p className="text-gray-600">
                  Explora casas, apartamentos y terrenos en venta o alquiler
                </p>
              </div>
            </div>
          </Link>

          <Link
            to="/professionals"
            className="card p-6 hover:scale-105 transform transition-all duration-200"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Users className="text-gold-ge w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Profesionales</h3>
                <p className="text-gray-600">
                  Conecta con expertos verificados en diversas áreas
                </p>
              </div>
            </div>
          </Link>
        </div>

        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <MapPin className="text-green-ge" />
              Explora Guinea Ecuatorial
            </h2>
          </div>
          <div className="card overflow-hidden">
            <GoogleMap
              center={{ lat: 1.6508, lng: 10.2679 }}
              zoom={7}
              className="w-full h-96"
            />
          </div>
        </div>

        {topProfessionals.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <TrendingUp className="text-green-ge" />
                Profesionales Destacados
              </h2>
              <Link to="/professionals" className="text-green-ge hover:text-green-dark font-semibold">
                Ver todos
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {topProfessionals.map((professional) => (
                <div key={professional.id} className="card p-6">
                  <div className="flex items-center gap-4 mb-4">
                    {professional.profiles?.avatar_url ? (
                      <img
                        src={professional.profiles.avatar_url}
                        alt={professional.profiles.full_name}
                        className="w-16 h-16 rounded-full object-cover"
                      />
                    ) : (
                      <div className="w-16 h-16 rounded-full bg-green-ge flex items-center justify-center text-white text-2xl font-bold">
                        {professional.profiles?.full_name?.[0]?.toUpperCase()}
                      </div>
                    )}
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-900">{professional.profiles?.full_name}</h3>
                      <p className="text-sm text-gray-600">{professional.profession}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="w-4 h-4 text-gold-ge fill-current" />
                    <span className="font-semibold">{professional.rating.toFixed(1)}</span>
                    <span className="text-gray-600 text-sm">
                      ({professional.total_reviews} reseñas)
                    </span>
                  </div>
                  {professional.verified && (
                    <span className="badge badge-success">Verificado</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {featuredProperties.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <Building2 className="text-blue-ge" />
                Propiedades Destacadas
              </h2>
              <Link to="/properties" className="text-green-ge hover:text-green-dark font-semibold">
                Ver todas
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {featuredProperties.map((property) => (
                <div key={property.id} className="card overflow-hidden">
                  {property.images?.[0] ? (
                    <img
                      src={property.images[0]}
                      alt={property.title}
                      className="w-full h-48 object-cover"
                    />
                  ) : (
                    <div className="w-full h-48 bg-gradient-to-br from-green-ge to-blue-ge flex items-center justify-center">
                      <Building2 className="w-16 h-16 text-white" />
                    </div>
                  )}
                  <div className="p-4">
                    <h3 className="font-bold text-gray-900 mb-2">{property.title}</h3>
                    <p className="text-sm text-gray-600 mb-2 flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {property.city}
                    </p>
                    <div className="flex items-baseline gap-2 mb-2">
                      <span className="text-2xl font-bold text-green-ge">
                        {property.price.toLocaleString()}
                      </span>
                      <span className="text-gray-600">{property.currency}</span>
                    </div>
                    <span className="badge badge-success capitalize">{property.listing_type}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
