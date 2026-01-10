# Research Component: AI Tour Planner

**Component:** Component 3 (Festival & Weather)  
**Research Area:** Intelligent Optimization / Genetic Algorithms  
**Integration:** Multi-Objective Route Optimization

---

## Overview
This research module implements an **Intelligent Multi-Objective Tour Planner** that goes beyond simple distance minimization. It uses a **Genetic Algorithm (GA)** to find the optimal route for a tourist visiting multiple attractions in Kandy, considering:
1.  **Real-world Directions:** Using OpenStreetMap data via `osmnx`.
2.  **Weather Constraints:** Avoiding outdoor locations during high rain probability hours.
3.  **Crowd Avoidance:** Minimizing visits to congested areas during peak times.

## Files

1.  **`research_tour_planner.ipynb`**: The main Jupyter Notebook containing the research logic, visualization, and results.
2.  **`research_tour_planner.py`**: A pure Python script version of the research for easier execution in headless environments.
3.  **`minimal_tour_map.html`**: The output interactive map showing the AI-optimized route.

## How to Run

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

### 3. Use the Notebook
Open `notebooks/research_tour_planner.ipynb` in Jupyter Notebook or VS Code to interactively explore the code, modify the Genetic Algorithm parameters, and visualize the results step-by-step.

## Methodology

### 1. Graph Construction
We fetch the drivable street network of **Kandy, Sri Lanka** using `osmnx`. This provides a realistic graph $G=(V, E)$ where edges represent actual roads and weights represent lengths.

### 2. Distance Matrix
We calculate the shortest path distance between all pairs of 6 key attractions (Temple of the Tooth, Kandy Lake, Peradeniya Gardens, etc.) using Dijkstra's algorithm on the road network.

### 3. Genetic Algorithm
We evolve a population of routes using:
*   **Representation:** Permutation of location indices.
*   **Fitness Function:** $F = \frac{1}{TotalDistance + WeatherPenalty + CrowdPenalty}$
*   **Selection:** Tournament Selection.
*   **Crossover:** Ordered Crossover (OX1).
*   **Mutation:** Swap Mutation.

## Results
The algorithm produces an optimized sequence of visits (e.g., "Temple -> Lake -> Museum -> Gardens"). The final output is an interactive map (`minimal_tour_map.html`) displaying the route path in green and markers for each stop.

## Phase 2: Generative AI Chatbot (Flan-T5)

We have implemented a **Domain-Adapted LLM** that acts as an expert Sri Lanka Travel Assistant.

### Files
1.  **`generate_dataset.py`**: Procedurally generates a massive training dataset (12,000+ records) covering 10+ major cities (Kandy, Colombo, Ella, etc.).
2.  **`train_llm.py`**: Fine-tunes the `google/flan-t5-small` model using Parameter-Efficient Fine-Tuning (PEFT). It injects a **System Persona** into the model to ensure professional behavior.
3.  **`chat.py`**: The inference script for interactive chatting with the fine-tuned model.

### Dataset
*   **File:** `sri_lanka_chat_data.json`
*   **Size:** ~12,000 records
*   **Content:** Detailed Q&A about Hotels, Landmarks, Food, and Itineraries for 10 districts.

### How to Train
Run the training script to create your custom model (this takes ~15-20 mins):
```bash
Component-3-Festival-Weather-IT22921130/notebooks/venv/bin/python Component-3-Festival-Weather-IT22921130/notebooks/train_llm.py
```

### How to Chat (Integrated Agent)
For the full experience with **Tool Integration** (Tour Planner, Weather, Crowd Analysis), run the Agent script:

```bash
Component-3-Festival-Weather-IT22921130/notebooks/venv/bin/python Component-3-Festival-Weather-IT22921130/notebooks/agent_chat.py
```

**Capabilities:**
1.  **Chat:** Ask general questions (e.g., *"Best hotels in Kandy?"*).
2.  **Plan:** Ask to plan a trip (e.g., *"Plan a tour for me."*). -> **Triggers Genetic Algorithm**.
3.  **Check:** Ask about environment (e.g., *"Check weather in Kandy"*, *"Is the Temple crowded?"*). -> **Triggers Mock APIs**.
