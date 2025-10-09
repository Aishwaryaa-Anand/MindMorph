from datetime import datetime
from bson import ObjectId
from app.ml_models.text_classifier import text_classifier

class TextService:
    """Service for text-based MBTI predictions"""
    
    def __init__(self, db):
        self.db = db
        self.predictions_collection = db.text_predictions
    
    def predict(self, text, user_id):
        """Predict MBTI from text"""
        try:
            # Validate text length
            if len(text) < 100:
                return None, 'Text too short. Please provide at least 100 characters.'
            
            if len(text) > 10000:
                text = text[:10000]  # Limit to 10k characters
            
            # Get prediction from ML model
            mbti_type, confidence, keywords = text_classifier.predict(text)
            
            # Save prediction
            prediction = {
                'userId': ObjectId(user_id),
                'mbtiType': mbti_type,
                'confidence': confidence,
                'textSnippet': text[:500],  # Store first 500 chars
                'textLength': len(text),
                'keywords': keywords,
                'timestamp': datetime.utcnow(),
                'ml_enhanced': True
            }
            
            result = self.predictions_collection.insert_one(prediction)
            
            return {
                'predictionId': str(result.inserted_id),
                'mbtiType': mbti_type,
                'confidence': confidence,
                'keywords': keywords,
                'textLength': len(text)
            }, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f'Prediction failed: {str(e)}'
    
    def get_latest_prediction(self, user_id):
        """Get user's most recent text prediction"""
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
    
    def get_user_predictions(self, user_id):
        """Get all predictions for a user"""
        try:
            predictions = list(self.predictions_collection.find(
                {'userId': ObjectId(user_id)}
            ).sort('timestamp', -1))
            
            for pred in predictions:
                pred['_id'] = str(pred['_id'])
                pred['userId'] = str(pred['userId'])
            
            return predictions
        except Exception:
            return []