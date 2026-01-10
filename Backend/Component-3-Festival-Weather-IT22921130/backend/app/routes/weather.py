from fastapi import APIRouter, HTTPException, Query
from app.services.weather_service import weather_service
from app.models.schemas import WeatherResponse, ForecastResponse
from loguru import logger

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Get current weather for given coordinates
    
    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    """
    try:
        weather = await weather_service.get_current_weather(lat, lon)
        return weather
    except Exception as e:
        logger.error(f"Error fetching current weather: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")

@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Get 5-day weather forecast for given coordinates
    
    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    """
    try:
        forecast = await weather_service.get_5day_forecast(lat, lon)
        return {"forecast": forecast}
    except Exception as e:
        logger.error(f"Error fetching forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch forecast data: {str(e)}")

@router.get("/alerts")
async def get_weather_alerts(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Get weather alerts for given coordinates
    
    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    """
    try:
        alerts = await weather_service.get_weather_alerts(lat, lon)
        return {"alerts": alerts}
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather alerts: {str(e)}")
