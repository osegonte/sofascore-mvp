#!/usr/bin/env python3
"""
Main entry point for the SofaScore CLI application.
Provides a unified interface to both CLI implementations.
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path to ensure imports work correctly
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def main():
    """Main entry point."""
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        print("SofaScore CLI - a command-line tool for SofaScore data")
        print("\nUsage:")
        print("  sofascore COMMAND [OPTIONS]")
        print("\nAvailable commands:")
        print("  live      - Show currently live events")
        print("  today     - Show events for today")
        print("  stats ID  - Show statistics for event with given ID")
        print("  help      - Show this help message")
        print("\nFor advanced usage:")
        print("  python -m src.cli.sofascore_cli --help")
        return 0
    
    # Check for help command
    command = sys.argv[1]
    if command in ["help", "--help", "-h"]:
        # Use the help from the Click-based CLI
        from src.cli.commands import cli
        cli(["--help"])
        return 0
    
    # Otherwise, use the Click-based CLI (our primary interface)
    from src.cli.commands import cli
    return cli(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())