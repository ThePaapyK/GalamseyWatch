#!/usr/bin/env python3
"""
Test real Earth Engine access
"""

import ee

def test_earth_engine():
    print("🛰️ Testing Earth Engine Access")
    print("=" * 40)
    
    try:
        # Initialize with project
        ee.Initialize(project='galamsey-ghana')
        print("✅ Earth Engine initialized successfully!")
        
        # Test Ghana data access
        print("📡 Testing Ghana boundary data...")
        ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
            ee.Filter.eq('country_na', 'Ghana')
        )
        
        area = ghana.geometry().area().getInfo()
        print(f"✅ Ghana area: {area/1e9:.0f} km²")
        
        # Test Landsat access
        print("🛰️ Testing Landsat data access...")
        landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(ghana.geometry()) \
            .filterDate('2024-01-01', '2024-02-01') \
            .first()
        
        if landsat:
            print("✅ Landsat data accessible")
            
            # Calculate NDVI
            ndvi = landsat.normalizedDifference(['SR_B5', 'SR_B4'])
            mean_ndvi = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=ghana.geometry(),
                scale=1000,
                maxPixels=1e9
            ).getInfo()
            
            print(f"✅ Mean NDVI for Ghana: {mean_ndvi.get('nd', 'N/A')}")
            
        return True
        
    except Exception as e:
        print(f"❌ Earth Engine test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_earth_engine()
    if success:
        print("\n🎉 Earth Engine ready for real analysis!")
    else:
        print("\n⚠️ Earth Engine not ready yet")