#!/usr/bin/env python3
"""
SofaScore CLI
A command-line interface for interacting with the SofaScore API.
"""
import sys
import os
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Import the SofaScore adapter
from src.adapter.sofascore import (
    list_events_for_day, 
    list_live_events, 
    fetch_event, 
    fetch_event_stats
)

def cmd_live(args):
    """Display live events."""
    print("Fetching live events...")
    events = list_live_events()
    
    if not events:
        print("No live events found.")
        return
    
    print(f"Found {len(events)} live events:\n")
    for i, event in enumerate(events, 1):
        print(f"{i}. {event.home_team.name} vs {event.away_team.name}")
        print(f"   ID: {event.id}")
        print(f"   Tournament: {event.tournament.get('name', 'Unknown')}")
        print(f"   Start time: {datetime.fromtimestamp(event.start_timestamp).strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # Optionally fetch statistics for a selected event
    if args.stats:
        while True:
            try:
                selection = input("Enter event number to view statistics (or press Enter to exit): ")
                if not selection:
                    break
                
                event_index = int(selection) - 1
                if 0 <= event_index < len(events):
                    event_id = events[event_index].id
                    cmd_stats(argparse.Namespace(id=event_id))
                    break
                else:
                    print("Invalid selection. Please enter a valid event number.")
            except ValueError:
                print("Please enter a number.")


def cmd_day(args):
    """Display events for a specific day."""
    try:
        target_date = date.fromisoformat(args.date)
    except ValueError:
        print(f"Invalid date format: {args.date}. Please use YYYY-MM-DD format.")
        return
    
    print(f"Fetching events for {target_date.isoformat()}...")
    events = list_events_for_day(target_date)
    
    if not events:
        print(f"No events found for {target_date.isoformat()}.")
        return
    
    print(f"Found {len(events)} events for {target_date.isoformat()}:\n")
    
    # Group events by tournament
    events_by_tournament = {}
    for event in events:
        tournament_name = event.tournament.get('name', 'Unknown')
        if tournament_name not in events_by_tournament:
            events_by_tournament[tournament_name] = []
        events_by_tournament[tournament_name].append(event)
    
    # Display events by tournament
    for tournament, tournament_events in events_by_tournament.items():
        print(f"\n== {tournament} ({len(tournament_events)} events) ==")
        
        for i, event in enumerate(tournament_events, 1):
            start_time = datetime.fromtimestamp(event.start_timestamp).strftime('%H:%M')
            print(f"{i}. {start_time} - {event.home_team.name} vs {event.away_team.name} (ID: {event.id})")


def cmd_event(args):
    """Display details for a specific event."""
    print(f"Fetching details for event {args.id}...")
    
    try:
        event_data = fetch_event(args.id)
        
        if not event_data or 'event' not in event_data:
            print(f"Could not fetch details for event {args.id}")
            return
        
        event = event_data['event']
        home_team = event.get('homeTeam', {}).get('name', 'Unknown')
        away_team = event.get('awayTeam', {}).get('name', 'Unknown')
        
        print(f"\nEvent: {home_team} vs {away_team}")
        
        # Show status
        if 'status' in event:
            print(f"Status: {event['status'].get('description', 'Unknown')}")
        
        # Show score if available
        if 'homeScore' in event and 'awayScore' in event:
            home_score = event['homeScore'].get('current', 0)
            away_score = event['awayScore'].get('current', 0)
            print(f"Score: {home_score} - {away_score}")
        
        # Show tournament
        if 'tournament' in event:
            tournament = event['tournament'].get('name', 'Unknown')
            category = event['tournament'].get('category', {}).get('name', '')
            print(f"Tournament: {tournament} ({category})")
        
        # Show venue if available
        if 'venue' in event:
            venue = event['venue'].get('name', 'Unknown')
            city = event['venue'].get('city', {}).get('name', '')
            print(f"Venue: {venue}, {city}")
        
        # Show time
        if 'startTimestamp' in event:
            start_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%Y-%m-%d %H:%M')
            print(f"Start time: {start_time}")
        
    except Exception as e:
        print(f"Error fetching event: {e}")


def cmd_stats(args):
    """Display statistics for a specific event."""
    print(f"Fetching statistics for event {args.id}...")
    
    try:
        # Get basic event info first for context
        try:
            event_data = fetch_event(args.id)
            if event_data and 'event' in event_data:
                event = event_data['event']
                home_team = event.get('homeTeam', {}).get('name', 'Home')
                away_team = event.get('awayTeam', {}).get('name', 'Away')
                print(f"\nStatistics for: {home_team} vs {away_team}")
        except:
            print(f"\nStatistics for event {args.id}:")
        
        # Get statistics
        stats_data = fetch_event_stats(args.id)
        
        if not stats_data or 'statistics' not in stats_data:
            print("No statistics available for this event.")
            return
        
        # Display statistics
        for group in stats_data['statistics']:
            group_name = group.get('name', 'General')
            print(f"\n=== {group_name} ===")
            
            for stat_group in group.get('groups', []):
                subgroup_name = stat_group.get('groupName', 'Stats')
                print(f"\n{subgroup_name}:")
                
                for stat_item in stat_group.get('statisticsItems', []):
                    stat_name = stat_item.get('name', 'Unknown')
                    home_value = stat_item.get('home', 'N/A')
                    away_value = stat_item.get('away', 'N/A')
                    
                    print(f"  {stat_name}: {home_value} - {away_value}")
                    
    except Exception as e:
        print(f"Error fetching statistics: {e}")


def cmd_next(args):
    """Display upcoming events for the next few days."""
    days = args.days
    print(f"Fetching events for the next {days} days...")
    
    today = date.today()
    for i in range(days):
        target_date = today + timedelta(days=i)
        events = list_events_for_day(target_date)
        
        date_str = target_date.strftime("%A, %B %d, %Y")
        if not events:
            print(f"\n{date_str}: No events scheduled.")
            continue
        
        print(f"\n{date_str}: {len(events)} events scheduled")
        
        # Show first few events as a sample
        sample_size = min(5, len(events))
        for j, event in enumerate(events[:sample_size], 1):
            start_time = datetime.fromtimestamp(event.start_timestamp).strftime('%H:%M')
            print(f"  {j}. {start_time} - {event.home_team.name} vs {event.away_team.name}")
        
        if len(events) > sample_size:
            print(f"  ... and {len(events) - sample_size} more events")


def main():
    parser = argparse.ArgumentParser(description="SofaScore CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Live events command
    live_parser = subparsers.add_parser("live", help="Show live events")
    live_parser.add_argument("--stats", action="store_true", help="Prompt to view statistics for a selected event")
    live_parser.set_defaults(func=cmd_live)
    
    # Events for a day command
    day_parser = subparsers.add_parser("day", help="Show events for a specific day")
    day_parser.add_argument("date", help="Date in ISO format (YYYY-MM-DD)")
    day_parser.set_defaults(func=cmd_day)
    
    # Today's events shortcut
    today_parser = subparsers.add_parser("today", help="Show events for today")
    today_parser.set_defaults(func=lambda args: cmd_day(argparse.Namespace(date=date.today().isoformat())))
    
    # Tomorrow's events shortcut
    tomorrow_parser = subparsers.add_parser("tomorrow", help="Show events for tomorrow")
    tomorrow_parser.set_defaults(func=lambda args: cmd_day(argparse.Namespace(date=(date.today() + timedelta(days=1)).isoformat())))
    
    # Event details command
    event_parser = subparsers.add_parser("event", help="Show details for a specific event")
    event_parser.add_argument("id", type=int, help="Event ID")
    event_parser.set_defaults(func=cmd_event)
    
    # Event statistics command
    stats_parser = subparsers.add_parser("stats", help="Show statistics for a specific event")
    stats_parser.add_argument("id", type=int, help="Event ID")
    stats_parser.set_defaults(func=cmd_stats)
    
    # Next days events command
    next_parser = subparsers.add_parser("next", help="Show events for the next few days")
    next_parser.add_argument("--days", type=int, default=3, help="Number of days to look ahead")
    next_parser.set_defaults(func=cmd_next)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())