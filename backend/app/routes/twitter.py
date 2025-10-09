from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services.twitter_service import TwitterService
from app.services.mbti_service import MBTIService

bp = Blueprint('twitter', __name__, url_prefix='/api/twitter')

# Initialize services
twitter_service = TwitterService(db)
mbti_service = MBTIService()

@bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    """
    Analyze Twitter profile
    
    Expected JSON:
    {
        "username": "elonmusk"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Analyze
        result, error = twitter_service.analyze_twitter(username, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get insights
        insights = mbti_service.get_insights(result['mbtiType'])
        
        return jsonify({
            **result,
            'insights': insights
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@bp.route('/results', methods=['GET'])
@jwt_required()
def get_results():
    """Get user's latest Twitter prediction"""
    try:
        user_id = get_jwt_identity()
        
        prediction = twitter_service.get_latest_prediction(user_id)
        
        if not prediction:
            return jsonify({'message': 'No results found'}), 404
        
        # Get insights
        insights = mbti_service.get_insights(prediction['mbtiType'])
        
        return jsonify({
            'prediction': prediction,
            'insights': insights
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load results: {str(e)}'}), 500

@bp.route('/result/<id>', methods=['GET'])
@jwt_required()
def get_result_by_id(id):
    """Get specific result by ID"""
    try:
        user_id = get_jwt_identity()
        
        prediction = twitter_service.get_prediction_by_id(id, user_id)
        
        if not prediction:
            return jsonify({'error': 'Result not found'}), 404
        
        # Get insights
        insights = mbti_service.get_insights(prediction['mbtiType'])
        
        return jsonify({
            'prediction': prediction,
            'insights': insights
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load result: {str(e)}'}), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Get all user's Twitter predictions"""
    try:
        user_id = get_jwt_identity()
        predictions = twitter_service.get_user_predictions(user_id)
        
        return jsonify({'predictions': predictions}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load history: {str(e)}'}), 500

@bp.route('/available-usernames', methods=['GET'])
def get_available_usernames():
    """Get list of available mock usernames (public endpoint)"""
    try:
        usernames = twitter_service.get_available_usernames()
        return jsonify({'usernames': usernames}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500