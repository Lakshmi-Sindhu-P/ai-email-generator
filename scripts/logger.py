"""
Logging configuration for AI Email Generator.
Sets up centralized logging for the entire application.
"""
import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Set up and configure a logger instance.
    
    Args:
        name: Name of the logger (typically __name__ of the calling module)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")
    
    return logger


# Create default logger
logger = setup_logger("ai_email_generator")

