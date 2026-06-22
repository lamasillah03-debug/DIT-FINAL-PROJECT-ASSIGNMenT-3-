"""
Input validation utilities
Provides validation functions for emails, passwords, phone numbers, etc.
"""
import re
from config.settings import VALIDATION


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = VALIDATION['email_regex']
    return re.match(pattern, email) is not None


def validate_password(password: str) -> dict:
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
    
    Returns:
        dict: Validation result with message
    """
    result = {
        'valid': True,
        'errors': []
    }
    
    min_length = VALIDATION['password_min_length']
    
    if len(password) < min_length:
        result['errors'].append(
            f'Password must be at least {min_length} characters long'
        )
        result['valid'] = False
    
    if not re.search(r'[A-Z]', password):
        result['errors'].append('Password must contain at least one uppercase letter')
        result['valid'] = False
    
    if not re.search(r'[a-z]', password):
        result['errors'].append('Password must contain at least one lowercase letter')
        result['valid'] = False
    
    if not re.search(r'[0-9]', password):
        result['errors'].append('Password must contain at least one number')
        result['valid'] = False
    
    return result


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if phone is valid, False otherwise
    """
    # Remove common separators
    clean_phone = re.sub(r'[\s\-\(\)\.]+', '', phone)
    pattern = VALIDATION['phone_regex']
    return re.match(pattern, clean_phone) is not None


def validate_name(name: str) -> bool:
    """
    Validate person name (at least 2 characters, letters and spaces)
    
    Args:
        name (str): Name to validate
    
    Returns:
        bool: True if name is valid, False otherwise
    """
    if len(name.strip()) < 2:
        return False
    # Name should contain letters and spaces only
    return bool(re.match(r"^[a-zA-Z\s]+$", name))


def validate_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
    """
    Validate date format
    
    Args:
        date_str (str): Date string to validate
        format (str): Expected date format
    
    Returns:
        bool: True if date is valid, False otherwise
    """
    from datetime import datetime
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def validate_student_id(student_id: str) -> bool:
    """
    Validate student ID format (STU followed by 6 digits)
    
    Args:
        student_id (str): Student ID to validate
    
    Returns:
        bool: True if student ID is valid, False otherwise
    """
    pattern = VALIDATION['student_id_regex']
    return re.match(pattern, student_id) is not None


def is_empty(value):
    """
    Check if value is empty
    
    Args:
        value: Value to check
    
    Returns:
        bool: True if empty, False otherwise
    """
    if value is None:
        return True
    if isinstance(value, str):
        return len(value.strip()) == 0
    return False
