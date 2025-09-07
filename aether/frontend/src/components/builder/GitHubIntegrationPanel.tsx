'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Github, ExternalLink, GitBranch, Rocket, CheckCircle, AlertCircle, Clock } from 'lucide-react'
import { GitHubIntegrationService, RepositoryInfo, DeploymentConfig } from '@/lib/builder/githubIntegration'
import { InterfaceSpec } from '@/types/builder'

interface GitHubIntegrationPanelProps {
  spec: InterfaceSpec
  onSuccess?: (prUrl: string, deployUrl?: string) => void
}

export default function GitHubIntegrationPanel({ spec, onSuccess }: GitHubIntegrationPanelProps) {
  const [repositoryUrl, setRepositoryUrl] = useState('')
  const [branchName, setBranchName] = useState(`aether-${spec.id}`)
  const [prTitle, setPrTitle] = useState(`✨ Generated ${spec.name} via Aether Builder`)
  const [deploymentConfig, setDeploymentConfig] = useState<DeploymentConfig>({
    platform: 'vercel',
    environment: 'preview'
  })
  const [isValidating, setIsValidating] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [status, setStatus] = useState<'idle' | 'validating' | 'creating' | 'success' | 'error'>('idle')
  const [result, setResult] = useState<{ prUrl?: string; deployUrl?: string; error?: string }>({})

  const githubService = new GitHubIntegrationService()

  const handleValidateRepository = async () => {
    if (!repositoryUrl.trim()) return
    
    setIsValidating(true)
    setStatus('validating')
    
    try {
      const isValid = await githubService.validateRepository(repositoryUrl)
      if (isValid) {
        setStatus('idle')
      } else {
        setStatus('error')
        setResult({ error: 'Repository not accessible. Check URL and permissions.' })
      }
    } catch (error) {
      setStatus('error')
      setResult({ error: 'Failed to validate repository' })
    } finally {
      setIsValidating(false)
    }
  }

  const handleCreatePR = async () => {
    if (!repositoryUrl.trim()) return
    
    setIsCreating(true)
    setStatus('creating')
    
    try {
      const result = await githubService.createPR(spec, {
        repositoryUrl,
        branchName,
        title: prTitle,
        description: `Generated with Aether Builder\n\nComponents: ${spec.components.length}\nTheme: ${spec.theme.fontFamily}`
      })
      
      setStatus('success')
      setResult(result)
      onSuccess?.(result.prUrl, result.deployUrl)
    } catch (error) {
      setStatus('error')
      setResult({ error: 'Failed to create pull request' })
    } finally {
      setIsCreating(false)
    }
  }

  const StatusIcon = () => {
    switch (status) {
      case 'validating':
      case 'creating':
        return <Clock className="w-4 h-4 animate-spin text-blue-500" />
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      default:
        return <Github className="w-4 h-4 text-gray-500" />
    }
  }

  return (
    <div className="h-full bg-white">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Github className="w-5 h-5 text-gray-700" />
          <h2 className="text-lg font-semibold text-gray-900">GitHub Integration</h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Create a pull request with your generated code
        </p>
      </div>

      <div className="p-6 space-y-6">
        {/* Repository Configuration */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Repository URL
            </label>
            <div className="flex space-x-2">
              <input
                type="url"
                value={repositoryUrl}
                onChange={(e) => setRepositoryUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleValidateRepository}
                disabled={isValidating || !repositoryUrl.trim()}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isValidating ? 'Validating...' : 'Validate'}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Branch Name
            </label>
            <div className="flex items-center space-x-2">
              <GitBranch className="w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={branchName}
                onChange={(e) => setBranchName(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Pull Request Title
            </label>
            <input
              type="text"
              value={prTitle}
              onChange={(e) => setPrTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Deployment Configuration */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-900">Deployment Settings</h3>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Platform
            </label>
            <select
              value={deploymentConfig.platform}
              onChange={(e) => setDeploymentConfig(prev => ({ 
                ...prev, 
                platform: e.target.value as 'vercel' | 'netlify' | 'github-pages' 
              }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="vercel">Vercel</option>
              <option value="netlify">Netlify</option>
              <option value="github-pages">GitHub Pages</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Environment
            </label>
            <select
              value={deploymentConfig.environment}
              onChange={(e) => setDeploymentConfig(prev => ({ 
                ...prev, 
                environment: e.target.value as 'production' | 'preview' 
              }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="preview">Preview</option>
              <option value="production">Production</option>
            </select>
          </div>
        </div>

        {/* Status Display */}
        {status !== 'idle' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-lg border ${
              status === 'success' 
                ? 'bg-green-50 border-green-200' 
                : status === 'error'
                ? 'bg-red-50 border-red-200'
                : 'bg-blue-50 border-blue-200'
            }`}
          >
            <div className="flex items-start space-x-3">
              <StatusIcon />
              <div className="flex-1">
                {status === 'validating' && (
                  <p className="text-sm text-blue-700">Validating repository access...</p>
                )}
                {status === 'creating' && (
                  <p className="text-sm text-blue-700">Creating pull request and deployment...</p>
                )}
                {status === 'success' && (
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-green-700">Successfully created!</p>
                    {result.prUrl && (
                      <a
                        href={result.prUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-green-600 hover:text-green-800"
                      >
                        View Pull Request <ExternalLink className="w-3 h-3 ml-1" />
                      </a>
                    )}
                    {result.deployUrl && (
                      <a
                        href={result.deployUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-green-600 hover:text-green-800 ml-4"
                      >
                        View Deployment <ExternalLink className="w-3 h-3 ml-1" />
                      </a>
                    )}
                  </div>
                )}
                {status === 'error' && (
                  <p className="text-sm text-red-700">{result.error}</p>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Action Button */}
        <button
          onClick={handleCreatePR}
          disabled={isCreating || !repositoryUrl.trim() || status === 'success'}
          className="w-full flex items-center justify-center space-x-2 px-4 py-3 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Rocket className="w-4 h-4" />
          <span>
            {isCreating ? 'Creating Pull Request...' : 'Create Pull Request & Deploy'}
          </span>
        </button>

        {/* Generated Files Preview */}
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-900">Files to be created:</h3>
          <div className="text-xs text-gray-600 space-y-1">
            <div>📄 pages/{spec.id}.tsx</div>
            <div>🎨 styles/{spec.id}.module.css</div>
            <div>⚙️ spec/{spec.id}.json</div>
            <div>📦 package.json (dependencies)</div>
          </div>
        </div>
      </div>
    </div>
  )
}