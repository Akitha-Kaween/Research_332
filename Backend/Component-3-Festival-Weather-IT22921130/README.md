# Festival & Weather Component

**Component ID:** IT22921130  
**Developer:** Malsha R.J.H  
**Type:** API Integration & Database Management  
**API Port:** 8000

---

## Overview

This component provides comprehensive festival calendar, weather information, and public holiday data for tourists visiting Sri Lanka. It integrates external APIs (OpenWeatherMap, Calendarific) with a local festival database to deliver real-time tourism information.

### Key Features

- **Real-time Weather:** Current weather and 5-day forecasts for Sri Lankan cities
- **Festival Calendar:** Curated database of Sri Lankan festivals and cultural events
- **Public Holidays:** Official Sri Lankan public holidays from Calendarific API
- **Smart Suggestions:** Combined recommendations based on weather, festivals, and holidays
- **AI Research Agent:** Hybrid Chatbot tailored for Sri Lanka (Flan-T5 + Tools)
- **Intelligent Tour Planner:** Genetic Algorithm (GA) for multi-objective route optimization
- **Caching:** Redis-based caching for improved performance
- **Fast Response:** < 200ms average response time
- **RESTful API:** Easy integration with mobile applications

---

---

## Research Component: AI Travel Agent

This component features a novel **Hybrid AI Architecture** that combines a Fine-Tuned LLM with a Deterministic Genetic Algorithm.

### 1. Generative AI Chatbot
- **Model:** Google Flan-T5 (Fine-Tuned)
- **Dataset:** 12,000+ procedurally generated Q&A pairs focused on Sri Lanka tourism.
- **Behavior:** Enforces a strict professional persona ("Expert Sri Lanka Travel Assistant").
- **Capabilities:** Answers general questions about hotels, history, and advice for 10+ major cities.

### 2. Intelligent Tour Planner (Genetic Algorithm)
- **Algorithm:** Multi-Objective Genetic Algorithm (GA).
- **Optimization Goals:** Minimize Travel Distance + Minimize Weather Risk + Minimize Crowd Levels.
- **Output:** Generates an optimal route map (`minimal_tour_map.html`) rather than just a text list.

### 3. Integrated Agent (`/agent/chat`)
- **Logic:** Rule-Based Intent Classification.
- **Workflow:**
    - Detects **"Plan Tour"** -> Triggers **Genetic Algorithm**.
    - Detects **"Weather"** -> Triggers **Weather API**.
    - Comparisons/General -> Triggers **Flan-T5 LLM**.

---

## Project Structure

```
Component-3-Festival-Weather-IT22921130/
├── backend/                      # FastAPI backend application
│   ├── app/                     # Main application package
│   │   ├── __init__.py         # Package initialization
│   │   ├── main.py             # Main FastAPI application
│   │   ├── config/             # Configuration files
│   │   │   ├── __init__.py
│   │   │   ├── database.py    # Database configuration
│   │   │   └── settings.py    # Application settings
│   │   ├── models/             # Database models
│   │   │   ├── __init__.py
│   │   │   └── festival.py    # Festival model
│   │   ├── routes/             # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── weather.py     # Weather endpoints
│   │   │   ├── holidays.py    # Holiday endpoints
│   │   │   ├── festivals.py   # Festival endpoints
│   │   │   └── suggestions.py # Suggestion endpoints
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── weather_service.py    # Weather API integration
│   │   │   ├── holiday_service.py    # Holiday API integration
│   │   │   └── festival_service.py   # Festival database operations
│   │   └── scripts/            # Utility scripts
│   │       ├── __init__.py
│   │       └── seed_festivals.py     # Database seeding
│   │
│   ├── tests/                   # Test files
│   │   ├── __init__.py
│   │   └── test_api.py         # API tests
│   │
│   ├── docs/                    # Additional documentation
│   ├── festival_weather.db      # SQLite database
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variable template
│   ├── ACTION_PLAN.md          # Development plan
│   ├── IMPLEMENTATION_SUMMARY.md  # Implementation details
│   └── README.md               # Backend-specific readme
│
├── docs/                         # Component documentation
│
├── API_DOCUMENTATION.md          # Complete API reference
├── IMPLEMENTATION_METHODOLOGY.md # Implementation details
├── README.md                     # This file
├── requirements.txt              # Component dependencies
└── .env.example                 # Environment configuration template
```

### File Descriptions

#### Backend Application Files

**`backend/app/main.py`**
- Main FastAPI application
- Application lifecycle management (startup/shutdown)
- Database and Redis initialization
- CORS middleware configuration
- Route registration
- **Key Functions:**
  - `lifespan()`: Manage app startup and shutdown
  - Database connection setup
  - Redis connection setup
  - Router inclusion

**`backend/app/config/database.py`**
- Database configuration and session management
- SQLAlchemy engine setup
- Session factory
- Base model class
- **Exports:**
  - `engine`: SQLAlchemy engine
  - `SessionLocal`: Session factory
  - `Base`: Declarative base for models
  - `get_db()`: Dependency for database sessions

**`backend/app/config/settings.py`**
- Application settings and environment variables
- API keys management
- Database URL configuration
- Redis configuration
- **Environment Variables:**
  - `OPENWEATHER_API_KEY`: Weather API key
  - `CALENDARIFIC_API_KEY`: Holiday API key
  - `DATABASE_URL`: Database connection string
  - `REDIS_URL`: Redis connection string

#### Model Files

**`backend/app/models/festival.py`**
- Festival database model
- SQLAlchemy ORM definition
- **Fields:**
  - `id`: Primary key
  - `name`: Festival name
  - `description`: Detailed description
  - `location`: City/region
  - `month`: Month (1-12)
  - `day`: Day of month
  - `duration_days`: Festival duration
  - `category`: Type (Buddhist, Hindu, etc.)
  - `significance`: Cultural/religious significance
  - `tourist_friendly`: Boolean flag
  - `image_url`: Optional image
  - `created_at`, `updated_at`: Timestamps

#### Route Files

**`backend/app/routes/weather.py`**
- Weather-related endpoints
- **Endpoints:**
  - `GET /api/weather/current`: Current weather
  - `GET /api/weather/forecast`: Weather forecast

**`backend/app/routes/holidays.py`**
- Holiday-related endpoints
- **Endpoints:**
  - `GET /api/holidays`: Get holidays by year
  - `GET /api/holidays/month`: Get holidays by month

**`backend/app/routes/festivals.py`**
- Festival CRUD endpoints
- **Endpoints:**
  - `GET /api/festivals`: List all festivals
  - `GET /api/festivals/{id}`: Get festival by ID
  - `GET /api/festivals/month/{month}`: Get festivals by month
  - `GET /api/festivals/search`: Search festivals
  - `POST /api/festivals`: Create festival (admin)
  - `PUT /api/festivals/{id}`: Update festival (admin)
  - `DELETE /api/festivals/{id}`: Delete festival (admin)

**`backend/app/routes/suggestions.py`**
- Smart suggestion endpoint
- **Endpoints:**
  - `GET /api/suggestions`: Get combined recommendations

#### Service Files

**`backend/app/services/weather_service.py`**
- OpenWeatherMap API integration
- Weather data fetching and parsing
- Caching logic for weather data
- **Functions:**
  - `get_current_weather()`: Fetch current weather
  - `get_weather_forecast()`: Fetch forecast
  - Cache management (30-minute TTL)

**`backend/app/services/holiday_service.py`**
- Calendarific API integration
- Holiday data fetching and parsing
- Caching logic for holiday data
- **Functions:**
  - `get_holidays()`: Fetch holidays for year
  - `get_holidays_by_month()`: Filter by month
  - Cache management (30-day TTL)

**`backend/app/services/festival_service.py`**
- Festival database operations
- CRUD operations
- Search functionality
- **Functions:**
  - `create_festival()`: Add new festival
  - `get_festivals()`: Retrieve festivals
  - `update_festival()`: Modify festival
  - `delete_festival()`: Remove festival
  - `search_festivals()`: Search by criteria

#### Utility Files

**`backend/app/scripts/seed_festivals.py`**
- Database seeding script
- Populates database with initial festival data
- **Festivals Seeded:**
  1. Sinhala and Tamil New Year
  2. Vesak
  3. Poson
  4. Esala Perahera
  5. Kandy Esala Perahera
  6. Deepavali
  7. Christmas
  8. Thai Pongal
  9. Maha Shivaratri
  10. Nallur Festival

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Redis (optional, for caching)
- Virtual environment (recommended)

### Setup Steps

**1. Navigate to Component Directory**
```bash
cd "Component-3-Festival-Weather-IT22921130"
```

**2. Create Virtual Environment**
```bash
python3 -m venv venv
```

**3. Activate Virtual Environment**

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

**4. Install Dependencies**
```bash
pip install -r requirements.txt
```

**5. Configure Environment Variables**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

**Required API Keys:**
- OpenWeatherMap API Key: https://openweathermap.org/api
- Calendarific API Key: https://calendarific.com/

**6. Initialize Database**
```bash
cd backend
python -c "from app.config.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

**7. Seed Database with Festivals**
```bash
python -m app.scripts.seed_festivals
```

### Dependencies

```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pydantic==2.5.0           # Data validation
sqlalchemy==2.0.23        # ORM
python-dotenv==1.0.0      # Environment variables
requests==2.31.0          # HTTP client
redis==5.0.1              # Redis client (optional)
loguru==0.7.2             # Logging
python-multipart==0.0.6   # Form data handling
```

---

## Running the Backend

### Development Mode

**Navigate to backend directory:**
```bash
cd backend
```

**Start the API server:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Options:**
- `--reload`: Auto-restart on code changes
- `--port 8000`: Run on port 8000
- `--host 0.0.0.0`: Accept connections from any IP

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Options:**
- `--workers 4`: Run 4 worker processes
- `--host 0.0.0.0`: Accept external connections

### With Redis (Optional)

**Start Redis server:**
```bash
redis-server
```

**In another terminal, start the API:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Note:** API works without Redis, but caching improves performance.

### Verify API is Running

**Check health endpoint:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "OK",
  "service": "Festival-Weather Backend",
  "version": "1.0.0",
  "component": "IT22921130"
}
```

---

## Testing the API

### Method 1: Interactive Documentation

**Swagger UI (Recommended):**
1. Open browser: `http://localhost:8000/docs`
2. Click on any endpoint to expand
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

**ReDoc:**
- Open browser: `http://localhost:8000/redoc`

### Method 2: cURL Commands

**Test Health Check:**
```bash
curl http://localhost:8000/health
```

**Test Current Weather:**
```bash
curl "http://localhost:8000/api/weather/current?city=Colombo"
```

**Test Holidays:**
```bash
curl "http://localhost:8000/api/holidays?year=2026"
```

**Test Festivals:**
```bash
curl http://localhost:8000/api/festivals
```

**Test Festivals by Month:**
```bash
curl http://localhost:8000/api/festivals/month/7
```

**Test Search:**
```bash
curl "http://localhost:8000/api/festivals/search?query=perahera"
```

**Test Suggestions:**
```bash
curl "http://localhost:8000/api/suggestions?date=2026-08-15&location=Kandy"
```

### Method 3: Python Test Script

**Run existing test script:**
```bash
cd backend
python tests/test_api.py
```

**Or create custom test:**
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test weather
response = requests.get(f"{BASE_URL}/api/weather/current?city=Colombo")
print(f"Weather: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test festivals
response = requests.get(f"{BASE_URL}/api/festivals")
print(f"\nFestivals: {response.status_code}")
print(f"Count: {len(response.json()['festivals'])}")
```

### Method 4: Postman

1. Create new GET request
2. URL: `http://localhost:8000/api/weather/current?city=Colombo`
3. Send request
4. View response

### Expected Test Results

**Weather Response:**
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

**Festivals Response:**
```json
{
  "festivals": [
    {
      "id": 1,
      "name": "Esala Perahera",
      "location": "Kandy",
      "month": 7,
      "day": 15,
      "duration_days": 10,
      "category": "Buddhist"
    }
  ]
}
```

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/weather/current` | Current weather |
| GET | `/api/weather/forecast` | Weather forecast |
| GET | `/api/holidays` | Get holidays by year |
| GET | `/api/holidays/month` | Get holidays by month |
| GET | `/api/festivals` | List all festivals |
| GET | `/api/festivals/{id}` | Get festival by ID |
| GET | `/api/festivals/month/{month}` | Get festivals by month |
| GET | `/api/festivals/search` | Search festivals |
| POST | `/api/festivals` | Create festival (admin) |
| PUT | `/api/festivals/{id}` | Update festival (admin) |
| DELETE | `/api/festivals/{id}` | Delete festival (admin) |
| GET | `/api/suggestions` | Get smart suggestions |

**For detailed API documentation, see:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## Database Management

### View Database

**Using SQLite command line:**
```bash
cd backend
sqlite3 festival_weather.db

# List tables
.tables

# View festivals
SELECT * FROM festivals;

# Exit
.quit
```

### Reseed Database

```bash
# Delete existing database
rm backend/festival_weather.db

# Recreate database
cd backend
python -c "from app.config.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Reseed festivals
python -m app.scripts.seed_festivals
```

### Add New Festival

**Using API:**
```bash
curl -X POST http://localhost:8000/api/festivals \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Festival",
    "description": "Description here",
    "location": "Colombo",
    "month": 8,
    "day": 20,
    "duration_days": 3,
    "category": "Cultural",
    "significance": "Cultural",
    "tourist_friendly": true
  }'
```

---

## External API Configuration

### OpenWeatherMap

**Get API Key:**
1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file:
```
OPENWEATHER_API_KEY=your_key_here
```

**Free Tier Limits:**
- 60 calls/minute
- 1,000,000 calls/month

### Calendarific

**Get API Key:**
1. Visit: https://calendarific.com/
2. Sign up for free account
3. Get API key
4. Add to `.env` file:
```
CALENDARIFIC_API_KEY=your_key_here
```

**Free Tier Limits:**
- 1,000 calls/month

---

## Troubleshooting

### Issue: Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: Database Not Found

**Error:**
```
OperationalError: no such table: festivals
```

**Solution:**
```bash
# Initialize database
cd backend
python -c "from app.config.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Seed festivals
python -m app.scripts.seed_festivals
```

### Issue: API Key Errors

**Error:**
```
401 Unauthorized
```

**Solution:**
1. Check `.env` file exists
2. Verify API keys are correct
3. Ensure no extra spaces in `.env`
4. Restart the server

### Issue: Redis Connection Failed

**Warning:**
```
Redis not available
```

**Solution:**
- This is optional - API works without Redis
- To enable caching:
  ```bash
  # Install Redis
  brew install redis  # macOS
  
  # Start Redis
  redis-server
  ```

---

## Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[IMPLEMENTATION_METHODOLOGY.md](IMPLEMENTATION_METHODOLOGY.md)** - Implementation details
- **[backend/README.md](backend/README.md)** - Backend-specific documentation
- **[backend/ACTION_PLAN.md](backend/ACTION_PLAN.md)** - Development plan
- **[backend/IMPLEMENTATION_SUMMARY.md](backend/IMPLEMENTATION_SUMMARY.md)** - Implementation summary

---

## Integration

### Flutter Integration Example

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
}
```

---

## Contributing

### Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

### Testing
- Test all endpoints after changes
- Verify external API integrations
- Check database operations
- Test error handling

---

## License

This project is part of the Smart Tourism research project.

---

## Contact

**Developer:** Malsha R.J.H  
**Component ID:** IT22921130  
**Project:** Smart Tourism - Festival & Weather

---

## Quick Start Summary

```bash
# 1. Navigate to directory
cd Component-3-Festival-Weather-IT22921130

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Initialize database
cd backend
python -c "from app.config.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 6. Seed database
python -m app.scripts.seed_festivals

# 7. Run the API
uvicorn app.main:app --reload --port 8000

# 8. Test the API
curl http://localhost:8000/health

# 9. Open interactive docs
open http://localhost:8000/docs
```

**API is now running on:** `http://localhost:8000`
