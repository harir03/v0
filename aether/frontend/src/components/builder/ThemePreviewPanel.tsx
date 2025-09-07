'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ThemeSpec } from '@/types/builder'
import { Palette, Eye, Check, Sparkles } from 'lucide-react'

interface ThemePreview {
  id: string
  name: string
  description: string
  theme: ThemeSpec
  category: 'light' | 'dark' | 'colorful' | 'minimal'
}

interface ThemePreviewPanelProps {
  currentTheme: ThemeSpec
  onThemeSelect: (theme: ThemeSpec) => void
  onThemePreview: (theme: ThemeSpec | null) => void
  isVisible: boolean
  onClose: () => void
}

const themePresets: ThemePreview[] = [
  // Light Themes
  {
    id: 'ocean-breeze',
    name: 'Ocean Breeze',
    description: 'Clean and professional with ocean-inspired blues',
    category: 'light',
    theme: {
      primaryColor: '#0ea5e9',
      secondaryColor: '#0284c7',
      accentColor: '#06b6d4',
      backgroundColor: '#ffffff',
      textColor: '#1f2937',
      fontFamily: 'Inter',
      borderRadius: '0.5rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', lg: '0 20px 25px -5px rgba(0, 0, 0, 0.1)' }
    }
  },
  {
    id: 'forest-green',
    name: 'Forest Green',
    description: 'Natural and calming with earth tones',
    category: 'light',
    theme: {
      primaryColor: '#10b981',
      secondaryColor: '#059669',
      accentColor: '#34d399',
      backgroundColor: '#f9fafb',
      textColor: '#111827',
      fontFamily: 'Poppins',
      borderRadius: '0.75rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', lg: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }
    }
  },
  {
    id: 'sunset-orange',
    name: 'Sunset Orange',
    description: 'Warm and energetic with sunset colors',
    category: 'colorful',
    theme: {
      primaryColor: '#f59e0b',
      secondaryColor: '#d97706',
      accentColor: '#fbbf24',
      backgroundColor: '#fffbeb',
      textColor: '#92400e',
      fontFamily: 'Montserrat',
      borderRadius: '1rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', lg: '0 20px 25px -5px rgba(0, 0, 0, 0.1)' }
    }
  },
  {
    id: 'royal-purple',
    name: 'Royal Purple',
    description: 'Luxurious and premium with purple gradients',
    category: 'colorful',
    theme: {
      primaryColor: '#8b5cf6',
      secondaryColor: '#7c3aed',
      accentColor: '#a78bfa',
      backgroundColor: '#faf5ff',
      textColor: '#581c87',
      fontFamily: 'Playfair Display',
      borderRadius: '0.5rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', md: '0 10px 15px -3px rgba(0, 0, 0, 0.1)', lg: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }
    }
  },
  // Dark Themes
  {
    id: 'midnight-blue',
    name: 'Midnight Blue',
    description: 'Professional dark theme with blue accents',
    category: 'dark',
    theme: {
      primaryColor: '#3b82f6',
      secondaryColor: '#1d4ed8',
      accentColor: '#60a5fa',
      backgroundColor: '#0f172a',
      textColor: '#f1f5f9',
      fontFamily: 'Inter',
      borderRadius: '0.5rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.4)', lg: '0 20px 25px -5px rgba(0, 0, 0, 0.5)' }
    }
  },
  {
    id: 'dark-emerald',
    name: 'Dark Emerald',
    description: 'Sophisticated dark theme with emerald highlights',
    category: 'dark',
    theme: {
      primaryColor: '#10b981',
      secondaryColor: '#047857',
      accentColor: '#34d399',
      backgroundColor: '#111827',
      textColor: '#f9fafb',
      fontFamily: 'Roboto',
      borderRadius: '0.75rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 3px 0 rgba(0, 0, 0, 0.4)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.5)', lg: '0 25px 50px -12px rgba(0, 0, 0, 0.6)' }
    }
  },
  {
    id: 'cyber-neon',
    name: 'Cyber Neon',
    description: 'Futuristic dark theme with neon accents',
    category: 'dark',
    theme: {
      primaryColor: '#06ffa5',
      secondaryColor: '#00d9ff',
      accentColor: '#ff0080',
      backgroundColor: '#000814',
      textColor: '#f8fafc',
      fontFamily: 'Orbitron',
      borderRadius: '0.25rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 0 10px rgba(6, 255, 165, 0.3)', md: '0 0 20px rgba(6, 255, 165, 0.2)', lg: '0 0 40px rgba(6, 255, 165, 0.1)' }
    }
  },
  // Minimal Themes
  {
    id: 'pure-minimal',
    name: 'Pure Minimal',
    description: 'Clean and minimal with subtle accents',
    category: 'minimal',
    theme: {
      primaryColor: '#374151',
      secondaryColor: '#1f2937',
      accentColor: '#6b7280',
      backgroundColor: '#ffffff',
      textColor: '#111827',
      fontFamily: 'Source Sans Pro',
      borderRadius: '0.25rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', md: '0 1px 3px 0 rgba(0, 0, 0, 0.1)', lg: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }
    }
  },
  {
    id: 'soft-gray',
    name: 'Soft Gray',
    description: 'Gentle grayscale with warm undertones',
    category: 'minimal',
    theme: {
      primaryColor: '#64748b',
      secondaryColor: '#475569',
      accentColor: '#94a3b8',
      backgroundColor: '#f8fafc',
      textColor: '#0f172a',
      fontFamily: 'Lato',
      borderRadius: '0.5rem',
      spacing: { xs: '0.25rem', sm: '0.5rem', md: '1rem', lg: '1.5rem', xl: '3rem' },
      shadows: { sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', lg: '0 20px 25px -5px rgba(0, 0, 0, 0.1)' }
    }
  }
]

export default function ThemePreviewPanel({ 
  currentTheme, 
  onThemeSelect, 
  onThemePreview,
  isVisible, 
  onClose 
}: ThemePreviewPanelProps) {
  const [activeCategory, setActiveCategory] = useState<'all' | 'light' | 'dark' | 'colorful' | 'minimal'>('all')
  const [previewTheme, setPreviewTheme] = useState<ThemeSpec | null>(null)

  const categories = [
    { id: 'all' as const, label: 'All Themes', count: themePresets.length },
    { id: 'light' as const, label: 'Light', count: themePresets.filter(t => t.category === 'light').length },
    { id: 'dark' as const, label: 'Dark', count: themePresets.filter(t => t.category === 'dark').length },
    { id: 'colorful' as const, label: 'Colorful', count: themePresets.filter(t => t.category === 'colorful').length },
    { id: 'minimal' as const, label: 'Minimal', count: themePresets.filter(t => t.category === 'minimal').length }
  ]

  const filteredThemes = activeCategory === 'all' 
    ? themePresets 
    : themePresets.filter(theme => theme.category === activeCategory)

  const handleThemeHover = (theme: ThemeSpec) => {
    setPreviewTheme(theme)
    onThemePreview(theme)
  }

  const handleThemeLeave = () => {
    setPreviewTheme(null)
    onThemePreview(null)
  }

  const handleThemeSelect = (theme: ThemeSpec) => {
    onThemeSelect(theme)
    setPreviewTheme(null)
    onThemePreview(null)
    onClose()
  }

  const isCurrentTheme = (theme: ThemeSpec) => {
    return theme.primaryColor === currentTheme.primaryColor &&
           theme.backgroundColor === currentTheme.backgroundColor &&
           theme.textColor === currentTheme.textColor
  }

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 overflow-hidden"
        >
          {/* Header */}
          <div className="p-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-white/20 rounded-lg">
                  <Palette className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">Theme Gallery</h3>
                  <p className="text-indigo-100 text-sm">Preview and select themes</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-1 hover:bg-white/20 rounded-md transition-colors"
              >
                <span className="sr-only">Close</span>
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Category Filter */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setActiveCategory(category.id)}
                  className={`px-3 py-1.5 text-sm rounded-full transition-all ${
                    activeCategory === category.id
                      ? 'bg-indigo-100 text-indigo-700 font-medium'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {category.label} ({category.count})
                </button>
              ))}
            </div>
          </div>

          {/* Theme Grid */}
          <div className="flex-1 overflow-y-auto p-4">
            <div className="space-y-4">
              {filteredThemes.map((themePreset) => (
                <motion.div
                  key={themePreset.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="group relative"
                >
                  <div
                    className={`p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 ${
                      isCurrentTheme(themePreset.theme)
                        ? 'border-green-500 bg-green-50'
                        : previewTheme === themePreset.theme
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
                    }`}
                    onMouseEnter={() => handleThemeHover(themePreset.theme)}
                    onMouseLeave={handleThemeLeave}
                    onClick={() => handleThemeSelect(themePreset.theme)}
                  >
                    {/* Theme Preview */}
                    <div 
                      className="h-24 rounded-lg mb-3 p-3 flex flex-col justify-between"
                      style={{ 
                        backgroundColor: themePreset.theme.backgroundColor,
                        color: themePreset.theme.textColor 
                      }}
                    >
                      {/* Header Bar */}
                      <div className="flex items-center justify-between">
                        <div className="flex space-x-1">
                          <div 
                            className="w-2 h-2 rounded-full"
                            style={{ backgroundColor: themePreset.theme.primaryColor }}
                          />
                          <div 
                            className="w-2 h-2 rounded-full opacity-60"
                            style={{ backgroundColor: themePreset.theme.secondaryColor }}
                          />
                          <div 
                            className="w-2 h-2 rounded-full opacity-40"
                            style={{ backgroundColor: themePreset.theme.accentColor }}
                          />
                        </div>
                        <div className="w-4 h-1 rounded" style={{ backgroundColor: themePreset.theme.primaryColor }} />
                      </div>
                      
                      {/* Content Area */}
                      <div className="space-y-1">
                        <div className="h-1.5 w-16 rounded" style={{ backgroundColor: themePreset.theme.primaryColor }} />
                        <div className="h-1 w-12 rounded opacity-60" style={{ backgroundColor: themePreset.theme.textColor }} />
                      </div>
                    </div>

                    {/* Theme Info */}
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900 mb-1">{themePreset.name}</h4>
                        <p className="text-sm text-gray-600 leading-tight">{themePreset.description}</p>
                        
                        {/* Color Palette */}
                        <div className="flex items-center space-x-2 mt-2">
                          <div className="flex space-x-1">
                            <div 
                              className="w-4 h-4 rounded border border-gray-200"
                              style={{ backgroundColor: themePreset.theme.primaryColor }}
                            />
                            <div 
                              className="w-4 h-4 rounded border border-gray-200"
                              style={{ backgroundColor: themePreset.theme.secondaryColor }}
                            />
                            <div 
                              className="w-4 h-4 rounded border border-gray-200"
                              style={{ backgroundColor: themePreset.theme.backgroundColor }}
                            />
                          </div>
                          <span className="text-xs text-gray-500 font-medium">
                            {themePreset.theme.fontFamily}
                          </span>
                        </div>
                      </div>

                      {/* Status Indicators */}
                      <div className="flex flex-col items-end space-y-2">
                        {isCurrentTheme(themePreset.theme) && (
                          <div className="flex items-center space-x-1 text-green-600">
                            <Check className="w-4 h-4" />
                            <span className="text-xs font-medium">Active</span>
                          </div>
                        )}
                        
                        {previewTheme === themePreset.theme && (
                          <div className="flex items-center space-x-1 text-indigo-600">
                            <Eye className="w-4 h-4" />
                            <span className="text-xs font-medium">Preview</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Hover Effects */}
                    <AnimatePresence>
                      {previewTheme === themePreset.theme && !isCurrentTheme(themePreset.theme) && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-xl border-2 border-indigo-500/20"
                        />
                      )}
                    </AnimatePresence>
                  </div>

                  {/* Quick Actions */}
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ 
                      opacity: previewTheme === themePreset.theme ? 1 : 0,
                      scale: previewTheme === themePreset.theme ? 1 : 0.8
                    }}
                    className="absolute top-2 right-2 flex items-center space-x-1"
                  >
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleThemeSelect(themePreset.theme)
                      }}
                      className="p-2 bg-indigo-600 text-white rounded-lg shadow-lg hover:bg-indigo-700 transition-colors"
                    >
                      <Sparkles className="w-4 h-4" />
                    </button>
                  </motion.div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <p className="text-xs text-gray-600 text-center">
              Hover to preview • Click to apply theme
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}