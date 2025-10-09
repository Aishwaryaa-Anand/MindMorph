from datetime import datetime
from bson import ObjectId
from app.services.nitter_scraper import nitter_scraper
from app.ml_models.text_classifier import text_classifier

class TwitterService:
    """Service for Twitter-based MBTI predictions"""
    
    def __init__(self, db):
        self.db = db
        self.predictions_collection = db.twitter_predictions
    
    def analyze_twitter(self, username, user_id):
        """Analyze Twitter profile and predict MBTI"""
        try:
            # Get tweets
            tweets, source = nitter_scraper.get_tweets(username)
            
            if not tweets:
                return None, f'Username @{username} not found. Try: {", ".join(nitter_scraper.get_available_usernames())}'
            
            # Get profile info
            profile = nitter_scraper.get_profile_info(username)
            
            # Combine tweets into one text
            combined_text = ' '.join(tweets)
            
            if len(combined_text) < 100:
                return None, 'Not enough tweet content for analysis. User may have too few tweets.'
            
            # Predict using text classifier
            mbti_type, confidence, keywords = text_classifier.predict(combined_text)
            
            # Save prediction
            prediction = {
                'userId': ObjectId(user_id),
                'username': username,
                'mbtiType': mbti_type,
                'confidence': confidence,
                'tweetCount': len(tweets),
                'totalCharacters': len(combined_text),
                'keywords': keywords,
                'source': source,  # 'nitter' or 'mock'
                'profileInfo': profile,
                'timestamp': datetime.utcnow(),
                'ml_enhanced': True
            }
            
            result = self.predictions_collection.insert_one(prediction)
            
            return {
                'predictionId': str(result.inserted_id),
                'username': username,
                'mbtiType': mbti_type,
                'confidence': confidence,
                'tweetCount': len(tweets),
                'keywords': keywords,
                'source': source,
                'profileInfo': profile
            }, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f'Analysis failed: {str(e)}'
    
    def get_latest_prediction(self, user_id):
        """Get user's most recent Twitter prediction"""
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
    
    def get_available_usernames(self):
        """Get list of available mock usernames"""
        return nitter_scraper.get_available_usernames()