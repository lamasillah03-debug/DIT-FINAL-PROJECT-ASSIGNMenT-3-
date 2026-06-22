"""
Utility functions for common operations
"""
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


def format_date(date_obj, format: str = '%Y-%m-%d') -> str:
    """
    Format date object to string
    
    Args:
        date_obj: Date object to format
        format (str): Format string
    
    Returns:
        str: Formatted date string
    """
    try:
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime(format)
    except Exception as e:
        logger.error(f"Date formatting error: {str(e)}")
        return str(date_obj)


def parse_date(date_str: str, format: str = '%Y-%m-%d') -> datetime:
    """
    Parse date string to datetime object
    
    Args:
        date_str (str): Date string to parse
        format (str): Date format
    
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(date_str, format)
    except Exception as e:
        logger.error(f"Date parsing error: {str(e)}")
        return None


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
    
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_phone(phone: str) -> str:
    """
    Format phone number for display
    
    Args:
        phone (str): Phone number
    
    Returns:
        str: Formatted phone number
    """
    # Remove all non-digits
    digits = ''.join(c for c in phone if c.isdigit())
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return phone


def get_file_extension(filename: str) -> str:
    """
    Get file extension
    
    Args:
        filename (str): Filename
    
    Returns:
        str: File extension
    """
    return filename.split('.')[-1].lower() if '.' in filename else ''


def generate_student_id() -> str:
    """
    Generate a unique student ID
    Format: STU + 6 digit number
    
    Returns:
        str: Generated student ID
    """
    from random import randint
    random_number = randint(100000, 999999)
    return f"STU{random_number}"
