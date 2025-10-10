from flask import Blueprint, jsonify, request
import json
import os
from datetime import datetime, timedelta
import random

bp = Blueprint('twitter_mock_api', __name__, url_prefix='/api/mock/twitter')

# Load mock data
def load_mock_data():
    try:
        mock_file = os.path.join(os.path.dirname(__file__), '../../data/mock_twitter_data.json')
        with open(mock_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load mock data: {e}")
        return {}

mock_data = load_mock_data()

@bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    """
    Mock Twitter API endpoint: Get user by username
    Simulates: GET https://api.twitter.com/2/users/by/username/:username
    """
    username = username.lower()
    
    if username not in mock_data:
        return jsonify({
            'errors': [{
                'title': 'Not Found Error',
                'detail': f'Could not find user with username: {username}',
                'type': 'https://api.twitter.com/2/problems/resource-not-found'
            }]
        }), 404
    
    profile = mock_data[username]
    
    # Format like real Twitter API v2 response
    return jsonify({
        'data': {
            'id': str(hash(username) % 10000000000),  # Generate fake ID
            'name': profile['displayName'],
            'username': username,
            'description': profile.get('bio', ''),
            'verified': profile.get('verified', False),
            'public_metrics': {
                'followers_count': int(profile.get('followers', '0').replace(',', '').replace('M', '000000').replace('K', '000')),
                'following_count': random.randint(100, 1000),
                'tweet_count': len(profile.get('tweets', [])),
                'listed_count': random.randint(50, 500)
            }
        }
    }), 200

@bp.route('/users/<user_id>/tweets', methods=['GET'])
def get_user_tweets(user_id):
    """
    Mock Twitter API endpoint: Get user's tweets
    Simulates: GET https://api.twitter.com/2/users/:id/tweets
    """
    # Find user by ID (reverse lookup)
    username = None
    for uname, profile in mock_data.items():
        if str(hash(uname) % 10000000000) == user_id:
            username = uname
            break
    
    if not username:
        return jsonify({
            'errors': [{
                'title': 'Not Found Error',
                'detail': f'Could not find user with id: {user_id}',
                'type': 'https://api.twitter.com/2/problems/resource-not-found'
            }]
        }), 404
    
    profile = mock_data[username]
    tweets = profile.get('tweets', [])
    
    # Get query parameters
    max_results = min(int(request.args.get('max_results', 10)), 100)
    
    # Create mock tweet objects
    tweet_data = []
    base_time = datetime.now()
    
    for i, tweet_text in enumerate(tweets[:max_results]):
        tweet_data.append({
            'id': str(hash(tweet_text) % 10000000000000000),
            'text': tweet_text,
            'created_at': (base_time - timedelta(days=i)).isoformat() + 'Z',
            'lang': 'en',
            'public_metrics': {
                'retweet_count': random.randint(10, 10000),
                'reply_count': random.randint(5, 1000),
                'like_count': random.randint(50, 50000),
                'quote_count': random.randint(0, 500)
            }
        })
    
    # Format like real Twitter API v2 response
    return jsonify({
        'data': tweet_data,
        'meta': {
            'result_count': len(tweet_data),
            'newest_id': tweet_data[0]['id'] if tweet_data else None,
            'oldest_id': tweet_data[-1]['id'] if tweet_data else None
        }
    }), 200

@bp.route('/available-users', methods=['GET'])
def get_available_users():
    """List all available mock users (custom endpoint)"""
    users = []
    for username, profile in mock_data.items():
        users.append({
            'username': username,
            'name': profile['displayName'],
            'verified': profile.get('verified', False),
            'tweet_count': len(profile.get('tweets', []))
        })
    
    return jsonify({'users': users}), 200