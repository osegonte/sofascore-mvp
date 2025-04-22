"""
Response schemas for SofaScore API.
These schemas define the structure of API responses.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TeamSchema(BaseModel):
    """Schema for a team in API responses."""
    id: int
    name: str
    slug: Optional[str] = None
    country: Optional[Dict[str, Any]] = None
    
class PlayerSchema(BaseModel):
    """Schema for a player in API responses."""
    id: int
    name: str
    slug: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[int] = Field(None, alias="jerseyNumber")
    
class ScoreSchema(BaseModel):
    """Schema for event scores."""
    current: Optional[int] = None
    display: Optional[int] = None
    period1: Optional[int] = None
    period2: Optional[int] = None
    normaltime: Optional[int] = None
    
class TournamentSchema(BaseModel):
    """Schema for a tournament."""
    id: int
    name: str
    slug: Optional[str] = None
    category: Optional[Dict[str, Any]] = None
    
class EventSchema(BaseModel):
    """Schema for an event/match."""
    id: int
    slug: str
    homeTeam: TeamSchema
    awayTeam: TeamSchema
    tournament: TournamentSchema
    startTimestamp: int
    status: Optional[Dict[str, Any]] = None
    homeScore: Optional[ScoreSchema] = None
    awayScore: Optional[ScoreSchema] = None
    
class StatisticItemSchema(BaseModel):
    """Schema for a single statistic item."""
    name: str
    home: Any = None
    away: Any = None
    
class StatisticGroupSchema(BaseModel):
    """Schema for a group of statistic items."""
    groupName: str
    statisticsItems: List[StatisticItemSchema]
    
class StatisticsSchema(BaseModel):
    """Schema for a set of statistics."""
    name: str
    groups: List[StatisticGroupSchema]