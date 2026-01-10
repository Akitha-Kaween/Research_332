from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# Weather Schemas
class WeatherResponse(BaseModel):
    location: str
    temperature: float
    feels_like: float
    condition: str
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    rainfall: float
    icon: str
    timestamp: str

class ForecastItem(BaseModel):
    datetime: str
    temperature: float
    condition: str
    description: str
    rainfall: float
    humidity: int
    icon: str

class ForecastResponse(BaseModel):
    forecast: List[ForecastItem]

# Holiday Schemas
class HolidayResponse(BaseModel):
    name: str
    date: str
    type: List[str]
    description: str
    is_public: bool
    primary_type: str
    country: str

class HolidayCheckResponse(BaseModel):
    is_holiday: bool
    holiday: Optional[HolidayResponse] = None

# Festival Schemas
class FestivalBase(BaseModel):
    name: str
    location: str
    start_date: date
    end_date: date
    type: Optional[str] = None
    description: Optional[str] = None
    cultural_significance: Optional[str] = None

class FestivalCreate(FestivalBase):
    pass

class FestivalUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    type: Optional[str] = None
    description: Optional[str] = None
    cultural_significance: Optional[str] = None
    is_active: Optional[bool] = None

class FestivalResponse(FestivalBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# Suggestion Schemas
class SuggestionResponse(BaseModel):
    type: str  # 'warning', 'alert', 'info', 'recommendation'
    priority: str  # 'high', 'medium', 'low'
    message: str
    rule_id: str
    alternatives: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    cultural_info: Optional[str] = None

class DashboardResponse(BaseModel):
    location: str
    date: str
    weather: WeatherResponse
    holidays: List[HolidayResponse]
    festivals: List[FestivalResponse]
    suggestions: List[SuggestionResponse]
