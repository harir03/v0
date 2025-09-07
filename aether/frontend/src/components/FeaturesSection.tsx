'use client'

import { motion, useScroll, useTransform } from 'framer-motion'
import { Code, Zap, Users, Shield, Brain, Workflow } from 'lucide-react'
import { useRef } from 'react'

export default function FeaturesSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  })
  
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.8, 1, 1, 0.8])

  const features = [
    {
      icon: Brain,
      title: "Instant Interface Builder",
      description: "Describe your agent's UI in plain English and watch it come to life. Our v0-style builder generates interactive interfaces in real-time.",
      gradient: "from-primary to-secondary"
    },
    {
      icon: Code,
      title: "Agentic Coding",
      description: "Agents that can read, write, and debug code. From reviewing pull requests to scaffolding entire projects, your agents are true developers.",
      gradient: "from-secondary to-muted"
    },
    {
      icon: Users,
      title: "Multi-Agent Collaboration",
      description: "Create agent societies where specialized agents delegate tasks to each other, forming sophisticated workflows and teams.",
      gradient: "from-muted to-inspiration-olive"
    },
    {
      icon: Workflow,
      title: "No-Code Workflows",
      description: "Build complex automation workflows without writing a single line of code. Drag, drop, and connect your way to productivity.",
      gradient: "from-inspiration-olive to-primary"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Powered by the latest AI models with optimized infrastructure. Your agents respond in seconds, not minutes.",
      gradient: "from-primary to-muted"
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "SOC 2 compliant with HIPAA options. On-premise deployment available. Your data stays secure and under your control.",
      gradient: "from-secondary to-inspiration-olive"
    },
  ]

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
    hidden: { y: 40, opacity: 0, scale: 0.9 },
    visible: {
      y: 0,
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.8,
        ease: [0.6, -0.05, 0.01, 0.99],
      },
    },
  }

  return (
    <section ref={ref} id="features" className="py-32 bg-gradient-to-b from-background to-inspiration-light relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-inspiration-beige rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-border rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDelay: '3s' }}></div>
      </div>

      <motion.div 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10"
        style={{ opacity, scale }}
      >
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.6, -0.05, 0.01, 0.99] }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-primary leading-tight tracking-tighter">
            Powerful Features
            <br />
            <span className="bg-gradient-to-r from-secondary via-muted to-inspiration-olive bg-clip-text text-transparent">
              Built for Scale
            </span>
          </h2>
          <p className="text-xl md:text-2xl text-muted max-w-4xl mx-auto leading-relaxed font-light">
            Everything you need to build, deploy, and manage AI agents that work 
            like human employees but never take a break.
          </p>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              variants={itemVariants}
              className="group"
            >
              <motion.div 
                className="bg-card/60 backdrop-blur-lg p-10 rounded-3xl border border-border/50 h-full hover:shadow-2xl transition-all duration-500 relative overflow-hidden hover:border-inspiration-beige hover:bg-card/80"
                whileHover={{ scale: 1.05, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                {/* Gradient overlay on hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-transparent via-inspiration-beige/5 to-inspiration-olive/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                
                <motion.div 
                  className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center mb-8 shadow-lg group-hover:shadow-xl transition-all duration-300`}
                  whileHover={{ rotate: 5, scale: 1.1 }}
                  transition={{ duration: 0.3 }}
                >
                  <feature.icon className="h-8 w-8 text-background" />
                </motion.div>
                
                <h3 className="text-2xl font-bold text-primary mb-6 group-hover:text-secondary transition-colors duration-300">
                  {feature.title}
                </h3>
                
                <p className="text-muted leading-relaxed text-lg group-hover:text-primary transition-colors duration-300">
                  {feature.description}
                </p>

                {/* Subtle shine effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              </motion.div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="text-center mt-20"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: [0.6, -0.05, 0.01, 0.99] }}
          viewport={{ once: true }}
        >
          <motion.button 
            className="group bg-gradient-to-r from-primary to-secondary text-background px-12 py-6 rounded-2xl font-bold text-xl hover:from-secondary hover:to-primary transition-all duration-500 shadow-2xl hover:shadow-3xl relative overflow-hidden"
            whileHover={{ scale: 1.05, y: -3 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="relative z-10">Explore All Features</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          </motion.button>
        </motion.div>
      </motion.div>
    </section>
  )
}