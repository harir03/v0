'use client'

import { useState } from 'react'
import { ThemeSpec } from '@/types/builder'
import { Palette, Type, Layout, Sparkles } from 'lucide-react'

interface ThemeCustomizerProps {
  theme: ThemeSpec
  onChange: (theme: ThemeSpec) => void
}

export default function ThemeCustomizer({ theme, onChange }: ThemeCustomizerProps) {
  const [activeSection, setActiveSection] = useState<'colors' | 'typography' | 'spacing' | 'effects'>('colors')

  const updateTheme = (updates: Partial<ThemeSpec>) => {
    onChange({ ...theme, ...updates })
  }

  const colorPresets = [
    { name: 'Blue Ocean', primary: '#3b82f6', secondary: '#1e40af', bg: '#ffffff', text: '#1f2937' },
    { name: 'Purple Magic', primary: '#8b5cf6', secondary: '#7c3aed', bg: '#ffffff', text: '#1f2937' },
    { name: 'Green Nature', primary: '#10b981', secondary: '#059669', bg: '#ffffff', text: '#1f2937' },
    { name: 'Orange Sunset', primary: '#f59e0b', secondary: '#d97706', bg: '#ffffff', text: '#1f2937' },
    { name: 'Dark Mode', primary: '#6366f1', secondary: '#4f46e5', bg: '#111827', text: '#f9fafb' },
  ]

  const fontFamilies = [
    'Inter',
    'Roboto',
    'Poppins',
    'Montserrat',
    'Open Sans',
    'Lato',
    'Source Sans Pro',
    'Nunito'
  ]

  return (
    <div className="h-full bg-white overflow-auto">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Theme Customizer</h3>
        <p className="text-sm text-gray-600 mt-1">
          Customize colors, typography, and spacing
        </p>
      </div>

      {/* Section Tabs */}
      <div className="border-b border-gray-200">
        <div className="flex">
          {[
            { id: 'colors' as const, label: 'Colors', icon: Palette },
            { id: 'typography' as const, label: 'Typography', icon: Type },
            { id: 'spacing' as const, label: 'Layout', icon: Layout },
            { id: 'effects' as const, label: 'Effects', icon: Sparkles }
          ].map((section) => {
            const Icon = section.icon
            return (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex-1 flex items-center justify-center space-x-2 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeSection === section.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{section.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      <div className="p-4">
        {/* Colors Section */}
        {activeSection === 'colors' && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-3">Color Presets</h4>
              <div className="grid grid-cols-1 gap-2">
                {colorPresets.map((preset) => (
                  <button
                    key={preset.name}
                    onClick={() => updateTheme({
                      primaryColor: preset.primary,
                      secondaryColor: preset.secondary,
                      backgroundColor: preset.bg,
                      textColor: preset.text
                    })}
                    className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                  >
                    <div className="flex space-x-1">
                      <div className="w-4 h-4 rounded" style={{ backgroundColor: preset.primary }} />
                      <div className="w-4 h-4 rounded" style={{ backgroundColor: preset.secondary }} />
                      <div className="w-4 h-4 rounded border border-gray-200" style={{ backgroundColor: preset.bg }} />
                    </div>
                    <span className="text-sm font-medium">{preset.name}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Primary Color
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={theme.primaryColor}
                    onChange={(e) => updateTheme({ primaryColor: e.target.value })}
                    className="w-12 h-10 border border-gray-300 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={theme.primaryColor}
                    onChange={(e) => updateTheme({ primaryColor: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Background Color
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={theme.backgroundColor}
                    onChange={(e) => updateTheme({ backgroundColor: e.target.value })}
                    className="w-12 h-10 border border-gray-300 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={theme.backgroundColor}
                    onChange={(e) => updateTheme({ backgroundColor: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Text Color
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={theme.textColor}
                    onChange={(e) => updateTheme({ textColor: e.target.value })}
                    className="w-12 h-10 border border-gray-300 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={theme.textColor}
                    onChange={(e) => updateTheme({ textColor: e.target.value })}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Typography Section */}
        {activeSection === 'typography' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Font Family
              </label>
              <select
                value={theme.fontFamily}
                onChange={(e) => updateTheme({ fontFamily: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                {fontFamilies.map((font) => (
                  <option key={font} value={font} style={{ fontFamily: font }}>
                    {font}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Font Preview
              </label>
              <div className="p-4 border border-gray-200 rounded-lg" style={{ fontFamily: theme.fontFamily }}>
                <h1 className="text-2xl font-bold mb-2">Heading Text</h1>
                <p className="text-base mb-2">Regular paragraph text with normal weight.</p>
                <p className="text-sm text-gray-600">Small text for captions and labels.</p>
              </div>
            </div>
          </div>
        )}

        {/* Spacing Section */}
        {activeSection === 'spacing' && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Border Radius
              </label>
              <input
                type="range"
                min="0"
                max="24"
                value={parseInt(theme.borderRadius || '8')}
                onChange={(e) => updateTheme({ borderRadius: `${e.target.value}px` })}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0px</span>
                <span>{theme.borderRadius || '8px'}</span>
                <span>24px</span>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">Preview</h4>
              <div className="space-y-3">
                <div 
                  className="p-4 bg-gray-100 border"
                  style={{ borderRadius: theme.borderRadius }}
                >
                  Card with current border radius
                </div>
                <button 
                  className="px-4 py-2 bg-blue-600 text-white"
                  style={{ borderRadius: theme.borderRadius }}
                >
                  Button Preview
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Effects Section */}
        {activeSection === 'effects' && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">Shadow Styles</h4>
              <div className="space-y-3">
                {['none', 'sm', 'md', 'lg', 'xl'].map((size) => (
                  <div
                    key={size}
                    className={`p-4 bg-white border border-gray-200 rounded-lg cursor-pointer hover:border-blue-300 transition-colors shadow-${size}`}
                  >
                    Shadow {size}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}