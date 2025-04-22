import logging
import sys
import os
from pathlib import Path

def setup_logger(name: str = "sofascore", level: int = None) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Logger name
        level: Logging level (defaults to INFO or value from SOFASCORE_LOG_LEVEL env var)
    
    Returns:
        Configured logger
    """
    # Determine log level from environment or use INFO as default
    if level is None:
        level_name = os.environ.get("SOFASCORE_LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
    
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Only configure if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        
        # Determine if we should log to file
        log_file = os.environ.get("SOFASCORE_LOG_FILE")
        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            
            # Add file handler to logger
            logger.addHandler(file_handler)
    
    return logger

# Create default logger
logger = setup_logger()

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a configured logger.
    
    Args:
        name: Optional name suffix for the logger
    
    Returns:
        Configured logger
    """
    if name:
        return setup_logger(f"sofascore.{name}")
    return logger