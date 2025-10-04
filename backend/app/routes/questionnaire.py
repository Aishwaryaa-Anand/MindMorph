from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.services.questionnaire_service import QuestionnaireService
from app.services.mbti_service import MBTIService

bp = Blueprint('questionnaire', __name__, url_prefix='/api/questionnaire')

# Initialize services
questionnaire_service = QuestionnaireService(db)
mbti_service = MBTIService()

@bp.route('/questions', methods=['GET'])
@jwt_required()
def get_questions():
    """Get all questionnaire questions"""
    try:
        questions = questionnaire_service.get_questions()
        return jsonify({'questions': questions}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to load questions: {str(e)}'}), 500

@bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """
    Calculate MBTI type from answers
    
    Expected JSON:
    {
        "answers": [
            {"questionId": 1, "choice": "A"},
            {"questionId": 2, "choice": "B"},
            ...
        ]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        answers = data.get('answers', [])
        
        # Validate answers
        if not answers or len(answers) != 20:
            return jsonify({'error': 'All 20 questions must be answered'}), 400
        
        # Calculate MBTI type
        mbti_type, confidence = questionnaire_service.calculate_mbti(answers)
        
        # Save prediction
        prediction_id, error = questionnaire_service.save_prediction(
            user_id, mbti_type, confidence, answers
        )
        
        if error:
            return jsonify({'error': error}), 500
        
        # Get insights
        insights = mbti_service.get_insights(mbti_type)
        
        return jsonify({
            'predictionId': prediction_id,
            'mbtiType': mbti_type,
            'confidence': confidence,
            'insights': insights
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@bp.route('/results', methods=['GET'])
@jwt_required()
def get_results():
    """Get user's latest questionnaire result"""
    try:
        user_id = get_jwt_identity()
        
        # Get latest prediction
        prediction = questionnaire_service.get_latest_prediction(user_id)
        
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

@bp.route('/result/:id', methods=['GET'])
@jwt_required()
def get_result_by_id(id):
    """Get specific result by ID"""
    try:
        user_id = get_jwt_identity()
        
        prediction = questionnaire_service.get_prediction_by_id(id, user_id)
        
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
    """Get all user's questionnaire results"""
    try:
        user_id = get_jwt_identity()
        predictions = questionnaire_service.get_user_predictions(user_id)
        
        return jsonify({'predictions': predictions}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load history: {str(e)}'}), 500

@bp.route('/insights/:mbti_type', methods=['GET'])
def get_insights(mbti_type):
    """Get insights for any MBTI type (public endpoint)"""
    try:
        insights = mbti_service.get_insights(mbti_type)
        
        if not insights:
            return jsonify({'error': 'Invalid MBTI type'}), 404
        
        return jsonify({'insights': insights}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load insights: {str(e)}'}), 500