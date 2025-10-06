import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export default function Navbar({ showBackButton = false, backTo = '/' }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  return (
    <nav className="glass border-b border-white/20 mb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left: Logo/Brand */}
          <div className="flex items-center gap-4">
            {showBackButton && (
              <button
                onClick={() => navigate(backTo)}
                className="px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition border border-white/20"
              >
                ← Back
              </button>
            )}
            <button
              onClick={() => navigate('/')}
              className="text-2xl font-bold text-white hover:text-white/80 transition"
            >
              MindMorph
            </button>
          </div>

          {/* Right: User info & Logout */}
          <div className="flex items-center gap-4">
            <span className="text-white/80 hidden sm:block">
              {user?.name}
            </span>
            <button
              onClick={logout}
              className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition border border-white/20"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}