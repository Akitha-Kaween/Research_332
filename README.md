# Crowd Analysis Component

**Component ID:** IT22255242  
**Developer:** Buddhima P.K.A.K  
**Type:** Machine Learning - Time Series Forecasting  
**API Port:** 8001

---

## Overview

This component provides intelligent crowd prediction services for tourist attractions in Sri Lanka. Using a trained Linear Regression model with time-based features, it predicts visitor numbers and crowd levels to help tourists plan optimal visit times.

### Key Features

- **Crowd Level Prediction:** Predict crowd levels (low/medium/high) for any date and time
- **Best Time Suggestions:** Identify optimal visiting times to avoid crowds
- **Historical Analysis:** Based on 13+ years of tourism data (2010-2023)
- **High Accuracy:** 94.43% R² score, 9.20% MAPE
- **Fast Response:** < 100ms average response time
- **RESTful API:** Easy integration with mobile applications

---

## Project Structure

```
Component-1-Crowd-Analysis-IT22255242/
├── backend/                      # FastAPI backend application
│   ├── __init__.py              # Package initialization
│   └── main.py                  # Main API application with endpoints
│
├── datasets/                     # Data storage
│   ├── processed/               # Cleaned, ready-to-use data
│   │   └── tourism2_revision2.csv
│   ├── raw/                     # Original downloaded data
│   ├── research-papers/         # Academic papers and references
│   └── un-tourism-data/         # UN tourism statistics
│
├── ml-models/                    # Trained machine learning models
│   ├── improved_model.pkl       # Main trained model (Linear Regression)
│   ├── scaler.pkl              # Feature scaler (inside model data)
│   ├── improved_metrics.json    # Model performance metrics
│   ├── baseline_model.pkl       # Baseline comparison model
│   └── training_metrics.json    # Training history
│
├── notebooks/                    # Jupyter notebooks for analysis
│   ├── 01_EDA_Tourism_Dataset.ipynb          # Exploratory data analysis
│   ├── 02_Model_Training_Improved.ipynb      # Model training and evaluation
│   ├── improved_model_results.png            # Visualization of results
│   └── README.md                             # Notebook documentation
│
├── docs/                         # Additional documentation
│
├── venv/                         # Python virtual environment
│
├── API_DOCUMENTATION.md          # Complete API reference
├── DATASET_DOCUMENTATION.md      # Dataset details and sources
├── ML_METHODOLOGY.md             # ML methodology and process
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

### File Descriptions

#### Backend Files

**`backend/main.py`**
- Main FastAPI application
- Defines all API endpoints
- Loads ML model on startup
- Handles prediction logic
- Implements CORS for frontend access
- **Key Functions:**
  - `predict_crowd()`: Extract features and make predictions
  - `classify_crowd_level()`: Convert predictions to crowd levels
  - API routes: `/`, `/health`, `/api/predict`, `/api/best-time`, `/api/metrics`

#### ML Model Files

**`ml-models/improved_model.pkl`**
- Trained Linear Regression model
- Contains model, scalers, and metadata
- Size: ~500 KB
- **Structure:**
  ```python
  {
      'type': 'linear_regression',
      'model': sklearn_model,
      'scaler_X': feature_scaler,
      'scaler_y': target_scaler,
      'feature_cols': list of features,
      'last_data': recent 12 months,
      'metrics': performance metrics
  }
  ```

**`ml-models/improved_metrics.json`**
- Model performance metrics
- RMSE, MAE, MAPE, R² scores
- Used for model validation

#### Notebook Files

**`notebooks/01_EDA_Tourism_Dataset.ipynb`**
- **Purpose:** Exploratory Data Analysis
- **Tasks:**
  - Load and inspect tourism data
  - Statistical analysis
  - Visualization of patterns
  - Identify trends and seasonality
  - Data quality checks

**`notebooks/02_Model_Training_Improved.ipynb`**
- **Purpose:** Model training and evaluation
- **Tasks:**
  - Feature engineering (time features, lag features)
  - Train-test split
  - Model training
  - Performance evaluation
  - Model saving
  - Results visualization

#### Dataset Files

**`datasets/processed/tourism2_revision2.csv`**
- Clean, preprocessed tourism data
- 163 rows (monthly data from 2010-2023)
- Ready for model training
- No missing values

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

**1. Clone or Navigate to Component Directory**
```bash
cd "Component-1-Crowd-Analysis-IT22255242"
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

### Dependencies

```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pydantic==2.5.0           # Data validation
scikit-learn==1.3.2       # Machine learning
pandas==2.1.3             # Data manipulation
numpy==1.26.2             # Numerical computing
joblib==1.3.2             # Model persistence
python-multipart==0.0.6   # Form data handling
```

---

## Running the Backend

### Development Mode

**Start the API server:**
```bash
uvicorn backend.main:app --reload --port 8001
```

**Options:**
- `--reload`: Auto-restart on code changes
- `--port 8001`: Run on port 8001
- `--host 0.0.0.0`: Accept connections from any IP

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Production Mode

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --workers 4
```

**Options:**
- `--workers 4`: Run 4 worker processes
- `--host 0.0.0.0`: Accept external connections

### Verify API is Running

**Check health endpoint:**
```bash
curl http://localhost:8001/health
```

**Expected response:**
```json
{
  "status": "OK",
  "model_loaded": true
}
```

---

## Testing the API

### Method 1: Interactive Documentation

**Swagger UI (Recommended for beginners):**
1. Open browser: `http://localhost:8001/docs`
2. Click on any endpoint to expand
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

**ReDoc (Clean documentation):**
- Open browser: `http://localhost:8001/redoc`

### Method 2: cURL Commands

**Test Health Check:**
```bash
curl http://localhost:8001/health
```

**Test Crowd Prediction:**
```bash
curl -X POST http://localhost:8001/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Sigiriya",
    "date": "2026-08-15",
    "time": "10:00"
  }'
```

**Test Best Time Endpoint:**
```bash
curl -X POST http://localhost:8001/api/best-time \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Sigiriya",
    "date": "2026-08-15"
  }'
```

**Test Model Metrics:**
```bash
curl http://localhost:8001/api/metrics
```

### Method 3: Python Test Script

**Create `test_api.py`:**
```python
import requests
import json

BASE_URL = "http://localhost:8001"

# Test prediction
payload = {
    "location": "Sigiriya",
    "date": "2026-08-15",
    "time": "10:00"
}

response = requests.post(f"{BASE_URL}/api/predict", json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

**Run:**
```bash
python test_api.py
```

### Method 4: Postman

1. Import collection or create new request
2. Set method to POST
3. URL: `http://localhost:8001/api/predict`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
```json
{
  "location": "Sigiriya",
  "date": "2026-08-15",
  "time": "10:00"
}
```
6. Send request

### Expected Test Results

**Successful Prediction:**
```json
{
  "location": "Sigiriya",
  "date": "2026-08-15",
  "time": "10:00",
  "crowd_level": "high",
  "crowd_percentage": 85,
  "expected_visitors": 4200,
  "confidence": 0.94
}
```

---

## API Endpoints

### Base URL
```
http://localhost:8001
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/predict` | Predict crowd level |
| POST | `/api/best-time` | Get best visiting times |
| GET | `/api/metrics` | Model performance metrics |

**For detailed API documentation, see:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## Model Information

### Model Type
Linear Regression with Time-Based Features

### Features Used
- `month`: Month of year (1-12)
- `quarter`: Quarter of year (1-4)
- `year_progress`: Continuous time variable
- `lag_1`: Previous month's visitors
- `lag_2`: 2 months ago
- `lag_3`: 3 months ago
- `lag_6`: 6 months ago
- `lag_12`: Same month last year

### Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **RMSE** | 350.20 | Average error: 350 visitors |
| **MAE** | 256.14 | Typical error: 256 visitors |
| **MAPE** | 9.20% | Average error: 9.20% |
| **R² Score** | 0.9443 | Explains 94.43% of variance |

**Conclusion:** Excellent predictive performance!

---

## Development Workflow

### 1. Data Analysis
```bash
# Open Jupyter notebook
jupyter notebook notebooks/01_EDA_Tourism_Dataset.ipynb
```

### 2. Model Training
```bash
# Open training notebook
jupyter notebook notebooks/02_Model_Training_Improved.ipynb
```

### 3. Backend Development
```bash
# Edit backend code
code backend/main.py

# Run with auto-reload
uvicorn backend.main:app --reload --port 8001
```

### 4. Testing
```bash
# Run test script
python test_api.py

# Or use Swagger UI
open http://localhost:8001/docs
```

---

## Troubleshooting

### Issue: Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8001
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 8002
```

### Issue: Model File Not Found

**Error:**
```
FileNotFoundError: ml-models/improved_model.pkl
```

**Solution:**
1. Ensure you're in the correct directory
2. Check if model file exists: `ls ml-models/`
3. If missing, run training notebook to generate model

### Issue: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Issue: CORS Errors (from frontend)

**Solution:**
CORS is already enabled in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[DATASET_DOCUMENTATION.md](DATASET_DOCUMENTATION.md)** - Dataset details and sources
- **[ML_METHODOLOGY.md](ML_METHODOLOGY.md)** - ML methodology and training process
- **[notebooks/README.md](notebooks/README.md)** - Notebook documentation

---

## Integration

### Flutter Integration Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> predictCrowd({
  required String location,
  required String date,
  required String time,
}) async {
  final response = await http.post(
    Uri.parse('http://localhost:8001/api/predict'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'location': location,
      'date': date,
      'time': time,
    }),
  );
  
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to predict crowd');
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
- Verify model predictions are reasonable
- Check error handling

---

## License

This project is part of the Smart Tourism research project.

---

## Contact

**Developer:** Buddhima P.K.A.K  
**Component ID:** IT22255242  
**Project:** Smart Tourism - Crowd Analysis

---

## Quick Start Summary

```bash
# 1. Navigate to directory
cd Component-1-Crowd-Analysis-IT22255242

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
uvicorn backend.main:app --reload --port 8001

# 5. Test the API
curl http://localhost:8001/health

# 6. Open interactive docs
open http://localhost:8001/docs
```

**API is now running on:** `http://localhost:8001`
