from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.festival_service import festival_service
from app.models.schemas import FestivalResponse, FestivalCreate, FestivalUpdate
from loguru import logger

router = APIRouter(prefix="/festivals", tags=["Festivals"])

@router.get("", response_model=List[FestivalResponse])
def get_all_festivals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get all festivals
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        festivals = festival_service.get_all_festivals(db, skip, limit)
        return festivals
    except Exception as e:
        logger.error(f"Error fetching festivals: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch festivals: {str(e)}")

@router.get("/{festival_id}", response_model=FestivalResponse)
def get_festival(
    festival_id: int,
    db: Session = Depends(get_db)
):
    """
    Get festival by ID
    
    - **festival_id**: Festival ID
    """
    festival = festival_service.get_festival_by_id(db, festival_id)
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    return festival

@router.get("/search/by-location", response_model=List[FestivalResponse])
def search_by_location(
    location: str = Query(..., description="Location to search"),
    db: Session = Depends(get_db)
):
    """
    Search festivals by location
    
    - **location**: Location name (partial match supported)
    """
    try:
        festivals = festival_service.get_festivals_by_location(db, location)
        return festivals
    except Exception as e:
        logger.error(f"Error searching festivals: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search festivals: {str(e)}")

@router.get("/search/by-date", response_model=List[FestivalResponse])
def search_by_date(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get festivals happening on a specific date
    
    - **date**: Date in YYYY-MM-DD format
    """
    try:
        target_date = datetime.fromisoformat(date).date()
        festivals = festival_service.get_festivals_by_date(db, target_date)
        return festivals
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error searching festivals by date: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search festivals: {str(e)}")

@router.get("/search/advanced", response_model=List[FestivalResponse])
def advanced_search(
    location: Optional[str] = Query(None),
    festival_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Advanced festival search with multiple filters
    
    - **location**: Location name (optional)
    - **festival_type**: Festival type (optional)
    - **start_date**: Start date in YYYY-MM-DD format (optional)
    - **end_date**: End date in YYYY-MM-DD format (optional)
    """
    try:
        start = datetime.fromisoformat(start_date).date() if start_date else None
        end = datetime.fromisoformat(end_date).date() if end_date else None
        
        festivals = festival_service.search_festivals(
            db, location, festival_type, start, end
        )
        return festivals
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error in advanced search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search festivals: {str(e)}")

@router.post("", response_model=FestivalResponse, status_code=201)
def create_festival(
    festival: FestivalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new festival (Admin only)
    
    - **festival**: Festival data
    """
    try:
        new_festival = festival_service.create_festival(db, festival)
        return new_festival
    except Exception as e:
        logger.error(f"Error creating festival: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create festival: {str(e)}")

@router.put("/{festival_id}", response_model=FestivalResponse)
def update_festival(
    festival_id: int,
    festival_update: FestivalUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a festival (Admin only)
    
    - **festival_id**: Festival ID
    - **festival_update**: Updated festival data
    """
    try:
        updated_festival = festival_service.update_festival(db, festival_id, festival_update)
        if not updated_festival:
            raise HTTPException(status_code=404, detail="Festival not found")
        return updated_festival
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating festival: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update festival: {str(e)}")

@router.delete("/{festival_id}", status_code=204)
def delete_festival(
    festival_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a festival (Admin only)
    
    - **festival_id**: Festival ID
    """
    try:
        success = festival_service.delete_festival(db, festival_id)
        if not success:
            raise HTTPException(status_code=404, detail="Festival not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting festival: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete festival: {str(e)}")
