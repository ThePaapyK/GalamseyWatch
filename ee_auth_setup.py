#!/usr/bin/env python3
"""
Proper Earth Engine authentication setup for GalamseyWatch
"""

import ee
import subprocess
import sys

def setup_earth_engine_auth():
    print("🛰️ Earth Engine Authentication Setup")
    print("=" * 50)
    
    try:
        # Step 1: Authenticate
        print("1. Authenticating with Earth Engine...")
        ee.Authenticate()
        print("✅ Authentication successful!")
        
        # Step 2: Initialize with a project
        print("\n2. Initializing Earth Engine...")
        
        # Try with the provided client project
        project_options = [
            '451577745659',  # From the client ID
            'ee-451577745659',
            'galamsey-watch-451577745659'
        ]
        
        for project in project_options:
            try:
                print(f"   Trying project: {project}")
                ee.Initialize(project=project)
                print(f"✅ Successfully initialized with project: {project}")
                
                # Test with a simple query
                print("\n3. Testing Earth Engine access...")
                ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
                    ee.Filter.eq('country_na', 'Ghana')
                )
                area = ghana.geometry().area().getInfo()
                print(f"✅ Test successful! Ghana area: {area/1e9:.0f} km²")
                
                return project
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                continue
        
        # If no project works, show manual setup
        print("\n🔧 Manual Project Setup Required:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable Earth Engine API")
        print("4. Run: ee.Initialize(project='YOUR_PROJECT_ID')")
        
        return None
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Manual Authentication Required:")
        print("Run: ee.Authenticate()")
        return None

if __name__ == "__main__":
    project = setup_earth_engine_auth()
    if project:
        print(f"\n🎉 Setup complete! Use: ee.Initialize(project='{project}')")
    else:
        print("\n⚠️  Manual setup required")
        sys.exit(1)