
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
import random

# Add notebooks path to sys.path to identify research module
NOTEBOOKS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../notebooks"))
if NOTEBOOKS_PATH not in sys.path:
    sys.path.append(NOTEBOOKS_PATH)

# Import Tour Planner with error handling
try:
    import research_tour_planner
except ImportError as e:
    print(f"Warning: Could not import Tour Planner: {e}")
    research_tour_planner = None

# Import Transformers (Lazy Loading recommended in Prod, but doing global for simplicity here)
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    # Load Model
    MODEL_PATH = os.path.join(NOTEBOOKS_PATH, "sri_lanka_flan_t5")
    if not os.path.exists(MODEL_PATH):
         print("Warning: Model path not found.")
         tokenizer = None
         model = None
    else:
         tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
         model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
except ImportError:
    print("Warning: Transformers not installed.")
    tokenizer = None
    model = None


router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    action_type: str = "chat" # chat, map, weather, crowd

# Mock Tools
def get_weather_update(location="Kandy"):
    conditions = ["Sunny ☀️", "Rainy 🌧️", "Cloudy ☁️", "Windy 💨"]
    temp = random.randint(22, 32)
    return f"Current weather in {location}: {random.choice(conditions)}, {temp}°C."

def get_crowd_status(location="Temple of the Tooth"):
    levels = ["High (Avoid) 🔴", "Medium (Okay) 🟡", "Low (Great time!) 🟢"]
    return f"Live crowd level at {location}: {random.choice(levels)}"

@router.post("/chat", response_model=ChatResponse)
async def chat_agent(request: ChatRequest):
    user_input = request.message
    user_input_lower = user_input.lower()
    
    # 1. TOOL: Tour Planner (Integrated Hybrid Logic)
    if "plan" in user_input_lower and ("tour" in user_input_lower or "trip" in user_input_lower):
        
        # Optimization Mode (Kandy)
        if "kandy" in user_input_lower or "optimize" in user_input_lower:
            if not research_tour_planner:
                return ChatResponse(response="Tour Planner module is not available.", action_type="error")
            
            try:
                # In a real API, we would upload the HTML to S3/Cloud and return URL
                # Here we just generate it locally and return the success message
                result = research_tour_planner.generate_tour_plan()
                # For API, we might return a static URL to the map if served
                map_url = "http://localhost:8000/static/minimal_tour_map.html" 
                return ChatResponse(
                    response=f"I have optimized your Kandy tour using the Genetic Algorithm. {result} (Map available at {map_url})", 
                    action_type="map"
                )
            except Exception as e:
                 return ChatResponse(response=f"Error running planner: {str(e)}", action_type="error")

        # General LLM Planning Mode
        else:
            if not model:
                 return ChatResponse(response="AI Model is not loaded.", action_type="error")
            
            prompt = (
                "System: You are an expert Sri Lanka Travel Agent. Create a detailed itinerary. "
                "User: " + user_input
            )
            inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = model.generate(inputs["input_ids"], max_length=400, num_beams=4, early_stopping=True, temperature=0.7)
            reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return ChatResponse(response=reply, action_type="chat")

    # 2. TOOL: Weather
    if "weather" in user_input_lower:
        return ChatResponse(response=get_weather_update(), action_type="weather")

    # 3. TOOL: Crowd
    if "crowd" in user_input_lower or "busy" in user_input_lower:
        return ChatResponse(response=get_crowd_status(), action_type="crowd")

    # 4. FALLBACK: Normal Chat
    if not model:
         return ChatResponse(response="AI Brain is offline.", action_type="error")

    prompt = (
        "System: You are an expert Sri Lanka Travel Assistant. "
        "Guidelines: Be polite, factual, and strictly focused on Sri Lankan tourism. "
        "User: " + user_input
    )
    inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=150, num_beams=4, early_stopping=True, temperature=0.7)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return ChatResponse(response=reply, action_type="chat")
