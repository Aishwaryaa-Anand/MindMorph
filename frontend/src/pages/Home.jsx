// import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/shared/Navbar';

export default function Home() {
  // const { user, logout } = useAuth();
  const navigate = useNavigate();

  const modules = [
    {
      title: 'Scenario Questionnaire',
      description: 'Answer realistic life scenarios to discover your personality',
      icon: '📝',
      time: '~10 minutes',
      route: '/questionnaire',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Text Analysis',
      description: 'Analyze your personality through your writing style',
      icon: '✍️',
      time: '~2 minutes',
      route: '/text',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Twitter Analysis',
      description: 'Discover personality insights from Twitter profiles',
      icon: '🐦',
      time: '~3 minutes',
      route: '/twitter',
      gradient: 'from-green-500 to-teal-500'
    }
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
              onClick={() => {
                if (module.route === '/questionnaire') {
                  navigate('/questionnaire/test');
                } else {
                  alert(`${module.title} - Coming soon!`);
                }
              }}  
              className="group glass-card hover:scale-105 transition-all duration-300 text-left"
            >
              {/* Icon */}
              <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${module.gradient} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}>
                {module.icon}
              </div>

              {/* Content */}
              <h3 className="text-2xl font-bold text-white mb-2">
                {module.title}
              </h3>
              <p className="text-white/70 mb-4">
                {module.description}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-white/60 text-sm">{module.time}</span>
                <span className="text-white font-medium group-hover:translate-x-2 transition-transform">
                  Start →
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}