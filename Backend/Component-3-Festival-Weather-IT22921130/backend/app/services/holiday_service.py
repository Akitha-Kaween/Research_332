import requests
from typing import List, Dict, Optional
from datetime import datetime
import json
from app.config.redis_client import redis_client
from app.config.settings import settings
from loguru import logger

class HolidayService:
    def __init__(self):
        self.api_key = settings.CALENDARIFIC_API_KEY
        self.base_url = "https://calendarific.com/api/v2"
        self.cache_ttl = settings.HOLIDAY_CACHE_TTL
    
    async def get_public_holidays(self, year: int = None) -> List[Dict]:
        """Get all public holidays for Sri Lanka"""
        if year is None:
            year = datetime.now().year
        
        # Check cache
        cache_key = f"holidays:LK:{year}"
        cached = await redis_client.get(cache_key)
        
        if cached:
            logger.info(f"Cache hit for holidays {year}")
            return json.loads(cached)
        
        try:
            url = f"{self.base_url}/holidays"
            params = {
                "api_key": self.api_key,
                "country": "LK",  # Sri Lanka
                "year": year
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("meta", {}).get("code") != 200:
                raise Exception(f"API returned error: {data.get('meta', {}).get('error_detail')}")
            
            holidays = []
            for h in data["response"]["holidays"]:
                holidays.append({
                    "name": h["name"],
                    "date": h["date"]["iso"],
                    "type": h["type"],
                    "description": h.get("description", ""),
                    "is_public": "National holiday" in h["type"],
                    "primary_type": h.get("primary_type", ""),
                    "country": h["country"]["name"]
                })
            
            # Cache for configured TTL (24 hours)
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(holidays))
            logger.info(f"Fetched and cached {len(holidays)} holidays for {year}")
            
            return holidays
            
        except requests.RequestException as e:
            logger.error(f"Holiday API error: {str(e)}")
            raise Exception(f"Failed to fetch holiday data: {str(e)}")
    
    async def check_if_holiday(self, date: datetime) -> Optional[Dict]:
        """Check if a specific date is a holiday"""
        holidays = await self.get_public_holidays(date.year)
        
        date_str = date.strftime("%Y-%m-%d")
        
        for holiday in holidays:
            if holiday["date"] == date_str:
                logger.info(f"Found holiday on {date_str}: {holiday['name']}")
                return holiday
        
        logger.info(f"No holiday found on {date_str}")
        return None
    
    async def get_upcoming_holidays(self, days: int = 30) -> List[Dict]:
        """Get upcoming holidays within specified days"""
        holidays = await self.get_public_holidays()
        
        today = datetime.now().date()
        upcoming = []
        
        for holiday in holidays:
            holiday_date = datetime.fromisoformat(holiday["date"]).date()
            days_until = (holiday_date - today).days
            
            if 0 <= days_until <= days:
                holiday["days_until"] = days_until
                upcoming.append(holiday)
        
        # Sort by date
        upcoming.sort(key=lambda x: x["date"])
        
        return upcoming

holiday_service = HolidayService()
