import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { textService } from '../../services/textService';
import Navbar from '../../components/shared/Navbar';
import { generateQuestionnairePDF } from "../../utils/pdfGenerator";
import Footer from '../../components/shared/Footer';

export default function TextResult() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadResult();
  }, [id]);

  const loadResult = async () => {
    try {
      const data = await textService.getResultById(id);
      setResult(data);
      setLoading(false);
    } catch {
      setError('Failed to load results');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center">
        <div className="glass-card p-8">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-white mx-auto"></div>
          <p className="text-white mt-4 text-center">Loading your results...</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center p-4">
        <div className="glass-card p-8 max-w-md text-center">
          <p className="text-white text-xl mb-4">Failed to load results</p>
          <button
            onClick={() => navigate('/')}
            className="btn-gradient px-6 py-3"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const { prediction, insights } = result;
  const mbti = prediction.mbtiType;
  const confidence = prediction.confidence;
  // const keywords = prediction.keywords || [];

  // MBTI letter colors
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

      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
            Your Personality Type
          </h1>
          <p className="text-white/80 text-lg">
            Based on {prediction.textLength} characters of your writing
          </p>
        </div>

        {/* MBTI Type Card */}
        <div className="glass-card mb-8 text-center">
          <h2 className="text-white/80 text-lg mb-4">You are an</h2>

          {/* MBTI Letters */}
          <div className="flex justify-center gap-3 mb-6">
            {mbti.split('').map((letter, idx) => (
              <div
                key={idx}
                className={`w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-gradient-to-br ${letterColors[letter]} flex items-center justify-center shadow-xl transform hover:scale-110 transition-transform`}
              >
                <span className="text-4xl md:text-5xl font-bold text-white">
                  {letter}
                </span>
              </div>
            ))}
          </div>

          <h3 className="text-3xl md:text-4xl font-bold text-white mb-2">
            {insights.title}
          </h3>
          <p className="text-xl text-white/90 mb-4">
            {mbti} - {insights.percentage}
          </p>
          <p className="text-white/80 text-lg max-w-3xl mx-auto leading-relaxed">
            {insights.description}
          </p>
        </div>

        {/* Confidence Scores */}
        <div className="glass-card mb-8">
          <h3 className="text-2xl font-bold text-white mb-6">
            Confidence Breakdown
          </h3>
          <div className="space-y-4">
            {Object.entries(confidence).map(([dimension, score]) => {
              const percentage = Math.round(score * 100);
              const labels = {
                IE: mbti[0] === 'I' ? 'Introversion' : 'Extraversion',
                NS: mbti[1] === 'N' ? 'Intuition' : 'Sensing',
                TF: mbti[2] === 'T' ? 'Thinking' : 'Feeling',
                JP: mbti[3] === 'J' ? 'Judging' : 'Perceiving'
              };

              return (
                <div key={dimension}>
                  <div className="flex justify-between mb-2">
                    <span className="text-white font-semibold">{labels[dimension]}</span>
                    <span className="text-white font-bold">{percentage}%</span>
                  </div>
                  <div className="w-full h-4 bg-gray-900/50 rounded-full overflow-hidden border border-white/30">
                    <div
                      className={`h-full bg-gradient-to-r ${
                        percentage >= 80 ? 'from-green-400 to-green-500' :
                        percentage >= 60 ? 'from-blue-400 to-blue-500' :
                        'from-yellow-400 to-yellow-500'
                      } transition-all duration-1000`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
          <p className="text-white/60 text-sm mt-4 text-center">
            ✨ Analyzed using BERT + Ensemble ML (80.36% accuracy)
          </p>
        </div>

        {/* Keywords Section - UNIQUE TO TEXT ANALYSIS
        {keywords.length > 0 && (
          <div className="glass-card mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">
              Key Language Patterns
            </h3>
            <p className="text-white/80 mb-4">
              Words and phrases that influenced your personality classification:
            </p>
            <div className="flex flex-wrap gap-2">
              {keywords.map((keyword, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 rounded-full bg-purple-500/30 border border-purple-500/50 text-white font-medium"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )} */}

        {/* Strengths & Weaknesses */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="glass-card">
            <h3 className="text-2xl font-bold text-white mb-4">Strengths</h3>
            <ul className="space-y-2">
              {insights.strengths.map((strength, idx) => (
                <li key={idx} className="flex items-start gap-2 text-white/90">
                  <span className="text-green-400 mt-1">✓</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="glass-card">
            <h3 className="text-2xl font-bold text-white mb-4">Growth Areas</h3>
            <ul className="space-y-2">
              {insights.weaknesses.map((weakness, idx) => (
                <li key={idx} className="flex items-start gap-2 text-white/90">
                  <span className="text-yellow-400 mt-1">→</span>
                  <span>{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Career Suggestions */}
        <div className="glass-card mb-8">
          <h3 className="text-2xl font-bold text-white mb-4">Recommended Careers</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {insights.careers.map((career, idx) => (
              <div
                key={idx}
                className="px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white text-center hover:bg-white/20 transition"
              >
                {career}
              </div>
            ))}
          </div>
        </div>

        {/* Compatibility */}
        {insights.compatibility && (
          <div className="glass-card mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">Best Matches</h3>
            <p className="text-white/80 mb-6">
              Personality types that complement yours well
            </p>
            <div className="space-y-4">
              {insights.compatibility.best_matches.map((match) => {
                const compat = insights.compatibility.compatibility[match];
                return (
                  <div
                    key={match}
                    className="p-4 rounded-lg bg-white/10 border border-white/20"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-xl font-bold text-white">{match}</h4>
                      <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 font-semibold">
                        {compat.score}% Match
                      </span>
                    </div>
                    <p className="text-white/90 mb-2">{compat.why}</p>
                    <p className="text-white/70 text-sm">
                      <span className="font-semibold">Challenge:</span> {compat.challenges}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Growth Tips */}
        <div className="glass-card mb-8">
          <h3 className="text-2xl font-bold text-white mb-4">Personal Growth Tips</h3>
          <ul className="space-y-3">
            {insights.growth_tips.map((tip, idx) => (
              <li key={idx} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-500/30 flex items-center justify-center text-white font-bold">
                  {idx + 1}
                </span>
                <span className="text-white/90 text-lg pt-1">{tip}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Famous People */}
        <div className="glass-card mb-8">
          <h3 className="text-2xl font-bold text-white mb-4">Famous {mbti}s</h3>
          <div className="flex flex-wrap gap-3">
            {insights.famous_people.map((person, idx) => (
              <div
                key={idx}
                className="px-4 py-2 rounded-full bg-purple-500/20 border border-purple-500/30 text-white"
              >
                {person}
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold transition border border-white/30"
          >
            Back to Home
          </button>
          <button
            onClick={() => navigate('/text/analyze')}
            className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-semibold transition shadow-lg"
          >
            Analyze New Text
          </button>
          <button
            onClick={() => generateQuestionnairePDF(prediction, insights)}
            className="px-8 py-3 rounded-lg btn-gradient"
          >
            Download PDF Report
          </button>
        </div>
      </div>
      <Footer />
    </div>
  );
}