'use client'

import { InterfaceSpec, ComponentSpec } from '@/types/builder'
import { motion } from 'framer-motion'

interface LivePreviewProps {
  spec: InterfaceSpec
}

export default function LivePreview({ spec }: LivePreviewProps) {
  const renderComponent = (component: ComponentSpec): JSX.Element => {
    switch (component.type) {
      case 'hero':
        return (
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
        )
      
      case 'features':
        return (
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
        )

      case 'pricing':
        return (
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
        )

      case 'cta':
        return (
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
        )

      default:
        return (
          <div key={component.id} className="p-4 border border-dashed border-gray-300 rounded">
            <p className="text-gray-500">Component: {component.type}</p>
          </div>
        )
    }
  }

  return (
    <div className="h-full overflow-auto bg-white">
      <div className="min-h-full">
        {spec.components.map(renderComponent)}
      </div>
    </div>
  )
}