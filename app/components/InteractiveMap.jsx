'use client'

import { useEffect, useRef } from 'react'

export default function InteractiveMap({ data }) {
  const mapRef = useRef()

  useEffect(() => {
    if (typeof window !== 'undefined' && mapRef.current) {
      // Create map with OpenStreetMap
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      script.onload = () => {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
        document.head.appendChild(link)

        const L = window.L
        const map = L.map(mapRef.current).setView([7.9465, -1.0232], 7)
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map)

        // Add hotspot markers
        data.filter(d => d.severity > 0.5).forEach(point => {
          const color = point.severity > 0.7 ? '#ef4444' : '#f97316'
          
          L.circleMarker([point.lat, point.lon], {
            color: color,
            fillColor: color,
            fillOpacity: 0.6,
            radius: point.severity * 15
          })
          .bindPopup(`
            <div class="p-2">
              <h3 class="font-bold">${point.location}</h3>
              <p>Region: ${point.region}</p>
              <p>Severity: ${point.severity.toFixed(2)}</p>
              <p>NDVI Change: ${point.ndvi_change.toFixed(3)}</p>
              <p>BSI Change: ${point.bsi_change.toFixed(3)}</p>
            </div>
          `)
          .addTo(map)
        })
      }
      document.head.appendChild(script)
    }
  }, [data])

  return <div ref={mapRef} style={{ height: '500px', width: '100%' }} />
}