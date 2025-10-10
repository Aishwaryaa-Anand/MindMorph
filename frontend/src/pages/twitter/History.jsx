import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { twitterService } from '../../services/twitterService';
import Navbar from '../../components/shared/Navbar';
import Footer from '../../components/shared/Footer';

export default function TextHistory() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await twitterService.getHistory();
      setPredictions(data.predictions || []);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load history:', err);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center">
        <div className="glass-card p-8">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-white mx-auto"></div>
          <p className="text-white mt-4 text-center">Loading history...</p>
        </div>
      </div>
    );
  }

  const letterColors = {
    I: 'from-blue-500 to-blue-600',
    E: 'from-red-500 to-red-600',
    N: 'from-purple-500 to-purple-600',
    S: 'from-yellow-500 to-yellow-600',
    T: 'from-green-500 to-green-600',
    F: 'from-pink-500 to-pink-600',
    J: 'from-orange-500 to-orange-600',
    P: 'from-cyan-500 to-cyan-600'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-blue-500">
      <Navbar showBackButton={true} backTo="/" />

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
            Twitter Analysis History
          </h1>
          <p className="text-white/80 text-lg">
            Your Past Twitter Analyses
          </p>
        </div>

        {predictions.length === 0 ? (
          <div className="glass-card text-center py-16">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-2xl font-bold text-white mb-2">No History Yet</h3>
            <p className="text-white/70 mb-6">
              Analyze twitter to see your results here
            </p>
            <button
              onClick={() => navigate('/twitter/analyze')}
              className="btn-gradient px-8 py-3"
            >
              Analyze Twitter
            </button>
          </div>
        ) : (
          <>
            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="glass-card text-center">
                <p className="text-white/70 mb-2">Total Analyses</p>
                <p className="text-4xl font-bold text-white">{predictions.length}</p>
              </div>
              <div className="glass-card text-center">
                <p className="text-white/70 mb-2">Total Characters</p>
                <p className="text-4xl font-bold text-white">
                  {predictions.reduce((sum, p) => sum + (p.textLength || 0), 0).toLocaleString()}
                </p>
              </div>
              <div className="glass-card text-center">
                <p className="text-white/70 mb-2">Latest Type</p>
                <div className="flex justify-center gap-1">
                  {predictions[0].mbtiType.split('').map((letter, idx) => (
                    <div
                      key={idx}
                      className={`w-12 h-12 rounded-lg bg-gradient-to-br ${letterColors[letter]} flex items-center justify-center`}
                    >
                      <span className="text-xl font-bold text-white">{letter}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* History List */}
            <div className="space-y-4">
              {predictions.map((pred) => (
                <div
                  key={pred._id}
                  className="glass-card hover:scale-[1.02] transition-transform cursor-pointer"
                  onClick={() => navigate(`/twitter/result/${pred._id}`)}
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex items-center gap-4">
                      <div className="flex gap-2">
                        {pred.mbtiType.split('').map((letter, idx) => (
                          <div
                            key={idx}
                            className={`w-14 h-14 rounded-xl bg-gradient-to-br ${letterColors[letter]} flex items-center justify-center shadow-lg`}
                          >
                            <span className="text-2xl font-bold text-white">{letter}</span>
                          </div>
                        ))}
                      </div>
                      <div>
                        <p className="text-xl font-bold text-white">{pred.username}</p>
                        <p className="text-white/70 text-sm">
                          {new Date(pred.timestamp).toLocaleString()}
                        </p>
                        <p className="text-white/60 text-sm">
                          {pred.textLength?.toLocaleString()} characters
                        </p>
                      </div>
                    </div>
                    <div className="text-white/50">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        <div className="flex justify-center gap-4 mt-8">
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold transition border border-white/30"
          >
            Back to Home
          </button>
          <button
            onClick={() => navigate('/twitter/analyze')}
            className="px-8 py-3 rounded-lg btn-gradient"
          >
            Analyze New Profile
          </button>
        </div>
      </div>
      <Footer />
    </div>
  );
}