#!/usr/bin/env python3
"""
Entry point wrapper for SofaScore CLI.
"""
import sys
import os
from pathlib import Path

def main():
    """Wrapper for the actual CLI that ensures correct import paths."""
    # Explicitly add the project root to the Python path
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Now we can safely import the CLI
    from src.cli.commands import cli
    return cli()

if __name__ == "__main__":
    sys.exit(main())