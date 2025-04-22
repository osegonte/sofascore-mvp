#!/usr/bin/env python3
# debug_sofascore.py

import sys
import os
from pathlib import Path
import traceback

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print("=== Debug Info ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

try:
    print("\n=== Trying to import modules ===")
    print("Importing click...")
    import click
    print("Importing httpx...")
    import httpx
    print("Importing src.adapter.sofascore...")
    from src.adapter import sofascore
    print("Importing src.cli.commands...")
    from src.cli.commands import cli
    
    print("\n=== Testing API call ===")
    print("Calling list_live_events()...")
    events = sofascore.list_live_events()
    print(f"Result: {events}")
    
    print("\n=== Running CLI command ===")
    print("Command arguments:", sys.argv[1:] if len(sys.argv) > 1 else ["--help"])
    cli(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])
    
except Exception as e:
    print(f"\n=== ERROR ===")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nTraceback:")
    traceback.print_exc()