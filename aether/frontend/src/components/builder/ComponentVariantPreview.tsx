'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Wand2, Palette, Eye } from 'lucide-react'

interface ComponentVariantPreviewProps {
  variant: any
  onSelect: () => void
  isSelected?: boolean
}

export default function ComponentVariantPreview({ 
  variant, 
  onSelect, 
  isSelected = false 
}: ComponentVariantPreviewProps) {
  const [isHovered, setIsHovered] = useState(false)

  const renderPreviewContent = () => {
    switch (variant.componentType) {
      case 'hero':
        return (
          <div className="relative w-full h-24 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-md overflow-hidden">
            <div className="p-3 text-center">
              <div className="h-2 bg-gray-800 rounded mb-1"></div>
              <div className="h-1 bg-gray-600 rounded mb-2 w-3/4 mx-auto"></div>
              <div className="h-1.5 bg-blue-600 rounded w-1/3 mx-auto"></div>
            </div>
          </div>
        )
      case 'navbar':
        return (
          <div className="relative w-full h-24 bg-white border rounded-md overflow-hidden">
            <div className="flex items-center justify-between p-3">
              <div className="h-2 bg-blue-600 rounded w-12"></div>
              <div className="flex space-x-2">
                <div className="h-1 bg-gray-400 rounded w-8"></div>
                <div className="h-1 bg-gray-400 rounded w-8"></div>
                <div className="h-1 bg-gray-400 rounded w-8"></div>
              </div>
              <div className="h-1.5 bg-blue-600 rounded w-10"></div>
            </div>
          </div>
        )
      case 'features':
        return (
          <div className="relative w-full h-24 bg-white rounded-md overflow-hidden">
            <div className="p-2">
              <div className="grid grid-cols-3 gap-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="text-center">
                    <div className="w-3 h-3 bg-blue-500 rounded-full mx-auto mb-1"></div>
                    <div className="h-0.5 bg-gray-400 rounded mb-0.5"></div>
                    <div className="h-0.5 bg-gray-300 rounded w-3/4 mx-auto"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )
      default:
        return (
          <div className="relative w-full h-24 bg-gray-100 rounded-md flex items-center justify-center">
            <Palette className="w-6 h-6 text-gray-400" />
          </div>
        )
    }
  }

  return (
    <motion.div
      className={`relative cursor-pointer group ${
        isSelected ? 'ring-2 ring-blue-500' : ''
      }`}
      onClick={onSelect}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200">
        {/* Preview */}
        <div className="mb-3">
          {renderPreviewContent()}
        </div>

        {/* Title and Description */}
        <div className="mb-2">
          <h4 className="font-medium text-sm text-gray-900 mb-1">
            {variant.name}
          </h4>
          <p className="text-xs text-gray-600 line-clamp-2">
            {variant.description}
          </p>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            {variant.styling?.layout && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                {variant.styling.layout}
              </span>
            )}
            {variant.styling?.size && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                {variant.styling.size}
              </span>
            )}
          </div>
          
          <div className="flex items-center space-x-1">
            {isSelected && <Sparkles className="w-3 h-3 text-blue-500" />}
            {isHovered && <Eye className="w-3 h-3 text-gray-400" />}
          </div>
        </div>

        {/* Hover Effects */}
        {isHovered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute inset-0 bg-blue-500/5 rounded-lg pointer-events-none"
          />
        )}
      </div>
    </motion.div>
  )
}