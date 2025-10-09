import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/shared/Navbar';
import { twitterService } from '../../services/twitterService';

export default function TwitterAnalyze() {
  const [username, setUsername] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [availableUsernames, setAvailableUsernames] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadAvailableUsernames();
  }, []);

  const loadAvailableUsernames = async () => {
    try {
      const data = await twitterService.getAvailableUsernames();
      setAvailableUsernames(data.usernames);
    } catch (err) {
      console.error('Failed to load usernames:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!username.trim()) {
      setError('Please enter a Twitter username');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const result = await twitterService.analyze(username);
      navigate(`/twitter/result/${result.predictionId}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Please try again.');
      setSubmitting(false);
    }
  };

  const handleUsernameClick = (user) => {
    setUsername(user);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-cyan-600 to-teal-600">
      <Navbar showBackButton={true} backTo="/" />

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            Twitter Analysis
          </h1>
          <p className="text-white/90 text-lg">
            Analyze tweets to discover personality type
          </p>
        </div>

        {/* Info Card */}
        <div className="glass-card mb-6">
          <h3 className="text-xl font-bold text-white mb-3">🐦 How It Works</h3>
          <ul className="space-y-2 text-white/90">
            <li>• Enter any Twitter username (with or without @)</li>
            <li>• We analyze recent tweets using our 80% accuracy ML model</li>
            <li>• Uses Nitter (free Twitter scraper) </li>
            <li>• BERT + Ensemble technology </li>
          </ul>
        </div>

        {/* Input Form */}
        <div className="glass-card mb-6">
          <h3 className="text-xl font-bold text-white mb-4">Enter Username</h3>
          
          <form onSubmit={handleSubmit}>
            <div className="flex gap-3">
              <div className="flex-1">
                <div className="relative">
                  <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white/60 text-lg">
                    @
                  </span>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="username"
                    className="w-full pl-10 pr-4 py-3 rounded-lg bg-gray-900/50 text-white border-2 border-white/30 focus:border-blue-400 focus:outline-none placeholder-white/50"
                    disabled={submitting}
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={submitting || !username.trim()}
                className="px-8 py-3 rounded-lg bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-bold transition shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? (
                  <span className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Analyzing...
                  </span>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-4 p-3 rounded-lg bg-red-500/20 border border-red-500/50">
              <p className="text-red-200 text-center">{error}</p>
            </div>
          )}
        </div>

        {/* Available Usernames */}
        {availableUsernames.length > 0 && (
          <div className="glass-card">
            <h3 className="text-xl font-bold text-white mb-4">
              Try These Profiles
            </h3>
            <p className="text-white/70 mb-4 text-sm">
              Click any username to analyze (uses mock data for demo)
            </p>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {availableUsernames.map((user) => (
                <button
                  key={user}
                  onClick={() => handleUsernameClick(user)}
                  disabled={submitting}
                  className="px-4 py-3 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 text-white font-medium transition disabled:opacity-50 text-left"
                >
                  <span className="text-blue-300">@</span>{user}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Info Footer */}
        <div className="text-center mt-8">
          <p className="text-white/60 text-sm">
            💡 Note: Due to Twitter API costs, we use Nitter (free scraper) with mock data fallback
          </p>
        </div>
      </div>
    </div>
  );
}