#!/usr/bin/env python3
"""
Entry point script for SofaScore CLI.
This script ensures proper path resolution for the src module.
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

print("Script starting...")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

try:
    print("Importing CLI...")
    from src.cli.commands import cli
    
    def main():
        """Entry point function called by the console script."""
        print("Running CLI command...")
        return cli(standalone_mode=False)
    
    if __name__ == "__main__":
        print("Command line arguments:", sys.argv)
        main()
        print("Command completed.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)