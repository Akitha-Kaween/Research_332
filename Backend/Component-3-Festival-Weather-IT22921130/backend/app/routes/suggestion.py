from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.suggestion_engine import suggestion_engine
from app.models.schemas import SuggestionResponse, DashboardResponse
from loguru import logger

router = APIRouter(prefix="/suggestions", tags=["Smart Suggestions"])

@router.get("/smart", response_model=List[SuggestionResponse])
async def get_smart_suggestions(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    crowd_prediction: int = Query(50, description="Crowd prediction (0-100)", ge=0, le=100),
    db: Session = Depends(get_db)
):
    """
    Get smart contextual suggestions based on weather, holidays, and festivals
    
    - **lat**: Latitude
    - **lon**: Longitude
    - **date**: Date in YYYY-MM-DD format
    - **crowd_prediction**: Expected crowd level (0-100, optional, default 50)
    """
    try:
        target_date = datetime.fromisoformat(date).date()
        location = {"lat": lat, "lon": lon}
        
        suggestions = await suggestion_engine.generate_suggestions(
            db, location, target_date, crowd_prediction
        )
        
        return suggestions
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate suggestions: {str(e)}")

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    location_name: str = Query(..., description="Location name (e.g., Kandy, Colombo)"),
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get unified dashboard with weather, holidays, festivals, and smart suggestions
    
    - **location_name**: Name of the location
    - **lat**: Latitude
    - **lon**: Longitude
    - **date**: Date in YYYY-MM-DD format
    """
    try:
        target_date = datetime.fromisoformat(date).date()
        location = {"lat": lat, "lon": lon}
        
        dashboard_data = await suggestion_engine.generate_dashboard_data(
            db, location, location_name, target_date
        )
        
        return dashboard_data
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error generating dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")
