from typing import Dict, Any, List
from .models import Event, Team

def parse_team(data: Dict[str, Any]) -> Team:
    """Parse raw team data into a Team model."""
    return Team.model_validate(data)

def parse_event(data: Dict[str, Any]) -> Event:
    """Parse raw event data into an Event model."""
    # First parse the team objects
    home_team = parse_team(data.get("homeTeam", {}))
    away_team = parse_team(data.get("awayTeam", {}))
    
    # Then create the event with properly parsed teams
    return Event.model_validate({
        "id": data.get("id"),
        "slug": data.get("slug"),
        "tournament": data.get("tournament"),
        "home_team": home_team,
        "away_team": away_team,
        "start_timestamp": data.get("startTimestamp"),
    })