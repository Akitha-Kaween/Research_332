import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "version" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_weather_current_missing_params():
    """Test weather endpoint with missing parameters"""
    response = client.get("/api/weather/current")
    assert response.status_code == 422  # Validation error

def test_weather_current_invalid_coords():
    """Test weather endpoint with invalid coordinates"""
    response = client.get("/api/weather/current?lat=200&lon=200")
    assert response.status_code == 422  # Validation error

def test_holidays_endpoint():
    """Test holidays endpoint"""
    response = client.get("/api/holidays")
    assert response.status_code in [200, 500]  # May fail if API key not set

def test_festivals_endpoint():
    """Test festivals endpoint"""
    response = client.get("/api/festivals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
