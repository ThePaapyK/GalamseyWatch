from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import GalamseyDetector
from real_data_processor import RealGalamseyDetector
from nasa_data_fetcher import NASADataFetcher
from ml_model import GalamseyMLModel
from nasa_endpoints import router as nasa_router
from real_data_endpoints import router as real_router
from demo_endpoints import router as demo_router
import uvicorn
import ee

# --- Earth Engine Initialization ---
try:
    ee.Initialize()
except Exception as e:
    print("🌍 Earth Engine not initialized. Authenticating and linking to project 'galamsey-ghana'...")
    try:
        ee.Authenticate()
        ee.Initialize(project='galamsey-ghana')
        print("✅ Earth Engine initialized successfully!")
    except Exception as inner_e:
        print(f"❌ Earth Engine initialization failed: {inner_e}")
        print("Please run: earthengine authenticate")


app = FastAPI(title="GalamseyWatch API")
app.include_router(nasa_router)
app.include_router(real_router)
app.include_router(demo_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = GalamseyDetector()
real_detector = RealGalamseyDetector()
data_fetcher = NASADataFetcher()
ml_model = GalamseyMLModel()

@app.get("/")
def read_root():
    return {
        "message": "GalamseyWatch API",
        "data_sources": [
            "NASA Landsat 8/9 Surface Reflectance",
            "MODIS Terra/Aqua NDVI",
            "Hansen Global Forest Change",
            "Sentinel-2 ESA (via NASA Earthdata)"
        ],
        "tools": ["Google Earth Engine", "TensorFlow", "scikit-learn"]
    }

@app.get("/hotspots")
def get_hotspots(region: str = None, start_date: str = "2023-01-01", end_date: str = "2024-01-01"):
    """Get detected galamsey hotspots using comprehensive NASA data"""
    try:
        region_coords = {
            "western": [-3.25, 4.74, -1.5, 6.5],
            "ashanti": [-2.5, 5.5, -0.5, 7.5],
            "eastern": [-1.0, 5.5, 0.5, 7.5]
        }
        
        coords = region_coords.get(region.lower()) if region else None
        results = detector.comprehensive_detection(start_date, end_date, coords)
        hotspots = detector.get_hotspots(results)
        
        return {
            "status": "success", 
            "hotspots": hotspots,
            "data_sources_used": ["Landsat 8/9", "MODIS", "Sentinel-2", "Hansen"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)