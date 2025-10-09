// import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from "react-router-dom";
import Navbar from "../components/shared/Navbar";

export default function Home() {
  // const { user, logout } = useAuth();
  const navigate = useNavigate();

  const modules = [
    {
      title: "Scenario Questionnaire",
      description:
        "Answer 20 real-life scenarios to discover your personality type",
      icon: "📋",
      path: "/questionnaire/test",
      color: "from-purple-500 to-pink-500",
      accuracy: "75%",
      status: "active",
    },
    {
      title: "Text Analysis",
      description: "Analyze your writing style to determine MBTI type",
      icon: "📝",
      path: "/text/analyze",
      color: "from-indigo-500 to-purple-500",
      accuracy: "80%",
      status: "active",
    },
    {
      title: "Twitter Analysis",
      description: "Analyze tweets and social media to predict personality",
      icon: "🐦",
      path: "/twitter/analyze",
      color: "from-blue-500 to-cyan-500",
      accuracy: "80%",
      status: "active", // Changed from 'coming-soon'
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-blue-500">
      {/* Use Navbar component */}
      <Navbar />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Choose Your Assessment Method
          </h2>
          <p className="text-xl text-white/80">
            Discover your MBTI personality type through multiple approaches
          </p>
        </div>

        {/* Module Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          {modules.map((module, index) => (
            <button
              key={index}
              onClick={() => navigate(module.path)}
              className="group glass-card hover:scale-105 transition-all duration-300 text-left"
            >
              {/* Icon */}
              <div
                className={`w-16 h-16 rounded-xl bg-gradient-to-br ${module.color} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}
              >
                {module.icon}
              </div>

              {/* Content */}
              <h3 className="text-2xl font-bold text-white mb-2">
                {module.title}
              </h3>
              <p className="text-white/70 mb-4">{module.description}</p>

              {/* Accuracy Badge */}
              {module.accuracy && (
                <div className="mb-3">
                  <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-sm font-semibold border border-green-500/30">
                    {module.accuracy} Accuracy
                  </span>
                </div>
              )}

              <div className="flex items-center justify-between">
                <span className="text-white/60 text-sm">
                  {module.status === "active" ? "Ready" : "Coming Soon"}
                </span>
                <span className="text-white font-medium group-hover:translate-x-2 transition-transform">
                  {module.status === "active" ? "Start →" : "Soon →"}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
