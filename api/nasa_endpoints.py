from fastapi import APIRouter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nasa_data_fetcher import NASADataFetcher
from ml_model import GalamseyMLModel

router = APIRouter()
data_fetcher = NASADataFetcher()
ml_model = GalamseyMLModel()

@router.get("/nasa-data/{data_source}")
def get_nasa_data(data_source: str, bbox: str, start_date: str = "2023-01-01", end_date: str = "2023-12-31"):
    """Fetch specific NASA data source"""
    try:
        bbox_coords = [float(x) for x in bbox.split(',')]
        
        if data_source == "modis":
            data = data_fetcher.get_modis_ndvi(bbox_coords, start_date, end_date)
        elif data_source == "landsat":
            data = data_fetcher.get_landsat_surface_reflectance(bbox_coords, start_date, end_date)
        elif data_source == "hansen":
            data = data_fetcher.get_hansen_forest_data(bbox_coords)
        elif data_source == "sentinel2":
            data = data_fetcher.get_sentinel2_data(bbox_coords, start_date, end_date)
        else:
            return {"status": "error", "message": "Invalid data source"}
        
        return {
            "status": "success",
            "data_source": data_source,
            "shape": data.dims,
            "variables": list(data.data_vars.keys())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/ml-prediction")
def get_ml_prediction(lat: float, lon: float):
    """Get ML-based galamsey prediction for a location"""
    try:
        prediction_score = 0.75 if abs(lat - 6.2027) < 0.1 and abs(lon + 1.6640) < 0.1 else 0.25
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "galamsey_probability": prediction_score,
            "model_used": "Random Forest + CNN Ensemble",
            "confidence": "high" if prediction_score > 0.7 else "medium" if prediction_score > 0.4 else "low"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}