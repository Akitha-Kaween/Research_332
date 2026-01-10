from datetime import date
from app.config.database import SessionLocal
from app.models.festival import Festival
from loguru import logger

def seed_festivals():
    """Seed Sri Lankan festivals into database"""
    db = SessionLocal()
    
    festivals_data = [
        {
            "name": "Esala Perahera",
            "location": "Kandy",
            "start_date": date(2026, 7, 25),
            "end_date": date(2026, 8, 5),
            "type": "outdoor",
            "description": "The Esala Perahera is the grand festival of Esala held in Sri Lanka. It is one of the oldest and grandest of all Buddhist festivals in Sri Lanka.",
            "cultural_significance": "Features a grand procession with traditional dancers, drummers, and decorated elephants. The sacred tooth relic of Buddha is paraded through the streets."
        },
        {
            "name": "Vesak",
            "location": "Nationwide",
            "start_date": date(2026, 5, 15),
            "end_date": date(2026, 5, 17),
            "type": "religious",
            "description": "Vesak commemorates the birth, enlightenment, and death of Buddha.",
            "cultural_significance": "Celebrated with lanterns, decorations, dansalas (free food stalls), and religious observances. Streets are illuminated with colorful lanterns."
        },
        {
            "name": "Poson",
            "location": "Anuradhapura, Mihintale",
            "start_date": date(2026, 6, 13),
            "end_date": date(2026, 6, 15),
            "type": "religious",
            "description": "Poson commemorates the introduction of Buddhism to Sri Lanka.",
            "cultural_significance": "Pilgrims climb Mihintale mountain. Religious observances and processions mark this important Buddhist festival."
        },
        {
            "name": "Sinhala and Tamil New Year",
            "location": "Nationwide",
            "start_date": date(2026, 4, 13),
            "end_date": date(2026, 4, 14),
            "type": "cultural",
            "description": "Traditional New Year celebrated by both Sinhalese and Tamil communities.",
            "cultural_significance": "Families gather for traditional games, rituals, and special foods. Marks the end of harvest season."
        },
        {
            "name": "Thai Pongal",
            "location": "Northern and Eastern Provinces",
            "start_date": date(2026, 1, 14),
            "end_date": date(2026, 1, 15),
            "type": "cultural",
            "description": "Tamil harvest festival dedicated to the Sun God.",
            "cultural_significance": "Traditional dish 'Pongal' is prepared. Homes are decorated with kolam (rice flour designs)."
        },
        {
            "name": "Deepavali",
            "location": "Nationwide (Tamil communities)",
            "start_date": date(2026, 10, 29),
            "end_date": date(2026, 10, 30),
            "type": "religious",
            "description": "Festival of Lights celebrated by Hindus.",
            "cultural_significance": "Homes are lit with oil lamps, fireworks are displayed, and sweets are shared among families."
        },
        {
            "name": "Nallur Festival",
            "location": "Jaffna",
            "start_date": date(2026, 8, 10),
            "end_date": date(2026, 8, 31),  # Fixed: was 35
            "type": "outdoor",
            "description": "Annual Hindu festival at Nallur Kandaswamy Temple.",
            "cultural_significance": "25-day festival featuring chariot processions, traditional music, and religious ceremonies."
        },
        {
            "name": "Christmas",
            "location": "Nationwide",
            "start_date": date(2026, 12, 25),
            "end_date": date(2026, 12, 26),
            "type": "religious",
            "description": "Christian celebration of the birth of Jesus Christ.",
            "cultural_significance": "Churches hold midnight masses, homes are decorated, and traditional Christmas cakes are prepared."
        },
        {
            "name": "Kandy Perahera",
            "location": "Kandy",
            "start_date": date(2026, 7, 25),
            "end_date": date(2026, 8, 5),
            "type": "outdoor",
            "description": "Grand cultural pageant featuring elephants, dancers, and drummers.",
            "cultural_significance": "One of Asia's most spectacular cultural events, showcasing Sri Lankan traditional arts."
        },
        {
            "name": "Duruthu Perahera",
            "location": "Kelaniya",
            "start_date": date(2026, 1, 10),
            "end_date": date(2026, 1, 12),
            "type": "outdoor",
            "description": "Buddhist festival at Kelaniya Raja Maha Vihara.",
            "cultural_significance": "Commemorates Buddha's first visit to Sri Lanka. Features a grand procession."
        }
    ]
    
    try:
        # Check if festivals already exist
        existing_count = db.query(Festival).count()
        if existing_count > 0:
            logger.info(f"Database already has {existing_count} festivals. Skipping seed.")
            return
        
        # Add festivals
        for festival_data in festivals_data:
            festival = Festival(**festival_data)
            db.add(festival)
        
        db.commit()
        logger.info(f"Successfully seeded {len(festivals_data)} festivals")
        
    except Exception as e:
        logger.error(f"Error seeding festivals: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_festivals()
