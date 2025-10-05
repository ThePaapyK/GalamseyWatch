import ee
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

class RealGalamseyDetector:
    def __init__(self):
        """Initialize Earth Engine with real authentication"""
        try:
            # Try with default project first
            ee.Initialize(project='ee-jamesanokye')
            print("✅ Google Earth Engine initialized successfully")
        except Exception as e:
            try:
                # Fallback to no project (legacy mode)
                ee.Initialize()
                print("✅ Google Earth Engine initialized (legacy mode)")
            except Exception as e2:
                print(f"❌ Earth Engine initialization failed: {e2}")
                print("Please create a Google Cloud Project and enable Earth Engine API")
    
    def get_real_landsat_data(self, start_date='2023-01-01', end_date='2024-01-01'):
        """Get real Landsat 8/9 data for Ghana mining regions"""
        
        # Ghana mining regions
        regions = {
            'western': ee.Geometry.Rectangle([-3.25, 4.74, -1.5, 6.5]),
            'ashanti': ee.Geometry.Rectangle([-2.5, 5.5, -0.5, 7.5]),
            'eastern': ee.Geometry.Rectangle([-1.0, 5.5, 0.5, 7.5])
        }
        
        results = {}
        
        for region_name, geometry in regions.items():
            # Get Landsat 8/9 Surface Reflectance
            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')) \
                .filterBounds(geometry) \
                .filterDate(start_date, end_date) \
                .filter(ee.Filter.lt('CLOUD_COVER', 20))
            
            if collection.size().getInfo() > 0:
                # Calculate indices
                def add_indices(image):
                    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
                    ndwi = image.normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI')
                    bsi = image.expression(
                        '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))',
                        {
                            'RED': image.select('SR_B4'),
                            'NIR': image.select('SR_B5'),
                            'BLUE': image.select('SR_B2'),
                            'SWIR1': image.select('SR_B6')
                        }
                    ).rename('BSI')
                    return image.addBands([ndvi, ndwi, bsi])
                
                processed = collection.map(add_indices)
                composite = processed.median()
                
                results[region_name] = {
                    'image': composite,
                    'geometry': geometry,
                    'image_count': collection.size().getInfo()
                }
        
        return results
    
    def detect_real_changes(self, region_data):
        """Detect actual land cover changes"""
        hotspots = []
        
        for region_name, data in region_data.items():
            image = data['image']
            geometry = data['geometry']
            
            # Mining detection criteria (more sensitive)
            ndvi_low = image.select('NDVI').lt(0.4)  # Less vegetation
            bsi_high = image.select('BSI').gt(0.1)   # Some soil exposure
            mining_mask = ndvi_low.Or(bsi_high)      # Either condition
            
            # Sample points from detected areas
            sample_points = mining_mask.selfMask().sample(
                region=geometry,
                scale=30,
                numPixels=50,
                geometries=True
            )
            
            # Convert to list
            points_list = sample_points.getInfo()
            
            for point in points_list['features']:
                coords = point['geometry']['coordinates']
                properties = point['properties']
                
                hotspots.append({
                    'lat': coords[1],
                    'lon': coords[0],
                    'region': region_name,
                    'ndvi': properties.get('NDVI', 0),
                    'bsi': properties.get('BSI', 0),
                    'ndwi': properties.get('NDWI', 0),
                    'severity': min(1.0, max(0.0, properties.get('BSI', 0) - properties.get('NDVI', 0) + 0.5))
                })
        
        return hotspots
    
    def get_modis_ndvi(self, start_date='2023-01-01', end_date='2024-01-01'):
        """Get real MODIS NDVI data"""
        ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
            ee.Filter.eq('country_na', 'Ghana')
        )
        
        modis = ee.ImageCollection('MODIS/006/MOD13Q1') \
            .filterBounds(ghana.geometry()) \
            .filterDate(start_date, end_date) \
            .select('NDVI')
        
        # Calculate mean NDVI
        mean_ndvi = modis.mean().multiply(0.0001)  # Scale factor
        
        # Sample NDVI values
        sample = mean_ndvi.sample(
            region=ghana.geometry(),
            scale=250,
            numPixels=100
        )
        
        return sample.getInfo()
    
    def run_real_analysis(self):
        """Run complete real data analysis"""
        print("🛰️ Starting real NASA satellite data analysis...")
        
        try:
            # Get Landsat data
            print("📡 Fetching Landsat 8/9 data...")
            landsat_data = self.get_real_landsat_data()
            
            # Detect changes
            print("🔍 Detecting land cover changes...")
            hotspots = self.detect_real_changes(landsat_data)
            
            # Get MODIS data
            print("🌿 Fetching MODIS vegetation data...")
            modis_data = self.get_modis_ndvi()
            
            print(f"✅ Analysis complete! Found {len(hotspots)} potential hotspots")
            
            return {
                'hotspots': hotspots,
                'modis_samples': len(modis_data['features']) if modis_data else 0,
                'regions_analyzed': list(landsat_data.keys()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return {'error': str(e)}

# Usage
if __name__ == "__main__":
    detector = RealGalamseyDetector()
    results = detector.run_real_analysis()
    
    # Save results
    with open('real_galamsey_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to real_galamsey_data.json")