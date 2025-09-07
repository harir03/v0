import { InterfaceSpec, ComponentSpec, GeneratedCode } from '@/types/builder'
import { FrameworkCodeGenerator } from './base'

/**
 * React/Next.js code generator (existing implementation, refactored)
 */
export class ReactCodeGenerator extends FrameworkCodeGenerator {
  
  generatePage(spec: InterfaceSpec): GeneratedCode {
    const imports = this.generateImports(spec)
    const components = this.generateComponents(spec.components)
    const styles = this.generateStyles(spec)
    const typescript = this.generatePageCode(spec, imports, components)

    return {
      typescript,
      css: styles,
      dependencies: this.getDependencies(spec),
      imports: imports
    }
  }

  generateComponent(component: ComponentSpec, theme: any): string {
    switch (component.type) {
      case 'hero':
        return this.generateHeroComponent(component, theme)
      case 'features':
        return this.generateFeaturesComponent(component, theme)
      case 'pricing':
        return this.generatePricingComponent(component, theme)
      case 'cta':
        return this.generateCTAComponent(component, theme)
      case 'button':
        return this.generateButtonComponent(component, theme)
      default:
        return this.generateGenericComponent(component, theme)
    }
  }

  generateImports(spec: InterfaceSpec): string[] {
    const imports = [
      "import React, { useState, useEffect } from 'react'"
    ]

    if (this.options.framework === 'next') {
      imports.push("import Image from 'next/image'")
      imports.push("import Link from 'next/link'")
    }

    // Add framework-specific imports
    if (this.hasAnimations(spec)) {
      imports.push("import { motion } from 'framer-motion'")
    }

    return imports
  }

  getDependencies(spec: InterfaceSpec): string[] {
    const deps = []

    if (this.options.framework === 'next') {
      deps.push('next@^14.0.0', 'react@^18.0.0', 'react-dom@^18.0.0')
    } else {
      deps.push('react@^18.0.0', 'react-dom@^18.0.0', '@vitejs/plugin-react@^4.1.0', 'vite@^4.4.0')
    }

    if (this.options.typescript) {
      deps.push('typescript@^5.0.0', '@types/react@^18.0.0', '@types/react-dom@^18.0.0')
    }

    if (this.options.styling === 'tailwind') {
      deps.push('tailwindcss@^3.3.0', 'autoprefixer@^10.4.0', 'postcss@^8.4.0')
    }

    if (this.hasAnimations(spec)) {
      deps.push('framer-motion@^10.16.0')
    }

    return deps
  }

  generatePropsInterface(component: ComponentSpec): string {
    if (!this.options.typescript) return ''

    const props = Object.keys(component.props || {})
    if (props.length === 0) return ''

    const propsInterface = props.map(prop => {
      const value = component.props[prop]
      const type = typeof value === 'string' ? 'string' : 
                   typeof value === 'number' ? 'number' :
                   typeof value === 'boolean' ? 'boolean' : 'any'
      return `  ${prop}: ${type}`
    }).join('\n')

    return `interface ${this.capitalizeFirst(component.type)}Props {\n${propsInterface}\n}`
  }

  generateEventHandlers(component: ComponentSpec): string {
    const events = component.props?.events || {}
    const handlers = Object.keys(events).map(event => {
      return `const handle${this.capitalizeFirst(event)} = () => {\n  // ${events[event]}\n}`
    })

    return handlers.join('\n\n')
  }

  generateLifecycleHooks(component: ComponentSpec): string {
    let hooks = ''

    if (component.props?.onMount) {
      hooks += `useEffect(() => {\n  // ${component.props.onMount}\n}, [])\n\n`
    }

    return hooks
  }

  private generatePageCode(spec: InterfaceSpec, imports: string[], components: string[]): string {
    const propsInterface = this.options.typescript ? `interface PageProps {}\n\n` : ''
    const isClient = this.options.framework === 'next' ? "'use client'\n\n" : ''
    
    return `${isClient}${imports.join('\n')}

${propsInterface}export default function ${this.capitalizeFirst(spec.name)}Page() {
  // Component state
  const [isLoaded, setIsLoaded] = useState(false)

  // Lifecycle
  useEffect(() => {
    setIsLoaded(true)
  }, [])

  // Component methods
  ${this.generatePageMethods(spec)}

  // Mock data for demo
  const features = [
    { id: 1, title: 'Fast', description: 'Lightning fast performance', icon: 'Zap' },
    { id: 2, title: 'Reliable', description: 'Rock solid reliability', icon: 'Shield' },
    { id: 3, title: 'Scalable', description: 'Scales with your needs', icon: 'TrendingUp' }
  ]

  const pricingPlans = [
    { id: 1, name: 'Starter', price: 9, ctaText: 'Start Free Trial' },
    { id: 2, name: 'Pro', price: 29, ctaText: 'Go Pro' },
    { id: 3, name: 'Enterprise', price: 99, ctaText: 'Contact Sales' }
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      ${this.generatePageContent(spec)}
    </div>
  )
}`
  }

  private generatePageContent(spec: InterfaceSpec): string {
    return spec.components.map(comp => 
      this.generateComponentJSX(comp, spec.theme)
    ).join('\n      ')
  }

  private generateComponents(components: ComponentSpec[]): string[] {
    return components.map(comp => this.generateComponent(comp, {}))
  }

  private generateStyles(spec: InterfaceSpec): string {
    if (this.options.styling === 'tailwind') {
      return `@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component styles */
.hero-gradient {
  background: linear-gradient(135deg, ${spec.theme.primaryColor || '#3b82f6'} 0%, ${spec.theme.secondaryColor || '#8b5cf6'} 100%);
}

.gradient-text {
  background: linear-gradient(135deg, ${spec.theme.primaryColor || '#3b82f6'} 0%, ${spec.theme.secondaryColor || '#8b5cf6'} 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}`
    }

    return `/* Component-specific styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Global transitions */
* {
  transition: all 0.2s ease;
}`
  }

  private generateComponentJSX(component: ComponentSpec, theme: any): string {
    const classes = this.generateTailwindClasses(component, theme)
    const responsiveClasses = this.generateResponsiveClasses(component).join(' ')
    const allClasses = [classes, responsiveClasses].filter(Boolean).join(' ')

    switch (component.type) {
      case 'hero':
        return `<section className="${allClasses} py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6 gradient-text">
            ${component.props?.title || 'Welcome to React App'}
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            ${component.props?.description || 'Build amazing applications with React'}
          </p>
          <button 
            className="bg-primary text-white px-8 py-3 rounded-lg hover:bg-primary/90 transition-colors" 
            onClick={handleCTAClick}
          >
            ${component.props?.ctaText || 'Get Started'}
          </button>
        </div>
      </section>`

      case 'features':
        return `<section className="${allClasses} py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            ${component.props?.title || 'Features'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature) => (
              <div key={feature.id} className="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="w-6 h-6 text-primary">{feature.icon}</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>`

      case 'pricing':
        return `<section className="${allClasses} py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            ${component.props?.title || 'Pricing'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricingPlans.map((plan) => (
              <div key={plan.id} className="border rounded-lg p-8 text-center hover:shadow-lg transition-shadow">
                <h3 className="text-2xl font-bold mb-4">{plan.name}</h3>
                <div className="text-4xl font-bold mb-6">
                  <span className="text-sm font-normal">$</span>{plan.price}
                  <span className="text-base font-normal text-gray-600">/month</span>
                </div>
                <button 
                  className="w-full bg-primary text-white py-3 rounded-lg hover:bg-primary/90 transition-colors"
                  onClick={() => handlePlanSelect(plan)}
                >
                  {plan.ctaText}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>`

      case 'button':
        return `<button 
        className="${allClasses} px-6 py-2 rounded-lg transition-colors"
        onClick={handleClick}
        disabled={${component.props?.disabled || false}}
      >
        ${component.props?.text || 'Button'}
      </button>`

      default:
        return `<div className="${allClasses}">
        {/* ${component.type} component */}
        ${component.children?.map(child => this.generateComponentJSX(child, theme)).join('\n        ') || ''}
      </div>`
    }
  }

  private generateHeroComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generateFeaturesComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generatePricingComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generateCTAComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generateButtonComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generateGenericComponent(component: ComponentSpec, theme: any): string {
    return this.generateComponentJSX(component, theme)
  }

  private generatePageMethods(spec: InterfaceSpec): string {
    return `// Page methods
  const handleCTAClick = () => {
    console.log('CTA clicked')
  }

  const handleClick = () => {
    console.log('Button clicked')
  }

  const handlePlanSelect = (plan: any) => {
    console.log('Plan selected:', plan)
  }`
  }

  private hasAnimations(spec: InterfaceSpec): boolean {
    return spec.components.some(comp => 
      comp.props?.animations || 
      comp.styling?.animations
    )
  }

  private capitalizeFirst(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1)
  }
}