# Aether Agents Frontend

This is the frontend application for Aether Agents, built with Next.js 14, React, TypeScript, and Tailwind CSS.

## Features

- **Modern Stack**: Next.js 14 with App Router, React 18, TypeScript
- **Styling**: Tailwind CSS with custom "Digital Synapse" theme
- **Animations**: Framer Motion for smooth animations and transitions
- **3D Graphics**: Three.js for neural network background animations
- **Dark Mode**: Beautiful dark theme with electric blue, purple, and neon green accents
- **Responsive**: Mobile-first design that works on all devices

## Design Theme

The "Digital Synapse" theme features:
- **Base Color**: Deep navy/charcoal (#0a0f1f)
- **Accent Colors**: Electric blue (#00BFFF), purple (#8A2BE2), neon green (#39FF14)
- **Typography**: Inter font family for modern, tech-forward feel
- **Animations**: Neural network backgrounds, text reveal effects, and hover interactions

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx      # Root layout with global styles
│   ├── page.tsx        # Home page
│   └── globals.css     # Global CSS and animations
├── components/         # React components
│   ├── Navigation.tsx  # Header navigation
│   ├── HeroSection.tsx # Main hero with animations
│   ├── FeaturesSection.tsx    # Feature showcase
│   ├── InteractiveDemo.tsx    # Live demo component
│   ├── PricingSection.tsx     # Pricing tiers
│   ├── Footer.tsx      # Footer
│   └── NeuralNetworkAnimation.tsx  # Three.js background
└── lib/
    └── utils.ts        # Utility functions
```

## Key Components

### HeroSection
- Animated headline with text reveal effects
- Neural network background animation
- Interactive stats and CTAs

### InteractiveDemo
- Live demonstration of the "Instant Interface" builder
- Real-time UI generation simulation
- Interactive prompt examples

### NeuralNetworkAnimation
- Three.js canvas animation
- Mouse-interactive neural network
- Flowing data visualization

### PricingSection
- Four-tier pricing model (Hobbyist, Startup, Scale-Up, Enterprise)
- Feature comparison
- Gradient cards with hover effects

## Build Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Technologies Used

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Three.js** - 3D graphics library
- **Lucide React** - Icon library