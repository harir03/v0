'use client'

import { useState, useMemo } from 'react'
import { InterfaceSpec, CodeGenerationOptions } from '@/types/builder'
import { CodeGenerator } from '@/lib/builder/codeGenerator'
import { Copy, Check, Download } from 'lucide-react'

interface CodeEditorProps {
  spec: InterfaceSpec
  framework?: CodeGenerationOptions['framework']
  onChange: (spec: InterfaceSpec) => void
}

export default function CodeEditor({ spec, framework = 'next', onChange }: CodeEditorProps) {
  const [copied, setCopied] = useState(false)
  const [activeTab, setActiveTab] = useState<'typescript' | 'css' | 'dependencies'>('typescript')
  
  const generatedCode = useMemo(() => {
    const generator = new CodeGenerator({
      framework,
      styling: 'tailwind',
      typescript: true,
      accessibility: true,
      responsive: true
    })
    
    try {
      return generator.generatePage(spec)
    } catch (error) {
      console.error('Code generation error:', error)
      return {
        typescript: '// Error generating code\n// Please check your component specification',
        css: '',
        dependencies: [],
        imports: []
      }
    }
  }, [spec, framework])

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const downloadCode = () => {
    const fileExtensions: Record<string, string> = {
      react: 'tsx',
      next: 'tsx',
      vue: 'vue',
      svelte: 'svelte',
      angular: 'ts'
    }
    
    const extension = fileExtensions[framework] || 'tsx'
    const filename = `${spec.name.toLowerCase().replace(/\s+/g, '-')}.${extension}`
    
    const blob = new Blob([generatedCode.typescript], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const getDisplayContent = () => {
    switch (activeTab) {
      case 'typescript':
        return generatedCode.typescript
      case 'css':
        return generatedCode.css || '/* No custom CSS needed - using Tailwind CSS */'
      case 'dependencies':
        return `// Package dependencies for ${framework}:\n\n` + 
               generatedCode.dependencies.map(dep => `"${dep}"`).join(',\n')
      default:
        return generatedCode.typescript
    }
  }

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-4">
          <h3 className="text-lg font-semibold text-gray-900">Generated Code</h3>
          <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
            {framework.toUpperCase()}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => copyToClipboard(getDisplayContent())}
            className="flex items-center space-x-2 px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
          >
            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>
          <button
            onClick={downloadCode}
            className="flex items-center space-x-2 px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Download</span>
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {[
          { id: 'typescript', label: framework === 'angular' ? 'TypeScript' : 'Component' },
          { id: 'css', label: 'Styles' },
          { id: 'dependencies', label: 'Dependencies' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Code Content */}
      <div className="flex-1 overflow-hidden">
        <pre className="h-full p-4 text-sm text-gray-800 font-mono bg-gray-50 overflow-auto leading-relaxed">
          <code>{getDisplayContent()}</code>
        </pre>
      </div>

      {/* Footer */}
      <div className="p-3 bg-gray-50 border-t border-gray-200 text-xs text-gray-500">
        <div className="flex items-center justify-between">
          <span>
            Generated for {framework} • {generatedCode.typescript.split('\n').length} lines • 
            {generatedCode.dependencies.length} dependencies
          </span>
          <span>
            Framework: {framework} | Styling: Tailwind CSS | TypeScript: Enabled
          </span>
        </div>
      </div>
    </div>
  )
}