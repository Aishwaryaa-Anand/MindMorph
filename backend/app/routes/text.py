from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services.text_service import TextService
from app.services.mbti_service import MBTIService

bp = Blueprint('text', __name__, url_prefix='/api/text')

# Initialize services
text_service = TextService(db)
mbti_service = MBTIService()

@bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """
    Predict MBTI from text
    
    Expected JSON:
    {
        "text": "Your text here..."
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Predict
        result, error = text_service.predict(text, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get insights
        insights = mbti_service.get_insights(result['mbtiType'])
        
        return jsonify({
            **result,
            'insights': insights
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@bp.route('/results', methods=['GET'])
@jwt_required()
def get_results():
    """Get user's latest text prediction"""
    try:
        user_id = get_jwt_identity()
        
        prediction = text_service.get_latest_prediction(user_id)
        
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
        
        prediction = text_service.get_prediction_by_id(id, user_id)
        
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
    """Get all user's text predictions"""
    try:
        user_id = get_jwt_identity()
        predictions = text_service.get_user_predictions(user_id)
        
        return jsonify({'predictions': predictions}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load history: {str(e)}'}), 500