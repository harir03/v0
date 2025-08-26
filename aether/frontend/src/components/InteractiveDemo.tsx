import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mail, BarChart3, Code } from 'lucide-react';

const InteractiveDemo: React.FC = () => {
  const [userInput, setUserInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedUI, setGeneratedUI] = useState<string | null>(null);

  const demoCommands = [
    "Create an agent for customer support dashboard",
    "Build a lead management system",
    "Design a code review workflow interface",
    "Make a project management agent"
  ];

  const handleSubmit = async () => {
    if (!userInput.trim()) return;

    setIsGenerating(true);
    
    // Simulate AI generation
    setTimeout(() => {
      setGeneratedUI(userInput);
      setIsGenerating(false);
    }, 2000);
  };

  const MockGeneratedInterface = ({ prompt }: { prompt: string }) => {
    if (prompt.toLowerCase().includes('customer support')) {
      return (
        <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-blue/30">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-white font-semibold">Customer Support Dashboard</h3>
            <span className="text-aether-blue text-sm">Live Demo</span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="bg-aether-dark p-3 rounded border-l-4 border-aether-blue">
              <div className="flex items-center space-x-2 mb-2">
                <Mail className="h-4 w-4 text-aether-blue" />
                <span className="text-sm text-aether-gray-300">Ticket #1234 - Open</span>
              </div>
              <p className="text-sm text-white">Login issues with account verification...</p>
            </div>
            
            <div className="bg-aether-dark p-3 rounded border-l-4 border-aether-green">
              <div className="flex items-center space-x-2 mb-2">
                <Mail className="h-4 w-4 text-green-400" />
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
          </div>
        </div>
      );
    }

    if (prompt.toLowerCase().includes('lead management')) {
      return (
        <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-purple/30">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-white font-semibold">Lead Management System</h3>
            <span className="text-aether-purple text-sm">Live Demo</span>
          </div>
          
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-aether-dark p-3 rounded text-center">
              <div className="text-2xl font-bold text-aether-blue mb-1">47</div>
              <div className="text-sm text-aether-gray-300">New Leads</div>
            </div>
            <div className="bg-aether-dark p-3 rounded text-center">
              <div className="text-2xl font-bold text-aether-purple mb-1">23</div>
              <div className="text-sm text-aether-gray-300">Qualified</div>
            </div>
            <div className="bg-aether-dark p-3 rounded text-center">
              <div className="text-2xl font-bold text-green-400 mb-1">12</div>
              <div className="text-sm text-aether-gray-300">Converted</div>
            </div>
          </div>
          
          <div className="bg-aether-dark p-4 rounded">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-white font-medium">John Smith</div>
                <div className="text-sm text-aether-gray-300">john@company.com • Score: 85</div>
              </div>
              <button className="bg-aether-purple text-white px-3 py-1 rounded text-sm">
                Contact
              </button>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-blue/30">
        <div className="flex items-center space-x-2 mb-4">
          <Code className="h-5 w-5 text-aether-blue" />
          <h3 className="text-white font-semibold">Generated Agent Interface</h3>
        </div>
        <p className="text-aether-gray-300">
          Your custom agent interface for "{prompt}" would be generated here with real functionality.
        </p>
      </div>
    );
  };

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-aether-gray-800">
      <div className="max-w-6xl mx-auto">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold text-white mb-4">
            See Aether in Action
          </h2>
          <p className="text-xl text-aether-gray-300 max-w-3xl mx-auto mb-8">
            Describe what you want to build and watch Aether generate a production-ready agent interface in seconds.
          </p>
          
          <div className="bg-aether-gray-900 rounded-lg p-6 border border-aether-gray-700">
            <div className="flex flex-wrap gap-2 mb-4">
              {demoCommands.map((command, index) => (
                <button
                  key={index}
                  onClick={() => setUserInput(command)}
                  className="text-sm bg-aether-gray-700 hover:bg-aether-gray-600 text-aether-gray-300 hover:text-white px-3 py-1 rounded-full transition-colors"
                >
                  {command}
                </button>
              ))}
            </div>
            
            <div className="flex space-x-2">
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
          </div>
        </motion.div>

        {generatedUI && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mt-8"
          >
            <MockGeneratedInterface prompt={generatedUI} />
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default InteractiveDemo;