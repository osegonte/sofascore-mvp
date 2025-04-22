from typing import Dict, Any, Optional
from src.adapter.sofascore import fetch_event_stats

class StatsService:
    """Service for working with sports statistics."""
    
    @staticmethod
    def get_event_statistics(event_id: int) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific event."""
        try:
            return fetch_event_stats(event_id)
        except Exception as e:
            print(f"Error fetching statistics for event {event_id}: {e}")
            return None