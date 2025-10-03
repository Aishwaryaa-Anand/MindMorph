from datetime import datetime
from bson import ObjectId
from flask_jwt_extended import create_access_token
from app.models.user import User

class AuthService:
    """Service for handling authentication logic"""
    
    def __init__(self, db):
        self.db = db
        self.users_collection = db.users
    
    def signup(self, email, password, name):
        """Register a new user"""
        try:
            email = email.lower().strip()
            
            # Check if user already exists
            existing_user = self.users_collection.find_one({'email': email})
            if existing_user:
                return None, 'Email already registered'
            
            # Create new user
            user = User(email, password, name)
            result = self.users_collection.insert_one(user.to_dict())
            
            # Generate JWT token
            token = create_access_token(identity=str(result.inserted_id))
            
            return {
                'token': token,
                'user': {
                    'id': str(result.inserted_id),
                    'email': email,
                    'name': name
                }
            }, None
            
        except Exception as e:
            return None, f'Signup failed: {str(e)}'
    
    def login(self, email, password):
        """Authenticate user and return token"""
        try:
            email = email.lower().strip()
            
            # Find user by email
            user_data = self.users_collection.find_one({'email': email})
            
            if not user_data:
                return None, 'Invalid email or password'
            
            # Verify password
            if not User.verify_password(password, user_data['password']):
                return None, 'Invalid email or password'
            
            # Update last login
            self.users_collection.update_one(
                {'_id': user_data['_id']},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            
            # Generate JWT token
            token = create_access_token(identity=str(user_data['_id']))
            
            return {
                'token': token,
                'user': User.sanitize_user(user_data)
            }, None
            
        except Exception as e:
            return None, f'Login failed: {str(e)}'
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user_data = self.users_collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User.sanitize_user(user_data)
            return None
        except Exception:
            return None
    
    def verify_token(self, user_id):
        """Verify if user exists (for token validation)"""
        try:
            user_data = self.users_collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return True, User.sanitize_user(user_data)
            return False, None
        except Exception:
            return False, None