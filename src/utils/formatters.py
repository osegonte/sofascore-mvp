from src.adapter.models import Event
from typing import Dict, Any
from datetime import datetime

def format_event_display(event: Event) -> str:
    """Format an event for display in the CLI."""
    home = event.home_team.name
    away = event.away_team.name
    tournament = event.tournament.get("name", "Unknown Tournament")
    
    # Format timestamp to local time
    event_time = datetime.fromtimestamp(event.start_timestamp).strftime("%Y-%m-%d %H:%M")
    
    return f"{home} vs {away} ({tournament}) - {event_time}"