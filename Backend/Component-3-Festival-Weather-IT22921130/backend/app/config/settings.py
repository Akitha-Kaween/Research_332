from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    OPENWEATHERMAP_API_KEY: str
    CALENDARIFIC_API_KEY: str
    
    # Cache TTL
    WEATHER_CACHE_TTL: int = 3600
    HOLIDAY_CACHE_TTL: int = 86400
    FESTIVAL_CACHE_TTL: int = 86400
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
