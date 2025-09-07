'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Mail, Calendar, User } from 'lucide-react'

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
        <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Customer Support Dashboard</h3>
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-red-400 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-500">
                <div className="flex items-center space-x-2 mb-2">
                  <Mail className="h-4 w-4 text-blue-500" />
                  <span className="text-sm text-gray-600">New Ticket #1234</span>
                </div>
                <p className="text-sm text-gray-900">Login issues with account verification...</p>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-green-500">
                <div className="flex items-center space-x-2 mb-2">
                  <Mail className="h-4 w-4 text-green-500" />
                  <span className="text-sm text-gray-600">Ticket #1233 - Resolved</span>
                </div>
                <p className="text-sm text-gray-900">Billing question resolved automatically...</p>
              </div>
            </div>
            
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="text-gray-900 font-medium mb-3">Draft Response</h4>
              <textarea 
                className="w-full h-20 bg-white text-gray-900 p-3 rounded border border-gray-200 resize-none"
                placeholder="AI-generated response will appear here..."
              />
              <button className="mt-3 bg-gray-900 text-white px-4 py-2 rounded text-sm hover:bg-gray-800 transition-colors duration-200">
                Send & Close Ticket
              </button>
            </div>
          </div>
        </div>
      )
    }
    
    return (
      <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
            <div className="h-3 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <section id="demo" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
            Try It Live
            <br />
            <span className="text-gray-600">Build an Agent Now</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Describe what you want your agent to do, and watch as Aether creates the interface and logic in real-time.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Demo Interface */}
          <motion.div
            className="space-y-6"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center">
                  <User className="h-5 w-5 text-gray-600" />
                </div>
                <div className="font-medium text-gray-900">Instant Interface Builder</div>
              </div>
              
              <div className="space-y-4">
                <textarea
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder="Describe your agent interface..."
                  className="w-full h-32 p-4 border border-gray-200 rounded-lg resize-none text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                />
                
                <button
                  onClick={handleSubmit}
                  disabled={isGenerating || !userInput.trim()}
                  className="w-full bg-gray-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {isGenerating ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                  <span>{isGenerating ? 'Generating...' : 'Generate'}</span>
                </button>
              </div>
            </div>

            {/* Demo Commands */}
            <div className="space-y-3">
              {demoCommands.map((command, index) => (
                <button
                  key={index}
                  onClick={() => setUserInput(command)}
                  className="w-full text-left p-4 bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-all duration-200"
                >
                  {command}
                </button>
              ))}
            </div>
          </motion.div>

          {/* Generated Output */}
          <motion.div
            className="space-y-6"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
          >
            {generatedUI ? (
              <MockGeneratedInterface prompt={generatedUI} />
            ) : (
              <div className="bg-gray-50 rounded-xl p-12 text-center border border-gray-200">
                <div className="text-gray-400 mb-4">
                  <Calendar className="h-12 w-12 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Generate</h3>
                <p className="text-gray-600">
                  Enter a description above and click Generate to see the magic happen.
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  )
}