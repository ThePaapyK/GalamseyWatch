'use client'

export default function SimpleMap({ data }) {
  const hotspots = data.filter(d => d.severity > 0.5)
  
  return (
    <div className="bg-gray-100 rounded-lg p-4" style={{ height: '500px' }}>
      <div className="text-center text-gray-600 mb-4">
        🗺️ Interactive Map (Install leaflet to enable full map)
      </div>
      <div className="grid grid-cols-2 gap-2 max-h-96 overflow-y-auto">
        {hotspots.map((point, idx) => (
          <div key={idx} className="bg-white p-3 rounded shadow-sm">
            <div className="font-semibold text-sm">{point.location}</div>
            <div className="text-xs text-gray-600">{point.region}</div>
            <div className={`text-xs font-medium ${
              point.severity > 0.7 ? 'text-red-600' : 'text-orange-600'
            }`}>
              Severity: {point.severity.toFixed(2)}
            </div>
            <div className="text-xs text-gray-500">
              Lat: {point.lat.toFixed(4)}, Lon: {point.lon.toFixed(4)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}