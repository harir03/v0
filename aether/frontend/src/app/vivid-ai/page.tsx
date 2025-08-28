"use client"

import { useState, useCallback } from 'react'
import { Upload, Play, Zap, Sparkles, Brain, Video, Download, Share, Star } from 'lucide-react'

// Mock data for demonstration
const mockProjects = [
  {
    id: '1',
    name: 'Travel Vlog - Bali',
    thumbnail: '/api/placeholder/300/200',
    duration: '02:34',
    status: 'completed',
    mode: 'AI Director',
    viralScore: 87
  },
  {
    id: '2', 
    name: 'Product Demo',
    thumbnail: '/api/placeholder/300/200',
    duration: '01:15',
    status: 'processing',
    mode: 'Style Synthesis',
    viralScore: null
  },
  {
    id: '3',
    name: 'Wedding Highlights',
    thumbnail: '/api/placeholder/300/200', 
    duration: '04:22',
    status: 'completed',
    mode: 'Aesthetic Discovery',
    viralScore: 94
  }
]

const aestheticSuggestions = [
  {
    id: '1',
    title: 'Dreamy Nostalgic',
    description: 'Soft vintage film aesthetic with warm light leaks',
    thumbnail: '/api/placeholder/200/150',
    noveltyScore: 0.85
  },
  {
    id: '2',
    title: 'Cyberpunk Neon',
    description: 'Futuristic neon-soaked digital landscape',
    thumbnail: '/api/placeholder/200/150',
    noveltyScore: 0.92
  },
  {
    id: '3',
    title: 'Golden Hour Magic',
    description: 'Warm cinematic glow with dramatic shadows',
    thumbnail: '/api/placeholder/200/150',
    noveltyScore: 0.78
  }
]

export default function VividAIPage() {
  const [activeMode, setActiveMode] = useState<'style' | 'director' | 'discovery'>('director')
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null)
  const [creativePrompt, setCreativePrompt] = useState('')

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setIsUploading(true)
      setUploadProgress(0)
      
      // Simulate upload progress
      const interval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval)
            setIsUploading(false)
            return 100
          }
          return prev + 10
        })
      }, 200)
    }
  }, [])

  const handleProcessVideo = useCallback(() => {
    // This would call the actual API
    console.log('Processing video with mode:', activeMode)
    console.log('Creative prompt:', creativePrompt)
  }, [activeMode, creativePrompt])

  return (
    <div className="min-h-screen bg-aether-dark">
      {/* Header */}
      <header className="border-b border-aether-medium/50 bg-aether-dark/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Video className="h-8 w-8 text-aether-green" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-aether-green to-aether-pink bg-clip-text text-transparent">
                  Vivid AI
                </h1>
              </div>
              <span className="text-sm text-aether-beige">Revolutionary AI Video Editor</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-aether-light">
                <span className="text-aether-green font-semibold">5</span> videos left this month
              </div>
              <button className="bg-gradient-to-r from-aether-green to-aether-pink hover:from-aether-green/80 hover:to-aether-pink/80 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200">
                Upgrade Pro
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Editor Area */}
          <div className="lg:col-span-2 space-y-6">
            {/* Upload Area */}
            <div className="bg-aether-gray-800/50 backdrop-blur-sm rounded-xl border border-aether-medium/50 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Upload Your Video</h2>
              
              <div className="border-2 border-dashed border-aether-medium rounded-lg p-8 text-center hover:border-aether-green transition-colors duration-200">
                <Upload className="h-12 w-12 text-aether-beige mx-auto mb-4" />
                <p className="text-aether-light mb-2">Drop your video here or click to browse</p>
                <p className="text-sm text-aether-medium">Supports MP4, MOV, AVI up to 500MB</p>
                
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="video-upload"
                />
                <label
                  htmlFor="video-upload"
                  className="inline-block bg-aether-green hover:bg-aether-green/80 text-white px-6 py-2 rounded-lg mt-4 cursor-pointer transition-colors duration-200"
                >
                  Choose File
                </label>
                
                {isUploading && (
                  <div className="mt-4">
                    <div className="bg-aether-medium rounded-full h-2 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-aether-green to-aether-pink h-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                    <p className="text-sm text-aether-beige mt-2">Uploading... {uploadProgress}%</p>
                  </div>
                )}
              </div>
            </div>

            {/* AI Processing Modes */}
            <div className="bg-aether-gray-800/50 backdrop-blur-sm rounded-xl border border-aether-medium/50 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Choose AI Processing Mode</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <button
                  onClick={() => setActiveMode('style')}
                  className={`p-4 rounded-lg border transition-all duration-200 ${
                    activeMode === 'style'
                      ? 'border-aether-green bg-aether-green/20 text-aether-green'
                      : 'border-aether-medium bg-aether-gray-700/50 text-aether-light hover:border-aether-beige'
                  }`}
                >
                  <Zap className="h-6 w-6 mb-2" />
                  <h3 className="font-medium">Style Synthesis</h3>
                  <p className="text-sm opacity-80">Transfer style from reference video</p>
                </button>
                
                <button
                  onClick={() => setActiveMode('director')}
                  className={`p-4 rounded-lg border transition-all duration-200 ${
                    activeMode === 'director'
                      ? 'border-aether-green bg-aether-green/20 text-aether-green'
                      : 'border-aether-medium bg-aether-gray-700/50 text-aether-light hover:border-aether-beige'
                  }`}
                >
                  <Brain className="h-6 w-6 mb-2" />
                  <h3 className="font-medium">AI Director</h3>
                  <p className="text-sm opacity-80">Create effects from text prompts</p>
                </button>
                
                <button
                  onClick={() => setActiveMode('discovery')}
                  className={`p-4 rounded-lg border transition-all duration-200 ${
                    activeMode === 'discovery'
                      ? 'border-aether-green bg-aether-green/20 text-aether-green'
                      : 'border-aether-medium bg-aether-gray-700/50 text-aether-light hover:border-aether-beige'
                  }`}
                >
                  <Sparkles className="h-6 w-6 mb-2" />
                  <h3 className="font-medium">Aesthetic Discovery</h3>
                  <p className="text-sm opacity-80">AI suggests novel aesthetics</p>
                </button>
              </div>

              {/* Mode-specific Controls */}
              {activeMode === 'director' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Creative Prompt
                    </label>
                    <textarea
                      value={creativePrompt}
                      onChange={(e) => setCreativePrompt(e.target.value)}
                      placeholder="Describe your vision... e.g., 'Make this travel vlog look like a dreamy, vintage 8mm film with light leaks and nostalgic feel'"
                      className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:border-purple-500 transition-colors duration-200"
                      rows={3}
                    />
                  </div>
                  <div className="flex items-center space-x-4">
                    <label className="flex items-center space-x-2 text-sm text-slate-300">
                      <input type="checkbox" className="rounded border-slate-600 bg-slate-700" />
                      <span>Sync to audio beats</span>
                    </label>
                    <label className="flex items-center space-x-2 text-sm text-slate-300">
                      <input type="checkbox" className="rounded border-slate-600 bg-slate-700" />
                      <span>Allow duration changes</span>
                    </label>
                  </div>
                </div>
              )}

              {activeMode === 'discovery' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {aestheticSuggestions.map((suggestion) => (
                    <div key={suggestion.id} className="bg-slate-700/50 rounded-lg p-4 border border-slate-600 hover:border-purple-500 transition-colors duration-200 cursor-pointer">
                      <div className="w-full h-24 bg-slate-600 rounded-lg mb-3 flex items-center justify-center">
                        <Play className="h-6 w-6 text-slate-400" />
                      </div>
                      <h4 className="font-medium text-white">{suggestion.title}</h4>
                      <p className="text-sm text-slate-400 mb-2">{suggestion.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-purple-400">Novelty: {Math.round(suggestion.noveltyScore * 100)}%</span>
                        <button className="text-xs bg-purple-600 hover:bg-purple-700 text-white px-2 py-1 rounded transition-colors duration-200">
                          Apply
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <button
                onClick={handleProcessVideo}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02]"
              >
                Process with AI ✨
              </button>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Recent Projects */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Recent Projects</h2>
              
              <div className="space-y-4">
                {mockProjects.map((project) => (
                  <div key={project.id} className="bg-slate-700/50 rounded-lg p-4 border border-slate-600 hover:border-slate-500 transition-colors duration-200">
                    <div className="flex items-start space-x-3">
                      <div className="w-16 h-12 bg-slate-600 rounded flex items-center justify-center">
                        <Play className="h-4 w-4 text-slate-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-white truncate">{project.name}</h3>
                        <p className="text-sm text-slate-400">{project.duration} • {project.mode}</p>
                        <div className="flex items-center justify-between mt-2">
                          <span className={`text-xs px-2 py-1 rounded ${
                            project.status === 'completed' 
                              ? 'bg-gray-500/20 text-gray-400'
                              : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {project.status}
                          </span>
                          {project.viralScore && (
                            <div className="flex items-center space-x-1">
                              <Star className="h-3 w-3 text-yellow-400" />
                              <span className="text-xs text-slate-300">{project.viralScore}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
              
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors duration-200">
                  <Download className="h-5 w-5 text-purple-400" />
                  <span className="text-slate-300">Export Latest</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors duration-200">
                  <Share className="h-5 w-5 text-purple-400" />
                  <span className="text-slate-300">Share to Social</span>
                </button>
                <button className="w-full flex items-center space-x-3 p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors duration-200">
                  <Star className="h-5 w-5 text-purple-400" />
                  <span className="text-slate-300">View Analytics</span>
                </button>
              </div>
            </div>

            {/* Viral Score Predictor */}
            <div className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 backdrop-blur-sm rounded-xl border border-purple-500/20 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Viral Prediction</h2>
              <div className="text-center">
                <div className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                  87%
                </div>
                <p className="text-sm text-slate-300 mb-4">Predicted viral potential for your latest video</p>
                <div className="space-y-2 text-left">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Visual Appeal</span>
                    <span className="text-gray-400">95%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Trend Alignment</span>
                    <span className="text-yellow-400">78%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Engagement</span>
                    <span className="text-gray-400">89%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}