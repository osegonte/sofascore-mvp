"""
Cache utility for SofaScore CLI.
Provides a simple file-based cache to reduce API calls.
"""
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from functools import wraps

from src.core.config import config
from src.core.logging import get_logger

# Setup logger
logger = get_logger("cache")

class Cache:
    """Simple file-based cache implementation."""
    
    def __init__(self, cache_dir: Optional[str] = None, enabled: bool = None):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory for cache files (default from config)
            enabled: Whether cache is enabled (default from config)
        """
        self.cache_dir = Path(cache_dir or config.CACHE_DIR)
        self.enabled = enabled if enabled is not None else config.CACHE_ENABLED
        
        # Create cache directory if it doesn't exist and caching is enabled
        if self.enabled and not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created cache directory: {self.cache_dir}")
    
    def _get_cache_path(self, key: str) -> Path:
        """
        Get the file path for a cache key.
        
        Args:
            key: Cache key
            
        Returns:
            Path to the cache file
        """
        # Hash the key to ensure valid filename
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"
    
    def get(self, key: str, max_age: int = 3600) -> Optional[Dict[str, Any]]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            max_age: Maximum age in seconds (default: 1 hour)
            
        Returns:
            Cached value or None if not found or expired
        """
        if not self.enabled:
            return None
            
        cache_path = self._get_cache_path(key)
        
        # Check if cache file exists
        if not cache_path.exists():
            return None
            
        # Check if cache is expired
        if time.time() - cache_path.stat().st_mtime > max_age:
            logger.debug(f"Cache expired for key: {key}")
            return None
            
        # Read and return cache
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read cache for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Dict[str, Any]) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
            
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(value, f)
            return True
        except IOError as e:
            logger.warning(f"Failed to write cache for key {key}: {e}")
            return False

# Create global cache instance
cache = Cache()

def cached(max_age: int = 3600):
    """
    Decorator for caching function results.
    
    Args:
        max_age: Maximum age of cache in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Check cache
            cached_result = cache.get(cache_key, max_age)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
                
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
            
        return wrapper
    return decorator