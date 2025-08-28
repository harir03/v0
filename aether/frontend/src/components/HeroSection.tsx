'use client'

import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import NeuralNetworkAnimation from './NeuralNetworkAnimation'

export default function HeroSection() {
  const titleRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    // Text reveal animation
    if (titleRef.current) {
      const words = titleRef.current.textContent?.split(' ') || []
      titleRef.current.innerHTML = words
        .map((word, index) => `<span class="inline-block" style="animation-delay: ${index * 0.1}s">${word}</span>`)
        .join(' ')
      
      titleRef.current.classList.add('text-reveal')
    }
  }, [])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: "easeOut",
      },
    },
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-aether-dark">
      {/* Neural Network Background */}
      <div className="absolute inset-0 z-0">
        <NeuralNetworkAnimation />
      </div>
      
      {/* Background Grid */}
      <div className="absolute inset-0 bg-grid opacity-20"></div>
      
      {/* Content */}
      <motion.div
        className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <h1
            ref={titleRef}
            className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 leading-tight"
          >
            <span className="gradient-text">Build Agents That</span>
            <br />
            <span className="text-white">Think, Create, and Code</span>
          </h1>
        </motion.div>

        <motion.p
          className="text-xl md:text-2xl text-aether-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed"
          variants={itemVariants}
        >
          Aether Agents is the no-code/low-code platform that empowers anyone to build 
          sophisticated AI agents. Move beyond simple automation with agentic coding, 
          revolutionary prompt-to-interface builders, and now featuring <strong className="text-purple-400">Vivid AI</strong> - 
          the ultimate AI-powered video editing platform.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
          variants={itemVariants}
        >
          <button className="btn-ripple bg-gradient-to-r from-aether-blue to-aether-purple text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-2xl hover:shadow-aether-blue/50 transition-all duration-300 transform hover:scale-105 animate-cyber-glow neon-glow">
            Start Building Free
          </button>
          <a 
            href="/vivid-ai"
            className="btn-ripple bg-gradient-to-r from-aether-purple to-aether-pink text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-2xl hover:shadow-aether-purple/50 transition-all duration-300 transform hover:scale-105 neon-glow"
          >
            Try Vivid AI ✨
          </a>
          <button className="btn-ripple gradient-border border-2 border-aether-blue text-aether-blue px-8 py-4 rounded-lg font-semibold text-lg hover:bg-aether-blue hover:text-white transition-all duration-300 transform hover:scale-105 hover:neon-glow">
            Watch Demo
          </button>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
          variants={itemVariants}
        >
          <div className="cyber-card p-6 data-stream group">
            <div className="text-3xl font-bold text-aether-cyan mb-2 transition-all duration-300 group-hover:scale-110">2M+</div>
            <div className="text-aether-gray-300">Tasks Automated</div>
          </div>
          <div className="cyber-card p-6 data-stream group">
            <div className="text-3xl font-bold text-aether-blue mb-2 transition-all duration-300 group-hover:scale-110">500+</div>
            <div className="text-aether-gray-300">Active Agents</div>
          </div>
          <div className="cyber-card p-6 data-stream group">
            <div className="text-3xl font-bold text-aether-purple mb-2 transition-all duration-300 group-hover:scale-110">99.9%</div>
            <div className="text-aether-gray-300">Uptime</div>
          </div>
        </motion.div>
      </motion.div>

      {/* Enhanced scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 2 }}
      >
        <div className="w-6 h-10 border-2 border-aether-blue rounded-full flex justify-center neon-glow">
          <div className="w-1 h-3 bg-gradient-to-b from-aether-cyan to-aether-blue rounded-full mt-2 animate-bounce"></div>
        </div>
      </motion.div>
    </section>
  )
}