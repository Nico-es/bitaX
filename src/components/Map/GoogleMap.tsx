import { useEffect, useRef, useState } from 'react'
import { Loader } from '@googlemaps/js-api-loader'

interface GoogleMapProps {
  center?: { lat: number; lng: number }
  zoom?: number
  markers?: Array<{ lat: number; lng: number; title?: string }>
  onMapClick?: (lat: number, lng: number) => void
  className?: string
}

export default function GoogleMap({
  center = { lat: 1.6508, lng: 10.2679 },
  zoom = 8,
  markers = [],
  onMapClick,
  className = 'w-full h-96',
}: GoogleMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const [map, setMap] = useState<google.maps.Map | null>(null)
  const [markersArray, setMarkersArray] = useState<google.maps.Marker[]>([])

  useEffect(() => {
    const loader = new Loader({
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
      version: 'weekly',
    })

    loader.load().then(() => {
      if (mapRef.current && !map) {
        const newMap = new google.maps.Map(mapRef.current, {
          center,
          zoom,
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }],
            },
          ],
        })

        if (onMapClick) {
          newMap.addListener('click', (e: google.maps.MapMouseEvent) => {
            if (e.latLng) {
              onMapClick(e.latLng.lat(), e.latLng.lng())
            }
          })
        }

        setMap(newMap)
      }
    })
  }, [])

  useEffect(() => {
    if (map && center) {
      map.setCenter(center)
    }
  }, [map, center])

  useEffect(() => {
    if (!map) return

    markersArray.forEach((marker) => marker.setMap(null))

    const newMarkers = markers.map((markerPos) => {
      const marker = new google.maps.Marker({
        position: { lat: markerPos.lat, lng: markerPos.lng },
        map,
        title: markerPos.title,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 10,
          fillColor: '#007A33',
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2,
        },
      })

      if (markerPos.title) {
        const infoWindow = new google.maps.InfoWindow({
          content: `<div class="p-2 font-semibold">${markerPos.title}</div>`,
        })

        marker.addListener('click', () => {
          infoWindow.open(map, marker)
        })
      }

      return marker
    })

    setMarkersArray(newMarkers)

    return () => {
      newMarkers.forEach((marker) => marker.setMap(null))
    }
  }, [map, markers])

  return <div ref={mapRef} className={className} />
}
