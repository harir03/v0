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
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Zap className="h-8 w-8 text-gray-900" />
              <span className="text-xl font-bold text-gray-900">Aether Agents</span>
            </div>
            <p className="text-gray-600 mb-6 max-w-sm">
              The next-generation platform for creating, deploying, and managing AI agents. 
              Build sophisticated automation that thinks, codes, and operates like human employees.
            </p>
            <div className="flex space-x-4">
              {social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                >
                  <span className="sr-only">{item.name}</span>
                  <item.icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Navigation */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
              Product
            </h3>
            <ul className="space-y-3">
              {navigation.product.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
              Company
            </h3>
            <ul className="space-y-3">
              {navigation.company.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
              Resources
            </h3>
            <ul className="space-y-3">
              {navigation.resources.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
              Legal
            </h3>
            <ul className="space-y-3">
              {navigation.legal.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors duration-200"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <div className="lg:flex lg:items-center lg:justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Stay updated</h3>
              <p className="text-gray-600">
                Get the latest news and updates about Aether Agents.
              </p>
            </div>
            <div className="mt-6 lg:mt-0 lg:flex-shrink-0">
              <div className="flex">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="px-4 py-3 border border-gray-300 rounded-l-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent min-w-0 flex-1 sm:min-w-0"
                />
                <button className="bg-gray-900 text-white px-6 py-3 rounded-r-lg font-medium hover:bg-gray-800 transition-colors duration-200">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 pt-8 border-t border-gray-200 flex flex-col lg:flex-row justify-between items-center">
          <div className="text-gray-600 text-sm">
            Built with ❤️ for the future of work
          </div>
          <p className="text-gray-600 text-sm mt-4 lg:mt-0">
            © 2024 Aether Agents. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}