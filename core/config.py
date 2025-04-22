"""
Configuration module for SofaScore CLI.
Handles loading environment variables and providing configuration values.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[2] / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Config:
    """Configuration class that provides access to all application settings."""
    
    # API Configuration
    API_BASE: str = os.getenv("SOFASCORE_API_BASE", "https://api.sofascore.com/api/v1")
    API_TIMEOUT: int = int(os.getenv("SOFASCORE_API_TIMEOUT", "10"))
    API_RETRIES: int = int(os.getenv("SOFASCORE_API_RETRIES", "3"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("SOFASCORE_LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("SOFASCORE_LOG_FILE", "")
    
    # Application Settings
    DEFAULT_SPORT: str = os.getenv("SOFASCORE_DEFAULT_SPORT", "football")
    CACHE_ENABLED: bool = os.getenv("SOFASCORE_CACHE_ENABLED", "True").lower() in ('true', '1', 'yes')
    CACHE_DIR: str = os.getenv("SOFASCORE_CACHE_DIR", str(Path.home() / ".sofascore" / "cache"))
    
    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Return all configuration values as a dictionary."""
        return {key: value for key, value in cls.__dict__.items() 
                if not key.startswith('_') and not callable(value)}
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value by key name."""
        return getattr(cls, key, default)

# Create a global instance for easy imports
config = Config()