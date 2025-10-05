#!/usr/bin/env python3
"""
Setup script for real NASA satellite data integration
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🛰️ GalamseyWatch - Real NASA Data Setup")
    print("=" * 50)
    
    # Check if Earth Engine is installed
    print("1. Checking Google Earth Engine...")
    success, stdout, stderr = run_command("python -c 'import ee; print(ee.__version__)'")
    
    if success:
        print(f"✅ Earth Engine installed: {stdout.strip()}")
    else:
        print("❌ Earth Engine not found. Installing...")
        run_command("pip install earthengine-api")
    
    # Check authentication
    print("\n2. Checking Earth Engine authentication...")
    success, stdout, stderr = run_command("python -c 'import ee; ee.Initialize()'")
    
    if success:
        print("✅ Earth Engine authenticated")
    else:
        print("❌ Earth Engine not authenticated")
        print("🔧 Run this command to authenticate:")
        print("   earthengine authenticate")
        print("\n📋 Steps:")
        print("   1. Run: earthengine authenticate")
        print("   2. Follow the browser authentication flow")
        print("   3. Copy the authorization code back to terminal")
        return False
    
    # Test real data access
    print("\n3. Testing real data access...")
    try:
        from real_data_processor import RealGalamseyDetector
        detector = RealGalamseyDetector()
        print("✅ Real data processor ready")
        
        # Quick test
        print("🧪 Running quick test...")
        results = detector.run_real_analysis()
        
        if 'error' not in results:
            print(f"✅ Test successful! Found {len(results.get('hotspots', []))} potential sites")
            print(f"📊 Regions analyzed: {results.get('regions_analyzed', [])}")
        else:
            print(f"❌ Test failed: {results['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Real data processor failed: {e}")
        return False
    
    print("\n🎉 Setup complete! Real NASA data integration ready.")
    print("\n🚀 Next steps:")
    print("   1. Start the API: cd api && python main.py")
    print("   2. Run analysis: GET /real-analysis")
    print("   3. Get results: GET /real-hotspots")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)