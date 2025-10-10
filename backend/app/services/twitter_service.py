from datetime import datetime
from bson import ObjectId
from app.ml_models.text_classifier import text_classifier
from app.services.twitter_mock_api_client import twitter_mock_client

class TwitterService:
    """Service for Twitter-based MBTI predictions using Mock API"""
    
    def __init__(self, db):
        self.db = db
        self.predictions_collection = db.twitter_predictions
    
    def analyze_twitter(self, username, user_id):
        """
        Analyze Twitter profile and predict MBTI using Mock API
        """
        try:
            # Remove @ if present
            username = username.lstrip('@').lower()
            
            print(f"\n{'='*60}")
            print(f"Starting Twitter analysis for @{username}")
            print(f"{'='*60}")
            
            # Fetch tweets via Mock API
            tweets = twitter_mock_client.get_user_tweets(username, max_tweets=20)
            
            if not tweets or len(tweets) < 5:
                return None, f'Username @{username} not found or has too few tweets.'
            
            # Get profile info
            profile = twitter_mock_client.get_user_profile(username)
            
            # Combine tweets into one text
            combined_text = ' '.join(tweets)
            
            if len(combined_text) < 100:
                return None, 'Not enough tweet content for analysis.'
            
            # Predict using text classifier
            print(f"\n🤖 Analyzing {len(combined_text)} characters with ML model...")
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
                'source': 'mock_api',
                'profileInfo': profile,
                'timestamp': datetime.utcnow(),
                'ml_enhanced': True
            }
            
            result = self.predictions_collection.insert_one(prediction)
            
            print(f"✅ Analysis complete: {mbti_type}")
            print(f"{'='*60}\n")
            
            return {
                'predictionId': str(result.inserted_id),
                'username': username,
                'mbtiType': mbti_type,
                'confidence': confidence,
                'tweetCount': len(tweets),
                'keywords': keywords,
                'source': 'mock_api',
                'profileInfo': profile
            }, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            import traceback
            traceback.print_exc()
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
        """Get list of available usernames from mock API"""
        try:
            response = requests.get('http://localhost:5000/api/mock/twitter/available-users')
            if response.status_code == 200:
                users = response.json()['users']
                return [user['username'] for user in users]
        except:
            pass
        
        # Fallback to hardcoded list
        return ['elonmusk', 'billgates', 'naval', 'sundarpichai', 'barackobama']