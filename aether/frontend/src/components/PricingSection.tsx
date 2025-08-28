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
    <section id="pricing" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
            Simple Pricing
            <br />
            <span className="text-gray-600">Scale as You Grow</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Start free and upgrade when you need more power. All plans include our core features with transparent pricing and no hidden fees.
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
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gray-900 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className={`bg-white rounded-xl p-8 h-full border ${plan.popular ? 'border-gray-900 shadow-lg' : 'border-gray-200'} hover:shadow-lg transition-shadow duration-200`}>
                <div className="text-center mb-8">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <plan.icon className="h-6 w-6 text-gray-700" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 text-sm mb-4">{plan.description}</p>
                  <div className="text-center">
                    <span className="text-3xl font-bold text-gray-900">{plan.price}</span>
                    {plan.period && <span className="text-gray-600">{plan.period}</span>}
                  </div>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start space-x-3">
                      <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button className={`w-full py-3 px-6 rounded-lg font-medium transition-colors duration-200 ${
                  plan.popular 
                    ? 'bg-gray-900 text-white hover:bg-gray-800' 
                    : plan.name === 'Enterprise'
                    ? 'border border-gray-300 text-gray-700 hover:bg-gray-50'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}>
                  {plan.name === 'Enterprise' ? 'Contact Sales' : plan.name === 'Hobbyist' ? 'Get Started Free' : 'Start Free Trial'}
                </button>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="mt-16 text-center space-y-4"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
        >
          <p className="text-gray-600">
            All plans include 14-day free trial • No credit card required • Cancel anytime
          </p>
          <div className="flex justify-center space-x-8 text-sm text-gray-500">
            <span className="flex items-center space-x-1">
              <Check className="h-4 w-4 text-green-500" />
              <span>99.9% SLA</span>
            </span>
            <span className="flex items-center space-x-1">
              <Check className="h-4 w-4 text-green-500" />
              <span>24/7 Support</span>
            </span>
            <span className="flex items-center space-x-1">
              <Check className="h-4 w-4 text-green-500" />
              <span>SOC 2 Compliant</span>
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  )
}