import { useState } from 'react';

export default function MBTIInfoModal() {
  const [isOpen, setIsOpen] = useState(false);

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-r from-red-200 to-blue-200 text-white text-2xl shadow-xl hover:scale-110 transition-transform z-50"
        title="Learn about MBTI"
      >
        ❓
      </button>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="glass-card max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white">About MBTI</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="text-white/70 hover:text-white text-2xl"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="space-y-6 text-white/90">
          <div>
            <h3 className="text-xl font-bold text-white mb-2">What is MBTI?</h3>
            <p>
              The Myers-Briggs Type Indicator (MBTI) is a personality assessment that categorizes 
              people into 16 distinct personality types based on four dimensions.
            </p>
          </div>

          <div>
            <h3 className="text-xl font-bold text-white mb-3">Four Dimensions:</h3>
            <div className="space-y-3">
              <div className="p-3 rounded-lg bg-white/10">
                <p className="font-semibold text-white mb-1">Extraversion (E) vs Introversion (I)</p>
                <p className="text-sm">How you gain energy: from social interaction or solitude</p>
              </div>
              <div className="p-3 rounded-lg bg-white/10">
                <p className="font-semibold text-white mb-1">Sensing (S) vs Intuition (N)</p>
                <p className="text-sm">How you process information: concrete facts or abstract patterns</p>
              </div>
              <div className="p-3 rounded-lg bg-white/10">
                <p className="font-semibold text-white mb-1">Thinking (T) vs Feeling (F)</p>
                <p className="text-sm">How you make decisions: logic or personal values</p>
              </div>
              <div className="p-3 rounded-lg bg-white/10">
                <p className="font-semibold text-white mb-1">Judging (J) vs Perceiving (P)</p>
                <p className="text-sm">How you approach life: structured or flexible</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-bold text-white mb-2">16 Personality Types</h3>
            <p className="mb-3">
              Combining these four dimensions creates 16 unique personality types, 
              each with distinct characteristics, strengths, and growth areas.
            </p>
            <div className="grid grid-cols-4 gap-2">
              {['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP',
                'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP'].map(type => (
                <div key={type} className="px-3 py-2 rounded-lg bg-purple-500/30 text-center font-semibold text-sm">
                  {type}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-xl font-bold text-white mb-2">Our Approach</h3>
            <p>
              MindMorph uses advanced machine learning (BERT + Ensemble models) with 80% accuracy 
              to predict personality types from multiple sources: questionnaires, text, and social media.
            </p>
          </div>

          <div className="pt-4 border-t border-white/20">
            <p className="text-white/70 text-sm">
              <strong>Note:</strong> MBTI is a tool for self-understanding, not a definitive label. 
              Use results as guidance for personal growth and better self-awareness.
            </p>
          </div>
        </div>

        {/* Close Button */}
        <button
          onClick={() => setIsOpen(false)}
          className="w-full mt-6 px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold hover:from-purple-600 hover:to-blue-600 transition"
        >
          Got it!
        </button>
      </div>
    </div>
  );
}