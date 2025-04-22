#!/usr/bin/env python3
"""
SofaScore Data Explorer Tool.
Interactive tool to explore and visualize SofaScore data.
"""
import sys
import json
from pathlib import Path
from datetime import date, datetime

# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.services.events import EventService
from src.services.stats import StatsService

def explore_live_events():
    """Explore currently live events."""
    print("Fetching live events...")
    events = EventService.get_live_events()
    
    if not events:
        print("No live events found.")
        return
    
    print(f"Found {len(events)} live events:")
    for i, event in enumerate(events, 1):
        print(f"{i}. {event.home_team.name} vs {event.away_team.name}")

if __name__ == "__main__":
    explore_live_events()