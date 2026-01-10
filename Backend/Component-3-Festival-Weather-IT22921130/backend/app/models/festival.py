from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from app.config.database import Base

class Festival(Base):
    __tablename__ = "festivals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False)
    type = Column(String(50))  # 'outdoor', 'indoor', 'religious', 'cultural'
    description = Column(Text)
    cultural_significance = Column(Text)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "type": self.type,
            "description": self.description,
            "cultural_significance": self.cultural_significance,
            "is_active": self.is_active
        }
