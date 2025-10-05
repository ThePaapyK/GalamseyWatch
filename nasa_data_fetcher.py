import requests
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
import os

class NASADataFetcher:
    def __init__(self, username=None, password=None):
        """Initialize NASA Earthdata credentials"""
        self.username = username or os.getenv('NASA_USERNAME')
        self.password = password or os.getenv('NASA_PASSWORD')
        self.session = requests.Session()
        
        if self.username and self.password:
            self.session.auth = (self.username, self.password)
    
    def get_modis_ndvi(self, bbox, start_date, end_date):
        """Fetch MODIS NDVI data from NASA"""
        # MODIS Terra/Aqua NDVI
        base_url = "https://modis.gsfc.nasa.gov/data/dataprod/"
        
        # Simulate MODIS data structure
        dates = []
        current = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=16)  # MODIS 16-day composite
        
        # Generate synthetic MODIS-like NDVI data
        lats = np.linspace(bbox[1], bbox[3], 50)  # south to north
        lons = np.linspace(bbox[0], bbox[2], 50)  # west to east
        
        ndvi_data = []
        for date in dates:
            # Simulate vegetation patterns
            ndvi = np.random.normal(0.6, 0.2, (50, 50))
            ndvi = np.clip(ndvi, -1, 1)
            ndvi_data.append(ndvi)
        
        # Create xarray dataset
        ds = xr.Dataset({
            'NDVI': (['time', 'lat', 'lon'], ndvi_data)
        }, coords={
            'time': dates,
            'lat': lats,
            'lon': lons
        })
        
        return ds
    
    def get_landsat_surface_reflectance(self, bbox, start_date, end_date):
        """Fetch Landsat 8/9 Surface Reflectance data"""
        # This would typically use USGS API or Google Earth Engine
        # For demo, return structure that matches Landsat bands
        
        bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']  # Landsat 8/9 bands
        
        # Generate synthetic Landsat data
        lats = np.linspace(bbox[1], bbox[3], 100)
        lons = np.linspace(bbox[0], bbox[2], 100)
        
        data_vars = {}
        for band in bands:
            # Different spectral characteristics per band
            if band in ['B2', 'B3', 'B4']:  # Visible
                data = np.random.normal(0.1, 0.05, (100, 100))
            elif band in ['B5', 'B6', 'B7']:  # NIR/SWIR
                data = np.random.normal(0.3, 0.1, (100, 100))
            else:  # Coastal/Aerosol
                data = np.random.normal(0.05, 0.02, (100, 100))
            
            data_vars[band] = (['lat', 'lon'], np.clip(data, 0, 1))
        
        ds = xr.Dataset(data_vars, coords={
            'lat': lats,
            'lon': lons
        })
        
        return ds
    
    def get_hansen_forest_data(self, bbox):
        """Fetch Hansen Global Forest Change data"""
        # Hansen data is typically accessed via Google Earth Engine
        # This simulates the data structure
        
        lats = np.linspace(bbox[1], bbox[3], 200)
        lons = np.linspace(bbox[0], bbox[2], 200)
        
        # Simulate forest cover and loss data
        tree_cover = np.random.exponential(30, (200, 200))  # Tree cover percentage
        tree_cover = np.clip(tree_cover, 0, 100)
        
        # Forest loss (binary)
        forest_loss = np.random.binomial(1, 0.05, (200, 200))
        
        # Loss year (2001-2022)
        loss_year = np.random.randint(1, 23, (200, 200)) * forest_loss
        
        ds = xr.Dataset({
            'treecover2000': (['lat', 'lon'], tree_cover),
            'loss': (['lat', 'lon'], forest_loss),
            'lossyear': (['lat', 'lon'], loss_year)
        }, coords={
            'lat': lats,
            'lon': lons
        })
        
        return ds
    
    def get_sentinel2_data(self, bbox, start_date, end_date):
        """Fetch Sentinel-2 data via NASA Earthdata"""
        # Sentinel-2 bands for vegetation analysis
        bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']  # Blue, Green, Red, NIR, SWIR1, SWIR2
        
        lats = np.linspace(bbox[1], bbox[3], 200)  # Higher resolution
        lons = np.linspace(bbox[0], bbox[2], 200)
        
        data_vars = {}
        for band in bands:
            if band in ['B2', 'B3', 'B4']:  # Visible
                data = np.random.normal(0.08, 0.03, (200, 200))
            elif band == 'B8':  # NIR
                data = np.random.normal(0.4, 0.15, (200, 200))
            else:  # SWIR
                data = np.random.normal(0.2, 0.08, (200, 200))
            
            data_vars[band] = (['lat', 'lon'], np.clip(data, 0, 1))
        
        ds = xr.Dataset(data_vars, coords={
            'lat': lats,
            'lon': lons
        })
        
        return ds
    
    def calculate_indices(self, dataset, sensor='landsat'):
        """Calculate vegetation and soil indices"""
        if sensor == 'landsat':
            # NDVI = (NIR - Red) / (NIR + Red)
            ndvi = (dataset['B5'] - dataset['B4']) / (dataset['B5'] + dataset['B4'])
            
            # NDWI = (Green - NIR) / (Green + NIR)
            ndwi = (dataset['B3'] - dataset['B5']) / (dataset['B3'] + dataset['B5'])
            
            # BSI = ((SWIR1 + Red) - (NIR + Blue)) / ((SWIR1 + Red) + (NIR + Blue))
            bsi = ((dataset['B6'] + dataset['B4']) - (dataset['B5'] + dataset['B2'])) / \
                  ((dataset['B6'] + dataset['B4']) + (dataset['B5'] + dataset['B2']))
        
        elif sensor == 'sentinel2':
            # Sentinel-2 indices
            ndvi = (dataset['B8'] - dataset['B4']) / (dataset['B8'] + dataset['B4'])
            ndwi = (dataset['B3'] - dataset['B8']) / (dataset['B3'] + dataset['B8'])
            bsi = ((dataset['B11'] + dataset['B4']) - (dataset['B8'] + dataset['B2'])) / \
                  ((dataset['B11'] + dataset['B4']) + (dataset['B8'] + dataset['B2']))
        
        # Add indices to dataset
        dataset['NDVI'] = ndvi
        dataset['NDWI'] = ndwi
        dataset['BSI'] = bsi
        
        return dataset

# Usage example
"""
fetcher = NASADataFetcher()

# Ghana bounding box [west, south, east, north]
ghana_bbox = [-3.25, 4.74, 1.19, 11.17]

# Fetch data
modis_data = fetcher.get_modis_ndvi(ghana_bbox, '2023-01-01', '2023-12-31')
landsat_data = fetcher.get_landsat_surface_reflectance(ghana_bbox, '2023-01-01', '2023-12-31')
hansen_data = fetcher.get_hansen_forest_data(ghana_bbox)
sentinel_data = fetcher.get_sentinel2_data(ghana_bbox, '2023-01-01', '2023-12-31')

# Calculate indices
landsat_with_indices = fetcher.calculate_indices(landsat_data, 'landsat')
sentinel_with_indices = fetcher.calculate_indices(sentinel_data, 'sentinel2')
"""