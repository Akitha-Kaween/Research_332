# API Documentation - Festival & Weather Component

**Component:** IT22921130 - Malsha R.J.H  
**API Type:** RESTful API with External API Integration  
**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Overview](#overview)
2. [System Logic and Integration](#system-logic-and-integration)
3. [API Endpoints](#api-endpoints)
4. [Testing Guide](#testing-guide)
5. [Integration with Final Product](#integration-with-final-product)
6. [Error Handling](#error-handling)

---

## Overview

### Purpose

This API provides festival calendar, weather information, and public holiday data for tourists visiting Sri Lanka. It integrates external APIs (OpenWeatherMap, Calendarific) with a local festival database to provide comprehensive tourism information.

### Technology Stack

**Backend Framework:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)

**Database:**
- SQLite (local database)
- SQLAlchemy (ORM)

**External APIs:**
- OpenWeatherMap (weather data)
- Calendarific (holiday data)

**Caching:**
- Redis (optional, for performance)

**API Features:**
- RESTful design
- JSON responses
- Real-time weather data
- Festival database
- Smart suggestions
- Caching for performance

---

## System Logic and Integration

### Architecture Overview

```
┌──────────────────────────────────────┐
│         Client Request               │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│      FastAPI Backend (Port 8000)     │
│  ┌────────────────────────────────┐  │
│  │   Route Layer                  │  │
│  │  - Weather routes              │  │
│  │  - Holiday routes              │  │
│  │  - Festival routes             │  │
│  │  - Suggestion routes           │  │
│  └────────┬───────────────────────┘  │
│           │                           │
│  ┌────────▼───────────────────────┐  │
│  │   Business Logic Layer         │  │
│  │  - Data validation             │  │
│  │  - API integration             │  │
│  │  - Cache management            │  │
│  │  - Response formatting         │  │
│  └────────┬───────────────────────┘  │
└───────────┼───────────────────────────┘
            │
     ┌──────┴──────────┬──────────────┐
     │                 │              │
┌────▼────┐    ┌──────▼──────┐  ┌───▼────┐
│ SQLite  │    │   Redis     │  │External│
│Database │    │   Cache     │  │  APIs  │
│         │    │  (Optional) │  │        │
│Festivals│    │             │  │Weather │
│         │    │             │  │Holidays│
└─────────┘    └─────────────┘  └────────┘
```

### Data Flow

**1. Weather Request Flow:**
```
Client → FastAPI → Check Redis Cache
                ↓ (if not cached)
         OpenWeatherMap API → Parse Response
                ↓
         Cache in Redis (30 min TTL)
                ↓
         Return to Client
```

**2. Festival Request Flow:**
```
Client → FastAPI → SQLite Database
                ↓
         Query festivals table
                ↓
         Filter by month/location
                ↓
         Return to Client
```

**3. Holiday Request Flow:**
```
Client → FastAPI → Check Redis Cache
                ↓ (if not cached)
         Calendarific API → Parse Response
                ↓
         Cache in Redis (30 days TTL)
                ↓
         Return to Client
```

**4. Smart Suggestions Flow:**
```
Client → FastAPI → Parallel Requests:
                ├→ Get Weather
                ├→ Get Festivals
                └→ Get Holidays
                ↓
         Combine all data
                ↓
         Generate recommendations
                ↓
         Return to Client
```

### External API Integration Logic

**OpenWeatherMap Integration:**

## 6. AI Agent (Research Component)

The AI Agent acts as an integrated "Travel Assistant". It handles general queries using the LLM and specific actions (Tour Planning, Weather) using Tools.

### Chat with Agent
**Endpoint**: `POST /agent/chat`

**Description**: Sends a message to the AI. The AI automatically detects intent (Plan Tour / Weather / Chat).

**Request Body**:
```json
{
  "message": "Plan a tour for me in Kandy"
}
```

**Response**:
```json
{
  "response": "I have optimized your Kandy tour using the Genetic Algorithm. (Map available at ...)",
  "action_type": "map" 
}
```
*   `action_type` can be: `chat`, `map`, `weather`, `crowd`, `error`.
*   If `action_type` is `map`, the `response` contains the link to the generated HTML map.
```python
import requests

async def fetch_weather(city: str):
    # API configuration
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Celsius
    }
    
    # Check cache first
    cache_key = f"weather:{city}"
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Make API request
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache for 30 minutes
        await redis_client.setex(
            cache_key,
            1800,  # 30 minutes
            json.dumps(weather_data)
        )
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        # Return cached data if available, even if expired
        if cached_data:
            return json.loads(cached_data)
        raise HTTPException(503, "Weather service unavailable")
```

**Calendarific Integration:**

```python
async def fetch_holidays(year: int, country: str = "LK"):
    # API configuration
    base_url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": CALENDARIFIC_API_KEY,
        "country": country,  # LK = Sri Lanka
        "year": year
    }
    
    # Check cache first (holidays don't change)
    cache_key = f"holidays:{country}:{year}"
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Make API request
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract holidays
        holidays = []
        for holiday in data["response"]["holidays"]:
            holidays.append({
                "name": holiday["name"],
                "date": holiday["date"]["iso"],
                "type": holiday["type"],
                "description": holiday.get("description", "")
            })
        
        # Cache for 30 days
        await redis_client.setex(
            cache_key,
            2592000,  # 30 days
            json.dumps(holidays)
        )
        
        return holidays
        
    except requests.exceptions.RequestException as e:
        if cached_data:
            return json.loads(cached_data)
        raise HTTPException(503, "Holiday service unavailable")
```

### Database Operations Logic

**Festival CRUD Operations:**

```python
from sqlalchemy.orm import Session
from app.models import Festival

# Create
def create_festival(db: Session, festival_data: dict):
    festival = Festival(**festival_data)
    db.add(festival)
    db.commit()
    db.refresh(festival)
    return festival

# Read
def get_festivals_by_month(db: Session, month: int):
    return db.query(Festival).filter(
        Festival.month == month
    ).all()

def get_festival_by_id(db: Session, festival_id: int):
    return db.query(Festival).filter(
        Festival.id == festival_id
    ).first()

# Update
def update_festival(db: Session, festival_id: int, updates: dict):
    festival = get_festival_by_id(db, festival_id)
    if not festival:
        return None
    
    for key, value in updates.items():
        setattr(festival, key, value)
    
    db.commit()
    db.refresh(festival)
    return festival

# Delete
def delete_festival(db: Session, festival_id: int):
    festival = get_festival_by_id(db, festival_id)
    if not festival:
        return False
    
    db.delete(festival)
    db.commit()
    return True

# Search
def search_festivals(db: Session, query: str = None, 
                     location: str = None, category: str = None):
    filters = []
    
    if query:
        filters.append(Festival.name.contains(query))
    if location:
        filters.append(Festival.location == location)
    if category:
        filters.append(Festival.category == category)
    
    return db.query(Festival).filter(*filters).all()
```

---

## API Endpoints

### 1. Root Endpoint

**Endpoint:** `GET /`

**Purpose:** API information

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
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
```

---

### 2. Health Check

**Endpoint:** `GET /health`

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "OK",
  "service": "Festival-Weather Backend",
  "version": "1.0.0",
  "component": "IT22921130"
}
```

---

### Weather Endpoints

#### 3. Get Current Weather

**Endpoint:** `GET /api/weather/current?city={city}`

**Purpose:** Get real-time weather for a city

**Request:**
```bash
curl "http://localhost:8000/api/weather/current?city=Colombo"
```

**Response:**
```json
{
  "city": "Colombo",
  "temperature": 28.5,
  "feels_like": 32.1,
  "humidity": 75,
  "description": "scattered clouds",
  "wind_speed": 3.5,
  "timestamp": "2026-01-03T19:00:00"
}
```

**Query Parameters:**
- `city` (required): City name (e.g., Colombo, Kandy, Galle)

**Status Codes:**
- `200`: Success
- `404`: City not found
- `503`: Weather service unavailable

---

#### 4. Get Weather Forecast

**Endpoint:** `GET /api/weather/forecast?city={city}&days={days}`

**Purpose:** Get weather forecast for upcoming days

**Request:**
```bash
curl "http://localhost:8000/api/weather/forecast?city=Colombo&days=5"
```

**Response:**
```json
{
  "city": "Colombo",
  "forecast": [
    {
      "date": "2026-01-04",
      "temp_max": 30,
      "temp_min": 25,
      "description": "partly cloudy",
      "rain_probability": 20
    },
    {
      "date": "2026-01-05",
      "temp_max": 29,
      "temp_min": 24,
      "description": "light rain",
      "rain_probability": 60
    }
  ]
}
```

**Query Parameters:**
- `city` (required): City name
- `days` (optional): Number of days (default: 5, max: 7)

---

### Holiday Endpoints

#### 5. Get Holidays by Year

**Endpoint:** `GET /api/holidays?year={year}`

**Purpose:** Get all public holidays for a year

**Request:**
```bash
curl "http://localhost:8000/api/holidays?year=2026"
```

**Response:**
```json
{
  "year": 2026,
  "country": "Sri Lanka",
  "holidays": [
    {
      "name": "Sinhala and Tamil New Year",
      "date": "2026-04-14",
      "type": ["National holiday"],
      "description": "Traditional New Year celebration"
    },
    {
      "name": "Vesak Full Moon Poya Day",
      "date": "2026-05-23",
      "type": ["National holiday"],
      "description": "Buddhist festival celebrating Buddha's birth"
    }
  ]
}
```

**Query Parameters:**
- `year` (required): Year (e.g., 2026)

---

#### 6. Get Holidays by Month

**Endpoint:** `GET /api/holidays/month?year={year}&month={month}`

**Purpose:** Get holidays for a specific month

**Request:**
```bash
curl "http://localhost:8000/api/holidays/month?year=2026&month=5"
```

**Response:**
```json
{
  "year": 2026,
  "month": 5,
  "holidays": [
    {
      "name": "Vesak Full Moon Poya Day",
      "date": "2026-05-23",
      "type": ["National holiday"]
    }
  ]
}
```

---

### Festival Endpoints

#### 7. Get All Festivals

**Endpoint:** `GET /api/festivals`

**Purpose:** Get all festivals in database

**Request:**
```bash
curl http://localhost:8000/api/festivals
```

**Response:**
```json
{
  "festivals": [
    {
      "id": 1,
      "name": "Esala Perahera",
      "description": "Grand procession in Kandy with decorated elephants",
      "location": "Kandy",
      "month": 7,
      "day": 15,
      "duration_days": 10,
      "category": "Buddhist",
      "significance": "Cultural",
      "tourist_friendly": true
    }
  ]
}
```

---

#### 8. Get Festivals by Month

**Endpoint:** `GET /api/festivals/month/{month}`

**Purpose:** Get festivals happening in a specific month

**Request:**
```bash
curl http://localhost:8000/api/festivals/month/7
```

**Response:**
```json
{
  "month": 7,
  "festivals": [
    {
      "id": 1,
      "name": "Esala Perahera",
      "location": "Kandy",
      "month": 7,
      "day": 15,
      "duration_days": 10
    },
    {
      "id": 2,
      "name": "Nallur Festival",
      "location": "Jaffna",
      "month": 7,
      "day": 20,
      "duration_days": 25
    }
  ]
}
```

---

#### 9. Get Festival by ID

**Endpoint:** `GET /api/festivals/{festival_id}`

**Purpose:** Get detailed information about a specific festival

**Request:**
```bash
curl http://localhost:8000/api/festivals/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Esala Perahera",
  "description": "The Esala Perahera is a grand festival held in Kandy, featuring a spectacular procession with beautifully decorated elephants, traditional dancers, and drummers. It celebrates the sacred tooth relic of Buddha.",
  "location": "Kandy",
  "month": 7,
  "day": 15,
  "duration_days": 10,
  "category": "Buddhist",
  "significance": "Cultural and Religious",
  "tourist_friendly": true,
  "created_at": "2026-01-03T10:00:00",
  "updated_at": "2026-01-03T10:00:00"
}
```

---

#### 10. Search Festivals

**Endpoint:** `GET /api/festivals/search?query={query}&location={location}&category={category}`

**Purpose:** Search festivals by various criteria

**Request:**
```bash
curl "http://localhost:8000/api/festivals/search?query=perahera&location=Kandy"
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Esala Perahera",
      "location": "Kandy",
      "month": 7,
      "category": "Buddhist"
    }
  ],
  "count": 1
}
```

**Query Parameters:**
- `query` (optional): Search in festival names
- `location` (optional): Filter by location
- `category` (optional): Filter by category (Buddhist, Hindu, etc.)

---

#### 11. Create Festival (Admin)

**Endpoint:** `POST /api/festivals`

**Purpose:** Add a new festival to database

**Request:**
```bash
curl -X POST http://localhost:8000/api/festivals \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Galle Literary Festival",
    "description": "Annual literary festival in Galle Fort",
    "location": "Galle",
    "month": 1,
    "day": 20,
    "duration_days": 4,
    "category": "Cultural",
    "significance": "Literary",
    "tourist_friendly": true
  }'
```

**Response:**
```json
{
  "id": 11,
  "name": "Galle Literary Festival",
  "location": "Galle",
  "month": 1,
  "day": 20,
  "created_at": "2026-01-03T19:00:00"
}
```

---

#### 12. Update Festival (Admin)

**Endpoint:** `PUT /api/festivals/{festival_id}`

**Purpose:** Update festival information

**Request:**
```bash
curl -X PUT http://localhost:8000/api/festivals/11 \
  -H "Content-Type: application/json" \
  -d '{
    "duration_days": 5,
    "description": "Updated description"
  }'
```

---

#### 13. Delete Festival (Admin)

**Endpoint:** `DELETE /api/festivals/{festival_id}`

**Purpose:** Remove a festival from database

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/festivals/11
```

**Response:**
```json
{
  "message": "Festival deleted successfully",
  "id": 11
}
```

---

### Suggestion Endpoints

#### 14. Get Smart Suggestions

**Endpoint:** `GET /api/suggestions?date={date}&location={location}`

**Purpose:** Get comprehensive suggestions combining weather, festivals, and holidays

**Request:**
```bash
curl "http://localhost:8000/api/suggestions?date=2026-08-15&location=Kandy"
```

**Response:**
```json
{
  "date": "2026-08-15",
  "location": "Kandy",
  "weather": {
    "temperature": 25,
    "description": "partly cloudy",
    "suitable_for_outdoor": true
  },
  "festivals": [
    {
      "name": "Esala Perahera",
      "status": "ongoing",
      "days_remaining": 3,
      "location": "Kandy"
    }
  ],
  "holidays": [],
  "recommendations": [
    "Great time to visit Kandy!",
    "Esala Perahera is happening - don't miss it!",
    "Weather is pleasant for outdoor activities",
    "Book accommodation early - festival period"
  ],
  "crowd_level": "high",
  "best_time_to_visit": "early morning or late evening"
}
```

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format
- `location` (required): City name

**Use Case:** Provide tourists with all relevant information for trip planning

---

## Testing Guide

### Manual Testing Script

**Test Script:** `tests/test_api.py`

```python
import requests
import json

BASE_URL = "http://localhost:8000"

print("="*60)
print("TESTING FESTIVAL & WEATHER API")
print("="*60)

# Test 1: Health Check
print("\n1. Testing /health endpoint...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Get Current Weather
print("\n2. Testing /api/weather/current...")
response = requests.get(f"{BASE_URL}/api/weather/current?city=Colombo")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Get Holidays
print("\n3. Testing /api/holidays...")
response = requests.get(f"{BASE_URL}/api/holidays?year=2026")
print(f"Status: {response.status_code}")
print(f"Holidays found: {len(response.json().get('holidays', []))}")

# Test 4: Get All Festivals
print("\n4. Testing /api/festivals...")
response = requests.get(f"{BASE_URL}/api/festivals")
print(f"Status: {response.status_code}")
print(f"Festivals found: {len(response.json().get('festivals', []))}")

# Test 5: Get Festivals by Month
print("\n5. Testing /api/festivals/month/7...")
response = requests.get(f"{BASE_URL}/api/festivals/month/7")
print(f"Status: {response.status_code}")
print(f"July festivals: {len(response.json().get('festivals', []))}")

# Test 6: Search Festivals
print("\n6. Testing /api/festivals/search...")
response = requests.get(f"{BASE_URL}/api/festivals/search?query=perahera")
print(f"Status: {response.status_code}")
print(f"Search results: {response.json().get('count', 0)}")

# Test 7: Get Suggestions
print("\n7. Testing /api/suggestions...")
response = requests.get(
    f"{BASE_URL}/api/suggestions?date=2026-08-15&location=Kandy"
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*60)
print("ALL TESTS COMPLETED")
print("="*60)
```

**Running Tests:**
```bash
# Start the API
cd festival-weather-backend
source venv/bin/activate
uvicorn app.main:app --port 8000

# Run tests
python tests/test_api.py
```

### Interactive Testing

**Swagger UI:** `http://localhost:8000/docs`
**ReDoc:** `http://localhost:8000/redoc`

---

## Integration with Final Product

### Mobile App Integration

**Flutter Service:**

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class FestivalWeatherService {
  final String baseUrl = 'http://localhost:8000';
  
  Future<Map<String, dynamic>> getWeather(String city) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/weather/current?city=$city'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get weather');
    }
  }
  
  Future<List<dynamic>> getFestivals(int month) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/festivals/month/$month'),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['festivals'];
    } else {
      throw Exception('Failed to get festivals');
    }
  }
  
  Future<Map<String, dynamic>> getSuggestions({
    required String date,
    required String location,
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/suggestions?date=$date&location=$location'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get suggestions');
    }
  }
}
```

### Integration Scenarios

**Scenario 1: Trip Planning Dashboard**
```
User selects destination and dates
→ Call /api/suggestions
→ Display weather, festivals, holidays
→ Show recommendations
```

**Scenario 2: Festival Discovery**
```
User browses festivals
→ Call /api/festivals
→ Display list with filters
→ User selects festival
→ Call /api/festivals/{id}
→ Show details
```

**Scenario 3: Weather-Based Recommendations**
```
User checks weather
→ Call /api/weather/current
→ If rainy: Suggest indoor activities
→ If sunny: Suggest outdoor attractions
→ Combine with festival data
```

---

## Error Handling

**Graceful Degradation:**
- If OpenWeatherMap fails: Return cached data
- If Calendarific fails: Return cached data
- If Redis unavailable: API still works (slower)
- If database error: Return appropriate error message

---

## Summary

**API Capabilities:**
- Real-time weather data
- Public holiday information
- Festival calendar
- Smart suggestions
- Fast and reliable

**Integration Benefits:**
- Easy mobile integration
- Multiple data sources
- Caching for performance
- Comprehensive information

**Business Value:**
- Helps tourists plan trips
- Provides local insights
- Improves travel experience
- Data-driven suggestions
