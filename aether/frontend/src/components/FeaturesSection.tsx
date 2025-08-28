'use client'

import { motion } from 'framer-motion'
import { Code, Zap, Users, Shield, Brain, Workflow } from 'lucide-react'

export default function FeaturesSection() {
  const features = [
    {
      icon: Brain,
      title: "Instant Interface Builder",
      description: "Describe your agent's UI in plain English and watch it come to life. Our v0-style builder generates interactive interfaces in real-time.",
    },
    {
      icon: Code,
      title: "Agentic Coding",
      description: "Agents that can read, write, and debug code. From reviewing pull requests to scaffolding entire projects, your agents are true developers.",
    },
    {
      icon: Users,
      title: "Multi-Agent Collaboration",
      description: "Create agent societies where specialized agents delegate tasks to each other, forming sophisticated workflows and teams.",
    },
    {
      icon: Workflow,
      title: "No-Code Workflows",
      description: "Build complex automation workflows without writing a single line of code. Drag, drop, and connect your way to productivity.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Powered by the latest AI models with optimized infrastructure. Your agents respond in seconds, not minutes.",
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "SOC 2 compliant with HIPAA options. On-premise deployment available. Your data stays secure and under your control.",
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
    <section id="features" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
            Powerful Features
            <br />
            <span className="text-gray-600">Built for Scale</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
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
              className="group"
            >
              <div className="bg-white p-8 rounded-xl border border-gray-200 h-full hover:shadow-lg hover:border-gray-300 transition-all duration-200">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-6 group-hover:bg-gray-200 transition-colors duration-200">
                  <feature.icon className="h-6 w-6 text-gray-700" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
        >
          <button className="bg-gray-900 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-800 transition-colors duration-200">
            Explore All Features
          </button>
        </motion.div>
      </div>
    </section>
  )
}