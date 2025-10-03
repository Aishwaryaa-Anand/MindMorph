from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    """User model for authentication"""
    
    def __init__(self, email, password, name, google_id=None):
        self.email = email.lower().strip()
        self.password = self.hash_password(password) if password else None
        self.name = name.strip()
        self.google_id = google_id
        self.created_at = datetime.utcnow()
        self.last_login = datetime.utcnow()
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def to_dict(self):
        """Convert user to dictionary for MongoDB"""
        return {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'google_id': self.google_id,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @staticmethod
    def from_dict(data):
        """Create User object from MongoDB document"""
        user = User.__new__(User)
        user.email = data.get('email', '')
        user.password = data.get('password')
        user.name = data.get('name', '')
        user.google_id = data.get('google_id')
        user.created_at = data.get('created_at', datetime.utcnow())
        user.last_login = data.get('last_login', datetime.utcnow())
        return user
    
    @staticmethod
    def sanitize_user(user_data):
        """Remove sensitive data before sending to client"""
        return {
            'id': str(user_data['_id']),
            'email': user_data['email'],
            'name': user_data['name']
        }