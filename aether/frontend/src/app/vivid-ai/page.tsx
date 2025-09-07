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
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-8 w-8 text-gray-900" />
                <span className="text-2xl font-bold text-gray-900">Vivid AI</span>
              </div>
              <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium">
                Beta
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-gray-900 transition-colors duration-200">
                Documentation
              </button>
              <button className="bg-gray-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200">
                Sign In
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            AI-Powered Video Editing
            <br />
            <span className="text-gray-600">That Actually Understands</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Vivid AI transforms your raw footage into cinematic masterpieces. Our AI doesn't just edit—it understands 
            your creative vision and elevates it beyond human capability.
          </p>
          
          {/* Mode Selection */}
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mb-12">
            <button
              onClick={() => setActiveMode('director')}
              className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2 ${
                activeMode === 'director' 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Brain className="h-5 w-5" />
              <span>AI Director Mode</span>
            </button>
            <button
              onClick={() => setActiveMode('style')}
              className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2 ${
                activeMode === 'style' 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Sparkles className="h-5 w-5" />
              <span>Style Synthesis</span>
            </button>
            <button
              onClick={() => setActiveMode('discovery')}
              className={`px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2 ${
                activeMode === 'discovery' 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Video className="h-5 w-5" />
              <span>Aesthetic Discovery</span>
            </button>
          </div>
        </div>

        {/* Upload Section */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-gray-400 transition-colors duration-200">
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Your Video</h3>
            <p className="text-gray-600 mb-6">
              Drop your video file here or click to browse. Supports MP4, MOV, AVI up to 2GB.
            </p>
            
            <input
              type="file"
              accept="video/*"
              onChange={handleFileUpload}
              className="hidden"
              id="video-upload"
            />
            <label
              htmlFor="video-upload"
              className="inline-block bg-gray-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200 cursor-pointer"
            >
              Choose File
            </label>
            
            {isUploading && (
              <div className="mt-6">
                <div className="bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gray-900 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mt-2">Uploading... {uploadProgress}%</p>
              </div>
            )}
          </div>
        </div>

        {/* Creative Prompt */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-white border border-gray-200 rounded-xl p-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Creative Direction</h3>
            <textarea
              value={creativePrompt}
              onChange={(e) => setCreativePrompt(e.target.value)}
              placeholder="Describe your vision... (e.g., 'Create a dreamy travel montage with golden hour lighting and smooth transitions')"
              className="w-full h-32 p-4 border border-gray-200 rounded-lg resize-none text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
            />
            <button
              onClick={handleProcessVideo}
              className="mt-4 bg-gray-900 text-white px-8 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200 flex items-center space-x-2"
            >
              <Zap className="h-5 w-5" />
              <span>Generate Video</span>
            </button>
          </div>
        </div>

        {/* Recent Projects */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Recent Projects</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockProjects.map((project) => (
              <div key={project.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow duration-200">
                <div className="aspect-video bg-gray-100 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Play className="h-12 w-12 text-gray-400" />
                  </div>
                  <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm">
                    {project.duration}
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">{project.name}</h3>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>{project.mode}</span>
                    {project.viralScore && (
                      <div className="flex items-center space-x-1">
                        <Star className="h-4 w-4 text-yellow-500" />
                        <span>{project.viralScore}% viral score</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Aesthetic Suggestions */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Trending Aesthetics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {aestheticSuggestions.map((aesthetic) => (
              <div key={aesthetic.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow duration-200">
                <div className="aspect-video bg-gray-100"></div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">{aesthetic.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{aesthetic.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">
                      {Math.round(aesthetic.noveltyScore * 100)}% novelty
                    </span>
                    <button className="text-gray-900 hover:text-gray-700 transition-colors duration-200">
                      Try Style →
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}