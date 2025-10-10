import requests
import os

class TwitterMockAPIClient:
    """
    Client for Mock Twitter API
    Mimics Tweepy's interface but uses our mock API
    """
    
    def __init__(self, base_url='http://localhost:5000/api/mock/twitter'):
        self.base_url = base_url
        self.is_mock = True
        print("✅ Mock Twitter API Client initialized")
    
    def is_available(self):
        """Check if mock API is available"""
        return True
    
    def get_user_tweets(self, username, max_tweets=20):
        """
        Fetch tweets from mock API
        
        Args:
            username: Twitter username (without @)
            max_tweets: Maximum number of tweets to fetch
        
        Returns:
            list: List of tweet texts, or None if failed
        """
        try:
            username = username.lstrip('@').lower()
            
            print(f"\n{'='*60}")
            print(f"🟢 MOCK API: Fetching tweets for @{username}")
            print(f"{'='*60}")
            
            # Step 1: Get user info
            user_response = requests.get(f"{self.base_url}/user/{username}")
            
            if user_response.status_code != 200:
                print(f"❌ User @{username} not found in mock API")
                return None
            
            user_data = user_response.json()['data']
            user_id = user_data['id']
            
            print(f"✅ Found user: {user_data['name']} (@{user_data['username']})")
            print(f"   User ID: {user_id}")
            
            # Step 2: Get user's tweets
            tweets_response = requests.get(
                f"{self.base_url}/users/{user_id}/tweets",
                params={'max_results': max_tweets}
            )
            
            if tweets_response.status_code != 200:
                print(f"❌ Failed to fetch tweets")
                return None
            
            tweets_data = tweets_response.json()['data']
            tweet_texts = [tweet['text'] for tweet in tweets_data]
            
            print(f"✅ Fetched {len(tweet_texts)} tweets from @{username}")
            print(f"\n📝 Sample tweets:")
            for i, tweet in enumerate(tweet_texts[:3], 1):
                preview = tweet[:80] + "..." if len(tweet) > 80 else tweet
                print(f"   {i}. {preview}")
            print(f"{'='*60}\n")
            
            return tweet_texts
            
        except Exception as e:
            print(f"❌ Mock API error: {str(e)}")
            return None
    
    def get_user_profile(self, username):
        """
        Get user profile from mock API
        
        Returns:
            dict: Profile info or None
        """
        try:
            username = username.lstrip('@').lower()
            
            response = requests.get(f"{self.base_url}/user/{username}")
            
            if response.status_code != 200:
                return None
            
            data = response.json()['data']
            metrics = data['public_metrics']
            
            profile = {
                'username': data['username'],
                'displayName': data['name'],
                'bio': data.get('description', ''),
                'verified': data.get('verified', False),
                'followers': f"{metrics['followers_count']:,}",
                'tweets': []
            }
            
            print(f"✅ Profile fetched: {profile['displayName']} (@{profile['username']})")
            print(f"   Followers: {profile['followers']}")
            
            return profile
            
        except Exception as e:
            print(f"❌ Failed to get profile: {str(e)}")
            return None

# Global instance
twitter_mock_client = TwitterMockAPIClient()