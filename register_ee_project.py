#!/usr/bin/env python3
"""
Register Earth Engine project and test
"""

import ee
import webbrowser

def register_and_test():
    print("🛰️ Earth Engine Project Registration")
    print("=" * 50)
    
    project_id = "galamsey-ghana"
    
    print(f"1. Project detected: {project_id}")
    print("2. Opening Earth Engine registration page...")
    
    # Open registration URL
    registration_url = f"https://code.earthengine.google.com/register?project={project_id}"
    print(f"   URL: {registration_url}")
    
    try:
        webbrowser.open(registration_url)
        print("✅ Registration page opened in browser")
    except:
        print("⚠️  Please manually open the URL above")
    
    print("\n3. After registration, testing initialization...")
    
    try:
        ee.Initialize(project=project_id)
        print(f"✅ Successfully initialized with project: {project_id}")
        
        # Test with Ghana data
        print("4. Testing Earth Engine access...")
        ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
            ee.Filter.eq('country_na', 'Ghana')
        )
        area = ghana.geometry().area().getInfo()
        print(f"✅ Test successful! Ghana area: {area/1e9:.0f} km²")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("\n📋 Next steps:")
        print("1. Complete registration at the opened URL")
        print("2. Wait 2-3 minutes for activation")
        print("3. Run this script again")
        return False

if __name__ == "__main__":
    success = register_and_test()
    if success:
        print("\n🎉 Earth Engine ready for real NASA data!")
    else:
        print("\n⏳ Registration in progress...")
