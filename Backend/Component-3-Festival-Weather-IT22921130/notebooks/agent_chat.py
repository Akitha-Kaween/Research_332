
import sys
import os
import torch
import random
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Import our customized Tool
try:
    import research_tour_planner
except ImportError:
    # Handle running from root directory vs notebooks directory
    sys.path.append(os.path.join(os.getcwd(), 'Component-3-Festival-Weather-IT22921130', 'notebooks'))
    try:
        import research_tour_planner
    except ImportError:
        print("Warning: Could not import Tour Planner module.")

# 1. Load Fine-Tuned Model
MODEL_PATH = "./sri_lanka_flan_t5"
# Adjust path if running from notebooks folder
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "../sri_lanka_flan_t5" # Try parent
    if not os.path.exists(MODEL_PATH):
         MODEL_PATH = "Component-3-Festival-Weather-IT22921130/notebooks/sri_lanka_flan_t5" # Try full path

print(f"Loading Intelligent Agent from {MODEL_PATH}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
except:
    print("Error: Model not found. Please run train_llm.py first.")
    exit()

# 2. Define Mock Tools (Simulating API Calls)
def get_weather_update(location="Kandy"):
    conditions = ["Sunny ☀️", "Rainy 🌧️", "Cloudy ☁️", "Windy 💨"]
    temp = random.randint(22, 32)
    return f"[API] Current weather in {location}: {random.choice(conditions)}, {temp}°C."

def get_crowd_status(location="Temple of the Tooth"):
    levels = ["High (Avoid) 🔴", "Medium (Okay) 🟡", "Low (Great time!) 🟢"]
    return f"[API] Live crowd level at {location}: {random.choice(levels)}"

# 3. Agent Logic (Intent Recognition)
def agent_response(user_input):
    user_input_lower = user_input.lower()
    
    # --- TOOL: Tour Planner (Integrated Hybrid Logic) ---
    if "plan" in user_input_lower and ("tour" in user_input_lower or "trip" in user_input_lower):
        
        # 1. OPTIMIZATION: If request is specific to Kandy or explicitly asks for optimization
        if "kandy" in user_input_lower or "optimize" in user_input_lower:
            print("\n🤖 Agent: Detected intent 'OPTIMIZE_ROUTE_KANDY'. Launching Genetic Algorithm...")
            try:
                result = research_tour_planner.generate_tour_plan()
                return f"I have run the Multi-Objective Genetic Algorithm for you. {result} Open the HTML file to see the optimized route."
            except Exception as e:
                return f"Error running Tour Planner: {e}"
                
        # 2. GENERAL CLASSIFICATION: If request is for a long trip (e.g. 10 days) or whole country
        else:
            print("\n🤖 Agent: Detected intent 'GENERAL_ITINERARY_PLANNING'. Using LLM Brain...")
            # We let the LLM handle this, but we prepend a special instruction to be detailed
            prompt = (
                "System: You are an expert Sri Lanka Travel Agent. Create a detailed itinerary. "
                "User: " + user_input
            )
            inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = model.generate(
                inputs["input_ids"], 
                max_length=400, # Allow longer response for 10-day plans
                num_beams=4, 
                early_stopping=True,
                temperature=0.7
            )
            return tokenizer.decode(outputs[0], skip_special_tokens=True)

    # --- TOOL: Weather API ---
    if "weather" in user_input_lower:
        print("\n🤖 Agent: Detected intent 'CHECK_WEATHER'. Calling Weather API...")
        return get_weather_update()
        
    # --- TOOL: Crowd API ---
    if "crowd" in user_input_lower or "busy" in user_input_lower:
        print("\n🤖 Agent: Detected intent 'CHECK_CROWD'. Calling Crowd Analysis API...")
        return get_crowd_status()

    # --- FALLBACK: LLM Chat ---
    # Construct Prompt with System Persona
    prompt = (
        "System: You are an expert Sri Lanka Travel Assistant. "
        "Guidelines: Be polite, factual, and strictly focused on Sri Lankan tourism. "
        "User: " + user_input
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)
    outputs = model.generate(
        inputs["input_ids"], 
        max_length=150, 
        num_beams=4, 
        early_stopping=True,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 4. Interactive Loop
if __name__ == "__main__":
    print("-" * 60)
    print("🤖 Smart Sri Lanka Agent (Integrated with Tools)")
    print("Capabilities: Chat, Tour Planning (GA), Weather, Crowd Analysis")
    print("Type 'exit' to quit.")
    print("-" * 60)

    while True:
        user_in = input("\nYou: ")
        if user_in.lower() in ["exit", "quit"]:
            break
            
        response = agent_response(user_in)
        print(f"Bot: {response}")
