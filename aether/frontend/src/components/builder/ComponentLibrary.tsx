'use client'

import { ComponentSpec } from '@/types/builder'
import { Plus, Layout, Type, Image, Square, CreditCard, Grid3X3 } from 'lucide-react'

interface ComponentLibraryProps {
  onAddComponent: (component: ComponentSpec) => void
}

export default function ComponentLibrary({ onAddComponent }: ComponentLibraryProps) {
  const componentTemplates = [
    {
      id: 'hero',
      name: 'Hero Section',
      icon: Layout,
      description: 'Large banner with title, subtitle, and CTA',
      template: {
        type: 'hero' as const,
        props: {
          title: 'Your Amazing Title',
          subtitle: 'Compelling subtitle that explains your value proposition',
          ctaText: 'Get Started',
          ctaVariant: 'primary'
        }
      }
    },
    {
      id: 'features',
      name: 'Features Grid',
      icon: Grid3X3,
      description: 'Grid of feature cards with icons and descriptions',
      template: {
        type: 'features' as const,
        props: {
          title: 'Key Features',
          features: [
            {
              title: 'Fast & Reliable',
              description: 'Lightning-fast performance you can count on',
              icon: '⚡'
            },
            {
              title: 'Easy to Use',
              description: 'Intuitive interface designed for everyone',
              icon: '🎯'
            },
            {
              title: 'Secure',
              description: 'Enterprise-grade security built-in',
              icon: '🔒'
            }
          ]
        }
      }
    },
    {
      id: 'pricing',
      name: 'Pricing Table',
      icon: CreditCard,
      description: 'Pricing plans with features and CTAs',
      template: {
        type: 'pricing' as const,
        props: {
          title: 'Choose Your Plan',
          plans: [
            {
              name: 'Starter',
              price: 29,
              features: ['5 Projects', 'Email Support', 'Basic Analytics'],
              featured: false
            },
            {
              name: 'Pro',
              price: 99,
              features: ['Unlimited Projects', 'Priority Support', 'Advanced Analytics', 'Custom Domains'],
              featured: true
            },
            {
              name: 'Enterprise',
              price: 299,
              features: ['Everything in Pro', 'Dedicated Manager', 'Custom Integrations', 'SLA'],
              featured: false
            }
          ]
        }
      }
    },
    {
      id: 'cta',
      name: 'Call to Action',
      icon: Square,
      description: 'Prominent section to drive user action',
      template: {
        type: 'cta' as const,
        props: {
          title: 'Ready to Get Started?',
          subtitle: 'Join thousands of satisfied customers today',
          ctaText: 'Start Free Trial'
        }
      }
    }
  ]

  const addComponent = (template: any) => {
    const component: ComponentSpec = {
      id: `${template.type}-${Date.now()}`,
      type: template.type,
      props: template.props
    }
    onAddComponent(component)
  }

  return (
    <div className="h-full bg-white overflow-auto">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Component Library</h3>
        <p className="text-sm text-gray-600 mt-1">
          Drag and drop components to build your page
        </p>
      </div>

      <div className="p-4 space-y-3">
        {componentTemplates.map((component) => {
          const Icon = component.icon
          return (
            <div
              key={component.id}
              className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer group"
              onClick={() => addComponent(component.template)}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-colors">
                    <Icon className="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-900 mb-1">
                    {component.name}
                  </h4>
                  <p className="text-xs text-gray-500 mb-2">
                    {component.description}
                  </p>
                  <button className="inline-flex items-center text-xs text-blue-600 hover:text-blue-700 font-medium">
                    <Plus className="w-3 h-3 mr-1" />
                    Add Component
                  </button>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Categories */}
      <div className="p-4 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Categories</h4>
        <div className="space-y-2">
          {['Layout', 'Content', 'Forms', 'Media', 'Navigation', 'E-commerce'].map((category) => (
            <button
              key={category}
              className="block w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded transition-colors"
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* AI Generation */}
      <div className="p-4 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-900 mb-3">AI Generation</h4>
        <div className="space-y-3">
          <textarea
            placeholder="Describe the component you want to generate..."
            className="w-full p-3 border border-gray-200 rounded-lg text-sm resize-none"
            rows={3}
          />
          <button className="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
            Generate Component
          </button>
        </div>
      </div>
    </div>
  )
}