'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Code, 
  Eye, 
  Palette, 
  Settings, 
  Download, 
  Github, 
  Activity,
  Image,
  Layout,
  Zap,
  Server
} from 'lucide-react'
import CodeEditor from '@/components/builder/CodeEditor'
import LivePreview from '@/components/builder/LivePreview'
import ComponentLibrary from '@/components/builder/ComponentLibrary'
import ThemeCustomizer from '@/components/builder/ThemeCustomizer'
import GitHubIntegrationPanel from '@/components/builder/GitHubIntegrationPanel'
import BrandIngestionPanel from '@/components/builder/BrandIngestionPanel'
import PerformanceDashboardPanel from '@/components/builder/PerformanceDashboardPanel'
import TemplateLibraryPanel from '@/components/builder/TemplateLibraryPanel'
import ComponentDesignPanel from '@/components/builder/ComponentDesignPanel'
import BackendBuilderPanel from '@/components/builder/BackendBuilderPanel'
import { FrameworkSelector } from '@/components/builder/FrameworkSelector'
import { InterfaceSpec, CodeGenerationOptions, ComponentSpec } from '@/types/builder'
import { ComponentVariant } from '@/types/component-variants'

export default function BuilderPage() {
  const [activeTab, setActiveTab] = useState<'preview' | 'code' | 'components' | 'theme' | 'templates' | 'brand' | 'github' | 'performance' | 'backend'>('preview')
  const [currentFramework, setCurrentFramework] = useState<CodeGenerationOptions['framework']>('next')
  const [selectedComponent, setSelectedComponent] = useState<ComponentSpec | null>(null)
  const [currentSpec, setCurrentSpec] = useState<InterfaceSpec>({
    id: 'demo-landing',
    name: 'Demo Landing Page',
    type: 'page',
    components: [
      {
        id: 'navbar-1',
        type: 'navbar',
        props: {
          logoText: 'Aether',
          menuItems: ['Features', 'Pricing', 'About', 'Contact'],
          ctaButton: true,
          ctaText: 'Get Started'
        }
      },
      {
        id: 'hero-1',
        type: 'hero',
        props: {
          title: 'Build Amazing Websites',
          subtitle: 'Create beautiful, responsive websites with our AI-powered builder',
          ctaText: 'Get Started',
          ctaVariant: 'primary'
        }
      },
      {
        id: 'features-1',
        type: 'features',
        props: {
          title: 'Amazing Features',
          features: [
            {
              title: 'AI-Powered',
              description: 'Leverage artificial intelligence to build better websites faster'
            },
            {
              title: 'Responsive Design',
              description: 'Your websites look great on all devices automatically'
            },
            {
              title: 'Modern Stack',
              description: 'Built with the latest web technologies and best practices'
            }
          ]
        }
      },
      {
        id: 'pricing-1',
        type: 'pricing',
        props: {
          title: 'Simple Pricing',
          plans: [
            {
              name: 'Starter',
              price: 9,
              features: ['5 Projects', 'Basic Support', 'Templates'],
              featured: false
            },
            {
              name: 'Pro',
              price: 29,
              features: ['Unlimited Projects', 'Priority Support', 'Custom Components', 'AI Features'],
              featured: true
            },
            {
              name: 'Enterprise',
              price: 99,
              features: ['Everything in Pro', 'White Label', 'Custom Integrations', 'Dedicated Support'],
              featured: false
            }
          ]
        }
      },
      {
        id: 'cta-1',
        type: 'cta',
        props: {
          title: 'Ready to Get Started?',
          subtitle: 'Join thousands of developers building amazing websites',
          ctaText: 'Start Building Now'
        }
      },
      {
        id: 'footer-1',
        type: 'footer',
        props: {
          companyName: 'Aether',
          description: 'Building the future of web development with AI-powered tools.',
          links: ['About', 'Privacy', 'Terms', 'Support'],
          email: 'hello@aether.ai',
          phone: '+1 (555) 123-4567'
        }
      }
    ],
    theme: {
      primaryColor: '#3b82f6',
      backgroundColor: '#ffffff',
      textColor: '#1f2937',
      fontFamily: 'Inter'
    }
  })
  const [deploymentUrl, setDeploymentUrl] = useState<string>()

  const tabs = [
    { id: 'preview' as const, label: 'Preview', icon: Eye },
    { id: 'templates' as const, label: 'Templates', icon: Layout },
    { id: 'components' as const, label: 'Components', icon: Settings },
    { id: 'theme' as const, label: 'Theme', icon: Palette },
    { id: 'brand' as const, label: 'Brand', icon: Image },
    { id: 'backend' as const, label: 'Backend', icon: Server },
    { id: 'code' as const, label: 'Code', icon: Code },
    { id: 'performance' as const, label: 'Performance', icon: Activity },
    { id: 'github' as const, label: 'Deploy', icon: Github }
  ]

  const handleTemplateSelect = (spec: InterfaceSpec) => {
    setCurrentSpec(spec)
    setActiveTab('preview')
  }

  const handleThemeGenerated = (theme: any) => {
    setCurrentSpec(prev => ({ ...prev, theme }))
    setActiveTab('theme')
  }

  const handleDeploymentSuccess = (prUrl: string, deployUrl?: string) => {
    if (deployUrl) {
      setDeploymentUrl(deployUrl)
    }
    setActiveTab('performance')
  }

  const handleComponentSelect = (component: ComponentSpec) => {
    setSelectedComponent(component)
  }

  const handleVariantSelect = (variant: ComponentVariant) => {
    if (!selectedComponent) return
    
    // Convert variant styling to component styling format
    const convertedStyling: import('@/types/builder').ComponentStyling | undefined = variant.styling ? {
      spacing: variant.styling.spacing ? {
        padding: variant.styling.spacing === 'tight' ? '0.5rem' : 
                variant.styling.spacing === 'loose' ? '2rem' : '1rem',
        margin: variant.styling.spacing === 'tight' ? '0.25rem' : 
               variant.styling.spacing === 'loose' ? '1rem' : '0.5rem'
      } : undefined,
      colors: {
        background: variant.styling.background,
        text: variant.styling.textColor
      },
      layout: {
        display: variant.styling.layout === 'grid' ? 'grid' : 
                variant.styling.layout === 'flex' ? 'flex' : 'block'
      }
    } : undefined
    
    // Apply variant to the selected component
    const updatedSpec = {
      ...currentSpec,
      components: currentSpec.components.map(comp => 
        comp.id === selectedComponent.id 
          ? {
              ...comp,
              props: { ...comp.props, ...variant.props },
              styling: convertedStyling
            }
          : comp
      )
    }
    
    setCurrentSpec(updatedSpec)
    // Keep the component selected so user can see the changes
  }

  const handleDesignPanelClose = () => {
    setSelectedComponent(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-semibold text-gray-900">Aether Builder</h1>
            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
              v2.0 Beta
            </span>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Zap className="w-4 h-4" />
              <span>AI-Powered</span>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <FrameworkSelector 
              currentFramework={currentFramework}
              onFrameworkChange={setCurrentFramework}
            />
            <div className="text-sm text-gray-600">
              {currentSpec.components.length} components • {currentSpec.theme.fontFamily}
            </div>
            <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export Code</span>
            </button>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-73px)]">
        {/* Sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <nav className="flex-1 p-4">
            <div className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-50 text-blue-700 border-blue-200'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                    {tab.id === 'performance' && deploymentUrl && (
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                    )}
                  </button>
                )
              })}
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex">
          {/* Left Panel */}
          <div className="w-1/2 border-r border-gray-200">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              {activeTab === 'preview' && (
                <LivePreview 
                  spec={currentSpec} 
                  onComponentSelect={handleComponentSelect}
                  selectedComponent={selectedComponent}
                />
              )}
              {activeTab === 'templates' && (
                <TemplateLibraryPanel onTemplateSelect={handleTemplateSelect} />
              )}
              {activeTab === 'code' && (
                <CodeEditor 
                  spec={currentSpec} 
                  framework={currentFramework}
                  onChange={setCurrentSpec} 
                />
              )}
              {activeTab === 'components' && (
                <ComponentLibrary onAddComponent={(component) => {
                  setCurrentSpec(prev => ({
                    ...prev,
                    components: [...prev.components, component]
                  }))
                }} />
              )}
              {activeTab === 'theme' && (
                <ThemeCustomizer 
                  theme={currentSpec.theme}
                  onChange={(theme) => setCurrentSpec(prev => ({ ...prev, theme }))}
                />
              )}
              {activeTab === 'brand' && (
                <BrandIngestionPanel onThemeGenerated={handleThemeGenerated} />
              )}
              {activeTab === 'backend' && (
                <BackendBuilderPanel onBackendGenerated={(code) => {
                  console.log('Backend generated:', code)
                }} />
              )}
              {activeTab === 'github' && (
                <GitHubIntegrationPanel 
                  spec={currentSpec} 
                  onSuccess={handleDeploymentSuccess}
                />
              )}
              {activeTab === 'performance' && (
                <PerformanceDashboardPanel 
                  spec={currentSpec} 
                  deploymentUrl={deploymentUrl}
                />
              )}
            </motion.div>
          </div>

          {/* Right Panel - Always Preview */}
          <div className="w-1/2 relative">
            <LivePreview 
              spec={currentSpec} 
              onComponentSelect={handleComponentSelect}
              selectedComponent={selectedComponent}
            />
          </div>
        </div>

        {/* Component Design Panel - Overlay */}
        {selectedComponent && (
          <ComponentDesignPanel
            selectedComponent={selectedComponent}
            onVariantSelect={handleVariantSelect}
            onClose={handleDesignPanelClose}
          />
        )}
      </div>
    </div>
  )
}