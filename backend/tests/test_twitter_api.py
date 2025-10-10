"""Test real Twitter API"""
import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

if not bearer_token:
    print("❌ No bearer token found in .env")
    exit(1)

print(f"✅ Bearer token found: {bearer_token[:20]}...")

try:
    # Initialize client
    print("\n🔧 Initializing Tweepy client...")
    client = tweepy.Client(bearer_token=bearer_token)
    print("✅ Client initialized")
    
    # Test 1: Get Twitter's official account
    # Test 1: Get a real active account
    print("\n🔵 Test 1: Fetching @elonmusk profile...")
    print("   Making API request...")
    
    user = client.get_user(username='elonmusk', user_fields=['description', 'public_metrics'])
    
    print(f"   Response received")
    print(f"   user object: {user}")
    print(f"   user.data: {user.data if hasattr(user, 'data') else 'No data attribute'}")
    
    if user.data:
        print(f"✅ SUCCESS! Found: {user.data.name}")
        print(f"   Username: @{user.data.username}")
        print(f"   ID: {user.data.id}")
    else:
        print("❌ user.data is None or empty")
        print(f"   Full response: {user}")
        exit(1)
    
    # Test 2: Get tweets
    print("\n🔵 Test 2: Fetching recent tweets...")
    tweets = client.get_users_tweets(
        id=user.data.id,
        max_results=5,
        exclude=['retweets', 'replies']
    )
    
    if tweets.data:
        print(f"✅ SUCCESS! Fetched {len(tweets.data)} tweets")
        for i, tweet in enumerate(tweets.data[:3], 1):
            print(f"\n{i}. {tweet.text[:100]}...")
    else:
        print("⚠️  No tweets found")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED! Twitter API is working!")
    print("="*60)
    
except tweepy.errors.Unauthorized as e:
    print(f"\n❌ UNAUTHORIZED ERROR")
    print(f"   Your bearer token is invalid or expired")
    print(f"   Error details: {str(e)}")
    print("\n🔧 How to fix:")
    print("   1. Go to https://developer.twitter.com/en/portal/dashboard")
    print("   2. Select your app")
    print("   3. Go to 'Keys and tokens' tab")
    print("   4. Regenerate Bearer Token")
    print("   5. Copy new token to .env file")
    
except tweepy.errors.Forbidden as e:
    print(f"\n❌ FORBIDDEN ERROR")
    print(f"   Your app doesn't have permission to access this endpoint")
    print(f"   Error details: {str(e)}")
    print("\n🔧 How to fix:")
    print("   1. Check app permissions in Twitter Developer Portal")
    print("   2. Make sure 'Read' permission is enabled")
    
except tweepy.errors.TooManyRequests as e:
    print(f"\n❌ RATE LIMIT EXCEEDED")
    print(f"   Error details: {str(e)}")
    print("   Wait 15 minutes and try again")
    
except tweepy.TweepyException as e:
    print(f"\n❌ Twitter API Error: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {str(e)}")
    import traceback
    traceback.print_exc()