# Festival, Weather & Holiday API
# Student: IT22921130 - Malsha R.J.H

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.routes import weather, holiday, festival, suggestion, agent
from app.config.redis_client import redis_client
from app.config.database import Base, engine

# Create database tables on startup
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run when app starts
    logger.info("Starting Festival-Weather Backend...")
    await redis_client.connect()
    logger.info("Redis connected")
    yield
    # Run when app stops
    logger.info("Shutting down...")
    await redis_client.disconnect()
    logger.info("Redis disconnected")

# Setup FastAPI app

app = FastAPI(
    title="Festival, Weather & Holiday API",
    description="Smart Tourism Planner - Festival/Weather Integration Component (IT22921130)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint - check if API is running
@app.get("/health")
async def health_check():
    return {
        "status": "OK",
        "service": "Festival-Weather Backend",
        "version": "1.0.0",
        "component": "IT22921130"
    }

# Main endpoint - shows API info
@app.get("/")
async def root():
    return {
        "message": "Festival, Weather & Holiday Integration API",
        "component": "IT22921130 - Malsha R.J.H",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "weather": "/api/weather",
            "holidays": "/api/holidays",
            "festivals": "/api/festivals",
            "suggestions": "/api/suggestions"
        }
    }

# Include all route modules
app.include_router(weather.router, prefix="/api")
app.include_router(holiday.router, prefix="/api")
app.include_router(festival.router, prefix="/api")
app.include_router(suggestion.router, prefix="/api")
app.include_router(agent.router, prefix="/agent", tags=["AI Agent"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
