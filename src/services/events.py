from datetime import date
from typing import List, Optional
from src.adapter.models import Event
from src.adapter.sofascore import list_events_for_day, list_live_events, fetch_event

class EventService:
    """Service for working with sports events."""
    
    @staticmethod
    def get_live_events() -> List[Event]:
        """Get all currently live events."""
        return list_live_events()
    
    @staticmethod
    def get_events_for_day(day: date) -> List[Event]:
        """Get all events for a specific day."""
        return list_events_for_day(day)