# RP 25_26J_332_Tourism management app
# Smart Tourism - Intelligent Travel Planning System for Sri Lanka
---

## Project Overview

Smart Tourism is an intelligent travel planning system designed to enhance the tourist experience in Sri Lanka. The system combines machine learning, real-time data integration, and personalized recommendations to help tourists make informed decisions about when to visit attractions, what to eat, and which festivals to experience.

### Vision

To create a comprehensive, data-driven tourism platform that helps visitors optimize their Sri Lankan travel experience by providing:
- Crowd predictions to avoid overcrowding
- Personalized food recommendations
- Festival and weather information
- Smart itinerary suggestions
- Aspect-Based Sentiment Analysis for Sri Lanka Tourism Reviews

## System Architecture

### Three-Component Architecture


┌─────────────────────────────────────────────────────────────────┐
│                    SMART TOURISM SYSTEM                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   Flutter Mobile Application                     │
│              (User Interface & Experience Layer)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ↓               ↓               ↓
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Component 1    │ │  Component 2    │ │  Component 3    │
│ Crowd Analysis  │ │      Food       │ │Festival/Weather │
│  IT22255242     │ │ Recommendation  │ │   IT22921130    │
│                 │ │   IT22551870    │ │                 │
│  Port: 8001     │ │  Port: 8002     │ │  Port: 8000     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
        │                   │                   │
        ↓                   ↓                   ↓
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  ML Model       │ │  ML Model       │ │  External APIs  │
│ Linear Reg.     │ │  Recommender    │ │ OpenWeatherMap  │
│ Time Series     │ │  System         │ │  Calendarific   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```



## Components

### Component 1: Crowd Analysis (IT22255242)

Developer: Buddhima P.K.A.K  
Technology: Machine Learning - Linear Regression  
API Port: 8001

Purpose:
Predicts crowd levels at tourist attractions to help visitors plan optimal visit times.

Key Features:
- Predict crowd levels (low/medium/high) for any date and time
- Suggest best times to visit attractions
- Historical analysis based on 13+ years of data
- 94.43% prediction accuracy (R² score)

ML Model:
- Type: Linear Regression with time-based features
- Features: Month, quarter, year progress, lag features (1, 2, 3, 6, 12 months)
- Performance: RMSE 350.20, MAE 256.14, MAPE 9.20%

API Endpoints:
- `POST /api/predict` - Predict crowd level
- `POST /api/best-time` - Get optimal visit times
- `GET /api/metrics` - Model performance

### Component 2: Food Recommendation (IT22551870)

Developer: Kumari M.S.S  
Technology: Machine Learning - Collaborative Filtering  
API Port: 8002

Purpose:
Provides personalized food and recipe recommendations for tourists visiting Sri Lanka.

Key Features:
- Personalized recipe recommendations
- Rating prediction for user-recipe pairs
- Popular recipe discovery
- Sri Lanka-focused cuisine filtering
- 94.2% prediction accuracy (within 1 star)

ML Model:
- Type: Baseline Recommender with user/recipe bias
- Formula: `prediction = global_mean + user_bias + recipe_bias`
- Performance: RMSE 0.67, MAE 0.42

Data Sources:
- Food.com: 698,901 interactions, 178,265 recipes
- Zomato: 1,247 Sri Lankan restaurants
- Yelp: 856 Sri Lanka-relevant reviews

**API Endpoints:
- `POST /api/recommend` - Get personalized recommendations
- `POST /api/predict` - Predict rating
- `GET /api/popular` - Get popular recipes
- `GET /api/metrics` - Model performance

### Component 3: Festival & Weather AI Tour Planner (IT22921130)

Developer: Malsha R.J.H  
Technology: API Integration & Database Management  
API Port: 8000

Purpose:
Provides real-time weather, festival calendar, and public holiday information.

Key Features:
- Real-time weather data for Sri Lankan cities
- 5-day weather forecasts
- Curated festival database (10+ major festivals)
- Public holiday information
- Smart suggestions combining all data
- Redis caching for performance

External APIs:
- OpenWeatherMap: Current weather and forecasts
- Calendarific: Sri Lankan public holidays

Database:
- SQLite: Local festival database
- 10 major Sri Lankan festivals seeded
- CRUD operations for festival management

**API Endpoints:**
- `GET /api/weather/current` - Current weather
- `GET /api/weather/forecast` - Weather forecast
- `GET /api/holidays` - Public holidays
- `GET /api/festivals` - Festival calendar
- `GET /api/suggestions` - Smart recommendations

# AI Tour Planner (IT22921130)

## Overview
This research module implements an **Intelligent Multi-Objective Tour Planner** that goes beyond simple distance minimization. It uses a Genetic Algorithm (GA) to find the optimal route for a tourist visiting multiple attractions in Kandy, considering:
1.  Real-world Directions:Using OpenStreetMap data via `osmnx`.
2.  Weather Constraints: Avoiding outdoor locations during high rain probability hours.
3.  Crowd Avoidance: Minimizing visits to congested areas during peak times.

### Dataset
*   File: `sri_lanka_chat_data.json`
*   Size: ~12,000 records
*   Content: Detailed Q&A about Hotels, Landmarks, Food, and Itineraries for 10 districts.

## Methodology

### 1. Graph Construction
We fetch the drivable street network of **Kandy, Sri Lanka** using `osmnx`. This provides a realistic graph $G=(V, E)$ where edges represent actual roads and weights represent lengths.

### 2. Distance Matrix
We calculate the shortest path distance between all pairs of 6 key attractions (Temple of the Tooth, Kandy Lake, Peradeniya Gardens, etc.) using Dijkstra's algorithm on the road network.

### 3. Genetic Algorithm
We evolve a population of routes using:
*   Representation: Permutation of location indices.
*   Fitness Function: $F = \frac{1}{TotalDistance + WeatherPenalty + CrowdPenalty}$
*   Selection: Tournament Selection.
*   Crossover: Ordered Crossover (OX1).
*   Mutation: Swap Mutation.

## Results
The algorithm produces an optimized sequence of visits (e.g., "Temple -> Lake -> Museum -> Gardens"). The final output is an interactive map (`minimal_tour_map.html`) displaying the route path in green and markers for each stop.


## How Components Work Together

### Integration Flow

Scenario 1: Planning a Trip to Kandy

```
User opens app → Selects "Kandy" and date "August 15, 2026"
    │
    ├→ Component 3: Get weather forecast
    │   └→ Returns: 25°C, partly cloudy, suitable for outdoor
    │
    ├→ Component 3: Check festivals
    │   └→ Returns: Esala Perahera (ongoing, 3 days remaining)
    │
    ├→ Component 1: Predict crowd level
    │   └→ Returns: HIGH (85% crowded, 4200 expected visitors)
    │
    ├→ Component 1: Get best times
    │   └→ Returns: Visit at 6:00 AM or 8:00 AM (low crowd)
    │
    └→ Component 2: Get food recommendations
        └→ Returns: Top 5 Sri Lankan dishes in Kandy
    
App displays:
✓ Weather: Pleasant, 25°C
✓ Festival: Esala Perahera happening! Don't miss it
✓ Crowd: Very busy - visit early morning
✓ Best time: 6:00 AM - 8:00 AM
✓ Recommended food: Kandy-style curry, kottu roti, etc.
```

Scenario 2: Food Discovery

```
User wants lunch recommendations
    │
    ├→ Component 2: Get personalized recommendations
    │   └→ Based on user's previous ratings
    │
    ├→ Component 3: Check weather
    │   └→ If rainy: Suggest indoor restaurants
    │   └→ If sunny: Suggest outdoor cafes
    │
    └→ Component 1: Check nearby attraction crowds
        └→ Suggest restaurants near less crowded areas
    
App displays:
✓ Top 5 personalized food recommendations
✓ Weather-appropriate dining options
✓ Restaurants near less crowded attractions
```

**Scenario 3: Itinerary Optimization**

```
User plans 3-day trip
    │
    ├→ Component 3: Get weather for all 3 days
    │   └→ Day 1: Sunny, Day 2: Rainy, Day 3: Cloudy
    │
    ├→ Component 3: Check festivals during dates
    │   └→ Day 2: Public holiday (Vesak)
    │
    ├→ Component 1: Predict crowds for each day
    │   └→ Day 1: Medium, Day 2: High (holiday), Day 3: Low
    │
    └→ Component 2: Suggest meals for each day
        └→ Based on locations and preferences
    
App suggests optimized itinerary:
Day 1: Outdoor attractions (sunny, medium crowd)
Day 2: Indoor activities + Vesak celebrations (rainy, high crowd)
Day 3: Major attractions (cloudy, low crowd - best day!)
```
## Mobile Application (Flutter)

### User Interface Screens
 
1. Home Dashboard
- Current location weather
- Nearby festivals
- Personalized food suggestions
- Quick crowd check

2. Attraction Planner
- Select attraction and date
- View crowd prediction
- See best visit times
- Check weather forecast

3. Food Discovery
- Personalized recommendations
- Filter by cuisine, location
- View predicted ratings
- Restaurant information

4. Festival Calendar
- Monthly festival view
- Festival details
- Location information
- Cultural significance

5. Trip Planner
- Multi-day itinerary
- Optimized schedule
- Combined recommendations
- Weather-aware planning

### User Experience Flow

```
App Launch
    ↓
Location Detection
    ↓
Dashboard (Personalized)
    ├→ Today's Weather
    ├→ Nearby Festivals
    ├→ Food Recommendations
    └→ Crowd Alerts
    ↓
User Selects Feature
    ├→ Plan Visit
    │   ├→ Select Attraction
    │   ├→ Choose Date/Time
    │   ├→ View Crowd Prediction
    │   └→ Get Best Times
    │
    ├→ Find Food
    │   ├→ View Recommendations
    │   ├→ Filter Options
    │   ├→ Check Ratings
    │   └→ Get Directions
    │
    └→ Explore Festivals
        ├→ Browse Calendar
        ├→ View Details
        ├→ Check Weather
        └→ Plan Visit
```

## Technical Architecture Framework (TAF)

### System Design Principles

1. Microservices Architecture
- Each component is independent
- Separate APIs on different ports
- Easy to scale and maintain
- Can deploy independently

2. RESTful API Design
- Standard HTTP methods
- JSON request/response
- Consistent error handling
- Comprehensive documentation

3. Data-Driven Decisions
- ML models for predictions
- Real-time data integration
- Historical data analysis
- Personalization algorithms

4. Performance Optimization
- Redis caching (Component 3)
- Model pre-loading on startup
- Efficient database queries
- Async operations

5. Scalability
- Stateless APIs
- Horizontal scaling ready
- Load balancing capable
- Cloud deployment ready

### Technology Stack

Backend:
- Python 3.8+
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Redis (caching)

Machine Learning:
- Scikit-learn (ML models)
- Pandas (data processing)
- NumPy (numerical computing)
- Joblib (model persistence)

Frontend (Planned):
- Flutter (mobile framework)
- Dart (programming language)
- HTTP package (API calls)
- State management (Provider/Riverpod)

External Services:
- OpenWeatherMap API
- Calendarific API

## Project Structure

```
Smart TOURISM/
├── Component-1-Crowd-Analysis-IT22255242/
│   ├── backend/                  # FastAPI application
│   ├── datasets/                 # Tourism data
│   ├── ml-models/                # Trained models
│   ├── notebooks/                # Jupyter notebooks
│   ├── API_DOCUMENTATION.md
│   ├── DATASET_DOCUMENTATION.md
│   ├── ML_METHODOLOGY.md
│   └── README.md
│
├── Component-2-Food-Recommendation-IT22551870/
│   ├── backend/                  # FastAPI application
│   ├── datasets/                 # Food datasets
│   ├── ml-models/                # Trained models
│   ├── notebooks/                # Jupyter notebooks
│   ├── API_DOCUMENTATION.md
│   ├── DATASET_DOCUMENTATION.md
│   ├── ML_METHODOLOGY.md
│   └── README.md
│
├── Component-3-Festival-Weather-IT22921130/
│   ├── backend/                  # FastAPI application
│   │   ├── app/                 # Main application
│   │   ├── tests/               # Test files
│   │   └── festival_weather.db  # SQLite database
│   ├── API_DOCUMENTATION.md
│   ├── IMPLEMENTATION_METHODOLOGY.md
│   └── README.md
│
├── mobile-app/                   # Flutter application (future)
│   ├── lib/
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
│
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Redis (optional, for caching)
- Flutter SDK (for mobile app development)

### Quick Start - All Components

1. Clone or Navigate to Project
```bash
cd "Smart TOURISM"
```

2. Start Component 1 (Crowd Analysis)
```bash
cd Component-1-Crowd-Analysis-IT22255242
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8001
```

3. Start Component 2 (Food Recommendation)
```bash
# In new terminal
cd Component-2-Food-Recommendation-IT22551870
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8002
```

4. Start Component 3 (Festival/Weather AI Tour Planner)
```bash
# In new terminal
cd Component-3-Festival-Weather-IT22921130/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from app.config.database import Base, engine; Base.metadata.create_all(bind=engine)"
python -m app.scripts.seed_festivals

# Start server
uvicorn app.main:app --reload --port 8000


## How to Run (AI Tour Planner)

### 1. Setup Environment
This research requires specific geospatial libraries. We recommend using the provided virtual environment.

```bash
# Activate the research environment
source notebooks/venv/bin/activate  # macOS/Linux
# notebooks\venv\Scripts\activate   # Windows

# Install dependencies (if not already installed)
pip install osmnx networkx folium pandas matplotlib scikit-learn
```

### 2. Run the Research Script
You can run the Python script directly to generate the map:

```bash
python notebooks/research_tour_planner.py
```


```
5. Verify All APIs
```bash
# Component 1
curl http://localhost:8001/health

# Component 2
curl http://localhost:8002/health

# Component 3
curl http://localhost:8000/health
```

All APIs Running:
- Component 1: http://localhost:8001/docs
- Component 2: http://localhost:8002/docs
- Component 3: http://localhost:8000/docs
  
## Testing the System

### Individual Component Testing

Component 1:
```bash
curl -X POST http://localhost:8001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"location": "Sigiriya", "date": "2026-08-15", "time": "10:00"}'
```

Component 2:
```bash
curl -X POST http://localhost:8002/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "n_recommendations": 5}'
```

Component 3:
```bash
curl "http://localhost:8000/api/weather/current?city=Colombo"
curl http://localhost:8000/api/festivals
```

### Integrated Testing

Test Smart Suggestions:
```bash
curl "http://localhost:8000/api/suggestions?date=2026-08-15&location=Kandy"
```

This combines weather, festivals, and holidays for comprehensive recommendations.

## Development Roadmap

### Phase 1: Backend Development  (Current)

Completed:
-  Component 1: ML model trained and API deployed
-  Component 2: Recommendation system and API deployed
-  Component 3: External API integration and database
- Comprehensive documentation
-  API testing and validation

### Phase 2: Mobile App Development (Next)

Timeline: 2-3 months

Tasks:
1. Setup Flutter Project
   - Initialize Flutter app
   - Setup project structure
   - Configure dependencies

2. API Integration
   - Create service classes for each component
   - Implement HTTP requests
   - Handle responses and errors

3. UI Development
   - Design app screens
   - Implement navigation
   - Create reusable widgets

4. State Management
   - Implement Provider/Riverpod
   - Manage app state
   - Handle data caching

5. Testing
   - Unit tests
   - Widget tests
   - Integration tests

### Phase 3: Enhancement & Optimization (Future)

Timeline:3-4 months

Planned Features:

Component 1 Enhancements:
- Add more attractions (expand beyond Sigiriya)
- Include daily granularity (not just monthly)
- Real-time crowd updates (if data available)
- Weather impact on crowds

Component 2 Enhancements:
- Content-based filtering (ingredients, cuisine)
- Hybrid recommendation system
- User profile creation
- Dietary restriction filters
- Restaurant booking integration

Component 3 Enhancements:
- More festivals (expand database to 50+)
- Festival notifications
- Weather alerts
- Multi-language support (Sinhala, Tamil)

**Mobile App Features:**
- Offline mode
- Push notifications
- User authentication
- Trip history
- Social sharing
- AR features for attractions
- Voice assistant integration

### Phase 4: Deployment & Launch (Future)

Timeline:1-2 months

Tasks:
1. **Backend Deployment**
   - Deploy to cloud (AWS/Google Cloud/Azure)
   - Setup load balancers
   - Configure auto-scaling
   - Setup monitoring

2. Mobile App Release
   - App Store submission (iOS)
   - Play Store submission (Android)
   - Beta testing
   - User feedback collection

3. Marketing & Outreach
   - Tourism board partnerships
   - Hotel collaborations
   - Travel agency integration
   - Social media campaigns
## Use Cases

### For Tourists

1. Trip Planning
- Check crowd levels before visiting attractions
- Plan visits during less crowded times
- Discover local festivals
- Get weather forecasts

2. Food Discovery
- Find restaurants matching preferences
- Discover local cuisine
- Get personalized recommendations
- Avoid tourist traps

3. Cultural Exploration
- Learn about Sri Lankan festivals
- Plan visits around cultural events
- Understand significance
- Get authentic experiences

### For Tourism Industry

1. Attraction Management
- Monitor visitor patterns
- Optimize staffing
- Manage capacity
- Improve visitor experience

2. Restaurant Owners
- Understand customer preferences
- Optimize menu offerings
- Target marketing
- Improve ratings

3. Tourism Board
- Promote festivals
- Distribute tourist flow
- Seasonal planning
- Data-driven decisions
  
## Research Contributions

### Academic Value

1. Machine Learning Applications
- Tourism demand forecasting
- Recommendation systems
- Time series analysis
- Collaborative filtering

2. Data Integration
- Multi-source data fusion
- External API integration
- Real-time data processing
- Caching strategies

3. System Design
- Microservices architecture
- RESTful API design
- Mobile-backend integration
- Scalable systems

### Publications (Planned)

1. "Crowd Prediction for Tourism Using Time Series Analysis"
2. "Personalized Food Recommendations for Tourists"
3. "Integrated Tourism Information System for Sri Lanka"

## Team

| Component | Student ID | Name | Role |
|-----------|-----------|------|------|
| Component 1 | IT22255242 | Buddhima P.K.A.K | Crowd Analysis & ML |
| Component 2 | IT22551870 | Kumari M.S.S | Food Recommendation & ML |
| Component 3 | IT22921130 | Malsha R.J.H | Festival/Weather & Integration Ai AI Tour Planner|
| Component4 | IT22033246 | Kavidu | Tourism reviews |

## License

This project is developed as part of academic research at Sri Lanka Institute of Information Technology (SLIIT).

## Contact

For questions or collaboration opportunities:

## Acknowledgments

- Sri Lanka Tourism Development Authority
- United Nations World Tourism Organization (UNWTO)
- OpenWeatherMap
- Calendarific
- Kaggle (for datasets)
- Food.com community


## Component 4: Aspect-Based Sentiment Analysis for Sri Lanka Tourism Reviews (IT22033246)

Developer: Kavindu  
Technology: Machine Learning

# Sri Lanka Tourism Sentiment Analysis System

**Aspect-Based Sentiment Analysis with Machine Learning for Sri Lanka Tourism**

A comprehensive machine learning system that analyzes 16,000+ tourism reviews to provide aspect-level sentiment insights and smart destination recommendations.

---

## Research Features

### Machine Learning Components
- **Overall Sentiment Classification** - Linear SVM with 81.58% accuracy
- **Aspect-Level ML Classification** - Separate models for 7 tourism aspects (74.11% avg F1)
- **Hybrid Analysis** - Combines ML + Lexicon approaches for robust predictions

### Aspect-Based Sentiment Analysis
- **7 Tourism Aspects**: Scenery, Safety, Facilities, Value, Accessibility, Experience, Service
- **200+ Domain Keywords**: Tourism-specific vocabulary
- **76 Destinations**: Comprehensive insights for Sri Lanka locations

### Smart Features
- **Preference-Based Recommendations** - Match destinations to user preferences
- **Location Comparison** - Compare multiple destinations across all aspects
- **Real-time Analysis** - Analyze any review text instantly

---

##  ML Results Summary

### Overall Sentiment Classification
| Model | Accuracy | F1 Score |
|-------|----------|----------|
| Linear SVM | 81.58% | 81.08% |
| Logistic Regression | 80.92% | 80.45% |
| Random Forest | 78.34% | 77.89% |

### Aspect-Level ML Classification
| Aspect | Best Model | F1 Score | Samples |
|--------|------------|----------|---------|
| Experience & Activities | Linear SVM | 77.67% | 11,076 |
| Scenery & Views | Linear SVM | 76.80% | 9,053 |
| Facilities | Linear SVM | 74.12% | 5,413 |
| Accessibility | Linear SVM | 73.59% | 8,986 |
| Value for Money | Linear SVM | 72.95% | 7,220 |
| Service & Staff | Logistic Regression | 72.47% | 2,093 |
| Safety & Crowds | Naive Bayes | 71.14% | 3,697 |

**Total ML Training Samples: 47,538**

---

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- 4GB RAM minimum

---

##  Quick Start Guide

### Step 1: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Application
- **Sentiment Analysis Dashboard**: http://127.0.0.1:5001/absa
- **Recommender System**: http://127.0.0.1:5001/

> ⚠️ **Note**: First startup takes ~2-3 minutes to train ML models. Wait for "✅ ABSA service ready!" message.

---

## 📊 Running Analysis Scripts

### Run Complete ML Training
```bash
python scripts/run_aspect_ml_training.py
```

### Export Research Results
```bash
python scripts/export_research_results.py
```

### Run Sentiment Analysis Evaluation
```bash
python scripts/run_sentiment_analysis.py
```

---

## 🔌 API Endpoints

### Core Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/absa/locations` | GET | Get all locations with ratings |
| `/api/absa/locations/<name>` | GET | Get detailed insight for a location |
| `/api/absa/locations/<name>/aspects` | GET | Get aspect scores for a location |
| `/api/absa/recommend` | POST | Get smart recommendations |
| `/api/absa/compare` | POST | Compare multiple locations |

### ML Endpoints (NEW)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/absa/analyze` | POST | Analyze review (lexicon-based) |
| `/api/absa/analyze/ml` | POST | Analyze review (ML hybrid) |
| `/api/absa/ml/evaluation` | GET | Get ML model evaluation metrics |
| `/api/absa/export/research` | GET | Export all research data |

### Example API Usage
```bash
# ML-based review analysis
curl -X POST http://127.0.0.1:5001/api/absa/analyze/ml \
  -H "Content-Type: application/json" \
  -d '{"text": "Beautiful scenery but very crowded and expensive."}'

# Get ML evaluation results
curl http://127.0.0.1:5001/api/absa/ml/evaluation

# Export research data
curl http://127.0.0.1:5001/api/absa/export/research
```

---

## 📁 Project Structure

```
tourism-recommender-system/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── dataset/
│   └── Reviews.csv                 # Tourism reviews (16,156 reviews)
├── src/
│   ├── aspect_sentiment.py         # ABSA core implementation
│   ├── aspect_ml_service.py        # ML service (NEW)
│   ├── aspect_ml_classifier.py     # ML training pipeline
│   ├── absa_api.py                 # API service layer
│   └── sentiment_analysis.py       # Overall sentiment ML
├── scripts/
│   ├── run_aspect_ml_training.py   # Train ML models
│   ├── export_research_results.py  # Export for paper (NEW)
│   └── run_sentiment_analysis.py   # Evaluate sentiment
├── models/
│   └── aspect_ml/                  # Trained ML models (NEW)
├── research_output/                # Exported research data (NEW)
├── templates/
│   └── absa.html                   # Enhanced frontend with charts
└── data/
    ├── aspect_statistics.csv
    └── location_insights.csv
```

---

## 📈 Research Output Files

After running `python scripts/export_research_results.py`:

```
research_output/
├── location_insights.csv       # 76 locations with aspect scores
├── aspect_statistics.csv       # 7 aspects with sentiment stats
├── ml_evaluation_results.csv   # ML metrics per aspect
├── dataset_statistics.json     # Overall dataset stats
└── complete_research_data.json # All data for paper
```

---

## 🔧 Configuration

Edit `.env` file:
```env
FLASK_DEBUG=0           # Keep 0 for production
API_PORT=5001           # Change port if needed
```

---

## 📚 Research Documentation

- `ABSA_RESEARCH.md` - Detailed ABSA methodology
- `ASPECT_ML_RESULTS.md` - ML training results
- `SENTIMENT_ANALYSIS_RESEARCH.md` - Overall sentiment methodology
- `SENTIMENT_ANALYSIS_RESULTS.md` - Evaluation results

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
lsof -ti:5001 | xargs kill -9
```

### NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('all')"
```

### Slow First Load
First startup trains ML models (~2-3 minutes). Subsequent loads are instant as models are cached.

---

## 📄 License

This project is for academic research purposes.


# Research_332
