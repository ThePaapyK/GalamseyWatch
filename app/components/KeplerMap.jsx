'use client'

import { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import KeplerGl from '@kepler.gl/components'
import { addDataToMap } from '@kepler.gl/actions'

export default function KeplerMap({ data, id = 'galamsey-map' }) {
  const dispatch = useDispatch()

  useEffect(() => {
    if (data && data.length > 0) {
      const hotspots = data.filter(d => d.severity > 0.3)
      
      const dataset = {
        info: {
          label: 'Galamsey Hotspots',
          id: 'galamsey_data'
        },
        data: {
          fields: [
            { name: 'lat', type: 'real' },
            { name: 'lng', type: 'real' },
            { name: 'location', type: 'string' },
            { name: 'severity', type: 'real' },
            { name: 'region', type: 'string' },
            { name: 'ndvi_change', type: 'real' },
            { name: 'bsi_change', type: 'real' }
          ],
          rows: hotspots.map(h => [
            h.lat, 
            h.lon, 
            h.location, 
            h.severity, 
            h.region, 
            h.ndvi_change || 0, 
            h.bsi_change || 0
          ])
        }
      }

      dispatch(addDataToMap({
        datasets: [dataset],
        option: {
          centerMap: true,
          readOnly: false
        }
      }))
    }
  }, [data, dispatch])

  return (
    <div style={{ height: '500px', width: '100%' }}>
      <KeplerGl
        id={id}
        mapboxApiAccessToken="pk.eyJ1IjoiZGVtbyIsImEiOiJjazl2a2JhZjAwMDAwM29wZmZpZHVvNGNkIn0.demo"
        width={800}
        height={500}
      />
    </div>
  )
}