import re
from src.models import User, db

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength (min 8 chars, at least one uppercase, lowercase, digit)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"

def validate_username(username):
    """Validate username format (3-20 chars, alphanumeric and underscore)"""
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    if User.query.filter_by(username=username).first():
        return False, "Username already exists"
    return True, "Username is valid"

def validate_name(name, field_name):
    """Validate name field"""
    if not name or len(name) < 2:
        return False, f"{field_name} must be at least 2 characters long"
    if not re.match(r'^[a-zA-Z\s\'-]+$', name):
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"
    return True, f"{field_name} is valid"
