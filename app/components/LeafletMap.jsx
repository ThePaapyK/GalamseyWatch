'use client'

import { useEffect, useRef } from 'react'

export default function LeafletMap({ data }) {
  const mapRef = useRef()

  useEffect(() => {
    if (typeof window !== 'undefined') {
      import('leaflet').then((L) => {
        if (mapRef.current && !mapRef.current._leaflet_id) {
          const map = L.default.map(mapRef.current).setView([7.9465, -1.0232], 7)
          
          L.default.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

          data.filter(d => d.severity > 0.5).forEach(point => {
            const color = point.severity > 0.7 ? '#ef4444' : '#f97316'
            
            L.default.circleMarker([point.lat, point.lon], {
              color: color,
              fillColor: color,
              fillOpacity: 0.6,
              radius: point.severity * 15
            })
            .bindPopup(`<b>${point.location}</b><br>Severity: ${point.severity.toFixed(2)}`)
            .addTo(map)
          })
        }
      })
    }
  }, [data])

  return <div ref={mapRef} style={{ height: '500px', width: '100%' }} />
}