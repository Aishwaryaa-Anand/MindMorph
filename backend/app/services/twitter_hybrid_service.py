from datetime import datetime
from bson import ObjectId
from app.ml_models.text_classifier import text_classifier
from app.services.twitter_real_api_client import twitter_real_client
from app.services.twitter_mock_api_client import twitter_mock_client
import os

# Toggle: Set to True to use Real API, False for Mock API
USE_REAL_API = os.getenv('USE_REAL_TWITTER_API', 'false').lower() == 'true'

class TwitterHybridService:
    """
    Hybrid Twitter service - tries Real API first, falls back to Mock
    """
    
    def __init__(self, db):
        self.db = db
        self.predictions_collection = db.twitter_predictions
        
        # Print which mode we're in
        if USE_REAL_API and twitter_real_client.is_available():
            print("🔵 Twitter Module: REAL API MODE (Limited to 100 reads/month)")
            print("⚠️  WARNING: Each analysis uses 20 tweets, so limit usage!")
        else:
            print("🟢 Twitter Module: MOCK API MODE (Unlimited)")
    
    def analyze_twitter(self, username, user_id):
        """Analyze Twitter profile - tries Real API first, falls back to Mock"""
        try:
            username = username.lstrip('@').lower()
            
            tweets = None
            profile = None
            source = None
            
            # Try Real API first (if enabled)
            if USE_REAL_API and twitter_real_client.is_available():
                print(f"\n{'='*60}")
                print(f"🔵 Attempting REAL Twitter API for @{username}")
                print(f"{'='*60}")
                
                tweets = twitter_real_client.get_user_tweets(username, max_tweets=20)
                
                if tweets and len(tweets) >= 5:
                    profile = twitter_real_client.get_user_profile(username)
                    source = 'twitter_api_real'
                    print(f"✅ SUCCESS: Using Real Twitter API")
                else:
                    print(f"⚠️  Real API returned insufficient data, falling back to Mock")
            
            # Fallback to Mock API
            if not tweets:
                print(f"\n{'='*60}")
                print(f"🟢 Using Mock API for @{username}")
                print(f"{'='*60}")
                
                tweets = twitter_mock_client.get_user_tweets(username, max_tweets=20)
                
                if tweets and len(tweets) >= 5:
                    profile = twitter_mock_client.get_user_profile(username)
                    source = 'mock_api'
                else:
                    return None, f'Username @{username} not found'
                
            # Store individual tweets (NEW)
            tweet_objects = []
            for i, tweet_text in enumerate(tweets):
                tweet_objects.append({
                    'index': i + 1,
                    'text': tweet_text,
                    'length': len(tweet_text)
                })

            
            # Combine tweets and predict
            combined_text = ' '.join(tweets)
            
            if len(combined_text) < 100:
                return None, 'Not enough tweet content for analysis.'
            
            print(f"\n🤖 Analyzing {len(combined_text)} characters with ML model...")
            mbti_type, confidence, keywords = text_classifier.predict(combined_text)
            
            # Save prediction WITH TWEETS (UPDATED)
            prediction = {
                'userId': ObjectId(user_id),
                'username': username,
                'mbtiType': mbti_type,
                'confidence': confidence,
                'tweetCount': len(tweets),
                'tweets': tweet_objects,  # NEW: Store actual tweets
                'totalCharacters': len(combined_text),
                'keywords': keywords,
                'source': source,
                'profileInfo': profile,
                'timestamp': datetime.utcnow(),
                'ml_enhanced': True
            }
            
            result = self.predictions_collection.insert_one(prediction)
            
            print(f"✅ Analysis complete: {mbti_type}")
            print(f"   Source: {source}")
            print(f"{'='*60}\n")
            
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
        """Get available mock usernames"""
        return ['elonmusk', 'billgates', 'naval', 'sundarpichai', 'barackobama']