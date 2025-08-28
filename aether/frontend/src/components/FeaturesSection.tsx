'use client'

import { motion } from 'framer-motion'
import { Code, Zap, Users, Shield, Brain, Workflow } from 'lucide-react'

export default function FeaturesSection() {
  const features = [
    {
      icon: Brain,
      title: "Instant Interface Builder",
      description: "Describe your agent's UI in plain English and watch it come to life. Our v0-style builder generates interactive interfaces in real-time.",
      color: "text-aether-blue",
      bgColor: "bg-aether-blue/10",
    },
    {
      icon: Code,
      title: "Agentic Coding",
      description: "Agents that can read, write, and debug code. From reviewing pull requests to scaffolding entire projects, your agents are true developers.",
      color: "text-aether-purple",
      bgColor: "bg-aether-purple/10",
    },
    {
      icon: Users,
      title: "Multi-Agent Collaboration",
      description: "Create agent societies where specialized agents delegate tasks to each other, forming sophisticated workflows and teams.",
      color: "text-aether-gray-400",
      bgColor: "bg-aether-gray-400/10",
    },
    {
      icon: Workflow,
      title: "No-Code Workflows",
      description: "Build complex automation workflows without writing a single line of code. Drag, drop, and connect your way to productivity.",
      color: "text-aether-blue",
      bgColor: "bg-aether-blue/10",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Powered by the latest AI models with optimized infrastructure. Your agents respond in seconds, not minutes.",
      color: "text-aether-gray-400",
      bgColor: "bg-aether-gray-400/10",
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "SOC 2 compliant with HIPAA options. On-premise deployment available. Your data stays secure and under your control.",
      color: "text-aether-purple",
      bgColor: "bg-aether-purple/10",
    },
  ]

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
    <section id="features" className="py-24 bg-aether-dark relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid opacity-5"></div>
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">Powerful Features</span>
            <br />
            <span className="text-white">Built for Scale</span>
          </h2>
          <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto">
            Everything you need to build, deploy, and manage AI agents that work 
            like human employees but never take a break.
          </p>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              variants={itemVariants}
              className="group relative"
            >
              <div className="cyber-card p-8 h-full group-hover:shadow-2xl group-hover:shadow-aether-blue/20 data-stream">
                <div className={`${feature.bgColor} w-16 h-16 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300 neon-glow`}>
                  <feature.icon className={`h-8 w-8 ${feature.color} transition-all duration-300 group-hover:animate-pulse`} />
                </div>
                
                <h3 className="text-xl font-semibold text-white mb-4 group-hover:gradient-text transition-all duration-300">
                  {feature.title}
                </h3>
                
                <p className="text-aether-gray-300 leading-relaxed">
                  {feature.description}
                </p>

                {/* Enhanced hover effect overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-aether-cyan/5 via-aether-blue/5 to-aether-purple/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Call to Action */}
        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
        >
          <button className="btn-ripple bg-gradient-to-r from-aether-blue to-aether-purple text-white px-8 py-4 rounded-lg font-semibold text-lg hover:shadow-2xl hover:shadow-aether-blue/50 transition-all duration-300 transform hover:scale-105 neon-glow">
            Explore All Features
          </button>
        </motion.div>
      </div>
    </section>
  )
}