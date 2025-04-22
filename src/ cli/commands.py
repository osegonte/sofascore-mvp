import click
from datetime import date
from src.services.events import EventService
from src.services.stats import StatsService
from src.utils.formatters import format_event_display

@click.group()
def cli():
    """SofaScore CLI for accessing sports data."""
    pass

@cli.command()
def live():
    """Display all currently live events."""
    events = EventService.get_live_events()
    
    if not events:
        click.echo("No live events found.")
        return
    
    click.echo(f"Found {len(events)} live events:")
    for event in events:
        click.echo(format_event_display(event))

@cli.command()
@click.argument('date_str', required=False)
def today(date_str=None):
    """Display all events for today."""
    target_date = date.today()
    events = EventService.get_events_for_day(target_date)
    
    if not events:
        click.echo(f"No events found for {target_date.isoformat()}.")
        return
    
    click.echo(f"Found {len(events)} events for {target_date.isoformat()}:")
    for event in events:
        click.echo(format_event_display(event))

@cli.command()
@click.argument('event_id', type=int)
def stats(event_id):
    """Display statistics for a specific event."""
    stats_data = StatsService.get_event_statistics(event_id)
    
    if not stats_data or 'statistics' not in stats_data:
        click.echo("No statistics available for this event.")
        return
    
    # Display statistics
    for group in stats_data['statistics']:
        group_name = group.get('name', 'General')
        click.echo(f"\n=== {group_name} ===")
        
        for stat_group in group.get('groups', []):
            subgroup_name = stat_group.get('groupName', 'Stats')
            click.echo(f"\n{subgroup_name}:")
            
            for stat_item in stat_group.get('statisticsItems', []):
                stat_name = stat_item.get('name', 'Unknown')
                home_value = stat_item.get('home', 'N/A')
                away_value = stat_item.get('away', 'N/A')
                
                click.echo(f"  {stat_name}: {home_value} - {away_value}")

if __name__ == '__main__':
    cli()