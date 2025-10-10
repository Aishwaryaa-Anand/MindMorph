import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/shared/Navbar';
import { textService } from '../../services/textService';
import toast from 'react-hot-toast';
import Footer from '../../components/shared/Footer';

export default function TextAnalyze() {
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (text.trim().length < 100) {
      setError('Please provide at least 100 characters for accurate analysis.');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const result = await textService.predict(text);
      toast.success('Analysis complete!');
      navigate(`/text/result/${result.predictionId}`);
    } catch (err) {
      toast.error(err.response?.data?.error || 'Analysis failed. Please try again.');
      setSubmitting(false);
    }
  };

  const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
  const charCount = text.length;
  const isValid = charCount >= 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-blue-600">
      <Navbar showBackButton={true} backTo="/" />

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            Text Analysis
          </h1>
          <p className="text-white/90 text-lg">
            Paste your writing and discover your MBTI personality type
          </p>
        </div>

        {/* Instructions Card */}
        <div className="glass-card mb-6">
          <h3 className="text-xl font-bold text-white mb-3">📝 Instructions</h3>
          <ul className="space-y-2 text-white/90">
            <li>• Paste any substantial text you've written (blog posts, essays, emails, journal entries)</li>
            <li>• Minimum 100 characters required (500+ recommended for best accuracy)</li>
            <li>• The more text, the more accurate the analysis</li>
            <li>• Our AI analyzes your writing style, word choice, and linguistic patterns</li>
          </ul>
        </div>

        {/* Text Input Card */}
        <div className="glass-card mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Your Text</h3>
            <div className="flex gap-4 text-sm">
              <span className={`font-semibold ${isValid ? 'text-green-400' : 'text-yellow-400'}`}>
                {charCount} characters
              </span>
              <span className="text-white/70">|</span>
              <span className="text-white/90">{wordCount} words</span>
            </div>
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your text here... Share your thoughts, experiences, or any writing that represents you."
            className="w-full h-64 md:h-80 p-4 rounded-lg bg-gray-900/50 text-white border-2 border-white/30 focus:border-blue-400 focus:outline-none resize-none placeholder-white/50"
            disabled={submitting}
          />

          {/* Character Progress Bar */}
          <div className="mt-4">
            <div className="flex justify-between mb-2 text-sm">
              <span className="text-white/80">Minimum: 100 characters</span>
              <span className="text-white/80">Recommended: 500+</span>
            </div>
            <div className="w-full h-3 bg-gray-900/50 rounded-full overflow-hidden border border-white/30">
              <div
                className={`h-full transition-all duration-300 ${
                  charCount >= 500 ? 'bg-green-500' :
                  charCount >= 100 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${Math.min((charCount / 500) * 100, 100)}%` }}
              ></div>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 rounded-lg bg-red-500/20 border border-red-500/50">
              <p className="text-red-200 text-center">{error}</p>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 rounded-lg bg-gray-900/50 hover:bg-gray-900/70 text-white font-semibold transition border border-white/30"
            disabled={submitting}
          >
            Cancel
          </button>

          <button
            onClick={handleSubmit}
            disabled={!isValid || submitting}
            className="px-8 py-3 rounded-lg bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-bold transition shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Analyzing...
              </span>
            ) : (
              'Analyze Text'
            )}
          </button>
        </div>

        {/* Sample Text Button */}
        {charCount === 0 && (
          <div className="text-center mt-6">
            <button
              onClick={() => setText("I've always been someone who prefers deep, meaningful conversations over small talk. I find myself constantly analyzing situations and thinking about the underlying patterns and connections. When I'm working on a project, I need to understand the complete picture before diving into details. I often get lost in thought about future possibilities and theoretical concepts. My friends say I'm a good listener, but I can be quite reserved in large social gatherings. I prefer spending time with a small group of close friends rather than attending big parties. I value authenticity and depth in relationships, and I'm always striving to understand myself and others better. Logic and reason guide most of my decisions, though I do consider how my choices affect people I care about. I like having a plan and structure in my life, but I'm flexible when needed. Reading, learning new things, and exploring ideas are some of my favorite activities.")}
              className="text-blue-300 hover:text-blue-200 underline text-sm"
            >
              Use Sample Text
            </button>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}