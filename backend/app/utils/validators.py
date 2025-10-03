import re

def validate_email(email):
    """Validate email format"""
    if not email or len(email) < 3:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_password(password):
    """
    Validate password strength
    Minimum 8 characters
    """
    if not password:
        return False
    return len(password) >= 8

def validate_name(name):
    """Validate name (not empty, reasonable length)"""
    if not name:
        return False
    name = name.strip()
    return 1 <= len(name) <= 100