import pytest
from src.adapter.models import Team, Event

def test_team_model():
    """Test Team model validation."""
    # Test with minimal data
    team_data = {
        "id": 1,
        "name": "Test Team"
    }
    team = Team.model_validate(team_data)
    assert team.id == 1
    assert team.name == "Test Team"
    assert team.slug is None
    
    # Test with optional fields
    team_data_full = {
        "id": 2,
        "name": "Full Team",
        "slug": "full-team"
    }
    team_full = Team.model_validate(team_data_full)
    assert team_full.id == 2
    assert team_full.name == "Full Team"
    assert team_full.slug == "full-team"
    
    # Test with invalid data
    with pytest.raises(Exception):
        Team.model_validate({"name": "Missing ID"})
    
    with pytest.raises(Exception):
        Team.model_validate({"id": "not-an-int", "name": "Invalid ID"})

def test_event_model():
    """Test Event model validation."""
    # Create test data
    home_team = Team.model_validate({"id": 1, "name": "Home Team"})
    away_team = Team.model_validate({"id": 2, "name": "Away Team"})
    
    event_data = {
        "id": 1001,
        "slug": "home-vs-away",
        "tournament": {"id": 5, "name": "Test Tournament"},
        "home_team": home_team,
        "away_team": away_team,
        "start_timestamp": 1650000000
    }
    
    # Test validation
    event = Event.model_validate(event_data)
    assert event.id == 1001
    assert event.slug == "home-vs-away"
    assert event.tournament["name"] == "Test Tournament"
    assert event.home_team.name == "Home Team"
    assert event.away_team.name == "Away Team"
    assert event.start_timestamp == 1650000000
    
    # Test with nested dict for teams
    event_data_nested = {
        "id": 1002,
        "slug": "team1-vs-team2",
        "tournament": {"id": 6, "name": "Another Tournament"},
        "home_team": {"id": 3, "name": "Team 1"},
        "away_team": {"id": 4, "name": "Team 2"},
        "start_timestamp": 1650010000
    }
    
    event_nested = Event.model_validate(event_data_nested)
    assert event_nested.id == 1002
    assert event_nested.home_team.name == "Team 1"
    assert event_nested.away_team.name == "Team 2"
    
    # Test with missing required fields
    with pytest.raises(Exception):
        Event.model_validate({
            "id": 1003,
            "slug": "incomplete",
            # Missing tournament, teams, and timestamp
        })
    
    # Test with invalid types
    with pytest.raises(Exception):
        Event.model_validate({
            "id": "not-an-int",
            "slug": "invalid-id",
            "tournament": {"id": 5, "name": "Test Tournament"},
            "home_team": home_team,
            "away_team": away_team,
            "start_timestamp": 1650000000
        })