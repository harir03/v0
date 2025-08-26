import React from 'react';
import { motion } from 'framer-motion';
import { Check, Zap, Star, Crown } from 'lucide-react';

const PricingSection: React.FC = () => {
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
      description: "For large organizations with custom requirements",
      icon: Crown,
      color: "border-aether-purple",
      buttonColor: "bg-gradient-to-r from-aether-purple to-aether-blue hover:shadow-lg hover:shadow-aether-purple/50",
      popular: false,
      features: [
        "Unlimited User Seats",
        "White-label Solution",
        "Custom Integrations",
        "On-premise Deployment",
        "SLA Guarantees",
        "24/7 Premium Support",
        "Custom Training",
        "Dedicated Success Manager"
      ]
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-aether-gray-900">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="bg-gradient-to-r from-aether-blue to-aether-purple bg-clip-text text-transparent">
              Simple Pricing.
            </span>
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
              className={`relative bg-aether-gray-800 rounded-xl p-6 border-2 ${plan.color} ${
                plan.popular ? 'ring-2 ring-aether-blue/50' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-aether-blue to-aether-purple text-white text-sm font-medium px-3 py-1 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="flex items-center space-x-3 mb-4">
                <plan.icon className="h-8 w-8 text-aether-blue" />
                <h3 className="text-xl font-bold text-white">{plan.name}</h3>
              </div>

              <div className="mb-4">
                <div className="flex items-baseline">
                  <span className="text-3xl font-bold text-white">{plan.price}</span>
                  {plan.period && (
                    <span className="text-aether-gray-400 ml-1">{plan.period}</span>
                  )}
                </div>
                <p className="text-aether-gray-300 text-sm mt-2">{plan.description}</p>
              </div>

              <button className={`w-full text-white py-3 px-4 rounded-lg font-medium transition-all duration-200 ${plan.buttonColor}`}>
                {plan.name === "Enterprise" ? "Contact Sales" : "Get Started"}
              </button>

              <ul className="mt-6 space-y-3">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start">
                    <Check className="h-5 w-5 text-aether-blue flex-shrink-0 mt-0.5" />
                    <span className="text-aether-gray-300 ml-3 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          className="text-center mt-12"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <p className="text-aether-gray-400 text-sm">
            All plans include 14-day free trial. No credit card required. Cancel anytime.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default PricingSection;