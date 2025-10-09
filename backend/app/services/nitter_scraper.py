import requests
from bs4 import BeautifulSoup
import json
import os
import time

class NitterScraper:
    """Scrape tweets from Nitter instances (free Twitter alternative)"""
    
    # Updated list of public Nitter instances (as of 2025)
    NITTER_INSTANCES = [
        'https://nitter.net',
        'https://nitter.poast.org',
        'https://nitter.privacydev.net',
        'https://nitter.1d4.us',
        'https://nitter.kavin.rocks'
    ]
    
    def __init__(self):
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self):
        """Load mock Twitter data"""
        try:
            mock_file = os.path.join(os.path.dirname(__file__), '../../data/mock_twitter_data.json')
            with open(mock_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load mock data: {e}")
            return {}
    
    def get_tweets(self, username):
        """
        Get tweets for a username
        Try Nitter first, fallback to mock data
        
        Returns:
            tuple: (tweets_list, source) where source is 'nitter' or 'mock'
        """
        # Remove @ if present
        username = username.lstrip('@').lower()
        
        print(f"\n{'='*60}")
        print(f"Attempting to fetch tweets for: @{username}")
        print(f"{'='*60}")
        
        # Try Nitter scraping first
        tweets = self._scrape_from_nitter(username)
        if tweets:
            print(f"✅ SUCCESS: Scraped {len(tweets)} tweets from Nitter")
            return tweets, 'nitter'
        
        print(f"⚠️  Nitter scraping failed, using mock data")
        
        # Fallback to mock data
        if username in self.mock_data:
            print(f"✅ Found {username} in mock data")
            return self.mock_data[username]['tweets'], 'mock'
        
        print(f"❌ Username {username} not found in mock data either")
        return None, None
    
    def get_profile_info(self, username):
        """Get profile information"""
        username = username.lstrip('@').lower()
        
        if username in self.mock_data:
            return self.mock_data[username]
        
        return None
    
    def _scrape_from_nitter(self, username):
        """Try to scrape tweets from Nitter instances"""
        for instance in self.NITTER_INSTANCES:
            try:
                url = f"{instance}/{username}"
                print(f"\n🔍 Trying: {url}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try multiple selectors (Nitter's HTML changes)
                    tweet_selectors = [
                        'div.tweet-content',
                        'div.tweet-body',
                        'div[class*="tweet-content"]',
                        'div[class*="tweet"] p'
                    ]
                    
                    tweets = []
                    for selector in tweet_selectors:
                        tweet_contents = soup.select(selector)
                        print(f"   Selector '{selector}': Found {len(tweet_contents)} elements")
                        
                        if tweet_contents:
                            for content in tweet_contents[:20]:  # Get max 20 tweets
                                text = content.get_text(strip=True)
                                if len(text) > 20:  # Filter out very short tweets
                                    tweets.append(text)
                            
                            if len(tweets) >= 5:  # Need at least 5 tweets
                                print(f"   ✅ Successfully extracted {len(tweets)} tweets!")
                                return tweets
                    
                    print(f"   ❌ No tweets found with any selector")
                    
                    # Debug: Save HTML to file to inspect
                    if len(soup.get_text()) > 100:
                        debug_file = f"nitter_debug_{username}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(str(soup.prettify()))
                        print(f"   💾 Saved HTML to {debug_file} for inspection")
                
            except requests.Timeout:
                print(f"   ⏱️  Timeout error")
            except requests.RequestException as e:
                print(f"   ❌ Request error: {str(e)}")
            except Exception as e:
                print(f"   ❌ Unexpected error: {str(e)}")
                continue
        
        return None
    
    def get_available_usernames(self):
        """Get list of available mock usernames"""
        return list(self.mock_data.keys())

# Global instance
nitter_scraper = NitterScraper()