'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Activity, 
  Zap, 
  Target, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle, 
  Clock,
  BarChart3,
  Lightbulb,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import { 
  PerformanceDashboard, 
  PerformanceAnalysis, 
  OptimizationSuggestion,
  PerformanceBudget,
  LiveMetrics
} from '@/lib/builder/performanceDashboard'
import { InterfaceSpec } from '@/types/builder'

interface PerformanceDashboardPanelProps {
  spec: InterfaceSpec
  deploymentUrl?: string
}

export default function PerformanceDashboardPanel({ spec, deploymentUrl }: PerformanceDashboardPanelProps) {
  const [analysis, setAnalysis] = useState<PerformanceAnalysis | null>(null)
  const [budget, setBudget] = useState<PerformanceBudget | null>(null)
  const [liveMetrics, setLiveMetrics] = useState<LiveMetrics | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [activeTab, setActiveTab] = useState<'overview' | 'suggestions' | 'budget' | 'live'>('overview')

  const dashboard = new PerformanceDashboard()

  useEffect(() => {
    analyzePerformance()
    generateBudget()
    
    if (deploymentUrl) {
      loadLiveMetrics()
    }
  }, [spec, deploymentUrl])

  const analyzePerformance = async () => {
    setIsAnalyzing(true)
    try {
      const result = await dashboard.analyzePerformance(spec)
      const suggestions = dashboard.getOptimizationSuggestions(spec)
      setAnalysis({ ...result, suggestions })
    } catch (error) {
      console.error('Performance analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const generateBudget = async () => {
    const result = dashboard.generatePerformanceBudget(spec)
    setBudget(result)
  }

  const loadLiveMetrics = async () => {
    if (!deploymentUrl) return
    
    try {
      const metrics = await dashboard.getLiveMetrics(deploymentUrl)
      setLiveMetrics(metrics)
    } catch (error) {
      console.error('Failed to load live metrics:', error)
    }
  }

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A': return 'text-green-600 bg-green-100'
      case 'B': return 'text-blue-600 bg-blue-100'
      case 'C': return 'text-yellow-600 bg-yellow-100'
      case 'D': return 'text-orange-600 bg-orange-100'
      case 'F': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'text-red-600 bg-red-100'
      case 'high': return 'text-orange-600 bg-orange-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getBudgetStatus = (item: any) => {
    const percentage = (item.current / item.max) * 100
    if (percentage <= 70) return 'good'
    if (percentage <= 90) return 'warning'
    return 'critical'
  }

  const getBudgetStatusColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const tabs = [
    { id: 'overview' as const, label: 'Overview', icon: BarChart3 },
    { id: 'suggestions' as const, label: 'Suggestions', icon: Lightbulb },
    { id: 'budget' as const, label: 'Budget', icon: Target },
    { id: 'live' as const, label: 'Live Metrics', icon: Activity }
  ]

  return (
    <div className="h-full bg-white">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-gray-700" />
          <h2 className="text-lg font-semibold text-gray-900">Performance Dashboard</h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Monitor and optimize your generated interface
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </nav>
      </div>

      <div className="p-6">
        {isAnalyzing && (
          <div className="flex items-center justify-center py-12">
            <div className="flex items-center space-x-3 text-gray-600">
              <Activity className="w-5 h-5 animate-spin" />
              <span>Analyzing performance...</span>
            </div>
          </div>
        )}

        {!isAnalyzing && (
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Overview Tab */}
            {activeTab === 'overview' && analysis && (
              <div className="space-y-6">
                {/* Performance Score */}
                <div className="text-center">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full text-2xl font-bold ${getGradeColor(analysis.grade)}`}>
                    {analysis.grade}
                  </div>
                  <div className="mt-2">
                    <div className="text-2xl font-bold text-gray-900">{analysis.score}/100</div>
                    <div className="text-sm text-gray-600">Performance Score</div>
                  </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Zap className="w-4 h-4 text-blue-500" />
                      <span className="text-sm font-medium text-gray-700">LCP</span>
                    </div>
                    <div className="text-xl font-bold text-gray-900 mt-1">
                      {analysis.metrics.loadTime.lcp.toFixed(1)}s
                    </div>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Target className="w-4 h-4 text-green-500" />
                      <span className="text-sm font-medium text-gray-700">FID</span>
                    </div>
                    <div className="text-xl font-bold text-gray-900 mt-1">
                      {analysis.metrics.loadTime.fid.toFixed(0)}ms
                    </div>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Activity className="w-4 h-4 text-purple-500" />
                      <span className="text-sm font-medium text-gray-700">CLS</span>
                    </div>
                    <div className="text-xl font-bold text-gray-900 mt-1">
                      {analysis.metrics.loadTime.cls.toFixed(3)}
                    </div>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <BarChart3 className="w-4 h-4 text-orange-500" />
                      <span className="text-sm font-medium text-gray-700">Bundle Size</span>
                    </div>
                    <div className="text-xl font-bold text-gray-900 mt-1">
                      {(analysis.metrics.bundleSize.total / 1024).toFixed(1)}MB
                    </div>
                  </div>
                </div>

                {/* Insights */}
                {analysis.insights.length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 mb-3">Key Insights</h3>
                    <div className="space-y-2">
                      {analysis.insights.map((insight, index) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                          <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5" />
                          <div>
                            <p className="text-sm text-blue-800">{insight.message}</p>
                            <p className="text-xs text-blue-600 mt-1">{insight.recommendation}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Suggestions Tab */}
            {activeTab === 'suggestions' && analysis && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-gray-900">Optimization Suggestions</h3>
                  <span className="text-xs text-gray-500">{analysis.suggestions.length} suggestions</span>
                </div>

                {analysis.suggestions.map((suggestion, index) => (
                  <div key={suggestion.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          <h4 className="text-sm font-medium text-gray-900">{suggestion.title}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(suggestion.priority)}`}>
                            {suggestion.priority}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                        
                        <div className="flex items-center space-x-4 mt-3">
                          <div className="flex items-center space-x-1">
                            <TrendingUp className="w-3 h-3 text-green-500" />
                            <span className="text-xs text-gray-600">Impact: {suggestion.impact}/10</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Clock className="w-3 h-3 text-blue-500" />
                            <span className="text-xs text-gray-600">Effort: {suggestion.effort}/10</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {analysis.suggestions.length === 0 && (
                  <div className="text-center py-8">
                    <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                    <h3 className="text-sm font-medium text-gray-900">No issues found!</h3>
                    <p className="text-sm text-gray-600">Your interface is well optimized.</p>
                  </div>
                )}
              </div>
            )}

            {/* Budget Tab */}
            {activeTab === 'budget' && budget && (
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-gray-900">Performance Budget</h3>

                {Object.entries(budget).map(([key, item]) => {
                  const status = getBudgetStatus(item)
                  const percentage = Math.min(100, (item.current / item.max) * 100)
                  
                  return (
                    <div key={key} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-sm font-medium text-gray-900 capitalize">
                          {key.replace(/([A-Z])/g, ' $1').trim()}
                        </h4>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getBudgetStatusColor(status)}`}>
                          {status}
                        </span>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">
                            {typeof item.current === 'number' ? item.current.toFixed(key.includes('Size') ? 0 : 2) : item.current}
                            {key.includes('Size') ? 'KB' : key.includes('lcp') || key.includes('fcp') ? 's' : key.includes('fid') ? 'ms' : ''}
                          </span>
                          <span className="text-gray-600">
                            Budget: {typeof item.max === 'number' ? item.max.toFixed(key.includes('Size') ? 0 : 2) : item.max}
                            {key.includes('Size') ? 'KB' : key.includes('lcp') || key.includes('fcp') ? 's' : key.includes('fid') ? 'ms' : ''}
                          </span>
                        </div>
                        
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              status === 'good' 
                                ? 'bg-green-500' 
                                : status === 'warning' 
                                ? 'bg-yellow-500' 
                                : 'bg-red-500'
                            }`}
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}

            {/* Live Metrics Tab */}
            {activeTab === 'live' && (
              <div className="space-y-6">
                {deploymentUrl ? (
                  liveMetrics ? (
                    <>
                      <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium text-gray-900">Live Performance</h3>
                        <span className="text-xs text-gray-500">
                          Last updated: {new Date(liveMetrics.timestamp).toLocaleTimeString()}
                        </span>
                      </div>

                      {/* Lighthouse Scores */}
                      <div className="grid grid-cols-2 gap-4">
                        {Object.entries(liveMetrics.lighthouse).map(([key, score]) => (
                          <div key={key} className="bg-gray-50 p-4 rounded-lg">
                            <div className="text-sm font-medium text-gray-700 capitalize mb-1">
                              {key.replace(/([A-Z])/g, ' $1').trim()}
                            </div>
                            <div className="text-2xl font-bold text-gray-900">{score}</div>
                          </div>
                        ))}
                      </div>

                      {/* Core Web Vitals */}
                      <div>
                        <h4 className="text-sm font-medium text-gray-900 mb-3">Core Web Vitals</h4>
                        <div className="grid grid-cols-3 gap-4">
                          <div className="text-center">
                            <div className="text-lg font-bold text-gray-900">{liveMetrics.metrics.lcp}s</div>
                            <div className="text-sm text-gray-600">LCP</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-gray-900">{liveMetrics.metrics.fid}ms</div>
                            <div className="text-sm text-gray-600">FID</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-gray-900">{liveMetrics.metrics.cls}</div>
                            <div className="text-sm text-gray-600">CLS</div>
                          </div>
                        </div>
                      </div>

                      {/* Uptime & Response Time */}
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-green-50 p-4 rounded-lg">
                          <div className="text-sm font-medium text-green-700">Uptime</div>
                          <div className="text-xl font-bold text-green-900">{liveMetrics.uptime}%</div>
                        </div>
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <div className="text-sm font-medium text-blue-700">Response Time</div>
                          <div className="text-xl font-bold text-blue-900">{liveMetrics.responseTime}ms</div>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-8">
                      <Activity className="w-8 h-8 text-gray-400 mx-auto mb-4 animate-spin" />
                      <p className="text-sm text-gray-600">Loading live metrics...</p>
                    </div>
                  )
                ) : (
                  <div className="text-center py-8">
                    <AlertCircle className="w-8 h-8 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-sm font-medium text-gray-900">No deployment available</h3>
                    <p className="text-sm text-gray-600">Deploy your interface to see live metrics</p>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  )
}