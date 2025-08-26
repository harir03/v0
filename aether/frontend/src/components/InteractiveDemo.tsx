'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Code, Mail, Calendar } from 'lucide-react'

export default function InteractiveDemo() {
  const [userInput, setUserInput] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedUI, setGeneratedUI] = useState<string | null>(null)

  const demoCommands = [
    "Create an agent for customer support dashboard",
    "Build a lead management system",
    "Design a code review workflow interface",
    "Make a project management agent"
  ]

  const handleSubmit = async () => {
    if (!userInput.trim()) return

    setIsGenerating(true)
    
    // Simulate AI generation
    setTimeout(() => {
      setGeneratedUI(userInput)
      setIsGenerating(false)
    }, 2000)
  }

  const MockGeneratedInterface = ({ prompt }: { prompt: string }) => {
    if (prompt.toLowerCase().includes('customer support')) {
      return (
        <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-blue/30">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Customer Support Dashboard</h3>
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-aether-green rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="bg-aether-dark p-3 rounded border-l-4 border-aether-blue">
                <div className="flex items-center space-x-2 mb-2">
                  <Mail className="h-4 w-4 text-aether-blue" />
                  <span className="text-sm text-aether-gray-300">New Ticket #1234</span>
                </div>
                <p className="text-sm text-white">Login issues with account verification...</p>
              </div>
              
              <div className="bg-aether-dark p-3 rounded border-l-4 border-aether-green">
                <div className="flex items-center space-x-2 mb-2">
                  <Mail className="h-4 w-4 text-aether-green" />
                  <span className="text-sm text-aether-gray-300">Ticket #1233 - Resolved</span>
                </div>
                <p className="text-sm text-white">Billing question resolved automatically...</p>
              </div>
            </div>
            
            <div className="bg-aether-dark p-4 rounded">
              <h4 className="text-white font-medium mb-3">Draft Response</h4>
              <textarea 
                className="w-full h-20 bg-aether-gray-800 text-white p-2 rounded border border-aether-blue/30 resize-none"
                placeholder="AI-generated response will appear here..."
              />
              <button className="mt-2 bg-aether-blue text-white px-4 py-2 rounded text-sm hover:bg-aether-blue/80">
                Send & Close Ticket
              </button>
            </div>
          </div>
        </div>
      )
    }
    
    return (
      <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-blue/30">
        <div className="animate-pulse">
          <div className="h-4 bg-aether-blue/30 rounded w-3/4 mb-4"></div>
          <div className="space-y-2">
            <div className="h-3 bg-aether-gray-700 rounded"></div>
            <div className="h-3 bg-aether-gray-700 rounded w-5/6"></div>
            <div className="h-3 bg-aether-gray-700 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <section id="demo" className="py-24 bg-gradient-to-b from-aether-dark to-aether-gray-900 relative overflow-hidden">
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
            <span className="gradient-text">Try It Live</span>
            <br />
            <span className="text-white">Build an Agent Now</span>
          </h2>
          <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto mb-8">
            Describe what you want your agent to do, and watch as Aether creates 
            the interface and logic in real-time.
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto">
          <motion.div
            className="bg-aether-gray-900/50 backdrop-blur-sm border border-aether-blue/20 rounded-xl p-8 mb-8"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <Code className="h-6 w-6 text-aether-blue" />
              <span className="text-lg font-semibold text-white">Instant Interface Builder</span>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Describe your agent interface..."
                className="flex-1 bg-aether-dark border border-aether-blue/30 rounded-lg px-4 py-3 text-white placeholder-aether-gray-400 focus:outline-none focus:border-aether-blue"
                onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              />
              <button
                onClick={handleSubmit}
                disabled={isGenerating || !userInput.trim()}
                className="bg-gradient-to-r from-aether-blue to-aether-purple text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg hover:shadow-aether-blue/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                <Send className="h-4 w-4" />
                <span>{isGenerating ? 'Generating...' : 'Generate'}</span>
              </button>
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              {demoCommands.map((command, index) => (
                <button
                  key={index}
                  onClick={() => setUserInput(command)}
                  className="text-sm bg-aether-dark border border-aether-blue/30 text-aether-blue px-3 py-1 rounded-full hover:bg-aether-blue/10 transition-colors duration-200"
                >
                  {command}
                </button>
              ))}
            </div>
          </motion.div>

          {/* Generated Interface Preview */}
          {(isGenerating || generatedUI) && (
            <motion.div
              className="bg-aether-gray-900/50 backdrop-blur-sm border border-aether-blue/20 rounded-xl p-8"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
            >
              <div className="flex items-center space-x-2 mb-6">
                <div className="w-3 h-3 bg-aether-green rounded-full animate-pulse"></div>
                <span className="text-lg font-semibold text-white">
                  {isGenerating ? 'Generating Interface...' : 'Generated Interface'}
                </span>
              </div>

              {isGenerating ? (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-aether-blue rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-aether-blue rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-aether-blue rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <span className="text-aether-gray-300 ml-2">AI is creating your interface...</span>
                  </div>
                  <MockGeneratedInterface prompt="" />
                </div>
              ) : (
                <MockGeneratedInterface prompt={generatedUI || ''} />
              )}
            </motion.div>
          )}
        </div>
      </div>
    </section>
  )
}