import click
from datetime import date
from src.services.events import EventService
from src.services.stats import StatsService

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
        click.echo(f"{event.home_team.name} vs {event.away_team.name}")

if __name__ == '__main__':
    cli()