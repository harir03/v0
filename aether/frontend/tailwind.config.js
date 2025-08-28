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
        // Sophisticated color palette from inspiration image
        'primary': '#262626', // Dark charcoal for text
        'secondary': '#595959', // Medium grey for secondary text
        'muted': '#888C79', // Olive grey for muted elements
        'border': '#D9D3C7', // Warm beige for borders
        'background': '#F0F1F2', // Light off-white background
        'card': '#ffffff', // Pure white for cards
        'accent': '#262626', // Dark charcoal for accents
        'success': '#888C79', // Olive grey for success states
        
        // Sophisticated grey palette from inspiration
        'inspiration': {
          'light': '#F0F1F2',  // Light off-white
          'beige': '#D9D3C7',  // Warm beige  
          'olive': '#888C79',  // Olive grey
          'medium': '#595959', // Medium grey
          'dark': '#262626',   // Dark charcoal
        },
        
        // Legacy compatibility with refined values
        'aether-dark': '#262626',
        'aether-blue': '#595959',
        'aether-purple': '#888C79',
        'aether-green': '#888C79',
        'aether-light': '#F0F1F2',
        'aether-gray': {
          50: '#F0F1F2',
          100: '#E8E9EA',
          200: '#D9D3C7',
          300: '#C4C0B8',
          400: '#888C79',
          500: '#737370',
          600: '#595959',
          700: '#454545',
          800: '#262626',
          900: '#1A1A1A',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      animation: {
        'fade-in': 'fade-in 0.5s ease-out forwards',
        'slide-up': 'slide-up 0.6s ease-out forwards',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'satoshi': ['Satoshi', 'sans-serif'],
      },
      boxShadow: {
        '3xl': '0 35px 60px -12px rgba(0, 0, 0, 0.25)',
        'glow': '0 0 20px rgba(38, 38, 38, 0.15)',
        'glow-lg': '0 0 40px rgba(38, 38, 38, 0.2)',
      },
      borderWidth: {
        '3': '3px',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        }
      }
    },
  },
  plugins: [],
}