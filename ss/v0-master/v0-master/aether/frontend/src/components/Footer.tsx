'use client'

import { Zap, Github, Twitter, Linkedin, Mail } from 'lucide-react'

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
    },
    {
      name: 'GitHub',
      href: '#',
      icon: Github,
    },
    {
      name: 'LinkedIn',
      href: '#',
      icon: Linkedin,
    },
    {
      name: 'Email',
      href: 'mailto:hello@aether-agents.com',
      icon: Mail,
    },
  ]

  return (
    <footer className="bg-aether-gray-900 border-t border-aether-blue/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="relative">
                <Zap className="h-8 w-8 text-aether-blue" />
                <div className="absolute inset-0 h-8 w-8 bg-aether-blue/20 rounded-full animate-ping"></div>
              </div>
              <span className="text-xl font-bold gradient-text">Aether Agents</span>
            </div>
            <p className="text-aether-gray-400 mb-6 max-w-sm">
              The next-generation platform for creating, deploying, and managing AI agents. 
              Build sophisticated automation that thinks, codes, and operates like human employees.
            </p>
            <div className="flex space-x-4">
              {social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-aether-gray-400 hover:text-aether-blue transition-colors duration-200"
                >
                  <span className="sr-only">{item.name}</span>
                  <item.icon className="h-6 w-6" />
                </a>
              ))}
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Product</h3>
            <ul className="space-y-3">
              {navigation.product.map((item) => (
                <li key={item.name}>
                  <a href={item.href} className="text-aether-gray-400 hover:text-aether-blue transition-colors duration-200">
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Company</h3>
            <ul className="space-y-3">
              {navigation.company.map((item) => (
                <li key={item.name}>
                  <a href={item.href} className="text-aether-gray-400 hover:text-aether-blue transition-colors duration-200">
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Resources</h3>
            <ul className="space-y-3">
              {navigation.resources.map((item) => (
                <li key={item.name}>
                  <a href={item.href} className="text-aether-gray-400 hover:text-aether-blue transition-colors duration-200">
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Legal</h3>
            <ul className="space-y-3">
              {navigation.legal.map((item) => (
                <li key={item.name}>
                  <a href={item.href} className="text-aether-gray-400 hover:text-aether-blue transition-colors duration-200">
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter Signup */}
        <div className="mt-12 pt-8 border-t border-aether-blue/20">
          <div className="md:flex md:items-center md:justify-between">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold text-white mb-2">Stay updated</h3>
              <p className="text-aether-gray-400">Get the latest news and updates about Aether Agents.</p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 md:max-w-md">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 bg-aether-dark border border-aether-blue/30 rounded-lg px-4 py-2 text-white placeholder-aether-gray-400 focus:outline-none focus:border-aether-blue"
              />
              <button className="bg-gradient-to-r from-aether-blue to-aether-purple text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg hover:shadow-aether-blue/50 transition-all duration-200 whitespace-nowrap">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-aether-blue/20 md:flex md:items-center md:justify-between">
          <div className="flex space-x-6 md:order-2">
            <span className="text-aether-gray-400 text-sm">
              Built with ❤️ for the future of work
            </span>
          </div>
          <p className="mt-4 text-aether-gray-400 text-sm md:mt-0 md:order-1">
            &copy; 2024 Aether Agents. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}