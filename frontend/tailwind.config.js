/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          from: '#8B5CF6',
          to: '#3B82F6',
        },
        mbti: {
          introvert: '#6366F1',
          extravert: '#F43F5E',
          intuition: '#A855F7',
          sensing: '#F59E0B',
          thinking: '#10B981',
          feeling: '#EC4899',
          judging: '#F97316',
          perceiving: '#06B6D4',
        }
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)',
        'gradient-hero': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(139, 92, 246, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(139, 92, 246, 0.8)' },
        }
      }
    },
  },
  plugins: [],
}