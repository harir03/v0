'use client'

import { motion } from 'framer-motion'

export default function HeroSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
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
    <section className="relative min-h-screen flex items-center justify-center bg-white overflow-hidden">
      {/* Simple gradient background */}
      <div className="absolute inset-0 bg-gradient-to-b from-white via-white to-gray-50"></div>
      
      {/* Content */}
      <motion.div
        className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight tracking-tight text-gray-900">
            Build Agents That
            <br />
            <span className="text-gray-600">Think, Create, and Code</span>
          </h1>
        </motion.div>

        <motion.p
          className="text-xl md:text-2xl text-gray-600 mb-12 max-w-4xl mx-auto leading-relaxed font-normal"
          variants={itemVariants}
        >
          Aether Agents is the no-code/low-code platform that empowers anyone to build 
          sophisticated AI agents. Move beyond simple automation with agentic coding, 
          revolutionary prompt-to-interface builders, and now featuring{' '}
          <span className="font-semibold text-gray-900">Vivid AI</span>{' '}
          - the ultimate AI-powered video editing platform.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
          variants={itemVariants}
        >
          <button className="bg-gray-900 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-800 transition-colors duration-200 min-w-[200px]">
            Start Building Free
          </button>
          <a 
            href="/vivid-ai"
            className="bg-accent text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-600 transition-colors duration-200 min-w-[200px]"
          >
            Try Vivid AI ✨
          </a>
          <button className="border border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-50 transition-colors duration-200 min-w-[200px]">
            Watch Demo
          </button>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto"
          variants={itemVariants}
        >
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">2M+</div>
            <div className="text-sm text-gray-600 font-medium">Tasks Automated</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">500+</div>
            <div className="text-sm text-gray-600 font-medium">Active Agents</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">99.9%</div>
            <div className="text-sm text-gray-600 font-medium">Uptime</div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  )
}