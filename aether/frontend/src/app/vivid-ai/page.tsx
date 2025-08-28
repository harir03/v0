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
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Subtle Background Pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900/20 via-transparent to-gray-800/20"></div>
      </div>
      
      {/* Enhanced Light Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Primary Light Nodes */}
        <div className="absolute top-20 left-20 w-3 h-3 bg-white rounded-full opacity-60 animate-pulse shadow-[0_0_20px_rgba(255,255,255,0.3)]"></div>
        <div className="absolute top-32 right-32 w-2 h-2 bg-gray-300 rounded-full opacity-80 animate-pulse delay-1000 shadow-[0_0_15px_rgba(255,255,255,0.2)]"></div>
        <div className="absolute bottom-40 left-16 w-4 h-4 bg-gray-200 rounded-full opacity-50 animate-pulse delay-500 shadow-[0_0_25px_rgba(255,255,255,0.25)]"></div>
        <div className="absolute bottom-20 right-20 w-3 h-3 bg-white rounded-full opacity-60 animate-pulse delay-300 shadow-[0_0_18px_rgba(255,255,255,0.3)]"></div>
        <div className="absolute top-1/2 left-10 w-2 h-2 bg-gray-300 rounded-full opacity-70 animate-pulse delay-700 shadow-[0_0_12px_rgba(255,255,255,0.2)]"></div>
        <div className="absolute top-1/3 right-16 w-3 h-3 bg-gray-200 rounded-full opacity-55 animate-pulse delay-200 shadow-[0_0_16px_rgba(255,255,255,0.25)]"></div>
        
        {/* Additional Light Points */}
        <div className="absolute top-1/4 left-1/3 w-2 h-2 bg-white rounded-full opacity-40 animate-pulse delay-800 shadow-[0_0_10px_rgba(255,255,255,0.2)]"></div>
        <div className="absolute bottom-1/3 right-1/4 w-3 h-3 bg-gray-300 rounded-full opacity-50 animate-pulse delay-400 shadow-[0_0_14px_rgba(255,255,255,0.2)]"></div>
        <div className="absolute top-1/2 right-1/3 w-2 h-2 bg-gray-200 rounded-full opacity-65 animate-pulse delay-600 shadow-[0_0_8px_rgba(255,255,255,0.15)]"></div>
        
        {/* Geometric Light Shapes */}
        <div className="absolute top-1/4 right-1/4 w-8 h-8 border border-gray-400/30 rounded-lg opacity-40 animate-pulse delay-1200 shadow-[0_0_20px_rgba(255,255,255,0.1)]"></div>
        <div className="absolute bottom-1/4 left-1/3 w-6 h-6 border border-gray-300/40 rounded-full opacity-35 animate-pulse delay-900 shadow-[0_0_15px_rgba(255,255,255,0.1)]"></div>
        
        {/* Connecting Light Lines */}
        <svg className="absolute inset-0 w-full h-full opacity-20">
          <defs>
            <linearGradient id="lightGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="rgba(255,255,255,0.1)" />
              <stop offset="50%" stopColor="rgba(255,255,255,0.3)" />
              <stop offset="100%" stopColor="rgba(255,255,255,0.1)" />
            </linearGradient>
          </defs>
          <line x1="20%" y1="20%" x2="80%" y2="32%" stroke="url(#lightGradient)" strokeWidth="1" opacity="0.3" className="animate-pulse delay-1000" />
          <line x1="16%" y1="40%" x2="33%" y2="25%" stroke="url(#lightGradient)" strokeWidth="1" opacity="0.2" className="animate-pulse delay-500" />
          <line x1="80%" y1="80%" x2="75%" y2="33%" stroke="url(#lightGradient)" strokeWidth="1" opacity="0.25" className="animate-pulse delay-700" />
        </svg>
      </div>

      {/* Enhanced Animated Background with Light Effects */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Large Gradient Orbs */}
        <div className="absolute top-1/4 left-1/4 w-[800px] h-[800px] bg-gradient-to-r from-gray-700/8 to-gray-600/8 rounded-full blur-3xl animate-pulse duration-[8s] shadow-[0_0_100px_rgba(255,255,255,0.02)]"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-gradient-to-r from-gray-800/6 to-gray-700/6 rounded-full blur-3xl animate-pulse delay-[4s] duration-[10s] shadow-[0_0_80px_rgba(255,255,255,0.015)]"></div>
        
        {/* Medium Glowing Elements */}
        <div className="absolute top-1/3 right-1/2 w-[400px] h-[400px] bg-gradient-to-r from-white/3 to-gray-300/3 rounded-full blur-2xl animate-pulse delay-[2s] duration-[12s] shadow-[0_0_60px_rgba(255,255,255,0.01)]"></div>
        <div className="absolute bottom-1/2 left-1/4 w-[300px] h-[300px] bg-gradient-to-r from-gray-200/4 to-white/4 rounded-full blur-2xl animate-pulse delay-[6s] duration-[9s] shadow-[0_0_50px_rgba(255,255,255,0.01)]"></div>
        
        {/* Subtle Light Rays */}
        <div className="absolute top-0 left-1/2 w-[2px] h-[200px] bg-gradient-to-b from-white/10 to-transparent opacity-30 animate-pulse delay-[3s] blur-sm"></div>
        <div className="absolute bottom-0 right-1/3 w-[1px] h-[150px] bg-gradient-to-t from-gray-300/15 to-transparent opacity-25 animate-pulse delay-[5s] blur-sm"></div>
      </div>
      
      {/* Header */}
      <header className="relative z-10 border-b border-gray-800/30 bg-black/80 backdrop-blur-sm">
        <div className="container mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Video className="h-6 w-6 text-white" />
              <h1 className="text-xl font-semibold text-white">Vivid AI</h1>
              <span className="text-sm text-gray-400">Revolutionary AI Video Editor</span>
            </div>
            <div className="flex items-center space-x-6">
              <span className="text-sm text-gray-400">5 videos left this month</span>
              <button className="bg-white text-black px-6 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                Upgrade Pro
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Hero Section */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-8 text-center">
        {/* Hero Content */}
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold text-white leading-tight">
            One-click for Video
            <br />
            <span className="bg-gradient-to-r from-gray-200 to-gray-400 bg-clip-text text-transparent">
              Creation
            </span>
          </h1>
          
          <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Dive into the art of video creation, where innovative AI technology meets creative expertise
          </p>
          
          <div className="flex items-center justify-center space-x-4 pt-6">
            <button className="bg-white text-black px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors flex items-center space-x-2">
              <span>Open App</span>
              <Play className="h-4 w-4" />
            </button>
            <button className="border border-gray-600 text-white px-8 py-3 rounded-lg font-semibold hover:border-gray-500 hover:bg-gray-900/50 transition-all">
              Discover More
            </button>
          </div>
        </div>
        
        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
          <div className="flex items-center space-x-2 text-gray-500 text-sm">
            <div className="w-6 h-6 border border-gray-600 rounded-full flex items-center justify-center">
              <div className="w-1 h-3 bg-gray-600 rounded-full animate-bounce"></div>
            </div>
            <span>Scroll down</span>
          </div>
        </div>
      </div>

      {/* Secondary Content */}
      <div className="relative z-10 container mx-auto px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 max-w-6xl mx-auto">
          {/* Upload Section */}
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-white mb-8">Upload Your Video</h2>
            
            <div className="border-2 border-dashed border-gray-700 rounded-2xl p-12 text-center hover:border-gray-600 transition-all duration-300 bg-gray-900/20">
              <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload className="h-8 w-8 text-gray-400" />
              </div>
              <p className="text-gray-300 mb-2 text-lg">Drop your video here or click to browse</p>
              <p className="text-sm text-gray-500 mb-8">Supports MP4, MOV, AVI up to 500MB</p>
              
              <input
                type="file"
                accept="video/*"
                onChange={handleFileUpload}
                className="hidden"
                id="video-upload"
              />
              <label
                htmlFor="video-upload"
                className="inline-block bg-white text-black px-8 py-3 rounded-lg font-semibold cursor-pointer hover:bg-gray-100 transition-colors"
              >
                Choose File
              </label>
              
              {isUploading && (
                <div className="mt-8">
                  <div className="bg-gray-800 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-white h-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-400 mt-3">Uploading... {uploadProgress}%</p>
                </div>
              )}
            </div>
          </div>

          {/* AI Processing Modes */}
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-white mb-8">Choose AI Processing Mode</h2>
            
            <div className="grid grid-cols-1 gap-4">
              <button
                onClick={() => setActiveMode('style')}
                className={`p-6 rounded-xl border transition-all duration-300 text-left ${
                  activeMode === 'style'
                    ? 'border-white bg-gray-900/40 text-white'
                    : 'border-gray-700 bg-gray-900/20 text-gray-300 hover:border-gray-600'
                }`}
              >
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    activeMode === 'style' ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'
                  }`}>
                    <Zap className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Style Synthesis</h3>
                    <p className="text-sm opacity-70">Transfer style from reference video</p>
                  </div>
                </div>
              </button>
              
              <button
                onClick={() => setActiveMode('director')}
                className={`p-6 rounded-xl border transition-all duration-300 text-left ${
                  activeMode === 'director'
                    ? 'border-white bg-gray-900/40 text-white'
                    : 'border-gray-700 bg-gray-900/20 text-gray-300 hover:border-gray-600'
                }`}
              >
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    activeMode === 'director' ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'
                  }`}>
                    <Brain className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">AI Director</h3>
                    <p className="text-sm opacity-70">Create effects from text prompts</p>
                  </div>
                </div>
              </button>
              
              <button
                onClick={() => setActiveMode('discovery')}
                className={`p-6 rounded-xl border transition-all duration-300 text-left ${
                  activeMode === 'discovery'
                    ? 'border-white bg-gray-900/40 text-white'
                    : 'border-gray-700 bg-gray-900/20 text-gray-300 hover:border-gray-600'
                }`}
              >
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    activeMode === 'discovery' ? 'bg-white text-black' : 'bg-gray-700 text-gray-400'
                  }`}>
                    <Sparkles className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Aesthetic Discovery</h3>
                    <p className="text-sm opacity-70">AI suggests novel aesthetics</p>
                  </div>
                </div>
              </button>
            </div>

            {/* Mode-specific Controls */}
            {activeMode === 'director' && (
              <div className="mt-8 space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Creative Prompt
                  </label>
                  <textarea
                    value={creativePrompt}
                    onChange={(e) => setCreativePrompt(e.target.value)}
                    placeholder="Describe your vision... e.g., 'Make this travel vlog look like a dreamy, vintage 8mm film with light leaks and nostalgic feel'"
                    className="w-full bg-gray-900/40 border border-gray-700 rounded-xl px-4 py-4 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-gray-500 transition-all duration-200"
                    rows={4}
                  />
                </div>
                <div className="flex items-center space-x-6">
                  <label className="flex items-center space-x-3 text-sm text-gray-400 cursor-pointer">
                    <input type="checkbox" className="w-4 h-4 rounded border-gray-600 text-white focus:ring-white bg-gray-800" />
                    <span>Sync to audio beats</span>
                  </label>
                  <label className="flex items-center space-x-3 text-sm text-gray-400 cursor-pointer">
                    <input type="checkbox" className="w-4 h-4 rounded border-gray-600 text-white focus:ring-white bg-gray-800" />
                    <span>Allow duration changes</span>
                  </label>
                </div>
              </div>
            )}

            <button
              onClick={handleProcessVideo}
              className="w-full bg-white text-black font-semibold py-4 px-8 rounded-xl hover:bg-gray-100 transition-colors text-lg mt-8"
            >
              Process with AI ✨
            </button>
          </div>
        </div>

        {/* Bottom Section - Stats */}
        <div className="mt-24 text-center">
          <h2 className="text-2xl font-bold text-white mb-12">Viral Prediction</h2>
          <div className="max-w-md mx-auto bg-gray-900/30 rounded-2xl p-8 border border-gray-800">
            <div className="text-6xl font-bold text-white mb-4">87%</div>
            <p className="text-gray-400 mb-6">Predicted viral potential for your latest video</p>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Visual Appeal</span>
                <span className="text-white font-semibold">95%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Trend Alignment</span>
                <span className="text-white font-semibold">78%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Engagement</span>
                <span className="text-white font-semibold">89%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}