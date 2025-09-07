import { InterfaceSpec, ComponentSpec, GeneratedCode, CodeGenerationOptions } from '@/types/builder'

/**
 * Core code generation engine
 */
export class CodeGenerator {
  private options: CodeGenerationOptions

  constructor(options: CodeGenerationOptions = {
    framework: 'next',
    styling: 'tailwind',
    typescript: true,
    accessibility: true,
    responsive: true
  }) {
    this.options = options
  }

  /**
   * Generate complete page code from interface specification
   */
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

  /**
   * Generate individual component code
   */
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
      default:
        return this.generateGenericComponent(component, theme)
    }
  }

  private generateImports(spec: InterfaceSpec): string[] {
    const baseImports = [
      "import React from 'react'",
      "import { motion } from 'framer-motion'"
    ]

    // Add conditional imports based on components used
    const componentTypes = spec.components.map(c => c.type)
    
    if (componentTypes.includes('hero') || componentTypes.includes('cta')) {
      baseImports.push("import { Button } from '@/components/ui/button'")
    }

    if (componentTypes.includes('features')) {
      baseImports.push("import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'")
    }

    return baseImports
  }

  private generatePageCode(spec: InterfaceSpec, imports: string[], components: string): string {
    return `${imports.join('\n')}

export default function ${this.toPascalCase(spec.name)}() {
  return (
    <div className="min-h-screen" style={{ 
      backgroundColor: '${spec.theme.backgroundColor}',
      color: '${spec.theme.textColor}',
      fontFamily: '${spec.theme.fontFamily}'
    }}>
${components}
    </div>
  )
}

// Theme configuration
export const theme = ${JSON.stringify(spec.theme, null, 2)}`
  }

  private generateComponents(components: ComponentSpec[]): string {
    return components.map(component => {
      return `      ${this.generateComponentJSX(component)}`
    }).join('\n\n')
  }

  private generateComponentJSX(component: ComponentSpec): string {
    const indentation = '      '
    
    switch (component.type) {
      case 'hero':
        return `<motion.section 
${indentation}  initial={{ opacity: 0, y: 20 }}
${indentation}  animate={{ opacity: 1, y: 0 }}
${indentation}  className="px-6 py-20 text-center bg-gradient-to-br from-blue-50 to-indigo-100"
${indentation}>
${indentation}  <div className="max-w-4xl mx-auto">
${indentation}    <h1 className="text-5xl font-bold mb-6">
${indentation}      ${component.props.title}
${indentation}    </h1>
${indentation}    <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
${indentation}      ${component.props.subtitle}
${indentation}    </p>
${indentation}    <Button className="px-8 py-3 text-lg font-semibold">
${indentation}      ${component.props.ctaText}
${indentation}    </Button>
${indentation}  </div>
${indentation}</motion.section>`

      case 'features':
        const features = component.props.features || []
        const featureItems = features.map((feature: any, index: number) => `
${indentation}      <Card key={${index}} className="text-center">
${indentation}        <CardHeader>
${indentation}          <div className="w-12 h-12 mx-auto mb-4 bg-blue-600 rounded-lg flex items-center justify-center">
${indentation}            <span className="text-white text-xl">${feature.icon || '✦'}</span>
${indentation}          </div>
${indentation}          <CardTitle>${feature.title}</CardTitle>
${indentation}        </CardHeader>
${indentation}        <CardContent>
${indentation}          <CardDescription>${feature.description}</CardDescription>
${indentation}        </CardContent>
${indentation}      </Card>`).join('')

        return `<motion.section 
${indentation}  initial={{ opacity: 0 }}
${indentation}  animate={{ opacity: 1 }}
${indentation}  className="px-6 py-16"
${indentation}>
${indentation}  <div className="max-w-6xl mx-auto">
${indentation}    <h2 className="text-3xl font-bold text-center mb-12">
${indentation}      ${component.props.title || 'Features'}
${indentation}    </h2>
${indentation}    <div className="grid md:grid-cols-3 gap-8">
${featureItems}
${indentation}    </div>
${indentation}  </div>
${indentation}</motion.section>`

      case 'pricing':
        return `<motion.section 
${indentation}  initial={{ opacity: 0 }}
${indentation}  animate={{ opacity: 1 }}
${indentation}  className="px-6 py-16 bg-gray-50"
${indentation}>
${indentation}  {/* Pricing component implementation */}
${indentation}</motion.section>`

      case 'cta':
        return `<motion.section 
${indentation}  initial={{ opacity: 0 }}
${indentation}  animate={{ opacity: 1 }}
${indentation}  className="px-6 py-20 text-center bg-blue-600"
${indentation}>
${indentation}  <div className="max-w-4xl mx-auto">
${indentation}    <h2 className="text-4xl font-bold text-white mb-6">
${indentation}      ${component.props.title}
${indentation}    </h2>
${indentation}    <p className="text-xl text-blue-100 mb-8">
${indentation}      ${component.props.subtitle}
${indentation}    </p>
${indentation}    <Button variant="secondary" className="px-8 py-3 text-lg font-semibold">
${indentation}      ${component.props.ctaText}
${indentation}    </Button>
${indentation}  </div>
${indentation}</motion.section>`

      default:
        return `{/* ${component.type} component */}`
    }
  }

  private generateHeroComponent(component: ComponentSpec, theme: any): string {
    return `// Hero Component Implementation`
  }

  private generateFeaturesComponent(component: ComponentSpec, theme: any): string {
    return `// Features Component Implementation`
  }

  private generatePricingComponent(component: ComponentSpec, theme: any): string {
    return `// Pricing Component Implementation`
  }

  private generateCTAComponent(component: ComponentSpec, theme: any): string {
    return `// CTA Component Implementation`
  }

  private generateGenericComponent(component: ComponentSpec, theme: any): string {
    return `// Generic Component Implementation for ${component.type}`
  }

  private generateStyles(spec: InterfaceSpec): string {
    return `/* Generated styles for ${spec.name} */
:root {
  --primary-color: ${spec.theme.primaryColor};
  --background-color: ${spec.theme.backgroundColor};
  --text-color: ${spec.theme.textColor};
  --font-family: ${spec.theme.fontFamily};
}

.theme-primary {
  color: var(--primary-color);
}

.theme-bg {
  background-color: var(--background-color);
}

.theme-text {
  color: var(--text-color);
}

.theme-font {
  font-family: var(--font-family);
}`
  }

  private getDependencies(spec: InterfaceSpec): string[] {
    const baseDeps = ['react', 'framer-motion']
    
    if (this.options.styling === 'tailwind') {
      baseDeps.push('tailwindcss')
    }

    // Add conditional dependencies based on components
    const componentTypes = spec.components.map(c => c.type)
    
    if (componentTypes.some(type => ['hero', 'features', 'pricing'].includes(type))) {
      baseDeps.push('@radix-ui/react-slot')
    }

    return baseDeps
  }

  private toPascalCase(str: string): string {
    return str.replace(/\w+/g, (w) => w[0].toUpperCase() + w.slice(1).toLowerCase()).replace(/\s+/g, '')
  }
}

/**
 * Template system for common patterns
 */
export class TemplateManager {
  static getLandingPageTemplate(): InterfaceSpec {
    return {
      id: 'landing-page-template',
      name: 'Landing Page',
      type: 'page',
      components: [
        {
          id: 'hero-1',
          type: 'hero',
          props: {
            title: 'Transform Your Business Today',
            subtitle: 'Discover the power of our innovative solution that drives real results',
            ctaText: 'Get Started Free',
            ctaVariant: 'primary'
          }
        },
        {
          id: 'features-1',
          type: 'features',
          props: {
            title: 'Why Choose Us',
            features: [
              {
                title: 'Lightning Fast',
                description: 'Blazing fast performance that scales with your business',
                icon: '⚡'
              },
              {
                title: 'Secure & Reliable',
                description: 'Enterprise-grade security with 99.9% uptime guarantee',
                icon: '🔒'
              },
              {
                title: '24/7 Support',
                description: 'Round-the-clock support from our expert team',
                icon: '🛟'
              }
            ]
          }
        },
        {
          id: 'pricing-1',
          type: 'pricing',
          props: {
            title: 'Simple, Transparent Pricing',
            plans: [
              {
                name: 'Starter',
                price: 29,
                features: ['5 Projects', 'Basic Support', 'Core Features'],
                featured: false
              },
              {
                name: 'Professional',
                price: 99,
                features: ['Unlimited Projects', 'Priority Support', 'Advanced Features', 'Analytics'],
                featured: true
              },
              {
                name: 'Enterprise',
                price: 299,
                features: ['Everything in Pro', 'Custom Integration', 'Dedicated Manager', 'SLA'],
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
            subtitle: 'Join thousands of satisfied customers today',
            ctaText: 'Start Your Free Trial'
          }
        }
      ],
      theme: {
        primaryColor: '#3b82f6',
        backgroundColor: '#ffffff',
        textColor: '#1f2937',
        fontFamily: 'Inter',
        borderRadius: '8px'
      }
    }
  }

  static getSaaSTemplate(): InterfaceSpec {
    return {
      id: 'saas-template',
      name: 'SaaS Landing',
      type: 'page',
      components: [
        {
          id: 'hero-saas',
          type: 'hero',
          props: {
            title: 'The Future of Productivity',
            subtitle: 'Streamline your workflow with our AI-powered platform',
            ctaText: 'Start Building',
            ctaVariant: 'primary'
          }
        }
      ],
      theme: {
        primaryColor: '#6366f1',
        backgroundColor: '#ffffff',
        textColor: '#1f2937',
        fontFamily: 'Inter'
      }
    }
  }
}