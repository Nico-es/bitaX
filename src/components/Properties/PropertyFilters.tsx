import { Building2, Home, Landmark, Store, SlidersHorizontal } from 'lucide-react'

interface PropertyFiltersProps {
  selectedType: string
  selectedListing: string
  onTypeChange: (type: string) => void
  onListingChange: (listing: string) => void
  onShowFilters: () => void
}

const propertyCategories = [
  { id: 'all', label: 'Todos', icon: SlidersHorizontal },
  { id: 'house', label: 'Casas', icon: Home },
  { id: 'apartment', label: 'Apartamentos', icon: Building2 },
  { id: 'land', label: 'Terrenos', icon: Landmark },
  { id: 'commercial', label: 'Comercial', icon: Store },
]

export default function PropertyFilters({
  selectedType,
  selectedListing,
  onTypeChange,
  onListingChange,
  onShowFilters,
}: PropertyFiltersProps) {
  return (
    <div className="border-b border-gray-200 bg-white sticky top-0 z-20">
      <div className="page-container">
        <div className="flex items-center gap-8 py-4 overflow-x-auto scrollbar-hide">
          <div className="flex items-center gap-6 flex-shrink-0">
            {propertyCategories.map((category) => {
              const Icon = category.icon
              const isActive = selectedType === category.id
              return (
                <button
                  key={category.id}
                  onClick={() => onTypeChange(category.id)}
                  className={`flex flex-col items-center gap-2 pb-2 border-b-2 transition-colors min-w-[60px] ${
                    isActive
                      ? 'border-gray-900 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-900 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-xs font-semibold whitespace-nowrap">
                    {category.label}
                  </span>
                </button>
              )
            })}
          </div>

          <div className="flex items-center gap-3 ml-auto flex-shrink-0">
            <select
              value={selectedListing}
              onChange={(e) => onListingChange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-semibold hover:border-gray-900 cursor-pointer focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2"
            >
              <option value="all">Todas las operaciones</option>
              <option value="sale">En Venta</option>
              <option value="rent">En Alquiler</option>
            </select>

            <button
              onClick={onShowFilters}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-semibold hover:border-gray-900 transition-colors"
            >
              <SlidersHorizontal className="w-4 h-4" />
              Filtros
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
