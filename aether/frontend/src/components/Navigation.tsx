'use client'

import { useState } from 'react'
import { Menu, X, Zap } from 'lucide-react'

export default function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navItems = [
    { name: 'Features', href: '#features' },
    { name: 'Demo', href: '#demo' },
    { name: 'Vivid AI', href: '/vivid-ai' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'Docs', href: '/docs' },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-aether-dark/90 backdrop-blur-md border-b border-aether-blue/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Zap className="h-8 w-8 text-aether-blue animate-pulse-slow" />
              <div className="absolute inset-0 h-8 w-8 bg-aether-blue/20 rounded-full animate-ping"></div>
            </div>
            <span className="text-xl font-bold gradient-text">Aether Agents</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className="text-aether-gray-300 hover:text-aether-blue transition-colors duration-200 font-medium"
              >
                {item.name}
              </a>
            ))}
            <button className="bg-gradient-to-r from-aether-blue to-aether-purple text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg hover:shadow-aether-blue/50 transition-all duration-200 transform hover:scale-105">
              Get Started
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-aether-gray-300 hover:text-aether-blue transition-colors duration-200"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-aether-blue/20">
            <div className="flex flex-col space-y-4">
              {navItems.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-aether-gray-300 hover:text-aether-blue transition-colors duration-200 font-medium px-4 py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </a>
              ))}
              <button className="mx-4 mt-4 bg-gradient-to-r from-aether-blue to-aether-purple text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg hover:shadow-aether-blue/50 transition-all duration-200">
                Get Started
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}