'use client'

import { useEffect, useRef } from 'react'

export default function SimpleLeafletMap({ data }) {
  const mapRef = useRef()

  useEffect(() => {
    if (typeof window !== 'undefined' && mapRef.current) {
      // Load Leaflet dynamically
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      script.onload = () => {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
        document.head.appendChild(link)

        const L = window.L
        
        // Clear existing map
        if (mapRef.current._leaflet_id) {
          mapRef.current._leaflet_map.remove()
        }
        
        const map = L.map(mapRef.current).setView([7.9465, -1.0232], 7)
        mapRef.current._leaflet_map = map
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map)

        console.log('Data received:', data?.length || 0, 'hotspots')

        // Add hotspot markers
        const hotspots = data?.filter(d => d.severity > 0.3) || []
        console.log('Filtered hotspots:', hotspots.length)
        
        hotspots.forEach((point, index) => {
          const color = point.severity > 0.7 ? '#ef4444' : '#f97316'
          
          L.circleMarker([point.lat, point.lon], {
            color: color,
            fillColor: color,
            fillOpacity: 0.7,
            radius: Math.max(5, point.severity * 15)
          })
          .bindPopup(`
            <div style="font-size: 12px;">
              <strong>${point.location}</strong><br>
              Region: ${point.region}<br>
              Severity: ${point.severity.toFixed(2)}<br>
              NDVI: ${point.ndvi_change?.toFixed(3) || 'N/A'}<br>
              BSI: ${point.bsi_change?.toFixed(3) || 'N/A'}
            </div>
          `)
          .addTo(map)
        })
        
        if (hotspots.length > 0) {
          // Fit map to show all hotspots
          const group = new L.featureGroup(map._layers)
          if (Object.keys(group._layers).length > 0) {
            map.fitBounds(group.getBounds().pad(0.1))
          }
        }
      }
      document.head.appendChild(script)
    }
  }, [data])

  return (
    <div>
      <div className="mb-2 text-sm text-gray-600">
        Showing {data?.filter(d => d.severity > 0.3).length || 0} hotspots
      </div>
      <div ref={mapRef} style={{ height: '500px', width: '100%' }} />
    </div>
  )
}