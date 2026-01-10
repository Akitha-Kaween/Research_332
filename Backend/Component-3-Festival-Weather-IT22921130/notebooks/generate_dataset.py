import json
import random
import os

# 1. Knowledge Base (Procedural Lists)
cities = [
    "Kandy", "Colombo", "Galle", "Ella", "Sigiriya", "Nuwara Eliya", "Jaffna", 
    "Anuradhapura", "Polonnaruwa", "Trincomalee", "Mirissa", "Unawatuna", 
    "Arugam Bay", "Dambulla", "Negombo", "Bentota", "Hikkaduwa", "Matara", 
    "Ratnapura", "Badulla"
]

attractions = {
    "Kandy": ["Temple of the Tooth", "Kandy Lake", "Peradeniya Botanical Gardens", "Bahirawakanda Buddha", "Udawatta Kele"],
    "Colombo": ["Lotus Tower", "Galle Face Green", "National Museum", "Gangaramaya Temple", "Pettah Market"],
    "Galle": ["Galle Fort", "Dutch Reformed Church", "Maritime Museum", "Jungle Beach", "Lighthouse"],
    "Ella": ["Nine Arch Bridge", "Little Adam's Peak", "Ella Rock", "Ravana Falls", "Demodara Loop"],
    "Sigiriya": ["Lion Rock", "Pidurangala Rock", "Mirror Wall", "Water Gardens", "Museum"],
    "Nuwara Eliya": ["Gregory Lake", "Horton Plains", "Victoria Park", "Pedro Tea Estate", "Moon Plains"],
    "Jaffna": ["Nallur Kandaswamy Kovil", "Jaffna Fort", "Public Library", "Nagadeepa", "Casuarina Beach"],
    "Anuradhapura": ["Jaya Sri Maha Bodhi", "Ruwanwelisaya", "Isurumuniya", "Thuparamaya", "Lovamahapaya"],
    "Polonnaruwa": ["Gal Vihara", "Parakrama Samudra", "Royal Palace", "Vatadage", "Rankoth Vehera"],
    "Trincomalee": ["Koneswaram Temple", "Nilaveli Beach", "Pigeon Island", "Marble Beach", "Fort Frederick"]
}

activities = ["sightseeing", "photography", "hiking", "swimming", "relaxing", "food tasting", "history exploration", "cultural tour"]

weather_conditions = ["sunny", "rainy", "cloudy", "windy", "humid"]

# 2. Templates for Question-Answer Pairs
templates = [
    {
        "q": "Plan a trip to {city}.",
        "a": "You should definitely visit {city}. Key attractions include {attraction1} and {attraction2}. It's great for {activity}."
    },
    {
        "q": "What is famous in {city}?",
        "a": "{city} is famous for {attraction1}. Don't miss out on {attraction2} while you are there."
    },
    {
        "q": "Best time to visit {city}?",
        "a": "The best time to visit {city} is usually when it is {weather} but avoiding heavy rains. {attraction1} is a must-see."
    },
    {
        "q": "Is {city} good for {activity}?",
        "a": "Yes, {city} is excellent for {activity}, especially around {attraction1}."
    },
    {
        "q": "Tell me about {attraction} in {city}.",
        "a": "{attraction} is a top landmark in {city}. It creates a perfect atmosphere for {activity}."
    },
    {
        "q": "I want to go to {city}.",
        "a": "Great choice! I will trigger the Tour Planner for {city}. Make sure to see {attraction1}."
    }
]

# 3. Generation Function (Appending Mode)
OUTPUT_FILE = "sri_lanka_chat_data.json"

def generate_batch(batch_size):
    new_data = []
    
    for _ in range(batch_size):
        city = random.choice(list(attractions.keys()))
        city_attractions = attractions.get(city, ["Main Temple", "City Center"])
        attraction1 = random.choice(city_attractions)
        attraction2 = random.choice(city_attractions)
        while attraction2 == attraction1:
            attraction2 = random.choice(city_attractions)
            
        activity = random.choice(activities)
        weather = random.choice(weather_conditions)
        
        template = random.choice(templates)
        
        # Fill template
        question = template["q"].format(city=city, attraction=attraction1, activity=activity, weather=weather)
        answer = template["a"].format(city=city, attraction1=attraction1, attraction2=attraction2, attraction=attraction1, activity=activity, weather=weather)
        
        new_data.append({
            "instruction": question,
            "input": "",
            "output": answer
        })
        
    return new_data

def append_to_file(data, filename):
    # Load existing or create new
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
        
    # Append
    existing_data.extend(data)
    
    # Save
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2)
    print(f"Appended {len(data)} records. Total: {len(existing_data)}")

# 5. SPECIAL: National Expert Expansion (Deep Dives for Major Hubs)

# Knowledge Base for "Super Expert" Level
city_specifics = {
    "Colombo": {
        "places": ["Lotus Tower", "Galle Face Green", "Gangaramaya Temple", "National Museum", "Pettah Floating Market", "One Galle Face Mall", "Independence Square", "Viharamahadevi Park", "Red Mosque (Jami Ul-Alfar)", "Mount Lavinia Beach", "Bellanwila Raja Maha Viharaya", "Kelaniya Raja Maha Vihara", "Planetarium", "Dehiwala Zoo"],
        "hotels": ["Shangri-La Colombo", "Cinnamon Grand", "The Kingsbury", "Galadari Hotel", "Taj Samudra", "Marino Beach Hotel", "Galle Face Hotel", "Mandarina Colombo", "Fairway Colombo", "Jetwing Colombo Seven", "Cinnamon Red", "Movenpick Hotel"],
        "food": ["Ministry of Crab", "Nihonbashi", "Upali's by Nawaloka", "The Gallery Cafe", "Beach Wadey at Galle Face", "Pilawoos (Kottu)", "Monsoon Colombo", "Isso", "Black Cat Cafe", "Barefoot Garden Cafe"]
    },
    "Galle": {
        "places": ["Galle Fort", "Galle Lighthouse", "Dutch Reformed Church", "Maritime Archaeology Museum", "Jungle Beach", "Unawatuna Beach", "Japanese Peace Pagoda", "Rumassala Sanctuary", "National Museum of Galle", "Sea Turtle Hatchery", "Koggala Lake", "Hikkaduwa Coral Reef"],
        "hotels": ["Amari Galle", "Jetwing Lighthouse", "Le Grand Galle", "The Fortress Resort", "Galle Fort Hotel", "Tamarind Hill", "Coco Bay Unawatuna", "Araliya Beach Resort", "Riu Sri Lanka"],
        "food": ["A Minute by Tuk Tuk", "Pedlar's Inn Cafe", "Lucky Fort Restaurant", "The Tuna & The Crab", "Coconut Sambol", "Isle of Gelato", "Dairy King", "Sugar Bistro"]
    },
    "Ella": {
        "places": ["Nine Arch Bridge", "Little Adam's Peak", "Ella Rock", "Ravana Falls", "Demodara Loop", "Lipton's Seat", "Diyaluma Falls", "Ella Spice Garden", "Flying Ravana Zipline"],
        "hotels": ["98 Acres Resort", "Mountain Heavens", "Ella Jungle Resort", "Chillville View", "Ekho Ella", "Morning Dew Hotel", "Oak Ray Ella Gap"],
        "food": ["Cafe Chill", "Matey Hut", "AK Ristoro", "Ella Village Restaurant", "MozzarElla", "Dream Cafe", "360 Ella"]
    },
    "Nuwara Eliya": {
        "places": ["Gregory Lake", "Victoria Park", "Horton Plains (World's End)", "Pedro Tea Estate", "Hakgala Botanical Garden", "Moon Plains", "Post Office Nuwara Eliya", "Lover's Leap Waterfall", "St. Clair's Falls", "Devon Falls", "Ambeywela Farm"],
        "hotels": ["Grand Hotel", "Araliya Green City", "Heritance Tea Factory", "Jetwing St. Andrew's", "The Golden Ridge", "Westbury Palace", "Araliya Red"],
        "food": ["Grand Indian", "The Pub", "Tea Factory Hotel Restaurant", "De Silva Food Centre", "Milano Restaurant", "Barnes Hall"]
    },
    "Sigiriya_Dambulla": {
        "places": ["Sigiriya Lion Rock", "Pidurangala Rock", "Dambulla Cave Temple", "Minneriya National Park (Elephant Gathering)", "Polonnaruwa Ancient City", "Hiriwadunna Village", "Ibbankatuwa Megalithic Tombs"],
        "hotels": ["Heritance Kandalama", "Aliya Resort & Spa", "Jetwing Vil Uyana", "Water Garden Sigiriya", "Cinnamon Lodge Habarana", "Sigiriana Resort"],
        "food": ["Pradeep Restaurant", "Rithu Restaurant", "Mango Mango", "Shenadi Restaurant", "Gimanhala"]
    },
    "Jaffna": {
        "places": ["Nallur Kandaswamy Kovil", "Jaffna Fort", "Jaffna Public Library", "Nagadeepa Purana Vihara", "Casuarina Beach", "Keerimalai Hot Springs", "Point Pedro", "Delft Island", "Dambakola Patuna"],
        "hotels": ["Jetwing Jaffna", "North Gate by Jetwing", "Fox Jaffna", "Tilko Jaffna City Hotel", "Valampuri Hotel"],
        "food": ["Mangos", "Malayan Cafe", "Rio Ice Cream", "Cosy Restaurant", "Nallur Bhavan"]
    },
    "South_Coast": {
        "places": ["Mirissa Whale Watching", "Coconut Tree Hill", "Parrot Rock", "Secret Beach Mirissa", "Weligama Surf Point", "Matara Fort", "Dondra Head Lighthouse", "Polhena Beach", "Hummanaya Blow Hole"],
        "hotels": ["Sri Sharavi Beach Villas", "Mandara Resort", "Weligama Bay Marriott", "Paragon Beach Resort", "Triple O Six"],
        "food": ["Zephyr Restaurant", "Dewmini Roti Shop", "No. 1 Dewmini Roti Shop", "Shady Lane Mirissa", "Hangover Cafe"]
    }
}

kandy_specifics = {
    "towns": ["Kandy City", "Peradeniya", "Katugastota", "Digana", "Kundasale", "Hanthana", "Pilimathalawa", "Gampola"],
    "detailed_attractions": [
        "Temple of the Sacred Tooth Relic", "Royal Botanical Gardens", "Udawatta Kele Sanctuary", 
        "International Buddhist Museum", "Kandy Lake Club", "Bahirawakanda Vihara", 
        "Hanthana Mountain Range", "Ceylon Tea Museum", "Degaldoruwa Raja Maha Vihara", 
        "Gadaladeniya Temple", "Embekka Devalaya", "Lankatilaka Vihara", 
        "Pallekele Cricket Stadium", "Victoria Dam", "Knuckles Mountain Range",
        "The Grand Kandyan", "Earl's Regency Hotel", "Queen's Hotel", "Cinnamon Citadel Kandy",
        "The Empire Cafe", "Kandy Muslim Hotel", "Devon Restaurant", "Balaji Dosai"
    ],
    "cultural_activities": [
        "watching a Kandyan dance performance", "offering flowers at the temple", "walking around the lake",
        "shopping for batiks", "visiting a tea factory", "hiking in the mountains", "meditation"
    ]
}

def generate_expert_city_batch(city_name, data, batch_size):
    city_data = []
    print(f"Generating Deep Dive for {city_name}...")
    
    places = data.get("places", [])
    hotels = data.get("hotels", [])
    foods = data.get("food", [])
    
    for _ in range(batch_size):
        category = random.choice(["place", "hotel", "food", "itinerary"])
        
        if category == "place" and places:
            item = random.choice(places)
            q = random.choice([
                f"Is {item} in {city_name} worth it?",
                f"Tell me about {item}.",
                f"History of {item}?",
                f"Opening hours for {item}?"
            ])
            a = f"{item} is a must-visit in {city_name}. It offers unique insights into the region's culture/nature. Best visited in the morning."
            
        elif category == "hotel" and hotels:
            item = random.choice(hotels)
            q = random.choice([
                f"Where should I stay in {city_name}?",
                f"Is {item} a good hotel?",
                f"Luxury stays in {city_name}?",
                f"Reviews for {item}?"
            ])
            a = f"{item} is widely recommended for varied budgets. It is located conveniently near main attractions of {city_name}."
            
        elif category == "food" and foods:
            item = random.choice(foods)
            q = random.choice([
                f"Best food in {city_name}?",
                f"Have you tried {item}?",
                f"Where to eat in {city_name}?",
                f"Famous dishes at {item}?"
            ])
            a = f"You must try {item} in {city_name}. It is famous for authentic local cuisine and great service."
            
        else:
            q = f"Plan a day in {city_name}."
            p1 = random.choice(places) if places else "City Center"
            p2 = random.choice(places) if places else "Market"
            f1 = random.choice(foods) if foods else "Local Cafe"
            a = f"Start your day at {p1}, then have lunch at {f1}. In the evening, visit {p2} for sunset."

        city_data.append({
            "instruction": q,
            "input": "",
            "output": a
        })
    return city_data

def generate_kandy_batch(batch_size):
    # (Keeping existing Kandy logic for backward compatibility, but simplified)
    return generate_expert_city_batch("Kandy", {"places": kandy_specifics["detailed_attractions"], "hotels": [], "food": []}, batch_size)

# 4. Main Execution
if __name__ == "__main__":
    # 1. General Knowledge (2000 records)
    print("Generating General Knowledge...")
    batch = generate_batch(2000)
    append_to_file(batch, OUTPUT_FILE)
    
    # 2. Deep Dive: Kandy (1500 records)
    kandy_batch = generate_kandy_batch(1500)
    append_to_file(kandy_batch, OUTPUT_FILE)
    
    # 3. Deep Dive: Other Major Hubs (1000 records EACH)
    for city, details in city_specifics.items():
        city_batch = generate_expert_city_batch(city.replace("_", " "), details, 1200)
        append_to_file(city_batch, OUTPUT_FILE)
    
    print(f"DONE. Generated Massive National Expert Dataset in '{OUTPUT_FILE}'.")
