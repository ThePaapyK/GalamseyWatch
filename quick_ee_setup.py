#!/usr/bin/env python3
"""
Quick Earth Engine setup for GalamseyWatch
"""

import ee
import subprocess
import sys

def setup_earth_engine():
    print("🛰️ Quick Earth Engine Setup")
    print("=" * 40)
    
    # Try to initialize with common project names
    project_attempts = [
        'ee-jamesanokye',
        'galamsey-watch',
        'nasa-space-apps-2024',
        None  # Legacy mode
    ]
    
    for project in project_attempts:
        try:
            if project:
                print(f"Trying project: {project}")
                ee.Initialize(project=project)
            else:
                print("Trying legacy mode...")
                ee.Initialize()
            
            print("✅ Earth Engine initialized successfully!")
            
            # Quick test
            ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
                ee.Filter.eq('country_na', 'Ghana')
            )
            area = ghana.geometry().area().getInfo()
            print(f"✅ Test successful! Ghana area: {area/1e9:.0f} km²")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed with project '{project}': {e}")
            continue
    
    print("\n🔧 Manual Setup Required:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project (e.g., 'galamsey-watch')")
    print("3. Enable Earth Engine API")
    print("4. Run: earthengine authenticate --project=YOUR_PROJECT_ID")
    
    return False

if __name__ == "__main__":
    success = setup_earth_engine()
    if not success:
        sys.exit(1)