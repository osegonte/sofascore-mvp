#!/usr/bin/env python3
"""
SofaScore adapter module.
Provides functions to fetch events and statistics from the SofaScore API.
"""
import sys
from pathlib import Path
from datetime import date
from typing import List, Dict, Any

# Ensure that the project root (src/) is on sys.path for local imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

import httpx
from httpx import RequestError, HTTPStatusError
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_fixed,
    stop_after_attempt,
)
from .models import Event, Team  # Use relative import

# Import configuration
from src.core.config import config
from src.core.logging import get_logger

# Setup logger
logger = get_logger("adapter")

# Base URL and headers for SofaScore API
API_BASE = config.API_BASE
API_TIMEOUT = config.API_TIMEOUT
API_RETRIES = config.API_RETRIES
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

@retry(
    retry=retry_if_exception_type(RequestError),
    wait=wait_fixed(1),
    stop=stop_after_attempt(API_RETRIES)
)
def _get(path: str) -> Dict[str, Any]:
    """
    Internal helper to perform GET requests against SofaScore API.
    Retries only on network errors (RequestError), not on HTTPStatusError.
    """
    url = f"{API_BASE}{path}"
    logger.debug(f"Making GET request to {url}")
    
    response = httpx.get(url, timeout=API_TIMEOUT, headers=HEADERS)
    response.raise_for_status()
    
    return response.json()


def _to_event(item: Dict[str, Any]) -> Event:
    """
    Convert API response to Event model.
    Properly handles nested Team objects.
    """
    # Create Team objects directly from the API response
    home_team = Team.model_validate(item.get("homeTeam", {}))
    away_team = Team.model_validate(item.get("awayTeam", {}))
    
    return Event.model_validate({
        "id": item.get("id"),
        "slug": item.get("slug"),
        "tournament": item.get("tournament"),
        "home_team": home_team,  # Pass the Team object, not just the name
        "away_team": away_team,  # Pass the Team object, not just the name
        "start_timestamp": item.get("startTimestamp"),
    })


from src.utils.cache import cached

@cached(max_age=3600)  # Cache for 1 hour
def list_events_for_day(day: date, sport: str = config.DEFAULT_SPORT) -> List[Event]:
    """
    List all events scheduled for a given day.
    Returns an empty list if the endpoint returns 404 or on other HTTP errors.
    
    Args:
        day: Date to fetch events for
        sport: Sport type (default from config)
        
    Returns:
        List of Event objects
    """
    path = f"/sport/{sport}/events/date/{day.isoformat()}"
    try:
        data = _get(path)
    except HTTPStatusError as e:
        # 404 or other HTTP errors: no events or bad request
        logger.warning(f"Could not fetch events for {day} (status {e.response.status_code}); returning empty list.")
        return []
    except RequestError as e:
        logger.error(f"Network error when fetching events for {day}: {e}.")
        return []

    raw = data.get("events") or data.get("eventList") or []
    return [_to_event(item) for item in raw]


@cached(max_age=60)  # Cache for 1 minute since this is live data
def list_live_events(sport: str = config.DEFAULT_SPORT) -> List[Event]:
    """
    Fetch all currently live events for the given sport.
    
    Args:
        sport: Sport type (default from config)
        
    Returns:
        List of Event objects
    """
    path = f"/sport/{sport}/events/live"
    try:
        data = _get(path)
    except (HTTPStatusError, RequestError) as e:
        logger.warning(f"Could not fetch live events (error: {e}); returning empty list.")
        return []
    
    raw = data.get("events", [])
    return [_to_event(item) for item in raw]


@cached(max_age=600)  # Cache for 10 minutes
def fetch_event(event_id: int) -> Dict[str, Any]:
    """
    Fetch detailed data for a single event.
    
    Args:
        event_id: ID of the event to fetch
        
    Returns:
        Dictionary with event data
    """
    return _get(f"/event/{event_id}")


@cached(max_age=300)  # Cache for 5 minutes
def fetch_event_stats(event_id: int) -> Dict[str, Any]:
    """
    Fetch statistical data for a single event.
    
    Args:
        event_id: ID of the event to fetch statistics for
        
    Returns:
        Dictionary with statistics data
    """
    return _get(f"/event/{event_id}/statistics")


if __name__ == "__main__":
    # Quick smoke tests via CLI
    print("Listing today's football events...")
    today = date.today()
    events = list_events_for_day(today)
    print(f"  → Found {len(events)} events; IDs: {[e.id for e in events[:5]]}")

    print("\nListing live football events...")
    live = list_live_events()
    print(f"  → Found {len(live)} live events; IDs: {[e.id for e in live[:5]]}")

    if live:
        eid = live[0].id
        print(f"\nFetching stats for event {eid}...")
        stats = fetch_event_stats(eid)
        groups = stats.get("statistics", [])
        print("  → Raw statistics keys:", [g.get("name") for g in groups])