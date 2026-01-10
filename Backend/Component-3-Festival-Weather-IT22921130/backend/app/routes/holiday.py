from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from app.services.holiday_service import holiday_service
from app.models.schemas import HolidayResponse, HolidayCheckResponse
from loguru import logger

router = APIRouter(prefix="/holidays", tags=["Holidays"])

@router.get("", response_model=List[HolidayResponse])
async def get_holidays(
    year: int = Query(None, description="Year (defaults to current year)")
):
    """
    Get all public holidays for Sri Lanka
    
    - **year**: Year to fetch holidays for (optional, defaults to current year)
    """
    try:
        if year is None:
            year = datetime.now().year
        
        holidays = await holiday_service.get_public_holidays(year)
        return holidays
    except Exception as e:
        logger.error(f"Error fetching holidays: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch holidays: {str(e)}")

@router.get("/check", response_model=HolidayCheckResponse)
async def check_holiday(
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    """
    Check if a specific date is a holiday
    
    - **date**: Date to check in YYYY-MM-DD format
    """
    try:
        target_date = datetime.fromisoformat(date)
        holiday = await holiday_service.check_if_holiday(target_date)
        
        return {
            "is_holiday": holiday is not None,
            "holiday": holiday
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error checking holiday: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check holiday: {str(e)}")

@router.get("/upcoming", response_model=List[HolidayResponse])
async def get_upcoming_holidays(
    days: int = Query(30, description="Number of days to look ahead", ge=1, le=365)
):
    """
    Get upcoming holidays within specified days
    
    - **days**: Number of days to look ahead (1-365, default 30)
    """
    try:
        holidays = await holiday_service.get_upcoming_holidays(days)
        return holidays
    except Exception as e:
        logger.error(f"Error fetching upcoming holidays: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch upcoming holidays: {str(e)}")
