import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { questionnaireService } from "../../services/questionnaireService";
import QuestionCard from "../../components/questionnaire/QuestionCard";
import ProgressBar from "../../components/questionnaire/ProgressBar";

export default function QuestionnaireTest() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await questionnaireService.getQuestions();
      setQuestions(data.questions);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load questions:", error);
      alert("Failed to load questions. Please try again.");
    }
  };

  const handleAnswer = (choice) => {
    setAnswers({
      ...answers,
      [currentQuestion]: choice,
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    // Check all questions answered
    const unanswered = questions.findIndex((_, idx) => !answers[idx]);
    if (unanswered !== -1) {
      alert(
        `Please answer all questions. Question ${unanswered + 1} is unanswered.`
      );
      setCurrentQuestion(unanswered);
      return;
    }

    setSubmitting(true);

    try {
      // Format answers for API
      const formattedAnswers = questions.map((q, idx) => ({
        questionId: q.id,
        choice: answers[idx],
      }));

      const result = await questionnaireService.predict(formattedAnswers);

      // Navigate to results page
      navigate(`/questionnaire/result/${result.predictionId}`);
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Failed to process your answers. Please try again.");
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
        <div className="glass-card p-8">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-white mx-auto"></div>
          <p className="text-white mt-4 text-center">Loading questions...</p>
        </div>
      </div>
    );
  }

  const isLastQuestion = currentQuestion === questions.length - 1;
  const allAnswered = questions.every((_, idx) => answers[idx]);
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-blue-500 py-6 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header - Compact with Exit button */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => {
              if (answeredCount > 0) {
                const confirm = window.confirm(
                  "Are you sure? Your progress will be lost."
                );
                if (confirm) navigate("/");
              } else {
                navigate("/");
              }
            }}
            className="px-4 py-2 rounded-lg bg-gray-900/50 hover:bg-gray-900/70 text-white font-medium transition border border-white/30"
          >
            ← Home
          </button>
          <div className="text-center flex-1">
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
              Personality Assessment
            </h1>
            <p className="text-white/90 text-sm md:text-base">
              Choose the answer that best describes you
            </p>
          </div>
          <div className="w-24"></div> {/* Spacer for centering */}
        </div>

        {/* Progress */}
        <ProgressBar current={currentQuestion + 1} total={questions.length} />

        {/* Question */}
        <QuestionCard
          question={questions[currentQuestion]}
          selectedAnswer={answers[currentQuestion]}
          onAnswer={handleAnswer}
          questionNumber={currentQuestion + 1}
          totalQuestions={questions.length}
        />

        {/* Navigation - Compact and clear */}
        <div className="mt-6 flex items-center justify-between gap-4">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="px-5 py-2.5 rounded-lg bg-gray-900/50 hover:bg-gray-900/70 text-white font-medium transition border border-white/30 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            ← Back
          </button>

          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-900/50 border border-white/30">
            <span className="text-white font-semibold">{answeredCount}</span>
            <span className="text-white/80">/</span>
            <span className="text-white/80">{questions.length}</span>
          </div>

          {!isLastQuestion ? (
            <button
              onClick={handleNext}
              disabled={!answers[currentQuestion]}
              className="px-5 py-2.5 rounded-lg bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-semibold transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!allAnswered || submitting}
              className="px-6 py-2.5 rounded-lg bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 hover:from-green-600 hover:via-blue-600 hover:to-purple-600 text-white font-bold transition shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? "Processing..." : "Get Results"}
            </button>
          )}
        </div>

        {/* Help text - Only show when needed */}
        {isLastQuestion && !allAnswered && (
          <div className="mt-4 p-3 rounded-lg bg-yellow-500/20 border border-yellow-500/50">
            <p className="text-center text-white text-sm font-medium">
              ⚠️ Please answer all questions to see your results
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
