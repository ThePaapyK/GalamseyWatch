import ee
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import requests
import xarray as xr

class GalamseyDetector:
    def __init__(self):
       
        
        # Ghana boundaries
        self.ghana = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
            ee.Filter.eq('country_na', 'Ghana')
        )
    
    def calculate_indices(self, image):
        """Calculate vegetation and soil indices"""
        # NDVI (vegetation health)
        ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
        
        # NDWI (water content)
        ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
        
        # BSI (bare soil)
        bsi = image.expression(
            '((RED + SWIR1) - (NIR + BLUE)) / ((RED + SWIR1) + (NIR + BLUE))',
            {
                'RED': image.select('B4'),
                'NIR': image.select('B5'),
                'BLUE': image.select('B2'),
                'SWIR1': image.select('B6')
            }
        ).rename('BSI')
        
        return image.addBands([ndvi, ndwi, bsi])
    
    def detect_changes(self, start_date, end_date, region_coords=None):
        """Detect land cover changes indicating potential mining"""
        
        # Define area of interest
        if region_coords:
            aoi = ee.Geometry.Rectangle(region_coords)
        else:
            aoi = self.ghana.geometry()
        
        # Get Landsat 8 collection
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUD_COVER', 20))
        
        # Calculate indices for each image
        collection_with_indices = collection.map(self.calculate_indices)
        
        # Create before/after composites
        mid_date = datetime.strptime(start_date, '%Y-%m-%d') + \
                  (datetime.strptime(end_date, '%Y-%m-%d') - 
                   datetime.strptime(start_date, '%Y-%m-%d')) / 2
        
        before = collection_with_indices.filterDate(start_date, mid_date.strftime('%Y-%m-%d')).median()
        after = collection_with_indices.filterDate(mid_date.strftime('%Y-%m-%d'), end_date).median()
        
        # Calculate changes
        ndvi_change = after.select('NDVI').subtract(before.select('NDVI')).rename('NDVI_change')
        bsi_change = after.select('BSI').subtract(before.select('BSI')).rename('BSI_change')
        
        # Mining detection criteria:
        # - Significant NDVI decrease (vegetation loss)
        # - Significant BSI increase (soil exposure)
        mining_mask = ndvi_change.lt(-0.2).And(bsi_change.gt(0.15))
        
        return {
            'ndvi_change': ndvi_change,
            'bsi_change': bsi_change,
            'mining_mask': mining_mask,
            'before_image': before,
            'after_image': after
        }
    
    def get_hotspots(self, detection_result, min_area=100):
        """Extract hotspot locations from detection results"""
        
        # Convert mining mask to vectors
        hotspots = detection_result['mining_mask'].selfMask().reduceToVectors(
            geometry=self.ghana.geometry(),
            scale=30,
            maxPixels=1e8
        )
        
        # Filter by minimum area
        hotspots = hotspots.filter(ee.Filter.gte('count', min_area))
        
        return hotspots
    
    def get_modis_data(self, start_date, end_date, aoi=None):
        """Get MODIS vegetation indices"""
        if aoi is None:
            aoi = self.ghana.geometry()
            
        modis = ee.ImageCollection('MODIS/006/MOD13Q1') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .select(['NDVI', 'EVI'])
            
        return modis.median()
    
    def get_sentinel2_data(self, start_date, end_date, aoi=None):
        """Get Sentinel-2 high-resolution data for validation"""
        if aoi is None:
            aoi = self.ghana.geometry()
            
        s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            
        return s2.median().select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    
    def get_forest_change_data(self, aoi=None):
        """Get Hansen Global Forest Change data"""
        if aoi is None:
            aoi = self.ghana.geometry()
            
        hansen = ee.Image('UMD/hansen/global_forest_change_2022_v1_10')
        
        return {
            'forest_loss': hansen.select('loss'),
            'forest_gain': hansen.select('gain'),
            'tree_cover': hansen.select('treecover2000'),
            'loss_year': hansen.select('lossyear')
        }
    
    def create_ml_features(self, landsat_img, modis_img, sentinel_img, hansen_data):
        """Create feature stack for ML model"""
        # Landsat indices
        ndvi_ls = landsat_img.normalizedDifference(['B5', 'B4'])
        ndwi_ls = landsat_img.normalizedDifference(['B3', 'B5'])
        bsi_ls = landsat_img.expression(
            '((RED + SWIR1) - (NIR + BLUE)) / ((RED + SWIR1) + (NIR + BLUE))',
            {
                'RED': landsat_img.select('B4'),
                'NIR': landsat_img.select('B5'),
                'BLUE': landsat_img.select('B2'),
                'SWIR1': landsat_img.select('B6')
            }
        )
        
        # MODIS vegetation indices
        ndvi_modis = modis_img.select('NDVI').multiply(0.0001)
        evi_modis = modis_img.select('EVI').multiply(0.0001)
        
        # Sentinel-2 indices
        ndvi_s2 = sentinel_img.normalizedDifference(['B8', 'B4'])
        
        # Hansen forest data
        tree_cover = hansen_data['tree_cover']
        forest_loss = hansen_data['forest_loss']
        
        # Stack all features
        features = ee.Image.cat([
            ndvi_ls.rename('ndvi_landsat'),
            ndwi_ls.rename('ndwi_landsat'),
            bsi_ls.rename('bsi_landsat'),
            ndvi_modis.rename('ndvi_modis'),
            evi_modis.rename('evi_modis'),
            ndvi_s2.rename('ndvi_sentinel'),
            tree_cover.rename('tree_cover'),
            forest_loss.rename('forest_loss')
        ])
        
        return features
    
    def train_ml_model(self, training_data):
        """Train Random Forest model for galamsey detection"""
        # Prepare training data
        X = training_data.drop(['galamsey'], axis=1)
        y = training_data['galamsey']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = self.rf_model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy:.3f}")
        
        return self.rf_model
    
    def comprehensive_detection(self, start_date, end_date, region_coords=None):
        """Comprehensive galamsey detection using all data sources"""
        aoi = ee.Geometry.Rectangle(region_coords) if region_coords else self.ghana.geometry()
        
        # Get all data sources
        landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
            .median()
            
        modis = self.get_modis_data(start_date, end_date, aoi)
        sentinel = self.get_sentinel2_data(start_date, end_date, aoi)
        hansen = self.get_forest_change_data(aoi)
        
        # Create feature stack
        features = self.create_ml_features(landsat, modis, sentinel, hansen)
        
        # Multi-criteria detection
        # 1. Vegetation loss (NDVI decrease)
        ndvi_threshold = features.select('ndvi_landsat').lt(0.3)
        
        # 2. Soil exposure (BSI increase)
        bsi_threshold = features.select('bsi_landsat').gt(0.2)
        
        # 3. Forest loss from Hansen data
        forest_loss_mask = hansen['forest_loss'].eq(1)
        
        # 4. Water turbidity (NDWI change)
        water_impact = features.select('ndwi_landsat').lt(-0.1)
        
        # Combined detection mask
        galamsey_mask = ndvi_threshold.And(bsi_threshold).And(
            forest_loss_mask.Or(water_impact)
        )
        
        return {
            'detection_mask': galamsey_mask,
            'features': features,
            'landsat': landsat,
            'modis': modis,
            'sentinel': sentinel,
            'hansen': hansen
        }

# Usage example (commented out for demo)
"""
detector = GalamseyDetector()

# Detect changes in Ashanti Region (around Obuasi)
obuasi_coords = [-2.0, 6.0, -1.5, 6.5]  # [west, south, east, north]

results = detector.detect_changes(
    start_date='2023-01-01',
    end_date='2024-01-01',
    region_coords=obuasi_coords
)

hotspots = detector.get_hotspots(results)
print(f"Detected {hotspots.size().getInfo()} potential mining sites")
"""