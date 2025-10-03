from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_password, validate_name

# Create blueprint
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize auth service
auth_service = AuthService(db)

@bp.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "John Doe"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        if not email or not password or not name:
            return jsonify({'error': 'All fields are required'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        if not validate_name(name):
            return jsonify({'error': 'Name must be between 1 and 100 characters'}), 400
        
        # Create user
        result, error = auth_service.signup(email, password, name)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate user
        result, error = auth_service.login(email, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    """
    Verify JWT token and return user info
    
    Headers:
    Authorization: Bearer <token>
    """
    try:
        user_id = get_jwt_identity()
        
        is_valid, user = auth_service.verify_token(user_id)
        
        if not is_valid:
            return jsonify({'error': 'Invalid token or user not found'}), 404
        
        return jsonify({
            'valid': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (JWT is stateless, so this is handled on frontend)
    
    Headers:
    Authorization: Bearer <token>
    """
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info
    
    Headers:
    Authorization: Bearer <token>
    """
    try:
        user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user}), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500