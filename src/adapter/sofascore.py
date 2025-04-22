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
from adapter.models import Event, Team  # Import Team model as well

# Base URL and headers for SofaScore API
API_BASE = "https://api.sofascore.com/api/v1"
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
    stop=stop_after_attempt(3)
)
def _get(path: str) -> Dict[str, Any]:
    """
    Internal helper to perform GET requests against SofaScore API.
    Retries only on network errors (RequestError), not on HTTPStatusError.
    """
    url = f"{API_BASE}{path}"
    response = httpx.get(url, timeout=10, headers=HEADERS)
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


def list_events_for_day(day: date, sport: str = "football") -> List[Event]:
    """
    List all events scheduled for a given day.
    Returns an empty list if the endpoint returns 404 or on other HTTP errors.
    """
    path = f"/sport/{sport}/events/date/{day.isoformat()}"
    try:
        data = _get(path)
    except HTTPStatusError as e:
        # 404 or other HTTP errors: no events or bad request
        print(f"Warning: could not fetch events for {day} (status {e.response.status_code}); returning empty list.")
        return []
    except RequestError as e:
        print(f"Network error when fetching events for {day}: {e}.")
        return []

    raw = data.get("events") or data.get("eventList") or []
    return [_to_event(item) for item in raw]


def list_live_events(sport: str = "football") -> List[Event]:
    """
    Fetch all currently live events for the given sport.
    """
    path = f"/sport/{sport}/events/live"
    try:
        data = _get(path)
    except (HTTPStatusError, RequestError) as e:
        print(f"Warning: could not fetch live events (error: {e}); returning empty list.")
        return []
    
    raw = data.get("events", [])
    return [_to_event(item) for item in raw]


def fetch_event(event_id: int) -> Dict[str, Any]:
    """
    Fetch detailed data for a single event.
    """
    return _get(f"/event/{event_id}")


def fetch_event_stats(event_id: int) -> Dict[str, Any]:
    """
    Fetch statistical data for a single event.
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