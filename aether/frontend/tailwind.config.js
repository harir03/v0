/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Enhanced Futuristic theme colors
        'aether-dark': '#000814',
        'aether-darker': '#001122',
        'aether-blue': '#00d9ff',
        'aether-purple': '#6366f1',
        'aether-green': '#64748b', // Changed from green to grey
        'aether-orange': '#ff6b35',
        'aether-cyan': '#06ffa5',
        'aether-pink': '#ec4899',
        'aether-gold': '#fbbf24',
        'aether-gray': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#94a3b8',
          400: '#64748b',
          500: '#475569',
          600: '#334155',
          700: '#1e293b',
          800: '#0f172a',
          900: '#020617',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'neural-pattern': "url('/neural-bg.svg')",
        'gradient-mesh': 'radial-gradient(at 40% 20%, #00d9ff 0%, transparent 50%), radial-gradient(at 80% 0%, #6366f1 0%, transparent 50%), radial-gradient(at 0% 50%, #ec4899 0%, transparent 50%)',
        'gradient-cyber': 'linear-gradient(135deg, #000814 0%, #001122 50%, #000814 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'gradient-shift': 'gradient-shift 4s ease-in-out infinite',
        'fade-in-up': 'fade-in-up 0.6s ease-out forwards',
        'fade-in-down': 'fade-in-down 0.6s ease-out forwards',
        'scale-in': 'scale-in 0.3s ease-out forwards',
        'slide-in-left': 'slide-in-left 0.6s ease-out forwards',
        'slide-in-right': 'slide-in-right 0.6s ease-out forwards',
        'ripple': 'ripple 0.6s ease-out',
        'cyber-glow': 'cyber-glow 3s ease-in-out infinite alternate',
        'data-flow': 'data-flow 2s linear infinite',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'satoshi': ['Satoshi', 'sans-serif'],
      },
      keyframes: {
        glow: {
          '0%': { 
            boxShadow: '0 0 5px #00d9ff, 0 0 10px #00d9ff, 0 0 15px #00d9ff'
          },
          '100%': { 
            boxShadow: '0 0 10px #00d9ff, 0 0 20px #00d9ff, 0 0 30px #00d9ff'
          }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        'gradient-shift': {
          '0%, 100%': { 
            backgroundPosition: '0% 50%' 
          },
          '50%': { 
            backgroundPosition: '100% 50%' 
          }
        },
        'fade-in-up': {
          '0%': {
            opacity: '0',
            transform: 'translateY(30px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        'fade-in-down': {
          '0%': {
            opacity: '0',
            transform: 'translateY(-30px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        'scale-in': {
          '0%': {
            opacity: '0',
            transform: 'scale(0.9)'
          },
          '100%': {
            opacity: '1',
            transform: 'scale(1)'
          }
        },
        'slide-in-left': {
          '0%': {
            opacity: '0',
            transform: 'translateX(-50px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateX(0)'
          }
        },
        'slide-in-right': {
          '0%': {
            opacity: '0',
            transform: 'translateX(50px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateX(0)'
          }
        },
        'ripple': {
          '0%': {
            transform: 'scale(0)',
            opacity: '1'
          },
          '100%': {
            transform: 'scale(4)',
            opacity: '0'
          }
        },
        'cyber-glow': {
          '0%': { 
            boxShadow: '0 0 5px #00d9ff, 0 0 10px #00d9ff, 0 0 15px #00d9ff, inset 0 0 5px #00d9ff'
          },
          '100%': { 
            boxShadow: '0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1, inset 0 0 10px #6366f1'
          }
        },
        'data-flow': {
          '0%': {
            transform: 'translateX(-100%)'
          },
          '100%': {
            transform: 'translateX(100%)'
          }
        }
      }
    },
  },
  plugins: [],
}