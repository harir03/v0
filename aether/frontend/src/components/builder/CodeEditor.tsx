'use client'

import { useState } from 'react'
import { InterfaceSpec } from '@/types/builder'
import { Copy, Check, Download } from 'lucide-react'

interface CodeEditorProps {
  spec: InterfaceSpec
  onChange: (spec: InterfaceSpec) => void
}

export default function CodeEditor({ spec, onChange }: CodeEditorProps) {
  const [copied, setCopied] = useState(false)
  
  const generateCode = (spec: InterfaceSpec): string => {
    const imports = [
      "import { motion } from 'framer-motion'",
      "import { useState } from 'react'"
    ]

    const components = spec.components.map(component => {
      switch (component.type) {
        case 'hero':
          return `
    <motion.section 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="px-6 py-20 text-center bg-gradient-to-br from-blue-50 to-indigo-100"
    >
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold mb-6">
          ${component.props.title}
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          ${component.props.subtitle}
        </p>
        <button className="px-8 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
          ${component.props.ctaText}
        </button>
      </div>
    </motion.section>`

        case 'features':
          return `
    <motion.section 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="px-6 py-16"
    >
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature cards will be generated here */}
        </div>
      </div>
    </motion.section>`

        default:
          return `    {/* ${component.type} component */}`
      }
    }).join('\n')

    return `${imports.join('\n')}

export default function GeneratedPage() {
  return (
    <div className="min-h-screen">
${components}
    </div>
  )
}

// Theme configuration
export const theme = ${JSON.stringify(spec.theme, null, 2)}`
  }

  const code = generateCode(spec)

  const copyCode = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadCode = () => {
    const blob = new Blob([code], { type: 'text/typescript' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${spec.name.toLowerCase().replace(/\s+/g, '-')}.tsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="h-full flex flex-col bg-gray-900 text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <h3 className="text-sm font-medium">Generated Code</h3>
        <div className="flex items-center space-x-2">
          <button
            onClick={copyCode}
            className="p-2 text-gray-400 hover:text-white rounded transition-colors"
            title="Copy code"
          >
            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
          </button>
          <button
            onClick={downloadCode}
            className="p-2 text-gray-400 hover:text-white rounded transition-colors"
            title="Download code"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Code Display */}
      <div className="flex-1 overflow-auto">
        <pre className="p-4 text-sm leading-relaxed">
          <code className="text-green-400">
            {code}
          </code>
        </pre>
      </div>

      {/* Spec Editor */}
      <div className="border-t border-gray-700 p-4">
        <h4 className="text-sm font-medium mb-2">Interface Specification</h4>
        <textarea
          value={JSON.stringify(spec, null, 2)}
          onChange={(e) => {
            try {
              const newSpec = JSON.parse(e.target.value)
              onChange(newSpec)
            } catch (error) {
              // Invalid JSON, don't update
            }
          }}
          className="w-full h-32 p-2 text-xs bg-gray-800 border border-gray-600 rounded font-mono resize-none"
          placeholder="Edit the interface specification JSON..."
        />
      </div>
    </div>
  )
}