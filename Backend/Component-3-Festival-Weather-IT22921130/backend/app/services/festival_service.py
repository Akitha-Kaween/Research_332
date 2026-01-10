from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.festival import Festival
from app.models.schemas import FestivalCreate, FestivalUpdate
from loguru import logger

class FestivalService:
    def get_all_festivals(self, db: Session, skip: int = 0, limit: int = 100) -> List[Festival]:
        """Get all festivals"""
        return db.query(Festival).filter(Festival.is_active == True).offset(skip).limit(limit).all()
    
    def get_festival_by_id(self, db: Session, festival_id: int) -> Optional[Festival]:
        """Get festival by ID"""
        return db.query(Festival).filter(Festival.id == festival_id).first()
    
    def get_festivals_by_location(self, db: Session, location: str) -> List[Festival]:
        """Get festivals by location"""
        return db.query(Festival).filter(
            Festival.location.ilike(f"%{location}%"),
            Festival.is_active == True
        ).all()
    
    def get_festivals_by_date(self, db: Session, target_date: date) -> List[Festival]:
        """Get festivals happening on a specific date"""
        return db.query(Festival).filter(
            Festival.start_date <= target_date,
            Festival.end_date >= target_date,
            Festival.is_active == True
        ).all()
    
    def get_festivals_by_date_range(
        self, 
        db: Session, 
        start_date: date, 
        end_date: date
    ) -> List[Festival]:
        """Get festivals within a date range"""
        return db.query(Festival).filter(
            Festival.start_date <= end_date,
            Festival.end_date >= start_date,
            Festival.is_active == True
        ).all()
    
    def create_festival(self, db: Session, festival: FestivalCreate) -> Festival:
        """Create a new festival"""
        db_festival = Festival(**festival.dict())
        db.add(db_festival)
        db.commit()
        db.refresh(db_festival)
        logger.info(f"Created festival: {db_festival.name}")
        return db_festival
    
    def update_festival(
        self, 
        db: Session, 
        festival_id: int, 
        festival_update: FestivalUpdate
    ) -> Optional[Festival]:
        """Update a festival"""
        db_festival = self.get_festival_by_id(db, festival_id)
        
        if not db_festival:
            return None
        
        update_data = festival_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_festival, key, value)
        
        db.commit()
        db.refresh(db_festival)
        logger.info(f"Updated festival: {db_festival.name}")
        return db_festival
    
    def delete_festival(self, db: Session, festival_id: int) -> bool:
        """Soft delete a festival"""
        db_festival = self.get_festival_by_id(db, festival_id)
        
        if not db_festival:
            return False
        
        db_festival.is_active = False
        db.commit()
        logger.info(f"Deleted festival: {db_festival.name}")
        return True
    
    def search_festivals(
        self, 
        db: Session, 
        location: Optional[str] = None,
        festival_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Festival]:
        """Search festivals with multiple filters"""
        query = db.query(Festival).filter(Festival.is_active == True)
        
        if location:
            query = query.filter(Festival.location.ilike(f"%{location}%"))
        
        if festival_type:
            query = query.filter(Festival.type == festival_type)
        
        if start_date:
            query = query.filter(Festival.end_date >= start_date)
        
        if end_date:
            query = query.filter(Festival.start_date <= end_date)
        
        return query.all()

festival_service = FestivalService()
