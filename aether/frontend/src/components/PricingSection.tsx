'use client'

import { motion } from 'framer-motion'
import { Check, Zap, Star, Crown } from 'lucide-react'

export default function PricingSection() {
  const plans = [
    {
      name: "Hobbyist",
      price: "Free",
      description: "Perfect for individuals exploring agentic automation",
      icon: Zap,
      color: "border-aether-gray-600",
      buttonColor: "bg-aether-gray-700 hover:bg-aether-gray-600",
      popular: false,
      features: [
        "1 User Seat",
        "Up to 2 Active Agents",
        "500 Tasks/Month",
        "Basic Integrations (Gmail, Slack, Calendar)",
        "Standard Code Completion",
        "Community Support"
      ]
    },
    {
      name: "Startup",
      price: "$49",
      period: "/month",
      description: "For startups and small teams building their core operations",
      icon: Star,
      color: "border-aether-blue",
      buttonColor: "bg-gradient-to-r from-aether-blue to-aether-purple hover:shadow-lg hover:shadow-aether-blue/50",
      popular: true,
      features: [
        "Up to 3 User Seats",
        "Up to 10 Active Agents",
        "5,000 Tasks/Month",
        "Agentic Coding Capabilities",
        "Premium Integrations (HubSpot, Salesforce, Notion)",
        "Custom Knowledge Base",
        "Priority Support"
      ]
    },
    {
      name: "Scale-Up",
      price: "$199",
      period: "/month",
      description: "For growing businesses that need advanced collaboration",
      icon: Crown,
      color: "border-aether-purple",
      buttonColor: "bg-gradient-to-r from-aether-purple to-aether-blue hover:shadow-lg hover:shadow-aether-purple/50",
      popular: false,
      features: [
        "Up to 10 User Seats",
        "Unlimited Agents",
        "50,000 Tasks/Month",
        "Multi-Agent Collaboration",
        "Autopilot Mode (Cloud VM Access)",
        "Voice Capabilities (Twilio Integration)",
        "Advanced Analytics",
        "Dedicated Support"
      ]
    },
    {
      name: "Enterprise",
      price: "Custom",
      description: "For large organizations requiring maximum security and scale",
      icon: Crown,
      color: "border-aether-gray-400",
      buttonColor: "bg-gradient-to-r from-aether-gray-400 to-aether-blue hover:shadow-lg hover:shadow-aether-gray-400/50",
      popular: false,
      features: [
        "Unlimited User Seats & Tasks",
        "SOC 2 & HIPAA Compliance",
        "On-Premise Deployment",
        "Custom AI Model Fine-tuning",
        "Dedicated Solutions Engineer",
        "24/7 Premium Support",
        "SLA Guarantees",
        "Custom Integrations"
      ]
    }
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
    <section id="pricing" className="py-24 bg-aether-dark relative overflow-hidden">
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
            <span className="gradient-text">Simple Pricing</span>
            <br />
            <span className="text-white">Scale as You Grow</span>
          </h2>
          <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto">
            Start free and upgrade when you need more power. All plans include our core features 
            with transparent pricing and no hidden fees.
          </p>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              variants={itemVariants}
              className={`relative bg-aether-gray-900/50 backdrop-blur-sm border-2 ${plan.color} rounded-xl p-8 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 ${plan.popular ? 'ring-2 ring-aether-blue ring-opacity-50' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-aether-blue to-aether-purple text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-6">
                <div className="flex justify-center mb-4">
                  <div className={`p-3 rounded-lg ${plan.color === 'border-aether-blue' ? 'bg-aether-blue/10' : plan.color === 'border-aether-purple' ? 'bg-aether-purple/10' : plan.color === 'border-aether-gray-400' ? 'bg-aether-gray-400/10' : 'bg-aether-gray-700'}`}>
                    <plan.icon className={`h-8 w-8 ${plan.color === 'border-aether-blue' ? 'text-aether-blue' : plan.color === 'border-aether-purple' ? 'text-aether-purple' : plan.color === 'border-aether-gray-400' ? 'text-aether-gray-400' : 'text-aether-gray-300'}`} />
                  </div>
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-aether-gray-400 text-sm mb-4">{plan.description}</p>
                
                <div className="mb-6">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  {plan.period && <span className="text-aether-gray-400">{plan.period}</span>}
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start space-x-3">
                    <Check className="h-5 w-5 text-aether-gray-400 mt-0.5 flex-shrink-0" />
                    <span className="text-aether-gray-300 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <button className={`w-full ${plan.buttonColor} text-white py-3 px-6 rounded-lg font-medium transition-all duration-300 transform hover:scale-105`}>
                {plan.name === 'Enterprise' ? 'Contact Sales' : plan.name === 'Hobbyist' ? 'Get Started Free' : 'Start Free Trial'}
              </button>
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
          <p className="text-aether-gray-400 mb-4">
            All plans include 14-day free trial • No credit card required • Cancel anytime
          </p>
          <div className="flex justify-center space-x-8 text-sm text-aether-gray-500">
            <span>✓ 99.9% SLA</span>
            <span>✓ 24/7 Support</span>
            <span>✓ SOC 2 Compliant</span>
          </div>
        </motion.div>
      </div>
    </section>
  )
}