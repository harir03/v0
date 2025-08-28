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
        // Digital Synapse theme colors
        'aether-dark': '#0a0f1f',
        'aether-blue': '#00BFFF',
        'aether-purple': '#8A2BE2',
        'aether-green': '#39FF14',
        'aether-gray': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'neural-pattern': "url('/neural-bg.svg')",
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'spin-slow': 'spin 8s linear infinite',
        'spin-very-slow': 'spin 20s linear infinite',
        'breathing': 'breathing 3s ease-in-out infinite',
        'kinetic-reveal': 'kinetic-reveal 1s ease-out forwards',
        'counter-bounce': 'counter-bounce 1s ease-out forwards',
        'wave': 'wave 3s ease-in-out infinite',
        'wave-delayed': 'wave 3s ease-in-out infinite 1s',
        'card-float': 'card-float 6s ease-in-out infinite',
        'card-bounce': 'card-bounce 0.6s ease-out forwards',
        'particle-drift': 'particle-drift 12s linear infinite',
        'draw-line': 'draw-line 2s ease-in-out forwards',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'satoshi': ['Satoshi', 'sans-serif'],
      },
      keyframes: {
        glow: {
          '0%': { 
            boxShadow: '0 0 5px #00BFFF, 0 0 10px #00BFFF, 0 0 15px #00BFFF'
          },
          '100%': { 
            boxShadow: '0 0 10px #00BFFF, 0 0 20px #00BFFF, 0 0 30px #00BFFF'
          }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        breathing: {
          '0%, 100%': { transform: 'scale(1)', opacity: '1' },
          '50%': { transform: 'scale(1.05)', opacity: '0.8' }
        },
        'kinetic-reveal': {
          '0%': { opacity: '0', transform: 'translateY(30px) rotateX(90deg)' },
          '100%': { opacity: '1', transform: 'translateY(0) rotateX(0)' }
        },
        'counter-bounce': {
          '0%': { opacity: '0', transform: 'translateY(50px) scale(0.3)' },
          '60%': { opacity: '1', transform: 'translateY(-10px) scale(1.1)' },
          '100%': { opacity: '1', transform: 'translateY(0) scale(1)' }
        },
        wave: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(10px)' }
        },
        'card-float': {
          '0%, 100%': { transform: 'translateY(0px) rotateX(0deg)' },
          '50%': { transform: 'translateY(-10px) rotateX(5deg)' }
        },
        'card-bounce': {
          '0%': { opacity: '0', transform: 'scale(0.8) translateY(30px)' },
          '60%': { transform: 'scale(1.05) translateY(-5px)' },
          '100%': { opacity: '1', transform: 'scale(1) translateY(0)' }
        },
        'particle-drift': {
          '0%': { transform: 'translate(0, 100vh) scale(0)', opacity: '0' },
          '10%': { opacity: '1' },
          '90%': { opacity: '1' },
          '100%': { transform: 'translate(0, -100vh) scale(1)', opacity: '0' }
        },
        'draw-line': {
          '0%': { strokeDasharray: '0 1000' },
          '100%': { strokeDasharray: '1000 0' }
        }
      }
    },
  },
  plugins: [],
}