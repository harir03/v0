'use client'

import { useState, useRef, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Upload, Palette, Image, Type, Wand2, CheckCircle, AlertCircle } from 'lucide-react'
import { BrandIngestionService, BrandAssets, BrandColors } from '@/lib/builder/brandIngestion'
import { ThemeSpec } from '@/types/builder'

interface BrandIngestionPanelProps {
  onThemeGenerated: (theme: ThemeSpec) => void
}

export default function BrandIngestionPanel({ onThemeGenerated }: BrandIngestionPanelProps) {
  const [brandAssets, setBrandAssets] = useState<BrandAssets>({})
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResults, setAnalysisResults] = useState<{
    colors?: BrandColors
    theme?: ThemeSpec
  }>({})
  const [step, setStep] = useState<'upload' | 'configure' | 'results'>('upload')
  
  const logoInputRef = useRef<HTMLInputElement>(null)
  const screenshotInputRef = useRef<HTMLInputElement>(null)
  const brandService = new BrandIngestionService()

  const handleFileUpload = useCallback((file: File, type: 'logo' | 'screenshot') => {
    setBrandAssets(prev => ({
      ...prev,
      [type]: file
    }))
  }, [])

  const handleLogoUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      handleFileUpload(file, 'logo')
    }
  }

  const handleScreenshotUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      handleFileUpload(file, 'screenshot')
    }
  }

  const handleAnalyzeBrand = async () => {
    if (!brandAssets.logo && !brandAssets.brandName) return
    
    setIsAnalyzing(true)
    
    try {
      const theme = await brandService.generateThemeFromBrand(brandAssets)
      
      let colors: BrandColors | undefined
      if (brandAssets.logo) {
        colors = await brandService.extractColorsFromImage(brandAssets.logo)
      }
      
      setAnalysisResults({ colors, theme })
      setStep('results')
    } catch (error) {
      console.error('Brand analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleApplyTheme = () => {
    if (analysisResults.theme) {
      onThemeGenerated(analysisResults.theme)
      setStep('upload')
      setBrandAssets({})
      setAnalysisResults({})
    }
  }

  const ColorPalette = ({ colors }: { colors: BrandColors }) => (
    <div className="space-y-3">
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">Primary Colors</h4>
        <div className="flex space-x-2">
          {Object.values(colors.primary).slice(2, 8).map((color, index) => (
            <div
              key={index}
              className="w-8 h-8 rounded-lg border border-gray-200"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>
      
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">Secondary Colors</h4>
        <div className="flex space-x-2">
          {Object.values(colors.secondary).slice(2, 8).map((color, index) => (
            <div
              key={index}
              className="w-8 h-8 rounded-lg border border-gray-200"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>
      
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">Accent Colors</h4>
        <div className="flex space-x-2">
          {Object.values(colors.accent).slice(2, 8).map((color, index) => (
            <div
              key={index}
              className="w-8 h-8 rounded-lg border border-gray-200"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <div className="h-full bg-white">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Palette className="w-5 h-5 text-gray-700" />
          <h2 className="text-lg font-semibold text-gray-900">Brand Ingestion</h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Extract design tokens from your brand assets
        </p>
      </div>

      <div className="p-6">
        {step === 'upload' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Brand Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Brand Name
              </label>
              <input
                type="text"
                value={brandAssets.brandName || ''}
                onChange={(e) => setBrandAssets(prev => ({ ...prev, brandName: e.target.value }))}
                placeholder="Enter your brand name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Logo Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Logo / Brand Asset
              </label>
              <div
                onClick={() => logoInputRef.current?.click()}
                className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition-colors"
              >
                {brandAssets.logo ? (
                  <div className="space-y-2">
                    <CheckCircle className="w-8 h-8 text-green-500 mx-auto" />
                    <p className="text-sm text-gray-600">Logo uploaded: {brandAssets.logo.name}</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Image className="w-8 h-8 text-gray-400 mx-auto" />
                    <p className="text-sm text-gray-600">Click to upload logo or brand image</p>
                    <p className="text-xs text-gray-500">PNG, JPG, SVG up to 10MB</p>
                  </div>
                )}
              </div>
              <input
                ref={logoInputRef}
                type="file"
                accept="image/*"
                onChange={handleLogoUpload}
                className="hidden"
              />
            </div>

            {/* Industry & Style */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry
                </label>
                <select
                  value={brandAssets.industry || ''}
                  onChange={(e) => setBrandAssets(prev => ({ ...prev, industry: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select industry</option>
                  <option value="technology">Technology</option>
                  <option value="finance">Finance</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="education">Education</option>
                  <option value="retail">Retail</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="consulting">Consulting</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Style
                </label>
                <select
                  value={brandAssets.style || ''}
                  onChange={(e) => setBrandAssets(prev => ({ ...prev, style: e.target.value as any }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select style</option>
                  <option value="modern">Modern</option>
                  <option value="classic">Classic</option>
                  <option value="premium">Premium</option>
                  <option value="playful">Playful</option>
                </select>
              </div>
            </div>

            {/* Manual Colors */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Brand Colors (Optional)
              </label>
              <p className="text-xs text-gray-500 mb-2">
                Add existing brand colors if available
              </p>
              <div className="flex space-x-2">
                <input
                  type="color"
                  className="w-12 h-10 border border-gray-300 rounded-md"
                  onChange={(e) => {
                    const colors = brandAssets.colors || []
                    setBrandAssets(prev => ({ 
                      ...prev, 
                      colors: [...colors.slice(0, 0), e.target.value, ...colors.slice(1)] 
                    }))
                  }}
                />
                <input
                  type="color"
                  className="w-12 h-10 border border-gray-300 rounded-md"
                  onChange={(e) => {
                    const colors = brandAssets.colors || ['', '']
                    setBrandAssets(prev => ({ 
                      ...prev, 
                      colors: [...colors.slice(0, 1), e.target.value, ...colors.slice(2)] 
                    }))
                  }}
                />
                <input
                  type="color"
                  className="w-12 h-10 border border-gray-300 rounded-md"
                  onChange={(e) => {
                    const colors = brandAssets.colors || ['', '', '']
                    setBrandAssets(prev => ({ 
                      ...prev, 
                      colors: [...colors.slice(0, 2), e.target.value, ...colors.slice(3)] 
                    }))
                  }}
                />
              </div>
            </div>

            <button
              onClick={handleAnalyzeBrand}
              disabled={isAnalyzing || (!brandAssets.logo && !brandAssets.brandName)}
              className="w-full flex items-center justify-center space-x-2 px-4 py-3 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Wand2 className={`w-4 h-4 ${isAnalyzing ? 'animate-spin' : ''}`} />
              <span>
                {isAnalyzing ? 'Analyzing Brand...' : 'Generate Theme from Brand'}
              </span>
            </button>
          </motion.div>
        )}

        {step === 'results' && analysisResults.theme && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <h3 className="font-medium">Brand Analysis Complete</h3>
            </div>

            {/* Generated Theme Preview */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-900">Generated Theme</h4>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Primary Color</label>
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-8 h-8 rounded border border-gray-200"
                      style={{ backgroundColor: analysisResults.theme.primaryColor }}
                    />
                    <span className="text-sm text-gray-700">{analysisResults.theme.primaryColor}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Secondary Color</label>
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-8 h-8 rounded border border-gray-200"
                      style={{ backgroundColor: analysisResults.theme.secondaryColor }}
                    />
                    <span className="text-sm text-gray-700">{analysisResults.theme.secondaryColor}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Accent Color</label>
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-8 h-8 rounded border border-gray-200"
                      style={{ backgroundColor: analysisResults.theme.accentColor }}
                    />
                    <span className="text-sm text-gray-700">{analysisResults.theme.accentColor}</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-xs text-gray-600 mb-1">Font Family</label>
                  <div className="text-sm text-gray-700" style={{ fontFamily: analysisResults.theme.fontFamily }}>
                    {analysisResults.theme.fontFamily}
                  </div>
                </div>
              </div>
            </div>

            {/* Color Palette */}
            {analysisResults.colors && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">Extracted Color Palette</h4>
                <ColorPalette colors={analysisResults.colors} />
              </div>
            )}

            <div className="flex space-x-3">
              <button
                onClick={handleApplyTheme}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
              >
                Apply Theme
              </button>
              <button
                onClick={() => setStep('upload')}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Try Again
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}