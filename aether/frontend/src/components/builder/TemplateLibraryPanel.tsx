'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Layout, 
  ShoppingBag, 
  Briefcase, 
  User, 
  Rocket,
  Search,
  Star,
  Eye,
  Download,
  Tag
} from 'lucide-react'
import { TemplateLibrary, Template, TemplateCategory } from '@/lib/builder/templateLibrary'
import { InterfaceSpec } from '@/types/builder'

interface TemplateLibraryPanelProps {
  onTemplateSelect: (spec: InterfaceSpec) => void
}

export default function TemplateLibraryPanel({ onTemplateSelect }: TemplateLibraryPanelProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null)

  const templateLibrary = new TemplateLibrary()
  const categories = templateLibrary.getTemplates()

  // Filter templates based on category and search
  const filteredTemplates = categories.flatMap(category => 
    category.templates.filter(template => {
      const matchesCategory = selectedCategory === 'all' || category.id === selectedCategory
      const matchesSearch = !searchQuery || 
        template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        template.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      
      return matchesCategory && matchesSearch
    })
  )

  const handleTemplateSelect = (template: Template) => {
    const spec = templateLibrary.generateSpecFromTemplate(template.id)
    onTemplateSelect(spec)
  }

  const categoryIcons = {
    saas: Layout,
    ecommerce: ShoppingBag,
    portfolio: User,
    business: Briefcase,
    startup: Rocket
  }

  return (
    <div className="h-full bg-white">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Layout className="w-5 h-5 text-gray-700" />
          <h2 className="text-lg font-semibold text-gray-900">Template Library</h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Professional templates for every use case
        </p>
      </div>

      <div className="p-6">
        {/* Search */}
        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search templates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Categories */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-3 py-1.5 text-sm font-medium rounded-full transition-colors ${
                selectedCategory === 'all'
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Templates
            </button>
            {categories.map((category) => {
              const Icon = categoryIcons[category.id as keyof typeof categoryIcons] || Layout
              return (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-3 py-1.5 text-sm font-medium rounded-full transition-colors flex items-center space-x-1 ${
                    selectedCategory === category.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <Icon className="w-3 h-3" />
                  <span>{category.name}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Templates Grid */}
        <div className="space-y-4">
          {filteredTemplates.map((template) => (
            <motion.div
              key={template.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="text-sm font-semibold text-gray-900">{template.name}</h3>
                      <div className="flex items-center space-x-1">
                        <Star className="w-3 h-3 text-yellow-400 fill-current" />
                        <span className="text-xs text-gray-500">4.8</span>
                      </div>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                    
                    {/* Tags */}
                    <div className="flex flex-wrap gap-1 mb-3">
                      {template.tags.map((tag) => (
                        <span
                          key={tag}
                          className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>

                    {/* Template Features */}
                    <div className="text-xs text-gray-500 mb-3">
                      {template.components.length} components • 
                      Responsive • 
                      Accessible • 
                      {template.defaultTheme.fontFamily}
                    </div>

                    {/* Color Preview */}
                    <div className="flex items-center space-x-2 mb-4">
                      <span className="text-xs text-gray-600">Colors:</span>
                      <div className="flex space-x-1">
                        <div
                          className="w-4 h-4 rounded border border-gray-200"
                          style={{ backgroundColor: template.defaultTheme.primaryColor }}
                          title={template.defaultTheme.primaryColor}
                        />
                        <div
                          className="w-4 h-4 rounded border border-gray-200"
                          style={{ backgroundColor: template.defaultTheme.secondaryColor }}
                          title={template.defaultTheme.secondaryColor}
                        />
                        <div
                          className="w-4 h-4 rounded border border-gray-200"
                          style={{ backgroundColor: template.defaultTheme.accentColor }}
                          title={template.defaultTheme.accentColor}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Preview Image Placeholder */}
                  <div className="w-20 h-16 bg-gray-100 rounded border border-gray-200 flex items-center justify-center ml-4">
                    <Layout className="w-6 h-6 text-gray-400" />
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setPreviewTemplate(template)}
                      className="flex items-center space-x-1 text-xs text-gray-600 hover:text-gray-800"
                    >
                      <Eye className="w-3 h-3" />
                      <span>Preview</span>
                    </button>
                    <div className="flex items-center space-x-1 text-xs text-gray-500">
                      <Download className="w-3 h-3" />
                      <span>1.2k uses</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleTemplateSelect(template)}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Use Template
                  </button>
                </div>
              </div>
            </motion.div>
          ))}

          {filteredTemplates.length === 0 && (
            <div className="text-center py-12">
              <Layout className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-sm font-medium text-gray-900 mb-2">No templates found</h3>
              <p className="text-sm text-gray-600">
                {searchQuery 
                  ? `No templates match "${searchQuery}"`
                  : 'No templates available in this category'
                }
              </p>
            </div>
          )}
        </div>

        {/* Category Info */}
        {selectedCategory !== 'all' && (
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            {categories.find(cat => cat.id === selectedCategory) && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-1">
                  {categories.find(cat => cat.id === selectedCategory)?.name}
                </h4>
                <p className="text-sm text-gray-600">
                  {categories.find(cat => cat.id === selectedCategory)?.description}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Preview Modal */}
      {previewTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden"
          >
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">{previewTemplate.name}</h3>
                <button
                  onClick={() => setPreviewTemplate(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                <p className="text-gray-600">{previewTemplate.description}</p>
                
                {/* Components List */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Included Components</h4>
                  <div className="space-y-2">
                    {previewTemplate.components.map((component, index) => (
                      <div key={index} className="flex items-center space-x-2 text-sm">
                        <div className="w-2 h-2 bg-blue-500 rounded-full" />
                        <span className="capitalize text-gray-700">{component.type}</span>
                        <span className="text-gray-500">- {component.props?.title || 'Component'}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Theme Preview */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Default Theme</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Font:</span>
                      <span className="ml-2 font-medium">{previewTemplate.defaultTheme.fontFamily}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Colors:</span>
                      <div className="flex space-x-1 ml-2">
                        <div
                          className="w-4 h-4 rounded border"
                          style={{ backgroundColor: previewTemplate.defaultTheme.primaryColor }}
                        />
                        <div
                          className="w-4 h-4 rounded border"
                          style={{ backgroundColor: previewTemplate.defaultTheme.secondaryColor }}
                        />
                        <div
                          className="w-4 h-4 rounded border"
                          style={{ backgroundColor: previewTemplate.defaultTheme.accentColor }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex space-x-3 mt-6 pt-6 border-t border-gray-200">
                <button
                  onClick={() => setPreviewTemplate(null)}
                  className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                >
                  Close
                </button>
                <button
                  onClick={() => {
                    handleTemplateSelect(previewTemplate)
                    setPreviewTemplate(null)
                  }}
                  className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                >
                  Use This Template
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}