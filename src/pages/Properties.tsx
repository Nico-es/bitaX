import { useState, useEffect } from 'react'
import { MapPin, X } from 'lucide-react'
import { supabase } from '../lib/supabase'
import PropertyCard from '../components/Properties/PropertyCard'
import PropertyFilters from '../components/Properties/PropertyFilters'
import PropertySearchBar from '../components/Properties/PropertySearchBar'

export default function Properties() {
  const [properties, setProperties] = useState<any[]>([])
  const [filteredProperties, setFilteredProperties] = useState<any[]>([])
  const [selectedType, setSelectedType] = useState('all')
  const [selectedListing, setSelectedListing] = useState('all')
  const [selectedCity, setSelectedCity] = useState('Todas las ciudades')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [showFiltersModal, setShowFiltersModal] = useState(false)

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

    if (selectedType !== 'all') {
      filtered = filtered.filter(
        (prop) => prop.property_type === selectedType
      )
    }

    if (selectedListing !== 'all') {
      filtered = filtered.filter(
        (prop) => prop.listing_type === selectedListing
      )
    }

    if (selectedCity !== 'Todas las ciudades') {
      filtered = filtered.filter(
        (prop) => prop.city === selectedCity
      )
    }

    if (searchQuery) {
      filtered = filtered.filter(
        (prop) =>
          prop.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          prop.address.toLowerCase().includes(searchQuery.toLowerCase()) ||
          prop.city.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredProperties(filtered)
  }

  return (
    <div className="min-h-screen bg-white pb-20 md:pb-8">
      <PropertySearchBar
        searchQuery={searchQuery}
        selectedCity={selectedCity}
        onSearchChange={setSearchQuery}
        onCityChange={setSelectedCity}
      />

      <PropertyFilters
        selectedType={selectedType}
        selectedListing={selectedListing}
        onTypeChange={setSelectedType}
        onListingChange={setSelectedListing}
        onShowFilters={() => setShowFiltersModal(true)}
      />

      <div className="page-container py-6">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="inline-block w-12 h-12 border-4 border-gray-900 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-gray-600 font-medium">Cargando propiedades...</p>
            </div>
          </div>
        ) : filteredProperties.length === 0 ? (
          <div className="text-center py-20">
            <MapPin className="w-20 h-20 text-gray-300 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              No se encontraron propiedades
            </h3>
            <p className="text-gray-600">
              Intenta ajustar tus filtros o buscar en otra ubicación
            </p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-sm text-gray-600">
                {filteredProperties.length} propiedades encontradas
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-6 gap-y-10">
              {filteredProperties.map((property) => (
                <PropertyCard key={property.id} property={property} />
              ))}
            </div>
          </>
        )}
      </div>

      {showFiltersModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end md:items-center justify-center p-4">
          <div className="bg-white rounded-t-2xl md:rounded-2xl w-full md:max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h3 className="text-lg font-bold">Filtros</h3>
              <button
                onClick={() => setShowFiltersModal(false)}
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6">
              <div className="mb-6">
                <h4 className="font-semibold mb-3">Tipo de operación</h4>
                <div className="space-y-2">
                  {['all', 'sale', 'rent'].map((type) => (
                    <label key={type} className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="radio"
                        name="listing"
                        checked={selectedListing === type}
                        onChange={() => setSelectedListing(type)}
                        className="w-4 h-4"
                      />
                      <span className="text-sm">
                        {type === 'all' && 'Todas las operaciones'}
                        {type === 'sale' && 'En Venta'}
                        {type === 'rent' && 'En Alquiler'}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <h4 className="font-semibold mb-3">Tipo de propiedad</h4>
                <div className="space-y-2">
                  {['all', 'house', 'apartment', 'land', 'commercial'].map((type) => (
                    <label key={type} className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="radio"
                        name="property"
                        checked={selectedType === type}
                        onChange={() => setSelectedType(type)}
                        className="w-4 h-4"
                      />
                      <span className="text-sm">
                        {type === 'all' && 'Todos los tipos'}
                        {type === 'house' && 'Casas'}
                        {type === 'apartment' && 'Apartamentos'}
                        {type === 'land' && 'Terrenos'}
                        {type === 'commercial' && 'Comercial'}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="sticky bottom-0 bg-white border-t border-gray-200 px-6 py-4 flex items-center gap-3">
              <button
                onClick={() => {
                  setSelectedType('all')
                  setSelectedListing('all')
                  setSelectedCity('Todas las ciudades')
                  setSearchQuery('')
                }}
                className="flex-1 px-6 py-3 border border-gray-900 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Limpiar filtros
              </button>
              <button
                onClick={() => setShowFiltersModal(false)}
                className="flex-1 px-6 py-3 bg-gray-900 text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
              >
                Mostrar propiedades
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
