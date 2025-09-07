'use client'

import { motion, useScroll, useTransform } from 'framer-motion'
import { Check, Zap, Star, Crown } from 'lucide-react'
import { useRef } from 'react'

export default function PricingSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  })
  
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.8, 1, 1, 0.8])

  const plans = [
    {
      name: "Hobbyist",
      price: "Free",
      description: "Perfect for individuals exploring agentic automation",
      icon: Zap,
      popular: false,
      gradient: "from-inspiration-beige to-border",
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
      gradient: "from-primary to-secondary",
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
      gradient: "from-secondary to-muted",
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
      gradient: "from-muted to-inspiration-olive",
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
    <section ref={ref} id="pricing" className="py-32 bg-gradient-to-b from-inspiration-light to-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 right-10 w-96 h-96 bg-inspiration-beige rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute bottom-20 left-10 w-96 h-96 bg-border rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse" style={{ animationDelay: '2s' }}></div>
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
            Simple Pricing
            <br />
            <span className="bg-gradient-to-r from-secondary via-muted to-inspiration-olive bg-clip-text text-transparent">
              Scale as You Grow
            </span>
          </h2>
          <p className="text-xl md:text-2xl text-muted max-w-4xl mx-auto leading-relaxed font-light">
            Start free and upgrade when you need more power. All plans include our core features with transparent pricing and no hidden fees.
          </p>
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              variants={itemVariants}
              className="relative group"
            >
              {plan.popular && (
                <motion.div 
                  className="absolute -top-6 left-1/2 transform -translate-x-1/2 z-10"
                  initial={{ scale: 0, rotate: -10 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
                >
                  <span className="bg-gradient-to-r from-primary to-secondary text-background px-6 py-2 rounded-full text-sm font-bold shadow-xl">
                    Most Popular
                  </span>
                </motion.div>
              )}
              
              <motion.div 
                className={`relative bg-card/60 backdrop-blur-lg rounded-3xl p-10 h-full border transition-all duration-500 overflow-hidden ${
                  plan.popular 
                    ? 'border-primary/30 shadow-2xl scale-105' 
                    : 'border-border/50 hover:border-inspiration-beige hover:shadow-xl'
                } hover:scale-105 group-hover:bg-card/80`}
                whileHover={{ y: -10 }}
                transition={{ duration: 0.3 }}
              >
                {/* Gradient overlay */}
                <div className={`absolute inset-0 bg-gradient-to-br ${plan.gradient} opacity-5 group-hover:opacity-10 transition-opacity duration-500`}></div>
                
                <div className="relative z-10">
                  <div className="text-center mb-10">
                    <motion.div 
                      className={`w-16 h-16 bg-gradient-to-br ${plan.gradient} rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg group-hover:shadow-xl transition-all duration-300`}
                      whileHover={{ rotate: 5, scale: 1.1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <plan.icon className="h-8 w-8 text-background" />
                    </motion.div>
                    <h3 className="text-2xl font-black text-primary mb-3 group-hover:text-secondary transition-colors duration-300">{plan.name}</h3>
                    <p className="text-muted text-base mb-6 leading-relaxed">{plan.description}</p>
                    <div className="text-center">
                      <span className="text-4xl lg:text-5xl font-black text-primary group-hover:text-secondary transition-colors duration-300">{plan.price}</span>
                      {plan.period && <span className="text-muted text-lg">{plan.period}</span>}
                    </div>
                  </div>

                  <ul className="space-y-4 mb-10">
                    {plan.features.map((feature, featureIndex) => (
                      <motion.li 
                        key={featureIndex} 
                        className="flex items-start space-x-3"
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: featureIndex * 0.1 }}
                        viewport={{ once: true }}
                      >
                        <div className="w-5 h-5 rounded-full bg-gradient-to-r from-inspiration-olive to-muted flex items-center justify-center flex-shrink-0 mt-1">
                          <Check className="h-3 w-3 text-background" />
                        </div>
                        <span className="text-muted text-base leading-relaxed group-hover:text-primary transition-colors duration-300">{feature}</span>
                      </motion.li>
                    ))}
                  </ul>

                  <motion.button 
                    className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-500 relative overflow-hidden group/btn ${
                      plan.popular 
                        ? 'bg-gradient-to-r from-primary to-secondary text-background hover:from-secondary hover:to-primary shadow-xl hover:shadow-2xl' 
                        : plan.name === 'Enterprise'
                        ? 'border-2 border-border bg-card/80 text-primary hover:bg-background hover:border-muted hover:shadow-xl'
                        : 'bg-gradient-to-r from-inspiration-beige to-border text-primary hover:from-border hover:to-inspiration-olive hover:text-background shadow-lg hover:shadow-xl'
                    }`}
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <span className="relative z-10">
                      {plan.name === 'Enterprise' ? 'Contact Sales' : plan.name === 'Hobbyist' ? 'Get Started Free' : 'Start Free Trial'}
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover/btn:translate-x-full transition-transform duration-1000"></div>
                  </motion.button>
                </div>

                {/* Subtle shine effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              </motion.div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="mt-20 text-center space-y-6"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: [0.6, -0.05, 0.01, 0.99] }}
          viewport={{ once: true }}
        >
          <p className="text-muted text-lg">
            All plans include 14-day free trial • No credit card required • Cancel anytime
          </p>
          <div className="flex flex-wrap justify-center gap-8 text-base text-muted">
            {[
              { icon: Check, text: "99.9% SLA" },
              { icon: Check, text: "24/7 Support" },
              { icon: Check, text: "SOC 2 Compliant" }
            ].map((item, index) => (
              <motion.span 
                key={item.text}
                className="flex items-center space-x-2 hover:text-primary transition-colors duration-300"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.8 + index * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="w-5 h-5 rounded-full bg-gradient-to-r from-inspiration-olive to-muted flex items-center justify-center">
                  <item.icon className="h-3 w-3 text-background" />
                </div>
                <span>{item.text}</span>
              </motion.span>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </section>
  )
}