'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Code, Eye, Palette, Settings, Download, Github } from 'lucide-react'
import CodeEditor from '@/components/builder/CodeEditor'
import LivePreview from '@/components/builder/LivePreview'
import ComponentLibrary from '@/components/builder/ComponentLibrary'
import ThemeCustomizer from '@/components/builder/ThemeCustomizer'
import { InterfaceSpec } from '@/types/builder'

export default function BuilderPage() {
  const [activeTab, setActiveTab] = useState<'code' | 'preview' | 'components' | 'theme'>('preview')
  const [currentSpec, setCurrentSpec] = useState<InterfaceSpec>({
    id: 'demo-landing',
    name: 'Demo Landing Page',
    type: 'page',
    components: [
      {
        id: 'hero-1',
        type: 'hero',
        props: {
          title: 'Build Amazing Websites',
          subtitle: 'Create beautiful, responsive websites with our AI-powered builder',
          ctaText: 'Get Started',
          ctaVariant: 'primary'
        }
      }
    ],
    theme: {
      primaryColor: '#3b82f6',
      backgroundColor: '#ffffff',
      textColor: '#1f2937',
      fontFamily: 'Inter'
    }
  })

  const tabs = [
    { id: 'preview' as const, label: 'Preview', icon: Eye },
    { id: 'code' as const, label: 'Code', icon: Code },
    { id: 'components' as const, label: 'Components', icon: Settings },
    { id: 'theme' as const, label: 'Theme', icon: Palette }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-semibold text-gray-900">Aether Builder</h1>
            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
              Beta
            </span>
          </div>
          <div className="flex items-center space-x-3">
            <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center space-x-2">
              <Github className="w-4 h-4" />
              <span>Export to GitHub</span>
            </button>
            <button className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Download Code</span>
            </button>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-73px)]">
        {/* Sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <nav className="flex-1 p-4">
            <div className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-50 text-blue-700 border-blue-200'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex">
          {/* Left Panel */}
          <div className="w-1/2 border-r border-gray-200">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              {activeTab === 'preview' && (
                <LivePreview spec={currentSpec} />
              )}
              {activeTab === 'code' && (
                <CodeEditor spec={currentSpec} onChange={setCurrentSpec} />
              )}
              {activeTab === 'components' && (
                <ComponentLibrary onAddComponent={(component) => {
                  setCurrentSpec(prev => ({
                    ...prev,
                    components: [...prev.components, component]
                  }))
                }} />
              )}
              {activeTab === 'theme' && (
                <ThemeCustomizer 
                  theme={currentSpec.theme}
                  onChange={(theme) => setCurrentSpec(prev => ({ ...prev, theme }))}
                />
              )}
            </motion.div>
          </div>

          {/* Right Panel - Always Preview */}
          <div className="w-1/2">
            <LivePreview spec={currentSpec} />
          </div>
        </div>
      </div>
    </div>
  )
}