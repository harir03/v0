'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Palette, 
  Layout, 
  Type, 
  Image, 
  Zap,
  ChevronLeft,
  Eye,
  Code,
  Wand2
} from 'lucide-react'
import { ComponentSpec } from '@/types/builder'
import { ComponentVariant, COMPONENT_VARIANTS } from '@/types/component-variants'

interface ComponentDesignPanelProps {
  selectedComponent: ComponentSpec | null
  onVariantSelect: (variant: ComponentVariant) => void
  onClose: () => void
}

export default function ComponentDesignPanel({ 
  selectedComponent, 
  onVariantSelect, 
  onClose 
}: ComponentDesignPanelProps) {
  const [activeCategory, setActiveCategory] = useState<'variants' | 'styling' | 'content'>('variants')

  if (!selectedComponent) return null

  const variants = COMPONENT_VARIANTS[selectedComponent.type] || []

  const categories = [
    {
      id: 'variants' as const,
      name: 'Design Variants',
      icon: Layout,
      description: 'Choose from different design layouts'
    },
    {
      id: 'styling' as const,
      name: 'Styling',
      icon: Palette,
      description: 'Customize colors and spacing'
    },
    {
      id: 'content' as const,
      name: 'Content',
      icon: Type,
      description: 'Edit text and media content'
    }
  ]

  return (
    <AnimatePresence>
      <motion.div
        initial={{ x: 400, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 400, opacity: 0 }}
        transition={{ type: "spring", damping: 25, stiffness: 200 }}
        className="fixed right-0 top-0 h-full w-96 bg-white border-l border-gray-200 shadow-2xl z-50"
      >
        {/* Header */}
        <div className="border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <button
                onClick={onClose}
                className="p-1 hover:bg-gray-100 rounded-md transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <div>
                <h3 className="font-semibold text-gray-900 capitalize">
                  {selectedComponent.type} Design
                </h3>
                <p className="text-sm text-gray-500">
                  Customize your {selectedComponent.type} component
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-1">
              <button className="p-2 hover:bg-gray-100 rounded-md transition-colors">
                <Eye className="w-4 h-4" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-md transition-colors">
                <Code className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Category Tabs */}
        <div className="border-b border-gray-200">
          <div className="flex">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors relative ${
                  activeCategory === category.id
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-center space-x-1">
                  <category.icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{category.name}</span>
                </div>
                {activeCategory === category.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                  />
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeCategory === 'variants' && (
            <VariantsSection 
              variants={variants} 
              onVariantSelect={onVariantSelect}
              selectedComponent={selectedComponent}
            />
          )}
          
          {activeCategory === 'styling' && (
            <StylingSection selectedComponent={selectedComponent} />
          )}
          
          {activeCategory === 'content' && (
            <ContentSection selectedComponent={selectedComponent} />
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  )
}

interface VariantsSectionProps {
  variants: ComponentVariant[]
  onVariantSelect: (variant: ComponentVariant) => void
  selectedComponent: ComponentSpec
}

function VariantsSection({ variants, onVariantSelect, selectedComponent }: VariantsSectionProps) {
  if (variants.length === 0) {
    return (
      <div className="text-center py-8">
        <Wand2 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">No design variants available for this component type.</p>
        <p className="text-sm text-gray-400 mt-2">We're working on adding more variants!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="mb-4">
        <h4 className="font-medium text-gray-900 mb-2">Design Variants</h4>
        <p className="text-sm text-gray-600">
          Choose from {variants.length} pre-designed layouts for your {selectedComponent.type} component.
        </p>
      </div>

      <div className="grid gap-3">
        {variants.map((variant) => (
          <motion.button
            key={variant.id}
            onClick={() => onVariantSelect(variant)}
            className="group text-left p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="flex items-start justify-between mb-2">
              <h5 className="font-medium text-gray-900 group-hover:text-blue-900">
                {variant.name}
              </h5>
              <div className="flex items-center space-x-1">
                <div 
                  className="w-3 h-3 rounded-full border"
                  style={{ 
                    backgroundColor: variant.styling?.accentColor || '#3b82f6',
                    borderColor: variant.styling?.accentColor || '#3b82f6'
                  }}
                />
                <span className="text-xs text-gray-400 capitalize">
                  {variant.styling?.size || 'md'}
                </span>
              </div>
            </div>
            
            <p className="text-sm text-gray-600 mb-3">
              {variant.description}
            </p>
            
            <div className="bg-gray-100 rounded-md p-3 text-xs text-gray-500 font-mono">
              {variant.preview}
            </div>
            
            <div className="flex items-center justify-between mt-3">
              <div className="flex space-x-2">
                {variant.styling?.layout && (
                  <span className="px-2 py-1 bg-gray-100 text-xs text-gray-600 rounded">
                    {variant.styling.layout}
                  </span>
                )}
                {variant.styling?.spacing && (
                  <span className="px-2 py-1 bg-gray-100 text-xs text-gray-600 rounded">
                    {variant.styling.spacing}
                  </span>
                )}
              </div>
              <Wand2 className="w-4 h-4 text-gray-400 group-hover:text-blue-500" />
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  )
}

function StylingSection({ selectedComponent }: { selectedComponent: ComponentSpec }) {
  return (
    <div className="space-y-6">
      <div>
        <h4 className="font-medium text-gray-900 mb-4">Styling Options</h4>
        
        {/* Background */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Background
          </label>
          <div className="grid grid-cols-3 gap-2">
            {['bg-white', 'bg-gray-50', 'bg-blue-50', 'bg-gradient-to-r'].map((bg) => (
              <button
                key={bg}
                className="h-12 rounded-md border border-gray-200 hover:border-blue-300 transition-colors"
                style={{
                  background: bg.includes('gradient') 
                    ? 'linear-gradient(to right, #3b82f6, #1d4ed8)' 
                    : bg.replace('bg-', '')
                }}
              />
            ))}
          </div>
        </div>

        {/* Spacing */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Spacing
          </label>
          <div className="space-y-2">
            {['tight', 'normal', 'loose'].map((spacing) => (
              <button
                key={spacing}
                className="w-full text-left px-3 py-2 border border-gray-200 rounded-md hover:border-blue-300 hover:bg-blue-50 transition-colors"
              >
                <span className="font-medium capitalize">{spacing}</span>
                <span className="text-sm text-gray-500 ml-2">
                  {spacing === 'tight' ? 'Compact layout' : 
                   spacing === 'normal' ? 'Balanced spacing' : 
                   'Generous spacing'}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Border Radius */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Border Radius
          </label>
          <div className="grid grid-cols-4 gap-2">
            {[
              { name: 'none', value: 'rounded-none' },
              { name: 'sm', value: 'rounded-sm' },
              { name: 'md', value: 'rounded-md' },
              { name: 'lg', value: 'rounded-lg' }
            ].map((radius) => (
              <button
                key={radius.name}
                className={`h-12 bg-gray-100 border border-gray-200 hover:border-blue-300 transition-colors ${radius.value}`}
              >
                <span className="text-xs text-gray-600">{radius.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function ContentSection({ selectedComponent }: { selectedComponent: ComponentSpec }) {
  return (
    <div className="space-y-6">
      <div>
        <h4 className="font-medium text-gray-900 mb-4">Content Settings</h4>
        
        {/* Text Content */}
        {selectedComponent.props.title && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            <input
              type="text"
              defaultValue={selectedComponent.props.title}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        )}

        {selectedComponent.props.subtitle && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Subtitle
            </label>
            <textarea
              rows={3}
              defaultValue={selectedComponent.props.subtitle}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        )}

        {selectedComponent.props.ctaText && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Call-to-Action Text
            </label>
            <input
              type="text"
              defaultValue={selectedComponent.props.ctaText}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        )}

        {/* Media Settings */}
        <div className="border-t pt-4">
          <h5 className="font-medium text-gray-700 mb-3">Media & Images</h5>
          
          <div className="space-y-3">
            <button className="w-full flex items-center justify-center px-4 py-3 border border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors">
              <Image className="w-5 h-5 text-gray-400 mr-2" />
              <span className="text-sm text-gray-600">Upload Image</span>
            </button>
            
            <div className="grid grid-cols-2 gap-2">
              <button className="px-3 py-2 text-sm border border-gray-200 rounded-md hover:border-blue-300 hover:bg-blue-50">
                Stock Photos
              </button>
              <button className="px-3 py-2 text-sm border border-gray-200 rounded-md hover:border-blue-300 hover:bg-blue-50">
                AI Generate
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}