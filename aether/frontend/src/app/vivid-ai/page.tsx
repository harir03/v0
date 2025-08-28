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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-emerald-500/10 to-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-purple-500/5 to-emerald-500/5 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>
      
      {/* Header */}
      <header className="relative z-10 border-b border-gray-800/50 bg-black/80 backdrop-blur-md shadow-lg shadow-black/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Video className="h-8 w-8 text-blue-400" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-emerald-400 bg-clip-text text-transparent">
                  Vivid AI
                </h1>
              </div>
              <span className="text-sm text-gray-400 font-medium">Revolutionary AI Video Editor</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-300 bg-gray-900/50 px-3 py-1 rounded-full border border-gray-700">
                <span className="text-blue-400 font-semibold">5</span> videos left this month
              </div>
              <button className="bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-700 hover:to-emerald-700 text-white px-6 py-2 rounded-xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all duration-200 transform hover:scale-105">
                Upgrade Pro
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="relative z-10 container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Editor Area */}
          <div className="lg:col-span-2 space-y-8">
            {/* Upload Area */}
            <div className="bg-gray-900/70 backdrop-blur-xl rounded-2xl border border-gray-700/40 p-8 shadow-xl shadow-black/20">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center space-x-2">
                <Upload className="h-6 w-6 text-blue-400" />
                <span>Upload Your Video</span>
              </h2>
              
              <div className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-emerald-400 transition-all duration-300 bg-gradient-to-br from-gray-800/50 to-gray-700/50">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Upload className="h-8 w-8 text-white" />
                </div>
                <p className="text-gray-200 mb-2 font-semibold">Drop your video here or click to browse</p>
                <p className="text-sm text-gray-400 mb-6">Supports MP4, MOV, AVI up to 500MB</p>
                
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="video-upload"
                />
                <label
                  htmlFor="video-upload"
                  className="inline-block bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-700 hover:to-emerald-700 text-white px-8 py-3 rounded-xl font-semibold cursor-pointer shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all duration-200 transform hover:scale-105"
                >
                  Choose File
                </label>
                
                {isUploading && (
                  <div className="mt-6">
                    <div className="bg-gray-700 rounded-full h-3 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-emerald-500 h-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                    <p className="text-sm text-gray-300 mt-2 font-medium">Uploading... {uploadProgress}%</p>
                  </div>
                )}
              </div>
            </div>

            {/* AI Processing Modes */}
            <div className="bg-gray-900/70 backdrop-blur-xl rounded-2xl border border-gray-700/40 p-8 shadow-xl shadow-black/20">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center space-x-2">
                <Brain className="h-6 w-6 text-emerald-400" />
                <span>Choose AI Processing Mode</span>
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <button
                  onClick={() => setActiveMode('style')}
                  className={`p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
                    activeMode === 'style'
                      ? 'border-blue-500 bg-gradient-to-br from-blue-900/50 to-blue-800/50 text-blue-300 shadow-lg shadow-blue-500/25'
                      : 'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-blue-400 hover:bg-blue-900/30 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'style' ? 'bg-blue-500' : 'bg-gray-600'
                  }`}>
                    <Zap className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg mb-2">Style Synthesis</h3>
                  <p className="text-sm opacity-80">Transfer style from reference video</p>
                </button>
                
                <button
                  onClick={() => setActiveMode('director')}
                  className={`p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
                    activeMode === 'director'
                      ? 'border-emerald-500 bg-gradient-to-br from-emerald-900/50 to-emerald-800/50 text-emerald-300 shadow-lg shadow-emerald-500/25'
                      : 'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-emerald-400 hover:bg-emerald-900/30 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'director' ? 'bg-emerald-500' : 'bg-gray-600'
                  }`}>
                    <Brain className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg mb-2">AI Director</h3>
                  <p className="text-sm opacity-80">Create effects from text prompts</p>
                </button>
                
                <button
                  onClick={() => setActiveMode('discovery')}
                  className={`p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
                    activeMode === 'discovery'
                      ? 'border-purple-500 bg-gradient-to-br from-purple-900/50 to-purple-800/50 text-purple-300 shadow-lg shadow-purple-500/25'
                      : 'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-purple-400 hover:bg-purple-900/30 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'discovery' ? 'bg-purple-500' : 'bg-gray-600'
                  }`}>
                    <Sparkles className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg mb-2">Aesthetic Discovery</h3>
                  <p className="text-sm opacity-80">AI suggests novel aesthetics</p>
                </button>
              </div>

              {/* Mode-specific Controls */}
              {activeMode === 'director' && (
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-200 mb-3">
                      Creative Prompt
                    </label>
                    <textarea
                      value={creativePrompt}
                      onChange={(e) => setCreativePrompt(e.target.value)}
                      placeholder="Describe your vision... e.g., 'Make this travel vlog look like a dreamy, vintage 8mm film with light leaks and nostalgic feel'"
                      className="w-full bg-gray-800/80 border-2 border-gray-600 rounded-xl px-4 py-4 text-gray-200 placeholder-gray-400 focus:outline-none focus:border-emerald-500 focus:bg-gray-800 transition-all duration-200 shadow-sm"
                      rows={4}
                    />
                  </div>
                  <div className="flex items-center space-x-6">
                    <label className="flex items-center space-x-3 text-sm text-gray-300 cursor-pointer">
                      <input type="checkbox" className="w-4 h-4 rounded border-gray-600 text-blue-600 focus:ring-blue-500 bg-gray-700" />
                      <span className="font-medium">Sync to audio beats</span>
                    </label>
                    <label className="flex items-center space-x-3 text-sm text-gray-300 cursor-pointer">
                      <input type="checkbox" className="w-4 h-4 rounded border-gray-600 text-blue-600 focus:ring-blue-500 bg-gray-700" />
                      <span className="font-medium">Allow duration changes</span>
                    </label>
                  </div>
                </div>
              )}

              {activeMode === 'discovery' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {aestheticSuggestions.map((suggestion) => (
                    <div key={suggestion.id} className="bg-gray-800/80 rounded-xl p-5 border-2 border-gray-700 hover:border-purple-400 transition-all duration-300 cursor-pointer group transform hover:scale-105 shadow-sm hover:shadow-lg">
                      <div className="w-full h-28 bg-gradient-to-br from-purple-900/50 to-blue-900/50 rounded-lg mb-4 flex items-center justify-center group-hover:from-purple-800/50 group-hover:to-blue-800/50 transition-all duration-300">
                        <Play className="h-8 w-8 text-purple-400" />
                      </div>
                      <h4 className="font-bold text-gray-200 mb-2">{suggestion.title}</h4>
                      <p className="text-sm text-gray-400 mb-4">{suggestion.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-purple-300 font-semibold bg-purple-900/50 px-2 py-1 rounded-full">
                          Novelty: {Math.round(suggestion.noveltyScore * 100)}%
                        </span>
                        <button className="text-xs bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
                          Apply
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <button
                onClick={handleProcessVideo}
                className="w-full bg-gradient-to-r from-blue-600 via-emerald-600 to-purple-600 hover:from-blue-700 hover:via-emerald-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-[1.02] shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 text-lg"
              >
                Process with AI ✨
              </button>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Recent Projects */}
            <div className="bg-gray-900/70 backdrop-blur-xl rounded-2xl border border-gray-700/40 p-6 shadow-xl shadow-black/20">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
                <Video className="h-5 w-5 text-blue-400" />
                <span>Recent Projects</span>
              </h2>
              
              <div className="space-y-4">
                {mockProjects.map((project) => (
                  <div key={project.id} className="bg-gray-800/80 rounded-xl p-4 border border-gray-700 hover:border-blue-400 transition-all duration-200 hover:shadow-md group">
                    <div className="flex items-start space-x-4">
                      <div className="w-16 h-12 bg-gradient-to-br from-blue-900/50 to-emerald-900/50 rounded-lg flex items-center justify-center group-hover:from-blue-800/50 group-hover:to-emerald-800/50 transition-all duration-200">
                        <Play className="h-4 w-4 text-blue-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-200 truncate">{project.name}</h3>
                        <p className="text-sm text-gray-400 font-medium">{project.duration} • {project.mode}</p>
                        <div className="flex items-center justify-between mt-3">
                          <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
                            project.status === 'completed' 
                              ? 'bg-emerald-900/50 text-emerald-300'
                              : 'bg-amber-900/50 text-amber-300'
                          }`}>
                            {project.status}
                          </span>
                          {project.viralScore && (
                            <div className="flex items-center space-x-1 bg-gradient-to-r from-yellow-900/50 to-orange-900/50 px-2 py-1 rounded-full">
                              <Star className="h-3 w-3 text-yellow-400" />
                              <span className="text-xs text-gray-300 font-semibold">{project.viralScore}</span>
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
            <div className="bg-gray-900/70 backdrop-blur-xl rounded-2xl border border-gray-700/40 p-6 shadow-xl shadow-black/20">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
                <Zap className="h-5 w-5 text-emerald-400" />
                <span>Quick Actions</span>
              </h2>
              
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-4 p-4 bg-gray-800/80 hover:bg-blue-900/30 rounded-xl transition-all duration-200 border border-gray-700 hover:border-blue-400 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-emerald-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Download className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-gray-200 font-semibold">Export Latest</span>
                </button>
                <button className="w-full flex items-center space-x-4 p-4 bg-gray-800/80 hover:bg-purple-900/30 rounded-xl transition-all duration-200 border border-gray-700 hover:border-purple-400 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Share className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-gray-200 font-semibold">Share to Social</span>
                </button>
                <button className="w-full flex items-center space-x-4 p-4 bg-gray-800/80 hover:bg-emerald-900/30 rounded-xl transition-all duration-200 border border-gray-700 hover:border-emerald-400 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Star className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-gray-200 font-semibold">View Analytics</span>
                </button>
              </div>
            </div>

            {/* Viral Score Predictor */}
            <div className="bg-gradient-to-br from-purple-900/50 via-blue-900/50 to-emerald-900/50 backdrop-blur-xl rounded-2xl border border-gray-700/60 p-6 shadow-xl shadow-purple-500/20">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
                <Star className="h-5 w-5 text-purple-400" />
                <span>Viral Prediction</span>
              </h2>
              <div className="text-center">
                <div className="text-5xl font-black bg-gradient-to-r from-purple-400 via-blue-400 to-emerald-400 bg-clip-text text-transparent mb-3">
                  87%
                </div>
                <p className="text-sm text-gray-300 mb-6 font-semibold">Predicted viral potential for your latest video</p>
                <div className="space-y-3 text-left">
                  <div className="flex justify-between text-sm bg-gray-800/50 rounded-lg p-3 border border-gray-700/60">
                    <span className="text-gray-300 font-semibold">Visual Appeal</span>
                    <span className="text-emerald-400 font-bold">95%</span>
                  </div>
                  <div className="flex justify-between text-sm bg-gray-800/50 rounded-lg p-3 border border-gray-700/60">
                    <span className="text-gray-300 font-semibold">Trend Alignment</span>
                    <span className="text-amber-400 font-bold">78%</span>
                  </div>
                  <div className="flex justify-between text-sm bg-gray-800/50 rounded-lg p-3 border border-gray-700/60">
                    <span className="text-gray-300 font-semibold">Engagement</span>
                    <span className="text-emerald-400 font-bold">89%</span>
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