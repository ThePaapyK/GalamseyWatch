'use client'

import { useEffect, useState } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'

export default function EarthEngineLayer({ dataset = 'landsat' }) {
  const map = useMap()
  const [layer, setLayer] = useState(null)

  useEffect(() => {
    const fetchEELayer = async () => {
      try {
        const response = await fetch(`http://localhost:8001/ee-map-id?dataset=${dataset}`)
        const data = await response.json()
        
        if (data.tile_url) {
          // Remove existing layer
          if (layer) {
            map.removeLayer(layer)
          }
          
          // Add Earth Engine tile layer
          const eeLayer = L.tileLayer(data.tile_url, {
            attribution: 'Google Earth Engine',
            opacity: 0.7
          })
          
          eeLayer.addTo(map)
          setLayer(eeLayer)
        }
      } catch (error) {
        console.log('Earth Engine layer failed, using fallback')
      }
    }

    fetchEELayer()
    
    return () => {
      if (layer) {
        map.removeLayer(layer)
      }
    }
  }, [dataset, map, layer])

  return null
}