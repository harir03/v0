'use client'

import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

export default function HeroSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  })
  
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"])
  const opacity = useTransform(scrollYProgress, [0, 1], [1, 0])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.3,
      },
    },
  }

  const itemVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.8,
        ease: [0.6, -0.05, 0.01, 0.99],
      },
    },
  }

  const titleVariants = {
    hidden: { y: 40, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 1,
        ease: [0.6, -0.05, 0.01, 0.99],
      },
    },
  }

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center bg-background overflow-hidden">
      {/* Enhanced gradient background with parallax */}
      <motion.div 
        className="absolute inset-0 bg-gradient-to-br from-background via-inspiration-light to-inspiration-beige"
        style={{ y }}
      />
      
      {/* Subtle animated background elements */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-20 left-10 w-72 h-72 bg-inspiration-beige rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-inspiration-olive rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-border rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDelay: '4s' }}></div>
      </div>
      
      {/* Content */}
      <motion.div
        className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        style={{ opacity }}
      >
        <motion.div variants={titleVariants}>
          <h1 className="text-7xl md:text-8xl lg:text-9xl font-extrabold mb-8 leading-[0.9] tracking-tighter text-primary">
            Build Agents That
            <br />
            <span className="bg-gradient-to-r from-secondary via-muted to-inspiration-olive bg-clip-text text-transparent">
              Think, Create, and Code
            </span>
          </h1>
        </motion.div>

        <motion.p
          className="text-xl md:text-2xl lg:text-3xl text-muted mb-20 max-w-5xl mx-auto leading-relaxed font-light"
          variants={itemVariants}
        >
          Aether Agents is the no-code/low-code platform that empowers anyone to build 
          sophisticated AI agents. Move beyond simple automation with agentic coding, 
          revolutionary prompt-to-interface builders, and now featuring{' '}
          <span className="font-semibold text-primary bg-inspiration-beige px-2 py-1 rounded-lg">Vivid AI</span>{' '}
          - the ultimate AI-powered video editing platform.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-8 justify-center items-center mb-24"
          variants={itemVariants}
        >
          <motion.button 
            className="group bg-primary text-background px-12 py-6 rounded-2xl font-semibold text-xl hover:bg-secondary transition-all duration-500 min-w-[250px] shadow-2xl hover:shadow-3xl relative overflow-hidden"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="relative z-10">Start Building Free</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          </motion.button>
          
          <motion.a 
            href="/vivid-ai"
            className="group bg-gradient-to-r from-muted to-inspiration-olive text-background px-12 py-6 rounded-2xl font-semibold text-xl hover:from-inspiration-olive hover:to-muted transition-all duration-500 min-w-[250px] shadow-2xl hover:shadow-3xl relative overflow-hidden"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="relative z-10">Try Vivid AI ✨</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          </motion.a>
          
          <motion.button 
            className="group border-3 border-border bg-card/80 backdrop-blur-sm text-primary px-12 py-6 rounded-2xl font-semibold text-xl hover:bg-background hover:border-muted hover:shadow-2xl transition-all duration-500 min-w-[250px] relative overflow-hidden"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="relative z-10">Watch Demo</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-inspiration-beige/30 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          </motion.button>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
          variants={itemVariants}
        >
          {[
            { number: "2M+", label: "Tasks Automated", delay: 0 },
            { number: "500+", label: "Active Agents", delay: 0.2 },
            { number: "99.9%", label: "Uptime", delay: 0.4 }
          ].map((stat, index) => (
            <motion.div 
              key={stat.label}
              className="group text-center bg-card/60 backdrop-blur-lg rounded-3xl p-10 shadow-xl hover:shadow-2xl transition-all duration-500 border border-border/50 hover:border-inspiration-beige hover:bg-card/80"
              whileHover={{ scale: 1.05, y: -5 }}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ 
                duration: 0.8, 
                delay: 1.2 + stat.delay,
                ease: [0.6, -0.05, 0.01, 0.99]
              }}
            >
              <div className="text-6xl lg:text-7xl font-black text-primary mb-4 group-hover:text-secondary transition-colors duration-300">
                {stat.number}
              </div>
              <div className="text-lg text-muted font-medium tracking-wide group-hover:text-primary transition-colors duration-300">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  )
}