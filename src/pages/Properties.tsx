import { useState, useEffect } from 'react'
import { Search, MapPin, Building2, Bed, Bath, Maximize, Filter } from 'lucide-react'
import { supabase } from '../lib/supabase'
import GoogleMap from '../components/Map/GoogleMap'

const propertyTypes = ['Todos', 'Casa', 'Apartamento', 'Terreno', 'Comercial']
const listingTypes = ['Todos', 'Venta', 'Alquiler']
const cities = ['Todas', 'Malabo', 'Bata', 'Ebebiyin', 'Aconibe', 'Mongomo', 'Evinayong']

export default function Properties() {
  const [properties, setProperties] = useState<any[]>([])
  const [filteredProperties, setFilteredProperties] = useState<any[]>([])
  const [selectedType, setSelectedType] = useState('Todos')
  const [selectedListing, setSelectedListing] = useState('Todos')
  const [selectedCity, setSelectedCity] = useState('Todas')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [showMap, setShowMap] = useState(false)

  useEffect(() => {
    loadProperties()
  }, [])

  useEffect(() => {
    filterProperties()
  }, [properties, selectedType, selectedListing, selectedCity, searchQuery])

  async function loadProperties() {
    try {
      const { data, error } = await supabase
        .from('properties')
        .select('*')
        .eq('available', true)
        .order('created_at', { ascending: false })

      if (error) throw error
      setProperties(data || [])
    } catch (error) {
      console.error('Error loading properties:', error)
    } finally {
      setLoading(false)
    }
  }

  function filterProperties() {
    let filtered = properties

    if (selectedType !== 'Todos') {
      filtered = filtered.filter(
        (prop) => prop.property_type.toLowerCase() === selectedType.toLowerCase()
      )
    }

    if (selectedListing !== 'Todos') {
      filtered = filtered.filter(
        (prop) => prop.listing_type.toLowerCase() === selectedListing.toLowerCase()
      )
    }

    if (selectedCity !== 'Todas') {
      filtered = filtered.filter(
        (prop) => prop.city.toLowerCase() === selectedCity.toLowerCase()
      )
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (prop) =>
          prop.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          prop.address.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredProperties(filtered)
  }

  const markers = filteredProperties
    .filter((prop) => prop.location)
    .map((prop) => ({
      lat: prop.location.coordinates[1],
      lng: prop.location.coordinates[0],
      title: prop.title,
    }))

  return (
    <div className="min-h-screen bg-gray-50 pb-20 md:pb-8">
      <div className="gradient-bg text-white py-8">
        <div className="page-container">
          <h1 className="text-4xl font-bold mb-4">Propiedades</h1>
          <p className="text-green-light text-lg">
            Encuentra tu próximo hogar o inversión en Guinea Ecuatorial
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
              placeholder="Buscar propiedades..."
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

          <div className="space-y-3">
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              <Filter className="text-gray-600 flex-shrink-0" />
              <span className="text-sm font-medium text-gray-700 whitespace-nowrap">Tipo:</span>
              {propertyTypes.map((type) => (
                <button
                  key={type}
                  onClick={() => setSelectedType(type)}
                  className={`px-4 py-2 rounded-full font-medium whitespace-nowrap transition-colors ${
                    selectedType === type
                      ? 'bg-green-ge text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              <span className="text-sm font-medium text-gray-700 whitespace-nowrap ml-8">
                Operación:
              </span>
              {listingTypes.map((type) => (
                <button
                  key={type}
                  onClick={() => setSelectedListing(type)}
                  className={`px-4 py-2 rounded-full font-medium whitespace-nowrap transition-colors ${
                    selectedListing === type
                      ? 'bg-blue-ge text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              <span className="text-sm font-medium text-gray-700 whitespace-nowrap ml-8">
                Ciudad:
              </span>
              {cities.map((city) => (
                <button
                  key={city}
                  onClick={() => setSelectedCity(city)}
                  className={`px-4 py-2 rounded-full font-medium whitespace-nowrap transition-colors ${
                    selectedCity === city
                      ? 'bg-green-ge text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {city}
                </button>
              ))}
            </div>
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
                <p className="text-gray-600 mt-4">Cargando propiedades...</p>
              </div>
            ) : filteredProperties.length === 0 ? (
              <div className="text-center py-12">
                <Building2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-600 text-lg">No se encontraron propiedades</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredProperties.map((property) => (
                  <div key={property.id} className="card overflow-hidden hover:shadow-xl transition-shadow">
                    {property.images?.[0] ? (
                      <div className="relative">
                        <img
                          src={property.images[0]}
                          alt={property.title}
                          className="w-full h-56 object-cover"
                        />
                        <div className="absolute top-3 right-3">
                          <span
                            className={`badge ${
                              property.listing_type === 'sale'
                                ? 'bg-green-ge text-white'
                                : 'bg-blue-ge text-white'
                            }`}
                          >
                            {property.listing_type === 'sale' ? 'Venta' : 'Alquiler'}
                          </span>
                        </div>
                      </div>
                    ) : (
                      <div className="w-full h-56 bg-gradient-to-br from-green-ge to-blue-ge flex items-center justify-center">
                        <Building2 className="w-20 h-20 text-white" />
                      </div>
                    )}
                    <div className="p-5">
                      <h3 className="font-bold text-xl text-gray-900 mb-2">{property.title}</h3>
                      <p className="text-gray-600 mb-3 flex items-center gap-1">
                        <MapPin className="w-4 h-4 flex-shrink-0" />
                        <span className="line-clamp-1">{property.address}, {property.city}</span>
                      </p>

                      <div className="flex items-center gap-4 mb-4 text-gray-600">
                        {property.bedrooms && (
                          <div className="flex items-center gap-1">
                            <Bed className="w-4 h-4" />
                            <span className="text-sm">{property.bedrooms}</span>
                          </div>
                        )}
                        {property.bathrooms && (
                          <div className="flex items-center gap-1">
                            <Bath className="w-4 h-4" />
                            <span className="text-sm">{property.bathrooms}</span>
                          </div>
                        )}
                        {property.area_sqm && (
                          <div className="flex items-center gap-1">
                            <Maximize className="w-4 h-4" />
                            <span className="text-sm">{property.area_sqm}m²</span>
                          </div>
                        )}
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="badge badge-success capitalize">
                          {property.property_type === 'house' && 'Casa'}
                          {property.property_type === 'apartment' && 'Apartamento'}
                          {property.property_type === 'land' && 'Terreno'}
                          {property.property_type === 'commercial' && 'Comercial'}
                        </span>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-green-ge">
                            {property.price.toLocaleString()}
                          </div>
                          <div className="text-sm text-gray-600">{property.currency}</div>
                        </div>
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
