// import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from "react-router-dom";
import Navbar from "../components/shared/Navbar";
import MBTIInfoModal from '../components/shared/MBTIInfoModal';
import Footer from '../components/shared/Footer';

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
      <Navbar />
      <MBTIInfoModal />
       

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            Welcome to MindMorph
          </h1>
          <p className="text-xl text-white/90 max-w-3xl mx-auto">
            Discover your personality through AI-powered analysis. Choose a module below to begin your journey.
          </p>
        </div>

        {/* Module Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {modules.map((module, index) => (
            <button
              key={index}
              onClick={() => navigate(module.path)}
              disabled={module.status === 'coming-soon'}
              className="group glass-card hover:scale-105 transition-all duration-300 text-left disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {/* Icon */}
              <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${module.color} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}>
                {module.icon}
              </div>

              {/* Content */}
              <h3 className="text-2xl font-bold text-white mb-2">
                {module.title}
              </h3>
              <p className="text-white/70 mb-4">
                {module.description}
              </p>
              
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
                  {module.status === 'active' ? 'Ready' : 'Coming Soon'}
                </span>
                <span className="text-white font-medium group-hover:translate-x-2 transition-transform">
                  {module.status === 'active' ? 'Start →' : 'Soon →'}
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* NEW: History Section */}
        <div className="glass-card mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2">
                📜 Your Analysis History
              </h2>
              <p className="text-white/70">
                View your past personality assessments and results
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {/* Questionnaire History */}
            <button
              onClick={() => navigate('/questionnaire/history')}
              className="p-6 rounded-xl bg-white/10 hover:bg-white/20 border-2 border-white/20 hover:border-purple-400 transition-all group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-2xl">
                  📋
                </div>
                <div className="text-left">
                  <h3 className="text-lg font-bold text-white">Questionnaire</h3>
                  <p className="text-white/60 text-sm">View past tests</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-white/70 group-hover:text-white transition">
                <span className="text-sm">View History</span>
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </button>

            {/* Text History */}
            <button
              onClick={() => navigate('/text/history')}
              className="p-6 rounded-xl bg-white/10 hover:bg-white/20 border-2 border-white/20 hover:border-indigo-400 transition-all group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-2xl">
                  📝
                </div>
                <div className="text-left">
                  <h3 className="text-lg font-bold text-white">Text Analysis</h3>
                  <p className="text-white/60 text-sm">View past analyses</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-white/70 group-hover:text-white transition">
                <span className="text-sm">View History</span>
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </button>

            {/* Twitter History */}
            <button
              onClick={() => navigate('/twitter/history')}
              className="p-6 rounded-xl bg-white/10 hover:bg-white/20 border-2 border-white/20 hover:border-blue-400 transition-all group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-2xl">
                  🐦
                </div>
                <div className="text-left">
                  <h3 className="text-lg font-bold text-white">Twitter Analysis</h3>
                  <p className="text-white/60 text-sm">View past profiles</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-white/70 group-hover:text-white transition">
                <span className="text-sm">View History</span>
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </button>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="glass-card text-center">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="text-xl font-bold text-white mb-2">80% Accuracy</h3>
            <p className="text-white/70">
              ML-enhanced predictions with BERT + Ensemble models
            </p>
          </div>
          <div className="glass-card text-center">
            <div className="text-4xl mb-3">🔒</div>
            <h3 className="text-xl font-bold text-white mb-2">Privacy First</h3>
            <p className="text-white/70">
              Your data is secure and never shared with third parties
            </p>
          </div>
          <div className="glass-card text-center">
            <div className="text-4xl mb-3">📄</div>
            <h3 className="text-xl font-bold text-white mb-2">PDF Reports</h3>
            <p className="text-white/70">
              Download detailed reports with insights and recommendations
            </p>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-blue-500">
//       {/* Use Navbar component */}
//       <Navbar />

//       {/* Main Content */}
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
//         {/* Header */}
//         <div className="text-center mb-12">
//           <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
//             Choose Your Assessment Method
//           </h2>
//           <p className="text-xl text-white/80">
//             Discover your MBTI personality type through multiple approaches
//           </p>
//         </div>

//         {/* Module Cards */}
//         <div className="grid md:grid-cols-3 gap-8">
//           {modules.map((module, index) => (
//             <button
//               key={index}
//               onClick={() => navigate(module.path)}
//               className="group glass-card hover:scale-105 transition-all duration-300 text-left"
//             >
//               {/* Icon */}
//               <div
//                 className={`w-16 h-16 rounded-xl bg-gradient-to-br ${module.color} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}
//               >
//                 {module.icon}
//               </div>

//               {/* Content */}
//               <h3 className="text-2xl font-bold text-white mb-2">
//                 {module.title}
//               </h3>
//               <p className="text-white/70 mb-4">{module.description}</p>

//               {/* Accuracy Badge */}
//               {module.accuracy && (
//                 <div className="mb-3">
//                   <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-sm font-semibold border border-green-500/30">
//                     {module.accuracy} Accuracy
//                   </span>
//                 </div>
//               )}

//               <div className="flex items-center justify-between">
//                 <span className="text-white/60 text-sm">
//                   {module.status === "active" ? "Ready" : "Coming Soon"}
//                 </span>
//                 <span className="text-white font-medium group-hover:translate-x-2 transition-transform">
//                   {module.status === "active" ? "Start →" : "Soon →"}
//                 </span>
//               </div>
//             </button>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// }
