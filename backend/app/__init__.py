from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize extensions
jwt = JWTManager()
mongo_client = None
db = None

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Initialize MongoDB
    global mongo_client, db
    mongo_uri = os.getenv('MONGO_URI')
    
    if not mongo_uri:
        raise ValueError("❌ MONGO_URI not found in .env file!")
    
    try:
        mongo_client = MongoClient(mongo_uri)
        db = mongo_client['mindmorph']
        
        # Test connection
        mongo_client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        
        # Create indexes
        db.users.create_index('email', unique=True)
        db.questionnaire_predictions.create_index('userId')
        db.text_predictions.create_index('userId')
        db.twitter_predictions.create_index('userId')
        db.cached_tweets.create_index('twitterHandle', unique=True)
        db.cached_tweets.create_index('expiresAt', expireAfterSeconds=0)
        
        print("✅ Database indexes created!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        raise
    
    # Register blueprints (routes)
    from app.routes import auth, questionnaire
    app.register_blueprint(auth.bp)
    app.register_blueprint(questionnaire.bp)
    
    # Root route
    @app.route('/')
    def home():
        return {
            'message': 'Welcome to MindMorph API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    # Health check route
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'database': 'connected'}
    
    return app