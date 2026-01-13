import { useState, useEffect } from 'react'
import { Search, MapPin, Star, Filter } from 'lucide-react'
import { supabase } from '../lib/supabase'
import GoogleMap from '../components/Map/GoogleMap'

const categories = [
  'Todos',
  'Construcción',
  'Mantenimiento',
  'Electricidad',
  'Plomería',
  'Carpintería',
  'Pintura',
  'Limpieza',
  'Jardinería',
  'Otros',
]

export default function Services() {
  const [services, setServices] = useState<any[]>([])
  const [filteredServices, setFilteredServices] = useState<any[]>([])
  const [selectedCategory, setSelectedCategory] = useState('Todos')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [showMap, setShowMap] = useState(false)

  useEffect(() => {
    loadServices()
  }, [])

  useEffect(() => {
    filterServices()
  }, [services, selectedCategory, searchQuery])

  async function loadServices() {
    try {
      const { data, error } = await supabase
        .from('services')
        .select(`
          *,
          professionals (
            *,
            profiles (full_name, avatar_url)
          )
        `)
        .eq('active', true)
        .order('created_at', { ascending: false })

      if (error) throw error
      setServices(data || [])
    } catch (error) {
      console.error('Error loading services:', error)
    } finally {
      setLoading(false)
    }
  }

  function filterServices() {
    let filtered = services

    if (selectedCategory !== 'Todos') {
      filtered = filtered.filter(
        (service) => service.category.toLowerCase() === selectedCategory.toLowerCase()
      )
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (service) =>
          service.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          service.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredServices(filtered)
  }

  const markers = filteredServices
    .filter((service) => service.location)
    .map((service) => ({
      lat: service.location.coordinates[1],
      lng: service.location.coordinates[0],
      title: service.title,
    }))

  return (
    <div className="min-h-screen bg-gray-50 pb-20 md:pb-8">
      <div className="gradient-bg text-white py-8">
        <div className="page-container">
          <h1 className="text-4xl font-bold mb-4">Servicios</h1>
          <p className="text-green-light text-lg">
            Encuentra profesionales para cualquier servicio que necesites
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
              placeholder="Buscar servicios..."
              className="flex-1 px-4 py-3 outline-none"
            />
            <button
              onClick={() => setShowMap(!showMap)}
              className="btn-secondary py-3 px-6 flex items-center gap-2"
            >
              <MapPin className="w-5 h-5" />
              {showMap ? 'Lista' : 'Mapa'}
            </button>
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-2">
            <Filter className="text-gray-600 flex-shrink-0" />
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full font-medium whitespace-nowrap transition-colors ${
                  selectedCategory === category
                    ? 'bg-green-ge text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {showMap ? (
          <div className="card overflow-hidden mb-8">
            <GoogleMap markers={markers} className="w-full h-[600px]" />
          </div>
        ) : (
          <>
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block w-12 h-12 border-4 border-green-ge border-t-transparent rounded-full animate-spin"></div>
                <p className="text-gray-600 mt-4">Cargando servicios...</p>
              </div>
            ) : filteredServices.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-600 text-lg">No se encontraron servicios</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredServices.map((service) => (
                  <div key={service.id} className="card overflow-hidden hover:shadow-xl transition-shadow">
                    {service.images?.[0] ? (
                      <img
                        src={service.images[0]}
                        alt={service.title}
                        className="w-full h-48 object-cover"
                      />
                    ) : (
                      <div className="w-full h-48 bg-gradient-to-br from-green-ge to-blue-ge"></div>
                    )}
                    <div className="p-5">
                      <div className="flex items-center gap-3 mb-3">
                        {service.professionals?.profiles?.avatar_url ? (
                          <img
                            src={service.professionals.profiles.avatar_url}
                            alt={service.professionals.profiles.full_name}
                            className="w-10 h-10 rounded-full object-cover"
                          />
                        ) : (
                          <div className="w-10 h-10 rounded-full bg-green-ge flex items-center justify-center text-white font-bold">
                            {service.professionals?.profiles?.full_name?.[0]?.toUpperCase()}
                          </div>
                        )}
                        <div className="flex-1">
                          <p className="font-semibold text-gray-900">
                            {service.professionals?.profiles?.full_name}
                          </p>
                          <div className="flex items-center gap-1 text-sm">
                            <Star className="w-3 h-3 text-gold-ge fill-current" />
                            <span>{service.professionals?.rating?.toFixed(1) || '0.0'}</span>
                          </div>
                        </div>
                      </div>

                      <h3 className="font-bold text-lg text-gray-900 mb-2">{service.title}</h3>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                        {service.description}
                      </p>

                      <div className="flex items-center justify-between">
                        <span className="badge badge-success">{service.category}</span>
                        {service.price_from && (
                          <span className="text-lg font-bold text-green-ge">
                            {service.price_from.toLocaleString()} {service.currency}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
