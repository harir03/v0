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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-emerald-50">
      {/* Header */}
      <header className="border-b border-white/20 bg-white/80 backdrop-blur-md shadow-lg shadow-blue-500/10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Video className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-emerald-600 bg-clip-text text-transparent">
                  Vivid AI
                </h1>
              </div>
              <span className="text-sm text-slate-600 font-medium">Revolutionary AI Video Editor</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-slate-700 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
                <span className="text-blue-600 font-semibold">5</span> videos left this month
              </div>
              <button className="bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-700 hover:to-emerald-700 text-white px-6 py-2 rounded-xl font-semibold shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transition-all duration-200 transform hover:scale-105">
                Upgrade Pro
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Editor Area */}
          <div className="lg:col-span-2 space-y-8">
            {/* Upload Area */}
            <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/40 p-8 shadow-xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
                <Upload className="h-6 w-6 text-blue-600" />
                <span>Upload Your Video</span>
              </h2>
              
              <div className="border-2 border-dashed border-blue-300 rounded-xl p-8 text-center hover:border-emerald-400 transition-all duration-300 bg-gradient-to-br from-blue-50 to-emerald-50">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Upload className="h-8 w-8 text-white" />
                </div>
                <p className="text-slate-700 mb-2 font-semibold">Drop your video here or click to browse</p>
                <p className="text-sm text-slate-500 mb-6">Supports MP4, MOV, AVI up to 500MB</p>
                
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
                    <div className="bg-slate-200 rounded-full h-3 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-emerald-500 h-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                    <p className="text-sm text-slate-600 mt-2 font-medium">Uploading... {uploadProgress}%</p>
                  </div>
                )}
              </div>
            </div>

            {/* AI Processing Modes */}
            <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/40 p-8 shadow-xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
                <Brain className="h-6 w-6 text-emerald-600" />
                <span>Choose AI Processing Mode</span>
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <button
                  onClick={() => setActiveMode('style')}
                  className={`p-6 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
                    activeMode === 'style'
                      ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-blue-100 text-blue-700 shadow-lg shadow-blue-500/25'
                      : 'border-slate-200 bg-white/50 text-slate-700 hover:border-blue-300 hover:bg-blue-50/50 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'style' ? 'bg-blue-500' : 'bg-slate-400'
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
                      ? 'border-emerald-500 bg-gradient-to-br from-emerald-50 to-emerald-100 text-emerald-700 shadow-lg shadow-emerald-500/25'
                      : 'border-slate-200 bg-white/50 text-slate-700 hover:border-emerald-300 hover:bg-emerald-50/50 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'director' ? 'bg-emerald-500' : 'bg-slate-400'
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
                      ? 'border-purple-500 bg-gradient-to-br from-purple-50 to-purple-100 text-purple-700 shadow-lg shadow-purple-500/25'
                      : 'border-slate-200 bg-white/50 text-slate-700 hover:border-purple-300 hover:bg-purple-50/50 shadow-sm hover:shadow-md'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                    activeMode === 'discovery' ? 'bg-purple-500' : 'bg-slate-400'
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
                    <label className="block text-sm font-semibold text-slate-700 mb-3">
                      Creative Prompt
                    </label>
                    <textarea
                      value={creativePrompt}
                      onChange={(e) => setCreativePrompt(e.target.value)}
                      placeholder="Describe your vision... e.g., 'Make this travel vlog look like a dreamy, vintage 8mm film with light leaks and nostalgic feel'"
                      className="w-full bg-white/80 border-2 border-slate-200 rounded-xl px-4 py-4 text-slate-800 placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:bg-white transition-all duration-200 shadow-sm"
                      rows={4}
                    />
                  </div>
                  <div className="flex items-center space-x-6">
                    <label className="flex items-center space-x-3 text-sm text-slate-700 cursor-pointer">
                      <input type="checkbox" className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                      <span className="font-medium">Sync to audio beats</span>
                    </label>
                    <label className="flex items-center space-x-3 text-sm text-slate-700 cursor-pointer">
                      <input type="checkbox" className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                      <span className="font-medium">Allow duration changes</span>
                    </label>
                  </div>
                </div>
              )}

              {activeMode === 'discovery' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {aestheticSuggestions.map((suggestion) => (
                    <div key={suggestion.id} className="bg-white/80 rounded-xl p-5 border-2 border-slate-200 hover:border-purple-400 transition-all duration-300 cursor-pointer group transform hover:scale-105 shadow-sm hover:shadow-lg">
                      <div className="w-full h-28 bg-gradient-to-br from-purple-100 to-blue-100 rounded-lg mb-4 flex items-center justify-center group-hover:from-purple-200 group-hover:to-blue-200 transition-all duration-300">
                        <Play className="h-8 w-8 text-purple-600" />
                      </div>
                      <h4 className="font-bold text-slate-800 mb-2">{suggestion.title}</h4>
                      <p className="text-sm text-slate-600 mb-4">{suggestion.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-purple-600 font-semibold bg-purple-100 px-2 py-1 rounded-full">
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
            <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/40 p-6 shadow-xl shadow-blue-500/10">
              <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
                <Video className="h-5 w-5 text-blue-600" />
                <span>Recent Projects</span>
              </h2>
              
              <div className="space-y-4">
                {mockProjects.map((project) => (
                  <div key={project.id} className="bg-white/80 rounded-xl p-4 border border-slate-200 hover:border-blue-300 transition-all duration-200 hover:shadow-md group">
                    <div className="flex items-start space-x-4">
                      <div className="w-16 h-12 bg-gradient-to-br from-blue-100 to-emerald-100 rounded-lg flex items-center justify-center group-hover:from-blue-200 group-hover:to-emerald-200 transition-all duration-200">
                        <Play className="h-4 w-4 text-blue-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-slate-800 truncate">{project.name}</h3>
                        <p className="text-sm text-slate-600 font-medium">{project.duration} • {project.mode}</p>
                        <div className="flex items-center justify-between mt-3">
                          <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
                            project.status === 'completed' 
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-amber-100 text-amber-700'
                          }`}>
                            {project.status}
                          </span>
                          {project.viralScore && (
                            <div className="flex items-center space-x-1 bg-gradient-to-r from-yellow-50 to-orange-50 px-2 py-1 rounded-full">
                              <Star className="h-3 w-3 text-yellow-600" />
                              <span className="text-xs text-slate-700 font-semibold">{project.viralScore}</span>
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
            <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/40 p-6 shadow-xl shadow-blue-500/10">
              <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
                <Zap className="h-5 w-5 text-emerald-600" />
                <span>Quick Actions</span>
              </h2>
              
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-4 p-4 bg-white/80 hover:bg-blue-50 rounded-xl transition-all duration-200 border border-slate-200 hover:border-blue-300 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-emerald-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Download className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-slate-800 font-semibold">Export Latest</span>
                </button>
                <button className="w-full flex items-center space-x-4 p-4 bg-white/80 hover:bg-purple-50 rounded-xl transition-all duration-200 border border-slate-200 hover:border-purple-300 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Share className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-slate-800 font-semibold">Share to Social</span>
                </button>
                <button className="w-full flex items-center space-x-4 p-4 bg-white/80 hover:bg-emerald-50 rounded-xl transition-all duration-200 border border-slate-200 hover:border-emerald-300 group">
                  <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <Star className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-slate-800 font-semibold">View Analytics</span>
                </button>
              </div>
            </div>

            {/* Viral Score Predictor */}
            <div className="bg-gradient-to-br from-purple-100 via-blue-100 to-emerald-100 backdrop-blur-xl rounded-2xl border border-white/60 p-6 shadow-xl shadow-purple-500/20">
              <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
                <Star className="h-5 w-5 text-purple-600" />
                <span>Viral Prediction</span>
              </h2>
              <div className="text-center">
                <div className="text-5xl font-black bg-gradient-to-r from-purple-600 via-blue-600 to-emerald-600 bg-clip-text text-transparent mb-3">
                  87%
                </div>
                <p className="text-sm text-slate-700 mb-6 font-semibold">Predicted viral potential for your latest video</p>
                <div className="space-y-3 text-left">
                  <div className="flex justify-between text-sm bg-white/50 rounded-lg p-3 border border-white/60">
                    <span className="text-slate-700 font-semibold">Visual Appeal</span>
                    <span className="text-emerald-600 font-bold">95%</span>
                  </div>
                  <div className="flex justify-between text-sm bg-white/50 rounded-lg p-3 border border-white/60">
                    <span className="text-slate-700 font-semibold">Trend Alignment</span>
                    <span className="text-amber-600 font-bold">78%</span>
                  </div>
                  <div className="flex justify-between text-sm bg-white/50 rounded-lg p-3 border border-white/60">
                    <span className="text-slate-700 font-semibold">Engagement</span>
                    <span className="text-emerald-600 font-bold">89%</span>
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