'use client'

import { motion } from 'framer-motion'
import { Zap, Github, Twitter, Linkedin, Mail, ArrowRight } from 'lucide-react'

export default function Footer() {
  const navigation = {
    product: [
      { name: 'Features', href: '#features' },
      { name: 'Pricing', href: '#pricing' },
      { name: 'Demo', href: '#demo' },
      { name: 'Changelog', href: '/changelog' },
    ],
    company: [
      { name: 'About', href: '/about' },
      { name: 'Blog', href: '/blog' },
      { name: 'Careers', href: '/careers' },
      { name: 'Contact', href: '/contact' },
    ],
    resources: [
      { name: 'Documentation', href: '/docs' },
      { name: 'API Reference', href: '/api' },
      { name: 'Guides', href: '/guides' },
      { name: 'Community', href: '/community' },
    ],
    legal: [
      { name: 'Privacy', href: '/privacy' },
      { name: 'Terms', href: '/terms' },
      { name: 'Security', href: '/security' },
      { name: 'Status', href: '/status' },
    ],
  }

  const social = [
    {
      name: 'Twitter',
      href: '#',
      icon: Twitter,
      gradient: 'from-blue-400 to-blue-600'
    },
    {
      name: 'GitHub',
      href: '#',
      icon: Github,
      gradient: 'from-gray-600 to-gray-800'
    },
    {
      name: 'LinkedIn',
      href: '#',
      icon: Linkedin,
      gradient: 'from-blue-600 to-blue-800'
    },
    {
      name: 'Email',
      href: 'mailto:hello@aether-agents.com',
      icon: Mail,
      gradient: 'from-red-400 to-red-600'
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
        ease: [0.6, -0.05, 0.01, 0.99],
      },
    },
  }

  return (
    <footer className="bg-gradient-to-b from-background to-inspiration-light border-t border-border/50 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/3 w-96 h-96 bg-inspiration-beige rounded-full mix-blend-multiply filter blur-xl opacity-50 animate-pulse"></div>
        <div className="absolute bottom-0 right-1/3 w-96 h-96 bg-border rounded-full mix-blend-multiply filter blur-xl opacity-50 animate-pulse" style={{ animationDelay: '3s' }}></div>
      </div>

      <motion.div 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10"
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-12">
          {/* Brand */}
          <motion.div className="lg:col-span-2" variants={itemVariants}>
            <div className="flex items-center space-x-3 mb-6">
              <motion.div
                className="p-3 rounded-2xl bg-gradient-to-br from-primary to-secondary"
                whileHover={{ rotate: 5, scale: 1.05 }}
                transition={{ duration: 0.3 }}
              >
                <Zap className="h-8 w-8 text-background" />
              </motion.div>
              <span className="text-2xl font-black text-primary tracking-tight">Aether Agents</span>
            </div>
            <p className="text-muted mb-8 max-w-sm text-lg leading-relaxed">
              The next-generation platform for creating, deploying, and managing AI agents. 
              Build sophisticated automation that thinks, codes, and operates like human employees.
            </p>
            <div className="flex space-x-4">
              {social.map((item, index) => (
                <motion.a
                  key={item.name}
                  href={item.href}
                  className={`w-12 h-12 rounded-xl bg-gradient-to-br ${item.gradient} flex items-center justify-center text-background hover:shadow-lg transition-all duration-300 group`}
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: 0.6 + index * 0.1 }}
                >
                  <span className="sr-only">{item.name}</span>
                  <item.icon className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                </motion.a>
              ))}
            </div>
          </motion.div>

          {/* Navigation Sections */}
          {Object.entries(navigation).map(([section, links], sectionIndex) => (
            <motion.div key={section} variants={itemVariants}>
              <h3 className="text-sm font-black text-primary tracking-wider uppercase mb-6">
                {section}
              </h3>
              <ul className="space-y-4">
                {links.map((item, linkIndex) => (
                  <motion.li 
                    key={item.name}
                    initial={{ opacity: 0, x: -10 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: sectionIndex * 0.1 + linkIndex * 0.05 }}
                    viewport={{ once: true }}
                  >
                    <a
                      href={item.href}
                      className="text-muted hover:text-primary transition-all duration-300 flex items-center group text-base"
                    >
                      <span>{item.name}</span>
                      <ArrowRight className="h-4 w-4 ml-1 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-300" />
                    </a>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Newsletter */}
        <motion.div 
          className="mt-20 pt-12 border-t border-border/50"
          variants={itemVariants}
        >
          <div className="lg:flex lg:items-center lg:justify-between">
            <div>
              <h3 className="text-2xl font-black text-primary mb-3">Stay updated</h3>
              <p className="text-muted text-lg">
                Get the latest news and updates about Aether Agents.
              </p>
            </div>
            <motion.div 
              className="mt-8 lg:mt-0 lg:flex-shrink-0"
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              viewport={{ once: true }}
            >
              <div className="flex rounded-2xl overflow-hidden shadow-lg">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="px-6 py-4 bg-card border-none text-primary placeholder-muted focus:outline-none focus:ring-2 focus:ring-primary/20 min-w-0 flex-1 sm:min-w-0 text-lg"
                />
                <motion.button 
                  className="bg-gradient-to-r from-primary to-secondary text-background px-8 py-4 font-bold hover:from-secondary hover:to-primary transition-all duration-300 relative overflow-hidden group"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <span className="relative z-10">Subscribe</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                </motion.button>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Bottom */}
        <motion.div 
          className="mt-16 pt-8 border-t border-border/50 flex flex-col lg:flex-row justify-between items-center"
          variants={itemVariants}
        >
          <div className="text-muted text-lg flex items-center space-x-2">
            <span>Built with</span>
            <motion.span
              className="text-red-500 text-xl"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity, repeatDelay: 2 }}
            >
              ❤️
            </motion.span>
            <span>for the future of work</span>
          </div>
          <p className="text-muted text-lg mt-4 lg:mt-0">
            © 2024 Aether Agents. All rights reserved.
          </p>
        </motion.div>
      </motion.div>
    </footer>
  )
}