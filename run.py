#!/usr/bin/env python3
"""
Direct entry point for SofaScore CLI.
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Directly run the CLI
if __name__ == "__main__":
    from cli.commands import cli
    cli()