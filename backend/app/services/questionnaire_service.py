from datetime import datetime
from bson import ObjectId
import json
import os
from app.ml_models.questionnaire_enhancer import ml_enhancer

class QuestionnaireService:
    """Service for handling questionnaire predictions"""
    
    def __init__(self, db):
        self.db = db
        self.predictions_collection = db.questionnaire_predictions
        
        # Load questions
        questions_path = os.path.join(os.path.dirname(__file__), '../../data/questions.json')
        with open(questions_path, 'r') as f:
            self.questions = json.load(f)
    
    def get_questions(self):
        """Return all questions"""
        return self.questions
    
    def calculate_mbti(self, answers):
        """
        Calculate MBTI type from answers using weighted scoring
        
        Args:
            answers: List of dicts with {questionId, choice}
        
        Returns:
            tuple: (mbti_type, confidence_scores)
        """
        # Initialize scores
        scores = {
            'I': 0, 'E': 0,
            'N': 0, 'S': 0,
            'T': 0, 'F': 0,
            'J': 0, 'P': 0
        }
        
        # Create question lookup
        questions_dict = {q['id']: q for q in self.questions}
        
        # Calculate scores
        for answer in answers:
            question_id = answer['questionId']
            chosen_label = answer['choice']
            
            question = questions_dict.get(question_id)
            if not question:
                continue
            
            # Find the chosen choice
            for choice in question['choices']:
                if choice['label'] == chosen_label:
                    scores[choice['value']] += choice['weight']
                    break
        
        # Determine MBTI type and calculate confidence
        mbti_type = ''
        confidence = {}
        
        dimensions = [
            ('I', 'E', 'IE'),
            ('S', 'N', 'NS'),
            ('T', 'F', 'TF'),
            ('J', 'P', 'JP')
        ]
        
        for letter1, letter2, dim_name in dimensions:
            total = scores[letter1] + scores[letter2]
            
            if total == 0:
                # Default if no answers for this dimension
                chosen_letter = letter1
                conf = 0.5
            else:
                if scores[letter1] > scores[letter2]:
                    chosen_letter = letter1
                    conf = scores[letter1] / total
                else:
                    chosen_letter = letter2
                    conf = scores[letter2] / total
            
            mbti_type += chosen_letter
            confidence[dim_name] = round(conf, 2)
        
        return mbti_type, confidence
    
    def save_prediction(self, user_id, mbti_type, confidence, answers):
        """Save prediction to database with ML enhancement"""
        try:
            # Enhance confidence with ML
            enhanced_confidence = ml_enhancer.enhance_confidence(
                answers, mbti_type, confidence
            )
            
            prediction = {
                'userId': ObjectId(user_id),
                'mbtiType': mbti_type,
                'confidence': enhanced_confidence,
                'base_confidence': confidence,  # Store original for comparison
                'answers': answers,
                'timestamp': datetime.utcnow(),
                'ml_enhanced': True
            }
            
            result = self.predictions_collection.insert_one(prediction)
            
            return str(result.inserted_id), None
        except Exception as e:
            return None, f'Failed to save prediction: {str(e)}'
    
    def get_user_predictions(self, user_id):
        """Get all predictions for a user"""
        try:
            predictions = list(self.predictions_collection.find(
                {'userId': ObjectId(user_id)}
            ).sort('timestamp', -1))
            
            # Convert ObjectId to string
            for pred in predictions:
                pred['_id'] = str(pred['_id'])
                pred['userId'] = str(pred['userId'])
            
            return predictions
        except Exception as e:
            return []
    
    def get_prediction_by_id(self, prediction_id, user_id):
        """Get specific prediction by ID"""
        try:
            prediction = self.predictions_collection.find_one({
                '_id': ObjectId(prediction_id),
                'userId': ObjectId(user_id)
            })
            
            if prediction:
                prediction['_id'] = str(prediction['_id'])
                prediction['userId'] = str(prediction['userId'])
                return prediction
            
            return None
        except Exception:
            return None
    
    def get_latest_prediction(self, user_id):
        """Get user's most recent prediction"""
        try:
            prediction = self.predictions_collection.find_one(
                {'userId': ObjectId(user_id)},
                sort=[('timestamp', -1)]
            )
            
            if prediction:
                prediction['_id'] = str(prediction['_id'])
                prediction['userId'] = str(prediction['userId'])
                return prediction
            
            return None
        except Exception:
            return None