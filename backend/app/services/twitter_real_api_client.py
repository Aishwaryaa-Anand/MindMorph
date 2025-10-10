import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterRealAPIClient:
    """Real Twitter API client using Tweepy"""
    
    def __init__(self):
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Twitter API"""
        try:
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            if not bearer_token:
                print("⚠️  No Twitter API credentials found")
                return
            
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )
            print("✅ Real Twitter API client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Twitter API: {e}")
    
    def is_available(self):
        """Check if API is ready"""
        return self.client is not None
    
    def get_user_tweets(self, username, max_tweets=20):
        """Fetch real tweets from Twitter API"""
        if not self.client:
            return None
        
        try:
            username = username.lstrip('@')
            print(f"\n🔵 REAL API: Fetching tweets for @{username}")
            
            # Get user
            user = self.client.get_user(username=username)
            if not user.data:
                print(f"❌ User @{username} not found")
                return None
            
            user_id = user.data.id
            print(f"✅ Found: {user.data.name} (@{user.data.username})")
            
            # Get tweets
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=min(max_tweets, 100),
                exclude=['retweets', 'replies'],
                tweet_fields=['lang']
            )
            
            if not tweets.data:
                print(f"⚠️  No tweets found")
                return None
            
            # Filter English tweets only
            tweet_texts = []
            for tweet in tweets.data:
                if hasattr(tweet, 'lang') and tweet.lang == 'en':
                    tweet_texts.append(tweet.text)
                elif not hasattr(tweet, 'lang'):
                    tweet_texts.append(tweet.text)
            
            print(f"✅ Fetched {len(tweet_texts)} tweets from Real Twitter API")
            return tweet_texts
            
        except tweepy.errors.Unauthorized:
            print(f"❌ Unauthorized - check bearer token")
            return None
        except tweepy.errors.NotFound:
            print(f"❌ User @{username} not found")
            return None
        except tweepy.TweepyException as e:
            print(f"❌ Twitter API error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def get_user_profile(self, username):
        """Get real profile from Twitter API"""
        if not self.client:
            return None
        
        try:
            username = username.lstrip('@')
            user = self.client.get_user(
                username=username,
                user_fields=['description', 'public_metrics', 'verified']
            )
            
            if not user.data:
                return None
            
            data = user.data
            metrics = data.public_metrics
            
            profile = {
                'username': data.username,
                'displayName': data.name,
                'bio': data.description or '',
                'verified': data.verified or False,
                'followers': f"{metrics['followers_count']:,}",
                'tweets': []
            }
            
            print(f"✅ Profile fetched from Real API: {profile['displayName']}")
            return profile
            
        except Exception as e:
            print(f"❌ Failed to get profile: {str(e)}")
            return None

# Global instance
twitter_real_client = TwitterRealAPIClient()