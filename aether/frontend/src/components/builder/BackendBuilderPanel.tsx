'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Server, 
  Database, 
  Code, 
  Settings, 
  Download, 
  Play,
  Check,
  AlertCircle,
  Loader2,
  ExternalLink
} from 'lucide-react'
import { BackendSpec, BackendFramework, DatabaseType, BackendGeneratedCode } from '@/types/backend'
import { BackendCodeGenerator } from '@/lib/backend-generator'
import { BackendTemplateLibrary } from '@/lib/backend-templates'

interface BackendBuilderPanelProps {
  onBackendGenerated?: (code: BackendGeneratedCode) => void
}

export default function BackendBuilderPanel({ onBackendGenerated }: BackendBuilderPanelProps) {
  const [activeTab, setActiveTab] = useState<'templates' | 'config' | 'preview' | 'deploy'>('templates')
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)
  const [backendSpec, setBackendSpec] = useState<BackendSpec | null>(null)
  const [generatedCode, setGeneratedCode] = useState<BackendGeneratedCode | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isDeploying, setIsDeploying] = useState(false)
  const [deploymentUrl, setDeploymentUrl] = useState<string | null>(null)

  const templates = BackendTemplateLibrary.getTemplates()
  
  const frameworks: { id: BackendFramework; name: string; description: string }[] = [
    { id: 'express', name: 'Express.js', description: 'Fast, minimalist Node.js framework' },
    { id: 'fastapi', name: 'FastAPI', description: 'Modern, fast Python API framework' },
    { id: 'nestjs', name: 'NestJS', description: 'Progressive Node.js framework' }
  ]

  const databases: { id: DatabaseType; name: string; description: string }[] = [
    { id: 'postgresql', name: 'PostgreSQL', description: 'Advanced open source database' },
    { id: 'mongodb', name: 'MongoDB', description: 'Document-based NoSQL database' },
    { id: 'mysql', name: 'MySQL', description: 'Popular relational database' },
    { id: 'sqlite', name: 'SQLite', description: 'Lightweight embedded database' },
    { id: 'supabase', name: 'Supabase', description: 'Open source Firebase alternative' }
  ]

  const handleTemplateSelect = (templateId: string) => {
    const template = BackendTemplateLibrary.getTemplateById(templateId)
    if (template) {
      setSelectedTemplate(templateId)
      setBackendSpec(template.spec)
      setActiveTab('config')
    }
  }

  const handleFrameworkChange = (framework: BackendFramework) => {
    if (backendSpec) {
      setBackendSpec({
        ...backendSpec,
        framework
      })
    }
  }

  const handleDatabaseChange = (dbType: DatabaseType) => {
    if (backendSpec) {
      setBackendSpec({
        ...backendSpec,
        database: {
          ...backendSpec.database,
          type: dbType
        }
      })
    }
  }

  const generateBackend = async () => {
    if (!backendSpec) return

    setIsGenerating(true)
    try {
      const generator = new BackendCodeGenerator(backendSpec.framework, backendSpec)
      const code = generator.generate()
      setGeneratedCode(code)
      onBackendGenerated?.(code)
      setActiveTab('preview')
    } catch (error) {
      console.error('Backend generation failed:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const deployBackend = async () => {
    if (!generatedCode) return

    setIsDeploying(true)
    try {
      // Simulate deployment
      await new Promise(resolve => setTimeout(resolve, 3000))
      const deployUrl = 'https://your-backend-api.railway.app'
      setDeploymentUrl(deployUrl)
      setActiveTab('deploy')
    } catch (error) {
      console.error('Deployment failed:', error)
    } finally {
      setIsDeploying(false)
    }
  }

  const tabs = [
    { id: 'templates', name: 'Templates', icon: Database },
    { id: 'config', name: 'Configuration', icon: Settings },
    { id: 'preview', name: 'Code Preview', icon: Code },
    { id: 'deploy', name: 'Deployment', icon: Server }
  ]

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Backend Builder</h2>
            <p className="text-sm text-gray-600">Generate complete backend APIs with databases</p>
          </div>
          <div className="flex items-center space-x-3">
            {backendSpec && (
              <button
                onClick={generateBackend}
                disabled={isGenerating}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
              >
                {isGenerating ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
                <span>{isGenerating ? 'Generating...' : 'Generate Backend'}</span>
              </button>
            )}
            {generatedCode && (
              <button
                onClick={deployBackend}
                disabled={isDeploying}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center space-x-2"
              >
                {isDeploying ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Server className="w-4 h-4" />
                )}
                <span>{isDeploying ? 'Deploying...' : 'Deploy API'}</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-6">
        {activeTab === 'templates' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Backend Templates</h3>
              <div className="grid grid-cols-1 gap-4">
                {templates.map((template) => (
                  <motion.div
                    key={template.id}
                    whileHover={{ scale: 1.02 }}
                    className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                      selectedTemplate === template.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => handleTemplateSelect(template.id)}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900">{template.name}</h4>
                        <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                        <div className="flex items-center space-x-2 mt-2">
                          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                            {template.framework}
                          </span>
                          {template.features.slice(0, 3).map((feature) => (
                            <span key={feature} className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded">
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                      {selectedTemplate === template.id && (
                        <Check className="w-5 h-5 text-blue-600" />
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'config' && backendSpec && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Backend Configuration</h3>
              
              {/* Framework Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">Framework</label>
                <div className="grid grid-cols-1 gap-3">
                  {frameworks.map((framework) => (
                    <div
                      key={framework.id}
                      className={`p-3 rounded-lg border cursor-pointer transition-all ${
                        backendSpec.framework === framework.id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => handleFrameworkChange(framework.id)}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="font-medium text-gray-900">{framework.name}</h4>
                          <p className="text-sm text-gray-600">{framework.description}</p>
                        </div>
                        {backendSpec.framework === framework.id && (
                          <Check className="w-5 h-5 text-blue-600" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Database Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">Database</label>
                <div className="grid grid-cols-1 gap-3">
                  {databases.map((database) => (
                    <div
                      key={database.id}
                      className={`p-3 rounded-lg border cursor-pointer transition-all ${
                        backendSpec.database.type === database.id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => handleDatabaseChange(database.id)}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="font-medium text-gray-900">{database.name}</h4>
                          <p className="text-sm text-gray-600">{database.description}</p>
                        </div>
                        {backendSpec.database.type === database.id && (
                          <Check className="w-5 h-5 text-blue-600" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* API Configuration */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">API Configuration</label>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Base Path</label>
                      <input
                        type="text"
                        value={backendSpec.api.basePath}
                        onChange={(e) => setBackendSpec({
                          ...backendSpec,
                          api: { ...backendSpec.api, basePath: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
                      <input
                        type="text"
                        value={backendSpec.api.version}
                        onChange={(e) => setBackendSpec({
                          ...backendSpec,
                          api: { ...backendSpec.api, version: e.target.value }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                      />
                    </div>
                  </div>
                  <div className="mt-4">
                    <p className="text-sm text-gray-600">
                      API will be available at: <code className="bg-gray-200 px-1 rounded">{backendSpec.api.basePath}</code>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'preview' && generatedCode && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Generated Backend Code</h3>
              
              {/* Framework Info */}
              <div className="mb-4 p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-blue-900">
                      {generatedCode.framework.charAt(0).toUpperCase() + generatedCode.framework.slice(1)} Backend
                    </h4>
                    <p className="text-sm text-blue-700">
                      {Object.keys(generatedCode.files).length} files generated
                    </p>
                  </div>
                  <Download className="w-5 h-5 text-blue-600" />
                </div>
              </div>

              {/* File Tree */}
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Generated Files:</h4>
                <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-auto">
                  {Object.entries(generatedCode.files).map(([filename, content]) => (
                    <details key={filename} className="mb-2">
                      <summary className="cursor-pointer font-mono text-sm text-gray-700 hover:text-gray-900">
                        📄 {filename}
                      </summary>
                      <pre className="mt-2 p-3 bg-white rounded border text-xs overflow-auto max-h-40">
                        <code>{content.slice(0, 500)}...</code>
                      </pre>
                    </details>
                  ))}
                </div>
              </div>

              {/* Dependencies */}
              <div className="mt-6">
                <h4 className="font-medium text-gray-900 mb-2">Dependencies:</h4>
                <div className="flex flex-wrap gap-2">
                  {generatedCode.dependencies.map((dep) => (
                    <span
                      key={dep.name}
                      className={`px-2 py-1 text-xs rounded ${
                        dep.type === 'production' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {dep.name}@{dep.version}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'deploy' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Deployment</h3>
              
              {deploymentUrl ? (
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Check className="w-5 h-5 text-green-600" />
                    <h4 className="font-medium text-green-900">Backend Deployed Successfully!</h4>
                  </div>
                  <p className="text-sm text-green-700 mt-1">
                    Your API is now live and ready to use.
                  </p>
                  <div className="mt-3 flex items-center space-x-3">
                    <a
                      href={deploymentUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1 text-sm text-green-600 hover:text-green-700"
                    >
                      <ExternalLink className="w-4 h-4" />
                      <span>View API</span>
                    </a>
                    <a
                      href={`${deploymentUrl}/api/docs`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1 text-sm text-green-600 hover:text-green-700"
                    >
                      <ExternalLink className="w-4 h-4" />
                      <span>API Documentation</span>
                    </a>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Server className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No deployment yet</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Generate your backend first, then deploy it to the cloud.
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}