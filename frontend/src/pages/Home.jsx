import { useAuth } from '../hooks/useAuth';

export default function Home() {
  const { user, logout } = useAuth();

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
      {/* Navbar */}
      <nav className="glass border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-white">MindMorph</h1>
            <div className="flex items-center gap-4">
              <span className="text-white/80">Hello, {user?.name}!</span>
              <button
                onClick={logout}
                className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition backdrop-blur-sm border border-white/20"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

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
              onClick={() => alert(`${module.title} - Coming in Day 2!`)}
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