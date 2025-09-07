'use client'

import { InterfaceSpec, ComponentSpec } from '@/types/builder'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { Edit, MousePointer, Sparkles } from 'lucide-react'

interface LivePreviewProps {
  spec: InterfaceSpec
  onComponentSelect?: (component: ComponentSpec) => void
  selectedComponent?: ComponentSpec | null
}

export default function LivePreview({ spec, onComponentSelect, selectedComponent }: LivePreviewProps) {
  const [hoveredComponent, setHoveredComponent] = useState<string | null>(null)
  const renderComponent = (component: ComponentSpec): JSX.Element => {
    const isSelected = selectedComponent?.id === component.id
    const isHovered = hoveredComponent === component.id
    
    const handleComponentClick = (e: React.MouseEvent) => {
      e.stopPropagation()
      if (onComponentSelect) {
        onComponentSelect(component)
      }
    }

    const ComponentWrapper = ({ children }: { children: React.ReactNode }) => (
      <div
        className={`relative cursor-pointer transition-all duration-200 ${
          isSelected ? 'ring-2 ring-blue-500 ring-offset-2' : ''
        } ${isHovered ? 'ring-1 ring-blue-300 ring-offset-1' : ''}`}
        onClick={handleComponentClick}
        onMouseEnter={() => setHoveredComponent(component.id)}
        onMouseLeave={() => setHoveredComponent(null)}
      >
        {children}
        
        {/* Component Selection Overlay */}
        {(isHovered || isSelected) && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute inset-0 bg-blue-500/5 border border-blue-300/50 rounded-sm pointer-events-none"
          />
        )}
        
        {/* Component Label */}
        {(isHovered || isSelected) && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute -top-8 left-0 bg-blue-600 text-white text-xs px-2 py-1 rounded-md shadow-lg z-10"
          >
            <div className="flex items-center space-x-1">
              <Edit className="w-3 h-3" />
              <span className="capitalize">{component.type}</span>
              {isSelected && <Sparkles className="w-3 h-3" />}
            </div>
          </motion.div>
        )}
      </div>
    )

    switch (component.type) {
      case 'hero':
        return (
          <ComponentWrapper>
            <motion.section 
              key={component.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="px-6 py-20 text-center bg-gradient-to-br from-blue-50 to-indigo-100"
              style={{ 
                backgroundColor: spec.theme.backgroundColor,
                color: spec.theme.textColor 
              }}
            >
              <div className="max-w-4xl mx-auto">
                <h1 className="text-5xl font-bold mb-6" style={{ fontFamily: spec.theme.fontFamily }}>
                  {component.props.title}
                </h1>
                <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                  {component.props.subtitle}
                </p>
                <button 
                  className="px-8 py-3 text-lg font-semibold text-white rounded-lg transition-colors hover:opacity-90"
                  style={{ backgroundColor: spec.theme.primaryColor }}
                >
                  {component.props.ctaText}
                </button>
              </div>
            </motion.section>
          </ComponentWrapper>
        )
      
      case 'navbar':
        return (
          <ComponentWrapper>
            <motion.nav
              key={component.id}
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white border-b border-gray-200 px-6 py-4"
            >
              <div className="max-w-7xl mx-auto flex items-center justify-between">
                <div className="flex items-center space-x-8">
                  <div className="font-bold text-xl" style={{ color: spec.theme.primaryColor }}>
                    {component.props.logoText || 'Logo'}
                  </div>
                  <div className="hidden md:flex space-x-6">
                    {(component.props.menuItems || ['Home', 'About', 'Services', 'Contact']).map((item: string) => (
                      <a key={item} href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
                        {item}
                      </a>
                    ))}
                  </div>
                </div>
                {component.props.ctaButton && (
                  <button 
                    className="px-4 py-2 text-white rounded-md transition-colors hover:opacity-90"
                    style={{ backgroundColor: spec.theme.primaryColor }}
                  >
                    {component.props.ctaText || 'Get Started'}
                  </button>
                )}
              </div>
            </motion.nav>
          </ComponentWrapper>
        )
      
      case 'features':
        return (
          <ComponentWrapper>
            <motion.section 
              key={component.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="px-6 py-16"
            >
              <div className="max-w-6xl mx-auto">
                <h2 className="text-3xl font-bold text-center mb-12">
                  {component.props.title || 'Features'}
                </h2>
                <div className="grid md:grid-cols-3 gap-8">
                  {(component.props.features || []).map((feature: any, index: number) => (
                    <div key={index} className="text-center p-6 rounded-lg border border-gray-200">
                      <div className="w-12 h-12 mx-auto mb-4 rounded-lg flex items-center justify-center"
                           style={{ backgroundColor: spec.theme.primaryColor }}>
                        <span className="text-white text-xl">✦</span>
                      </div>
                      <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                      <p className="text-gray-600">{feature.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </motion.section>
          </ComponentWrapper>
        )

      case 'pricing':
        return (
          <ComponentWrapper>
            <motion.section 
              key={component.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="px-6 py-16 bg-gray-50"
            >
              <div className="max-w-4xl mx-auto text-center">
                <h2 className="text-3xl font-bold mb-12">
                  {component.props.title || 'Pricing'}
                </h2>
                <div className="grid md:grid-cols-3 gap-8">
                  {(component.props.plans || []).map((plan: any, index: number) => (
                    <div key={index} className={`bg-white p-8 rounded-lg border-2 ${
                      plan.featured ? 'border-blue-500 shadow-lg' : 'border-gray-200'
                    }`}>
                      <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
                      <div className="text-3xl font-bold mb-4">
                        ${plan.price}<span className="text-sm text-gray-500">/month</span>
                      </div>
                      <ul className="space-y-2 mb-6">
                        {plan.features.map((feature: string, idx: number) => (
                          <li key={idx} className="flex items-center">
                            <span className="text-green-500 mr-2">✓</span>
                            {feature}
                          </li>
                        ))}
                      </ul>
                      <button 
                        className={`w-full py-3 rounded-lg font-semibold transition-colors ${
                          plan.featured 
                            ? 'text-white' 
                            : 'text-gray-700 border border-gray-300 hover:bg-gray-50'
                        }`}
                        style={plan.featured ? { backgroundColor: spec.theme.primaryColor } : {}}
                      >
                        Choose Plan
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </motion.section>
          </ComponentWrapper>
        )

      case 'cta':
        return (
          <ComponentWrapper>
            <motion.section 
              key={component.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="px-6 py-20 text-center"
              style={{ backgroundColor: spec.theme.primaryColor }}
            >
              <div className="max-w-4xl mx-auto">
                <h2 className="text-4xl font-bold text-white mb-6">
                  {component.props.title}
                </h2>
                <p className="text-xl text-blue-100 mb-8">
                  {component.props.subtitle}
                </p>
                <button className="px-8 py-3 text-lg font-semibold bg-white rounded-lg transition-colors hover:bg-gray-100"
                        style={{ color: spec.theme.primaryColor }}>
                  {component.props.ctaText}
                </button>
              </div>
            </motion.section>
          </ComponentWrapper>
        )

      case 'footer':
        return (
          <ComponentWrapper>
            <motion.footer
              key={component.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-gray-900 text-white px-6 py-12"
            >
              <div className="max-w-7xl mx-auto">
                <div className="grid md:grid-cols-4 gap-8">
                  <div className="col-span-2">
                    <h3 className="text-xl font-bold mb-4">{component.props.companyName || 'Company'}</h3>
                    <p className="text-gray-400 mb-4">{component.props.description || 'Company description goes here.'}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-4">Links</h4>
                    <ul className="space-y-2">
                      {(component.props.links || ['About', 'Services', 'Contact']).map((link: string) => (
                        <li key={link}>
                          <a href="#" className="text-gray-400 hover:text-white transition-colors">{link}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-4">Contact</h4>
                    <div className="text-gray-400 space-y-2">
                      <p>{component.props.email || 'hello@company.com'}</p>
                      <p>{component.props.phone || '+1 (555) 123-4567'}</p>
                    </div>
                  </div>
                </div>
                <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
                  <p>&copy; 2024 {component.props.companyName || 'Company'}. All rights reserved.</p>
                </div>
              </div>
            </motion.footer>
          </ComponentWrapper>
        )

      default:
        return (
          <ComponentWrapper>
            <div key={component.id} className="p-4 border border-dashed border-gray-300 rounded">
              <p className="text-gray-500">Component: {component.type}</p>
            </div>
          </ComponentWrapper>
        )
    }
  }

  return (
    <div className="h-full overflow-auto bg-white relative">
      {/* Selection Guide */}
      {onComponentSelect && !selectedComponent && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-4 left-1/2 transform -translate-x-1/2 z-20 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg"
        >
          <div className="flex items-center space-x-2">
            <MousePointer className="w-4 h-4" />
            <span className="text-sm">Click on any component to customize its design</span>
          </div>
        </motion.div>
      )}
      
      <div className="min-h-full">
        {spec.components.map(renderComponent)}
      </div>
    </div>
  )
}