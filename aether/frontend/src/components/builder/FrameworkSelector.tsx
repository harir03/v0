'use client'

import React, { useState } from 'react'
import { FrameworkFactory, FrameworkInfo } from '@/lib/builder/frameworks/factory'
import { CodeGenerationOptions } from '@/types/builder'

interface FrameworkSelectorProps {
  currentFramework: CodeGenerationOptions['framework']
  onFrameworkChange: (framework: CodeGenerationOptions['framework']) => void
  className?: string
}

export function FrameworkSelector({ 
  currentFramework, 
  onFrameworkChange, 
  className = '' 
}: FrameworkSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const frameworks = FrameworkFactory.getAvailableFrameworks()
  const selectedFramework = frameworks.find(f => f.key === currentFramework)

  const handleFrameworkSelect = (frameworkKey: string) => {
    onFrameworkChange(frameworkKey as CodeGenerationOptions['framework'])
    setIsOpen(false)
  }

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 px-4 py-3 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors bg-white min-w-[200px]"
      >
        <span className="text-2xl">{selectedFramework?.icon}</span>
        <div className="flex-1 text-left">
          <div className="font-medium">{selectedFramework?.name}</div>
          <div className="text-sm text-gray-500">{selectedFramework?.version}</div>
        </div>
        <svg 
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
          {frameworks.map((framework) => (
            <button
              key={framework.key}
              onClick={() => handleFrameworkSelect(framework.key)}
              className={`w-full flex items-start gap-3 px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0 ${
                framework.key === currentFramework ? 'bg-blue-50 border-blue-200' : ''
              }`}
            >
              <span className="text-2xl">{framework.icon}</span>
              <div className="flex-1 text-left">
                <div className="font-medium">{framework.name}</div>
                <div className="text-sm text-gray-500 mb-1">{framework.description}</div>
                <div className="text-xs text-gray-400">
                  {framework.version} • {framework.buildTool}
                </div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {framework.features.slice(0, 3).map((feature) => (
                    <span 
                      key={feature}
                      className="px-2 py-1 text-xs bg-gray-100 rounded-full"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>
              {framework.key === currentFramework && (
                <div className="text-blue-600">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export function FrameworkComparison() {
  const frameworks = FrameworkFactory.getAvailableFrameworks()
  
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold mb-4">Framework Comparison</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2">Framework</th>
              <th className="text-left py-2">Version</th>
              <th className="text-left py-2">Build Tool</th>
              <th className="text-left py-2">Key Features</th>
              <th className="text-left py-2">Best For</th>
            </tr>
          </thead>
          <tbody>
            {frameworks.map((framework) => (
              <tr key={framework.key} className="border-b last:border-b-0">
                <td className="py-3">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{framework.icon}</span>
                    <span className="font-medium">{framework.name}</span>
                  </div>
                </td>
                <td className="py-3 text-gray-600">{framework.version}</td>
                <td className="py-3 text-gray-600">{framework.buildTool}</td>
                <td className="py-3">
                  <div className="flex flex-wrap gap-1">
                    {framework.features.slice(0, 2).map((feature) => (
                      <span 
                        key={feature}
                        className="px-2 py-1 text-xs bg-gray-100 rounded-full"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-3 text-gray-600 text-xs">
                  {getBestUseCase(framework.key)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function getBestUseCase(frameworkKey: string): string {
  const useCases: Record<string, string> = {
    'react': 'SPAs, Complex UIs',
    'next': 'SSR, Full-stack Apps',
    'vue': 'Progressive Enhancement',
    'svelte': 'Performance-critical',
    'angular': 'Enterprise, Large Teams'
  }
  return useCases[frameworkKey] || 'General Purpose'
}