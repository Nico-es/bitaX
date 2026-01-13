import { MapPin, Bed, Bath, Maximize, Heart } from 'lucide-react'
import { useState } from 'react'

interface PropertyCardProps {
  property: {
    id: string
    title: string
    address: string
    city: string
    property_type: string
    listing_type: string
    price: number
    currency: string
    bedrooms?: number
    bathrooms?: number
    area_sqm?: number
    images?: string[]
  }
  onFavorite?: (id: string) => void
}

export default function PropertyCard({ property, onFavorite }: PropertyCardProps) {
  const [isFavorited, setIsFavorited] = useState(false)

  const handleFavorite = (e: React.MouseEvent) => {
    e.preventDefault()
    setIsFavorited(!isFavorited)
    onFavorite?.(property.id)
  }

  const getPropertyTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      house: 'Casa',
      apartment: 'Apartamento',
      land: 'Terreno',
      commercial: 'Comercial',
    }
    return labels[type] || type
  }

  return (
    <div className="group cursor-pointer">
      <div className="relative mb-3">
        <div className="aspect-[4/3] rounded-xl overflow-hidden">
          {property.images?.[0] ? (
            <img
              src={property.images[0]}
              alt={property.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
              <MapPin className="w-16 h-16 text-slate-300" />
            </div>
          )}
        </div>

        <button
          onClick={handleFavorite}
          className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center rounded-full bg-white/90 hover:bg-white hover:scale-110 transition-all shadow-md"
        >
          <Heart
            className={`w-4 h-4 transition-colors ${
              isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-700'
            }`}
          />
        </button>

        <div className="absolute bottom-3 left-3">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white text-gray-900 shadow-md">
            {property.listing_type === 'sale' ? 'En Venta' : 'En Alquiler'}
          </span>
        </div>
      </div>

      <div className="space-y-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-gray-900 line-clamp-1">
            {property.city}
          </h3>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-md whitespace-nowrap">
            {getPropertyTypeLabel(property.property_type)}
          </span>
        </div>

        <p className="text-sm text-gray-600 line-clamp-1">
          {property.title}
        </p>

        <div className="flex items-center gap-3 text-xs text-gray-600">
          {property.bedrooms && (
            <div className="flex items-center gap-1">
              <Bed className="w-3.5 h-3.5" />
              <span>{property.bedrooms}</span>
            </div>
          )}
          {property.bathrooms && (
            <div className="flex items-center gap-1">
              <Bath className="w-3.5 h-3.5" />
              <span>{property.bathrooms}</span>
            </div>
          )}
          {property.area_sqm && (
            <div className="flex items-center gap-1">
              <Maximize className="w-3.5 h-3.5" />
              <span>{property.area_sqm}m²</span>
            </div>
          )}
        </div>

        <div className="pt-1">
          <span className="font-semibold text-gray-900">
            {property.price.toLocaleString()} {property.currency}
          </span>
        </div>
      </div>
    </div>
  )
}
