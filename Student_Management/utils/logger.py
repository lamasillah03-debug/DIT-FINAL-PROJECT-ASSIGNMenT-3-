"""
Logging utilities
Provides consistent logging configuration
"""
import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)


def get_logger(name):
    """
    Get logger instance
    
    Args:
        name (str): Logger name (usually __name__)
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
