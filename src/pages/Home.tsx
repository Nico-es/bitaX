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
    <div className="min-h-screen">
      <div className="gradient-bg text-white">
        <div className="page-container py-20">
          <div className="max-w-4xl mx-auto text-center animate-fade-in">
            <div className="flex justify-center mb-6">
              <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center shadow-2xl">
                <span className="text-6xl">🇬🇶</span>
              </div>
            </div>

            <h1 className="text-6xl font-black mb-4 text-white drop-shadow-lg">
              Bienvenido a abitaX
            </h1>

            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="h-1 w-16 bg-gradient-to-r from-transparent to-white rounded"></div>
              <p className="text-2xl font-bold text-white">
                La SuperApp de Guinea Ecuatorial
              </p>
              <div className="h-1 w-16 bg-gradient-to-l from-transparent to-white rounded"></div>
            </div>

            <p className="text-lg mb-10 text-white/90 max-w-2xl mx-auto leading-relaxed">
              Conectando personas, lugares y servicios en todo el país. Descubre propiedades, encuentra profesionales verificados y accede a servicios de calidad.
            </p>

            <div className="search-bar-enhanced max-w-3xl mx-auto">
              <Search className="text-gray-400 ml-2 w-6 h-6" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar servicios, propiedades, profesionales..."
              />
              <button className="btn-primary px-8 py-3 text-lg font-bold">
                Buscar
              </button>
            </div>

            <div className="grid grid-cols-3 gap-6 mt-12 max-w-2xl mx-auto">
              <div className="stat-card glass-effect">
                <div className="stat-number">500+</div>
                <div className="stat-label">Propiedades</div>
              </div>
              <div className="stat-card glass-effect">
                <div className="stat-number">1000+</div>
                <div className="stat-label">Profesionales</div>
              </div>
              <div className="stat-card glass-effect">
                <div className="stat-number">100+</div>
                <div className="stat-label">Servicios</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="page-container py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <Link
            to="/services"
            className="feature-card group"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-green-ge to-emerald-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <Briefcase className="text-white w-10 h-10" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Servicios</h3>
              <p className="text-gray-600 leading-relaxed">
                Encuentra profesionales verificados para cualquier servicio que necesites
              </p>
            </div>
          </Link>

          <Link
            to="/properties"
            className="feature-card group"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-ge to-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <Building2 className="text-white w-10 h-10" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Propiedades</h3>
              <p className="text-gray-600 leading-relaxed">
                Explora casas, apartamentos y terrenos en venta o alquiler
              </p>
            </div>
          </Link>

          <Link
            to="/professionals"
            className="feature-card group"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <Users className="text-white w-10 h-10" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Profesionales</h3>
              <p className="text-gray-600 leading-relaxed">
                Conecta con expertos calificados en diversas áreas
              </p>
            </div>
          </Link>
        </div>

        <div className="mb-16">
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-3 mb-4">
              <div className="h-1 w-12 bg-gradient-to-r from-transparent to-green-ge rounded"></div>
              <MapPin className="text-green-ge w-8 h-8" />
              <div className="h-1 w-12 bg-gradient-to-l from-transparent to-green-ge rounded"></div>
            </div>
            <h2 className="text-4xl font-black text-gray-900 mb-3">
              Explora Guinea Ecuatorial
            </h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Descubre ubicaciones, propiedades y servicios en todo el territorio nacional
            </p>
          </div>
          <div className="map-container">
            <GoogleMap
              center={{ lat: 1.6508, lng: 10.2679 }}
              zoom={7}
              className="w-full h-[500px]"
            />
          </div>
        </div>

        {topProfessionals.length > 0 && (
          <div className="mb-16">
            <div className="flex items-center justify-between mb-8">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <TrendingUp className="text-green-ge w-8 h-8" />
                  <h2 className="text-4xl font-black text-gray-900">
                    Profesionales Destacados
                  </h2>
                </div>
                <p className="text-gray-600 text-lg ml-11">Los mejores profesionales verificados</p>
              </div>
              <Link
                to="/professionals"
                className="btn-outline px-6 py-3 font-bold hidden md:flex"
              >
                Ver todos →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {topProfessionals.map((professional) => (
                <div key={professional.id} className="feature-card">
                  <div className="flex items-center gap-4 mb-4">
                    {professional.profiles?.avatar_url ? (
                      <img
                        src={professional.profiles.avatar_url}
                        alt={professional.profiles.full_name}
                        className="w-20 h-20 rounded-2xl object-cover shadow-lg"
                      />
                    ) : (
                      <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-green-ge to-emerald-600 flex items-center justify-center text-white text-3xl font-black shadow-lg">
                        {professional.profiles?.full_name?.[0]?.toUpperCase()}
                      </div>
                    )}
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-900 text-lg">{professional.profiles?.full_name}</h3>
                      <p className="text-sm text-gray-600 font-medium">{professional.profession}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-5 h-5 ${i < Math.floor(professional.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
                        />
                      ))}
                    </div>
                    <span className="font-bold text-gray-900">{professional.rating.toFixed(1)}</span>
                    <span className="text-gray-500 text-sm">
                      ({professional.total_reviews} reseñas)
                    </span>
                  </div>
                  {professional.verified && (
                    <div className="pro-badge pro-badge-verified">
                      ✓ Verificado
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {featuredProperties.length > 0 && (
          <div className="mb-16">
            <div className="flex items-center justify-between mb-8">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <Building2 className="text-blue-ge w-8 h-8" />
                  <h2 className="text-4xl font-black text-gray-900">
                    Propiedades Destacadas
                  </h2>
                </div>
                <p className="text-gray-600 text-lg ml-11">Las mejores oportunidades inmobiliarias</p>
              </div>
              <Link
                to="/properties"
                className="btn-outline px-6 py-3 font-bold hidden md:flex"
              >
                Ver todas →
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {featuredProperties.map((property) => (
                <div key={property.id} className="feature-card p-0">
                  {property.images?.[0] ? (
                    <img
                      src={property.images[0]}
                      alt={property.title}
                      className="w-full h-56 object-cover"
                    />
                  ) : (
                    <div className="w-full h-56 bg-gradient-to-br from-blue-ge to-blue-600 flex items-center justify-center">
                      <Building2 className="w-20 h-20 text-white opacity-50" />
                    </div>
                  )}
                  <div className="p-6">
                    <h3 className="font-bold text-gray-900 mb-3 text-xl line-clamp-1">{property.title}</h3>
                    <p className="text-gray-600 mb-4 flex items-center gap-2">
                      <MapPin className="w-5 h-5 text-green-ge" />
                      <span className="font-medium">{property.city}</span>
                    </p>
                    <div className="price-tag mb-4">
                      <span className="price-amount">
                        {property.price.toLocaleString()}
                      </span>
                      <span className="price-currency">{property.currency}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className={`pro-badge ${property.listing_type === 'venta' ? 'pro-badge-new' : 'pro-badge-featured'} capitalize text-xs`}>
                        {property.listing_type}
                      </span>
                      <button className="text-green-ge hover:text-green-dark font-bold text-sm">
                        Ver detalles →
                      </button>
                    </div>
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
