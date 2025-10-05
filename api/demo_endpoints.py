from fastapi import APIRouter
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo_data_processor import DemoGalamseyDetector

router = APIRouter()
demo_detector = DemoGalamseyDetector()

@router.get("/demo-analysis")
def run_demo_analysis():
    """Run demo satellite analysis with realistic data"""
    try:
        results = demo_detector.run_analysis()
        
        # Save for frontend
        with open('demo_galamsey_data.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        return {
            "status": "success",
            "message": "Demo analysis completed",
            "summary": results['summary'],
            "data_type": "Realistic simulation based on actual mining locations"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/demo-hotspots")
def get_demo_hotspots():
    """Get demo hotspots for frontend display"""
    try:
        # Load latest demo results
        with open('demo_galamsey_data.json', 'r') as f:
            results = json.load(f)
        
        return {
            "status": "success",
            "hotspots": results['hotspots'],
            "total_count": len(results['hotspots']),
            "data_source": "Realistic simulation based on actual Ghana mining locations",
            "summary": results['summary']
        }
    except FileNotFoundError:
        # Generate new data if file doesn't exist
        results = demo_detector.run_analysis()
        return {
            "status": "success", 
            "hotspots": results['hotspots'],
            "total_count": len(results['hotspots']),
            "data_source": "Realistic simulation",
            "summary": results['summary']
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}