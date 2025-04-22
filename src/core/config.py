import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[2] / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# API Configuration
API_BASE = os.getenv("SOFASCORE_API_BASE", "https://api.sofascore.com/api/v1")
API_TIMEOUT = int(os.getenv("SOFASCORE_API_TIMEOUT", "10"))