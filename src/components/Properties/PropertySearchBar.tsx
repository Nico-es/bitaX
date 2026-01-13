import { Search, MapPin } from 'lucide-react'

interface PropertySearchBarProps {
  searchQuery: string
  selectedCity: string
  onSearchChange: (query: string) => void
  onCityChange: (city: string) => void
}

const cities = [
  'Todas las ciudades',
  'Malabo',
  'Bata',
  'Ebebiyin',
  'Aconibe',
  'Mongomo',
  'Evinayong',
]

export default function PropertySearchBar({
  searchQuery,
  selectedCity,
  onSearchChange,
  onCityChange,
}: PropertySearchBarProps) {
  return (
    <div className="bg-white border-b border-gray-200 py-4">
      <div className="page-container">
        <div className="flex items-center gap-3 max-w-4xl mx-auto">
          <div className="flex-1 flex items-center bg-white border border-gray-300 hover:shadow-md transition-shadow rounded-full overflow-hidden">
            <div className="flex-1 flex items-center px-6 py-3 border-r border-gray-300">
              <MapPin className="w-5 h-5 text-gray-400 mr-3" />
              <select
                value={selectedCity}
                onChange={(e) => onCityChange(e.target.value)}
                className="flex-1 text-sm font-semibold outline-none cursor-pointer bg-transparent"
              >
                {cities.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex-1 flex items-center px-6 py-3">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
                placeholder="Buscar propiedades..."
                className="flex-1 text-sm font-semibold outline-none placeholder:text-gray-400 placeholder:font-normal"
              />
            </div>

            <button className="m-2 w-10 h-10 bg-gradient-to-r from-green-600 to-green-700 rounded-full flex items-center justify-center hover:scale-105 transition-transform">
              <Search className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
