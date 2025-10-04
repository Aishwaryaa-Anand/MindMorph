export default function QuestionCard({ question, selectedAnswer, onAnswer, questionNumber, totalQuestions }) {
  return (
    <div className="glass-card max-w-4xl mx-auto">
      {/* Question Number - More contrast */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-white/30">
        <span className="text-white font-semibold text-base">
          Question {questionNumber} of {totalQuestions}
        </span>
        <span className="px-3 py-1 rounded-full bg-white/20 text-white text-sm font-medium">
          {question.dimension === 'IE' ? 'Energy' :
           question.dimension === 'NS' ? 'Information' :
           question.dimension === 'TF' ? 'Decisions' :
           'Lifestyle'}
        </span>
      </div>

      {/* Scenario - Better spacing */}
      <h3 className="text-xl md:text-2xl font-bold text-white mb-6 leading-relaxed">
        {question.scenario}
      </h3>

      {/* Choices - Improved contrast and spacing */}
      <div className="space-y-3">
        {question.choices.map((choice) => (
          <button
            key={choice.label}
            onClick={() => onAnswer(choice.label)}
            className={`w-full text-left p-4 md:p-5 rounded-xl border-2 transition-all duration-200 ${
              selectedAnswer === choice.label
                ? 'border-green-400 bg-green-400/20 shadow-lg shadow-green-400/30'
                : 'border-white/30 bg-gray-900/30 hover:bg-gray-900/50 hover:border-white/50'
            }`}
          >
            <div className="flex items-start gap-3">
              {/* Radio button - Better visibility */}
              <div className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                selectedAnswer === choice.label
                  ? 'border-green-400 bg-green-400'
                  : 'border-white/60 bg-transparent'
              }`}>
                {selectedAnswer === choice.label && (
                  <div className="w-3 h-3 rounded-full bg-white"></div>
                )}
              </div>

              {/* Choice text - Better contrast */}
              <div className="flex-1">
                <span className="text-white font-bold text-base md:text-lg">
                  {choice.label}.
                </span>
                <span className="text-white/95 ml-2 text-base md:text-lg">
                  {choice.text}
                </span>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}