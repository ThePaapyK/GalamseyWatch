from fastapi import APIRouter, BackgroundTasks
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from real_data_processor import RealGalamseyDetector
import json
from datetime import datetime

router = APIRouter()
real_detector = RealGalamseyDetector()

@router.get("/real-analysis")
async def run_real_analysis(background_tasks: BackgroundTasks):
    """Run real NASA satellite data analysis"""
    try:
        # Run analysis in background
        def analyze():
            results = real_detector.run_real_analysis()
            with open('latest_real_analysis.json', 'w') as f:
                json.dump(results, f, indent=2)
        
        background_tasks.add_task(analyze)
        
        return {
            "status": "started",
            "message": "Real satellite data analysis started. Check /real-results for updates.",
            "estimated_time": "2-5 minutes"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/real-results")
def get_real_results():
    """Get latest real analysis results"""
    try:
        with open('latest_real_analysis.json', 'r') as f:
            results = json.load(f)
        
        return {
            "status": "success",
            "data": results,
            "data_source": "Real NASA Landsat 8/9 + MODIS",
            "analysis_type": "Live satellite data"
        }
    except FileNotFoundError:
        return {
            "status": "no_data",
            "message": "No analysis results found. Run /real-analysis first."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/real-hotspots")
def get_real_hotspots():
    """Get real detected hotspots for frontend"""
    try:
        with open('latest_real_analysis.json', 'r') as f:
            results = json.load(f)
        
        if 'hotspots' in results:
            # Format for frontend
            formatted_hotspots = []
            for i, hotspot in enumerate(results['hotspots']):
                formatted_hotspots.append({
                    'location': f"Site_{i+1}",
                    'lat': hotspot['lat'],
                    'lon': hotspot['lon'],
                    'severity': hotspot['severity'],
                    'region': hotspot['region'].title(),
                    'date': results.get('timestamp', datetime.now().isoformat())[:10],
                    'ndvi_change': hotspot['ndvi'],
                    'bsi_change': hotspot['bsi']
                })
            
            return {
                "status": "success",
                "hotspots": formatted_hotspots,
                "total_count": len(formatted_hotspots),
                "data_source": "Real NASA satellite data",
                "regions_analyzed": results.get('regions_analyzed', [])
            }
        else:
            return {"status": "no_hotspots", "message": "No hotspots detected in latest analysis"}
            
    except FileNotFoundError:
        return {
            "status": "no_data", 
            "message": "No real analysis data available. Run /real-analysis first."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}