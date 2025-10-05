from fastapi import APIRouter
import ee
import json

router = APIRouter()

@router.get("/ee-tiles/{z}/{x}/{y}")
def get_ee_tiles(z: int, x: int, y: int, dataset: str = "landsat"):
    """Get Earth Engine tiles for map display"""
    try:
        if dataset == "landsat":
            # Get latest Landsat composite
            ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
                ee.Filter.eq('country_na', 'Ghana')
            )
            
            landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .filterBounds(ghana.geometry()) \
                .filterDate('2024-01-01', '2024-12-31') \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .median()
            
            # RGB visualization
            vis_params = {
                'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
                'min': 0.0,
                'max': 0.3,
                'gamma': 1.4
            }
            
            # Get tile URL
            tile_url = landsat.getThumbURL({
                'region': ee.Geometry.Rectangle([x, y, x+1, y+1]),
                'dimensions': 256,
                'format': 'png',
                **vis_params
            })
            
            return {"tile_url": tile_url}
            
        elif dataset == "ndvi":
            # NDVI visualization
            ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
                ee.Filter.eq('country_na', 'Ghana')
            )
            
            landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .filterBounds(ghana.geometry()) \
                .filterDate('2024-01-01', '2024-12-31') \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .median()
            
            ndvi = landsat.normalizedDifference(['SR_B5', 'SR_B4'])
            
            vis_params = {
                'min': -1,
                'max': 1,
                'palette': ['red', 'yellow', 'green']
            }
            
            tile_url = ndvi.getThumbURL({
                'region': ee.Geometry.Rectangle([x, y, x+1, y+1]),
                'dimensions': 256,
                'format': 'png',
                **vis_params
            })
            
            return {"tile_url": tile_url}
            
    except Exception as e:
        return {"error": str(e)}

@router.get("/ee-map-id")
def get_ee_map_id(dataset: str = "landsat"):
    """Get Earth Engine map ID for tile layer"""
    try:
        ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
            ee.Filter.eq('country_na', 'Ghana')
        )
        
        if dataset == "landsat":
            landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .filterBounds(ghana.geometry()) \
                .filterDate('2024-01-01', '2024-12-31') \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .median()
            
            vis_params = {
                'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
                'min': 0.0,
                'max': 0.3,
                'gamma': 1.4
            }
            
            map_id = landsat.getMapId(vis_params)
            
        elif dataset == "ndvi":
            landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .filterBounds(ghana.geometry()) \
                .filterDate('2024-01-01', '2024-12-31') \
                .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
                .median()
            
            ndvi = landsat.normalizedDifference(['SR_B5', 'SR_B4'])
            
            vis_params = {
                'min': -1,
                'max': 1,
                'palette': ['red', 'yellow', 'green']
            }
            
            map_id = ndvi.getMapId(vis_params)
        
        return {
            "mapid": map_id['mapid'],
            "token": map_id['token'],
            "tile_url": f"https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/maps/{map_id['mapid']}/tiles/{{z}}/{{x}}/{{y}}?token={map_id['token']}"
        }
        
    except Exception as e:
        return {"error": str(e)}