'use client'

import { useEffect, useRef } from 'react'

export default function KeplerGLMap({ data }) {
  const mapRef = useRef()

  useEffect(() => {
    if (typeof window !== 'undefined' && mapRef.current && data) {
      // Load Kepler.gl via CDN
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/kepler.gl@3.0.0/umd/keplergl.min.js'
      script.onload = () => {
        const KeplerGl = window.KeplerGl
        
        const hotspots = data.filter(d => d.severity > 0.3)
        
        const dataset = {
          info: { label: 'Galamsey Hotspots', id: 'galamsey_data' },
          data: {
            fields: [
              { name: 'lat', type: 'real' },
              { name: 'lng', type: 'real' },
              { name: 'location', type: 'string' },
              { name: 'severity', type: 'real' },
              { name: 'region', type: 'string' }
            ],
            rows: hotspots.map(h => [h.lat, h.lon, h.location, h.severity, h.region])
          }
        }

        const config = {
          version: 'v1',
          config: {
            mapState: { latitude: 7.9465, longitude: -1.0232, zoom: 7 },
            visState: {
              layers: [{
                type: 'point',
                config: {
                  dataId: 'galamsey_data',
                  columns: { lat: 'lat', lng: 'lng' },
                  visConfig: {
                    radius: 15,
                    colorField: { name: 'severity', type: 'real' },
                    colorRange: {
                      colors: ['#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026']
                    }
                  }
                }
              }]
            }
          }
        }

        // Initialize Kepler.gl
        const app = KeplerGl({
          mapboxApiAccessToken: 'pk.eyJ1IjoiZGVtbyIsImEiOiJjazl2a2JhZjAwMDAwM29wZmZpZHVvNGNkIn0.demo',
          width: 800,
          height: 500
        })
        
        mapRef.current.appendChild(app)
        
        // Add data
        setTimeout(() => {
          app.addDataToMap({ datasets: [dataset], config })
        }, 100)
      }
      
      document.head.appendChild(script)
    }
  }, [data])

  return (
    <div>
      <div className="mb-2 text-sm text-gray-600">
        Professional Kepler.gl visualization - {data?.filter(d => d.severity > 0.3).length || 0} hotspots
      </div>
      <div ref={mapRef} style={{ height: '500px', width: '100%' }} />
    </div>
  )
}