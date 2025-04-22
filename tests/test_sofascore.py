import pytest
from datetime import date
from src.adapter.sofascore import list_live_events, list_events_for_day

def test_list_live_events():
    """Test listing live events."""
    events = list_live_events()
    # Basic validation - events should be a list
    assert isinstance(events, list)
    
    # If there are events, check their structure
    if events:
        event = events[0]
        assert hasattr(event, 'id')
        assert hasattr(event, 'home_team')
        assert hasattr(event, 'away_team')

def test_list_events_for_day():
    """Test listing events for a specific day."""
    today = date.today()
    events = list_events_for_day(today)
    assert isinstance(events, list)