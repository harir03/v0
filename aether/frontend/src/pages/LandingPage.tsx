import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Star, Crown, Check } from 'lucide-react';
import PricingSection from '../components/PricingSection';
import InteractiveDemo from '../components/InteractiveDemo';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-aether-dark">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-aether-blue to-aether-purple bg-clip-text text-transparent">
                Aether Agents
              </span>
              <br />
              <span className="text-white">Production Ready</span>
            </h1>
            <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto mb-8">
              Transform your business with enterprise-grade AI agents. Build, deploy, and scale 
              intelligent automation that competes with industry leaders.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register" className="btn-primary text-lg px-8 py-4">
                Start Building
              </Link>
              <Link to="/login" className="btn-secondary text-lg px-8 py-4">
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Interactive Demo */}
      <InteractiveDemo />

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Enterprise-Grade Platform
            </h2>
            <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto">
              Built for scale with production-ready features that enterprise customers demand.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              className="card text-center"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-aether-blue to-aether-purple rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Lightning Fast</h3>
              <p className="text-aether-gray-300">
                Built on modern infrastructure with sub-second response times and 99.9% uptime SLA.
              </p>
            </motion.div>

            <motion.div
              className="card text-center"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-aether-blue to-aether-purple rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Star className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Enterprise Security</h3>
              <p className="text-aether-gray-300">
                SOC 2 compliant with enterprise-grade security, encryption, and compliance features.
              </p>
            </motion.div>

            <motion.div
              className="card text-center"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <div className="w-12 h-12 bg-gradient-to-r from-aether-blue to-aether-purple rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Crown className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Scalable Architecture</h3>
              <p className="text-aether-gray-300">
                Microservices architecture that scales from startup to enterprise with 10,000+ users.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <PricingSection />

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-aether-gray-900">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-aether-gray-300 mb-8">
            Join thousands of companies already using Aether Agents to automate their workflows.
          </p>
          <Link to="/register" className="btn-primary text-lg px-8 py-4">
            Start Your Free Trial
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;