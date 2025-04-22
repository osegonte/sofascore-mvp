#!/usr/bin/env python3
"""
SofaScore Data Visualizer.
Visualize sports data from SofaScore API.
"""
import sys
import os
from pathlib import Path
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.services.events import EventService
from src.services.stats import StatsService

def visualize_events_by_tournament(day: date = None):
    """Create a pie chart of events by tournament for a specific day."""
    if day is None:
        day = date.today()
    
    events = EventService.get_events_for_day(day)
    
    if not events:
        print(f"No events found for {day.isoformat()}.")
        return
    
    # Group events by tournament
    tournaments = {}
    for event in events:
        tournament_name = event.tournament.get('name', 'Unknown')
        tournaments[tournament_name] = tournaments.get(tournament_name, 0) + 1
    
    # Sort by event count
    sorted_tournaments = sorted(tournaments.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 10 tournaments and group the rest
    if len(sorted_tournaments) > 10:
        top_tournaments = sorted_tournaments[:9]
        others_count = sum(count for _, count in sorted_tournaments[9:])
        top_tournaments.append(('Others', others_count))
        sorted_tournaments = top_tournaments
    
    # Prepare data for visualization
    labels = [t[0] for t in sorted_tournaments]
    sizes = [t[1] for t in sorted_tournaments]
    
    # Create pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f'Events by Tournament - {day.isoformat()}')
    
    # Save the chart
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f'events_by_tournament_{day.isoformat()}.png'
    plt.savefig(output_path)
    
    print(f"Chart saved to {output_path}")
    plt.close()

def visualize_event_statistics(event_id: int):
    """Create a bar chart for selected statistics of an event."""
    stats_data = StatsService.get_event_statistics(event_id)
    
    if not stats_data or 'statistics' not in stats_data:
        print("No statistics available for this event.")
        return
    
    # Find the event data to get team names
    try:
        event_data = fetch_event(event_id)
        if event_data and 'event' in event_data:
            event = event_data['event']
            home_team = event.get('homeTeam', {}).get('name', 'Home')
            away_team = event.get('awayTeam', {}).get('name', 'Away')
        else:
            home_team, away_team = 'Home', 'Away'
    except:
        home_team, away_team = 'Home', 'Away'
    
    # Find the statistics we want to visualize (e.g., shots, possession, etc.)
    stats_to_visualize = {}
    
    for group in stats_data['statistics']:
        for stat_group in group.get('groups', []):
            for stat_item in stat_group.get('statisticsItems', []):
                stat_name = stat_item.get('name')
                
                # Filter for numeric statistics that we can visualize
                if stat_name in ['Ball Possession', 'Total Shots', 'Shots on Goal', 
                               'Corner Kicks', 'Fouls', 'Yellow Cards']:
                    home_value = stat_item.get('home', '0')
                    away_value = stat_item.get('away', '0')
                    
                    # Clean up percentage signs and convert to float
                    if isinstance(home_value, str) and '%' in home_value:
                        home_value = float(home_value.strip('%'))
                    if isinstance(away_value, str) and '%' in away_value:
                        away_value = float(away_value.strip('%'))
                    
                    try:
                        stats_to_visualize[stat_name] = {
                            'home': float(home_value),
                            'away': float(away_value)
                        }
                    except (ValueError, TypeError):
                        pass  # Skip if conversion fails
    
    if not stats_to_visualize:
        print("No suitable statistics found for visualization.")
        return
    
    # Prepare data for the bar chart
    labels = list(stats_to_visualize.keys())
    home_values = [stats_to_visualize[label]['home'] for label in labels]
    away_values = [stats_to_visualize[label]['away'] for label in labels]
    
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    
    fig, ax = plt.subplots(figsize=(12, 8))
    rects1 = ax.bar(x - width/2, home_values, width, label=home_team)
    rects2 = ax.bar(x + width/2, away_values, width, label=away_team)
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Values')
    ax.set_title(f'Match Statistics: {home_team} vs {away_team}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    # Attach a text label above each bar
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    
    # Save the chart
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f'event_stats_{event_id}.png'
    plt.savefig(output_path)
    
    print(f"Chart saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        if sys.argv[1] == 'tournament':
            target_date = date.today()
            if len(sys.argv) > 2:
                try:
                    target_date = date.fromisoformat(sys.argv[2])
                except ValueError:
                    print(f"Invalid date format. Using today's date.")
            visualize_events_by_tournament(target_date)
        
        elif sys.argv[1] == 'stats' and len(sys.argv) > 2:
            try:
                event_id = int(sys.argv[2])
                visualize_event_statistics(event_id)
            except ValueError:
                print("Please provide a valid event ID.")
    else:
        print("Usage:")
        print("  python visualizer.py tournament [YYYY-MM-DD]")
        print("  python visualizer.py stats EVENT_ID")