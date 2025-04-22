# src/adapter/models.py
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Team(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    # Add other fields as needed

class Event(BaseModel):
    id: int
    slug: str
    tournament: Dict[str, Any]
    home_team: Team
    away_team: Team
    start_timestamp: int