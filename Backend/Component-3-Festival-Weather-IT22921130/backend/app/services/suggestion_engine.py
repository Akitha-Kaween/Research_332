from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from datetime import datetime, date
import asyncio
from sqlalchemy.orm import Session
from app.services.weather_service import weather_service
from app.services.holiday_service import holiday_service
from app.services.festival_service import festival_service
from loguru import logger

@dataclass
class Rule:
    id: str
    condition: Callable
    action: Callable
    priority: str = "medium"

class SuggestionEngine:
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[Rule]:
        """Initialize all suggestion rules"""
        return [
            Rule(
                id="rain_outdoor_festival",
                condition=lambda data: (
                    data.get("weather", {}).get("rainfall", 0) > 5 and
                    data.get("festival") and
                    data["festival"].get("type") == "outdoor"
                ),
                action=lambda data: {
                    "type": "warning",
                    "priority": "high",
                    "message": f"Heavy rain expected during {data['festival']['name']}. Consider indoor alternatives.",
                    "alternatives": [
                        "Visit indoor museums nearby",
                        "Reschedule visit to another day",
                        "Check covered viewing areas"
                    ]
                }
            ),
            Rule(
                id="holiday_attraction_closed",
                condition=lambda data: (
                    data.get("holiday") is not None and
                    data["holiday"].get("is_public", False)
                ),
                action=lambda data: {
                    "type": "alert",
                    "priority": "high",
                    "message": f"Attractions may be closed on {data['holiday']['name']}. Verify opening hours before visiting.",
                    "alternatives": [
                        "Visit on alternative date",
                        "Check attraction schedule in advance",
                        "Contact venue for confirmation"
                    ]
                }
            ),
            Rule(
                id="festival_crowd_warning",
                condition=lambda data: (
                    data.get("festival") is not None and
                    data.get("crowd_prediction", 0) > 70
                ),
                action=lambda data: {
                    "type": "info",
                    "priority": "medium",
                    "message": f"High crowds expected during {data['festival']['name']}. Visit during off-peak hours for better experience.",
                    "suggestions": [
                        "Visit early morning (6-8 AM)",
                        "Visit on weekdays instead of weekends",
                        "Book tickets in advance"
                    ]
                }
            ),
            Rule(
                id="perfect_weather_festival",
                condition=lambda data: (
                    data.get("weather", {}).get("condition") in ["Clear", "Clouds"] and
                    data.get("weather", {}).get("rainfall", 0) < 1 and
                    data.get("festival") is not None and
                    data.get("holiday") is None
                ),
                action=lambda data: {
                    "type": "recommendation",
                    "priority": "low",
                    "message": f"Perfect weather for {data['festival']['name']}! Great time to visit and experience the cultural festivities.",
                    "cultural_info": data["festival"].get("cultural_significance", "")
                }
            ),
            Rule(
                id="hot_weather_warning",
                condition=lambda data: (
                    data.get("weather", {}).get("temperature", 0) > 35
                ),
                action=lambda data: {
                    "type": "warning",
                    "priority": "medium",
                    "message": "Very hot weather expected. Take precautions to stay hydrated and avoid heat exhaustion.",
                    "suggestions": [
                        "Carry water bottle",
                        "Wear sunscreen and hat",
                        "Take breaks in shaded areas",
                        "Avoid midday sun (11 AM - 3 PM)"
                    ]
                }
            ),
            Rule(
                id="monsoon_season_warning",
                condition=lambda data: (
                    data.get("weather", {}).get("rainfall", 0) > 10 or
                    data.get("weather", {}).get("humidity", 0) > 85
                ),
                action=lambda data: {
                    "type": "alert",
                    "priority": "high",
                    "message": "Heavy monsoon conditions expected. Outdoor activities may be affected.",
                    "alternatives": [
                        "Visit indoor attractions",
                        "Carry rain gear",
                        "Check for weather updates regularly"
                    ]
                }
            ),
            Rule(
                id="religious_festival_respect",
                condition=lambda data: (
                    data.get("festival") and
                    data["festival"].get("type") == "religious"
                ),
                action=lambda data: {
                    "type": "info",
                    "priority": "medium",
                    "message": f"{data['festival']['name']} is a religious festival. Please dress modestly and respect local customs.",
                    "suggestions": [
                        "Wear modest clothing covering shoulders and knees",
                        "Remove shoes when entering temples",
                        "Ask permission before taking photos",
                        "Maintain respectful behavior"
                    ]
                }
            )
        ]
    
    async def generate_suggestions(
        self, 
        db: Session,
        location: Dict,
        target_date: date,
        crowd_prediction: Optional[int] = None
    ) -> List[Dict]:
        """Generate smart suggestions based on all data"""
        try:
            # Fetch all data in parallel
            weather_task = weather_service.get_current_weather(location["lat"], location["lon"])
            holiday_task = holiday_service.check_if_holiday(datetime.combine(target_date, datetime.min.time()))
            
            # Festivals need database session, can't be async
            festivals = festival_service.get_festivals_by_date(db, target_date)
            
            # Wait for async tasks
            weather, holiday = await asyncio.gather(weather_task, holiday_task)
            
            # Prepare context data
            context_data = {
                "weather": weather,
                "holiday": holiday,
                "festival": festivals[0].to_dict() if festivals else None,
                "crowd_prediction": crowd_prediction or 50  # Default moderate crowd
            }
            
            # Evaluate all rules
            suggestions = []
            for rule in self.rules:
                try:
                    if rule.condition(context_data):
                        suggestion = rule.action(context_data)
                        suggestion["rule_id"] = rule.id
                        suggestions.append(suggestion)
                except Exception as e:
                    logger.warning(f"Rule {rule.id} evaluation failed: {str(e)}")
                    continue
            
            # Prioritize suggestions
            prioritized = self._prioritize_suggestions(suggestions)
            logger.info(f"Generated {len(prioritized)} suggestions for {location} on {target_date}")
            
            return prioritized
            
        except Exception as e:
            logger.error(f"Suggestion generation error: {str(e)}")
            return []
    
    def _prioritize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Sort suggestions by priority"""
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(
            suggestions,
            key=lambda x: priority_order.get(x.get("priority", "medium"), 2)
        )
    
    async def generate_dashboard_data(
        self,
        db: Session,
        location: Dict,
        location_name: str,
        target_date: date
    ) -> Dict:
        """Generate unified dashboard with all data"""
        try:
            # Fetch weather and holiday in parallel
            weather_task = weather_service.get_current_weather(location["lat"], location["lon"])
            holiday_task = holiday_service.get_public_holidays(target_date.year)
            
            # Get festivals from database
            festivals = festival_service.get_festivals_by_date(db, target_date)
            
            # Wait for async tasks
            weather, all_holidays = await asyncio.gather(weather_task, holiday_task)
            
            # Filter holidays for the specific date
            date_str = target_date.isoformat()
            relevant_holidays = [h for h in all_holidays if h["date"] == date_str]
            
            # Generate suggestions
            suggestions = await self.generate_suggestions(
                db, location, target_date
            )
            
            return {
                "location": location_name,
                "date": date_str,
                "weather": weather,
                "holidays": relevant_holidays,
                "festivals": [f.to_dict() for f in festivals],
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Dashboard generation error: {str(e)}")
            raise

suggestion_engine = SuggestionEngine()
