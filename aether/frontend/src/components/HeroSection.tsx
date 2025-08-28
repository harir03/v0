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
    <section className="relative min-h-screen flex items-center justify-center bg-background overflow-hidden">
      {/* Sophisticated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-inspiration-light to-inspiration-beige"></div>
      
      {/* Content */}
      <motion.div
        className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold mb-8 leading-tight tracking-tight text-primary">
            Build Agents That
            <br />
            <span className="text-secondary">Think, Create, and Code</span>
          </h1>
        </motion.div>

        <motion.p
          className="text-xl md:text-2xl text-muted mb-16 max-w-4xl mx-auto leading-relaxed font-light"
          variants={itemVariants}
        >
          Aether Agents is the no-code/low-code platform that empowers anyone to build 
          sophisticated AI agents. Move beyond simple automation with agentic coding, 
          revolutionary prompt-to-interface builders, and now featuring{' '}
          <span className="font-medium text-primary">Vivid AI</span>{' '}
          - the ultimate AI-powered video editing platform.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-20"
          variants={itemVariants}
        >
          <button className="bg-primary text-background px-10 py-5 rounded-xl font-medium text-lg hover:bg-secondary transition-all duration-300 min-w-[220px] shadow-lg hover:shadow-xl">
            Start Building Free
          </button>
          <a 
            href="/vivid-ai"
            className="bg-muted text-background px-10 py-5 rounded-xl font-medium text-lg hover:bg-inspiration-olive transition-all duration-300 min-w-[220px] shadow-lg hover:shadow-xl"
          >
            Try Vivid AI ✨
          </a>
          <button className="border-2 border-border bg-card text-primary px-10 py-5 rounded-xl font-medium text-lg hover:bg-background hover:border-muted transition-all duration-300 min-w-[220px] shadow-lg hover:shadow-xl">
            Watch Demo
          </button>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-3xl mx-auto"
          variants={itemVariants}
        >
          <div className="text-center bg-card rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="text-5xl font-bold text-primary mb-3">2M+</div>
            <div className="text-base text-muted font-medium tracking-wide">Tasks Automated</div>
          </div>
          <div className="text-center bg-card rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="text-5xl font-bold text-primary mb-3">500+</div>
            <div className="text-base text-muted font-medium tracking-wide">Active Agents</div>
          </div>
          <div className="text-center bg-card rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="text-5xl font-bold text-primary mb-3">99.9%</div>
            <div className="text-base text-muted font-medium tracking-wide">Uptime</div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  )
}