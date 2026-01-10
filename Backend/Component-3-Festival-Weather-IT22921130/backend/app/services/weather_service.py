import requests
from typing import Dict, List, Optional
from datetime import datetime
import json
from app.config.redis_client import redis_client
from app.config.settings import settings
from loguru import logger

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache_ttl = settings.WEATHER_CACHE_TTL
    
    async def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather for coordinates"""
        # Check cache first
        cache_key = f"weather:current:{lat}:{lon}"
        cached = await redis_client.get(cache_key)
        
        if cached:
            logger.info(f"Cache hit for weather at {lat},{lon}")
            return json.loads(cached)
        
        try:
            # Fetch from API
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {
                "location": data.get("name", "Unknown"),
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "rainfall": data.get("rain", {}).get("1h", 0),
                "icon": data["weather"][0]["icon"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Cache for configured TTL
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(result))
            logger.info(f"Fetched and cached weather for {lat},{lon}")
            
            return result
            
        except requests.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")
    
    async def get_5day_forecast(self, lat: float, lon: float) -> List[Dict]:
        """Get 5-day weather forecast"""
        cache_key = f"weather:forecast:{lat}:{lon}"
        cached = await redis_client.get(cache_key)
        
        if cached:
            logger.info(f"Cache hit for forecast at {lat},{lon}")
            return json.loads(cached)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast = []
            for item in data["list"]:
                forecast.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "condition": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"],
                    "rainfall": item.get("rain", {}).get("3h", 0),
                    "humidity": item["main"]["humidity"],
                    "icon": item["weather"][0]["icon"]
                })
            
            # Cache for configured TTL
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(forecast))
            logger.info(f"Fetched and cached forecast for {lat},{lon}")
            
            return forecast
            
        except requests.RequestException as e:
            logger.error(f"Forecast API error: {str(e)}")
            raise Exception(f"Failed to fetch forecast data: {str(e)}")
    
    async def get_weather_alerts(self, lat: float, lon: float) -> List[Dict]:
        """Get weather alerts (using OneCall API)"""
        try:
            url = f"{self.base_url}/onecall"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "exclude": "minutely,hourly"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            alerts = data.get("alerts", [])
            
            return [
                {
                    "event": alert.get("event"),
                    "start": alert.get("start"),
                    "end": alert.get("end"),
                    "description": alert.get("description"),
                    "sender": alert.get("sender_name")
                }
                for alert in alerts
            ]
            
        except requests.RequestException as e:
            logger.warning(f"Weather alerts API error: {str(e)}")
            return []  # Return empty list if alerts not available

weather_service = WeatherService()
